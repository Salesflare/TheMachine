"""The AppImage with the runtime desktop.yml pins, in place of the one its tools fetched.

    python3 linux/runtime.py <AppImage> <runtime>

An AppImage is a small program (the runtime) and a squashfs image after it. Tauri's tools fetch the newest type2 runtime
when they build; this puts the one desktop.yml names by release and checksum in its place, and keeps the image as it was,
byte for byte. That runtime is static and mounts with fuse3's fusermount3 (or fuse2's fusermount), so no libfuse is needed.
Nothing is run: both are read as files.
"""

import os
import struct
import sys

SQUASHFS = b"hsqs"


def end_of_elf(data):
    """Where a 64-bit little-endian ELF ends: after its section headers, as the runtime itself finds its image."""
    if data[:4] != b"\x7fELF" or data[4] != 2 or data[5] != 1:
        raise SystemExit("not a 64-bit little-endian ELF")
    shoff, = struct.unpack_from("<Q", data, 0x28)
    shentsize, shnum = struct.unpack_from("<HH", data, 0x3A)
    return shoff + shentsize * shnum


def main(appimage, runtime):
    with open(appimage, "rb") as f:
        old = f.read()
    with open(runtime, "rb") as f:
        new = f.read()
    at = end_of_elf(old)
    if old[at:at + 4] != SQUASHFS:
        raise SystemExit(f"{appimage}: no squashfs image at {at}")
    if end_of_elf(new) != len(new):
        raise SystemExit(f"{runtime}: not a runtime alone")
    out = new + old[at:]
    if out[end_of_elf(out):end_of_elf(out) + 4] != SQUASHFS:
        raise SystemExit("the image isn't where the runtime looks for it")
    part = appimage + ".part"
    with open(part, "wb") as f:
        f.write(out)
    os.chmod(part, 0o755)
    os.replace(part, appimage)
    print(f"{appimage}: runtime {at} bytes replaced by {len(new)}, image {len(old) - at} bytes kept")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
