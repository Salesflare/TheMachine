#!/usr/bin/env bash
# Whether the app's web view needs a user namespace of its own, which Ubuntu 23.10 and newer and Debian 13 let AppArmor refuse
# (kernel.apparmor_restrict_unprivileged_userns). Writes, every half second until stopped, each of the app's and WebKit's
# processes (and bubblewrap's, which WebKit's sandbox starts) with its user namespace, and each FUSE mount of an AppImage.
#
#   smoke/namespaces.sh <file>        stop it with kill; then: sort -u <file>
set -uo pipefail
out="$1"
: > "$out"
trap 'exit 0' TERM INT
while true; do
  for comm in /proc/[0-9]*/comm; do
    read -r name 2> /dev/null < "$comm" || continue
    case "$name" in
      the-machine-des*|WebKit*|bwrap|xdg-dbus-proxy)
        pid="${comm%/comm}"
        echo "process $name $(readlink "$pid/ns/user" 2> /dev/null)" >> "$out" ;;
    esac
  done
  grep -o ' [^ ]*/\.mount_[^ ]* fuse[^ ]*' /proc/mounts | sed 's/^/mount/' >> "$out" || true
  sleep 0.5
done
