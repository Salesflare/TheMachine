"""Draws icons/badges.png: the number on the app's taskbar button on Windows (windows_app.rs), 1 to 99 and then 99+.

  python3 tools/badges.py     # needs ImageMagick 7 (magick); by hand, when the look changes, never in CI

They look as the dashboard's own number does when it is installed as an app (navigator.setAppBadge): Chrome and Edge
draw it on Windows as a dark circle with the number in white, its ink centered and as large as fits a box of 10/16 of the
circle (taskbar_decorator_win.cc), and above 99 they say 99+ (badge_manager.cc). Here in the dashboard's font, Inter. Each
is drawn 8 times larger and made smaller, so its edges and the number's are smooth at 32 x 32, the size Windows takes.
Ten in a row, ten rows: badge n is at column (n - 1) % 10, row (n - 1) // 10.
"""
import pathlib
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent.parent
FONT = HERE.parent / 'brand' / 'fonts' / 'inter-latin.woff2'
SIDE, LARGER = 32, 8
BIG = SIDE * LARGER
UNIT = BIG / 16  # Chrome draws on 16 x 16
CIRCLE, INK = '#26252D', 'white'  # Chrome's, the color of Windows' own badges
# Inter's digits are wider than those of Segoe UI, the font Chrome draws them in on Windows ("20": 1.47 times as wide as
# high, against 1.3): the box is as much wider, so a number is as high as there
WIDER = 1.13
BOLDER = 0.5  # its lines as thick as Chrome's 16 pixels' are when Windows makes them larger


def magick(*args):
    return subprocess.run(['magick', *map(str, args)], check=True, capture_output=True, text=True).stdout


def ink(text, size, into):
    """The number at this size, cut to its ink."""
    magick('-background', 'none', '-fill', INK, '-stroke', INK, '-strokewidth', BOLDER * UNIT, '-font', FONT, '-pointsize', size * UNIT,
           f'label:{text}', '-trim', '+repage', into)
    return tuple(map(int, magick(into, '-format', '%w %h', 'info:').split()))


def badge(text, folder):
    """As Chrome does: from 24 down to 7, the first size whose ink fits 10 x 10 of the 16."""
    number = folder / 'number.png'
    for size in range(24, 6, -1):
        wide, high = ink(text, size, number)
        if wide <= 10 * WIDER * UNIT and high <= 10 * UNIT:
            break
    one = folder / f'{text.replace("+", "plus")}.png'
    magick('-size', f'{BIG}x{BIG}', 'xc:none', '-fill', CIRCLE, '-draw', f'circle {BIG / 2 - 0.5},{BIG / 2 - 0.5} {BIG / 2 - 0.5},-0.5',
           number, '-geometry', f'+{round((BIG - wide) / 2)}+{round((BIG - high) / 2)}', '-composite',
           '-filter', 'box', '-resize', f'{SIDE}x{SIDE}', one)
    return one


def main():
    with tempfile.TemporaryDirectory() as folder:
        folder = pathlib.Path(folder)
        each = [badge(str(n) if n < 100 else '99+', folder) for n in range(1, 101)]
        rows = [folder / f'row{r}.png' for r in range(10)]
        for r, row in enumerate(rows):
            magick(*each[r * 10:r * 10 + 10], '-background', 'none', '+append', row)
        magick(*rows, '-background', 'none', '-append', '-strip', '-depth', '8', '-define', 'png:color-type=6', HERE / 'icons' / 'badges.png')


if __name__ == '__main__':
    main()
