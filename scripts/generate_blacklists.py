#!/usr/bin/env python3
"""
Mikrotik Blacklist Generator

This script downloads IP blocklists from various sources, normalizes them,
removes duplicates, and generates RouterOS script files for both standard
and light versions.

The light version excludes heavy sources to support devices with limited flash.
"""

import argparse
import ipaddress
import logging
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Source definitions
# Format: (name, url, included_in_standard, included_in_light, description)
SOURCES = [
    (
        "Spamhaus DROP",
        "https://www.spamhaus.org/drop/drop.txt",
        True,
        True,
        "Spamhaus Don't Route Or Peer List"
    ),
    (
        "Spamhaus EDROP",
        "https://www.spamhaus.org/drop/edrop.txt",
        True,
        True,
        "Spamhaus Extended DROP List"
    ),
    (
        "DShield",
        "https://www.dshield.org/block.txt",
        True,
        True,
        "DShield Recommended Block List"
    ),
    (
        "Blacklist.de",
        "https://lists.blocklist.de/lists/all.txt",
        True,
        True,
        "Blocklist.de All Lists"
    ),
    (
        "Feodo Tracker",
        "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
        True,
        True,
        "Feodo Tracker IP Blocklist"
    ),
    (
        "FireHOL Level1",
        "https://raw.githubusercontent.com/ktsaou/blocklist-ipsets/master/firehol_level1.netset",
        True,
        False,
        "FireHOL Level1 - Excluded from light due to size"
    ),
    (
        "Tor Exit Nodes",
        "https://check.torproject.org/torbulkexitlist",
        True,
        False,
        "Tor Exit Nodes - Excluded from light"
    ),
]

# Configuration
MIN_STANDARD_SIZE = 1000  # Minimum number of IPs in standard list
MIN_LIGHT_SIZE = 500      # Minimum number of IPs in light list
USER_AGENT = "Mozilla/5.0 (compatible; Mikrotik-Blacklist-Generator/2.0)"


def download_source(name: str, url: str) -> Tuple[str, List[str]]:
    """
    Download a blocklist source and return its content as lines.
    
    Args:
        name: Human-readable name of the source
        url: URL to download from
        
    Returns:
        Tuple of (name, list of lines)
        
    Raises:
        Exception: If download fails
    """
    logger.info(f"Downloading {name} from {url}")
    
    try:
        req = Request(url, headers={'User-Agent': USER_AGENT})
        with urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8', errors='ignore')
            lines = content.splitlines()
            logger.info(f"Downloaded {name}: {len(lines)} lines")
            return name, lines
    except (URLError, HTTPError) as e:
        logger.error(f"Failed to download {name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error downloading {name}: {e}")
        raise


def is_valid_ip_or_cidr(address: str) -> bool:
    """
    Check if a string is a valid IP address or CIDR notation.
    
    Args:
        address: String to check
        
    Returns:
        True if valid IP or CIDR, False otherwise
    """
    try:
        ipaddress.ip_network(address, strict=False)
        return True
    except ValueError:
        return False


def normalize_ip(line: str) -> str | None:
    """
    Extract and normalize IP address or CIDR from a line.
    
    Handles various formats:
    - Plain IP or CIDR
    - Lines with comments (# or ;)
    - Tab-separated fields (like DShield format)
    
    Args:
        line: Raw line from source
        
    Returns:
        Normalized IP/CIDR string or None if invalid
    """
    # Skip empty lines and comments
    line = line.strip()
    if not line or line.startswith('#') or line.startswith(';'):
        return None
    
    # Remove inline comments
    if '#' in line:
        line = line.split('#')[0].strip()
    if ';' in line:
        line = line.split(';')[0].strip()
    
    # Handle tab-separated format (DShield)
    if '\t' in line:
        parts = line.split('\t')
        # DShield format: IP\tsubnet_mask\tcount
        if len(parts) >= 2:
            ip = parts[0].strip()
            mask = parts[1].strip()
            try:
                # Convert subnet mask to CIDR
                cidr_bits = sum([bin(int(x)).count('1') for x in mask.split('.')])
                line = f"{ip}/{cidr_bits}"
            except:
                line = ip
        else:
            line = parts[0].strip()
    
    # Extract first word (should be IP or CIDR)
    words = line.split()
    if not words:
        return None
    
    candidate = words[0].strip()
    
    # Validate
    if is_valid_ip_or_cidr(candidate):
        # Normalize CIDR notation
        try:
            network = ipaddress.ip_network(candidate, strict=False)
            return str(network)
        except ValueError:
            return None
    
    return None


def process_sources(sources: List[Tuple], include_light_only: bool = False) -> Tuple[Set[str], Dict[str, int]]:
    """
    Download and process all sources.
    
    Args:
        sources: List of source tuples
        include_light_only: If True, only include sources marked for light list
        
    Returns:
        Tuple of (set of normalized IPs, dict of source name to count)
    """
    all_ips = set()
    source_counts = defaultdict(int)
    failed_sources = []
    
    for name, url, in_standard, in_light, description in sources:
        # Skip sources not in the desired list
        if include_light_only and not in_light:
            logger.info(f"Skipping {name} (not included in light list)")
            continue
        if not include_light_only and not in_standard:
            logger.info(f"Skipping {name} (not included in standard list)")
            continue
        
        try:
            _, lines = download_source(name, url)
            
            # Normalize and collect IPs
            source_ips = set()
            for line in lines:
                normalized = normalize_ip(line)
                if normalized:
                    source_ips.add(normalized)
            
            count = len(source_ips)
            source_counts[name] = count
            all_ips.update(source_ips)
            logger.info(f"Processed {name}: {count} unique IPs")
            
        except Exception as e:
            logger.error(f"Failed to process {name}: {e}")
            failed_sources.append(name)
    
    if failed_sources:
        logger.warning(f"Some sources failed: {', '.join(failed_sources)}")
    
    return all_ips, dict(source_counts)


def generate_rsc_file(
    ips: Set[str],
    output_path: Path,
    list_type: str,
    source_counts: Dict[str, int]
) -> None:
    """
    Generate RouterOS script file.
    
    Args:
        ips: Set of IP addresses/CIDRs
        output_path: Path to output file
        list_type: "standard" or "light"
        source_counts: Dictionary of source name to IP count
    """
    logger.info(f"Generating {list_type} list with {len(ips)} IPs to {output_path}")
    
    # Sort IPs for deterministic output
    sorted_ips = sorted(ips, key=lambda x: ipaddress.ip_network(x, strict=False))
    
    # Generate header
    timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
    header = f"""# Generated on {timestamp}
# Mikrotik Blacklist ({list_type})
# Total entries: {len(sorted_ips)}
#
# Sources:
"""
    
    for source_name, count in sorted(source_counts.items()):
        header += f"#   - {source_name}: {count} entries\n"
    
    header += "#\n# This list is generated automatically by scripts/generate_blacklists.py\n# Do not edit manually.\n"
    
    # Generate IP list in RouterOS format
    with open(output_path, 'w') as f:
        f.write(header)
        f.write(":local ips { \\\n")
        
        for i, ip in enumerate(sorted_ips):
            # Last entry doesn't have semicolon
            if i < len(sorted_ips) - 1:
                f.write(f'{ "{"}"{ip}"{ "}"};\\\n')
            else:
                f.write(f'{ "{"}"{ip}"{ "}"};\\\n')
        
        f.write("}\n")
        f.write(":foreach i in=$ips do={\n")
        f.write('  /ip firewall address-list add list=pwlgrzs-blacklist address=$i\n')
        f.write("}\n")
    
    logger.info(f"Successfully generated {output_path}")


def validate_lists(standard_count: int, light_count: int, min_standard: int, min_light: int) -> None:
    """
    Validate generated lists meet requirements.
    
    Args:
        standard_count: Number of IPs in standard list
        light_count: Number of IPs in light list
        min_standard: Minimum required IPs in standard list
        min_light: Minimum required IPs in light list
        
    Raises:
        ValueError: If validation fails
    """
    errors = []
    
    # Check minimum sizes
    if standard_count < min_standard:
        errors.append(
            f"Standard list too small: {standard_count} < {min_standard} (minimum)"
        )
    
    if light_count < min_light:
        errors.append(
            f"Light list too small: {light_count} < {min_light} (minimum)"
        )
    
    # Check that light list is not larger than standard
    if light_count > standard_count:
        errors.append(
            f"Light list larger than standard: {light_count} > {standard_count}"
        )
    
    if errors:
        for error in errors:
            logger.error(error)
        raise ValueError("List validation failed:\n" + "\n".join(errors))
    
    logger.info("✓ All validation checks passed")
    logger.info(f"  Standard list: {standard_count} entries")
    logger.info(f"  Light list: {light_count} entries")
    logger.info(f"  Difference: {standard_count - light_count} entries")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Mikrotik blacklist files from various sources"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory for generated files (default: current directory)"
    )
    parser.add_argument(
        "--min-standard",
        type=int,
        default=MIN_STANDARD_SIZE,
        help=f"Minimum IPs in standard list (default: {MIN_STANDARD_SIZE})"
    )
    parser.add_argument(
        "--min-light",
        type=int,
        default=MIN_LIGHT_SIZE,
        help=f"Minimum IPs in light list (default: {MIN_LIGHT_SIZE})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Download and process sources without writing files"
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("=" * 60)
        logger.info("Mikrotik Blacklist Generator")
        logger.info("=" * 60)
        
        # Process standard list
        logger.info("\n--- Processing STANDARD list ---")
        standard_ips, standard_counts = process_sources(
            [(n, u, s, l, d) for n, u, s, l, d in SOURCES if s],
            include_light_only=False
        )
        
        # Process light list
        logger.info("\n--- Processing LIGHT list ---")
        light_ips, light_counts = process_sources(
            [(n, u, s, l, d) for n, u, s, l, d in SOURCES if l],
            include_light_only=True
        )
        
        # Validate
        logger.info("\n--- Validating lists ---")
        validate_lists(
            len(standard_ips),
            len(light_ips),
            args.min_standard,
            args.min_light
        )
        
        if args.dry_run:
            logger.info("\n--- Dry run mode: skipping file generation ---")
            return 0
        
        # Generate files
        logger.info("\n--- Generating files ---")
        standard_path = args.output_dir / "blacklist.rsc"
        light_path = args.output_dir / "blacklist-light.rsc"
        
        generate_rsc_file(standard_ips, standard_path, "standard", standard_counts)
        generate_rsc_file(light_ips, light_path, "light", light_counts)
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ Generation completed successfully")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"\n✗ Generation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
