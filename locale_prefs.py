"""Language and region: how dates and times read on the dashboard, in cards, Telegram, the digest and Fleet messages
(Settings, General).

`locale` in config.json is a language-REGION tag like en-US, en-GB or nl-BE: the region sets the date order (Oct 24 or
24 Oct) and the default clock. `language` is the UI language (LANGUAGES, the catalogs in i18n/): what the dashboard,
Telegram, emails and the model's own notes read in. Without one, a non-English language in `locale` (from signup) counts,
else English; the dashboard's first load sets it from the browser's languages (Accept-Language), once. `clock` is '12h' or '24h' when the owner overrides the region's. A hosted Machine gets its first
`locale` from signup (ASSISTANT_LOCALE at install). A Machine without one (self-hosted) gets it the same way from the
dashboard's first load (guess: the country of the browser's time zone, else its language's region), and keeps US
dates and a 24-hour clock until then.

`todo_scope` is the To-dos filter (all, work or personal), kept here with the language so every device of the owner
shows the same list; None until it is first set (a dashboard then brings the one its browser kept, once).

The dashboard gets view() and formats with the same rules (dashboard.html, applyLocale)."""
from __future__ import annotations

import functools
import re
import zoneinfo
from pathlib import Path

LANGUAGES = {'en': 'English', 'nl': 'Nederlands', 'fr': 'Français', 'de': 'Deutsch', 'es': 'Español', 'it': 'Italiano',
             'pt-BR': 'Português (Brasil)'}  # i18n/<code>.json
# A browser language without its own catalog that reads one of these for now: Portuguese from Portugal reads Brazilian.
NEAREST = {'pt': 'pt-BR'}
_CODES = {code.lower(): code for code in LANGUAGES}
_BASES = {code.split('-')[0] for code in LANGUAGES}
DEFAULT_REGION = 'US'  # dates without a locale
CLOCKS = ('auto', '12h', '24h')
SCOPES = ('all', 'work', 'personal')  # the To-dos filter
# Regions whose people mostly read a 12-hour clock (CLDR's preferred hour cycle "h"); the rest read 24-hour.
H12 = frozenset('US CA AU NZ IN PK BD PH MY SG HK TW KR EG SA AE JO KW QA BH OM IQ SY LB YE LY SD CO VE SV HN NI GT DO '
                'PR GU AS VI MP UM'.split())
# Regions that put the month first (Oct 24); the rest read the day first (24 Oct).
MONTH_FIRST = frozenset('US CA PH PR GU AS VI MP UM FM MH PW'.split())

_current = {'locale': None, 'clock': 'auto', 'language': None, 'todo_scope': None}


def normalize(value):
    """'en-BE' from 'en-BE' or 'en_be', 'nl-BE' from 'nl-be', 'en-JP' from 'ja-JP' (a language there is no catalog for),
    '' for no setting, None when it isn't a tag."""
    text = str(value or '').strip().replace('_', '-')
    if not text:
        return ''
    found = re.fullmatch(r'([A-Za-z]{2,3})-([A-Za-z]{2})', text)
    if not found:
        return None
    language = found.group(1).lower()
    return (language if language in _BASES else 'en') + '-' + found.group(2).upper()


def region(locale):
    """'BE' for en-BE; '' without a locale."""
    tag = normalize(locale)
    return tag.split('-')[1] if tag else ''


def hour12(locale, clock='auto'):
    """True when times read 2:00 PM: the owner's choice, else the region's; a Machine without a locale stays 24-hour."""
    if clock in ('12h', '24h'):
        return clock == '12h'
    return region(locale) in H12


def code(value):
    """The catalog code for a language setting: 'pt-BR' from 'pt-br' or 'pt_BR', 'it' from 'IT'; None for another."""
    return _CODES.get(str(value or '').strip().lower().replace('_', '-'))


def language():
    """The owner's UI language now ('en' until configured)."""
    return _current['language'] or 'en'


def language_of(config):
    """The UI language: the owner's choice, else a non-English language from the locale (signup), else English."""
    chosen = code((config or {}).get('language'))
    if chosen:
        return chosen
    tag = normalize((config or {}).get('locale'))
    return pick_language([tag]) if tag else 'en'


def date_locale(locale, language='en'):
    """The Intl locale the dashboard formats dates with: in English US order (Sat, Oct 24) or day first (Sat 24 Oct),
    in another language that language as the region writes it (nl-BE: za 24 okt.)."""
    if language and '-' in language:
        return language  # its own region's way (pt-BR), wherever the owner is
    if language and language != 'en':
        return f'{language}-{region(locale) or {"nl": "NL", "fr": "FR", "de": "DE", "es": "ES", "it": "IT"}.get(language, "US")}'
    return 'en-US' if (region(locale) or DEFAULT_REGION) in MONTH_FIRST else 'en-GB'


def pick_language(wanted):
    """The first UI language in a browser's list (navigator.languages, or an Accept-Language header): 'nl' from
    'nl-BE,nl;q=0.9,en;q=0.8', 'en' when none has a catalog."""
    if isinstance(wanted, str):
        ranked = []
        for i, part in enumerate(wanted.split(',')[:20]):
            tag, _, q = part.strip().partition(';q=')
            try:
                weight = float(q) if q else 1.0
            except ValueError:
                weight = 0.0
            ranked.append((-weight, i, tag.strip()))
        wanted = [tag for _, _, tag in sorted(ranked)]
    for tag in list(wanted or [])[:20]:
        tag = str(tag or '').strip().lower().replace('_', '-')
        base = tag.split('-')[0]
        found = _CODES.get(tag) or _CODES.get(base) or NEAREST.get(base)
        if found:
            return found
    return 'en'


def configure(config):
    """Use the owner's setting from config.json; a bad value is ignored (the defaults stand)."""
    tag = normalize((config or {}).get('locale'))
    clock = (config or {}).get('clock')
    scope = (config or {}).get('todo_scope')
    _current.update(locale=tag or None, clock=clock if clock in CLOCKS else 'auto', language=language_of(config),
                    chosen=code((config or {}).get('language')) is not None, todo_scope=scope if scope in SCOPES else None)


def view(config=None):
    """What Settings shows and the dashboard formats with."""
    if config is not None:
        tag, clock = normalize(config.get('locale')) or None, config.get('clock') if config.get('clock') in CLOCKS else 'auto'
        language, chosen = language_of(config), code(config.get('language')) is not None
        scope = config.get('todo_scope') if config.get('todo_scope') in SCOPES else None
    else:
        tag, clock, language, chosen = _current['locale'], _current['clock'], _current['language'] or 'en', _current.get('chosen', False)
        scope = _current.get('todo_scope')
    return {'locale': tag, 'region': region(tag), 'language': language, 'language_set': chosen, 'clock': clock, 'todo_scope': scope,
            'hour12': hour12(tag, clock), 'auto_hour12': hour12(tag), 'date_locale': date_locale(tag, language), 'languages': LANGUAGES}


@functools.lru_cache(maxsize=1)
def zone_countries():
    """{'Europe/Brussels': 'BE', ...} from the system's zone.tab (as the control plane does at signup)."""
    text = ''
    for folder in zoneinfo.TZPATH:
        path = Path(folder) / 'zone.tab'
        if path.exists():
            text = path.read_text(encoding='utf-8', errors='replace')
            break
    else:
        try:
            import importlib.resources
            text = (importlib.resources.files('tzdata') / 'zoneinfo' / 'zone.tab').read_text(encoding='utf-8')
        except Exception:  # noqa: BLE001 - no tz database: the language's region alone
            return {}
    out = {}
    for line in text.splitlines():
        parts = line.split('\t')
        if len(parts) >= 3 and not line.startswith('#') and re.fullmatch(r'[A-Z]{2}', parts[0]):
            out[parts[2].strip()] = parts[0]
    return out


def guess(zone, language=''):
    """'en-BE' from a browser's time zone (Europe/Brussels), else the region of its language (en-GB); None when neither
    says (UTC and a bare 'en')."""
    country = zone_countries().get(str(zone or '').strip(), '')
    if not country:
        found = re.fullmatch(r'[A-Za-z]{2,3}[-_]([A-Za-z]{2})', str(language or '').strip()[:20])
        country = found.group(1).upper() if found else ''
    return 'en-' + country if country else None


def settings(changes):
    """{'language', 'locale', 'clock', 'todo_scope'} from the dashboard, checked; a ValueError says what is wrong."""
    out = {}
    if 'language' in changes:
        if not code(changes.get('language')):
            raise ValueError('Pick a language: ' + ', '.join(LANGUAGES))
        out['language'] = code(changes['language'])
    if 'locale' in changes:
        tag = normalize(changes.get('locale'))
        if not tag:
            raise ValueError('Pick a region, like en-US or en-GB')
        out['locale'] = tag
    if 'clock' in changes:
        if changes.get('clock') not in CLOCKS:
            raise ValueError('The time format is auto, 12h or 24h')
        out['clock'] = changes['clock']
    if 'todo_scope' in changes:
        if changes.get('todo_scope') not in SCOPES:
            raise ValueError('Show all, work or personal to-dos')
        out['todo_scope'] = changes['todo_scope']
    if not out:
        raise ValueError('Nothing to change')
    return out


def is_h12():
    return hour12(_current['locale'], _current['clock'])


def clock_text(moment, seconds=False):
    """'2:05 PM' or '14:05' (with seconds: '2:05:09 PM', '14:05:09'), as the owner reads times."""
    if is_h12():
        hour = moment.hour % 12 or 12
        return f'{hour}:{moment:%M}' + (f':{moment:%S}' if seconds else '') + (' AM' if moment.hour < 12 else ' PM')
    return moment.strftime('%H:%M:%S' if seconds else '%H:%M')


# Short day and month names in the other UI languages (English uses strftime's, in the C locale)
NAMES = {
    'nl': ('ma di wo do vr za zo'.split(), 'jan feb mrt apr mei jun jul aug sep okt nov dec'.split()),
    'fr': ('lun. mar. mer. jeu. ven. sam. dim.'.split(), 'janv. févr. mars avr. mai juin juil. août sept. oct. nov. déc.'.split()),
    'de': ('Mo. Di. Mi. Do. Fr. Sa. So.'.split(), 'Jan. Feb. März Apr. Mai Juni Juli Aug. Sep. Okt. Nov. Dez.'.split()),
    'es': ('lun mar mié jue vie sáb dom'.split(), 'ene feb mar abr may jun jul ago sept oct nov dic'.split()),
    'it': ('lun mar mer gio ven sab dom'.split(), 'gen feb mar apr mag giu lug ago set ott nov dic'.split()),
    'pt-BR': ('seg. ter. qua. qui. sex. sáb. dom.'.split(), 'jan. fev. mar. abr. mai. jun. jul. ago. set. out. nov. dez.'.split()),
}
AT = {'en': ' at ', 'nl': ' om ', 'fr': ' à ', 'de': ' um ', 'es': ' a las ', 'it': ' alle ', 'pt-BR': ' às '}


def weekday_name(moment):
    """'Sat', 'za', 'sam.': the short weekday in the owner's language."""
    names = NAMES.get(language())
    return names[0][moment.weekday()] if names else f'{moment:%a}'


def day_text(moment, weekday=True, year=False):
    """'Sat, Oct 24' or 'Sat 24 Oct' (as the dashboard's Intl en-US and en-GB write them), with ', 2026' or ' 2026'. In
    another language day first with its names: 'za 24 okt', 'sam. 24 oct.', 'Sa. 24. Okt.', 'sáb. 24 de out.'."""
    names = NAMES.get(language())
    if names:
        text = f'{moment.day}{"." if language() == "de" else " de" if language() == "pt-BR" else ""} {names[1][moment.month - 1]}'
        return (names[0][moment.weekday()] + ' ' if weekday else '') + text + (f' {moment.year}' if year else '')
    us = (region(_current['locale']) or DEFAULT_REGION) in MONTH_FIRST
    text = (f'{moment:%b} {moment.day}' if us else f'{moment.day} {moment:%b}')
    if weekday:
        text = f'{moment:%a}' + (', ' if us else ' ') + text
    if year:
        text += (', ' if us else ' ') + str(moment.year)
    return text


def span_text(start, end):
    """'Oct 19–23' or '19–23 Oct'; across months 'Oct 30 – Nov 5' or '30 Oct – 5 Nov'."""
    if (start.month, start.year) == (end.month, end.year) and language() in NAMES:
        return f'{start.day}–{day_text(end, weekday=False)}'
    if (start.month, start.year) == (end.month, end.year):
        us = (region(_current['locale']) or DEFAULT_REGION) in MONTH_FIRST
        return f'{end:%b} {start.day}–{end.day}' if us else f'{start.day}–{end.day} {end:%b}'
    return day_text(start, weekday=False) + ' – ' + day_text(end, weekday=False)


def at_text(moment, year=False):
    """'Sat, Oct 24 at 2:05 PM' or 'Sat 24 Oct at 14:05'."""
    return day_text(moment, year=year) + AT.get(language(), ' at ') + clock_text(moment)


def short_text(moment):
    """'Sat 2:05 PM' or 'Sat 14:05': a moment this week."""
    return weekday_name(moment) + ' ' + clock_text(moment)


def range_text(start, end):
    """'2:00 PM–3:00 PM' or '14:00–15:00'."""
    return clock_text(start) + '–' + clock_text(end)

