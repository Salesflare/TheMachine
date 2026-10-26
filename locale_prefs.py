"""Language and region: how dates and times read on the dashboard, in cards, Telegram, the digest and Fleet messages
(Settings, General).

`locale` in config.json is a language-REGION tag like en-US, en-GB or en-BE. The language is English for now (the
only one the app speaks; others come with translations), the region sets the date order (Oct 24 or 24 Oct) and the
default clock. `clock` is '12h' or '24h' when the owner overrides the region's. A hosted Machine gets its first
`locale` from signup (ASSISTANT_LOCALE at install). A Machine without one (self-hosted) gets it the same way from the
dashboard's first load (guess: the country of the browser's time zone, else its language's region), and keeps US
dates and a 24-hour clock until then.

The dashboard gets view() and formats with the same rules (dashboard.html, applyLocale)."""
from __future__ import annotations

import functools
import re
import zoneinfo
from pathlib import Path

LANGUAGES = {'en': 'English'}  # UI languages; a tag in another language keeps its region and reads English for now
DEFAULT_REGION = 'US'  # dates without a locale
CLOCKS = ('auto', '12h', '24h')
# Regions whose people mostly read a 12-hour clock (CLDR's preferred hour cycle "h"); the rest read 24-hour.
H12 = frozenset('US CA AU NZ IN PK BD PH MY SG HK TW KR EG SA AE JO KW QA BH OM IQ SY LB YE LY SD CO VE SV HN NI GT DO '
                'PR GU AS VI MP UM'.split())
# Regions that put the month first (Oct 24); the rest read the day first (24 Oct).
MONTH_FIRST = frozenset('US CA PH PR GU AS VI MP UM FM MH PW'.split())

_current = {'locale': None, 'clock': 'auto'}


def normalize(value):
    """'en-BE' from 'en-BE', 'en_be' or 'nl-BE' (English for now), '' for no setting, None when it isn't a tag."""
    text = str(value or '').strip().replace('_', '-')
    if not text:
        return ''
    found = re.fullmatch(r'([A-Za-z]{2,3})-([A-Za-z]{2})', text)
    if not found:
        return None
    language = found.group(1).lower()
    return (language if language in LANGUAGES else 'en') + '-' + found.group(2).upper()


def region(locale):
    """'BE' for en-BE; '' without a locale."""
    tag = normalize(locale)
    return tag.split('-')[1] if tag else ''


def hour12(locale, clock='auto'):
    """True when times read 2:00 PM: the owner's choice, else the region's; a Machine without a locale stays 24-hour."""
    if clock in ('12h', '24h'):
        return clock == '12h'
    return region(locale) in H12


def date_locale(locale):
    """The Intl locale the dashboard formats dates with: US order (Sat, Oct 24) or day first (Sat 24 Oct)."""
    return 'en-US' if (region(locale) or DEFAULT_REGION) in MONTH_FIRST else 'en-GB'


def configure(config):
    """Use the owner's setting from config.json; a bad value is ignored (the defaults stand)."""
    tag = normalize((config or {}).get('locale'))
    clock = (config or {}).get('clock')
    _current.update(locale=tag or None, clock=clock if clock in CLOCKS else 'auto')


def view(config=None):
    """What Settings shows and the dashboard formats with."""
    if config is not None:
        tag, clock = normalize(config.get('locale')) or None, config.get('clock') if config.get('clock') in CLOCKS else 'auto'
    else:
        tag, clock = _current['locale'], _current['clock']
    return {'locale': tag, 'region': region(tag), 'language': (tag or 'en-US').split('-')[0], 'clock': clock,
            'hour12': hour12(tag, clock), 'auto_hour12': hour12(tag), 'date_locale': date_locale(tag), 'languages': LANGUAGES}


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
    """{'locale', 'clock'} from the dashboard, checked; a ValueError says what is wrong."""
    out = {}
    if 'locale' in changes:
        tag = normalize(changes.get('locale'))
        if not tag:
            raise ValueError('Pick a region, like en-US or en-GB')
        out['locale'] = tag
    if 'clock' in changes:
        if changes.get('clock') not in CLOCKS:
            raise ValueError('The time format is auto, 12h or 24h')
        out['clock'] = changes['clock']
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


def day_text(moment, weekday=True, year=False):
    """'Sat, Oct 24' or 'Sat 24 Oct' (as the dashboard's Intl en-US and en-GB write them), with ', 2026' or ' 2026'."""
    us = (region(_current['locale']) or DEFAULT_REGION) in MONTH_FIRST
    text = (f'{moment:%b} {moment.day}' if us else f'{moment.day} {moment:%b}')
    if weekday:
        text = f'{moment:%a}' + (', ' if us else ' ') + text
    if year:
        text += (', ' if us else ' ') + str(moment.year)
    return text


def span_text(start, end):
    """'Oct 19–23' or '19–23 Oct'; across months 'Oct 30 – Nov 5' or '30 Oct – 5 Nov'."""
    if (start.month, start.year) == (end.month, end.year):
        us = (region(_current['locale']) or DEFAULT_REGION) in MONTH_FIRST
        return f'{end:%b} {start.day}–{end.day}' if us else f'{start.day}–{end.day} {end:%b}'
    return day_text(start, weekday=False) + ' – ' + day_text(end, weekday=False)


def at_text(moment, year=False):
    """'Sat, Oct 24 at 2:05 PM' or 'Sat 24 Oct at 14:05'."""
    return day_text(moment, year=year) + ' at ' + clock_text(moment)


def short_text(moment):
    """'Sat 2:05 PM' or 'Sat 14:05': a moment this week."""
    return f'{moment:%a} ' + clock_text(moment)


def range_text(start, end):
    """'2:00 PM–3:00 PM' or '14:00–15:00'."""
    return clock_text(start) + '–' + clock_text(end)

