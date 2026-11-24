#!/bin/bash
# Makes the app from the built program, one for each chip put together: mac/bundle.sh <folder> <program>...
# Signed ad hoc, as Apple silicon asks at least, or by the identity in SIGN. With the hardened runtime either way, and no
# entitlement: it needs none.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
app="$1/The Machine.app"
shift
rm -rf "$app"
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
lipo -create -output "$app/Contents/MacOS/the-machine-desktop" "$@"
cp "$here/Info.plist" "$app/Contents/"

set=$(mktemp -d)/icon.iconset
mkdir "$set"
for size in 16 32 128 256 512; do
  sips -z $size $size "$here/icon.png" --out "$set/icon_${size}x$size.png" > /dev/null
  sips -z $((size * 2)) $((size * 2)) "$here/icon.png" --out "$set/icon_${size}x$size@2x.png" > /dev/null
done
iconutil -c icns -o "$app/Contents/Resources/icon.icns" "$set"

plutil -lint -s "$app/Contents/Info.plist"
time=--timestamp
[ "${SIGN:--}" = - ] && time=--timestamp=none
codesign --force --sign "${SIGN:--}" --options runtime $time "$app"
codesign --verify --strict --verbose=2 "$app"
