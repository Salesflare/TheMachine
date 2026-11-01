# Contributing

The Machine is an early release: one owner per installation, on Linux, with macOS and Windows in beta.
Small fixes, clearer setup instructions and new general-purpose sources are welcome.

## Development

1. Clone the repository. Use Python 3.12+ and a supported Node version ([README](README.md#requirements)).
2. Install the pinned OpenClaw: `npm install -g openclaw@2026.10.7` (the version in `openclaw-pin.json`).
3. Install Chromium, or set `CHROMIUM_PATH` to an existing Chromium executable.
4. Run `python3 scripts/test.py`. No real accounts or Gateway are needed.

About the test runner:

- It runs every Python and Node suite, each test file in its own process with a throwaway HOME, several at once.
  `THE_MACHINE_TEST_JOBS=1` runs them one by one.
- It returns a failing exit code if any suite fails.
- Name files to run only those: `python3 scripts/test.py test_moving.py`.
- If OpenClaw is installed outside the Node prefix, set `OPENCLAW_PACKAGE_DIR` to its package directory.
  `PLAYWRIGHT_CORE` may point to another `playwright-core/index.mjs`.

The tests live in `tests/` (`test_*.py`, `test_*.mjs` and helpers such as `test-env.mjs`). They run from the
repository root, so they import the app's modules directly and open files like `sw.js` by their root path. The
dashboard's page is read assembled, through `dashboardPage()` (`tests/dashboard-page.mjs`) or
`dashboard_parts.assemble()` ([Code map](docs/code-map.md)).

CI runs the suite on every pull request with the minimum supported Python, Node and OpenClaw. A weekly run adds a
newer combination (the latest OpenClaw) and macOS and Windows.

The Python runtime uses the standard library. Keep extra runtime dependencies small and explain why they are needed.
The dashboard is plain HTML, CSS and JavaScript.

## Pull requests

What every pull request needs:

- Explain the user-visible problem, the change and how it was checked.
- Add a regression test for a concrete behavior or failure boundary. Cosmetic changes don't need tests that merely
  repeat their implementation.
- Run your own tests and the checks every change ships with, before you open it:
  `python3 scripts/test.py test_i18n.py test_help.py test_us_english.py` plus the suites of the code you touched.
  A red pull request waits until it is fixed.
- Check `git diff --check`. CI also scans the whole reachable Git history with Gitleaks. A passing secret scan
  doesn't prove a text is free of private information: review every added fixture and attachment yourself.

### Help articles and translations

- Every feature change updates its help article in `docs/help/` in the same pull request (the articles are the help
  at themachine.computer/help). `python3 scripts/help_check.py` names the article a new connector, dashboard tab or
  Settings tab needs, and any button text, route or command an article names that the code no longer has.
- New UI strings go in every catalog in `i18n/` (glossary in `i18n/glossary.md`). Add keys anywhere: the catalogs are
  kept sorted by key, so pull requests that add different strings merge without conflicts.
- Run `python3 scripts/i18n_extract.py --sort` before pushing; `tests/test_i18n.py` fails on a catalog that isn't
  sorted. When merging main still leaves a catalog conflict, `python3 scripts/i18n_extract.py --merge` settles it key
  by key.

### Where code goes

- Put code in the module that owns its domain and tables ([Code map](docs/code-map.md)). `tests/test_architecture.py`
  fails on a name a module uses but never imports, a new module that loads `assistant.py`, and a write to a table
  from outside its owner.
- Keep changes where they belong, so parallel pull requests merge cleanly:
  - a new dashboard function goes next to the functions of its area, not at the end of the script;
  - the dashboard's static markup has one element with an id per line (break inside the tag before it,
    `</div` newline `><div id=…>`, so the page stays the same);
  - the action lists in `assistant.py` (`*_ACTIONS`) have one name per line, sorted (`tests/test_owner_boundary.py`
    checks).

### Sources and sends

- Source adapters verify the account's identity and save each page with its checkpoint atomically. Use fixtures to
  check pagination, replay and failures. See [Adding a source](docs/adding-a-source.md).
- Connectors sign in with OAuth when the service offers it, reusing The Machine's existing sign-ins with the narrowest
  scopes. A pasted token or key only when there's no OAuth, with the reason in `SETUP['no_oauth']` and the pull
  request ([Signing in: OAuth first](docs/adding-a-source.md#signing-in-oauth-first)).
- Keep collected evidence, owner decisions and approved sends apart. An unknown send outcome must never cause a blind
  resend.

### Data in the repository

- Use reserved example addresses and made-up content in fixtures and screenshots.
- Never include real emails, chats, credentials, task exports, browser sessions or databases.
- Keep personal preferences in the OpenClaw workspace's `USER.md`, outside the checkout.

### Changes built from a team learning

A change built from a team learning (the hosted service's Learnings inbox, a picked learning's **Build brief**) treats
its use cases as the reference for what was meant:

- Add a test per use case where one fits, and check the result against each.
- The PR body lists every use case with the test that covers it, or says plainly where it falls short:
  "Use case 2: only partly covered, because …", "Use case 3: not covered, because …", or "doesn't hold up, because …".
- Never reword a use case to fit what was built, and never drop one quietly.

## Contributions from a hosted Machine

A connector built and shared from a hosted Machine arrives as a pull request from The Machine's contributions fork, on
a `contrib/` branch. The Machine's hosted service opens it for its owner: their own GitHub account gets no fork, and
their Machine holds no GitHub credential for it.

Like any fork's pull request, its checks wait for a maintainer's approval, get no secrets and run on GitHub's own
runners. Review it like any outside contribution before approving its checks.

On your own computer, contribute the usual way: fork the repository and open a pull request from your fork.

## Releases

Merged changes reach installs only through a signed release (`python3 scripts/release.py cut`, by the release key
holder). See [Operations](docs/operations.md#releases).

## Issues and security

For ordinary bugs, include the version, a redacted error category and steps to reproduce with made-up data. Don't
attach a raw database, environment dump or full service logs. Follow [SECURITY.md](SECURITY.md) for vulnerabilities.

Contributions are accepted under the project license, AGPL-3.0-only (see [LICENSE](LICENSE)).
