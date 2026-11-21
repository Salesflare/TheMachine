"""Clicking through a password manager's export page to its export step, for the owner (login_import.export_open).

The owner signs in on the page themselves. Then a fixed script, the same every time and never the model, clicks the
way to the export step: LastPass's Advanced options and Export, Bitwarden's Export vault, Google Password Manager's
Export passwords. What stays the owner's is everything that proves it's them: the sign-in, 2FA, the master password
asked again before the export, an email to confirm. The script never types anything, never reads a field's value and
takes no screenshot; it only looks for the next button by fixed words and selectors (RECIPES) and clicks it, and focuses
the master password field so the owner can type right away.

Nothing from the page leaves it: the script answers with one of a fixed set of words (`at`) and, for a click, the
button's position on screen, and step() checks both against that set before using them. The log gets what it saw
from that fixed set only (`at` and the recipe's step number), when it changes: never an address, a word or a value. When the
page doesn't look the way a recipe expects (the manager changed it), step() says 'manual' once GIVE_UP seconds go by
without a step, and the dialog shows the owner the manual steps instead.
"""
from __future__ import annotations

import logging
import re
import time
import urllib.parse

import browser_login

LOG = logging.getLogger('personal-assistant')

browser_cdp = browser_login.browser_cdp  # the one module object, so its CdpError is the one raised

GIVE_UP = 20  # seconds signed in with no step found before the owner is handed the manual steps (signing in never counts)
CLICKS = 4  # each button at most this often (an email to confirm sends the owner back to the start once or twice)
AGAIN = 4  # seconds before the same button is clicked again
GOES = 3  # how often a recipe's export address is opened
OWNER_REST = 30  # seconds after the master password showed before anything is clicked again (the download may be on its way)
SETTLE = 5  # seconds after a click to wait for the next step's button before a step up to it may be clicked again
ROUNDS = 2  # going back to a step already clicked: the second time, the guide stops clicking and hands over the steps
STARTED = 3  # seconds after the step that starts the export for the master password to show, before 'email' is said

# Per manager: `signin` (address of its sign-in, 2FA or unlock pages), `vault` (address once signed in), `go`/`at` (an
# address to open once signed in, and how to tell it's there), `steps` (buttons in order, each by CSS selectors first,
# then by its exact words, lowercase), `arm` (the first step after which a password field is the master password asked
# again rather than the sign-in) and `email` (words that say an email waits to be confirmed). A step with `starts` starts
# the export (LastPass emails a link to confirm on each click): it is clicked once per export, once more only after the
# guide opened that email's link (`verify`: its sender's domain, subject, the hosts its link may be on and the link's
# path; login_export_mail), and nothing up to it is clicked again while the owner's part waits.
_EXPORT = ['export', 'exporteren', 'exportieren', 'exporter', 'exportar', 'esporta']
RECIPES = {
    'lastpass': {
        'signin': r'^https://(www\.)?lastpass\.(com|eu)/(\?|.*[?&]ac=1|[^#]*(login|signin|sso|multifactor|mfa))',
        'vault': r'^https://(www\.)?lastpass\.(com|eu)/',
        # LastPass's help: in the vault's left navigation, Advanced options, then Export in the list it opens. Export
        # itself starts the export: the page only says to look for an email from LastPass ("Verify export", whose
        # Continue export link expires in 10 minutes), the menu folds again, and Advanced options > Export once more
        # asks the master password and downloads the CSV. A narrow window folds the left navigation behind its menu
        # button, so that comes first (only clicked when neither of the others shows).
        'steps': [
            {'css': [], 'text': ['menu', 'open menu', 'main menu', 'open navigation', 'toggle navigation', 'expand navigation',
                                 'navigation menu', 'show navigation', 'expand menu']},
            {'css': ['[data-automation-id="advanced-options-menu-item"]', '#advancedOptionsMenuItem'],
             'text': ['advanced options', 'geavanceerde opties', 'erweiterte optionen', 'options avancées', 'opciones avanzadas',
                      'opzioni avanzate', 'opções avançadas']},
            {'css': ['[data-automation-id="export-menu-item"]', '#exportMenuItem'], 'starts': True,
             'text': _EXPORT + ['export items', 'export vault items', 'items exporteren', 'elemente exportieren', 'exporter les éléments',
                                'exportar elementos', 'esporta elementi', 'exportar itens']},
            {'css': [], 'text': ['lastpass csv file', 'csv file', 'csv']},
        ],
        'arm': 2,
        'email': r'check your (email|inbox)|verification email|(sent|emailed) you an? (email|link)|verify (this |your )?export|'
                 r'look for an email|finish the export',
        'verify': {'from': r'(^|\.)lastpass\.(com|eu)$', 'subject': r'verify export', 'hosts': r'^([a-z0-9-]+\.)*lastpass\.(com|eu)$',
                   'path': r'^/export-tokens/[0-9a-f-]+/approve/?$'},
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
# all inside the page; none of it is in the answer. It looks through the whole page: the document, each open shadow
# root (a web component's insides) and each frame of the same origin, recursively. Frames of another origin are the
# guide's (look: it runs this again in each, with s.inner). On no match, it counts what it saw: numbers only.
SCRIPT = r'''function (r, s) {
  const href = location.href, test = (re) => !!re && new RegExp(re, 'i').test(href);
  const roots = [], n = {frames: 0, other: 0, shadow: 0, custom: 0};
  const gather = (root) => { roots.push(root); for (const el of root.querySelectorAll('*')) {
    if (el.shadowRoot) { n.shadow++; gather(el.shadowRoot); } else if (el.localName.includes('-')) n.custom++;
    if (/^i?frame$/.test(el.localName)) { let d = null; try { d = el.contentDocument; } catch (e) {}
      if (d && d.documentElement) { n.frames++; gather(d); } else n.other++; } } };
  gather(document);
  const all = (css) => roots.flatMap((root) => { try { return [...root.querySelectorAll(css)]; } catch (e) { return []; } });
  const style = (el, p) => (el.ownerDocument.defaultView || window).getComputedStyle(el, p);
  // an element's box in this window: its frame's place added for one in a frame
  const place = (el) => { const b = el.getBoundingClientRect(); let x = b.left, y = b.top;
    for (let w = el.ownerDocument.defaultView; w && w.frameElement; w = w.parent) {
      const f = w.frameElement, o = f.getBoundingClientRect(); x += o.left + f.clientLeft; y += o.top + f.clientTop; }
    return {x, y, w: b.width, h: b.height}; };
  const shows = (el) => { if (!el || el.disabled) return false; const b = el.getBoundingClientRect();
    if (b.width < 1 || b.height < 1) return false; const st = style(el);
    return st.visibility !== 'hidden' && st.display !== 'none' && Number(st.opacity) > 0; };
  const words = (t) => String(t || '').replace(/\s+/g, ' ').trim().toLowerCase();
  const active = () => { let a = document.activeElement;
    for (;;) { let d = null; try { d = a && (a.shadowRoot || a.contentDocument); } catch (e) {}
      const next = d && d.activeElement; if (!next || next === a) return a; a = next; } };
  const pw = all('input[type=password]').find(shows);
  const signin = test(r.signin);
  // Where the owner types, for the live view to zoom to on a phone: the field with the focus, else the password or
  // the first text field, with its form or dialog around it when that fits. Its place in the window only.
  const box = () => {
    const a = active(), field = a && a.matches && a.matches('input') && shows(a) ? a : pw ||
      all('input[type=email],input[type=text],input:not([type])').find(shows);
    if (!field) return null;
    const area = field.closest('form,dialog,[role=dialog]'), b0 = area && shows(area) && place(area);
    const b = b0 && b0.h < innerHeight * 0.8 && b0.w < innerWidth * 0.9 ? b0 : place(field);
    const W = outerWidth || innerWidth, H = outerHeight || innerHeight, top = Math.max(0, H - innerHeight), left = Math.max(0, (W - innerWidth) / 2);
    const x = Math.max(0, b.x), y = Math.max(0, b.y);
    return {x: (left + x) / W, y: (top + y) / H, w: Math.min(b.x + b.w, innerWidth) - x, h: Math.min(b.y + b.h, innerHeight) - y, W, H};
  };
  const at = (word) => { const b = !s.inner && box(); return b && b.w > 0 && b.h > 0 ? {at: word, box: {x: b.x, y: b.y, w: b.w / b.W, h: b.h / b.H}} : {at: word}; };
  if (s.inner) {  // a frame of another origin: only its buttons and the master password asked again
    if (pw && s.armed) { if (s.focus && active() !== pw) pw.focus(); return at('password'); }
  } else {
    if (pw && (s.armed || test(r.at)) || s.armed && signin) {
      if (pw && s.focus && active() !== pw) pw.focus();
      return at('password');
    }
    // A sign-in that asks the email first (LastPass's, on the vault's own address): an email or user name field
    // before the script found anything to click is the owner's sign-in too, not a page it doesn't know.
    const ident = !s.stepped && all('input[type=email],input[autocomplete~=username],input[autocomplete~=email],' +
      'input[name*=email i],input[id*=email i],input[name*=user i],input[id*=user i]').find(shows);
    if (pw || signin || ident) return at('signin');
    if (!test(r.vault)) return at('elsewhere');
    if (s.armed && r.email && roots.some((d) => d.body && new RegExp(r.email, 'i').test(d.body.innerText || ''))) return {at: 'email'};
    if (r.go && !test(r.at)) { if (s.go) location.assign(r.go); return {at: 'going'}; }
  }
  const clickable = 'button,a[href],[role=button],[role=menuitem],[role=link],[role=tab],[role=option],[role=radio],' +
    'input[type=submit],input[type=button],input[type=radio],label,li,[jsaction*="click"],[tabindex]:not([tabindex="-1"])';
  // up the page, out of a shadow root into its host
  const up = (a) => a.parentElement || (a.parentNode && a.parentNode.host) || null;
  // What to click for a match: its closest button-like element, else the closest that shows a pointer (a navigation
  // item that is a plain div with a click handler), else the element itself
  const target = (el) => { if (!el) return null; let t = null;
    for (let a = el; !t && a && a !== a.ownerDocument.body; a = up(a)) if (a.matches(clickable)) t = a;
    for (let a = el; !t && a && a !== a.ownerDocument.body; a = up(a)) if (style(a).cursor === 'pointer') t = a;
    t = t || el; return words(t.textContent).length <= 80 && shows(t) ? t : null; };
  // words drawn by the style sheet (::before, ::after) count as the element's own
  const drawn = (el, p) => { const c = style(el, p).content; return /^["']/.test(c) ? c.slice(1, -1) : ''; };
  const said = (el) => words(drawn(el, '::before') + ' ' + el.textContent + ' ' + drawn(el, '::after'));
  const find = (step) => {
    for (const css of step.css) { const el = all(css).find(shows); if (el) return el; }
    const want = new Set(step.text), hit = (el, t) => want.has(words(t)) && target(el);
    for (const el of all('[aria-label],[title]')) {
      for (const t of [el.getAttribute('aria-label'), el.getAttribute('title')]) if (t && hit(el, t)) return target(el); }
    for (const root of roots) {
      const walk = (root.ownerDocument || root).createTreeWalker(root.body || root, NodeFilter.SHOW_TEXT);
      for (let t = walk.nextNode(); t; t = walk.nextNode()) if (hit(t.parentElement, t.nodeValue)) return target(t.parentElement);
    }
    // words split over several pieces of text (an icon's text, a badge) or drawn by the style sheet, in navigation,
    // menus and dialogs (anywhere in a frame or a web component): the smallest element whose words are the step's
    const parts = 'nav *,aside *,header *,[role=navigation] *,[role=menu] *,[role=menubar] *,[role=dialog] *,dialog *,ul *';
    for (const root of roots) for (const el of root.querySelectorAll(root === document ? parts : '*'))
      if (el.childElementCount < 6 && el.textContent.length < 200 && hit(el, said(el))) return target(el);
    return null;
  };
  for (let i = r.steps.length - 1; i >= 0; i--) {
    const el = find(r.steps[i]);
    if (!el) continue;
    if (!s.may[i]) return {at: 'held', step: i};
    el.scrollIntoView({block: 'center', inline: 'center'});
    const b = place(el);
    return {at: 'click', step: i, x: b.x + b.w / 2, y: b.y + b.h / 2};
  }
  return {at: 'missing', frames: n.frames, other: n.other, shadow: n.shadow, custom: n.custom, candidates: all(clickable).filter(shows).length};
}'''
AT = {'password', 'signin', 'elsewhere', 'email', 'going', 'held', 'click', 'missing'}


def owns(manager, url):
    """Whether a tab's address is this manager's sign-in, vault or export page (login_import follows the one used
    last)."""
    recipe = RECIPES.get(manager) or {}
    return any(recipe.get(k) and re.search(recipe[k], url or '', re.I) for k in ('signin', 'vault'))


def allowed(manager, url):
    """Whether `url` may be opened as this manager's export verification (login_export_mail): https, on one of its own
    hosts (`verify`), no user name or other port."""
    verify = (RECIPES.get(manager) or {}).get('verify')
    if not verify or not isinstance(url, str) or len(url) > 2000:
        return False
    try:
        part = urllib.parse.urlsplit(url.strip())
        port = part.port
    except ValueError:
        return False
    return (part.scheme == 'https' and not part.username and not part.password and port in (None, 443)
            and bool(re.search(verify['hosts'], (part.hostname or '').lower())))


def start():
    """A guide's state, kept by the export's watch: what was clicked when, and since when nothing happened."""
    # top/top_at: the step clicked last and when; rounds: how often a click went back to a step already clicked;
    # started: when the step that starts the export was clicked (None: not yet, or again allowed after a verification);
    # starts: how many more times it may be clicked; verified: whether the email's link was opened (at most once)
    return {'clicks': {}, 'last': {}, 'goes': 0, 'armed': False, 'focused': False, 'progress': time.monotonic(), 'box': None,
            'top': -1, 'top_at': 0.0, 'rounds': 0, 'started': None, 'starts': 1, 'verified': False}


def _starts(recipe):
    """The recipe's step that starts the export, or None."""
    return next((i for i, s in enumerate(recipe['steps']) if s.get('starts')), None)


def verified(state):
    """The email's link was opened (login_import): the step that starts the export may be clicked exactly once more,
    and the steps on the way to it again."""
    if state['verified']:
        return
    state.update(verified=True, started=None, starts=state['starts'] + 1, top=-1, rounds=0, progress=time.monotonic())


def _may(recipe, state, now):
    """Which steps may be clicked now. Nothing up to the step that starts the export once it was clicked (the owner's
    email, the master password); nothing up to the step clicked last while its next step may still show (SETTLE); and
    after a round back to an earlier step, no second one (the page loops)."""
    rested = now - state.get('owner', -OWNER_REST) >= OWNER_REST
    first = _starts(recipe)
    settling = now - state['top_at'] < SETTLE
    spent = state['rounds'] >= ROUNDS - 1
    out = []
    for i in range(len(recipe['steps'])):
        ok = rested and state['clicks'].get(i, 0) < CLICKS and now - state['last'].get(i, -AGAIN) >= AGAIN
        if i <= state['top'] and (settling or spent):
            ok = False
        if first is not None and i <= first and (state['started'] is not None or state['starts'] < 1):
            ok = False
        out.append(ok)
    return out


def _box(box):
    """Where the owner types, as fractions of the browser's window {x, y, w, h}, or None: numbers only, each checked."""
    if not isinstance(box, dict):
        return None
    values = {k: box.get(k) for k in ('x', 'y', 'w', 'h')}
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 1 for v in values.values()):
        return None
    if values['w'] <= 0 or values['h'] <= 0:
        return None
    return {k: round(float(v), 4) for k, v in values.items()}


MISS = ('frames', 'other', 'shadow', 'custom', 'candidates')


def _checked(got, recipe):
    """SCRIPT's answer checked: {at, step, x, y, box, miss}, numbers and fixed words only, or None."""
    at = got.get('at') if isinstance(got, dict) else None
    if at not in AT:
        return None
    step = got.get('step')
    if at in ('click', 'held') and not (isinstance(step, int) and 0 <= step < len(recipe['steps'])):
        return None
    x, y = got.get('x'), got.get('y')
    if at == 'click' and not all(isinstance(v, (int, float)) and not isinstance(v, bool) and -20000 < v < 20000 for v in (x, y)):
        return None
    miss = {k: got.get(k) if isinstance(got.get(k), int) and not isinstance(got.get(k), bool) and got.get(k) >= 0 else 0
            for k in MISS} if at == 'missing' else None
    return {'at': at, 'step': step, 'x': x, 'y': y, 'box': _box(got.get('box')), 'miss': miss}


def _frames(base, tab, session, opened):
    """Where else in the tab to look: its frames of another origin, which SCRIPT in the page can't read, as
    [(session, context, x, y)]: a frame in the tab's own process in a world of the guide's own (context), one of
    another site through its own target in the browser (context None). x, y: where its content starts in the tab."""
    found = []

    def owner(at, frame):  # where the frame's content sits in its parent target's window
        node = at.call('DOM.getFrameOwner', {'frameId': frame})['backendNodeId']
        quad = at.call('DOM.getBoxModel', {'backendNodeId': node})['model']['content']
        return float(quad[0]), float(quad[1])

    def local(at, dx, dy):
        tree = at.call('Page.getFrameTree')['frameTree']
        todo = [(f, tree['frame'].get('securityOrigin')) for f in tree.get('childFrames') or []]
        while todo:
            f, reach = todo.pop(0)
            frame = f['frame']['id']
            same = reach is not None and f['frame'].get('securityOrigin') == reach  # SCRIPT read it from its parent
            todo += [(c, reach if same else None) for c in f.get('childFrames') or []]
            if same:
                continue
            try:
                x, y = owner(at, frame)
                world = at.call('Page.createIsolatedWorld', {'frameId': frame, 'worldName': 'export guide'})['executionContextId']
            except (browser_cdp.CdpError, KeyError, IndexError, TypeError, ValueError):
                continue
            found.append((at, world, dx + x, dy + y))

    local(session, 0.0, 0.0)
    apart, parents = browser_cdp.frames(base, timeout=5), {tab: (session, 0.0, 0.0)}
    for _ in range(4):  # a frame of another site in one of another site: a few deep
        for frame, parent in apart:
            if frame in parents or parent not in parents:
                continue
            at, dx, dy = parents[parent]
            try:
                x, y = owner(at, frame)
                inner = browser_cdp.Session(base, frame, timeout=5)
            except (browser_cdp.CdpError, OSError, KeyError, IndexError, TypeError, ValueError):
                continue
            opened.append(inner)
            parents[frame] = (inner, dx + x, dy + y)
            found.append((inner, None, dx + x, dy + y))
            try:
                local(inner, dx + x, dy + y)
            except (browser_cdp.CdpError, KeyError, TypeError):
                pass
    return found


def look(base, tab, recipe, state):
    """Runs SCRIPT once in the tab: its checked answer, or None when the page can't be reached right now (loading,
    the browser busy). Nothing found there: runs it again in each frame of another origin (_frames). Clicks the
    button it found, as a mouse click there."""
    may = _may(recipe, state, time.monotonic())
    flags = {'armed': state['armed'], 'stepped': bool(state['clicks']), 'focus': not state['focused'], 'go': state['goes'] < GOES, 'may': may}
    opened = []
    try:
        with browser_cdp.Session(base, tab, timeout=5) as session:
            got = _checked(session.run(SCRIPT, recipe, flags), recipe)
            if got and got['at'] == 'missing':
                outside = _frames(base, tab, session, opened)
                got['miss']['outside'] = len(outside)
                for where, context, dx, dy in outside:
                    try:
                        inner = _checked(where.run(SCRIPT, recipe, dict(flags, inner=True), context=context), recipe)
                    except (browser_cdp.CdpError, OSError, ValueError, TypeError, KeyError):
                        continue
                    if inner and inner['at'] in ('click', 'held', 'password'):
                        got = dict(inner, x=(inner['x'] or 0) + dx, y=(inner['y'] or 0) + dy)
                        break
                    if inner and inner['miss']:
                        for k in ('shadow', 'custom', 'candidates'):
                            got['miss'][k] += inner['miss'][k]
            if got and got['at'] == 'click':
                x, y = got['x'], got['y']
                if not all(0 <= v < 20000 for v in (x, y)):
                    return None
                for kind in ('mouseMoved', 'mousePressed', 'mouseReleased'):
                    session.call('Input.dispatchMouseEvent', {'type': kind, 'x': x, 'y': y, 'button': 'left', 'clickCount': 1})
            return got and {'at': got['at'], 'step': got['step'], 'box': got['box'], 'miss': got['miss']}
    except (browser_cdp.CdpError, OSError, ValueError, TypeError, KeyError, AttributeError):
        return None
    finally:
        for inner in opened:
            inner.ws.close()


def step(base, tab, manager, state):
    """One look at the export tab: what the owner is told now, one of 'signin' (sign in on the page), 'working' (the
    script is on it), 'password' (type the master password to export), 'email' (confirm the manager's email) or
    'manual' (the page isn't as expected: the steps are the owner's). None: no new word (the page didn't answer).
    At sign-in and password, state['box'] is where the owner types in the window (_box), for the live view."""
    recipe = RECIPES[manager]
    seen = look(base, tab, recipe, state)
    said_now = ('none',) if seen is None else (seen['at'], seen['step'])
    if said_now != state.get('seen'):
        state['seen'] = said_now
        LOG.info('login export guide manager=%s at=%s step=%s', manager, said_now[0], said_now[1] if len(said_now) > 1 else '-')
        if seen and seen['miss']:  # what kind of miss: how much of the page it could look into, counts only
            LOG.info('login export guide miss manager=%s %s', manager, ' '.join('%s=%d' % (k, seen['miss'][k]) for k in MISS + ('outside',)))
    if seen is None:  # the page didn't answer (loading, busy): no new word, unless it stays that way long after the last
        return 'manual' if time.monotonic() - state['progress'] > 3 * GIVE_UP else None
    now, at = time.monotonic(), seen['at']
    said = {'signin': 'signin', 'elsewhere': 'signin', 'password': 'password', 'email': 'email'}.get(at)
    state['box'] = seen['box'] if said in ('signin', 'password') else None
    if at == 'password':
        state['focused'], state['owner'] = True, now
    if at == 'going' and state['goes'] < GOES:
        state['goes'] += 1
        said = 'working'
    if at == 'click':
        i = seen['step']
        if i <= state['top']:  # back to a step already clicked: a round
            state['rounds'] += 1
        state['top'], state['top_at'] = i, now
        state['clicks'][i] = state['clicks'].get(i, 0) + 1
        state['last'][i] = now
        state['armed'] = state['armed'] or i >= recipe['arm']
        if recipe['steps'][i].get('starts'):
            state['started'], state['starts'], state['started_at'] = now, state['starts'] - 1, time.time()
            LOG.info('login export guide started manager=%s step=%d', manager, i)
        said = 'working'
    elif state['started'] is not None and at in ('held', 'missing', 'going'):
        # The export started and no later step shows: the manager waits on the owner (LastPass's email to confirm).
        # Nothing up to that step is clicked again; it says so once the master password had time to show.
        said = 'email' if recipe['email'] and now - state['started'] >= STARTED else 'working'
    elif at == 'held' and seen['step'] <= state['top'] and state['rounds'] >= ROUNDS - 1 and now - state['top_at'] >= SETTLE:
        # the same steps again and again: stop clicking, the owner gets the steps (and keeps the live view)
        LOG.info('login export guide loop manager=%s step=%d rounds=%d', manager, seen['step'], state['rounds'] + 1)
        return 'manual'
    elif at == 'held' and state['clicks'].get(seen['step'], 0) < CLICKS:
        said = 'working'
    if said:
        state['progress'] = now
        return said
    return 'manual' if now - state['progress'] > GIVE_UP else 'working'
