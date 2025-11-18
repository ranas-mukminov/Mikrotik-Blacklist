# Scripts Directory

This directory contains utility scripts for maintaining the Mikrotik-Blacklist project.

## generate_blacklists.py

Python script that generates the `blacklist.rsc` and `blacklist-light.rsc` files from upstream sources.

### Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

### Usage

```bash
# Generate both lists in the repository root
python3 scripts/generate_blacklists.py

# Generate in a specific directory
python3 scripts/generate_blacklists.py --output-dir /path/to/output

# Dry run (validate sources without writing files)
python3 scripts/generate_blacklists.py --dry-run

# Custom minimum size thresholds
python3 scripts/generate_blacklists.py --min-standard 2000 --min-light 1000
```

### What it does

1. **Downloads** blocklists from configured sources:
   - Spamhaus DROP & EDROP
   - DShield
   - Blacklist.de
   - Feodo Tracker
   - FireHOL Level1 (standard only)
   - Tor Exit Nodes (standard only)

2. **Normalizes** IP addresses and CIDR ranges:
   - Handles various input formats
   - Converts subnet masks to CIDR notation
   - Removes comments and invalid entries

3. **Deduplicates** entries across all sources

4. **Validates** the results:
   - Checks minimum size thresholds
   - Ensures light list ≤ standard list
   - Fails if lists are suspiciously small

5. **Generates** RouterOS script files:
   - Adds informative headers with source counts
   - Sorts entries deterministically
   - Formats for MikroTik RouterOS import

### Configuration

Source configuration is in the script itself (SOURCES list). To modify:

1. Edit `scripts/generate_blacklists.py`
2. Update the `SOURCES` list with format:
   ```python
   (name, url, in_standard, in_light, description)
   ```
3. Test with `--dry-run` before committing

### Error Handling

- If sources fail to download, the script logs errors and continues
- If too many sources fail, validation will catch the undersized list
- The script exits with code 1 on failure (suitable for CI/CD)

### CI/CD Integration

The script is designed to be used in GitHub Actions:

```yaml
- name: Generate lists
  run: python3 scripts/generate_blacklists.py --output-dir .
```

See `.github/workflows/list-health.yml` for the complete CI configuration.
