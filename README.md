# 🛡️ Mikrotik-Blacklist

[![List Health Checks](https://github.com/ranas-mukminov/Mikrotik-Blacklist/actions/workflows/list-health.yml/badge.svg)](https://github.com/ranas-mukminov/Mikrotik-Blacklist/actions/workflows/list-health.yml)
[![Security Audit](https://github.com/ranas-mukminov/Mikrotik-Blacklist/workflows/Security%20Audit/badge.svg)](https://github.com/ranas-mukminov/Mikrotik-Blacklist/actions/workflows/security.yml)
[![Code Quality](https://github.com/ranas-mukminov/Mikrotik-Blacklist/workflows/Code%20Quality/badge.svg)](https://github.com/ranas-mukminov/Mikrotik-Blacklist/actions/workflows/code-quality.yml)

Regularly updated IP blocklists for MikroTik routers to block connections from known spam, criminal, and malicious networks.

**Automated** | **Validated** | **Production-Ready** | **Community-Driven**

> This is an actively maintained fork of [pwlgrzs/Mikrotik-Blacklist](https://github.com/pwlgrzs/Mikrotik-Blacklist), continuing development after the original author announced they could no longer support the project.

---

## 📊 Quick Stats

| Metric | Standard List | Light List |
|--------|--------------|------------|
| **IP Entries** | ~15,000-20,000 | ~5,000-10,000 |
| **File Size** | ~4-5 MB | ~2-3 MB |
| **Sources** | 7 providers | 5 providers |
| **Update Frequency** | Weekly | Weekly |
| **Min Flash Required** | 32 MB | 16 MB |
| **Recommended Devices** | RB4011, hEX S, CCR | hEX, hAP, RB750 |

---

## 🔄 Fork Status

The original project maintainer announced:

> "Good day people, because of personal stuff going on I cannot support this project further... I suggest moving to more actively developed lists."

**This fork aims to be that actively developed list.** We continue maintaining the blocklists with:

- ✅ **Bug fixes** and quality improvements
- 🤖 **Automated testing** and validation
- 📖 **Clear documentation** and reproducible generation
- 🔄 **Regular updates** respecting upstream sources
- 🛠️ **Compatibility** with original usage patterns

---

## 🚀 Quick Start - Installation

### ⚡ Choose Your List

**📦 Standard List** (`install.rsc`) - For 32MB+ devices:
```routeros
/tool fetch url="https://raw.githubusercontent.com/ranas-mukminov/Mikrotik-Blacklist/main/install.rsc"
/import install.rsc
```

**💡 Light List** (`install-light.rsc`) - For 16MB devices:
```routeros
/tool fetch url="https://raw.githubusercontent.com/ranas-mukminov/Mikrotik-Blacklist/main/install-light.rsc"
/import install-light.rsc
```

### 🔥 Add Firewall Rule

```routeros
/ip firewall raw add chain=prerouting action=drop in-interface-list=WAN log=no log-prefix="" src-address-list=pwlgrzs-blacklist
```

> **Note:** Replace `WAN` with your actual WAN interface list name

### ✅ What Gets Installed

The installer automatically creates:

- 📥 **`pwlgrzs-blacklist-dl`** - Script to download latest blocklist
- 🔄 **`pwlgrzs-blacklist-replace`** - Script to update address list
- ⏰ **Two scheduled tasks** running weekly:
  - Downloads new list at 00:05
  - Imports new list at 00:10
- 🧹 **Self-cleanup** - Installer removes itself after setup

---

## 📋 Blocklist Sources

The blocklists are automatically generated from multiple trusted sources:

| Source | Standard | Light | Description |
|--------|----------|-------|-------------|
| 🛡️ **Spamhaus DROP** | ✅ | ✅ | Don't Route Or Peer List |
| 🛡️ **Spamhaus EDROP** | ✅ | ✅ | Extended DROP List |
| 🔒 **DShield** | ✅ | ✅ | SANS Recommended Block List |
| 🚫 **Blacklist.de** | ✅ | ✅ | All Attack Lists |
| 🦠 **Feodo Tracker** | ✅ | ✅ | Botnet C&C IP Blocklist |
| 🔥 **FireHOL Level1** | ✅ | ❌ | Large list, excluded from light |
| 🧅 **Tor Exit Nodes** | ✅ | ❌ | Excluded from light |

**Update Schedule:** Lists are updated automatically every 7 days, respecting upstream source frequencies.

---

## 🎯 Standard vs Light Lists

### 📦 Standard List (`blacklist.rsc`)

**Use when you have:**
- ✅ Devices with **32MB+ flash/disk** (e.g., RB4011, hEX S, CCR series)
- ✅ Need for maximum protection
- ✅ ~15,000-20,000 IP entries
- ✅ All available blocklist sources
- 📏 File size: ~4-5MB

**Best for:** Production routers, enterprise networks, high-security environments

### 💡 Light List (`blacklist-light.rsc`)

**Use when you have:**
- ✅ Devices with **16MB or less flash** (e.g., hEX, hEX PoE, hAP series)
- ✅ Limited storage or RAM constraints
- ✅ ~5,000-10,000 IP entries
- ✅ Core protection sources only
- 📏 File size: ~2-3MB

**Best for:** Home networks, small office routers, resource-constrained devices

---

## ⚠️ Important Warnings

### 💾 Storage Requirements

**Before installing, check available space:**
```routeros
/system resource print
```

**Installing on devices with insufficient space may cause:**
- ❌ Inability to save configurations
- ❌ Router instability
- ❌ Flash memory exhaustion
- ⚠️ **Always use light version for 16MB devices!**

### ⚡ Performance Considerations

- Large address lists can impact routing performance on lower-end devices
- Test on non-production device first if possible
- Monitor CPU usage after installation:
  ```routeros
  /system resource print
  ```

---

## 🔄 Manual Updates

The lists update automatically every 7 days. To manually trigger an update:

```routeros
# Download latest list
/system script run pwlgrzs-blacklist-dl

# Wait a few minutes for download to complete

# Import new list
/system script run pwlgrzs-blacklist-replace
```

**Check current list size:**
```routeros
/ip firewall address-list print count-only where list=pwlgrzs-blacklist
```

---

## 🔧 List Generation & Development

### 🤖 Automated Generation

The blocklists are generated using `scripts/generate_blacklists.py`:

- 📥 Downloads lists from all configured sources
- 🔄 Normalizes IP addresses and CIDR ranges
- 🗑️ Removes duplicates
- 📊 Sorts entries for deterministic diffs
- ✅ Validates list sizes and relationships
- 📝 Generates RouterOS-compatible `.rsc` files

### 🛠️ Running Generator Locally

**Requirements:** Python 3.7+

```bash
# Generate both lists
python3 scripts/generate_blacklists.py

# Generate in specific directory
python3 scripts/generate_blacklists.py --output-dir ./output

# Dry run (validate sources without writing)
python3 scripts/generate_blacklists.py --dry-run

# Custom size thresholds
python3 scripts/generate_blacklists.py --min-standard 2000 --min-light 1000
```

### 📡 Source Rate Limits

- ⏰ **Update frequency**: Once per day recommended
- 🚫 **Never** more frequent than every 6 hours
- 🤝 Respect upstream source rate limits and terms of service
- 📅 Automatic scheduler runs weekly (every 7 days) by default

---

## 🐛 Troubleshooting

### Problem: "Light list larger than standard"

**This should not happen with this fork!** If encountered:

1. Check version:
   ```routeros
   /file print where name~"blacklist"
   ```

2. Verify list counts:
   ```routeros
   /ip firewall address-list print count-only where list=pwlgrzs-blacklist
   ```

3. Re-download correct version

If problem persists: [Open an issue](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues)

### Problem: "List appears almost empty"

**Possible causes:** Download interrupted, source unavailable, incorrect import

**Solutions:**

1. Check file size:
   ```routeros
   /file print where name~"blacklist"
   ```
   Expected: Standard ~4-5MB, Light ~2-3MB

2. Manually re-download:
   ```routeros
   /system script run pwlgrzs-blacklist-dl
   ```

3. Check error logs:
   ```routeros
   /log print where topics~"error"
   ```

### Problem: "Router running slow after installing"

**Causes:** Too many firewall rules, limited resources, wrong firewall chain

**Solutions:**

1. **Use light list** on lower-end devices

2. **Ensure using raw firewall chain** (faster):
   ```routeros
   /ip firewall raw add chain=prerouting action=drop in-interface-list=WAN src-address-list=pwlgrzs-blacklist
   ```

3. **Check CPU usage:**
   ```routeros
   /system resource print
   ```

4. **Enable hardware offloading** if available

### Problem: "Can't save configuration - disk full"

**Cause:** Insufficient space (common on 16MB devices with standard list)

**Solution - Switch to light list:**

```routeros
# Remove current blocklist
/ip firewall address-list remove [find where list=pwlgrzs-blacklist]
/file remove [find where name~"blacklist"]
/system script remove [find where name~"blacklist"]
/system scheduler remove [find where name~"blacklist"]

# Install light version instead (see Quick Start)
```

**Check free space:**
```routeros
/system resource print
```

---

## 🔒 Security Considerations

### ✅ What This Blocklist Does

- 🛡️ Blocks known malicious networks
- 📉 Reduces spam and scanning attempts  
- 🔐 Provides additional security layer
- 🎯 Stops connections from known bad actors

### ❌ What This Blocklist Does NOT Do

- 🚫 Replace proper firewall configuration
- 🚫 Protect against zero-day attacks
- 🚫 Guarantee 100% protection (false negatives possible)
- 🚫 Prevent all unwanted traffic
- 🚫 Block sophisticated targeted attacks

### ⚠️ False Positives

Blocklists can occasionally include legitimate networks. If you experience connectivity issues:

1. **Check if destination is blocked:**
   ```routeros
   /ip firewall address-list print where address=X.X.X.X
   ```

2. **Temporarily disable rule to test:**
   ```routeros
   /ip firewall raw disable [find where src-address-list=pwlgrzs-blacklist]
   ```

3. **Whitelist specific IPs if needed** (contact maintainer for widespread issues)

---

## 👨‍💻 Professional Services – run-as-daemon.ru

**Professional MikroTik & network security services by [run-as-daemon.ru](https://run-as-daemon.ru)**

This project is maintained by the DevSecOps / SRE engineer behind run-as-daemon.ru.

### 💼 Services Offered:

- 🛡️ **MikroTik Security Hardening**: Complete router security audits and configuration
- 🔧 **Network Architecture Design**: Enterprise-grade network planning and implementation
- 🚨 **Firewall Configuration**: Advanced firewall rules, IDS/IPS integration
- 📊 **Monitoring & Alerting**: Grafana, Prometheus, logging infrastructure
- 🎓 **Training & Workshops**: MikroTik, network security, best practices
- 🔄 **Automated Security**: CI/CD for network configurations, GitOps workflows
- 💪 **24/7 Support Packages**: Production environment monitoring and incident response

### 📞 Contact for Consulting:

**Website:** [run-as-daemon.ru](https://run-as-daemon.ru)

*"Defense by design. Speed by default"* — Security-first architecture with performance optimization

---

## 🤝 Contributing

Contributions are welcome! Please:

1. 🔍 Check existing [issues](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues) and [pull requests](https://github.com/ranas-mukminov/Mikrotik-Blacklist/pulls)
2. 🐛 **For bugs:** Provide MikroTik model, RouterOS version, and logs
3. 📥 **For new sources:** Ensure they're reputable and regularly updated
4. 💻 Follow the code style in existing scripts
5. ✅ Test changes before submitting

**Development Guidelines:**
- Write clear commit messages
- Keep PRs focused on single concern
- Add documentation for new features
- Validate generated lists before submitting

---

## 📜 Changelog

### 2024 (This Fork - ranas-mukminov)

**November 2024:**
- 🔧 Fixed light vs standard list size inconsistency
- 🤖 Added automated list generation with Python script
- ✅ Implemented CI/CD health checks (GitHub Actions)
- 📝 Updated comprehensive documentation
- 🔄 Fork created to continue active maintenance

### 2023 (Original Project - pwlgrzs)

**January 2023:**
- Rewritten blacklist script due to potential filesize issue

**September 2023:**
- Added danger.rulez.sk bruteforceblocker as source
- Added Tor exit nodes list
- pfSense sources removed (permanent 404)
- Added FireHOL abusers source for standard list

**April 2023:**
- Added light version for small disk devices
- Added light version installer
- Installers now remove themselves
- Added pfSense sources (abuse, badguys, block)

---

## 📄 License

This project maintains the same license as the original [pwlgrzs/Mikrotik-Blacklist](https://github.com/pwlgrzs/Mikrotik-Blacklist) project.

---

## 🙏 Acknowledgments

- 👨‍💻 Original project by [@pwlgrzs](https://github.com/pwlgrzs)
- 🛡️ All upstream blocklist providers:
  - [Spamhaus](https://www.spamhaus.org/)
  - [DShield](https://www.dshield.org/)
  - [Blocklist.de](https://www.blocklist.de/)
  - [Feodo Tracker](https://feodotracker.abuse.ch/)
  - [FireHOL](https://iplists.firehol.org/)
  - [Tor Project](https://www.torproject.org/)
- 💬 MikroTik community

---

## 📮 Support

**Community Support:**
- 📖 **Documentation**: This README
- 🐛 **Issues**: [GitHub Issues](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/ranas-mukminov/Mikrotik-Blacklist/discussions)
- 📝 **Original blog**: [Mikrotik: Blocking unwanted connections](https://pawelgrzes.pl/posts/Mikrotik-Blocking-unwanted-connections-with-external-IP-list/)

**Professional Support:**
- MikroTik security audits and hardening
- Custom blocklist generation and management
- Enterprise network security consulting
- Incident response and threat mitigation
- Training and knowledge transfer
- 24/7 production environment support

**Contact:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

**Maintained by**: [Ranas Mukminov](https://github.com/ranas-mukminov) | **Original author**: [@pwlgrzs](https://github.com/pwlgrzs)

**Made with ❤️ for the MikroTik community**

**Professional MikroTik & Network Security:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

**⚠️ Disclaimer**: This blocklist is provided as-is. Use at your own risk. Always test in a non-production environment first. The maintainers are not responsible for any connectivity issues, false positives, or other problems that may arise from using these lists.
