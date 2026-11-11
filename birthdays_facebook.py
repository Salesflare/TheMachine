"""Birthdays from Facebook (docs/help/routines.md, "Templates"): the owner's friends' birthdays, read once from
Facebook's birthdays page in The Machine's own browser, matched to people in the Graph and kept only on the owner's OK.

Only on the owner's tap, on the Birthdays template's one to-do (birthdays_facebook_app.py): never in the background,
never on a schedule. A new import is their tap again. Read through the browser the other readers already use (LinkedIn,
X: the shared browser at browser_cdp_url, under the shared browser lease), the way the owner would: open the page in a
tab of its own, scroll it to the end, read each friend's name and birthday as the page has them, close the tab. No
sign-in is handled here: a browser that isn't signed in to Facebook is told to the owner, and the read stops.

What is kept: each matched person's birthday (month and day, the year when the page shows it), as the one
birthday their page shows (person_birthday.offer, source facebook), which the Birthdays routine reads. One the owner set
or removed on the person's page stays. And for a matched person who shows no photo yet, their profile picture, as the
page already has it (its link in the same data, so no request to Facebook of its own): on Save, a small copy is saved on
this Machine like a looked-up photo (enrichment.keep_photo), one at a time with a pause, never over a photo they have or
one the owner set or took off. Facebook's picture links expire, so the link itself is never kept past Save. Nothing else
from Facebook is kept: no link or ID. The names read are for matching and for the Add button (below), and live only on
the to-do until the owner reads again. After Save the to-do keeps who was saved (their Graph id and name), to link to
their pages. Nothing is ever written to Facebook.

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
FILL_READS = 3  # reads an older to-do's fill takes at most, while they come back short
SHORT = 0.9  # a fill's read that found less than this share of what the to-do's own read found came back short
PERSONAL = {'side': 'personal'}  # their Type, as the owner sets it on a person's page (person_edits)
PHOTO_LINK = re.compile(r'https://(?:[a-z0-9-]+\.)+fbcdn\.net/[^\s"\'<>\\]{1,2000}')  # a profile picture on Facebook's own image hosts
PHOTO_PAUSE = 0.3  # seconds between two pictures on Save

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
# after SETTLE quiet rounds in a row. With months still missing, IDLE ms of quiet rounds end it: nobody has a birthday
# then, and the preview names them (missing). A quiet round scrolled to the end and brought nobody new, no new month, and
# no request for more still on its way (each waits up to NET ms for its answer). A page that keeps growing with nobody new,
# or keeps a busy part on screen, doesn't hold it up. Neither rule counts before the page has answered a scroll (it grew,
# or asked for more) with friends on it: a page just opened in a browser just up shows its first friends, every month
# even, before it loads more, and can't end the read. A page that answers no scroll for WAKE ms is read as it is, and the
# result says so (woke: false). The limits (items, ms) are a safety net well above Facebook's 5,000 friends: capped only
# when one stopped it. Each round waits for the page as long as it needs and no longer: on as soon as it grows, else after
# PAUSE ms (BUSY ms more while it shows a progress bar or busy part). Reads only; nothing is clicked or typed.
LIMITS = {'items': 6000, 'ms': 360000, 'idle': 20000, 'settle': 2, 'pause': 800, 'busy': 1200, 'net': 30000, 'wake': 45000}
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
  const https = u => typeof u === 'string' && /^https:\/\//.test(u) && u.length <= 2000 ? u : '';
  // A friend's profile picture, as the page already has it (no request of its own): its link in their data, or the picture's image
  const pictureOf = el => { const img = /^(img|image)$/i.test(el.tagName) ? el : el.querySelector('img, image'); return img ? https(img.currentSrc || img.getAttribute('src') || img.getAttribute('href') || img.getAttribute('xlink:href')) : ''; };
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
      const key = String(o.id || o.name), had = people.get(key), pic = o.profile_picture || o.profilePicture || o.picture || {};
      const photo = https(typeof pic === 'string' ? pic : pic.uri || pic.url) || (had && had.photo) || '';
      if (!had || (+b.year && !had.year)) people.set(key, {name: clean(o.name).slice(0, 160), month: +b.month, day: +b.day, year: +b.year || null, photo});
      else if (photo && !had.photo) had.photo = photo;
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
  // The page's requests for more, while they are on their way: a round with one isn't quiet until it is answered
  const pending = new Set();
  let asked = 0;
  const ask = () => { const req = {at: Date.now()}; pending.add(req); asked++; return () => pending.delete(req); };
  const loading = () => [...pending].some(req => Date.now() - req.at < limits.net);
  const open = XMLHttpRequest.prototype.open, fetched = window.fetch;
  XMLHttpRequest.prototype.open = function (method, url) {
    if (/graphql/i.test(String(url))) {
      const done = ask();
      this.addEventListener('loadend', () => { done(); try { eat(this.responseText); } catch (e) {} });
    }
    return open.apply(this, arguments);
  };
  window.fetch = function (input) {
    const answer = fetched.apply(this, arguments);
    if (/graphql/i.test(String(input && input.url || input))) {
      const done = ask();
      answer.then(r => r.clone().text()).then(eat, () => {}).finally(done);
    }
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
      const key = label + '\n' + heading; if (!seen.has(key)) seen.set(key, {label, heading, photo: pictureOf(el)}); } };
  const count = () => people.size + seen.size;
  const start = Date.now(), high = () => document.documentElement.scrollHeight;
  let capped = false, woke = false, settled = 0, rounds = 0, extra = 0, last = start, gaps = missing().length;
  try {
    collect();
    for (;;) {
      const done = !gaps, live = woke || Date.now() - start > limits.wake;  // a page not answering yet can't end it
      if (live && (done ? settled >= limits.settle : Date.now() - last > limits.idle)) break;
      if (count() >= limits.items || Date.now() - start > limits.ms) { capped = true; break; }
      const before = count(), height = high(), sent = asked;
      window.scrollBy(0, -400);  // up a little first, so the page sees a scroll to its end even when it didn't grow
      await wait(50);
      window.scrollTo(0, high());
      rounds++;
      if (done) extra++;
      const grew = () => count() !== before || high() !== height;
      for (let t = 0; t < limits.pause && !grew() && !loading(); t += 100) await wait(100);
      for (let t = 0; t < limits.busy && !grew() && !loading() && busy(); t += 100) await wait(100);  // loading: a little longer
      for (let t = 0; t < limits.net && loading(); t += 100) await wait(100);  // asked for more: its answer
      if (grew()) await wait(150);  // what came in, drawn
      collect();
      const now = missing().length, fresh = count() !== before || now !== gaps;
      if (count() && (fresh || high() !== height || asked !== sent)) woke = true;  // the page answered the scroll
      const quiet = !fresh && !loading();
      if (!quiet || !live) last = Date.now();
      settled = quiet && live ? settled + 1 : 0;
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
      if (tip) hovered.push({label: tip, heading: headingOf(el, headings), photo: pictureOf(el)});
    }
    if (hovered.length) items = hovered;
  }
  return {items: items.slice(0, limits.items), capped: capped || items.length > limits.items, missing: missing(),
          woke, rounds, extra, ms: Date.now() - start};
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


def pictures(items, today=None):
    """{name: link} of the profile pictures the page showed with its birthdays (the read's items), once per name: only
    a link to Facebook's own image hosts (PHOTO_LINK)."""
    out = {}
    for item in items or ():
        link = str(item.get('photo') or '') if isinstance(item, dict) else ''
        if not PHOTO_LINK.fullmatch(link):
            continue
        got = from_data(item, today) if 'month' in item else parse(item.get('label'), item.get('heading') or '', today)
        if got:
            out.setdefault(got[0], link)
    return out


def match(db, names, links=None):
    """The page's names against the Graph's people: {'matched': [{id, name, date, photo when links has theirs}],
    'ambiguous': [name], 'unmatched': n, 'others': [{name, date}]}. Matched: exactly one person with the same full name,
    else with the same first and last name (a middle name on one side only). Others: the unmatched ones with a full
    name, but none with the name of someone the owner deleted permanently (graph.name_keys). Someone deleted
    permanently is nobody."""
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
            matched.append({'id': hits[0][0], 'name': hits[0][1], 'date': value, **({'photo': links[name]} if name in (links or {}) else {})})
        elif hits:
            ambiguous.append(name)
        else:
            unmatched += 1
            if full and not any(gone(k) for k in graph.name_keys(name)):
                others.append({'name': name, 'date': value})
    return {'matched': matched, 'ambiguous': ambiguous, 'unmatched': unmatched, 'others': others}


def owner_set(db, ids):
    """Which of these people (node ids) the owner set or removed the birthday of on their page
    (person_birthday.set_birthday): theirs stays. One query for all of them."""
    enrichment.fact_tables(db)
    return {r[0] for r in db.execute('SELECT identifier FROM person_facts WHERE field=? AND source=? AND identifier IN (SELECT value FROM json_each(?))',
                                     (person_birthday.FIELD, person_birthday.SOURCE, json.dumps(sorted(set(ids)))))}


def nodes(db, matched):
    """{their id in matched: the person's graph_nodes row now}, all at once: an id from an earlier preview that is part
    of another person since (a merge) is that person, as person_birthday.get has it."""
    ids = {m['id'] for m in matched or ()}
    if not ids:
        return {}
    rows = db.execute("SELECT id,name,info,kind FROM graph_nodes WHERE id IN (SELECT value FROM json_each(?))", (json.dumps(sorted(ids)),)).fetchall()
    node = {r['id']: r for r in rows}
    for gone in ids - set(node):
        row = graph.resolve(db, gone)
        if row:
            node[gone] = row
    return {i: r for i, r in node.items() if r['kind'] == 'person'}


def photo_news(db, matched):
    """The matched people ([{id, photo}]) whose profile picture would fill in a photo: they show none yet, and the
    owner neither set nor took off theirs (enrichment.without_photo). {their id in matched: the person's node id now}.
    Only reads."""
    node = nodes(db, [m for m in matched or () if m.get('photo')])
    bare = enrichment.without_photo(db, list({r['id']: r for r in node.values()}.values())) if node else set()
    return {i: r['id'] for i, r in node.items() if r['id'] in bare}


def fresh(db, matched):
    """The matched people ([{id, date}]) whose birthday is news, as {their id in matched: the person's node id now}:
    nobody set theirs by hand, and the one their page shows (person_birthday.known, as person_birthday.get has it) is
    another day or none. All at once: every birthday and every person is looked at once, not once per person
    (thousands of friends, each a person with a birthday). Only reads: callers run it before taking the write lock."""
    node = nodes(db, matched)
    if not node:
        return {}
    people = {r['id']: {'id': r['id'], 'name': r['name'], 'info': json.loads(r['info'] or '{}')} for r in node.values()}
    mine = owner_set(db, people)
    have = person_birthday.known(db, people) if people else {}
    out = {}
    for m in matched:
        person = node.get(m['id'])
        if not person:
            continue  # nobody in the Graph by now
        got = have.get(person['id'])
        if person['id'] in mine or (got and got['source'] == person_birthday.SOURCE):
            continue
        if not got or birthdays.birthday_value(got['value']) != birthdays.birthday_value(m['date']):
            out[m['id']] = person['id']
    return out


def due(deadline):
    """A step with a deadline (time.monotonic()) that has passed it stops: TimeoutError."""
    if deadline is not None and time.monotonic() > deadline:
        raise TimeoutError


def preview(db, items, today=None, capped=False, missing=(), deadline=None):
    """What the owner sees before saving: {'found', 'matched', 'new', 'ambiguous', 'unmatched', 'capped', 'missing'}.
    new: matched people whose birthday is new to the Machine (or another day than it knew), and not set by the owner.
    deadline: past it (time.monotonic()), TimeoutError."""
    names = found(items, today)
    due(deadline)
    out = match(db, names, pictures(items, today))
    due(deadline)
    out['found'] = len(names)
    out['capped'] = bool(capped)  # the read stopped at its limits: the page may have had more
    out['missing'] = sorted({int(m) for m in missing or () if str(m).isdigit() and 1 <= int(m) <= 12})  # months it never saw
    news = fresh(db, out['matched'])
    for m in out['matched']:
        if m['id'] in news:
            m['new'] = True  # Save writes theirs: the to-do lists these, the rest is a count
    out['new'] = len([m for m in out['matched'] if m.get('new')])
    bare = photo_news(db, out['matched'])
    for m in out['matched']:
        if m['id'] not in bare:
            m.pop('photo', None)  # only the links Save would use stay on the to-do
    out['photos'] = len(bare)
    out['flagged'] = True  # matched people carry new (a preview before this listed every matched person)
    due(deadline)
    return out


def to_save(db, data):
    """What Save writes, worked out from reads only (fresh), before the write lock: [{id, node, name, date}] for each
    matched person whose birthday is news."""
    matched = [m for m in data.get('matched') or () if isinstance(m, dict) and m.get('id') and person_birthday.parts(m.get('date'))]
    news = fresh(db, matched)
    return [{'id': m['id'], 'node': news[m['id']], 'name': m['name'], 'date': m['date']} for m in matched if m['id'] in news]


def write_saved(db, picks, stamp):
    """Save's write, in the caller's short transaction: the birthdays to_save found, in one pass (source facebook,
    enrichment.offer_facts). One the owner set since stays, as does one a higher source has. Returns the people saved:
    [{id, name}]."""
    mine = owner_set(db, [p['node'] for p in picks])
    picks = [p for p in picks if p['node'] not in mine]
    if not picks:
        return []
    enrichment.offer_facts(db, [([p['node']], {person_birthday.FIELD: p['date']}, enrichment.RECORD) for p in picks], SOURCE, stamp)
    kept = {r[0]: r[1] for r in db.execute('SELECT identifier,value FROM person_facts WHERE field=? AND source=? AND identifier IN (SELECT value FROM json_each(?))',
                                           (person_birthday.FIELD, SOURCE, json.dumps(sorted({p['node'] for p in picks}))))}
    return [{'id': p['id'], 'name': p['name']} for p in picks
            if p['node'] in kept and birthdays.birthday_value(kept[p['node']]) == birthdays.birthday_value(p['date'])]


def to_photos(db, data):
    """The profile pictures Save keeps, from reads only: [{node, link}] for each matched person the preview found a
    picture for who still shows no photo (photo_news)."""
    matched = [m for m in data.get('matched') or () if isinstance(m, dict) and m.get('id') and PHOTO_LINK.fullmatch(str(m.get('photo') or ''))]
    bare = photo_news(db, matched)
    return [{'node': bare[m['id']], 'link': m['photo']} for m in matched if m['id'] in bare]


def save_photos(connect, picks, stamp, fetch=None, pause=PHOTO_PAUSE, wait=None):
    """The pictures to_photos found, one at a time with a pause: each downloaded (enrichment.download_photo: https to
    a public address, small, only an image), then saved in a short write of its own (enrichment.keep_photo, which
    checks again that they still show none) and put on their page at once (graph_show). Returns how many were saved."""
    fetch, wait = fetch or enrichment.download_photo, wait or time.sleep
    saved = 0
    for n, pick in enumerate(picks):
        if n:
            wait(pause)
        try:
            got = fetch(pick['link'])
        except Exception:  # noqa: BLE001 - a picture that didn't come: the next one
            got = None
        if not got:
            continue
        with connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if enrichment.keep_photo(db, pick['node'], got, stamp):
                graph_show.show_person_edit(db, pick['node'], ())
                saved += 1
    return saved


def save(db, data, stamp):
    """The matched birthdays, each as the person's one birthday (source facebook): one the owner set stays, one the
    Machine already knew for that day is left as it is. Returns the people saved: [{id, name}]. The action works it out
    before its write lock (to_save) and writes in a short transaction (write_saved)."""
    return write_saved(db, to_save(db, data), stamp)


def put(db, suggestion_id, state, data, stamp):
    ensure(db)
    db.execute('INSERT INTO facebook_birthdays(suggestion_id,state,data,updated_at) VALUES(?,?,?,?) ON CONFLICT(suggestion_id) DO UPDATE SET '
               'state=excluded.state,data=excluded.data,updated_at=excluded.updated_at', (suggestion_id, state, json.dumps(data or {}), stamp))


CARRIED = ('added', 'people', 'saved', 'others')  # what Import again keeps: who Add added (Undo), who Save saved, the friends for Add


def carried(data):
    """What a to-do keeps through Import again (CARRIED): into the read, and into its preview or failure."""
    data = data if isinstance(data, dict) else {}
    return {k: data[k] for k in CARRIED if k in data}


def report(result):
    """What a read says about itself, kept on the to-do: {'capped', 'missing', 'woke', 'rounds', 'ms'}. woke: the page
    answered its scrolls (false: it was read as it first showed)."""
    result = result if isinstance(result, dict) else {}
    number = lambda key: int(result.get(key) or 0) if str(result.get(key) or 0).isdigit() else 0  # noqa: E731
    return {'capped': bool(result.get('capped')), 'missing': sorted({int(m) for m in result.get('missing') or () if str(m).isdigit() and 1 <= int(m) <= 12}),
            'woke': result.get('woke') is not False, 'rounds': number('rounds'), 'ms': number('ms')}


def needs_fill(data):
    """Whether a to-do's friends nobody in the Graph has still come from a fill: none yet; a fill whose reads came back
    short, until FILL_READS of them; or, once, one filled before fills kept their read's report whose others fall short of
    the friends its own read didn't match (or that kept no count of them). Never once the owner added them, nor after a
    read of its own that kept its report (Import again)."""
    if data.get('added') or 'read' in data:
        return False
    if 'fill' in data:
        return not data['fill'].get('done')
    if 'others' not in data:
        return True
    unmatched = data.get('unmatched')
    return not isinstance(unmatched, int) or len(data['others']) < SHORT * unmatched


def to_fill(db):
    """The to-dos whose friends nobody in the Graph has a fill at start reads (needs_fill): a preview or Save."""
    try:
        rows = db.execute("SELECT suggestion_id,data FROM facebook_birthdays WHERE state IN ('preview','saved')").fetchall()
    except Exception:  # noqa: BLE001 - a database before this table
        return []
    return [row['suggestion_id'] for row in rows if needs_fill(json.loads(row['data'] or '{}'))]


def fill_others(db, suggestion_id, result, today, reads=FILL_READS):
    """An older to-do gains the friends nobody in the Graph has, from a fresh read (read's result). Kept with the read's
    report (fill: found, capped, missing, woke, tries, done). A read that was cut short, missed months, never saw the page
    answer, failed, or found clearly fewer than the to-do's own read (SHORT) came back short: its others are kept when
    they are more than the to-do had, and it is read again, up to FILL_READS reads. Its state, matched people, Save and
    time stay as they are. Returns the fill with 'others' (how many it has now), or None when it needs none by now."""
    got = get(db, suggestion_id)
    if not got or got[0] not in ('preview', 'saved') or not needs_fill(got[1]):
        return None
    state, data, at = got
    result = result if isinstance(result, dict) else {}
    names = {} if result.get('error') else found(result.get('items') or [], today)
    fill = {'found': len(names), **report(result), 'error': str(result.get('error') or '')[:40]}
    before = data.get('fill') or {}
    earlier = max(int(data.get('found') or 0), int(before.get('best') or 0))
    short = bool(fill['error'] or not names or fill['capped'] or fill['missing'] or not fill['woke'] or len(names) < SHORT * earlier)
    fill.update(tries=int(before.get('tries') or 0) + 1, best=max(len(names), int(before.get('best') or 0)), complete=not short)
    fill['done'] = not short or fill['tries'] >= reads
    others = match(db, names)['others']
    if not short or len(others) > len(data.get('others') or ()):
        data['others'] = others  # never fewer from a read that came back short than the to-do had
    data.setdefault('others', [])
    data.setdefault('added', [])
    data['fill'] = fill
    put(db, suggestion_id, state, data, at)
    return {**fill, 'others': len(data['others'])}


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
        listed = [m for m in matched if m.get('new')] if data.get('flagged') else matched  # what Save writes; the rest is a count
        return {'state': 'preview', 'found': data.get('found', 0), 'matched': len(matched), 'new': data.get('new', 0), 'photos': data.get('photos', 0),
                'shown': [{'id': m['id'], 'name': m['name'], 'date': m['date']} for m in listed[:SHOWN]], 'more': max(0, len(listed) - SHOWN),
                'ambiguous': (data.get('ambiguous') or [])[:AMBIGUOUS_SHOWN], 'unmatched': data.get('unmatched', 0),
                'capped': bool(data.get('capped')), 'missing': data.get('missing') or [], **others_view(db, data)}
    if state == 'saved':
        people = data.get('people') or []
        return {'state': 'saved', 'saved': data.get('saved', 0), 'photos': data.get('photos', 0), 'people': people[:SHOWN], 'more': max(0, data.get('saved', 0) - SHOWN),
                **others_view(db, data)}
    if state == 'failed':
        return {'state': 'failed', 'empty': bool(data.get('empty'))}  # empty: the page showed no birthdays it could read
    return {'state': state if state in STATES else 'failed'}


def addable(db, data):
    """The friends nobody in the Graph has that Add would add: at most ADD_MAX, none named as someone the owner deleted
    permanently since the read (graph.name_keys)."""
    gone = graph.forgotten(db)
    others = [o for o in data.get('others') or () if isinstance(o, dict) and o.get('name')]
    return [o for o in others if not any(gone(k) for k in graph.name_keys(o['name']))][:ADD_MAX]


def others_view(db, data):
    """The friends nobody in the Graph has, as the to-do shows them: {'others': how many Add adds,
    'others_shown': a few names, 'added': how many it added (Undo takes them away)}."""
    others = addable(db, data)
    return {'others': len(others), 'others_shown': [o['name'] for o in others[:SHOWN]], 'added': len(data.get('added') or ())}


def add(db, data, stamp):
    """Add the friends nobody in the Graph has (addable: at most ADD_MAX, none the owner deleted) as people, in the caller's transaction:
    each as if added by hand (graph.create_record), Type Personal (the owner's word, as on their page), with their
    birthday (source facebook). Matched against the Graph again first: a name that now has a person, or more than one,
    is skipped. They show on their own pages at once (graph_show), in one write. Returns [{node_id, name}]."""
    names = {o['name']: o['date'] for o in addable(db, data)}
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
