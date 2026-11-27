"""The gtk-layer-shell the app brings, with the GTK of the computer it runs on: one layer surface (as the robot and the bubble)
and one plain window (as the dashboard), whose popups must not crash the program. gtk-layer-shell watches every window's
popups, and reads GTK's own structures as the GTK versions it knows lay them out: on a newer GTK an old one read the wrong
field, and a right-click menu, a <select>, a tooltip or a move to another workspace crashed the app (gdk_window_get_toplevel).
For CI's throwaway computers only (desktop.yml), on wayland.sh's sway, with the library to try first on LD_LIBRARY_PATH.

  python3 smoke/popups.py <gtk-layer-shell version it must be, as 0.10.1>
"""
import os
import pathlib
import shutil
import subprocess
import sys

import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gdk, GLib, Gtk, GtkLayerShell  # noqa: E402

if not (pathlib.Path.home() / '.made-up-home').exists():
    sys.exit('only by wayland.sh')
wanted = sys.argv[1]
have = f'{GtkLayerShell.get_major_version()}.{GtkLayerShell.get_minor_version()}.{GtkLayerShell.get_micro_version()}'
print(f'gtk {Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}, gtk-layer-shell {have}', flush=True)
if have != wanted:
    sys.exit(f'gtk-layer-shell {have} was loaded, not {wanted}')
if not GtkLayerShell.is_supported():
    sys.exit('no layer-shell on this compositor')

bubble = Gtk.Window()
GtkLayerShell.init_for_window(bubble)
GtkLayerShell.set_namespace(bubble, 'the-machine-bubble')
GtkLayerShell.set_layer(bubble, GtkLayerShell.Layer.TOP)
for edge in (GtkLayerShell.Edge.RIGHT, GtkLayerShell.Edge.BOTTOM):
    GtkLayerShell.set_anchor(bubble, edge, True)
bubble.add(Gtk.Label(label='bubble'))
bubble.set_size_request(200, 80)
bubble.show_all()

main = Gtk.Window(title='the-machine-dashboard')
main.set_default_size(800, 600)
column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
pick = Gtk.ComboBoxText()
for text in ('one', 'two', 'three'):
    pick.append_text(text)
pick.set_active(0)
column.pack_start(pick, False, False, 0)
main.add(column)
main.show_all()

menu = Gtk.Menu()
for text in ('Copy', 'Paste', 'Inspect Element'):
    menu.append(Gtk.MenuItem(label=text))
menu.show_all()
menu.attach_to_widget(main)

tip = Gtk.Window(type=Gtk.WindowType.POPUP)  # what WebKit shows for a title on hover
tip.set_type_hint(Gdk.WindowTypeHint.TOOLTIP)
tip.set_transient_for(main)
tip.add(Gtk.Label(label='a tooltip'))


def spot():
    at = Gdk.Rectangle()
    at.x, at.y, at.width, at.height = 40, 40, 1, 1
    return at


def right_click():
    menu.popup_at_rect(main.get_window(), spot(), Gdk.Gravity.NORTH_WEST, Gdk.Gravity.NORTH_WEST, None)


def hover():
    tip.show_all()
    tip.get_window().move_to_rect(spot(), Gdk.Gravity.SOUTH, Gdk.Gravity.NORTH, Gdk.AnchorHints.FLIP_Y, 0, 4)


def workspace(name):
    sway = shutil.which('swaymsg')
    if sway and os.environ.get('SWAYSOCK'):
        subprocess.run([sway, f'[title="the-machine-dashboard"] move to workspace {name}; workspace {name}'], check=True,
                       capture_output=True, timeout=10)


steps = [
    ('right-click menu', right_click),
    ('menu closed', menu.popdown),
    ('tooltip', hover),
    ('tooltip moved', lambda: tip.get_window().move_to_rect(spot(), Gdk.Gravity.NORTH, Gdk.Gravity.SOUTH, Gdk.AnchorHints.FLIP_Y, 0, 4)),
    ('moved to another workspace, the tooltip still up', lambda: workspace('2')),
    ('tooltip closed', tip.hide),
    ('select', pick.popup),
    ('select closed', pick.popdown),
    ('resized', lambda: main.resize(600, 400)),
    ('hidden', main.hide),
    ('shown', main.show),
    ('back to the first workspace', lambda: workspace('1')),
    ('right-click menu again', right_click),
    ('menu closed again', menu.popdown),
]


def run(i=0):
    if i == len(steps):
        print('all popups opened and closed', flush=True)
        Gtk.main_quit()
        return False
    name, do = steps[i]
    print(name, flush=True)
    do()
    GLib.timeout_add(400, run, i + 1)
    return False


def late():
    print('timed out', flush=True)
    os._exit(3)


GLib.timeout_add(1000, run)
GLib.timeout_add_seconds(60, late)
Gtk.main()
