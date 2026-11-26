#!/bin/bash
# Makes the app from the built program, one for each chip put together: mac/bundle.sh <folder> <program>...
# Signed ad hoc, as Apple silicon asks at least, or by the identity in SIGN. With the hardened runtime either way, and one
# entitlement: the microphone, which macOS still asks the person about.
# STORE=1: the Mac App Store's build (README.md), in the App Sandbox (store-entitlements.plist), for macOS 14 and later,
# with the ID in BUNDLE_ID (else Info.plist's), the build number in BUILD_NUMBER and the provisioning profile in PROFILE.
# Signed ad hoc, it has neither its app's nor its team's entitlement, which only a profile allows; all of them are left
# beside the app, for the store's signature.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
app="$1/The Machine.app"
shift
rm -rf "$app"
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
lipo -create -output "$app/Contents/MacOS/the-machine-desktop" "$@"
cp "$here/Info.plist" "$app/Contents/"
entitlements="$here/entitlements.plist"
if [ "${STORE:-}" = 1 ]; then
  info="$app/Contents/Info.plist" entitlements=$(mktemp -d)/entitlements.plist
  cp "$here/store-entitlements.plist" "$entitlements"
  id=${BUNDLE_ID:-$(plutil -extract CFBundleIdentifier raw "$info")}
  plutil -replace CFBundleIdentifier -string "$id" "$info"
  plutil -replace LSMinimumSystemVersion -string 14.0 "$info"
  plutil -replace CFBundleVersion -string "${BUILD_NUMBER:-1}" "$info" # the store takes each build number once
  team=$(plutil -extract 'com\.apple\.developer\.team-identifier' raw "$entitlements")
  plutil -replace 'com\.apple\.application-identifier' -string "$team.$id" "$entitlements"
  cp "$entitlements" "$(dirname "$app")/store-entitlements.plist" # all of them, for the store's signature (desktop.yml)
  if [ "${SIGN:--}" = - ]; then
    plutil -remove 'com\.apple\.application-identifier' "$entitlements"
    plutil -remove 'com\.apple\.developer\.team-identifier' "$entitlements"
  fi
  if [ -n "${PROFILE:-}" ]; then cp "$PROFILE" "$app/Contents/embedded.provisionprofile"; fi
fi

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
codesign --force --sign "${SIGN:--}" --options runtime --entitlements "$entitlements" $time "$app"
codesign --verify --strict --verbose=2 "$app"
