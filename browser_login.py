"""Signing in to a site in the assistant's browser from a small dialog on the dashboard, instead of the browser itself.

When a preparation or a source reader stops at a sign-in page, the owner types the username, password and, when the
page asks, a one-time code in the dashboard. The service puts them in that page over DevTools (CDP, loopback only)
and submits. This is its own code path: the agent and the model never see these values, nothing here logs them, and
errors never quote them.

"Save for next time" keeps a site's username and password in browser-logins.sealed in the data folder, sealed with the
message key (message_seal.py: the same key as the messages, so a hosted Machine keeps it off the disk, and no backup of
the disk holds a key that opens them). Without a message key (message protection turned off) they go in
browser-logins.enc with a key of their own next to it (browser-logins.key, readable by this user only), as before; once
there is a message key they move over and the old file and its key are overwritten and removed. Saved sign-ins are
listed and forgotten on the dashboard; a move (moving.py) only takes them along with a passphrase. One-time codes are
never saved.

Accounts: a site can have several saved sign-ins, each a named account ("Work", "Personal"), each bound to exact
origins (scheme, host and port, as the browser's location.origin says them). A saved password goes only into a page
whose origin is one of them: never a lookalike, a subdomain or plain http. They live in browser-logins.v2.sealed (or
.v2.enc without a message key). The first save, or the service's start, writes that file from the older one (one site,
one sign-in), each becoming a "Default" account bound to https://site and https://www.site (the older key had dropped
the www and the scheme). The older file stays as it was, as the backup: revert() removes the newer file and the older
one is used again, and Forget takes a sign-in out of both. login_import.py brings sign-ins in from a password
manager's export or its command-line tool.
"""
import datetime as dt, hashlib, json, os, re, secrets, subprocess, sys, threading, time, urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'integrations'))
import browser_cdp  # noqa: E402
import message_seal  # noqa: E402
import portable  # noqa: E402
import timeutil
from machine.owner_error import OwnerError

LOOPBACK = ('127.0.0.1', 'localhost', '::1')
SEALED = 'browser-logins.sealed'  # sealed with the message key
STORE, KEY = 'browser-logins.enc', 'browser-logins.key'  # only without a message key, and what older versions kept
ACCOUNTS, ACCOUNTS_STORE = 'browser-logins.v2.sealed', 'browser-logins.v2.enc'  # accounts per site; the older file is its backup
DEFAULT_ACCOUNT = 'Default'
OPENSSL = 'openssl'
SETTLE = 10  # seconds a submitted page has to move on before the dialog says it is still there

# Finds the sign-in fields on the page: {u, p, c, next} (username, password, one-time code, a Next/Sign in button).
# Read-only, and never returns what is in a field.
_FIELDS = r'''
const fields = () => {
  const shown = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && !e.disabled && !e.readOnly; };
  const words = e => [e.name, e.id, e.autocomplete, e.getAttribute('aria-label'), e.placeholder].join(' ').toLowerCase();
  const inputs = [...document.querySelectorAll('input')].filter(shown);
  const texts = inputs.filter(e => /^(text|email|tel|number|)$/.test(e.type));
  const p = inputs.find(e => e.type === 'password' && e.autocomplete !== 'new-password');
  const c = texts.find(e => e.autocomplete === 'one-time-code' || (/otp|totp|2fa|mfa|one.?time|verif|security.?code|auth.?code|two.?factor|passcode|\bcode\b|\bpin\b/.test(words(e))
    && !/zip|post|promo|coupon|country|area|voucher/.test(words(e))));
  const named = e => e.autocomplete === 'username' || e.type === 'email' || /user|login|e-?mail|identifier|account|phone/.test(words(e));
  let u = texts.find(e => e !== c && named(e) && (!p || !p.form || e.form === p.form));
  if (!u && p) u = texts.filter(e => e !== c && e.form === p.form && (e.compareDocumentPosition(p) & 4)).pop();
  const buttons = [...document.querySelectorAll('button, input[type=submit], [role=button]')].filter(shown);
  const next = buttons.find(b => /^\s*(next|continue|sign ?in|log ?in|submit|verify|weiter|volgende|suivant|inloggen|aanmelden|anmelden|connexion)\b/i
    .test(b.innerText || b.value || b.getAttribute('aria-label') || ''));
  if (!p && !c && !(u && next && texts.length <= 2)) return null;  // a username alone counts on a short "Next" page only
  return {u, p, c, next};
};
'''

# What the page itself says around a one-time code field, so the dialog can say which code it wants: `ask`, the site's
# own words before the field (its label, heading and instructions); `error`, a message it flags (role=alert, an
# invalid field's description); `others`, the links and buttons that switch method or send the code again. Visible
# text only, never what is in a field: inputs carry no text, and buttons, links and form controls are left out.
_WORDS = r'''
const clean = t => (t || '').replace(/\s+/g, ' ').trim();
const ALERT = '[role=alert],[aria-live=assertive],[aria-invalid=true],[class*=error i],[id*=error i],[class*=invalid i]';
const CONTROL = 'a,button,[role=button],[role=link],input,textarea,select,option,script,style,noscript,svg,template';
const shownText = e => { const s = getComputedStyle(e); return s.visibility !== 'hidden' && s.display !== 'none' && e.getClientRects().length > 0; };
const inAlert = el => { const a = el.closest(ALERT); return !!a && !a.querySelector('input') && clean(a.innerText).length <= 300; };
// The visible text in `box`, per block (a paragraph, heading, label...): [{el, text}] in page order.
const blocks = box => {
  const found = new Map(), walk = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
  for (let n; (n = walk.nextNode());) {
    const el = n.parentElement;
    if (!clean(n.data) || !el || el.closest(CONTROL) || inAlert(el) || !shownText(el)) continue;
    const block = el.closest('p,h1,h2,h3,h4,h5,h6,label,legend,li,dt,dd,td,th,div,section,header,form,main,body') || el;
    found.set(block, (found.get(block) || '') + ' ' + n.data);
  }
  return [...found].map(([el, text]) => ({el, text: clean(text)}));
};
const asks = (c, f) => {
  const said = [], add = t => { t = clean(t); if (t && t.length <= 300 && !said.includes(t)) said.push(t); };
  for (const id of clean(c.getAttribute('aria-labelledby') + ' ' + c.getAttribute('aria-describedby')).split(' ')) {
    const e = id && id !== 'null' && document.getElementById(id); if (e && !inAlert(e) && shownText(e)) add(e.innerText);
  }
  let box = c.parentElement, before = [];
  for (let up = 0; box && up < 8; up++, box = box.parentElement) {  // widen until there are a few words before the field
    before = blocks(box).filter(b => b.el.compareDocumentPosition(c) & 4 || b.el.contains(c)).map(b => b.text);
    if (before.join(' ').split(' ').length >= 6 || box === document.body) break;
  }
  before.slice(-3).forEach(add);
  let text = said.join(' \u00b7 ');
  return text.length > 300 ? '\u2026' + text.slice(-299) : text;
};
const flagged = c => {
  const ids = clean(c.getAttribute('aria-describedby') + ' ' + c.getAttribute('aria-errormessage')).split(' ');
  const own = c.getAttribute('aria-invalid') === 'true' ? ids.map(id => id && document.getElementById(id)).filter(Boolean) : [];
  const all = [...own, ...document.querySelectorAll(ALERT)].filter(e => e.tagName !== 'INPUT' && shownText(e) && !e.querySelector('input'));
  const leaves = all.filter(e => clean(e.innerText).length > 2 && clean(e.innerText).length <= 300 && !all.some(o => o !== e && e.contains(o) && clean(o.innerText)));
  return leaves.length ? clean(leaves[0].innerText) : '';
};
// Another way to get the code, or a new one: the page's own links and buttons for it, on this site only. Never a
// button that submits the form with the code or password in it.
const OTHER = /\b(another|other|different|instead|alternative|switch|resend|re-send|new code|send (it |a |the )?(code )?again|send (a |the )?(new )?code|get (a )?(new )?code|didn.?t (get|receive)|did not (get|receive)|can.?t (use|access|get)|try (another|a different|again)|more options|use (a|an|your|my|the)\b|call me|text me|email me|by (phone|text|sms|email|call)|via (phone|text|sms|email))/i;
const others = f => {
  const shown = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && shownText(e) && !e.disabled; };
  const found = [];
  for (const e of document.querySelectorAll('a[href],button,[role=button],[role=link],input[type=button]')) {
    const label = clean(e.innerText || e.value || e.getAttribute('aria-label'));
    if (!label || label.length > 60 || found.some(o => o.label === label) || e === f.next || !shown(e) || !OTHER.test(label)) continue;
    if (/account|sign ?out|log ?out|password|cancel|privacy|terms|help\b/i.test(label)) continue;
    if (e.form && (e.type === 'submit' || e.type === 'image') && [f.c, f.p].some(x => x && x.form === e.form)) continue;
    if (e.tagName === 'A') { try { const u = new URL(e.getAttribute('href'), location.href);
      if (!/^(https?|javascript):$/.test(u.protocol) || (u.protocol !== 'javascript:' && u.origin !== location.origin)) continue; } catch (_) { continue; } }
    found.push({label, e});
    if (found.length >= 4) break;
  }
  return found;
};
'''

DETECT = '() => {' + _FIELDS + _WORDS + '''
  const f = fields();
  if (!f) return null;
  const found = {host: location.host, origin: location.origin, secure: location.protocol === 'https:', title: document.title.slice(0, 80),
                 username: !!f.u, password: !!f.p, code: !!f.c};
  if (f.c) {
    const meta = document.querySelector('meta[property="og:site_name"]');
    Object.assign(found, {ask: asks(f.c, f), error: flagged(f.c), others: others(f).map(o => o.label), step: location.pathname.slice(0, 200),
      field: [f.c.name, f.c.id, f.c.autocomplete, f.c.getAttribute('aria-label')].join(' ').slice(0, 200),
      name: meta ? clean(meta.content).slice(0, 40) : ''});
  }
  return found;
}'''

# Clicks one of `others` by its label, after checking the page is still on `host`. Never a field or a submit.
CHOOSE = 'function(host, label) {' + _FIELDS + _WORDS + '''
  if (location.host !== host) return 'moved';
  const f = fields(), pick = f && f.c && others(f).find(o => o.label === label);
  if (!pick) return 'missing';
  pick.e.scrollIntoView({block: 'center'}); pick.e.click();
  return 'clicked';
}'''

# Focuses one field after checking the page is still on `host` (and, for a saved sign-in, on one of its exact
# `origins`), and selects what is in it, so typing replaces it.
FOCUS = 'function(host, which, origins) {' + _FIELDS + '''
  if (location.host !== host || (origins && !origins.includes(location.origin))) return 'moved';
  const f = fields(), e = f && f[which];
  if (!e) return 'missing';
  e.scrollIntoView({block: 'center'}); e.focus();
  try { e.select(); } catch (_) { e.value = ''; }
  return 'ok';
}'''

SUBMIT = 'function(host, mark, origins) {' + _FIELDS + '''
  if (location.host !== host || (origins && !origins.includes(location.origin))) return 'moved';
  window.__machineLogin = mark;
  const f = fields() || {}, field = f.p || f.c || f.u, form = field && field.form;
  const button = (form && [...form.querySelectorAll('button:not([type=button]):not([type=reset]), input[type=submit]')].find(b => b.offsetParent)) || f.next;
  if (button) { button.click(); return 'clicked'; }
  if (form) { form.requestSubmit ? form.requestSubmit() : form.submit(); return 'submitted'; }
  return 'enter';
}'''

# Still the same document, with the field filled last still filled, after the submit? Then empty the password field (without events: the site already has it)
# so it does not stay readable in the page.
SETTLED = 'function(mark, which, clear) {' + _FIELDS + '''
  if (window.__machineLogin !== mark) return 'moved';
  const f = fields(), e = f && f[which];
  if (!e || !e.value) return 'changed';
  if (clear && which === 'p') Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(e, '');
  return 'same';
}'''


def _loopback(base):
    parsed = urllib.parse.urlsplit(base)
    return parsed.scheme == 'http' and parsed.hostname in LOOPBACK


def endpoints(config):
    """The DevTools addresses of the assistant's browsers: the shared one and each source account's own. Loopback only."""
    found = []
    for base in [config.get('browser_cdp_url') or 'http://127.0.0.1:9222'] + [a.get('browser_cdp') for a in config.get('accounts', [])]:
        if isinstance(base, str) and _loopback(base) and base.rstrip('/') not in found:
            found.append(base.rstrip('/'))
    return found


def site(host):
    host = str(host or '').lower().split(':')[0]
    return host[4:] if host.startswith('www.') else host


_PORTS = {'http': 80, 'https': 443}


def origin(address):
    """scheme://host[:port] of an address, as a browser's location.origin says it (lowercase, the host in punycode,
    no default port), or None for anything that is not an http(s) address with a host. A bare host is taken as https.
    Two addresses share a saved sign-in only when these are equal: a lookalike, a subdomain or http never match."""
    text = str(address or '').strip()
    if not text or len(text) > 2000 or any(c in text for c in '\r\n\t '):
        return None
    if '://' not in text:
        text = 'https://' + text
    try:
        parts = urllib.parse.urlsplit(text)
        scheme, host, port = parts.scheme.lower(), parts.hostname, parts.port
    except ValueError:
        return None
    if scheme not in _PORTS or not host or parts.username or parts.password:
        return None
    if ':' in host:
        host = '[' + host + ']'
    else:
        try:
            host = host.encode('idna').decode('ascii').lower()
        except UnicodeError:
            return None
    return f'{scheme}://{host}' + (f':{port}' if port and port != _PORTS[scheme] else '')


def origin_label(value):
    """An origin as the dashboard shows it: the host (and port), with the scheme only when it is not https."""
    value = str(value or '')
    return value[len('https://'):] if value.startswith('https://') else value


def _host_origins(host):
    """The origins a host the dialog or an older version named stands for: https on it (http on loopback)."""
    name = str(host or '').lower()
    return [o for o in [origin(('http://' if urllib.parse.urlsplit('//' + name).hostname in LOOPBACK else 'https://') + name)] if o]


def brand(host, name=''):
    """The site's name for the dialog: what the page calls itself (og:site_name), else its domain's own label
    (dashboard.stripe.com: Stripe; shop.example.co.uk: Example), else the host."""
    if name and len(name) <= 40:
        return name
    labels = site(host).split('.')
    if len(labels) < 2 or labels[-1].isdigit() or ':' in site(host):
        return site(host)
    label = labels[-3] if len(labels) >= 3 and len(labels[-1]) == 2 and len(labels[-2]) <= 3 else labels[-2]
    return label[:1].upper() + label[1:]


# Which code a page wants, by what it says. The page's own words decide, before what its field is called and its
# address: an authenticator app is named outright; a text message or an email is where it was sent (a masked number
# or address, "your phone", "your inbox"). General phrasing, never per site.
_MASK = '•*●·∙xX'
_PHONE_SENT = re.compile(r'(?i)(?:ending (?:in|with)|last (?:\w+ )?digits?(?: are| of)?)\s*:?\s*([\d]{2,4})\b|'
                         r'((?:\+\d{1,3}[\s.-]?)?(?:[(\[]?[' + _MASK + r'][' + _MASK + r'\s().\-]*)\d{2,4})\b')
_EMAIL_SENT = re.compile(r'[\w.+\-' + _MASK + r']*[\w' + _MASK + r']@[\w' + _MASK + r'.\-]+\.[a-z' + _MASK + r']{2,}', re.I)
_KINDS = (
    ('app', re.compile(r'(?i)\bauthenticat(?:or|ion) app|\bauthenticator\b|\btotp\b|\bauthy\b|code generator|'
                       r'\b(?:from|in|on|by|with) (?:the |your |an? )?(?:\w+ )?app\b|\bapp(?:lication)? (?:code|generates?)|generated by')),
    ('sms', re.compile(r'(?i)\bsms\b|\btext(?:ed| message)\b|\bby text\b|\bvia text\b|\btext(?:ed)? (?:you|it|a code)|'
                       r'\b(?:to|on) (?:your|the) (?:mobile|cell|phone)(?: number)?\b(?! app)|\bphone (?:number )?ending\b|\bmobile number\b')),
    ('email', re.compile(r'(?i)\be-?mail(?:ed)?\b|\binbox\b')),
    ('key', re.compile(r'(?i)\bsecurity key\b|\bpasskey\b|\byubikey\b|\bhardware key\b')),
)
_HINTS = (('app', re.compile(r'(?i)totp|authenticator|\bapp\b')), ('sms', re.compile(r'(?i)sms|phone|mobile')),
          ('email', re.compile(r'(?i)e-?mail')), ('key', re.compile(r'(?i)webauthn|security.?key|u2f')))


def _phone(ask):
    """(position, last digits) of a phone number the words say the code went to, masked as the site masks it."""
    for found in _PHONE_SENT.finditer(ask or ''):
        if found.group(1):
            return found.start(), found.group(1)
        if not any(c.isalpha() and c not in 'xX' for c in found.group(2)):
            return found.start(), re.findall(r'\d+', found.group(2))[-1]
    return None


def _email(ask):
    """(position, address) of an email address the words say the code went to: masked, or right after "to"."""
    for found in _EMAIL_SENT.finditer(ask or ''):
        if any(c in found.group(0) for c in '•*●·∙') or re.search(r'(?i)\bto\s*$', ask[:found.start()]):
            return found.start(), found.group(0)
    return None


def code_kind(ask, field='', step=''):
    """'sms', 'app', 'email', 'key' or 'unknown' for a one-time code page, from the site's own words (`ask`), then
    the code field's attributes and the address's path. An app named outright wins ("the authenticator app on your
    phone"); else the first channel the words name, where a destination shown masked (•••• 12, j•••@example.com)
    counts as naming it."""
    ask, found = ask or '', {}
    for kind, where in (('email', _email(ask)), ('sms', _phone(ask))):
        if where:
            found[kind] = where[0]
    for kind, pattern in _KINDS:
        hit = pattern.search(ask)
        if hit:
            found[kind] = min(found.get(kind, hit.start()), hit.start())
    if 'app' in found:
        return 'app'
    if found:
        return min(found, key=found.get)
    hints = (field or '') + ' ' + re.sub(r'[/_-]', ' ', step or '')
    return next((kind for kind, pattern in _HINTS if pattern.search(hints)), 'unknown')


def sent_to(ask, kind):
    """Where the site says it sent the code, as the site shows it (masked as it masks it), or ''."""
    where = _email(ask) if kind == 'email' else _phone(ask) if kind == 'sms' else None
    if not where:
        return ''
    return where[1] if kind == 'email' else 'ending in ' + where[1]


def describe(form):
    """A page from DETECT as the dialog shows it: for a code, which one (code_kind), the site's name and where it
    was sent. Drops what only served to tell."""
    if not isinstance(form, dict):
        return form
    form = dict(form)
    field, step = form.pop('field', ''), form.pop('step', '')
    form['brand'] = brand(form.get('host'), form.pop('name', ''))
    if form.get('code'):
        form['code_kind'] = code_kind(form.get('ask'), field, step)
        form['sent_to'] = sent_to(form.get('ask'), form['code_kind'])
    return form


def pages(config, store=None, account=None):
    """The open tabs that show a sign-in form: [{id, host, origin, title, username, password, code, saved, accounts}].
    `accounts`: the saved sign-ins bound to that page's exact origin, [{id, account, username}], never a password;
    `saved`: the first of them, as older dashboards read it. Looks in the browser of `account` (an account id) when it
    has one of its own, else in the shared one: asking a browser that is not running can start it."""
    found, bases = [], endpoints(config)
    for base, tab in _tabs(config, account):
        try:
            form = browser_cdp.evaluate(base, tab['id'], DETECT, timeout_ms=3000)
        except (browser_cdp.CdpError, OSError):
            continue
        if isinstance(form, dict) and form.get('host'):
            saved = store.for_origin(form.get('origin')) if store else []
            found.append({**describe(form), 'id': f'{bases.index(base)}:{tab["id"]}', 'site': site(form['host']),
                          'accounts': saved, 'saved': {'username': saved[0]['username']} if saved else None})
    return found


def _tabs(config, account=None):
    """(DevTools address, tab) for each web page open in the browser of `account` (an account id) when it has one of
    its own, else in the shared one."""
    own = next((a.get('browser_cdp') for a in config.get('accounts', []) if a.get('id') == account), None)
    for base in endpoints(config):
        if base != (own.rstrip('/') if isinstance(own, str) and _loopback(own) else endpoints(config)[0]):
            continue
        try:
            tabs = [t for t in browser_cdp._http(base, '/json/list', timeout=3) if t.get('type') == 'page']
        except (browser_cdp.CdpError, TypeError, AttributeError):
            continue
        for tab in tabs:
            if urllib.parse.urlsplit(tab.get('url') or '').scheme in ('http', 'https'):
                yield base, tab


_filling = threading.Lock()
_store_locks = {}
_store_locks_guard = threading.Lock()


def fill(config, page, host, username=None, password=None, code=None, settle=SETTLE, origins=None, seen=None):
    """Types what the owner gave into the sign-in page `page` (an id from pages()) on `host`, and submits it.
    `origins`: for a saved sign-in, the exact origins it is bound to; nothing is typed unless the page's own origin
    is one of them, checked before and while typing. `seen`: a dict that gets the 'origin' of the page it typed into.

    Returns {'result': 'next'|'done'|'approve'|'captcha'|'blocked'|'still_here', 'page': the sign-in form now shown, if
    any}. 'approve': no form left, but the tab is still at a sign-in step (approve
    it in the site's app); watch() says when it is past. 'captcha': that step is a robot check, for the browser itself.
    'blocked': after a code, the site asks for the username and password again (it stopped this sign-in).
    Errors are plain ValueErrors that never contain a value given here."""
    if origins is not None:
        origins = [o for o in origins if isinstance(o, str) and o]
        if not origins:
            raise OwnerError('That saved sign-in has no address to go to')
    index, _, target = str(page or '').partition(':')
    bases = endpoints(config)
    if not index.isdigit() or int(index) >= len(bases) or not target:
        raise OwnerError('That page is not open in the browser any more')
    base, given = bases[int(index)], {'u': username, 'p': password, 'c': code}
    given = {k: v for k, v in given.items() if isinstance(v, str) and v}
    if not given:
        raise OwnerError('Nothing to fill in')
    if any(len(v) > 1000 or '\n' in v or '\r' in v for v in given.values()):
        raise OwnerError('That is too long, or has a line break')
    if not _filling.acquire(timeout=30):
        raise OwnerError('Another sign-in is still going on')
    try:
        try:
            with browser_cdp.Session(base, target, timeout=20) as tab:
                form = tab.run('(' + DETECT + ')')
                if not form or form.get('host') != host:
                    raise OwnerError(f'The page in the browser is no longer the sign-in to {site(host)}')
                if not form['secure'] and urllib.parse.urlsplit('//' + host).hostname not in LOOPBACK:
                    raise OwnerError('That page is not on a secure (https) address; open the browser to sign in there')
                filled_origin = form.get('origin') if isinstance(form.get('origin'), str) else None
                if origins is not None and filled_origin not in origins:
                    raise OwnerError('That saved sign-in is for another address, so it was not filled in')
                if seen is not None:
                    seen['origin'] = filled_origin
                wanted = {k: v for k, v in given.items() if form[{'u': 'username', 'p': 'password', 'c': 'code'}[k]]}
                if not wanted:
                    raise OwnerError('The page does not ask for that right now')
                tab.call('Page.bringToFront')
                for which, value in wanted.items():
                    if tab.run(FOCUS, host, which, origins) != 'ok':
                        raise OwnerError(f'The page in the browser is no longer the sign-in to {site(host)}')
                    tab.call('Input.insertText', {'text': value})
                mark, last = secrets.token_hex(8), 'p' if 'p' in wanted else 'c' if 'c' in wanted else 'u'
                how = tab.run(SUBMIT, host, mark, origins)
                if how == 'moved':
                    raise OwnerError(f'The page in the browser is no longer the sign-in to {site(host)}')
                if how == 'enter':
                    for kind in ('keyDown', 'keyUp'):
                        tab.call('Input.dispatchKeyEvent', {'type': kind, 'key': 'Enter', 'code': 'Enter',
                                                            'windowsVirtualKeyCode': 13, 'text': '\r' if kind == 'keyDown' else ''})
        except browser_cdp.CdpError:
            raise OwnerError('The browser did not take that; open the browser to sign in there') from None
        state, until = 'same', time.monotonic() + settle
        while time.monotonic() < until:
            time.sleep(0.5)
            try:
                with browser_cdp.Session(base, target, timeout=5) as tab:
                    state = tab.run(SETTLED, mark, last, False)
            except browser_cdp.CdpError:
                state = 'moved'  # mid-navigation; look again
                continue
            if state != 'same':
                break
        if state == 'same':
            try:
                with browser_cdp.Session(base, target, timeout=5) as tab:
                    state = tab.run(SETTLED, mark, last, True)
            except browser_cdp.CdpError:
                pass
        time.sleep(1.5 if state != 'same' else 0)  # the next step's page settles
        shown = None
        try:
            shown = describe(browser_cdp.evaluate(base, target, DETECT, timeout_ms=3000))
        except browser_cdp.CdpError:
            raise OwnerError('The browser did not answer after submitting; could not confirm the sign-in') from None
        if state == 'same':
            return {'result': 'still_here', 'page': shown and {**shown, 'id': page, 'site': site(shown['host'])}}
        if shown:
            # a code sent, and the site asks for the username and password again: it stopped this sign-in
            back = 'c' in wanted and shown.get('username') and shown.get('password') and not shown.get('code')
            return {'result': 'blocked' if back else 'next', 'page': {**shown, 'id': page, 'site': site(shown['host'])}}
        if _wall(base, target):  # the site put a bot wall up instead of letting the sign-in through
            return {'result': 'captcha', 'page': {'id': page, 'host': host, 'site': site(host)}}
        if _checkpoint(base, target):  # nothing to type, but not in yet: a robot check, or approve it in the site's app
            return {'result': 'captcha' if _captcha(base, target) else 'approve', 'page': {'id': page, 'host': host, 'site': site(host)}}
        return {'result': 'done', 'page': None}
    finally:
        _filling.release()


def choose(config, page, host, label, settle=2.0):
    """Clicks one of the page's own "another way" links or buttons (`others`: use the authenticator app instead,
    resend the code), by its label, and returns what it shows then, like fill(): {'result': 'next', 'page'} with a
    sign-in form, else {'result': 'elsewhere', 'page': None} (finish in the browser). Types nothing and submits no
    field."""
    index, _, target = str(page or '').partition(':')
    bases = endpoints(config)
    if not index.isdigit() or int(index) >= len(bases) or not target:
        raise OwnerError('That page is not open in the browser any more')
    if not isinstance(label, str) or not label or len(label) > 60:
        raise OwnerError('Which one?')
    base = bases[int(index)]
    if not _filling.acquire(timeout=30):
        raise OwnerError('Another sign-in is still going on')
    try:
        try:
            with browser_cdp.Session(base, target, timeout=20) as tab:
                form = tab.run('(' + DETECT + ')')
                if not form or form.get('host') != host:
                    raise OwnerError(f'The page in the browser is no longer the sign-in to {site(host)}')
                if tab.run(CHOOSE, host, label) != 'clicked':
                    raise OwnerError(f'{brand(host)} doesn’t show “{label}” any more; open the browser to see what it shows')
        except browser_cdp.CdpError:
            raise OwnerError('The browser did not take that; open the browser to sign in there') from None
        shown, until = None, time.monotonic() + settle + 4
        time.sleep(settle)
        while True:
            try:
                shown = describe(browser_cdp.evaluate(base, target, DETECT, timeout_ms=3000))
                break
            except browser_cdp.CdpError:  # mid-navigation
                if time.monotonic() > until:
                    break
                time.sleep(0.5)
        if shown:
            return {'result': 'next', 'page': {**shown, 'id': page, 'site': site(shown['host'])}}
        return {'result': 'elsewhere', 'page': None}
    finally:
        _filling.release()


# A tab address that is still part of signing in, with nothing to type: approving it in the site's own app (LinkedIn's
# checkpoint), a two-step or verification page, a challenge.
CHECKPOINT = re.compile(r'(?i)checkpoint|challenge|/2fa|/mfa|two.?(step|factor)|verif|approv|log-?in|sign-?in|/uas/|/auth\b')
ADDRESS = '() => location.pathname + location.search'


# A robot check on the page (reCAPTCHA, hCaptcha, Arkose, Cloudflare's): only someone at the browser can do it.
# By what the page is made of (its frames and their sources), never what it says.
CAPTCHA = r'''() => [...document.querySelectorAll('iframe[src], [id*="captcha" i], [class*="captcha" i]')].some(e => {
  const r = e.getBoundingClientRect();
  return r.width > 0 && r.height > 0 && (e.tagName !== 'IFRAME' || /captcha|arkoselabs|funcaptcha|challenges\.cloudflare\.com/i.test(e.src)); })'''


# A whole page that is a bot wall in front of the site: Cloudflare's browser check (its challenge script and form) or
# its block page, DataDome's or PerimeterX's check. Sites often show one to a browser in the cloud. By what the page is
# made of (its scripts, forms, frames and the block page's own markup), never what it says.
WALL = r'''() => !!(window._cf_chl_opt || document.querySelector([
  'script[src*="/cdn-cgi/challenge-platform/"]', 'form#challenge-form', '[data-translate="block_headline"]',
  'iframe[src*="challenges.cloudflare.com"]', 'iframe[src*="captcha-delivery.com"]', '#px-captcha'].join()))'''


def _wall(base, target):
    try:
        return browser_cdp.evaluate(base, target, WALL, timeout_ms=3000) is True
    except (browser_cdp.CdpError, OSError):
        return False


def walls(config, account=None):
    """The open tabs that show a bot wall rather than a sign-in form: [{host, site}]. Read-only, like pages()."""
    found = []
    for base, tab in _tabs(config, account):
        if _wall(base, tab['id']):
            host = urllib.parse.urlsplit(tab.get('url') or '').hostname or ''
            found.append({'host': host, 'site': site(host)})
    return found


def _checkpoint(base, target):
    try:
        return bool(CHECKPOINT.search(str(browser_cdp.evaluate(base, target, ADDRESS, timeout_ms=3000) or '')))
    except (browser_cdp.CdpError, OSError):
        return False


def _captcha(base, target):
    try:
        return browser_cdp.evaluate(base, target, CAPTCHA, timeout_ms=3000) is True
    except (browser_cdp.CdpError, OSError):
        return False


def watch(config, page):
    """How the sign-in in tab `page` (an id from pages()) is going, after the dialog sent it: {'state': 'form', 'page'}
    when the page asks for something to type, 'waiting' while it waits on the owner elsewhere (their phone's app),
    'captcha' at a robot check (for the browser itself), 'done' once past it. Read-only: which fields show and the tab's address, never what is in them."""
    index, _, target = str(page or '').partition(':')
    bases = endpoints(config)
    if not index.isdigit() or int(index) >= len(bases) or not target:
        raise OwnerError('That page is not open in the browser any more')
    base = bases[int(index)]
    try:
        if not any(t.get('id') == target for t in browser_cdp._http(base, '/json/list', timeout=3)):
            raise OwnerError('That page is not open in the browser any more')
        shown = describe(browser_cdp.evaluate(base, target, DETECT, timeout_ms=3000))
    except (browser_cdp.CdpError, OSError, TypeError, AttributeError):
        return {'state': 'waiting'}  # mid-navigation, or the browser is slow: look again
    if isinstance(shown, dict) and shown.get('host'):
        return {'state': 'form', 'page': {**shown, 'id': page, 'site': site(shown['host'])}}
    if _wall(base, target):  # not past it: a bot wall is not a signed-in page
        return {'state': 'captcha'}
    if _checkpoint(base, target):
        return {'state': 'captcha' if _captcha(base, target) else 'waiting'}
    return {'state': 'done'}


class LoginStore:
    """Saved sign-ins, encrypted at rest: sealed with the message key, or, without one, AES-256 with openssl and a key
    in a file of its own (KEY). Only the service reads them; list() and for_origin() never return a password, and no
    error quotes one.

    The current file (ACCOUNTS, or ACCOUNTS_STORE without a message key) holds {'version': 2, 'logins': [{id, origins,
    account, username, password, saved_at, source}], 'picks': {to-do id: login id}}. The older file (SEALED or STORE)
    held {site: {username, password, saved_at}}, one per site: until the current file exists it is read as that, each
    site one "Default" account; once it does, the older file is only the backup that revert() goes back to."""

    def __init__(self, folder):
        self.folder = Path(folder)
        self.sealed_path = self.folder / SEALED
        self.path, self.key_path = self.folder / STORE, self.folder / KEY
        self.accounts_path, self.accounts_store = self.folder / ACCOUNTS, self.folder / ACCOUNTS_STORE
        # API requests construct separate stores, but their read/change/write must share one lock.
        with _store_locks_guard:
            self.lock = _store_locks.setdefault(str(self.sealed_path.resolve()), threading.Lock())

    def _message_key(self):
        """The message key next to the database in this folder (a link to memory on a hosted Machine), or None."""
        try:
            return message_seal.load_key(self.sealed_path)  # the key of anything in this folder: its key_path
        except (OSError, ValueError):
            return None

    def _key(self):
        if not self.key_path.exists():
            fd = os.open(self.key_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w') as handle:
                handle.write(secrets.token_hex(32))
        return self.key_path.read_text().strip()

    def _openssl(self, data, decrypt):
        run = subprocess.run([OPENSSL, 'enc', '-aes-256-cbc', '-pbkdf2', '-iter', '100000', '-md', 'sha256', '-salt',
                              *(['-d'] if decrypt else []), '-pass', 'env:MACHINE_LOGIN_KEY'],
                             input=data, capture_output=True, env={**os.environ, 'MACHINE_LOGIN_KEY': self._key()})
        if run.returncode:
            raise OwnerError('Saved sign-ins could not be ' + ('read' if decrypt else 'saved'))
        return run.stdout

    def _read_file(self, sealed, own):
        """What one pair of files holds (`sealed` with the message key, `own` with the key of its own), or None when
        neither is there. A file opened by an export and put here by an import, or one still under the key of its own
        while there is a message key, is encrypted again with the message key at once."""
        key = self._message_key()
        if sealed.exists():
            data = sealed.read_bytes()
            if message_seal.is_sealed_bytes(data):
                if not key:
                    raise OwnerError('Saved sign-ins are encrypted with the message key, which is not here '
                                     + ('yet' if message_seal.held_elsewhere(sealed) else 'any more'))
                try:
                    return json.loads(message_seal.Sealer(key).open_bytes(data))
                except message_seal.SealError:
                    raise OwnerError('Saved sign-ins could not be read') from None
            try:
                content = json.loads(data)
            except ValueError:
                raise OwnerError('Saved sign-ins could not be read') from None
            self._write_file(sealed, own, content)
            return content
        if own.exists():
            content = json.loads(self._openssl(own.read_bytes(), True))
            if key:  # a message key now: over to it, and the old file goes
                self._write_file(sealed, own, content)
            return content
        return None

    def _write_file(self, sealed, own, content):
        key = self._message_key()
        if key:
            target, data = sealed, message_seal.Sealer(key).seal_bytes(json.dumps(content).encode())
        elif message_seal.held_elsewhere(sealed):
            raise OwnerError('Saved sign-ins wait for the message key ' + ('from your keyring' if message_seal.in_keyring(sealed) else 'your hosting keeps')
                             + '; try again in a minute')
        else:
            target, data = own, self._openssl(json.dumps(content).encode(), False)
        temp = target.with_name(target.name + '.tmp')
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, target)
        portable.shred(own if key else sealed)
        if key and not (self.path.exists() or self.accounts_store.exists()):
            portable.shred(self.key_path)  # nothing left under the key of its own

    def _older(self):
        return self._read_file(self.sealed_path, self.path)

    def _read(self):
        """The current sign-ins: {'version': 2, 'logins': [...], 'picks': {...}}; from the older file, as Default
        accounts, while the current one isn't there yet."""
        doc = self._read_file(self.accounts_path, self.accounts_store)
        if isinstance(doc, dict) and doc.get('version') == 2:
            doc.setdefault('logins', [])
            doc.setdefault('picks', {})
            return doc
        return {'version': 2, 'logins': upgrade(self._older() or {}), 'picks': {}}

    def _write(self, doc):
        self._write_file(self.accounts_path, self.accounts_store, doc)

    def migrate(self):
        """At the service's start: the older file (or one opened by an import) goes over to the message key, and the
        current file is written from it when there isn't one yet, the older file staying as its backup. Running it
        again changes nothing. Returns whether anything moved."""
        with self.lock:
            moved = False
            key = self._message_key()
            try:
                for sealed, own in ((self.sealed_path, self.path), (self.accounts_path, self.accounts_store)):
                    plain = sealed.exists() and not message_seal.is_sealed_file(sealed)
                    if plain or (key and own.exists()):
                        self._read_file(sealed, own)
                        moved = True
                if not (self.accounts_path.exists() or self.accounts_store.exists()) and (self.sealed_path.exists() or self.path.exists()):
                    self._write({'version': 2, 'logins': upgrade(self._older() or {}), 'picks': {}})
                    moved = True
            except OwnerError:
                return moved  # the message key isn't here yet: the next start does it
            return moved

    def revert(self):
        """Undoes the move to accounts: the current file goes, and the older file (its backup, less anything forgotten
        since) is used again. Sign-ins saved since the move go with it. Returns whether there was anything to undo."""
        with self.lock:
            found = self.accounts_path.exists() or self.accounts_store.exists()
            for path in (self.accounts_path, self.accounts_store):
                portable.shred(path)
            if not self.path.exists() and self.key_path.exists() and not self.accounts_store.exists():
                portable.shred(self.key_path)
            return found

    # Reading

    def get(self, login):
        """One saved sign-in with its password, by its id; or, for a host or address, the one bound to that origin
        (its Default account, else the only one). None when there is none."""
        with self.lock:
            logins = self._read()['logins']
        found = next((e for e in logins if e.get('id') == login), None)
        if found:
            return dict(found)
        wanted = origin(login) if '://' in str(login or '') else (_host_origins(login) or [None])[0]
        here = [e for e in logins if wanted in e.get('origins', ())]
        pick = next((e for e in here if e.get('account') == DEFAULT_ACCOUNT), None) or (here[0] if len(here) == 1 else None)
        return dict(pick) if pick else None

    def for_origin(self, page_origin):
        """The saved sign-ins bound to this exact origin: [{id, account, username}], never a password."""
        if not page_origin:
            return []
        with self.lock:
            logins = self._read()['logins']
        return [{'id': e['id'], 'account': e.get('account') or DEFAULT_ACCOUNT, 'username': e.get('username') or ''}
                for e in sorted(logins, key=_order) if page_origin in e.get('origins', ())]

    def list(self):
        with self.lock:
            logins = self._read()['logins']
        # whether a password is kept, never the password or anything from it (not even its length)
        return [{'id': e['id'], 'site': origin_label(e['origins'][0]), 'origin': e['origins'][0],
                 'account': e.get('account') or DEFAULT_ACCOUNT, 'username': e.get('username') or '',
                 'saved_at': e.get('saved_at'), 'password_saved': bool(e.get('password')), 'source': e.get('source') or 'dialog'}
                for e in sorted(logins, key=_order) if e.get('origins')]

    def pick(self, page_origin, task=None, area=None):
        """Which saved sign-in a to-do uses on this origin: the one the owner chose for it before; else the only one;
        else the account named for the to-do's side ('work' or 'personal', or its company's name); else None, and the
        dialog asks once."""
        here = self.for_origin(page_origin)
        if not here:
            return None
        if task:
            with self.lock:
                chosen = self._read()['picks'].get(task)
            if any(e['id'] == chosen for e in here):
                return chosen
        if len(here) == 1:
            return here[0]['id']
        names = [str(n).lower() for n in area_names(area)]
        matched = [e for e in here if e['account'].lower() in names]
        return matched[0]['id'] if len(matched) == 1 else None

    # Changing

    def save(self, where, username=None, password=None, account=None, source='dialog'):
        """Keeps a sign-in for an origin (or a host, taken as https) under `account` (Default when not named), replacing
        what that account had there. Returns its id."""
        bound = [origin(where)] if '://' in str(where or '') else _host_origins(where)
        bound = [o for o in bound if o]
        if not bound:
            raise OwnerError('That address can’t keep a sign-in')
        name = account_name(account)
        with self.lock:
            doc = self._read()
            entry = next((e for e in doc['logins'] if bound[0] in e.get('origins', ()) and (e.get('account') or DEFAULT_ACCOUNT).lower() == name.lower()), None)
            if entry is None:
                entry = {'id': secrets.token_hex(8), 'origins': bound, 'account': name}
                doc['logins'].append(entry)
            if username:
                entry['username'] = username
            if password:
                entry['password'] = password
            entry['saved_at'], entry['source'] = timeutil.stamp(), source
            self._write(doc)
            return entry['id']

    def save_many(self, items, account=None, source='import'):
        """Keeps several sign-ins at once ([{origin, username, password}], each with its own `account` or the one
        given), in one write. Returns how many."""
        with self.lock:
            doc = self._read()
            count = 0
            for item in items:
                bound = origin(item.get('origin'))
                if not bound or not (item.get('username') or item.get('password')):
                    continue
                name = account_name(item.get('account') or account)
                entry = next((e for e in doc['logins'] if bound in e.get('origins', ()) and (e.get('account') or DEFAULT_ACCOUNT).lower() == name.lower()), None)
                if entry is None:
                    entry = {'id': secrets.token_hex(8), 'origins': [bound], 'account': name}
                    doc['logins'].append(entry)
                entry.update({k: item[k] for k in ('username', 'password') if item.get(k)})
                entry['saved_at'], entry['source'] = timeutil.stamp(), source
                count += 1
            if count:
                self._write(doc)
            return count

    def remember(self, task, login):
        """The owner chose this saved sign-in for this to-do: it uses that one again without asking."""
        if not (isinstance(task, str) and task and isinstance(login, str)):
            return
        with self.lock:
            doc = self._read()
            if not any(e.get('id') == login for e in doc['logins']):
                return
            doc['picks'] = {k: v for k, v in list(doc['picks'].items())[-199:] if k != task}
            doc['picks'][task] = login
            self._write(doc)

    def rename(self, login, account):
        """Names a saved sign-in's account: Work, Personal, a name of the owner's own, or Default (not set) again. The
        list keeps it changeable, so a wrong mark is undone there. Refuses a name another account on the same address
        already has. The to-dos that remembered this sign-in forget it, so each picks again by the new name (the only
        one, the one for its side, or the dialog asks once). Returns whether it changed."""
        name = account_name(account)
        with self.lock:
            doc = self._read()
            entry = next((e for e in doc['logins'] if e.get('id') == login), None)
            if entry is None:
                raise OwnerError('That sign-in isn’t saved any more')
            if (entry.get('account') or DEFAULT_ACCOUNT) == name:
                return False
            if any(e is not entry and set(e.get('origins', ())) & set(entry.get('origins', ()))
                   and (e.get('account') or DEFAULT_ACCOUNT).lower() == name.lower() for e in doc['logins']):
                raise OwnerError('That site already has a sign-in for ' + name)
            entry['account'] = name
            doc['picks'] = {k: v for k, v in doc['picks'].items() if v != login}
            self._write(doc)
            return True

    def forget(self, login):
        """Forgets one saved sign-in by its id, or every account of a site by its host. Also from the older file
        kept as the backup, so a forgotten password is nowhere. Returns whether anything went."""
        with self.lock:
            doc = self._read()
            gone = [e for e in doc['logins'] if e.get('id') == login]
            if not gone and isinstance(login, str) and '://' not in login:
                wanted = set(_host_origins(login)) | set(_host_origins('www.' + site(login)))
                gone = [e for e in doc['logins'] if wanted & set(e.get('origins', ()))]
            if not gone:
                return False
            doc['logins'] = [e for e in doc['logins'] if e not in gone]
            ids = {e['id'] for e in gone}
            doc['picks'] = {k: v for k, v in doc['picks'].items() if v not in ids}
            self._write(doc)
            older_sites = {e['older'] for e in gone if e.get('older')}
            if older_sites:
                older = self._older() or {}
                if older_sites & set(older):
                    self._write_file(self.sealed_path, self.path, {k: v for k, v in older.items() if k not in older_sites})
            return True

    def forget_all(self):
        """Every saved sign-in, and the backup, gone. Returns how many there were."""
        with self.lock:
            count = len(self._read()['logins'])
            for path in (self.accounts_path, self.accounts_store, self.sealed_path, self.path, self.key_path):
                portable.shred(path)
            return count


def _order(entry):
    return (site((entry.get('origins') or [''])[0].split('://')[-1]), (entry.get('origins') or [''])[0],
            (entry.get('account') or '') != DEFAULT_ACCOUNT, (entry.get('account') or '').lower())


def account_name(value):
    """An account's name as kept: trimmed, at most 40 characters, Default when empty."""
    name = re.sub(r'\s+', ' ', str(value or '')).strip()[:40]
    return name or DEFAULT_ACCOUNT


def side_of(area):
    """The account a new sign-in for a to-do is saved under by default: Personal for its Personal side, Work for
    its Work side, None when there is no to-do."""
    if not area:
        return None
    return 'Personal' if str(area).lower() == 'personal' else 'Work'


def area_names(area):
    """The account names that fit a to-do's area: 'personal' for Personal; for Work, 'work' and the company's name
    ('work:Acme' or 'Acme')."""
    if not area:
        return []
    area = str(area)
    if area.lower() == 'personal':
        return ['personal']
    company = area.partition(':')[2] if area.lower().startswith('work:') else ('' if area.lower() == 'work' else area)
    return ['work'] + ([company] if company else [])


def upgrade(older):
    """The older file's {site: {username, password, saved_at}} as accounts: each one Default, bound to https on the
    site and on its www (the older key had dropped both), and marked with the site it came from."""
    logins = []
    for name, entry in sorted((older or {}).items()):
        if not isinstance(entry, dict):
            continue
        bound = _host_origins(name)
        if bound and bound[0].startswith('https://') and not name.startswith('www.') and not re.fullmatch(r'[\d.]+', name):
            bound.append(origin('https://www.' + name))
        if not bound:
            continue
        logins.append({'id': hashlib.sha256(('older:' + name).encode()).hexdigest()[:16], 'origins': [o for o in bound if o],
                       'account': DEFAULT_ACCOUNT, 'username': entry.get('username') or '', 'password': entry.get('password') or '',
                       'saved_at': entry.get('saved_at'), 'source': 'dialog', 'older': name})
    return logins
