#!/usr/bin/env bash
# A command on a Wayland screen that isn't there: sway on its headless backend (wlroots, with layer-shell as Hyprland has it),
# no XWayland, and a home, runtime folder and message bus of its own. For CI's throwaway computers (desktop.yml): never on a
# desktop in use.
#
#   smoke/wayland.sh <folder for the pictures> <command...>
#
# Needs sway, grim, dbus and Python.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
shots="$1"
shift
mkdir -p "$shots"
shots="$(realpath "$shots")"
own="$(mktemp -d "${TMPDIR:-/tmp}/made-up-home-XXXXXX")"
trap 'kill $(jobs -p) 2> /dev/null || true; wait || true; rm -rf "$own"' EXIT
mkdir -p "$own"/{home/Downloads,bin,run}
chmod 700 "$own/run"
touch "$own/home/.made-up-home"
# What a browser would ask for is asked for
printf '#!/bin/sh\necho "$1" >> "%s/opened.txt"\n' "$shots" > "$own/bin/xdg-open"
chmod +x "$own/bin/xdg-open"
printf 'xwayland disable\noutput * resolution 1920x1080\n' > "$own/sway.conf"
plain=(PATH="$own/bin:$PATH" HOME="$own/home" XDG_RUNTIME_DIR="$own/run" TMPDIR="$own" LANG=C.UTF-8)
env -i "${plain[@]}" WLR_BACKENDS=headless WLR_RENDERER=pixman WLR_LIBINPUT_NO_DEVICES=1 WLR_HEADLESS_OUTPUTS=1 \
  sway -c "$own/sway.conf" > "$shots/sway.txt" 2>&1 &
for _ in {1..80}; do compgen -G "$own/run/sway-ipc.*" > /dev/null && compgen -G "$own/run/wayland-?" > /dev/null && break; sleep 0.25; done
plain+=(WAYLAND_DISPLAY="$(basename "$(compgen -G "$own/run/wayland-?" | head -1)")" SWAYSOCK="$(compgen -G "$own/run/sway-ipc.*" | head -1)")
[ "$(env -i "${plain[@]}" swaymsg -t get_outputs -r)" != "[]" ] || env -i "${plain[@]}" swaymsg create_output > /dev/null
env -i "${plain[@]}" swaymsg -t get_outputs > "$shots/outputs.txt"
cd "$here/.."
env -i "${plain[@]}" XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway NO_AT_BRIDGE=1 GTK_USE_PORTAL=0 GSETTINGS_BACKEND=memory LIBGL_ALWAYS_SOFTWARE=1 \
  XDG_DATA_DIRS="${XDG_DATA_DIRS:-/usr/local/share:/usr/share}" GTK_THEME=Adwaita dbus-run-session -- "$@"
