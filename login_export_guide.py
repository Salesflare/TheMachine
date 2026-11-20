"""Clicking through a password manager's export page to its export step, for the owner (login_import.export_open).

The owner signs in on the page themselves. Then a fixed script, the same every time and never the model, clicks the
way to the export step: LastPass's Advanced options and Export, Bitwarden's Export vault, Google Password Manager's
Export passwords. What stays the owner's is everything that proves it's them: the sign-in, 2FA, the master password
asked again before the export, an email to confirm. The script never types anything, never reads a field's value and
takes no screenshot; it only looks for the next button by fixed words and selectors (RECIPES) and clicks it, and focuses
the master password field so the owner can type right away.

Nothing from the page leaves it: the script answers with one of a fixed set of words (`at`) and, for a click, the
button's position on screen, and step() checks both against that set before using them. Nothing here logs. When the
page doesn't look the way a recipe expects (the manager changed it), step() says 'manual' once GIVE_UP seconds go by
without a step, and the dialog shows the owner the manual steps instead.
"""
from __future__ import annotations

import time

import browser_login

browser_cdp = browser_login.browser_cdp  # the one module object, so its CdpError is the one raised

GIVE_UP = 20  # seconds signed in with no step found before the owner is handed the manual steps
CLICKS = 4  # each button at most this often (an email to confirm sends the owner back to the start once or twice)
AGAIN = 4  # seconds before the same button is clicked again
GOES = 3  # how often a recipe's export address is opened
OWNER_REST = 30  # seconds after the master password showed before anything is clicked again (the download may be on its way)

# Per manager: `signin` (address of its sign-in, 2FA or unlock pages), `vault` (address once signed in), `go`/`at` (an
# address to open once signed in, and how to tell it's there), `steps` (buttons in order, each by CSS selectors first,
# then by its exact words, lowercase), `arm` (the first step after which a password field is the master password asked
# again rather than the sign-in) and `email` (words that say an email waits to be confirmed).
_EXPORT = ['export', 'exporteren', 'exportieren', 'exporter', 'exportar', 'esporta']
RECIPES = {
    'lastpass': {
        'signin': r'^https://(www\.)?lastpass\.(com|eu)/(\?|.*[?&]ac=1|[^#]*(login|signin|sso|multifactor|mfa))',
        'vault': r'^https://(www\.)?lastpass\.(com|eu)/',
        'steps': [
            {'css': ['[data-automation-id="advanced-options-menu-item"]', '#advancedOptionsMenuItem'],
             'text': ['advanced options', 'geavanceerde opties', 'erweiterte optionen', 'options avancées', 'opciones avanzadas',
                      'opzioni avanzate', 'opções avançadas']},
            {'css': ['[data-automation-id="export-menu-item"]', '#exportMenuItem'], 'text': _EXPORT},
            {'css': [], 'text': ['lastpass csv file', 'csv file', 'csv']},
        ],
        'arm': 1,
        'email': r'check your (email|inbox)|verification email|(sent|emailed) you an? (email|link)',
    },
    'bitwarden': {
        'signin': r'^https://vault\.bitwarden\.(com|eu)/#/(login|2fa|lock|sso|signup|hint|accept|finish|set-password|verify)',
        'vault': r'^https://vault\.bitwarden\.(com|eu)/#/',
        'go': '#/tools/export', 'at': r'#/tools/(vault-)?export',
        'steps': [{'css': ['tools-export button[type="submit"]', 'app-export button[type="submit"]'],
                   'text': ['export vault', 'confirm format', 'kluis exporteren', 'tresor exportieren', 'exporter le coffre',
                            'exportar caja fuerte']}],
        'arm': 0,
        'email': r'check your email|verification code (has been )?sent|sent .{0,20}code to your email',
    },
    'chrome': {
        'signin': r'^https://accounts\.google\.com/',
        'vault': r'^https://passwords\.google\.com/',
        'go': '/options', 'at': r'^https://passwords\.google\.com/options',
        'steps': [
            {'css': [], 'text': ['export passwords', 'wachtwoorden exporteren', 'passwörter exportieren', 'exporter les mots de passe',
                                 'exportar contraseñas', 'esporta password', 'exportar senhas']},
            {'css': [], 'text': ['download file', 'download', 'bestand downloaden', 'datei herunterladen', 'télécharger le fichier',
                                 'descargar archivo', 'scarica file', 'baixar arquivo'] + _EXPORT},
        ],
        'arm': 0,
        'email': None,
    },
}

# Runs in the page with the recipe and what may happen now, both as values. Answers {at} with at one of AT, plus the
# step and its position for a click. It reads the address, whether fields and buttons show and the words on buttons,
# all inside the page; none of it is in the answer.
SCRIPT = r'''function (r, s) {
  const href = location.href, test = (re) => !!re && new RegExp(re, 'i').test(href);
  const shows = (el) => { if (!el || el.disabled) return false; const b = el.getBoundingClientRect();
    if (b.width < 1 || b.height < 1) return false; const st = getComputedStyle(el);
    return st.visibility !== 'hidden' && st.display !== 'none' && Number(st.opacity) > 0; };
  const words = (t) => String(t || '').replace(/\s+/g, ' ').trim().toLowerCase();
  const pw = [...document.querySelectorAll('input[type=password]')].find(shows);
  const signin = test(r.signin);
  if (pw && (s.armed || test(r.at)) || s.armed && signin) {
    if (pw && s.focus && document.activeElement !== pw) pw.focus();
    return {at: 'password'};
  }
  if (pw || signin) return {at: 'signin'};
  if (!test(r.vault)) return {at: 'elsewhere'};
  if (s.armed && r.email && document.body && new RegExp(r.email, 'i').test(document.body.innerText || '')) return {at: 'email'};
  if (r.go && !test(r.at)) { if (s.go) location.assign(r.go); return {at: 'going'}; }
  const clickable = 'button,a[href],[role=button],[role=menuitem],[role=link],[role=tab],[role=option],[role=radio],' +
    'input[type=submit],input[type=button],input[type=radio],label,li,[jsaction*="click"],[tabindex]:not([tabindex="-1"])';
  const target = (el) => { const t = el && el.closest(clickable); return t && words(t.textContent).length <= 80 && shows(t) ? t : null; };
  const find = (step) => {
    for (const css of step.css) { let el = null; try { el = [...document.querySelectorAll(css)].find(shows); } catch (e) {} if (el) return el; }
    const want = new Set(step.text);
    for (const el of document.querySelectorAll('[aria-label]')) if (want.has(words(el.getAttribute('aria-label'))) && target(el)) return target(el);
    const walk = document.createTreeWalker(document.body || document.documentElement, NodeFilter.SHOW_TEXT);
    for (let n = walk.nextNode(); n; n = walk.nextNode()) if (want.has(words(n.nodeValue)) && target(n.parentElement)) return target(n.parentElement);
    return null;
  };
  for (let i = r.steps.length - 1; i >= 0; i--) {
    const el = find(r.steps[i]);
    if (!el) continue;
    if (!s.may[i]) return {at: 'held', step: i};
    el.scrollIntoView({block: 'center', inline: 'center'});
    const b = el.getBoundingClientRect();
    return {at: 'click', step: i, x: b.left + b.width / 2, y: b.top + b.height / 2};
  }
  return {at: 'missing'};
}'''
AT = {'password', 'signin', 'elsewhere', 'email', 'going', 'held', 'click', 'missing'}


def start():
    """A guide's state, kept by the export's watch: what was clicked when, and since when nothing happened."""
    return {'clicks': {}, 'last': {}, 'goes': 0, 'armed': False, 'focused': False, 'progress': time.monotonic()}


def look(base, tab, recipe, state):
    """Runs SCRIPT once in the tab: its checked answer, or None when the page can't be reached right now (loading,
    the browser busy). Clicks the button it found, as a mouse click there."""
    now = time.monotonic()
    rested = now - state.get('owner', -OWNER_REST) >= OWNER_REST
    may = [rested and state['clicks'].get(i, 0) < CLICKS and now - state['last'].get(i, -AGAIN) >= AGAIN for i in range(len(recipe['steps']))]
    flags = {'armed': state['armed'], 'focus': not state['focused'], 'go': state['goes'] < GOES, 'may': may}
    try:
        with browser_cdp.Session(base, tab, timeout=5) as session:
            got = session.run(SCRIPT, recipe, flags)
            at = got.get('at') if isinstance(got, dict) else None
            if at not in AT:
                return None
            step = got.get('step')
            if at in ('click', 'held') and not (isinstance(step, int) and 0 <= step < len(recipe['steps'])):
                return None
            if at == 'click':
                x, y = got.get('x'), got.get('y')
                if not all(isinstance(v, (int, float)) and 0 <= v < 20000 for v in (x, y)):
                    return None
                for kind in ('mouseMoved', 'mousePressed', 'mouseReleased'):
                    session.call('Input.dispatchMouseEvent', {'type': kind, 'x': x, 'y': y, 'button': 'left', 'clickCount': 1})
            return {'at': at, 'step': step}
    except (browser_cdp.CdpError, OSError, ValueError, TypeError, KeyError, AttributeError):
        return None


def step(base, tab, manager, state):
    """One look at the export tab: what the owner is told now, one of 'signin' (sign in on the page), 'working' (the
    script is on it), 'password' (type the master password to export), 'email' (confirm the manager's email) or
    'manual' (the page isn't as expected: the steps are the owner's). None: no new word (the page didn't answer)."""
    recipe = RECIPES[manager]
    seen = look(base, tab, recipe, state)
    if seen is None:
        return None
    now, at = time.monotonic(), seen['at']
    said = {'signin': 'signin', 'elsewhere': 'signin', 'password': 'password', 'email': 'email'}.get(at)
    if at == 'password':
        state['focused'], state['owner'] = True, now
    if at == 'going' and state['goes'] < GOES:
        state['goes'] += 1
        said = 'working'
    if at == 'click':
        i = seen['step']
        state['clicks'][i] = state['clicks'].get(i, 0) + 1
        state['last'][i] = now
        state['armed'] = state['armed'] or i >= recipe['arm']
        said = 'working'
    if at == 'held' and state['clicks'].get(seen['step'], 0) < CLICKS:
        said = 'working'
    if said:
        state['progress'] = now
        return said
    return 'manual' if now - state['progress'] > GIVE_UP else 'working'
