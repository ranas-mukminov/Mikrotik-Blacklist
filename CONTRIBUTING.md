# Contributing to Mikrotik-Blacklist

Thank you for your interest in contributing to this project! This fork aims to provide an actively maintained, high-quality MikroTik blocklist.

## Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ➕ Propose new blocklist sources
- ✅ Help with testing and validation

## Before You Start

1. Check [existing issues](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues) to avoid duplicates
2. For major changes, open an issue first to discuss your approach
3. Ensure your contribution aligns with project goals (stability, safety, quality)

## Pull Request Guidelines

### General Rules

- **Keep PRs focused**: One bug fix or feature per PR
- **Small changes are better**: Easier to review and merge
- **Test your changes**: Verify they work as expected
- **Follow existing code style**: Match the patterns you see in the codebase
- **Update documentation**: If your change affects usage, update README.md

### For Code Changes

1. **Branch naming**: Use descriptive names
   - `feature/add-new-source`
   - `fix/light-count-issue`
   - `docs/update-troubleshooting`

2. **Commit messages**: Be clear and descriptive
   ```
   Add DShield Recommended Block List source
   
   - Downloads from dshield.org/block.txt
   - Handles tab-separated format
   - Includes in both standard and light lists
   ```

3. **Testing requirements**:
   - Run the generator script: `python3 scripts/generate_blacklists.py --dry-run`
   - Verify RouterOS script syntax (balanced braces, proper formatting)
   - If modifying CI: test workflow locally or in a fork first

### For RouterOS Scripts (*.rsc)

- **Safety first**: Never commit destructive operations without clear warnings
- **Comment dangerous operations**: `:execute`, `/file remove`, etc. need explanations
- **Maintain compatibility**: Don't break existing installer behavior
- **No secrets**: Never commit passwords, tokens, or keys

### For Blocklist Sources

When proposing a new source:

1. **Verify reputation**: Source must be trustworthy and maintained
2. **Check update frequency**: Should update at least weekly
3. **Provide details**:
   - Source name and URL
   - Maintainer/organization
   - Update frequency
   - Approximate size (number of IPs/CIDRs)
   - Format details (if non-standard)
4. **Specify list inclusion**: Standard, light, or both?
5. **Test it**: Run generator with your new source

Example:
```python
(
    "Example BlockList",
    "https://example.com/blocklist.txt",
    True,   # Include in standard
    False,  # Exclude from light (too large)
    "Example org's malicious IP list - Updated daily"
),
```

## Code Style

### Python (scripts/generate_blacklists.py)

- Follow PEP 8 style guide
- Use type hints for function signatures
- Add docstrings for functions
- Keep functions focused and testable
- Use descriptive variable names

### Shell Scripts (if any)

- Use POSIX-compatible syntax when possible
- Quote variables to prevent word splitting
- Check exit codes: `command || handle_error`
- Add comments for non-obvious operations

### RouterOS Scripts (*.rsc)

- Use consistent indentation (2 or 4 spaces)
- Add comments for complex logic
- Group related commands
- Use meaningful variable names (`:local myVar` not `:local x`)

## Documentation Style

### README and Docs

- Use clear, concise language
- Provide examples for complex operations
- Structure with headers and lists
- Test all commands and code snippets
- Add troubleshooting for common issues

### Code Comments

- Explain *why*, not *what* (code shows what)
- Comment non-obvious decisions
- Update comments when code changes
- Remove outdated comments

## Testing

### Manual Testing

Before submitting:

1. Run the generator:
   ```bash
   python3 scripts/generate_blacklists.py --dry-run
   ```

2. Check generated files (if generating):
   ```bash
   python3 scripts/generate_blacklists.py --output-dir /tmp/test
   # Inspect /tmp/test/blacklist*.rsc
   ```

3. Verify file sizes and entry counts

### CI/CD Testing

- All PRs automatically run the list-health workflow
- Workflow must pass before merge
- If workflow fails, check the logs and fix issues

## Reporting Issues

### Bug Reports

Include:
- **MikroTik model** and **RouterOS version**
- **List version** (standard or light)
- **Symptoms**: What went wrong?
- **Expected behavior**: What should happen?
- **Steps to reproduce**
- **Logs** (if available):
  ```routeros
  /log print where topics~"error"
  ```

### Feature Requests

Describe:
- **Problem**: What challenge are you facing?
- **Proposed solution**: How would you solve it?
- **Alternatives**: Any other approaches considered?
- **Impact**: Who benefits from this feature?

## Code of Conduct

- Be respectful and professional
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions
- No harassment, discrimination, or inappropriate behavior

## Questions?

- Open a [Discussion](https://github.com/ranas-mukminov/Mikrotik-Blacklist/discussions)
- Check existing [Issues](https://github.com/ranas-mukminov/Mikrotik-Blacklist/issues)
- Review the [README](README.md) and [Copilot Instructions](.github/copilot-instructions.md)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see original [pwlgrzs/Mikrotik-Blacklist](https://github.com/pwlgrzs/Mikrotik-Blacklist) repository).

---

Thank you for helping make Mikrotik-Blacklist better! 🙏
