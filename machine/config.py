"""Where the app and its files are, and the app's fixed settings: the app folder (ROOT), the rule and source-note files,
the OpenClaw workspace, the config file, the brand assets the dashboard serves and the log every module writes to
(always the logger 'personal-assistant', never __name__). Moved out of assistant.py as is, apart from ROOT, which is
the app folder above machine/."""
import logging
import os
from pathlib import Path

import voice_input

ROOT = Path(__file__).resolve().parent.parent


# How reviews and Do it work; edits show as markers on the hit-rate chart.
RULE_FILES = (ROOT / 'AGENTS.md', ROOT / 'PREPARATION.md')


# How to read each connector (source-notes/<service>.md): a review or Do it gets only the notes for sources it has.
SOURCE_NOTES = ROOT / 'source-notes'


SOURCE_NOTE_ALIASES = {'outlook_calendar': 'calendar'}


# The OpenClaw agent workspace (memory/, data/, USER.md). Override with OPENCLAW_WORKSPACE.
WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE') or Path.home() / '.openclaw/workspace').expanduser()


BROWSER_LEASE = WORKSPACE / 'data/browser-lease/lease.json'


# Served from the bundled brand/ folder. Replace these files to rebrand the dashboard.
BRAND_ASSETS = {
    '/brand/avatar.png': ROOT / 'brand/app-icon-192.png',
    '/brand/avatar-blink.png': ROOT / 'brand/avatar-blink.png',  # the same robot, eyes closed: replace it with avatar.png
    '/brand/favicon-32.png': ROOT / 'brand/app-icon-192.png',
    '/brand/favicon-512.png': ROOT / 'brand/app-icon-maskable-512.png',
    # The robot's moods (stickers, 256 px): nothing to do, can't reach the assistant, nothing found.
    '/brand/sleepy.webp': ROOT / 'brand/sleepy.webp',
    '/brand/sad.webp': ROOT / 'brand/sad.webp',
    '/brand/thinking.webp': ROOT / 'brand/thinking.webp',
    # Inbox-zero game: poked awake, catching a Z, a new best.
    '/brand/wave.webp': ROOT / 'brand/wave.webp',
    # The waving robot while it works (the first look, setting up): eyes closed, a glance aside, the hand's lines moved.
    '/brand/wave-blink.webp': ROOT / 'brand/wave-blink.webp',
    '/brand/wave-look.webp': ROOT / 'brand/wave-look.webp',
    '/brand/wave-hand.webp': ROOT / 'brand/wave-hand.webp',
    '/brand/laugh.webp': ROOT / 'brand/laugh.webp',
    '/brand/party.webp': ROOT / 'brand/party.webp',
    # Home-screen app icons; maskable ones keep the robot inside Android's crop.
    '/brand/app-icon-192.png': ROOT / 'brand/app-icon-192.png',
    '/brand/app-icon-maskable-192.png': ROOT / 'brand/app-icon-maskable-192.png',
    '/brand/app-icon-maskable-512.png': ROOT / 'brand/app-icon-maskable-512.png',
    '/brand/app-icon-badge-96.png': ROOT / 'brand/app-icon-badge-96.png',  # monochrome status-bar icon for pushes
    # Heading typeface (Source Serif 4, SIL OFL; license in brand/fonts/OFL.txt).
    '/brand/serif.woff2': ROOT / 'brand/fonts/source-serif-4-latin.woff2',
    # Interface typeface (Inter, SIL OFL; license in brand/fonts/Inter-OFL.txt).
    '/brand/sans.woff2': ROOT / 'brand/fonts/inter-latin.woff2',
    # Talk live's voices, a short sample each for Settings (voice_input.TALK_VOICES)
    **{f'/brand/voices/{name}.mp3': ROOT / f'brand/voices/{name}.mp3' for name in voice_input.TALK_VOICES},
    # The services' logos for Connections, + Add, each loaded when shown (their sources and terms: dashboard/logos/NOTICE.md)
    **{f'/brand/logos/{logo.name}': logo for logo in sorted((ROOT / 'dashboard/logos').glob('*.svg'))},
}


DEFAULT_CONFIG = Path(os.environ.get('ASSISTANT_CONFIG') or Path.home() / '.local/share/personal-assistant/config.json').expanduser()


LOG = logging.getLogger('personal-assistant')


# A sync error that a new sign-in ends: Google's or Microsoft's sign-in expired or revoked, or Gmail's or Calendar's 401 (gog's
# "HTTP_401" once Google revoked the grant). The sync watches for that sign-in, and a reconnect clears it at once.
SIGNIN_ERROR = r'(google|microsoft)_signin_(expired|pending)|microsoft_broker|\b(gmail|calendar):HTTP_401\b'
