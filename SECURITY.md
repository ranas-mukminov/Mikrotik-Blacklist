# Security Policy

## Supported Versions

This project is actively maintained. Security updates are applied to the latest version.

| Version | Supported          |
| ------- | ------------------ |
| Latest (main branch) | :white_check_mark: |
| Older commits | :x: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

### For Security Issues

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please report security issues privately:

1. **Email**: Contact [@ranas-mukminov](https://github.com/ranas-mukminov) through GitHub
2. **GitHub Security Advisory**: Use the [Security Advisories](https://github.com/ranas-mukminov/Mikrotik-Blacklist/security/advisories) feature

### What to Include

Please provide:

- **Description** of the vulnerability
- **Impact** assessment (what could an attacker do?)
- **Steps to reproduce** the issue
- **Affected versions** (if known)
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix timeline**: Depends on severity
  - Critical: As soon as possible (hours to days)
  - High: Within 1-2 weeks
  - Medium/Low: Next regular release
- **Disclosure**: After fix is deployed and users have time to update

## Security Considerations

### Using This Blocklist

This blocklist is a **security enhancement**, not a complete security solution:

✅ **It provides**:
- Additional layer of protection
- Blocks known malicious networks
- Reduces attack surface

❌ **It does NOT**:
- Replace proper firewall rules
- Guarantee 100% protection
- Prevent zero-day attacks
- Protect against all threats

### Risks and Limitations

1. **False Positives**
   - Legitimate services might be blocked
   - Shared IP spaces can affect innocent users
   - Always have a rollback plan

2. **False Negatives**
   - Not all malicious IPs are listed
   - Attackers can use unlisted IPs
   - Lists have update lag

3. **Performance Impact**
   - Large address lists consume memory
   - Can impact routing performance on low-end devices
   - Test before deploying to production

4. **Availability**
   - If GitHub or source lists are unavailable, updates fail
   - Keep previous version as backup
   - Don't rely solely on automatic updates

## Best Practices

### Secure Deployment

1. **Test First**
   ```routeros
   # Test on non-production device first
   # Monitor for false positives
   # Verify performance impact
   ```

2. **Backup Configuration**
   ```routeros
   /export file=backup-before-blacklist
   ```

3. **Use Proper Firewall Rules**
   ```routeros
   # Use 'raw' chain for better performance
   /ip firewall raw add chain=prerouting action=drop \
       in-interface-list=WAN \
       src-address-list=pwlgrzs-blacklist \
       comment="Block malicious networks"
   ```

4. **Monitor Logs**
   ```routeros
   # Enable logging to see what's being blocked
   /ip firewall raw set [find where src-address-list=pwlgrzs-blacklist] log=yes log-prefix="BLACKLIST-DROP"
   ```

5. **Whitelist Critical IPs**
   ```routeros
   # Create whitelist for important IPs
   /ip firewall address-list add list=whitelist address=x.x.x.x
   
   # Add accept rule BEFORE blacklist rule
   /ip firewall raw add chain=prerouting action=accept \
       src-address-list=whitelist \
       place-before=[find where src-address-list=pwlgrzs-blacklist]
   ```

### Secure Updates

1. **Use HTTPS**
   - All installer scripts use HTTPS mode
   - Verifies SSL certificates

2. **Regular Updates**
   - Default 7-day schedule is reasonable
   - Don't update more than once per day

3. **Validate After Update**
   ```routeros
   # Check list count after update
   /ip firewall address-list print count-only where list=pwlgrzs-blacklist
   
   # Should be thousands, not zero or suspiciously small
   ```

## Vulnerability Disclosure Policy

### Our Commitments

- **Timely response** to security reports
- **Transparent communication** with reporters
- **Credit** to reporters (unless anonymity requested)
- **Responsible disclosure** timeline (typically 90 days)

### Coordinated Disclosure

1. Reporter notifies maintainers privately
2. Maintainers confirm and assess vulnerability
3. Fix is developed and tested
4. Fix is deployed to main branch
5. Security advisory is published
6. Credit given to reporter (if desired)

## Known Security Considerations

### By Design

1. **List Generation**
   - Sources are fetched over HTTPS
   - No authentication required (public lists)
   - Source availability is not guaranteed

2. **MikroTik Installation**
   - Installers modify firewall configuration
   - Requires admin access to router
   - Uses scheduler for automatic updates

3. **Storage**
   - Lists stored in plaintext on router
   - No encryption (not sensitive data)
   - Accessible to all admin users

### Mitigations

- CI/CD validation prevents malformed lists
- Minimum size checks prevent empty lists
- HTTPS ensures integrity during download
- Version control provides audit trail

## Additional Resources

- [MikroTik Security Best Practices](https://wiki.mikrotik.com/wiki/Manual:Securing_Your_Router)
- [RouterOS Firewall Documentation](https://wiki.mikrotik.com/wiki/Manual:IP/Firewall)
- [Original Project](https://github.com/pwlgrzs/Mikrotik-Blacklist)

## Contact

For non-security issues, use [GitHub Issues](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues).

---

**Remember**: Security is a continuous process, not a one-time setup. Stay informed, keep your systems updated, and always have a backup plan.
