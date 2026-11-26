#!/usr/bin/env bash
# window.py on a screen that isn't there: an X server of its own with nothing to see it, a home, runtime folder and message
# bus of its own, and no browser (what would open one is asked for and shown nowhere). Nothing of a desktop in use is seen or
# touched, its files, keyring and portals neither.
#
#   smoke/linux.sh <sandbox build> <folder for the pictures> [a command instead of window.py]
#
# Needs Xvfb, openbox, dunst, xdotool, xclip, ImageMagick's import, curl, and Python with GTK 3 (gi).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
program="$(realpath "$1")" shots="$2"
shift 2
mkdir -p "$shots"
shots="$(realpath "$shots")"
own="$(mktemp -d "${TMPDIR:-/tmp}/made-up-home-XXXXXX")"
trap 'kill $(jobs -p) 2> /dev/null || true; wait || true; rm -rf "$own"' EXIT
mkdir -p "$own"/{home/Downloads,bin,run} "$own/home/.config/dunst" "$own/home/.config/openbox"
chmod 700 "$own/run"
touch "$own/home/.made-up-home"
echo 'XDG_DOWNLOAD_DIR="$HOME/Downloads"' > "$own/home/.config/user-dirs.dirs"
printf '[global]\nmouse_left_click = do_action, close_current\n[urgency_normal]\ntimeout = 0\n' > "$own/home/.config/dunst/dunstrc"
# What a browser would ask for is asked for
printf '#!/bin/sh\necho "$1" >> "%s/opened.txt"\nexec curl -sL -o /dev/null --max-time 10 "$1"\n' "$shots" > "$own/bin/xdg-open"
chmod +x "$own/bin/xdg-open"
for n in {90..120}; do [ -e "/tmp/.X$n-lock" ] || break; done
Xvfb ":$n" -screen 0 "${SCREEN:-1920x1080x24}" -nolisten tcp 2> "$shots/xvfb.txt" &
for _ in {1..40}; do [ -e "/tmp/.X11-unix/X$n" ] && break; sleep 0.25; done
cat > "$own/go" <<'T'
set -e
openbox &
dunst &
sleep 1
"$@"
T
cd "$here/.."
[ $# -gt 0 ] || set -- /usr/bin/python3 -u smoke/window.py "$program" - "$shots"
env -i PATH="$own/bin:$PATH" LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-}" HOME="$own/home" XDG_RUNTIME_DIR="$own/run" TMPDIR="$own" LANG=C.UTF-8 DISPLAY=":$n" GDK_BACKEND=x11 XDG_SESSION_TYPE=x11 \
  NO_AT_BRIDGE=1 GTK_USE_PORTAL=0 GSETTINGS_BACKEND=memory LIBGL_ALWAYS_SOFTWARE=1 XDG_DATA_DIRS="${XDG_DATA_DIRS:-/usr/local/share:/usr/share}" GDK_SCALE="${SCALE:-1}" GTK_THEME="${THEME:-Adwaita}" \
  dbus-run-session -- bash "$own/go" "$@"
