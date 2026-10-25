#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build-data.py
APP="$PWD/build/Switch.app"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
swift -module-cache-path "${TMPDIR:-/tmp}/switch-icon-cache" scripts/build-icon.swift "$PWD/build"
python3 - <<'ICON'
from pathlib import Path
import struct
folder=Path('build/Switch.iconset')
entries=[('ic07','icon_128x128.png'),('ic08','icon_256x256.png'),('ic09','icon_512x512.png'),('ic10','icon_512x512@2x.png')]
body=b''
for kind,name in entries:
    data=(folder/name).read_bytes()
    body+=kind.encode()+struct.pack('>I',len(data)+8)+data
Path('build/Switch.app/Contents/Resources/Switch.icns').write_bytes(b'icns'+struct.pack('>I',len(body)+8)+body)
ICON
cp native/Info.plist "$APP/Contents/Info.plist"
cp -R web "$APP/Contents/Resources/"
cp -R native/include "$APP/Contents/Resources/"
for ARCH in arm64 x86_64; do
  swiftc -module-cache-path "${TMPDIR:-/tmp}/switch-swift-$ARCH" -O -target "$ARCH-apple-macos12.0" -framework Cocoa -framework WebKit native/Switch.swift -o "build/Switch-$ARCH"
done
lipo -create build/Switch-arm64 build/Switch-x86_64 -output "$APP/Contents/MacOS/Switch"
codesign --force --deep --sign - "$APP"
codesign --verify --deep --strict "$APP"
mkdir -p dist
cp README.md dist/README.md
cp -R web dist/web
ditto "$APP" dist/Switch.app
COPYFILE_DISABLE=1 ditto -c -k --keepParent "$APP" dist/Switch-macOS.zip
printf 'Built universal Mac app: %s\n' "$PWD/dist/Switch-macOS.zip"
