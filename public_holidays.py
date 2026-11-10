"""Public holidays, so "the 2nd workday of the month" skips them (recurring.py).

Nationwide days off only, for the countries the app's languages are mostly used in; regional ones (a German state, a
Spanish community) are left out. A country not listed here has no holidays: its workdays are Monday to Friday."""
import datetime as dt
import functools

D = dt.date


def easter(year):
    """Easter Sunday (Gregorian, the anonymous algorithm)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    wk = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * wk) // 451
    month, day = divmod(h + wk - 7 * m + 114, 31)
    return D(year, month, day + 1)


def _weekday_in(year, month, weekday, nth):
    """The nth (1..5, or -1 for the last) weekday (0=Monday) of a month."""
    if nth > 0:
        first = D(year, month, 1)
        return first + dt.timedelta(days=(weekday - first.weekday()) % 7 + 7 * (nth - 1))
    last = (D(year + month // 12, month % 12 + 1, 1) - dt.timedelta(days=1))
    return last - dt.timedelta(days=(last.weekday() - weekday) % 7)


def _substitute(days):
    """A holiday on a weekend is also off on the next free weekday (GB): Christmas on a Saturday, Boxing Day on a Sunday."""
    out = set(days)
    for day in sorted(days):
        if day.weekday() > 4:
            extra = day + dt.timedelta(days=1)
            while extra.weekday() > 4 or extra in out:
                extra += dt.timedelta(days=1)
            out.add(extra)
    return out


def _observed_us(days):
    """A US federal holiday on a Saturday is observed the Friday before, on a Sunday the Monday after."""
    out = set(days)
    for day in days:
        if day.weekday() == 5:
            out.add(day - dt.timedelta(days=1))
        elif day.weekday() == 6:
            out.add(day + dt.timedelta(days=1))
    return out


@functools.lru_cache(maxsize=64)
def days_off(region, year):
    """The country's nationwide public holidays in a year, as a frozenset of dates (empty for a country not listed)."""
    region = str(region or '').upper()
    e = easter(year)
    after = lambda n: e + dt.timedelta(days=n)  # noqa: E731
    fixed = lambda *md: {D(year, m, d) for m, d in md}  # noqa: E731
    if region == 'BE':
        days = fixed((1, 1), (5, 1), (7, 21), (8, 15), (11, 1), (11, 11), (12, 25)) | {after(1), after(39), after(50)}
    elif region == 'NL':
        kings = D(year, 4, 27) if D(year, 4, 27).weekday() != 6 else D(year, 4, 26)
        days = fixed((1, 1), (12, 25), (12, 26)) | {after(1), after(39), after(50), kings}
        if year % 5 == 0:
            days.add(D(year, 5, 5))  # Liberation Day, a day off every fifth year
    elif region == 'LU':
        days = fixed((1, 1), (5, 1), (5, 9), (6, 23), (8, 15), (11, 1), (12, 25), (12, 26)) | {after(1), after(39), after(50)}
    elif region == 'FR':
        days = fixed((1, 1), (5, 1), (5, 8), (7, 14), (8, 15), (11, 1), (11, 11), (12, 25)) | {after(1), after(39), after(50)}
    elif region == 'DE':
        days = fixed((1, 1), (5, 1), (10, 3), (12, 25), (12, 26)) | {after(-2), after(1), after(39), after(50)}
    elif region == 'AT':
        days = fixed((1, 1), (1, 6), (5, 1), (8, 15), (10, 26), (11, 1), (12, 8), (12, 25), (12, 26)) | {after(1), after(39), after(50), after(60)}
    elif region == 'CH':
        days = fixed((1, 1), (8, 1), (12, 25)) | {after(39)}
    elif region == 'IT':
        days = fixed((1, 1), (1, 6), (4, 25), (5, 1), (6, 2), (8, 15), (11, 1), (12, 8), (12, 25), (12, 26)) | {after(1)}
    elif region == 'ES':
        days = fixed((1, 1), (1, 6), (5, 1), (8, 15), (10, 12), (11, 1), (12, 6), (12, 8), (12, 25)) | {after(-2)}
    elif region == 'PT':
        days = fixed((1, 1), (4, 25), (5, 1), (6, 10), (8, 15), (10, 5), (11, 1), (12, 1), (12, 8), (12, 25)) | {after(-2), after(60)}
    elif region == 'BR':
        days = fixed((1, 1), (4, 21), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (12, 25)) | {after(-2)}
        if year >= 2024:
            days.add(D(year, 11, 20))
    elif region == 'IE':
        days = _substitute(fixed((1, 1), (3, 17), (12, 25), (12, 26))) | {after(1), _weekday_in(year, 5, 0, 1), _weekday_in(year, 6, 0, 1),
                                                                          _weekday_in(year, 8, 0, 1), _weekday_in(year, 10, 0, -1)}
        if year >= 2023:
            feb = D(year, 2, 1)
            days.add(feb if feb.weekday() == 4 else _weekday_in(year, 2, 0, 1))
    elif region == 'GB':
        days = _substitute(fixed((1, 1), (12, 25), (12, 26))) | {after(-2), after(1), _weekday_in(year, 5, 0, 1), _weekday_in(year, 5, 0, -1),
                                                                 _weekday_in(year, 8, 0, -1)}
    elif region == 'US':
        days = _observed_us(fixed((1, 1), (6, 19), (7, 4), (11, 11), (12, 25))) | {
            _weekday_in(year, 1, 0, 3), _weekday_in(year, 2, 0, 3), _weekday_in(year, 5, 0, -1), _weekday_in(year, 9, 0, 1),
            _weekday_in(year, 10, 0, 2), _weekday_in(year, 11, 3, 4)}
    else:
        days = set()
    return frozenset(days)


def known(region):
    """Whether this country's holidays are listed here."""
    return bool(days_off(region, 2026))


def is_workday(day, region=None):
    return day.weekday() < 5 and day not in days_off(region, day.year)
