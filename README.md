# Mikrotik-Blacklist

[![List Health Checks](https://github.com/ranas-mukminov/Mikrotik-Blacklist/actions/workflows/list-health.yml/badge.svg)](https://github.com/ranas-mukminov/Mikrotik-Blacklist/actions/workflows/list-health.yml)

This is an actively maintained fork of [pwlgrzs/Mikrotik-Blacklist](https://github.com/pwlgrzs/Mikrotik-Blacklist), continuing development after the original author announced they could no longer support the project.

This repository provides regularly updated IP blocklists for MikroTik routers to block connections from known spam, criminal, and malicious networks.

## 🔄 Fork Status

The original project maintainer announced in their README:

> "Good day people, because of personal stuff going on I cannot support this project further, it's already been going "on its own" or a while. I am leaving this as is (meaning the script will be pushing changes until it's not). I suggest moving to more actively developed lists."

**This fork aims to be that actively developed list.** We continue maintaining the blocklists with:
- Bug fixes and quality improvements
- Automated testing and validation
- Clear documentation and reproducible generation
- Compatibility with the original project's usage patterns

## 📋 List Sources

The blocklists are automatically generated from multiple trusted sources:

| Source | Standard List | Light List | Description |
|--------|--------------|------------|-------------|
| Spamhaus DROP | ✅ | ✅ | Don't Route Or Peer List |
| Spamhaus EDROP | ✅ | ✅ | Extended DROP List |
| DShield | ✅ | ✅ | Recommended Block List |
| Blacklist.de | ✅ | ✅ | All Lists |
| Feodo Tracker | ✅ | ✅ | IP Blocklist |
| FireHOL Level1 | ✅ | ❌ | Large list, excluded from light |
| Tor Exit Nodes | ✅ | ❌ | Excluded from light |

Lists are updated automatically, respecting upstream source frequencies (typically daily).

## 📊 Standard vs Light Lists

### When to use which list?

**Standard List (`blacklist.rsc`):**
- ✅ Devices with **32MB+ flash/disk** (e.g., RB4011, hEX S, CCR series)
- ✅ You want maximum protection
- ✅ ~15,000-20,000 entries (may vary)
- ✅ Includes all available sources
- ⚠️ File size: ~4-5MB

**Light List (`blacklist-light.rsc`):**
- ✅ Devices with **16MB or less flash** (e.g., hEX, hEX PoE, hAP series)
- ✅ Limited storage or RAM
- ✅ ~5,000-10,000 entries (may vary)
- ✅ Core protection sources only
- ⚠️ File size: ~2-3MB

### ⚠️ Important Warnings

**Before installing on devices with limited flash:**
- Check available space: `/system resource print`
- Installing on devices with insufficient space (like hEX PoE with 16MB) **may cause issues**:
  - Inability to save other configurations
  - Router instability
  - **Use the light version for 16MB devices!**

**Performance considerations:**
- Large address lists can impact routing performance on lower-end devices
- Test on a non-production device first if possible
- Monitor CPU usage after installation

# READ THIS BEFORE GOING ANY FORWARD!

As of April 2023 blocklist has almost 5MB, installing this on a device with low disk space, such as HeX PoE, may (and almost certainly will) cause issues such as inability to save other settings if disk is full.  
If you have a device with 16MB disk space I suggest you use a light version of the list, it's also being updated but without heavy sources.

## 🚀 Quick Start - How to Install on MikroTik

### Installation Steps

1. **Download the installer script:**
   - For standard list (32MB+ devices): Download `install.rsc`
   - For light list (16MB devices): Download `install-light.rsc`

2. **Upload to your MikroTik device:**
   - Via WebFig/WinBox: Files section
   - Via FTP/SFTP to the router

3. **Import the script in terminal:**
   ```routeros
   /import install.rsc
   ```
   or
   ```routeros
   /import install-light.rsc
   ```

4. **Add firewall rule:**
   ```routeros
   /ip firewall raw add chain=prerouting action=drop in-interface-list=WAN log=no log-prefix="" src-address-list=pwlgrzs-blacklist
   ```
   *Note: Replace `WAN` with your actual WAN interface list name*

### What the installer does:

- Creates two scripts:
  - `pwlgrzs-blacklist-dl`: Downloads the latest blocklist
  - `pwlgrzs-blacklist-replace`: Updates the address list
- Creates two scheduled tasks that run weekly (every 7 days):
  - Downloads new list at 00:05
  - Imports new list at 00:10
- Removes itself after installation

### Automatic Updates

The lists update automatically every 7 days. You can manually trigger an update:

```routeros
/system script run pwlgrzs-blacklist-dl
# Wait a few minutes for download
/system script run pwlgrzs-blacklist-replace
```

## How to run this on MT
Run following to your MT device with not less that 7d schedule (sources are not updated more frequently anyway):  

1. Download install.rsc or install-light.rsc file and upload it to your device
2. In the Mikrotik terminal run: `/import install.rsc` or `/import install-light.rsc`
3. Enjoy!

You'll also need firewall rule:  
`/ip firewall raw add chain=prerouting action=drop in-interface-list=WAN log=no log-prefix="" src-address-list=pwlgrzs-blacklist`  
*Note: Replace WAN in in-interface-list with one you have configured*

I sometimes add updates and notes about the list [here](https://pawelgrzes.pl/posts/Mikrotik-Blocking-unwanted-connections-with-external-IP-list/).

## 🔧 List Generation and Sources

### Automated Generation

The blocklists are generated using `scripts/generate_blacklists.py`, which:
- Downloads lists from all configured sources
- Normalizes IP addresses and CIDR ranges
- Removes duplicates
- Sorts entries for deterministic diffs
- Validates list sizes and relationships
- Generates RouterOS-compatible `.rsc` files with headers documenting sources

### Running the Generator Locally

Requirements: Python 3.7+

```bash
# Generate both lists in current directory
python3 scripts/generate_blacklists.py

# Generate in specific directory
python3 scripts/generate_blacklists.py --output-dir ./output

# Dry run (validate sources without writing files)
python3 scripts/generate_blacklists.py --dry-run

# Custom size thresholds
python3 scripts/generate_blacklists.py --min-standard 2000 --min-light 1000
```

### Source Rate Limits

- **Update frequency**: Once per day recommended
- **Never** more frequent than every 6 hours
- Respect upstream source rate limits and terms of service
- The automatic scheduler runs weekly (every 7 days) by default

## 🐛 Troubleshooting

### Problem: "Light list larger than standard"

**This should not happen with this fork!** If you encounter this:

1. Check which version you're using:
   ```routeros
   /file print where name~"blacklist"
   ```

2. Verify list counts:
   ```routeros
   /ip firewall address-list print count-only where list=pwlgrzs-blacklist
   ```

3. Re-download and re-import the correct version for your device

If the problem persists, please [open an issue](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues).

### Problem: "List appears almost empty"

Possible causes:
- Download interrupted
- Source temporarily unavailable
- Incorrect import

**Solutions:**

1. Check the downloaded file size:
   ```routeros
   /file print where name~"blacklist"
   ```
   - Standard list should be ~4-5MB
   - Light list should be ~2-3MB

2. Manually re-download:
   ```routeros
   /system script run pwlgrzs-blacklist-dl
   ```

3. Check for errors in the log:
   ```routeros
   /log print where topics~"error"
   ```

4. If sources are down, the CI/CD system will catch this before publishing

### Problem: "Router running slow after installing list"

**Causes:**
- Too many firewall rules being evaluated
- Device has limited CPU/RAM
- Firewall rule placed in wrong chain

**Solutions:**

1. Use the **light list** instead of standard on lower-end devices

2. Ensure you're using the **raw** firewall chain (faster):
   ```routeros
   /ip firewall raw add chain=prerouting action=drop in-interface-list=WAN src-address-list=pwlgrzs-blacklist
   ```

3. Check CPU usage:
   ```routeros
   /system resource print
   ```

4. Consider using hardware offloading if available on your device

### Problem: "Can't save configuration - disk full"

**Cause:** Not enough space on device (common on 16MB devices with standard list)

**Solution:**

1. **Switch to light list immediately:**
   ```routeros
   /ip firewall address-list remove [find where list=pwlgrzs-blacklist]
   /file remove [find where name~"blacklist"]
   /system script remove [find where name~"blacklist"]
   /system scheduler remove [find where name~"blacklist"]
   ```

2. Install light version instead (see Quick Start)

3. Check free space:
   ```routeros
   /system resource print
   ```

## 🔒 Security Considerations

### What this blocklist does:
- ✅ Blocks known malicious networks
- ✅ Reduces spam and scanning attempts  
- ✅ Provides additional security layer

### What this blocklist does NOT do:
- ❌ Replace a proper firewall configuration
- ❌ Protect against zero-day attacks
- ❌ Guarantee 100% protection (false negatives possible)
- ❌ Prevent all unwanted traffic

### False Positives

Blocklists can occasionally include legitimate networks. If you experience connectivity issues:

1. Check if the destination is in the blocklist:
   ```routeros
   /ip firewall address-list print where address=X.X.X.X
   ```

2. Temporarily disable the rule to test:
   ```routeros
   /ip firewall raw disable [find where src-address-list=pwlgrzs-blacklist]
   ```

3. If confirmed, you can whitelist specific IPs/ranges (contact maintainer if it's a widespread issue)

## 🤝 Contributing

Contributions are welcome! Please:

1. Check existing [issues](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues) and [pull requests](https://github.com/ranas-mukminov/Mikrotik-Blacklist/pulls)
2. For bugs: provide MikroTik model, RouterOS version, and logs
3. For new sources: ensure they're reputable and regularly updated
4. Follow the code style in existing scripts
5. Test changes before submitting

## 📜 Changelog

### 2024 (This Fork - ranas-mukminov)
 - **November 2024**
   - 🔧 Fixed light vs standard list size inconsistency
   - 🤖 Added automated list generation with Python script
   - ✅ Implemented CI/CD health checks (GitHub Actions)
   - 📝 Updated documentation with troubleshooting and source details
   - 🔄 Fork created to continue active maintenance

### 2023 (Original Project - pwlgrzs)
 - 25.01.2023
   - rewritten blacklist script due to potential issue with filesize.
 - 17.09.2023
   - added danger.rulez.sk bruteforceblocker as source
   - added Tor exit nodes list
 - 17.09.2023
   - pfSense sources removed due to permanent 404
   - added FireHOL abusers source for standard list
 - 15.04.2023
   - Added light version of the list (without heavy pfSense sources) for small disk devices
   - Added light version installer
   - Installers now remove themselves
 - 12.04.2023
   - added pfSense sources (abuse, badguys, block)

## 📄 License

This project maintains the same license as the original [pwlgrzs/Mikrotik-Blacklist](https://github.com/pwlgrzs/Mikrotik-Blacklist) project.

## 🙏 Acknowledgments

- Original project by [@pwlgrzs](https://github.com/pwlgrzs)
- All upstream blocklist providers (Spamhaus, DShield, Blocklist.de, Feodo, FireHOL, Tor Project)
- MikroTik community

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ranas-mukminov/Mikrotik-Blacklist/discussions)
- **Original blog post**: [Mikrotik: Blocking unwanted connections](https://pawelgrzes.pl/posts/Mikrotik-Blocking-unwanted-connections-with-external-IP-list/)

---

**⚠️ Disclaimer**: This blocklist is provided as-is. Use at your own risk. Always test in a non-production environment first. The maintainers are not responsible for any connectivity issues, false positives, or other problems that may arise from using these lists.

