"""Birthdays from Facebook (docs/help/routines.md, "Templates"): the owner's friends' birthdays, read once from
Facebook's birthdays page in The Machine's own browser, matched to people in the Graph and kept only on the owner's OK.

Only on the owner's tap, on the Birthdays template's one to-do (birthdays_facebook_app.py): never in the background,
never on a schedule. A new import is their tap again. Read through the browser the other readers already use (LinkedIn,
X: the shared browser at browser_cdp_url, under the shared browser lease), the way the owner would: open the page in a
tab of its own, scroll it to the end, read each friend's name and birthday as the page has them, close the tab. No
sign-in is handled here: a browser that isn't signed in to Facebook is told to the owner, and the read stops.

What is kept: only each matched person's birthday (month and day, the year when the page shows it), as the one
birthday their page shows (person_birthday.offer, source facebook), which the Birthdays routine reads. One the owner set
or removed on the person's page stays. Nothing else from Facebook is kept: no link, photo or ID. The names read are for
matching and for the Add button (below), and live only on the to-do until the owner reads again. After Save the
to-do keeps who was saved (their Graph id and name), to link to their pages.

Matching never makes a new person: the same full name as exactly one person in the Graph (else the same first and last
name, one with a middle name the other doesn't have). Two people with that name is ambiguous: skipped, and named in the
preview so the owner can add it themselves.

Friends nobody in the Graph has (others) become people only on the owner's tap on Add (add): each a person added
by hand (graph.create_record), with their name and birthday (source facebook) and Type Personal, so never shared with a
Work Fleet (shared_graph.Scope). Matched again at that moment, so anyone who now has the same name as a person in the
Graph is skipped. One transaction for all of them; their pages show at once and the rest of the Graph follows in one
build. Nothing is looked up for them: no address, so no lookup, and no messages, so no summary or embedding. Undo
(remove) takes exactly those people away again.

Table (this module owns it): facebook_birthdays, one row per to-do: its state and, while it waits on the owner, the
preview."""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'integrations'))
import birthdays  # noqa: E402
import browser_cdp  # noqa: E402
import crm_import  # noqa: E402
import enrichment  # noqa: E402
import graph  # noqa: E402
import graph_show  # noqa: E402
import person_birthday  # noqa: E402

PAGE = 'https://www.facebook.com/events/birthdays/'
SOURCE = 'facebook'
STATES = ('reading', 'signed_out', 'failed', 'preview', 'saved')
READ_MINUTES = 8  # a read that still says reading after this ended without a word (a restart): it failed
SHOWN = 8  # matched people the preview names; the rest is a count
AMBIGUOUS_SHOWN = 20
ADD_MAX = 5000  # friends one Add adds at most
PERSONAL = {'side': 'personal'}  # their Type, as the owner sets it on a person's page (person_edits)

# Months as the page may write them, in the languages the app speaks (and their short forms)
MONTHS = {}
for _n, _names in enumerate((
        'january jan januari janvier janv enero ene gennaio gen janeiro januar jänner',
        'february feb februari fevrier février fevr févr febrero febbraio fevereiro fev februar',
        'march mar maart mars marzo março marco märz marz',
        'april apr avril avr abril aprile',
        'may mei mai mayo maggio mag maio',
        'june jun juni juin junio giugno giu junho',
        'july jul juli juillet juil julio luglio lug julho',
        'august aug augustus aout août agosto ago',
        'september sep sept septembre septiembre settembre set setembro',
        'october oct oktober octobre octubre ottobre ott outubro out okt',
        'november nov novembre noviembre novembro',
        'december dec dez december décembre decembre diciembre dic dicembre dezembro dezember'), start=1):
    for _word in _names.split():
        MONTHS.setdefault(_word, _n)
WEEKDAYS = set('monday tuesday wednesday thursday friday saturday sunday mon tue wed thu fri sat sun maandag dinsdag woensdag '
               'donderdag vrijdag zaterdag zondag montag dienstag mittwoch donnerstag freitag samstag sonntag lundi mardi mercredi '
               'jeudi vendredi samedi dimanche lunes martes miercoles jueves viernes sabado domingo lunedi martedi mercoledi giovedi '
               'venerdi segunda terca quarta quinta sexta feira'.split())
TODAY_WORDS = ('today', 'vandaag', 'heute', "aujourd'hui", 'aujourd’hui', 'hoy', 'oggi', 'hoje')
_MON = r'(?P<mon>[^\W\d_]{3,10})\.?'
_YEAR = r'(?:,?\s+(?:de\s+)?(?P<year>(?:19|20)\d{2}))?'
DATES = (
    re.compile(_MON + r'\s+(?P<day>\d{1,2})(?:st|nd|rd|th)?' + _YEAR + r'\W*$', re.I),          # November 14, 1990
    re.compile(r'(?P<day>\d{1,2})(?:\.|er|º)?\s+(?:de\s+)?' + _MON + _YEAR + r'\W*$', re.I),   # 14 november / 14. November / 14 de noviembre
    re.compile(r'(?P<a>\d{1,2})[/.-](?P<b>\d{1,2})(?:[/.-](?P<year>(?:19|20)\d{2}))?\W*$'),     # 11/14, 14.11.1990
)
SEPARATORS = ' \t\n,;:·•|()[]-–—'

# Run in the page (browser_cdp.Session.run, with LIMITS and the months): whether Facebook shows its sign-in instead; then
# scrolled down round by round, as the page loads more months, keeping every friend it shows on the way.
# Each friend is read from the page's own data where it has some (each friend's name and birthdate, in the data the page
# came with and in what it loads as it is scrolled: Facebook's page works this way, and the pictures under its months say
# only a name). Else from each profile picture's label (aria-label, title, its image's alt) with the heading above it,
# kept as it is scrolled past, so a page that drops what was scrolled past still counts it; without a date in any label,
# each picture is hovered once and its tooltip read.
# When it stops: once every month has its section or friends (the current one may sit under Today or Upcoming instead),
# after SETTLE rounds in a row with nothing new. A page that keeps growing, or keeps a busy part on screen, doesn't hold it
# up. With months still missing, IDLE ms with nothing new end it: nobody has a birthday then, and the preview names them
# (missing). The limits (items, ms) are a safety net well above Facebook's 5,000 friends: capped only when one stopped it.
# Each round waits for the page as long as it needs and no longer: on as soon as it grows, else after PAUSE ms (BUSY ms
# more while it shows a progress bar or busy part). Reads only; nothing is clicked or typed.
LIMITS = {'items': 6000, 'ms': 360000, 'idle': 20000, 'settle': 2, 'pause': 800, 'busy': 1200}
READ_JS = r'''async function (limits) {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  for (let i = 0; i < 40 && document.readyState !== 'complete'; i++) await wait(250);
  const signin = () => /^\/(login|checkpoint)/.test(location.pathname) || !!document.querySelector('input[name="pass"], form#login_form, form[action*="/login"]');
  if (signin()) return {error: 'signed-out'};
  const clean = t => String(t || '').replace(/\s+/g, ' ').trim();
  const headingsNow = () => [...document.querySelectorAll('h1, h2, h3, h4, [role=heading]')];
  const headingOf = (el, headings) => { let found = ''; for (const h of headings) { if (h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) found = clean(h.innerText || h.textContent); else break; } return found.slice(0, 60); };
  const pictures = () => [...document.querySelectorAll('a, [role=link], [role=button], [aria-label], [title]')]
    .filter(el => el.querySelector('img, image, svg image') || /^(img|image)$/i.test(el.tagName));
  const labelOf = el => { const img = el.querySelector('img, image'); return clean(el.getAttribute('aria-label') || el.getAttribute('title') || el.getAttribute('data-tooltip-content') || (img && (img.getAttribute('alt') || img.getAttribute('aria-label')))); };
  const busy = () => !!document.querySelector('[role=progressbar], [aria-busy=true]');
  const fold = t => t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const monthOf = t => { const m = [...new Set((fold(t).match(/\p{L}{3,10}/gu) || []).map(w => limits.months[w]).filter(Boolean))]; return m.length === 1 ? m[0] : 0; };
  // The page's own data: every object with a name and a birthdate (month, day, maybe year), once per friend
  const people = new Map();
  const take = (o, depth) => {
    if (!o || typeof o !== 'object' || depth > 100) return;
    const b = o.birthdate;
    if (b && typeof b === 'object' && typeof o.name === 'string' && +b.month && +b.day) {
      const key = String(o.id || o.name), had = people.get(key);
      if (!had || (+b.year && !had.year)) people.set(key, {name: clean(o.name).slice(0, 160), month: +b.month, day: +b.day, year: +b.year || null});
    }
    for (const v of Array.isArray(o) ? o : Object.values(o)) if (v && typeof v === 'object') take(v, depth + 1);
  };
  const eat = text => {
    text = String(text || '').replace(/^\s*for\s*\(;;\);/, '');
    if (!text.includes('birthdate')) return;
    try { take(JSON.parse(text), 0); return; } catch (e) {}
    for (const line of text.split('\n')) if (line.includes('birthdate')) { try { take(JSON.parse(line), 0); } catch (e) {} }  // one answer a line
  };
  for (const s of document.querySelectorAll('script[type="application/json"]')) eat(s.textContent);
  const open = XMLHttpRequest.prototype.open, fetched = window.fetch;
  XMLHttpRequest.prototype.open = function (method, url) {
    if (/graphql/i.test(String(url))) this.addEventListener('load', () => { try { eat(this.responseText); } catch (e) {} });
    return open.apply(this, arguments);
  };
  window.fetch = function () {
    const answer = fetched.apply(this, arguments);
    answer.then(r => { if (/graphql/i.test(String(r.url))) r.clone().text().then(eat, () => {}); }, () => {});
    return answer;
  };
  const missing = () => { const hs = headingsNow().map(h => clean(h.innerText || h.textContent));
    const have = new Set(hs.map(monthOf)), other = hs.some(h => h && !monthOf(h));
    for (const p of people.values()) have.add(p.month);
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].filter(m => !have.has(m) && !(m === limits.month && other)); };
  const seen = new Map();
  const collect = () => { if (people.size) return;  // the data has them: no labels needed
    const headings = headingsNow();
    for (const el of pictures()) { const label = labelOf(el); if (!label) continue; const heading = headingOf(el, headings);
      const key = label + '\n' + heading; if (!seen.has(key)) seen.set(key, {label, heading}); } };
  const count = () => people.size + seen.size;
  const start = Date.now();
  let capped = false, settled = 0, rounds = 0, extra = 0, last = Date.now(), gaps = missing().length;
  try {
    collect();
    for (;;) {
      const done = !gaps;
      if (done ? settled >= limits.settle : Date.now() - last > limits.idle) break;
      if (count() >= limits.items || Date.now() - start > limits.ms) { capped = true; break; }
      const before = count(), height = document.documentElement.scrollHeight;
      window.scrollBy(0, -400);  // up a little first, so the page sees a scroll to its end even when it didn't grow
      await wait(50);
      window.scrollTo(0, document.documentElement.scrollHeight);
      rounds++;
      if (done) extra++;
      const grew = () => count() !== before || document.documentElement.scrollHeight !== height;
      for (let t = 0; t < limits.pause && !grew(); t += 100) await wait(100);
      for (let t = 0; t < limits.busy && !grew() && busy(); t += 100) await wait(100);  // loading: a little longer
      if (grew()) await wait(150);  // what came in, drawn
      collect();
      const now = missing().length;
      if (count() !== before || now !== gaps) last = Date.now();
      settled = count() === before ? settled + 1 : 0;
      gaps = now;
    }
  } finally {
    XMLHttpRequest.prototype.open = open;
    window.fetch = fetched;
  }
  let items = people.size ? [...people.values()] : [...seen.values()];
  if (!people.size && !items.some(i => /\d/.test(i.label))) {
    const hovered = [], headings = headingsNow();
    for (const el of pictures().slice(0, limits.items)) {
      if (Date.now() - start > limits.ms * 1.5) { capped = true; break; }
      for (const type of ['pointerover', 'mouseover', 'mouseenter']) el.dispatchEvent(new MouseEvent(type, {bubbles: type !== 'mouseenter', view: window}));
      await wait(60);
      const tip = [...document.querySelectorAll('[role=tooltip]')].map(t => clean(t.innerText || t.textContent)).filter(Boolean).pop();
      for (const type of ['pointerout', 'mouseout', 'mouseleave']) el.dispatchEvent(new MouseEvent(type, {bubbles: type !== 'mouseleave', view: window}));
      if (tip) hovered.push({label: tip, heading: headingOf(el, headings)});
    }
    if (hovered.length) items = hovered;
  }
  return {items: items.slice(0, limits.items), capped: capped || items.length > limits.items, missing: missing(),
          rounds, extra, ms: Date.now() - start};
}'''


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS facebook_birthdays(suggestion_id TEXT PRIMARY KEY,state TEXT NOT NULL,data TEXT,updated_at TEXT NOT NULL)')


def _fold(text):
    return unicodedata.normalize('NFKD', str(text or '')).encode('ascii', 'ignore').decode().casefold()


def _month(word):
    word = str(word or '').casefold().rstrip('.')
    return MONTHS.get(word) or MONTHS.get(_fold(word))


def heading_month(heading):
    """The month a section heading names ("November", "Upcoming birthdays in November"), or None."""
    found = [m for m in (_month(w) for w in re.findall(r'[^\W\d_]{3,10}', str(heading or ''))) if m]
    return found[-1] if len(found) == 1 or len(set(found)) == 1 else None


def _valid(month, day):
    try:
        dt.date(2000, month, day)
    except (TypeError, ValueError):
        return False
    return True


def parse(label, heading='', today=None):
    """(name, 'YYYY-MM-DD' or '--MM-DD') from one picture's label: "Sam Lee (November 14)", "Sam Lee, 14 November 1990",
    "Sam Lee 11/14" (under a November heading). A label with only a name counts under a Today heading. None when the
    label holds no clear name and day: numbers that could be either day or month, without a month heading to tell."""
    text = ' '.join(str(label or '').split())
    if not text or len(text) > 160:
        return None
    month = day = year = None
    name = None
    for pattern in DATES:
        found = pattern.search(text)
        if not found:
            continue
        groups = found.groupdict()
        if 'mon' in groups:
            month, day = _month(groups['mon']), int(groups['day'])
            if not month:
                continue
        else:
            a, b, hint = int(groups['a']), int(groups['b']), heading_month(heading)
            options = {(m, d) for m, d in ((a, b), (b, a)) if _valid(m, d)}
            picked = [o for o in options if o[0] == hint] if hint else list(options) if len(options) == 1 else []
            if len(picked) != 1:
                return None
            month, day = picked[0]
        year = int(groups['year']) if groups.get('year') else None
        name = text[:found.start()]
        break
    if name is None:  # a name alone: only under Today
        if today and any(w in _fold(heading) for w in TODAY_WORDS) and not re.search(r'\d', text):
            name, month, day = text, today.month, today.day
        else:
            return None
    words = name.strip(SEPARATORS).split()
    while words and _fold(words[-1].strip(SEPARATORS + '.')) in WEEKDAYS:  # "Sam Lee, Saturday, November 14"
        words.pop()
    name = graph.person_name(' '.join(words).strip(SEPARATORS))
    if not _valid(month, day) or len(graph.name_words(name)) < 2:
        return None
    return name, (f'{year:04d}-{month:02d}-{day:02d}' if year and 1900 <= year <= (today or dt.date.today()).year else f'--{month:02d}-{day:02d}')


def from_data(item, today=None):
    """(name, 'YYYY-MM-DD' or '--MM-DD') from one friend in the page's own data ({name, month, day, year}), or None."""
    try:
        month, day = int(item.get('month')), int(item.get('day'))
        year = int(item.get('year') or 0)
    except (TypeError, ValueError):
        return None
    name = graph.person_name(' '.join(str(item.get('name') or '').split())[:160])
    if not _valid(month, day) or len(graph.name_words(name)) < 2:
        return None
    return name, (f'{year:04d}-{month:02d}-{day:02d}' if 1900 <= year <= (today or dt.date.today()).year else f'--{month:02d}-{day:02d}')


def found(items, today=None):
    """{name: value} of the birthdays on the page, once per name. A name shown with two different days is left out.
    Each item is a friend from the page's data ({name, month, day, year}) or a picture's label ({label, heading})."""
    out, clash = {}, set()
    for item in items or ():
        if not isinstance(item, dict):
            continue
        got = from_data(item, today) if 'month' in item else parse(item.get('label'), item.get('heading') or '', today)
        if not got:
            continue
        name, value = got
        if name in out and birthdays.birthday_value(out[name]) != birthdays.birthday_value(value):
            clash.add(name)
        elif name not in out or value[:2] != '--':  # the one with a year wins
            out[name] = value
    return {n: v for n, v in out.items() if n not in clash}


def match(db, names):
    """The page's names against the Graph's people: {'matched': [{id, name, date}], 'ambiguous': [name], 'unmatched': n,
    'others': [{name, date}]}. Matched: exactly one person with the same full name, else with the same first and last
    name (a middle name on one side only). Others: the unmatched ones with a full name. Someone deleted permanently is
    nobody."""
    gone = graph.forgotten(db)
    people, ends = {}, {}
    for row in db.execute("SELECT id,name FROM graph_nodes WHERE kind='person'"):
        words = graph.name_words(row['name'])
        if len(words) >= 2 and not gone(row['id']):
            people.setdefault(' '.join(words), []).append((row['id'], graph.person_name(row['name'])))
            ends.setdefault((words[0], words[-1]), []).append((row['id'], graph.person_name(row['name'])))
    matched, ambiguous, unmatched, others = [], [], 0, []
    for name, value in sorted(names.items()):
        words = graph.name_words(name)
        full = graph.name_match(words, words) == 'same'  # a full name
        hits = people.get(' '.join(words), []) if full else []
        if full and not hits:  # with or without a middle name ("Ann Marie Lee", "Ann Lee"): the same first and last name
            hits = ends.get((words[0], words[-1]), [])
        if len(hits) == 1:
            matched.append({'id': hits[0][0], 'name': hits[0][1], 'date': value})
        elif hits:
            ambiguous.append(name)
        else:
            unmatched += 1
            if full:
                others.append({'name': name, 'date': value})
    return {'matched': matched, 'ambiguous': ambiguous, 'unmatched': unmatched, 'others': others}


def owner_set(db, node_id):
    """Whether the owner set or removed this person's birthday on their page (person_birthday.set_birthday): theirs stays."""
    enrichment.fact_tables(db)
    return bool(db.execute("SELECT 1 FROM person_facts WHERE identifier=? AND field=? AND source=?",
                           (node_id, person_birthday.FIELD, person_birthday.SOURCE)).fetchone())


def fresh(db, node_id, value):
    """Whether this birthday is news for the person: nobody set theirs by hand, and the one their page shows
    (person_birthday.get) is another day or none."""
    if owner_set(db, node_id):
        return False
    got = person_birthday.get(db, node_id)
    if got and got['source'] == person_birthday.SOURCE:
        return False
    return not got or birthdays.birthday_value(got['value']) != birthdays.birthday_value(value)


def preview(db, items, today=None, capped=False, missing=()):
    """What the owner sees before saving: {'found', 'matched', 'new', 'ambiguous', 'unmatched', 'capped', 'missing'}.
    new: matched people whose birthday is new to the Machine (or another day than it knew), and not set by the owner."""
    names = found(items, today)
    out = match(db, names)
    out['found'] = len(names)
    out['capped'] = bool(capped)  # the read stopped at its limits: the page may have had more
    out['missing'] = sorted({int(m) for m in missing or () if str(m).isdigit() and 1 <= int(m) <= 12})  # months it never saw
    out['new'] = sum(1 for m in out['matched'] if fresh(db, m['id'], m['date']))
    return out


def save(db, data, stamp):
    """The matched birthdays, each through the person's one birthday (person_birthday.offer, source facebook): one the
    owner set stays, one the Machine already knew for that day is left as it is. Returns the people saved: [{id, name}]."""
    saved = []
    for m in data.get('matched') or ():
        if fresh(db, m['id'], m['date']) and person_birthday.offer(db, m['id'], m['date'], SOURCE, stamp):
            saved.append({'id': m['id'], 'name': m['name']})
    return saved


def put(db, suggestion_id, state, data, stamp):
    ensure(db)
    db.execute('INSERT INTO facebook_birthdays(suggestion_id,state,data,updated_at) VALUES(?,?,?,?) ON CONFLICT(suggestion_id) DO UPDATE SET '
               'state=excluded.state,data=excluded.data,updated_at=excluded.updated_at', (suggestion_id, state, json.dumps(data or {}), stamp))


def without_others(db):
    """The to-dos read before the friends nobody in the Graph were kept: a preview or Save with no others yet."""
    try:
        rows = db.execute("SELECT suggestion_id,data FROM facebook_birthdays WHERE state IN ('preview','saved')").fetchall()
    except Exception:  # noqa: BLE001 - a database before this table
        return []
    return [row['suggestion_id'] for row in rows if 'others' not in json.loads(row['data'] or '{}')]


def fill_others(db, suggestion_id, items, today):
    """An older to-do gains the friends nobody in the Graph has, from a fresh read's items (none when the read failed,
    so it isn't tried again). Its state, matched people, Save and time stay as they are. Returns how many, or None
    when it has them by now (Import again, or another fill)."""
    got = get(db, suggestion_id)
    if not got or got[0] not in ('preview', 'saved') or 'others' in got[1]:
        return None
    state, data, at = got
    data['others'] = match(db, found(items or [], today))['others']
    data.setdefault('added', [])
    put(db, suggestion_id, state, data, at)
    return len(data['others'])


def get(db, suggestion_id):
    """(state, data, updated_at) of a to-do, or None for any other to-do."""
    try:
        row = db.execute('SELECT state,data,updated_at FROM facebook_birthdays WHERE suggestion_id=?', (suggestion_id,)).fetchone()
    except Exception:  # noqa: BLE001 - a database before this table
        return None
    return (row['state'], json.loads(row['data'] or '{}'), row['updated_at']) if row else None


def view(db, suggestion_id, now=None):
    """What the to-do shows, or None for any other to-do: {'state', ...}. state: new (not read yet), reading, signed_out,
    failed, preview (found, matched, new, ambiguous, shown: a few matched names with their day, more: how many else),
    saved (saved: how many)."""
    got = get(db, suggestion_id)
    if not got:
        return None
    state, data, at = got
    if state == 'new':
        return {'state': 'new'}
    if state == 'reading':
        now = now or dt.datetime.now(dt.timezone.utc)
        try:
            late = dt.datetime.fromisoformat(at) + dt.timedelta(minutes=READ_MINUTES) < now
        except ValueError:
            late = True
        return {'state': 'failed', 'empty': False} if late else {'state': 'reading'}
    if state == 'preview':
        matched = data.get('matched') or []
        return {'state': 'preview', 'found': data.get('found', 0), 'matched': len(matched), 'new': data.get('new', 0),
                'shown': [{'id': m['id'], 'name': m['name'], 'date': m['date']} for m in matched[:SHOWN]], 'more': max(0, len(matched) - SHOWN),
                'ambiguous': (data.get('ambiguous') or [])[:AMBIGUOUS_SHOWN], 'unmatched': data.get('unmatched', 0),
                'capped': bool(data.get('capped')), 'missing': data.get('missing') or [], **others_view(data)}
    if state == 'saved':
        people = data.get('people') or []
        return {'state': 'saved', 'saved': data.get('saved', 0), 'people': people[:SHOWN], 'more': max(0, data.get('saved', 0) - SHOWN),
                **others_view(data)}
    if state == 'failed':
        return {'state': 'failed', 'empty': bool(data.get('empty'))}  # empty: the page showed no birthdays it could read
    return {'state': state if state in STATES else 'failed'}


def others_view(data):
    """The friends nobody in the Graph has, as the to-do shows them: {'others': how many Add adds,
    'others_shown': a few names, 'added': how many it added (Undo takes them away)}."""
    others = (data.get('others') or [])[:ADD_MAX]
    return {'others': len(others), 'others_shown': [o['name'] for o in others[:SHOWN]], 'added': len(data.get('added') or ())}


def add(db, data, stamp):
    """Add the friends nobody in the Graph has (data's others, at most ADD_MAX) as people, in the caller's transaction:
    each as if added by hand (graph.create_record), Type Personal (the owner's word, as on their page), with their
    birthday (source facebook). Matched against the Graph again first: a name that now has a person, or more than one,
    is skipped. They show on their own pages at once (graph_show), in one write. Returns [{node_id, name}]."""
    names = {o['name']: o['date'] for o in (data.get('others') or [])[:ADD_MAX] if isinstance(o, dict) and o.get('name')}
    made = []
    for other in match(db, names)['others']:
        try:
            done = graph.create_record(db, 'person', {'name': other['name']}, stamp)
        except ValueError:  # a name over the length a person's name may have
            continue
        if done.get('created'):
            made.append({'node_id': done['node_id'], 'name': done['name'], 'date': other['date']})
    crm_import.details_made(db, [m['node_id'] for m in made], PERSONAL, stamp)
    graph_show.show_new_people(db, made, PERSONAL)
    enrichment.offer_facts(db, [([m['node_id']], {person_birthday.FIELD: m['date']}, enrichment.RECORD) for m in made], SOURCE, stamp)
    return [{'node_id': m['node_id'], 'name': m['name']} for m in made]


def remove(db, ids):
    """Undo of add: exactly those people go again (crm_import.drop_made, as an import's Undo), with their birthday, in
    the caller's transaction. One the owner joined with another person since (graph_merges) stays: it is part of that
    person now. Returns how many went."""
    try:
        joined = {r[0] for r in db.execute('SELECT a FROM graph_merges UNION SELECT b FROM graph_merges')}
    except Exception:  # noqa: BLE001 - a database before merges
        joined = set()
    ids = sorted({str(i) for i in ids or () if str(i).startswith('manual:')} - joined)
    ids = [r[0] for r in db.execute("SELECT identifier FROM manual_nodes WHERE kind='person' AND identifier IN (SELECT value FROM json_each(?))",
                                    (json.dumps(ids),))]
    for node_id in ids:
        crm_import.drop_made(db, node_id)
    for source in (SOURCE, person_birthday.SOURCE):  # theirs from Facebook, and one the owner set on their page since
        enrichment.drop_facts(db, ids, person_birthday.FIELD, source)
    graph_show.drop_people(db, ids)
    return len(ids)


def read(base, url=PAGE, limits=None, timeout=420):
    """Read the page in a tab of its own in the browser at base (a DevTools address), then close the tab: {'items'} or
    {'error': 'signed-out'}. The tab is in front while it reads: the owner asked for it, and a page in a background tab
    doesn't load more as it is scrolled. Raises browser_cdp.CdpError when the browser can't be reached."""
    target = browser_cdp.open_tab(base, url)
    try:
        with browser_cdp.Session(base, target, timeout=timeout) as session:
            session.call('Page.bringToFront')
            for _ in range(60):  # until the page is there to read (a fresh tab answers before its page loads)
                try:
                    ready = session.call('Runtime.evaluate', {'expression': "location.href !== 'about:blank' && document.readyState",
                                                              'returnByValue': True})['result'].get('value')
                except browser_cdp.CdpError:
                    ready = None
                if ready in ('interactive', 'complete'):
                    break
                time.sleep(0.5)
            months = {word: n for word, n in MONTHS.items() if len(word) >= 3}
            result = session.run(READ_JS, {**LIMITS, 'months': months, 'month': dt.date.today().month, **(limits or {})})
    finally:
        browser_cdp.close_tab(base, target)
    return result if isinstance(result, dict) else {'items': []}
