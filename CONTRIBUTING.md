# Contributing

The Machine is an early release for a single owner running OpenClaw on Linux.
Small fixes, clearer setup instructions and additional general-purpose sources are welcome.

## Development

1. Clone the repository. Use Python 3.12+ and a supported Node version from the README.
2. Install the pinned SDK: `npm install -g openclaw@2026.10.7`.
3. Install Chromium, or set `CHROMIUM_PATH` to an existing Chromium executable.
4. Run `python3 scripts/test.py`. It runs every Python and Node suite, each test file in its own process
   with a disposable HOME, several at once (`THE_MACHINE_TEST_JOBS=1` runs them one by one), and returns a
   failing exit code if any suite fails. Name files to run only those: `python3 scripts/test.py test_moving.py`.
   No real accounts or Gateway are needed.

The tests live in `tests/` (`test_*.py`, `test_*.mjs` and their helpers such as `test-env.mjs`). They run from the
repository root, so they import the app's modules directly and open files like `dashboard.html` by their root path;
a new test goes in `tests/` too.

If OpenClaw is installed outside the Node prefix, set `OPENCLAW_PACKAGE_DIR` to its package
directory. `PLAYWRIGHT_CORE` may point to another `playwright-core/index.mjs`.
CI tests the minimum supported Python/Node combination and a newer combination, including
the actual pinned SDK imports and the dashboard in Chromium.

The Python runtime uses the standard library. Keep additional runtime dependencies small
and explain why they are needed. The dashboard is plain HTML, CSS and JavaScript.

## Pull requests

- Explain the user-visible problem, the change and how it was checked.
- Add a regression test for a concrete behavior or failure boundary. Cosmetic changes
  do not need tests that merely repeat their implementation.
- Source adapters must verify account identity and save each page with its checkpoint
  atomically. Use fixtures to check pagination, replay and failures. See README “Adding a source”.
- Every feature change updates its help article in `docs/help/` in the same pull request (the articles are the help at
  themachine.computer/help). `python3 scripts/help_check.py` names the article a new connector, dashboard tab or Settings
  tab needs, and any button text, route or command an article names that the code no longer has.
- New UI strings go in every catalog in `i18n/` (glossary in `i18n/glossary.md`). Add keys anywhere in the files: the
  catalogs are kept sorted by key, so pull requests that add different strings merge without conflicts. Run
  `python3 scripts/i18n_extract.py --sort` before pushing; `tests/test_i18n.py` fails on a catalog that isn't sorted.
- A change built from a team learning (the control plane's Learnings inbox, a picked learning's **Build brief**) treats
  its use cases as the reference for what was meant. Add a test per use case where one fits, and check the result
  against each. The PR body lists every use case with the test that covers it, or says plainly where it falls short:
  "Use case 2: only partly covered, because …", "Use case 3: not covered, because …", or "doesn't hold up, because …".
  Never reword a use case to fit what was built, and never drop one quietly.
- Preserve the separation between collected evidence, owner decisions and approved sends.
  An unknown send outcome must never cause a blind resend.
- Use reserved example addresses and synthetic content in fixtures and screenshots.
  Never include real emails, chats, credentials, task exports, browser sessions or databases.
- Keep personal preferences in the OpenClaw workspace's `USER.md`, outside the checkout.

Merged changes reach installs only through a signed release (`python3 scripts/release.py cut`, by the release key holder; see [Operations](docs/operations.md#releases)).

Check `git diff --check` and the test suite before submitting. CI also scans the complete
reachable Git history with Gitleaks. A passing secret scan does not prove that text is
free of private information; review every added fixture and attachment yourself.

## Issues and security

For ordinary bugs, include the version, a redacted error category and steps to reproduce
with synthetic data. Do not attach a raw database, environment dump or full service logs.
Follow [SECURITY.md](SECURITY.md) for vulnerabilities.

Contributions are accepted under the project license, AGPL-3.0-only (see [LICENSE](LICENSE)).
