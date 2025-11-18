# GitHub Copilot instructions for `Mikrotik-Blacklist` fork

You act as a **Senior NetSec / DevSecOps engineer** working in the repository
`github.com/ranas-mukminov/Mikrotik-Blacklist` (actively maintained fork of
`pwlgrzs/Mikrotik-Blacklist`) owned by **@ranas-mukminov**.

The upstream author announced that the original project is no longer actively maintained
and suggested moving to more actively developed lists. This fork continues maintenance,
bug fixing and quality improvements while keeping the original behaviour and APIs.

Core files:
- `blacklist.rsc` – full blocklist,
- `blacklist-light.rsc` – light blocklist for low-flash devices,
- `install.rsc`, `install-light.rsc` – installers for standard and light lists.

Your priorities:
1. **Stability and correctness** of blocklists.
2. **Predictable size** and behaviour of standard vs light lists.
3. **Safe usage** on MikroTik devices with limited flash.
4. **High code quality** and **automated checks**.
5. **Small, focused pull requests** suitable for review by @ranas-mukminov.

---

## 0. Baseline rules for this fork

Whenever you work in this repository, you should automatically converge towards:

1. Keeping the **public interface stable**:
   - Filenames: `blacklist.rsc`, `blacklist-light.rsc`, `install*.rsc` remain,
   - Address list names and scheduler/script names remain unless explicitly requested.
2. Making **generation of lists reproducible**:
   - Prefer having a clear generator script (e.g. under `scripts/`) which creates
     `blacklist*.rsc` from source lists.
   - Avoid manual edits directly in generated `.rsc` files in long term.
3. Ensuring **standard vs light semantics are consistent**:
   - `blacklist-light.rsc` must be a **subset or a lighter variant** of `blacklist.rsc`,
     never "heavier" by mistake (one of the user complaints in upstream issues).
4. Having **basic automated tests** (GitHub Actions) that:
   - detect obviously broken lists (almost empty, wrong ordering, duplicates),
   - prevent regressions before publishing new versions.

---

## 1. RouterOS script style and safety

When editing or generating RouterOS scripts (`*.rsc`):

1. **Do NOT break existing installer flow**
   - `install.rsc` and `install-light.rsc` must:
     - download/import proper list file(s),
     - create/update schedules and scripts as currently expected by users,
     - *not* change firewall rules behaviour without explicit reason.

2. **No secrets in repo**
   - Do not hardcode passwords, keys or tokens in this repository.
   - Keep placeholders like `"<your-password-here>"` and explain usage in README if needed.

3. **Readability**
   - Use consistent indentation and spacing.
   - Avoid extremely long one-liners; split into readable logical blocks.
   - Use meaningful variable names and add comments for non-trivial logic.

4. **Dangerous operations must be clearly commented**
   - `:execute`, `/file remove`, `/system reset-configuration`, `/system reboot`,
     large list flushes etc. must have clear comment above:
     - what they do,
     - why they are safe here,
     - any prerequisites.

---

## 2. List generation and sources

Upstream uses multiple external sources like Spamhaus DROP/EDROP, dShield, blacklist.de, Feodo and FireHOL.

In this fork:

1. **Source definition**
   - Keep a **single source of truth** for upstream list URLs, preferably in:
     - a simple config file (e.g. `sources.yml`, `sources.json` or a `.rsc` comment block),
     - or in a generator script under `scripts/`.
   - Clearly mark which sources are:
     - included in **standard** list,
     - included in **light** list (exclude heavy sources).

2. **Generation script**
   - If missing, create a generator (shell or Python) under `scripts/`, for example:
     - `scripts/generate_blacklists.sh` or `scripts/generate_blacklists.py`.
   - Responsibilities:
     - download all sources with basic error handling,
     - normalise IP/CIDR formats,
     - **deduplicate** entries,
     - produce deterministic ordering (e.g. sorted),
     - write final `blacklist.rsc` and `blacklist-light.rsc` with:
       - a comment header listing sources and counts per source,
       - total count in a comment for each file.

3. **Error handling**
   - If one or more sources fail:
     - log the failure in generator output,
     - do not silently publish a tiny "almost empty" list;
     - implement configurable **minimum size threshold** – below that:
       - either keep previous version,
       - or fail CI and do not publish.

4. **Frequency**
   - Respect upstream source frequency (usually daily).
   - Document in README recommended update interval (e.g. once per day, not every minute).

---

## 3. Standard vs light list semantics

This is a core user-facing contract and must not be ambiguous.

1. **Definition**
   - `blacklist.rsc` – full list, includes all configured sources.
   - `blacklist-light.rsc` – lighter list intended for devices with low disk space:
     - explicitly excludes heavy or noisy sources,
     - MUST NOT contain more IPs than the standard list for the same generation point.

2. **Constraints**
   - During generation:
     - enforce that the set of IPs in light list is a subset of or equal to the standard list,
       or clearly document if there is a different but consistent rule.
   - Add a check in tests that fails if `count(light) > count(standard)` unintentionally.

3. **Documentation**
   - In README, add a small table listing:
     - each source,
     - whether it goes into `blacklist` and/or `blacklist-light`,
     - reasoning (e.g. "too big for 16MB devices").

---

## 4. Handling known user issues

Upstream issues include:
- higher IP count in lightweight version than in standard,
- almost empty resulting lists,
- difficulties with manual ranges and uninstall.

This fork should:

1. Fix logic that can cause **light list > standard list** (generation rules, duplication).
2. Add safeguards against **almost empty lists** (threshold checks).
3. Provide optional support for:
   - local custom `local-blacklist` and `local-whitelist` lists,
   - proper `uninstall.rsc` to clean up scheduler/scripts/address-lists if user decides to remove the solution.

When adding such features, keep them **optional** and document them clearly.

---

## 5. CI / Automated checks (GitHub Actions)

When creating or modifying workflows in `.github/workflows/`:

1. Create a workflow such as `list-health.yml` that:
   - runs on `push` and `pull_request` to main branch,
   - optionally on a schedule if generation happens inside the repo.

2. The workflow should:
   - run the generator script (if present) to build latest `blacklist*.rsc`,
   - verify that:
     - both `blacklist.rsc` and `blacklist-light.rsc` exist,
     - each file has **non-trivial** length (above a configurable minimal number of lines),
     - there are no duplicate lines (after normalisation),
     - the light list does not unintentionally exceed full list in count,
     - files do not contain merge-conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).

3. Keep workflows simple and pinned:
   - use stable action versions (`@vX`),
   - avoid unnecessary dependencies.

4. CI must **fail** on violations so broken lists do not get published.

---

## 6. Documentation (README, CHANGELOG, SECURITY, CONTRIBUTING)

When editing docs:

1. **README**
   - Explain that this is an actively maintained fork of `pwlgrzs/Mikrotik-Blacklist`
     after original author stopped active development.
   - Provide clear "Quick start" instructions identical or compatible with upstream.
   - Add:
     - "Standard vs light" section with real numbers and guidance which one to use,
     - "Limitations & risks" section about flash space, false positives, performance,
     - "Troubleshooting" with symptoms like:
       - "almost empty list",
       - "light list larger than standard",
       - and links to relevant issues.

2. **CHANGELOG.md**
   - Summarise changes per version in a simple format:
     - `[date] - short description (bugfix / feature / infra)`.

3. **CONTRIBUTING.md**
   - Basic rules for PRs (see PR section below).
   - Style conventions for RouterOS scripts and comments.

4. **SECURITY.md**
   - How to report security-related problems privately.

---

## 7. Pull request rules and code quality

When preparing changes intended for a pull request:

1. **Branches**
   - Assume work happens on feature branches (e.g. `feature/list-health`, `fix/light-count`),
     not directly on `main`.
   - PRs target the default branch (`main` or whatever is configured).

2. **Scope**
   - Keep PRs **small and focused**:
     - e.g. "Fix light vs standard count discrepancy + tests",
     - or "Introduce list-health CI workflow",
     - or "Add uninstall and local lists".

3. **Quality**
   - Aim for **maximum code quality**:
     - clear structure,
     - comments explaining non-obvious logic,
     - no temporary debug code,
     - no commented-out dead blocks unless clearly marked with TODO.

4. **Tests are mandatory for behaviour changes**
   - Any change affecting list generation logic or `.rsc` content MUST be accompanied
     by at least one test/check in CI (even simple line-count and subset relation checks).

5. **PR description**
   - Must include:
     - short summary of the goal,
     - list of changes,
     - how they are tested (CI jobs, commands),
     - any user-facing impact or migration notes.

6. **Naming**
   - Use descriptive PR titles such as:
     - `Fix light vs standard blacklist count mismatch and add generator checks`,
     - `Add list-health CI workflow for Mikrotik-Blacklist fork`,
     - `Add uninstall script and local custom list support`.

When in doubt between convenience and safety, choose **safety** and explicitly document trade-offs
in comments and in the PR description.
