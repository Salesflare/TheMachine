# Third-party notices

The Machine is open source under AGPL-3.0-only (see [LICENSE](LICENSE)). It does not copy or bundle third-party source code (one font aside, below): it runs on top of software you install yourself, which keeps its own license. This file lists that software and its license, for convenience.

## OpenClaw

The Machine is a service with an OpenClaw plugin. The installer installs OpenClaw from npm (`npm install -g openclaw`); that package ships its own `LICENSE` and `THIRD_PARTY_NOTICES.md`. The plugin imports OpenClaw's plugin SDK at run time from your installation.

```
MIT License

Copyright (c) 2026 OpenClaw Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Node packages

The installer installs these from npm at the exact versions in `package-lock.json` (`npm ci`, no install scripts). The to-do chat uses them to read a to-do's session from the OpenClaw Gateway. Each package ships its own license.

| Package | Version | License |
| --- | --- | --- |
| `@openclaw/gateway-client` | 2026.8.1 | MIT, OpenClaw Foundation |
| `@openclaw/gateway-protocol` | 2026.8.1 | MIT, OpenClaw Foundation |
| `ws` | 8.21.3 | MIT |
| `ipaddr.js` | 2.5.0 | MIT |
| `typebox` | 1.3.16 | MIT |

## Optional tools

Installed from their own package sources only when you use the feature that needs them. Each keeps its own license and copyright notice.

| Software | Used for | License |
| --- | --- | --- |
| Node.js | runs OpenClaw and the plugin | MIT |
| Python | runs the service | PSF License |
| Tailscale | private dashboard access | BSD-3-Clause |
| [`wacli`](https://github.com/openclaw/wacli), installed from the [Salesflare/wacli](https://github.com/Salesflare/wacli) fork (upstream plus read-only profile picture lookups) | local WhatsApp store, owner-approved WhatsApp sends and profile pictures | MIT, Copyright (c) 2026 Peter Steinberger |
| [Telethon](https://codeberg.org/Lonami/Telethon) 1.45.0, unpacked from PyPI by `telegram_release.py` (`telegram-pin.json`) | Telegram chats: the logged-in device, reads and owner-approved sends | MIT, Copyright (c) 2016-Present LonamiWebs |
| [pyaes](https://github.com/ricmoo/pyaes) 1.6.1 | Telethon's AES | MIT, Copyright (c) 2014 Richard Moore |
| [rsa](https://github.com/sybrenstuvel/python-rsa) 4.9.1 | Telethon's RSA | Apache-2.0 |
| [pyasn1](https://github.com/pyasn1/pyasn1) 0.6.4 | used by rsa | BSD-2-Clause |
| [qrcode](https://github.com/lincolnloop/python-qrcode) 8.2 | the Telegram login QR code | BSD-3-Clause |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) 1.2.1 and the packages pinned in `voice-requirements.txt`, installed into their own virtualenv on first use | voice input on your own Machine, with a Whisper model from Hugging Face (`Systran/faster-whisper-small` or `-base`) | MIT; each package keeps its own license |

## Source Serif 4

The dashboard's headings use Source Serif 4 by Adobe, bundled unmodified as `brand/fonts/source-serif-4-latin.woff2` (the Latin subset Google Fonts serves). It is licensed under the SIL Open Font License 1.1; the full license is in [brand/fonts/OFL.txt](brand/fonts/OFL.txt).

## Inter

The dashboard's interface text uses Inter by The Inter Project Authors, bundled unmodified as `brand/fonts/inter-latin.woff2` (the Latin subset Google Fonts serves). It is licensed under the SIL Open Font License 1.1; the full license is in [brand/fonts/Inter-OFL.txt](brand/fonts/Inter-OFL.txt).
