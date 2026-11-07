"""The Omarchy theme of the computer the Machine runs on, for the dashboard's "Omarchy theme" setting.

Omarchy (omarchy.org) renders the current theme's palette to colors.toml in the user's state folder on every theme
switch, the same file it fills its own app templates from. Only that file is read: nothing in Omarchy's folders is
written, and a computer without Omarchy has no file, so theme() is None and the dashboard never offers the setting.

A leaf module: no imports from the app."""
from pathlib import Path
import re
import tomllib

# Omarchy 4 keeps the current theme under ~/.local/state, Omarchy 3 under ~/.config.
PLACES = ('.local/state/omarchy/current', '.config/omarchy/current')
# The colors the dashboard maps onto its own tokens (dashboard/settings-omarchy.js); every Omarchy theme has these.
KEYS = ('accent', 'background', 'dark_background', 'foreground', 'muted', 'selection', 'red', 'yellow', 'orange',
        'green', 'blue', 'magenta')
REQUIRED = ('accent', 'background', 'foreground')
HEX = re.compile(r'#[0-9a-fA-F]{6}')


def theme(home=None):
    """{'name', 'mode', 'colors'} for the current Omarchy theme, or None when there is none to follow."""
    home = Path(home) if home else Path.home()
    for place in PLACES:
        folder = home / place
        try:
            data = tomllib.loads((folder / 'theme' / 'colors.toml').read_text(encoding='utf-8'))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            continue
        # Only plain #rrggbb colors go on: they end up in the page's style, so nothing else may.
        colors = {k: data[k].lower() for k in KEYS if isinstance(data.get(k), str) and HEX.fullmatch(data[k])}
        if not all(k in colors for k in REQUIRED):
            continue
        try:
            name = (folder / 'theme.name').read_text(encoding='utf-8').strip()[:60]
        except (OSError, UnicodeError):
            name = ''
        mode = 'light' if data.get('mode') == 'light' else 'dark'
        return {'name': re.sub(r'[^\w .+-]', '', name), 'mode': mode, 'colors': colors}
    return None
