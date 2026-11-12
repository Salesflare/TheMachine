#!/usr/bin/env python3
"""Install, upgrade or remove The Machine for the current user.

    ./install.sh                     interactive install, or upgrade of an existing install
    ./install.sh --non-interactive   read answers from ASSISTANT_* environment variables
    ./install.sh --preview           one review of the last 7 days, shown only; nothing is sent
    ./install.sh --uninstall         remove the service, plugin and CLI link; keep data
    ./install.sh --browser-viewer    existing install: give the assistant a browser of its own that you watch and
                                     use from yours (noVNC on 127.0.0.1:6080; see browser_viewer.py)
    ./install.sh --uninstall --purge also delete the data directory (config, database, secrets)
    ./install.sh --dry-run           check prerequisites and show what would be written; changes nothing

Linux runs the service as a systemd user unit, macOS as a launchd agent (service.py). On Windows, run
install.ps1: it sets up WSL2 and runs this installer inside it.

In a terminal, a healthy install goes on to connect each source (onboarding.py: sign-ins,
keys and IDs, a test read and the first sync), offers the dashboard on your tailnet and a
starter USER.md, then a preview review and, after it, turning reviews and Telegram on.

Without OpenClaw, a terminal install offers to install it (npm, after a yes) and then hands
over to OpenClaw's own setup (`openclaw onboard`: your model, the Gateway service, Telegram),
saying first what The Machine needs from it.

Re-running is safe: an existing config.json is kept, missing keys are added, and secrets
are only created when absent. OpenClaw's own configuration is only read (your approved
Telegram ID, paired phones); the installer changes nothing there beyond `openclaw plugins
install/enable/uninstall`, approving your own Telegram pairing request if you say yes, and
OpenClaw's own setup commands when it offers them and you say yes.
In your OpenClaw workspace it adds memory rules to AGENTS.md once, and later replaces only a block that is still
exactly as it wrote it (see memory_rules).
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

import google_pair
import locale_prefs
import message_seal
import onboarding
import openclaw_pin
import service
from onboarding import CONNECTORS, expand, write_private

ROOT = Path(__file__).resolve().parent
PLUGIN_ID = 'personal-assistant-bridge'
UNIT_NAME = service.UNIT_NAME
MIN_PYTHON = (3, 12)
# The Node.js an OpenClaw that is already set up runs The Machine with, and the one installing the pinned OpenClaw
# needs (the Node releases with October 2026's TLS fixes, which OpenClaw required from 2026.10.6; 2026.11.2 accepts
# 24.16+ and 26.1+ again, and installs keep the stricter floor).
NODE_REQUIREMENT = '>=24.16.0 <25 or >=26.1.0'
NODE_FLOORS = {24: (24, 16, 0), 26: (26, 1, 0)}
OPENCLAW_NODE_REQUIREMENT = '>=24.22.1 <25 or >=26.12.1'
OPENCLAW_NODE_FLOORS = {24: (24, 22, 1), 26: (26, 12, 1)}


MACOS = service.manager() == 'launchd'


def supported_node(version, floors=NODE_FLOORS):
    """Node 24 from its floor, Node 26 from its floor and anything newer; 22, 25 and older lines are not."""
    if not version:
        return False
    if version[0] == 24:
        return version >= floors[24]
    return version >= floors[26]

# Answers for --non-interactive (and defaults for the wizard).
ENV = {
    'owner_name': 'ASSISTANT_OWNER_NAME',
    'telegram_owner': 'ASSISTANT_TELEGRAM_OWNER',
    'tailscale_owner': 'ASSISTANT_TAILSCALE_OWNER',
    'dashboard_host': 'ASSISTANT_DASHBOARD_HOST',
    'timezone': 'ASSISTANT_TIMEZONE',
    'locale': 'ASSISTANT_LOCALE',               # language-region for dates and times, e.g. en-GB (hosted: from signup)
    'connectors': 'ASSISTANT_CONNECTORS',       # comma list: gmail,calendar,gateway,android,whatsapp,telegram,slack,crm (or none)
    'email': 'ASSISTANT_EMAIL',                 # Google account for gmail/calendar
    'gog_client': 'ASSISTANT_GOG_CLIENT',
    'boundary': 'ASSISTANT_BOUNDARY',           # e.g. work:Acme
    'android_node_id': 'ASSISTANT_ANDROID_NODE_ID',
    'whatsapp_store': 'ASSISTANT_WHATSAPP_STORE',
}
class Paths:
    def __init__(self, home=None):
        self.home = Path(home or os.environ.get('HOME') or Path.home())
        self.data = self.home / '.local/share/personal-assistant'
        self.config = Path(os.environ.get('ASSISTANT_CONFIG') or self.data / 'config.json')
        self.unit = service.definition_path(UNIT_NAME, self.home)
        self.cli = self.home / '.local/bin/assistant'
        self.workspace = Path(os.environ.get('OPENCLAW_WORKSPACE') or self.home / '.openclaw/workspace')


# A first install in a terminal runs the steps that need no answers (bytecode, Node packages, the OpenClaw bridge and
# settings) while the questions are asked (Ahead). Their lines are kept for after the questions, their programs never
# read the terminal, and OpenClaw is never called by both at once (OPENCLAW_TURN: the questions' Telegram pairing).
_ahead = threading.local()
OPENCLAW_TURN = threading.Lock()


def say(*parts):
    lines = getattr(_ahead, 'lines', None)
    if lines is not None:
        lines.append(' '.join(str(p) for p in parts))
        return
    print(*parts, flush=True)


def version_tuple(text):
    found = re.search(r'(\d+)\.(\d+)(?:\.(\d+))?', text or '')
    return tuple(int(x or 0) for x in found.groups()) if found else None


def run(args, check=False, **kwargs):
    kwargs.setdefault('capture_output', True)
    kwargs.setdefault('text', True)
    behind = getattr(_ahead, 'lines', None) is not None
    if behind:  # the terminal belongs to the questions
        kwargs['capture_output'] = True
        if 'input' not in kwargs:
            kwargs['stdin'] = subprocess.DEVNULL
    try:
        if behind:
            with OPENCLAW_TURN:
                return subprocess.run(args, check=check, timeout=kwargs.pop('timeout', 120), **kwargs)
        return subprocess.run(args, check=check, timeout=kwargs.pop('timeout', 120), **kwargs)
    except (OSError, subprocess.TimeoutExpired) as error:
        return subprocess.CompletedProcess(args, 127, '', str(error))


# ---------------------------------------------------------------- prerequisites

def required_openclaw():
    package = json.loads((ROOT / 'openclaw-plugin/package.json').read_text())
    return package.get('peerDependencies', {}).get('openclaw', '')


def resolve_tool(binary):
    """Resolve symlinks and mise/asdf shims without depending on a shell startup file."""
    if not binary:
        return None
    path = Path(binary)
    if 'shims' in path.parts:
        for manager in ('mise', 'asdf'):
            command = shutil.which(manager)
            if command:
                result = run([command, 'which', path.name])
                candidate = Path(result.stdout.strip())
                if result.returncode == 0 and candidate.is_file() and candidate != path:
                    return str(candidate.absolute())
    return str(path.absolute())


def openclaw_package_dir(binary, node=None):
    """The installed openclaw npm package (for the Node helpers), found from the CLI's real path."""
    if not binary:
        return None
    path = Path(binary).resolve()
    for parent in [path.parent, *path.parents]:
        manifest = parent / 'package.json'
        if manifest.exists():
            try:
                if json.loads(manifest.read_text()).get('name') == 'openclaw':
                    return parent
            except ValueError:
                pass
    guesses = [Path(binary).parent.parent / 'lib/node_modules/openclaw']
    if node:
        guesses.append(Path(node).resolve().parent.parent / 'lib/node_modules/openclaw')
    npm = shutil.which('npm')
    if npm:
        result = run([npm, 'root', '-g'])
        if result.returncode == 0 and result.stdout.strip():
            guesses.append(Path(result.stdout.strip()) / 'openclaw')
    for guess in guesses:
        manifest = guess / 'package.json'
        try:
            if json.loads(manifest.read_text()).get('name') == 'openclaw':
                return guess.resolve()
        except (OSError, ValueError):
            pass
    return None


def check_prerequisites():
    """Report what is there; return (ok, facts). Python, Node and OpenClaw are required."""
    facts, ok = {}, True
    say('Checking prerequisites')
    py = sys.version_info[:2]
    if py >= MIN_PYTHON:
        say(f'  ok    python {py[0]}.{py[1]} ({sys.executable})')
    else:
        ok = False
        say(f'  FAIL  python {py[0]}.{py[1]}: need {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+; install a newer python3 and rerun with it')
    facts['python'] = sys.executable
    if hasattr(os, 'geteuid') and os.geteuid() == 0:
        ok = False
        say('  FAIL  running as root: run ./install.sh as the user who runs OpenClaw (the service runs as that user)')

    node = resolve_tool(shutil.which('node'))
    node_version = version_tuple(run([node, '--version']).stdout) if node else None
    if node and supported_node(node_version):
        say(f'  ok    node {".".join(map(str, node_version))} ({node})')
        if not supported_node(node_version, OPENCLAW_NODE_FLOORS):
            say(f'  note  OpenClaw {required_openclaw()} needs Node.js {OPENCLAW_NODE_REQUIREMENT}: update Node.js before you update OpenClaw')
    else:
        ok = False
        say(f'  FAIL  need Node.js {NODE_REQUIREMENT}; install a supported version and rerun'
            + ('' if not MACOS else ' (Homebrew: brew install node@24, then put it on your PATH as brew says)'))
    facts['node'] = node

    openclaw = resolve_tool(shutil.which('openclaw'))
    want = required_openclaw()
    if openclaw:
        got = run([openclaw, '--version']).stdout
        have = '.'.join(map(str, version_tuple(got) or ())) or 'unknown'
        note = '' if have == want else f' (tested with {want}; the Telegram Change prompt falls back to a plain prompt on other versions)'
        say(f'  ok    openclaw {have}{note}')
        if version_tuple(got) and version_tuple(got) < version_tuple(want):
            say(f'  note  to update: openclaw backup create --verify, then openclaw update --tag {want}. It migrates'
                ' OpenClaw\'s data and restarts its Gateway; after a plain npm install, run openclaw doctor --fix before the restart')
        facts['openclaw_version'] = have
    else:
        ok = False
        say(f'  FAIL  openclaw CLI not found: install OpenClaw {want} (npm install -g openclaw@{want}) and set up its Telegram channel,'
            ' or run ./install.sh in a terminal and it offers to do that with you')
    facts['openclaw'] = openclaw
    facts['openclaw_package_dir'] = openclaw_package_dir(openclaw, node)
    if openclaw and not facts['openclaw_package_dir']:
        ok = False
        say('  FAIL  cannot locate the OpenClaw npm package; expose its installed CLI on PATH and rerun')

    manager = {'systemd': 'systemctl', 'launchd': 'launchctl'}.get(service.manager(), 'systemctl')
    for name, hint in (('gog', 'Gmail and Calendar sources: install gog (gogcli' + (', brew install gogcli' if MACOS else '')
                        + '); signing in comes later in this setup'),
                       ('tailscale', 'dashboard access: install Tailscale and join your tailnet'),
                       ('caddy', 'only needed to serve the dashboard on a custom domain (see deploy/Caddyfile)'),
                       ('wacli', 'only needed for the WhatsApp source'),
                       (manager, 'needed to run the service; without it start `python3 assistant.py serve` yourself')):
        found = onboarding.portable.tailscale() if name == 'tailscale' else shutil.which(name)
        facts[name] = found
        say(f'  {"ok   " if found else "skip "} {name}{"" if found else ": " + hint}')
    facts['service'] = service.available()
    fresh = not Paths().config.exists()
    if fresh and not facts['tailscale'] and not (os.environ.get(ENV['tailscale_owner']) and os.environ.get(ENV['dashboard_host'])):
        ok = False
        say('  FAIL  tailscale: the dashboard only opens for your Tailscale login. Install Tailscale on this machine and your phone\n'
            '        (https://tailscale.com/download), run `sudo tailscale up`, then rerun ./install.sh')
    elif fresh and facts['tailscale'] and not tailscale_identity(facts['tailscale']).get('dashboard_host'):
        say('  note  tailscale is installed but not logged in; run `sudo tailscale up` first, or type your login and host below')
    return ok, facts


# ---------------------------------------------------------------- OpenClaw itself

def writable(path):
    path = Path(path)
    while not path.exists() and path != path.parent:
        path = path.parent
    return os.access(path, os.W_OK)


def npm_beside(node):
    """npm from the same Node install as `node`, else the one on PATH."""
    beside = Path(node).parent / 'npm' if node else None
    return str(beside) if beside and beside.exists() else shutil.which('npm')


def openclaw_install_command(npm, want, home=None):
    """npm install -g openclaw@<want>, into ~/.local when npm's global folder isn't yours: never sudo."""
    command = [npm, 'install', '-g', f'openclaw@{want}']
    prefix = run([npm, 'prefix', '-g']).stdout.strip()
    if not prefix or not writable(Path(prefix) / 'lib/node_modules'):
        command += ['--prefix', str(Path(home or Path.home()) / '.local')]
    return command


def installed_openclaw(npm, command):
    """The openclaw CLI npm just installed, put on this run's PATH when it isn't there yet."""
    if '--prefix' in command:
        prefix = command[command.index('--prefix') + 1]
    else:
        prefix = run([npm, 'prefix', '-g']).stdout.strip()
    if shutil.which('mise') and '/mise/' in str(npm):
        run(['mise', 'reshim'], timeout=60)  # mise puts new global npm binaries on PATH through its shims
    found = shutil.which('openclaw')
    if found:
        return found
    binary = Path(prefix) / 'bin/openclaw'
    if not binary.exists():
        return None
    os.environ['PATH'] = f'{binary.parent}{os.pathsep}{os.environ.get("PATH", "")}'
    say(f'  note  {binary.parent} is not on your PATH; add it in your shell profile so `openclaw` works in new terminals')
    return str(binary)


def has_telegram(settings):
    """OpenClaw's config has a Telegram channel (a bot token, a token file or accounts), whatever its shape."""
    channel = (settings.get('channels') or {}).get('telegram')
    return isinstance(channel, dict) and bool(channel) and channel.get('enabled') is not False


ALLOW_SCRIPTS = re.compile(r'--allow-scripts=([\w@./,-]+)')


def allow_install_scripts(npm, command, output, ui):
    """npm 11+ skips package install scripts unless they're allowed, and says which ones it skipped. OpenClaw
    needs them (its own setup and native parts such as koffi), so the install runs again with exactly those allowed,
    as npm's own message says. (`npm rebuild -g` instead can stop on the files the install just put down.)"""
    skipped = ALLOW_SCRIPTS.search(output)
    if not skipped:
        return subprocess.CompletedProcess(command, 0, '', '')
    ui.say(f'  Running the install steps npm held back: {skipped.group(1).replace(",", ", ")}')
    result = run([*command, f'--allow-scripts={skipped.group(1)}'], timeout=1800)
    if result.returncode != 0:
        ui.say(((result.stderr or '') + (result.stdout or '')).strip()[-1500:])
    return result


def offer_openclaw(ui):
    """In a terminal, before the prerequisite check: without OpenClaw, offer to install it; when it was never
    set up, or has no Telegram bot, walk through OpenClaw's own setup with what The Machine needs from it.
    Every step asks first and can be answered no; the prerequisite check after it says what is still missing."""
    openclaw = resolve_tool(shutil.which('openclaw'))
    want = required_openclaw()
    acted = False
    if not openclaw:
        node = resolve_tool(shutil.which('node'))
        npm = npm_beside(node)
        if not (node and supported_node(version_tuple(run([node, '--version']).stdout), OPENCLAW_NODE_FLOORS) and npm):
            ui.say(f'\nThe Machine runs on OpenClaw, which is not installed here. It needs Node.js {OPENCLAW_NODE_REQUIREMENT} with npm first:\n'
                   '  install it from https://nodejs.org or with a version manager (mise use -g node@24), then rerun ./install.sh')
            return
        command = openclaw_install_command(npm, want)
        ui.say('\nThe Machine runs on OpenClaw: your own agent, with your model, talking to you through its dashboard app and, if you like, a Telegram bot.'
               ' It is not installed here.')
        if not ui.yes(f'Install OpenClaw {want} now? (runs: npm {" ".join(command[1:])})', True):
            return
        try:  # the registry must name the checksum pinned in openclaw-pin.json; npm checks the download against it
            openclaw_pin.check(want)
        except Exception as error:
            ui.say(f'  ✗ OpenClaw {want} was not installed: {error}. Nothing changed; try again later or report it.')
            return
        ui.say('  Installing (a few minutes)...')
        result = run(command, timeout=1800)
        if result.returncode == 0:
            result = allow_install_scripts(npm, command, (result.stdout or '') + (result.stderr or ''), ui)
        else:
            ui.say(((result.stderr or '') + (result.stdout or '')).strip()[-1500:])
        openclaw = installed_openclaw(npm, command) if result.returncode == 0 else None
        if not openclaw:
            ui.say(f'  ✗ OpenClaw did not install. Run it yourself and rerun ./install.sh:\n    npm {" ".join(command[1:])}')
            return
        ui.say(f'  ✓ OpenClaw {want} installed')
        acted = True
    settings = onboarding.openclaw_settings()
    if not settings:
        ui.say('\nOpenClaw is not set up yet. Its own guided setup comes next; this is what The Machine needs from it:\n'
               '  1. Model: pick the provider you use and sign in or paste its key. Checks and Do it run on it.\n'
               '  2. Gateway: say yes to running it as a service, so it keeps running in the background.\n'
               '  3. Channels (optional): choose Telegram to get to-dos there too. Make a bot first: in Telegram, message\n'
               '     @BotFather, send /newbot, pick a name and a free username ending in "bot", and paste the token. Skip it to use the dashboard app\'s notifications.\n'
               '  The rest is up to you. When it finishes, you come back here.')
        if ui.yes('Start OpenClaw\'s setup now?', True):
            run([openclaw, 'onboard', '--install-daemon'], timeout=None, capture_output=False)
            settings = onboarding.openclaw_settings()
            acted = True
        if not settings:
            ui.say('  OpenClaw is still not set up; run `openclaw onboard --install-daemon`, then rerun ./install.sh')
            return
    if not has_telegram(settings):
        ui.say('\nOpenClaw has no Telegram bot. That is optional: to-dos also reach you through the dashboard app\n'
               '(add it to your phone\'s home screen, turn on notifications). For Telegram too: in Telegram, message\n'
               '@BotFather, send /newbot, pick a name and a free username ending in "bot", and copy the token it gives you.')
        if ui.yes('Connect a Telegram bot to OpenClaw now? (runs: openclaw channels add --channel telegram)', False):
            run([openclaw, 'channels', 'add', '--channel', 'telegram'], timeout=None, capture_output=False)
            acted = True
        if not has_telegram(onboarding.openclaw_settings()):
            ui.say('  No Telegram bot yet; add one later with `openclaw channels add --channel telegram`.')
    if acted and run([openclaw, 'health'], timeout=60).returncode != 0:
        ui.say('  note  the OpenClaw Gateway is not answering yet; `openclaw doctor --fix` says why (checks and to-dos need it)')


# ---------------------------------------------------------------- config

def tailscale_identity(binary):
    if not binary:
        return {}
    result = run([binary, 'status', '--json'], timeout=10)
    try:
        status = json.loads(result.stdout)
        user = status['User'][str(status['Self']['UserID'])]['LoginName']
        # A tagged machine has no owner login of its own: the dashboard owner is whoever you sign in as on your phone.
        return {'tailscale_owner': '' if user == 'tagged-devices' or '@' not in user else user,
                'dashboard_host': dashboard_address(status['Self']['DNSName'].rstrip('.'))}
    except (ValueError, KeyError, TypeError):
        return {}


def dashboard_address(host):
    """A tailnet name gets the dashboard's own port (:8443): its own origin, so the phone app installs
    cleanly next to OpenClaw's web app on :443. Your own domain is kept as typed."""
    host = host.strip().removeprefix('https://').rstrip('/')
    return f'{host}:8443' if host.endswith('.ts.net') and ':' not in host else host


def ask(prompt, default=''):
    answer = input(f'{prompt}{f" [{default}]" if default else ""}: ').strip()
    return answer or default


def ask_until(prompt, default, valid, problem):
    """Ask again until the answer passes `valid`; Enter keeps a valid default."""
    while True:
        answer = ask(prompt, default)
        if valid(answer):
            return answer
        say(f'  {problem(answer)}')


def valid_timezone(name):
    try:
        ZoneInfo(name)
        return True
    except (ValueError, KeyError, OSError):
        return False


def answers(interactive, facts):
    # Smart defaults from this machine: Tailscale identity, the Telegram ID OpenClaw already trusts,
    # Google accounts gog knows, and sources that are installed or linked here.
    detected = tailscale_identity(facts.get('tailscale'))
    owners = onboarding.telegram_owners()
    google = onboarding.gog_accounts(facts.get('gog'))
    defaults = {'owner_name': onboarding.owner_name(), 'telegram_owner': owners[0] if owners else '',
                'tailscale_owner': detected.get('tailscale_owner', ''),
                'dashboard_host': detected.get('dashboard_host', ''), 'timezone': local_timezone(), 'locale': '',
                'connectors': onboarding.suggested_sources(facts), 'email': google[0][0] if google else '',
                'gog_client': google[0][1] if google else 'default', 'boundary': '',
                'android_node_id': '', 'whatsapp_store': str(Path.home() / '.local/share/wacli')}
    values = {key: os.environ.get(var) or defaults[key] for key, var in ENV.items()}
    unknown = lambda text: sorted(set(split(text)) - set(CONNECTORS) - {'none'})
    if interactive:
        say('\nA few questions (Enter keeps the default):')
        values['owner_name'] = ask('Your name (used to sign emails)', values['owner_name'])
        if not values['telegram_owner'] and facts.get('openclaw'):
            if not OPENCLAW_TURN.acquire(blocking=False):  # it approves a pairing: not while the steps ahead call OpenClaw
                say('One moment: OpenClaw is busy with the install.')
                OPENCLAW_TURN.acquire()
            try:
                values['telegram_owner'] = onboarding.telegram_from_pairing(facts['openclaw'], onboarding.UI()) or ''
            finally:
                OPENCLAW_TURN.release()
        values['telegram_owner'] = ask_until('Your Telegram user ID (the private chat with your OpenClaw bot'
                                             + (', found in OpenClaw)' if values['telegram_owner'] else
                                                '; your bot\'s pairing reply shows it. Optional: Enter skips Telegram,'
                                                ' then to-dos reach you through the dashboard app)'), values['telegram_owner'],
                                             lambda a: telegram_off(a) or onboarding.telegram_id(a),
                                             lambda a: f'{a!r} is not a Telegram user ID: that is a number like 123456789')
        values['telegram_owner'] = onboarding.telegram_id(values['telegram_owner']) or ''
        values['tailscale_owner'] = ask_until('Your Tailscale login, as on your phone (only it may open the dashboard)'
                                              + ('' if values['tailscale_owner'] else '; this machine is tagged or not logged in, so type it'),
                                              values['tailscale_owner'], lambda a: bool(a.strip()), lambda a: 'needed for the dashboard')
        values['dashboard_host'] = ask_until('Dashboard address (your machine on the tailnet, e.g. machine.tailnet.ts.net:8443)', values['dashboard_host'],
                                             lambda a: bool(re.fullmatch(r'[A-Za-z0-9.-]+\.[A-Za-z]{2,}(:\d{2,5})?', dashboard_address(a))),
                                             lambda a: 'a host name, like machine.tailnet.ts.net:8443 (no path)')
        values['timezone'] = ask_until('Time zone', values['timezone'], valid_timezone,
                                       lambda a: f'unknown time zone {a!r}; use a name like Europe/Brussels or America/New_York')
        values['connectors'] = ask_until('Sources to enable (' + ','.join(CONNECTORS) + '; you connect each one next)',
                                         values['connectors'], lambda a: not unknown(a),
                                         lambda a: 'unknown: ' + ', '.join(unknown(a)) + '; other sources (github, x, ...) come later with assistant connect')
        chosen = set(split(values['connectors']))
        if chosen & {'gmail', 'calendar', 'slack', 'crm'}:
            values['email'] = ask_until('Your email address for these sources', values['email'], lambda a: '@' in a,
                                        lambda a: 'an email address, like you@company.com')
            guess = values['boundary'] or onboarding.company_of(values['email']) or ('personal' if values['email'] else '')
            values['boundary'] = ask('Company name for these sources, or "personal" (keeps work and private apart)', guess)
    values['boundary'] = onboarding.boundary_label(values['boundary'] or onboarding.company_of(values['email']))
    values['dashboard_host'] = dashboard_address(values['dashboard_host'])
    # Telegram is optional: without it, cards reach the owner through the installed dashboard app.
    values['telegram_owner'] = '' if telegram_off(values['telegram_owner']) else onboarding.telegram_id(values['telegram_owner']) or values['telegram_owner']
    missing = [key for key in ('tailscale_owner', 'dashboard_host') if not values[key]]
    if missing:
        raise SystemExit('Missing answers: ' + ', '.join(missing) + ' (set ' + ', '.join(ENV[k] for k in missing) + ')')
    if not values['telegram_owner']:
        say('No Telegram: to-dos reach you through the dashboard app (add it to your home screen, turn on notifications).'
            ' Add Telegram later with assistant telegram on <your Telegram user ID>.')
    elif not re.fullmatch(r'-?\d{3,20}', values['telegram_owner']):
        raise SystemExit('The Telegram owner must be a numeric chat ID, got ' + repr(values['telegram_owner']))
    if unknown(values['connectors']):
        raise SystemExit('Unknown sources: ' + ', '.join(unknown(values['connectors'])))
    if not valid_timezone(values['timezone']):
        raise SystemExit('Unknown time zone ' + repr(values['timezone']) + ' (set ASSISTANT_TIMEZONE, e.g. Europe/Brussels)')
    return values


def telegram_off(answer):
    return str(answer or '').strip().lower() in ('', 'none', 'off', 'no')


def split(text):
    return [part.strip() for part in (text or '').split(',') if part.strip()]


def local_timezone():
    link = Path('/etc/localtime')
    try:
        target = str(link.resolve())
        return target.split('zoneinfo/', 1)[1] if 'zoneinfo/' in target else 'UTC'
    except OSError:
        return 'UTC'


def new_config(values, facts, paths):
    """config.json from config.example.json plus the wizard's answers."""
    example = json.loads((ROOT / 'config.example.json').read_text())
    templates = {a['id']: a for a in example.pop('accounts')}
    config = expand(example, paths.home)
    config.update(owner_name=values['owner_name'], timezone=values['timezone'], telegram_owner=values['telegram_owner'],
                  tailscale_owner=values['tailscale_owner'], dashboard_host=values['dashboard_host'], heartbeat_job_id='',
                  booking_links={})
    if locale_prefs.normalize(values.get('locale')):
        config['locale'] = locale_prefs.normalize(values['locale'])  # else US dates and 24-hour times until Settings
    bot = onboarding.telegram_account(values['telegram_owner'])
    if bot != 'default':
        config['telegram_account'] = bot  # the OpenClaw Telegram account (bot) you talk to
    config['delivery_enabled'] = False
    config['review_worker']['enabled'] = False
    data = str(paths.data)
    config['database'] = data + '/events.sqlite'
    config['prompt_receipts'] = data + '/prompt-receipts'
    config['attachment_dir'] = data + '/attachments'
    config['credentials'] = {'api-token': data + '/api-token', 'owner-token': data + '/owner-token'}
    config['attachment_sources'] = [str(paths.workspace / 'data/assistant-attachments'), str(paths.workspace / 'memory/assistant')]
    accounts = []
    for name in split(values['connectors']):
        if name == 'none':
            continue
        if name == 'gateway' and not onboarding.gateway_unit():
            say('  skipped the Gateway log source: the OpenClaw Gateway does not run as a systemd user unit here')
            continue
        account = expand(dict(templates[CONNECTORS[name]]), paths.home)
        if 'email' in account:
            account['email'] = values['email'] or account['email']
            if 'owner_emails' in account:
                account['owner_emails'] = [account['email']]
        if account.get('transport') == 'gog':
            account['client'] = values['gog_client']
            config['credentials']['gog-password'] = data + '/gog-password'
        if account.get('boundary', '').startswith('work:'):
            account['boundary'] = values['boundary']
            if values['boundary'].startswith('personal:'):
                account['id'] = account['id'].replace('work-', 'personal-', 1)
        account.pop('exclude', None)  # example noise rules are not yours
        if name == 'android':
            account['node_id'] = values['android_node_id'] or account['node_id']
        if name == 'whatsapp':
            account['store'] = values['whatsapp_store']
        if name == 'gateway':
            account['unit'] = onboarding.gateway_unit()
        if account.get('credential'):
            config['credentials'][account['credential']] = f"{data}/{account['credential']}.env"
        accounts.append(account)
    config['accounts'] = accounts
    return config


def refresh_install_paths(config, facts, paths):
    """Keys that describe this checkout and toolchain; safe to update on every run."""
    config['app_dir'] = str(ROOT)
    for key in ('openclaw', 'node'):
        if facts.get(key):
            config[key] = facts[key]
    if facts.get('openclaw_package_dir'):
        config['openclaw_package_dir'] = str(facts['openclaw_package_dir'])
    if facts.get('gog') and config.get('gog') in (None, 'gog'):
        config['gog'] = facts['gog']
    if facts.get('wacli') and config.get('wacli') in (None, 'wacli'):
        config['wacli'] = facts['wacli']
    return config


def setup_config(interactive, facts, paths):
    if paths.config.exists():
        config = json.loads(paths.config.read_text())
        example = expand(json.loads((ROOT / 'config.example.json').read_text()), paths.home)
        example.pop('accounts')
        # The example's identity (owner, Telegram, Tailscale, host) is not yours; its time zone is this machine's.
        added = [key for key in example if key not in config and key not in
                 ('booking_links', 'heartbeat_job_id', 'owner_name', 'telegram_owner', 'tailscale_owner', 'dashboard_host')]
        for key in added:
            config[key] = local_timezone() if key == 'timezone' else example[key]
        bot = onboarding.telegram_account(config.get('telegram_owner', ''))
        if 'telegram_account' not in config and bot != 'default':
            config['telegram_account'] = bot
            added.append(f'telegram_account {bot}')
        say(f'Keeping existing {paths.config}' + (f' (added defaults: {", ".join(added)})' if added else ''))
    else:
        config = new_config(answers(interactive, facts), facts, paths)
        say(f'Writing {paths.config}')
    refresh_install_paths(config, facts, paths)
    # Built-in sources plus connector plugins (connectors/<service>.py, see docs/adding-a-source.md).
    supported = {'gmail', 'calendar', 'outlook', 'outlook_calendar', 'imap', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange', 'slack', 'salesflare', 'android', 'whatsapp', 'telegram', 'signal', 'gateway'} | {
        p.stem for p in (ROOT / 'connectors').glob('*.py') if re.fullmatch(r'[a-z][a-z0-9_]{0,30}', p.stem)}
    unsupported = [a['id'] for a in config.get('accounts', []) if a.get('service', 'gmail') not in supported]
    if unsupported:
        raise SystemExit('Unsupported sources in existing config: ' + ', '.join(unsupported)
                         + '. Remove those accounts and unused credentials from config.json; database history is kept.')
    text = json.dumps(config, indent=2) + '\n'
    if not paths.config.exists() or paths.config.read_text() != text:
        write_private(paths.config, text)
    os.chmod(paths.config, 0o600)
    return config


# ---------------------------------------------------------------- secrets

def setup_secrets(config, facts, paths):
    paths.data.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(paths.data, 0o700)
    created = []
    for name in ('api-token', 'owner-token'):
        path = Path(config['credentials'].get(name) or paths.data / name)
        if not path.exists():
            write_private(path, secrets.token_hex(32))
            created.append(name)
        os.chmod(path, 0o600)
    vapid = Path(config['database']).parent / 'vapid.json'
    if not vapid.exists() and facts.get('node'):
        env = dict(os.environ, PUSH_VAPID_FILE=str(vapid))
        result = run([facts['node'], str(ROOT / 'push-send.mjs')], input='{"action":"key"}', env=env, timeout=30)
        if result.returncode == 0 and vapid.exists():
            created.append('vapid.json')
        else:
            say('  note: could not create the Web Push key now; the service creates it on first use')
    if vapid.exists():
        os.chmod(vapid, 0o600)
    say('Secrets: ' + (('created ' + ', '.join(created)) if created else 'already present, unchanged') + f' in {paths.data} (mode 600)')


# ---------------------------------------------------------------- systemd, CLI, plugin

def quote_unit(path):
    """A path for a systemd command line: quoted when it has spaces."""
    text = str(path)
    return f'"{text}"' if re.search(r'\s', text) else text


def unit_path(facts):
    bins = [str(Path(p).parent) for p in (facts.get('node'), facts.get('openclaw'), facts.get('gog'), facts.get('wacli')) if p]
    return ':'.join(dict.fromkeys(bins + ['%h/.local/bin', '/usr/local/bin', '/usr/bin', '/bin']))


def unit_text(config, facts, config_path=None):
    path = unit_path(facts)
    return f"""# Written by install.sh from {ROOT}; rerun ./install.sh to update it.
[Unit]
Description=The Machine: signal collector and suggestions inbox
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=10

[Service]
Type=simple
WorkingDirectory={ROOT}
ExecStart={quote_unit(facts.get('python') or sys.executable)} {quote_unit(ROOT / 'assistant.py')} serve
Restart=always
RestartSec=10
TimeoutStopSec=20
KillMode=control-group
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
Environment="PATH={path}"
Environment=PYTHONUNBUFFERED=1
Environment="ASSISTANT_CONFIG={str(config_path or Paths().config)}"
Environment="OPENCLAW_WORKSPACE={Paths().workspace}"

[Install]
WantedBy=default.target
"""


def service_path(facts):
    bins = [str(Path(p).parent) for p in (facts.get('node'), facts.get('openclaw'), facts.get('gog'), facts.get('wacli')) if p]
    home = str(Paths().home)
    return ':'.join(dict.fromkeys(bins + [home + '/.local/bin', '/opt/homebrew/bin', '/usr/local/bin', '/usr/bin', '/bin',
                                          '/usr/sbin', '/sbin']))


def agent_text(config, facts, config_path=None, paths=None):
    """The launchd agent for macOS: the same program, environment and restart policy as the systemd unit."""
    paths = paths or Paths()
    return service.plist_text([facts.get('python') or sys.executable, str(ROOT / 'assistant.py'), 'serve'], workdir=ROOT,
                              env={'PATH': service_path(facts), 'PYTHONUNBUFFERED': '1', 'HOME': str(paths.home),
                                   'ASSISTANT_CONFIG': str(config_path or paths.config), 'OPENCLAW_WORKSPACE': str(paths.workspace)},
                              base=paths.home)


def install_unit(config, facts, paths, start):
    launchd = service.manager() == 'launchd'
    text = agent_text(config, facts, paths.config, paths) if launchd else unit_text(config, facts, paths.config)
    changed = not paths.unit.exists() or paths.unit.read_text() != text
    if changed:
        paths.unit.parent.mkdir(parents=True, exist_ok=True)
        paths.unit.write_text(text)
    say(f'{"launchd agent" if launchd else "systemd unit"}: {"written" if changed else "unchanged"} {paths.unit}')
    if not facts.get('service', facts.get('systemctl')):
        say(f'  {"launchctl" if launchd else "systemctl"} not found: start the service with `python3 assistant.py serve`')
        return None if not start else False
    if launchd:
        if not start:
            say('  not started (--no-start)')
            return None
        result = service.enable(UNIT_NAME, run=run)
        if result.returncode != 0:
            say('  could not start it: ' + (result.stderr or result.stdout).strip()[:300])
            return False
        say(f'  loaded and started; it starts at login. Log: {service.log_path()}')
        return True
    reload = run(['systemctl', '--user', 'daemon-reload'])
    if reload.returncode != 0:
        error = (reload.stderr or reload.stdout).strip()
        say('  daemon-reload failed: ' + error[:300])
        if re.search(r'bus|XDG_RUNTIME_DIR', error, re.I):
            say('  There is no systemd user session here (sudo su, a container, or SSH without one). Log in as this user\n'
                '  directly (or: sudo loginctl enable-linger $USER, then log in again) and rerun, or install with\n'
                '  --no-start and run `python3 assistant.py serve` yourself.')
        return False
    if not start:
        say('  not started (--no-start)')
        return None
    result = run(['systemctl', '--user', 'enable', UNIT_NAME])
    result = run(['systemctl', '--user', 'restart', UNIT_NAME]) if result.returncode == 0 else result
    if result.returncode != 0:
        say('  could not start it: ' + (result.stderr or result.stdout).strip()[:300])
        return False
    say('  enabled and (re)started')
    linger = run(['loginctl', 'show-user', os.environ.get('USER') or str(os.getuid()), '-p', 'Linger', '--value'], timeout=10)
    if linger.returncode == 0 and linger.stdout.strip() == 'no':
        say('  note: it stops when you log out. To keep it (and the Gateway) running: sudo loginctl enable-linger $USER')
    return True


UPDATE_UNIT = 'the-machine-update.service'
UPDATE_TIMER = 'the-machine-update.timer'
HOSTED_AGENT = Path('/var/lib/machine-agent')  # hosted Machines: their agent installs releases instead


def to_signed_release():
    """A first install from git moves the checkout to the newest signed release before any of it runs (scripts/
    release.py first_install): True when it moved (the installer then starts again from the release), None when there
    is nothing to do, False when no release verifies (nothing installed). --from-main installs the checkout as it is."""
    if not (ROOT / '.git').exists() or HOSTED_AGENT.exists():
        return None  # not a clone, or hosted: its agent installs the release
    sys.path.insert(0, str(ROOT / 'scripts'))
    import release
    try:
        moved = release.first_install()
    except (release.Refused, SystemExit) as error:
        say(f'Unsigned install refused: {error}. Nothing was installed. To install this checkout as it is, rerun with '
            '--from-main.')
        return False
    if moved:
        say(f'Signed release: {moved[0]} ({moved[1][:7]}), signature verified')
    return bool(moved) or None


def update_texts(config, facts, paths):
    """The daily signed update of a self-hosted install: the newest signed release, only when nothing runs."""
    service_text = f"""# Written by install.sh from {ROOT}; rerun ./install.sh to update it.
[Unit]
Description=The Machine: install the newest signed release
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory={ROOT}
ExecStart={quote_unit(facts.get('python') or sys.executable)} {quote_unit(ROOT / 'scripts' / 'release.py')} update --install
TimeoutStartSec=1h
Environment="PATH={unit_path(facts)}"
Environment=PYTHONUNBUFFERED=1
Environment="ASSISTANT_CONFIG={paths.config}"
Environment="OPENCLAW_WORKSPACE={paths.workspace}"
"""
    timer_text = f"""# Written by install.sh from {ROOT}; rerun ./install.sh to update it.
[Unit]
Description=The Machine: daily signed update

[Timer]
OnCalendar=*-*-* 04:00
RandomizedDelaySec=2h
Persistent=true

[Install]
WantedBy=timers.target
"""
    return service_text, timer_text


def install_updates(config, facts, paths, start):
    """Self-hosted Linux installs from git: a daily timer that installs signed releases only (scripts/release.py
    update --install). Off with "auto_update": false; hosted Machines and other installs get none."""
    unit_dir = paths.unit.parent
    wanted = (service.manager() == 'systemd' and facts.get('systemctl') and (ROOT / '.git').exists()
              and not HOSTED_AGENT.exists() and config.get('auto_update', True) is not False)
    files = [unit_dir / UPDATE_UNIT, unit_dir / UPDATE_TIMER]
    if not wanted:
        if any(f.exists() for f in files):
            if facts.get('systemctl'):
                run(['systemctl', '--user', 'disable', '--now', UPDATE_TIMER])
            for f in files:
                f.unlink(missing_ok=True)
            say('Daily update: turned off')
        return None
    for f, text in zip(files, update_texts(config, facts, paths)):
        if not f.exists() or f.read_text() != text:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text)
    if not start:
        say('Daily update: written, not turned on (--no-start)')
        return None
    run(['systemctl', '--user', 'daemon-reload'])
    result = run(['systemctl', '--user', 'enable', '--now', UPDATE_TIMER])
    say('Daily update: ' + ('signed releases only, every night' if result.returncode == 0
                            else 'could not turn on: ' + (result.stderr or result.stdout).strip()[:300]))
    return result.returncode == 0


def install_cli(paths):
    target = ROOT / 'cli.py'
    paths.cli.parent.mkdir(parents=True, exist_ok=True)
    if paths.cli.is_symlink() and paths.cli.resolve() == target:
        warn_path(paths)
        return
    if paths.cli.exists() and not paths.cli.is_symlink():
        raise SystemExit(f'CLI install failed: {paths.cli} is an existing file; move it aside and rerun')
    if paths.cli.is_symlink():
        paths.cli.unlink()
    paths.cli.symlink_to(target)
    os.chmod(target, 0o755)
    say(f'CLI: {paths.cli} -> cli.py')
    warn_path(paths)


def node_packages_current(root=ROOT):
    """Every package in package-lock.json is installed at its locked version."""
    try:
        packages = json.loads((root / 'package-lock.json').read_text())['packages']
        return all(json.loads((root / path / 'package.json').read_text()).get('version') == entry.get('version')
                   for path, entry in packages.items() if path)
    except (OSError, ValueError, KeyError, AttributeError):
        return False


def install_node_packages(node, root=ROOT):
    """The pinned Node packages beside the app (package-lock.json: the Gateway's official client for card chat).
    npm ci only when they don't match the lock, with no install scripts. Not fatal: without them only the card
    chat view is unavailable."""
    if not (root / 'package-lock.json').exists() or node_packages_current(root):
        return True
    npm = npm_beside(node)
    result = run([npm, 'ci', '--omit=dev', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=str(root)) if npm else None
    if not result or result.returncode or not node_packages_current(root):
        say('  warn  could not install the Node packages (npm ci); to-do chat stays unavailable until the next install')
        return False
    say('Node packages: installed (package-lock.json)')
    return True


def precompile(facts):
    """The app's bytecode, so the service's first start reads it instead of compiling every module (about 6 of its
    9 seconds on a busy machine). Not fatal: the service compiles what is missing itself."""
    python = facts.get('python') or sys.executable
    result = run([python, '-m', 'compileall', '-q', '-j', '0', '-x', r'/(tests|node_modules|\.git)/', str(ROOT)], timeout=300)
    return result.returncode == 0


def prepare(facts, paths, fresh, start, skip_plugin, bytecode=False):
    """The install steps that need no answers: on a first install in a terminal they run while the questions are asked
    (Ahead), with the bytecode too, which is free there. False when the bridge could not go into OpenClaw (the install
    then stops, as before)."""
    paths.data.mkdir(mode=0o700, parents=True, exist_ok=True)  # its stamps go here; setup_secrets keeps it 700
    if bytecode:
        precompile(facts)
    install_node_packages(facts['node'])
    # The bridge reads config.json when it needs it; before the answers, the credentials it guards are all in paths.data
    if not (skip_plugin or install_plugin(facts, reload=start, stamp=paths.data / 'plugin-installed', restart=may_restart_gateway(paths))):
        return False
    quiet_openclaw(facts, paths.data / 'openclaw-quiet.json')
    gateway_keep_retrying(paths)
    memory_rules(paths.workspace, paths.data / 'memory-rules.json')
    if fresh:
        start_thinking(facts)
    return True


class Ahead(threading.Thread):
    """prepare() in the background while the questions are asked; result() waits for it and says its lines."""

    def __init__(self, step, *args):
        super().__init__(name='install-ahead')
        self.step, self.args, self.lines, self.ok, self.error = step, args, [], False, None
        self.start()

    def run(self):
        _ahead.lines = self.lines
        try:
            self.ok = self.step(*self.args)
        except BaseException as error:  # raised again in result(), where the install would have raised it
            self.error = error

    def result(self):
        if self.is_alive():
            print('Finishing the OpenClaw steps...', flush=True)
        self.join()
        for line in self.lines:
            say(line)
        if self.error:
            raise self.error
        return self.ok


def warn_path(paths):
    folders = [Path(p).expanduser() for p in os.environ.get('PATH', '').split(os.pathsep) if p]
    if paths.cli.parent not in folders:
        say(f'  note: {paths.cli.parent} is not on your PATH, so `assistant` is not found yet. Use {paths.cli},\n'
            f'  or add it: echo \'export PATH="$HOME/.local/bin:$PATH"\' >> ~/.profile (then open a new terminal)')


def plugin_fingerprint(facts):
    """What the bridge in OpenClaw is made of: its files, where they are and the OpenClaw that runs them."""
    digest = hashlib.sha256()
    root = ROOT / 'openclaw-plugin'
    for path in sorted(p for p in root.rglob('*') if p.is_file() and 'node_modules' not in p.parts):
        digest.update(str(path.relative_to(root)).encode() + b'\0' + path.read_bytes() + b'\0')
    digest.update(f"{root}\0{facts.get('openclaw')}\0{facts.get('openclaw_version')}".encode())
    return digest.hexdigest()


def bridge_parts(facts):
    """The same, part by part, so a later run can tell what changed: only the OpenClaw around a bridge whose files
    and folder stayed the same needs no swap (bridge_in_openclaw)."""
    digest = hashlib.sha256()
    root = ROOT / 'openclaw-plugin'
    for path in sorted(p for p in root.rglob('*') if p.is_file() and 'node_modules' not in p.parts):
        digest.update(str(path.relative_to(root)).encode() + b'\0' + path.read_bytes() + b'\0')
    return {'files': digest.hexdigest(), 'root': str(root), 'openclaw': str(facts.get('openclaw')), 'version': str(facts.get('openclaw_version'))}


def read_stamp(stamp):
    """(the fingerprint, its parts) the last finished swap left; parts None in a stamp from before they were kept."""
    try:
        lines = stamp.read_text().splitlines()
    except (OSError, ValueError):
        return None, None
    try:
        parts = json.loads(lines[1]) if len(lines) > 1 else None
    except ValueError:
        parts = None
    return (lines[0].strip() if lines else None), (parts if isinstance(parts, dict) else None)


def write_stamp(stamp, facts):
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(plugin_fingerprint(facts) + '\n' + json.dumps(bridge_parts(facts), sort_keys=True) + '\n')
    stamp.with_name(BRIDGE_WAITING).unlink(missing_ok=True)


def bridge_in_openclaw(openclaw):
    """Whether OpenClaw already has this bridge: its install record is a link to this folder, it is enabled, loads
    from here, may run its conversation hooks, and the running Gateway lists it as loaded. Anything less, or anything
    that cannot be read, is False: the bridge then goes in the usual way."""
    result = run([openclaw, 'plugins', 'inspect', PLUGIN_ID, '--json'], timeout=120)
    try:
        found = json.loads(result.stdout or '') if result.returncode == 0 else None
    except ValueError:
        found = None
    plugin, install = ((found.get('plugin'), found.get('install')) if isinstance(found, dict) else (None, None))
    if not (isinstance(plugin, dict) and isinstance(install, dict)):
        return False
    root = (ROOT / 'openclaw-plugin').resolve()
    def here(value):
        try:
            return isinstance(value, str) and bool(value) and Path(value).resolve() == root
        except (OSError, ValueError, RuntimeError):
            return False
    if not (install.get('source') == 'path' and here(install.get('sourcePath')) and here(plugin.get('rootDir'))
            and plugin.get('enabled') is True and plugin.get('status') == 'loaded'):
        return False
    if not onboarding.hooks_allowed(onboarding.openclaw_settings()):
        return False
    live = gateway_health(openclaw)
    return PLUGIN_ID in (((live or {}).get('plugins') or {}).get('loaded') or [])


def bridge_changed_at():
    """The last time anything in the bridge's folder changed on disk: its newest change time (ctime, which a checkout
    or an unpacked archive always sets to now, unlike the modified time an archive can carry over). The folders count
    too, so a removed file counts as a change. None when it cannot be read."""
    root = ROOT / 'openclaw-plugin'
    try:
        return max(p.stat().st_ctime for p in [root, *root.rglob('*')] if 'node_modules' not in p.relative_to(root).parts)
    except (OSError, ValueError):
        return None


def elapsed_seconds(text):
    """ps's etime, [[dd-]hh:]mm:ss, in seconds; None when it is not that."""
    days, _, clock = text.rpartition('-')
    parts = clock.split(':')
    if not (days.isdigit() or not days) or not 2 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
        return None
    seconds = 0
    for part in parts:
        seconds = seconds * 60 + int(part)
    return int(days or 0) * 86400 + seconds


def gateway_started():
    """When the running OpenClaw Gateway started (epoch seconds), from the process list: a process run as `openclaw
    ... gateway ...`. The oldest one counts, so a younger one (a CLI call) never makes it look newer. None when no such
    process is found or ps cannot tell."""
    result = run(['ps', '-eo', 'etime=,args='], timeout=15)
    ages = []
    for line in (result.stdout or '').splitlines() if result.returncode == 0 else []:
        words = line.split()
        if len(words) > 1 and 'gateway' in words[1:] and any('openclaw' in word for word in words[1:]):
            age = elapsed_seconds(words[0])
            if age is None:
                return None
            ages.append(age)
    return time.time() - max(ages) if ages else None


def gateway_runs_these_files(openclaw):
    """Whether the running Gateway is known to have loaded the bridge's files as they are on disk now, without a stamp
    that says which files it loaded: it started after they last changed (a linked bridge is read from this folder when
    the Gateway starts), and it has this bridge in (bridge_in_openclaw). bridge_in_openclaw alone cannot say it: it
    checks the link and that the bridge is loaded, not which version of the files. Anything unclear is False: the
    usual swap."""
    changed, started = bridge_changed_at(), gateway_started()
    return bool(changed and started and changed < started - 2) and bridge_in_openclaw(openclaw)


def may_restart_gateway(paths):
    """Whether this install may restart the OpenClaw Gateway to get the bridge or the model runtime back: yes, unless
    config.json says "gateway_restart": false (a Gateway with live chats and a browser its owner restarts themself)."""
    try:
        return json.loads(paths.config.read_text()).get('gateway_restart', True) is not False
    except (OSError, ValueError, AttributeError, TypeError):
        return True


# OpenClaw 2026.11.2 has no call that says its memory index is running: `openclaw memory status` and the Gateway's
# `memory.status` and `doctor.memory.status` each open a manager of their own, not the one that indexes. What does say
# it is the embedding server: the one the Gateway starts for a local embedding model (llama-server --embeddings
# --metrics, a child of the Gateway), and any other on this computer named in ASSISTANT_EMBEDDING_PORTS (a hosted
# Machine runs its own as a service). Its /metrics counts the requests in hand and queued, its /slots says which slots
# are working. A run does not keep those above zero from start to end: it pauses between batches, for longer than a
# few looks, and goes on. So idle is one unbroken quiet stretch (SWAP_QUIET), not a quiet look. An index on a remote
# embedding provider cannot be seen; the checks after each step cover that.
# A quiet embedding server is not the whole answer either: a full rebuild goes on for minutes without embedding
# anything (most likely texts it embedded before, taken from its cache) and still cannot be stopped in OpenClaw's 5 seconds. What
# shows a rebuild is the database it builds next to the real one, <state dir>/agents/<agent>/agent/
# <name>.sqlite.memory-reindex-<uuid> (with -wal and -shm), which OpenClaw removes when the rebuild ends or is cut
# off. One written in the last REINDEX_FRESH seconds is a rebuild that runs; an older one was left by a Gateway that
# stopped mid-rebuild. Measured on a real Machine: up to 51 seconds between two writes while it ran.
REINDEX_FRESH = 120  # seconds since the last write to a rebuild's database within which the rebuild counts as running
BRIDGE_WAITING = 'plugin-waiting'  # in the data folder, next to the stamp: a changed bridge that is not in OpenClaw yet
SWAP_WAIT = 600  # seconds an update waits for a running index before the bridge goes in
REBUILD_WAIT = 1200  # the same for a rebuild on local embeddings (local_rebuild); one still running then is never swapped into
SWAP_QUIET = 60  # seconds the embedding server has to stay quiet, without a break, before the index counts as stopped
EMBEDDING_COUNTS = re.compile(r'^llamacpp:requests_(?:processing|deferred)\s+([0-9.]+(?:[eE][+-]?[0-9]+)?)\s*$', re.M)


def gateway_embedding_ports():
    """The ports of the embedding servers the running Gateway started, from the process list."""
    result = run(['ps', '-eo', 'pid=,ppid=,args='], timeout=15)
    rows = {}
    for line in (result.stdout or '').splitlines() if result.returncode == 0 else []:
        parts = line.split(None, 2)
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
            rows[int(parts[0])] = (int(parts[1]), parts[2].split())
    def under_gateway(pid):
        seen = set()
        while pid in rows and pid not in seen:
            seen.add(pid)
            pid = rows[pid][0]
            words = rows.get(pid, (0, []))[1]
            if 'gateway' in words and any('openclaw' in word for word in words):
                return True
        return False
    ports = []
    for pid, (_, words) in rows.items():
        if words and Path(words[0]).name == 'llama-server' and '--embeddings' in words and '--metrics' in words and '--port' in words[:-1]:
            port = words[words.index('--port') + 1]
            if port.isdigit() and under_gateway(pid):
                ports.append(int(port))
    return sorted(ports)


def extra_embedding_ports():
    """More embedding servers to ask, for one the Gateway did not start itself: ASSISTANT_EMBEDDING_PORTS, port
    numbers separated by commas. Always on this computer (127.0.0.1); anything that is not a port number is skipped."""
    words = (word.strip() for word in os.environ.get('ASSISTANT_EMBEDDING_PORTS', '').split(','))
    return sorted({int(word) for word in words if word.isascii() and word.isdigit() and 0 < int(word) < 65536})


def embedding_answer(port, path, size):
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{int(port)}{path}', timeout=5) as response:
            return response.read(size).decode('utf-8', 'replace')
    except (OSError, ValueError):
        return None


def embedding_requests(port):
    """The requests an embedding server has in hand or queued, from its own /metrics; from a server that has no
    /metrics, the slots that are working (/slots). None when it says neither."""
    found = EMBEDDING_COUNTS.findall(embedding_answer(port, '/metrics', 200_000) or '')
    if found:
        return sum(float(x) for x in found)
    try:
        slots = json.loads(embedding_answer(port, '/slots', 2_000_000) or 'null')
    except ValueError:
        return None
    working = [slot['is_processing'] for slot in slots if isinstance(slot, dict) and 'is_processing' in slot] if isinstance(slots, list) else []
    return sum(1 for one in working if one) if working else None


def agent_dirs():
    """The folders OpenClaw keeps its agents' databases in, the way it finds them itself: <state dir>/agents/<agent>/
    agent, and the agentDir openclaw.json sets for an agent (agents.list[].agentDir, ~ for the home folder)."""
    found = []
    try:
        found = sorted((onboarding.openclaw_dir() / 'agents').glob('*/agent'))
    except OSError:
        pass
    agents = onboarding.openclaw_settings().get('agents')
    for entry in (agents.get('list') if isinstance(agents, dict) else None) or []:
        value = entry.get('agentDir') if isinstance(entry, dict) else None
        if isinstance(value, str) and value.strip():
            found.append(Path(value.strip()).expanduser())
    return list(dict.fromkeys(found))


def reindex_running():
    """Whether OpenClaw is rebuilding a memory index right now: a rebuild database written in the last REINDEX_FRESH
    seconds, in any agent folder (agent_dirs). Only looks at file times, never inside, and never changes them."""
    newest = 0.0
    for folder in agent_dirs():
        try:
            for path in folder.glob('*.memory-reindex-*'):
                try:
                    newest = max(newest, path.stat().st_mtime)
                except OSError:
                    pass  # removed between the listing and the look: that rebuild just ended
        except OSError:
            continue
    return bool(newest) and time.time() - newest < float(os.environ.get('ASSISTANT_REINDEX_FRESH', REINDEX_FRESH))


def local_memory_search():
    """Whether OpenClaw embeds its memory on this computer (memory.search.provider "local" in openclaw.json, or the
    same under agents.defaults.memorySearch). Only then does a rebuild take long enough to outlast a Gateway stop."""
    settings = onboarding.openclaw_settings()
    def provider(*keys):
        value = settings
        for key in keys:
            value = value.get(key) if isinstance(value, dict) else None
        return value
    return 'local' in (provider('memory', 'search', 'provider'), provider('agents', 'defaults', 'memorySearch', 'provider'))


def local_rebuild():
    """A memory index rebuild on local embeddings that runs now (local_memory_search, reindex_running). OpenClaw waits
    for it on a Gateway stop and on every plugin swap, and nothing cuts it off: the stop runs into systemd's
    TimeoutStopSec and is killed, the swap fails ("plugin service stop timed out ... memory-core-index"). So neither
    happens while one runs."""
    return reindex_running() and local_memory_search()


def index_busy():
    """Whether OpenClaw's memory index is running right now: rebuilding (reindex_running) or embedding. None when
    nothing here can tell (no rebuild, no Gateway embedding server and none named in ASSISTANT_EMBEDDING_PORTS, or one
    that does not say)."""
    if reindex_running():
        return True
    ports = sorted({*gateway_embedding_ports(), *extra_embedding_ports()})
    counts = [n for n in map(embedding_requests, ports) if n is not None]
    return any(counts) if counts else None


def gateway_idle(before, indent=''):
    """Wait until OpenClaw's memory index has stopped: a plugin swap asks it to stop, gives it 5 seconds, and fails
    when it does not. Stopped is SWAP_QUIET seconds without one busy look: a run pauses between batches and goes on,
    so any busy look starts the stretch again. A server that was quiet at the first look gets the same stretch (that
    look may have been in a pause). SWAP_WAIT bounds the wait for a busy index, counted from the first busy look and
    through its pauses; a quiet stretch under way at the bound is let finish. True when stopped, or at once when
    nothing can tell at the first look (no embedding server to ask: nothing to wait for). False when it is still
    running at the bound. An embedding server that goes away during the wait counts as quiet from then on.
    A rebuild on local embeddings (local_rebuild) gets REBUILD_WAIT instead; one that outlasts it ends every later
    wait in this run at once while it still runs."""
    global REBUILD_OUTLASTED
    bound = float(os.environ.get('ASSISTANT_SWAP_WAIT', SWAP_WAIT))
    quiet = float(os.environ.get('ASSISTANT_SWAP_QUIET', SWAP_QUIET))
    pause = float(os.environ.get('ASSISTANT_SWAP_POLL', 2))
    if REBUILD_OUTLASTED and local_rebuild():
        return False  # this run already waited the whole bound for this rebuild: not again
    started = quiet_since = None
    first = told = True
    while True:
        busy = index_busy()
        now = time.monotonic()
        if busy is None and first:
            return True
        if busy:
            quiet_since = None
            rebuilding = local_rebuild()
            if rebuilding and told:
                told = False
                say(f'{indent}OpenClaw is rebuilding its memory index on local embeddings; waiting up to {swap_minutes(True)} for it'
                    f' to finish before {before} (a Gateway stop or plugin swap during a rebuild hangs until it ends).')
            if started is None:
                started = now
                if not rebuilding:
                    say(f'{indent}OpenClaw is building its memory index; waiting up to {swap_minutes()} for it before {before}.')
            elif now - started >= (max(bound, rebuild_bound()) if rebuilding else bound):
                REBUILD_OUTLASTED = rebuilding
                return False
        else:
            if quiet_since is None:
                quiet_since = now
                if first:
                    say(f"{indent}Checking that OpenClaw's memory index stays quiet for {quiet:g} s before {before}.")
            if now - quiet_since >= quiet:
                return True
        first = False
        time.sleep(pause)


def rebuild_bound():
    return float(os.environ.get('ASSISTANT_REBUILD_WAIT', REBUILD_WAIT))


def swap_minutes(rebuild=False):
    """The longest gateway_idle waits, for a rebuild on local embeddings (`rebuild`) or any other index run."""
    bound = float(os.environ.get('ASSISTANT_SWAP_WAIT', SWAP_WAIT))
    return f"{(max(bound, rebuild_bound()) if rebuild else bound) / 60:g} min"


REBUILD_OUTLASTED = False  # gateway_idle: a rebuild on local embeddings outlasted a whole wait in this run


def restore_model_runtime(openclaw, restart, after, restarted=False):
    """A plugin step left the running Gateway unable to run models. Reload the bridge once, after the memory
    index has been quiet for SWAP_QUIET (gateway_idle; OpenClaw's own advice is a reload when the Gateway is
    idle); if that does not bring it back, the same recovery as a failed reload: load_in_gateway, which restarts
    the Gateway where this install may. True once model calls work again; False with the reason and the one
    command that fixes it said."""
    say(f'  After {after}, the OpenClaw Gateway cannot run models. Bringing that back before anything else.')
    if gateway_idle('reloading the bridge', '  '):
        result = run([openclaw, 'plugins', 'reload', PLUGIN_ID, '--wait'], timeout=300)
        if service.model_runtime(openclaw, run) is not False:
            say('  Reloaded the bridge: model calls work again.')
            return RELOADED if result.returncode == 0 else True
    if not restarted and load_in_gateway(openclaw, 'the Gateway cannot run models', restart, recovery=True) and service.model_runtime(openclaw, run) is not False:
        say('  Model calls work again.')
        return RELOADED
    say('  NOT FIXED: the OpenClaw Gateway cannot run models, so no chat, check or to-do run works until it restarts.'
        f'\n  Restart it: {service.gateway_restart_hint(onboarding.gateway_units())}')
    return False


RELOADED = 'reloaded'  # restore_model_runtime: models work again and the Gateway read the bridge from disk doing it
WAITING = 'waiting'  # install_plugin: the bridge waits for the memory index; the rest of the install goes on


def install_plugin(facts, reload=True, stamp=None, restart=True):
    """Link, enable and reload the bridge, unless this exact bridge is already in. Every reload replaces the plugin
    inside a running Gateway, which is slow on a small server and can leave the model runtime unpublished (every
    model call then fails until the Gateway restarts): an update that did not touch the bridge should not do it.
    So a swap only happens when the files changed since the Gateway loaded them: per the stamp's parts, or, without
    them, per gateway_runs_these_files. The nightly --if-bridge-waits run comes through here too.
    One that did waits until OpenClaw's memory index has been quiet for SWAP_QUIET (gateway_idle) before the swap
    and again before the reload, and after each step checks that the Gateway can still run models: it never ends, done or failed, with that
    broken and no recovery tried (restore_model_runtime). `restart`: whether that recovery may restart the
    Gateway (may_restart_gateway).
    Returns True when the bridge is in, False when it failed, and WAITING (true as well: the install goes on) when
    the index was still running at the bound on a Gateway this install may not restart, or was a rebuild on local
    embeddings (local_rebuild, on any Gateway: a restart would hang on it as well): nothing is forced, the
    stamp stays as it was and BRIDGE_WAITING stays next to it, so the next install or nightly update tries again."""
    global REBUILD_OUTLASTED
    REBUILD_OUTLASTED = False
    openclaw = facts.get('openclaw')
    if not openclaw:
        return False
    fingerprint = plugin_fingerprint(facts)
    if stamp and reload:
        had, parts = read_stamp(stamp)
        if had == fingerprint:
            if parts is None:
                write_stamp(stamp, facts)  # a stamp from before the parts were kept: the same bridge, now with them
            stamp.with_name(BRIDGE_WAITING).unlink(missing_ok=True)
            say(f'OpenClaw plugin {PLUGIN_ID}: unchanged, left as it is')
            return True
        now = bridge_parts(facts)
        if parts and (parts.get('files'), parts.get('root')) == (now['files'], now['root']) and bridge_in_openclaw(openclaw):
            # Only the OpenClaw around it changed. The bridge is a link to this folder, not a copy: the new OpenClaw
            # loaded these same files when its Gateway started, so there is nothing to swap.
            write_stamp(stamp, facts)
            say(f'OpenClaw plugin {PLUGIN_ID}: unchanged and already loaded by this OpenClaw, left as it is')
            return True
        if not parts and gateway_runs_these_files(openclaw):
            # No stamp, or one from before the parts were kept, so it cannot say what the Gateway loaded; but the
            # Gateway started after the bridge's files last changed and has it in: a swap would change nothing.
            write_stamp(stamp, facts)
            say(f'OpenClaw plugin {PLUGIN_ID}: already loaded as it is by the running Gateway, left as it is')
            return True
        try:
            stamp.parent.mkdir(parents=True, exist_ok=True)
            stamp.with_name(BRIDGE_WAITING).write_text(fingerprint + '\n')  # until write_stamp: a nightly update tries again
        except OSError:
            pass
    plugin = str(ROOT / 'openclaw-plugin')
    if not gateway_idle('the bridge goes in'):
        rebuilding = local_rebuild()  # a rebuild is never swapped into, not even where a restart could follow: that hangs too
        if rebuilding or not (restart and onboarding.gateway_units()):
            say(f'OpenClaw plugin {PLUGIN_ID}: not swapped in yet. The memory index is still running after {swap_minutes(rebuilding)} and a swap now would'
                ' leave the Gateway unable to run models, so nothing in OpenClaw was changed.\n  Everything else is updated. The bridge goes in'
                ' when the index is done: the next nightly update tries again by itself, and so does ./install.sh.')
            return WAITING
        say(f'  The memory index is still running after {swap_minutes()}; going on. If the Gateway does not take the bridge, it is restarted.')
    def kept(after):  # the Gateway can still run models, or could again after the recovery
        return service.model_runtime(openclaw, run) is not False or restore_model_runtime(openclaw, restart, after)
    say('Installing the local bridge and accepting its declared OpenClaw capabilities (see README Security model).')
    result = run([openclaw, 'plugins', 'install', '--link', '--force', '--accept-capabilities', plugin], timeout=300, capture_output=False)
    if result.returncode != 0:
        say(f'  plugin install failed; run it yourself: openclaw plugins install --link --force --accept-capabilities {plugin}')
        recovered = service.model_runtime(openclaw, run) is not False or restore_model_runtime(openclaw, restart, 'the failed plugin install')
        if recovered == RELOADED and stamp and reload and bridge_in_openclaw(openclaw):
            # The reload (or restart) that brought models back read the bridge from this folder: it is in after all.
            write_stamp(stamp, facts)
            say(f'OpenClaw plugin {PLUGIN_ID}: in after all; the reload that brought model calls back loaded it')
            return True
        if recovered:
            say('  The bridge is not updated yet: run ./install.sh again.')
        return False
    if not kept('the plugin install'):
        return False
    wait = float(os.environ.get('ASSISTANT_PLUGIN_RETRY_WAIT', 5))
    for attempt in range(3):  # right after an install the Gateway may still be applying it; the CLI then fails briefly
        result = run([openclaw, 'plugins', 'enable', PLUGIN_ID], timeout=120)
        if result.returncode == 0 or attempt == 2:
            break
        time.sleep(wait * (attempt + 1))
    if result.returncode != 0:
        say('  plugin enable failed: ' + (result.stderr or result.stdout).strip()[:300])
        kept('the failed plugin enable')
        return False
    if not kept('the plugin enable'):
        return False
    # OpenClaw only runs a non-bundled plugin's conversation hooks with this set; without them a review
    # is never tied to its run and every preview ends "without saving its review".
    result = run([openclaw, 'config', 'set', f'plugins.entries.{PLUGIN_ID}.hooks.allowConversationAccess', 'true', '--strict-json'], timeout=120)
    if result.returncode != 0:
        say('  could not allow the plugin\'s conversation hooks: ' + (result.stderr or result.stdout).strip()[:300]
            + f'\n  run it yourself: openclaw config set plugins.entries.{PLUGIN_ID}.hooks.allowConversationAccess true --strict-json')
        kept('the failed config step')
        return False
    applied = True
    if reload:
        # An index can have started since the swap, and a reload fails on a running one the same way: a fresh stretch.
        if not gateway_idle('reloading the bridge', '  '):
            rebuilding = local_rebuild()
            if rebuilding or not (restart and onboarding.gateway_units()):
                say(f'OpenClaw plugin {PLUGIN_ID}: not reloaded yet. The memory index is still running after {swap_minutes(rebuilding)} and a reload now'
                    ' would leave the Gateway unable to run models, so the bridge is linked but not reloaded: the Gateway runs the one it had'
                    ' until then.\n  Everything else is updated. The bridge goes in when the index is done: the next nightly update tries'
                    ' again by itself, and so does ./install.sh.')
                return WAITING
            say(f'  The memory index is still running after {swap_minutes()}; going on. If the Gateway does not take the bridge, it is restarted.')
        result = run([openclaw, 'plugins', 'reload', PLUGIN_ID, '--wait'], timeout=300)
        if result.returncode != 0:
            # Reload only works in a running Gateway. One that is down (stopped, still starting, or given up by
            # systemd after failed starts) has the bridge saved and loads it as it starts: start it and check.
            applied = load_in_gateway(openclaw, (result.stderr or result.stdout).strip(), restart,
                                      recovery=lambda: service.model_runtime(openclaw, run) is False)  # asked only during a rebuild
            if applied is False:
                if service.model_runtime(openclaw, run) is False:
                    restore_model_runtime(openclaw, restart, 'the failed plugin reload', restarted=True)
                return False
            if applied and service.model_runtime(openclaw, run) is False \
                    and not restore_model_runtime(openclaw, restart, 'the Gateway restart', restarted=True):
                return False
        elif not kept('the plugin reload'):
            return False
    if stamp and reload and applied:
        write_stamp(stamp, facts)
    say(f'OpenClaw plugin {PLUGIN_ID}: linked and enabled'
        + ('' if reload else ' (not reloaded: --no-start)')
        + (' (loads when the Gateway starts)' if applied is None else ''))
    return True


# OpenClaw's own background model work that only spends the owner's usage limits here (The Machine runs its own reviews,
# skills and recaps): the heartbeat turn, Skill Workshop's reviews of finished sessions and the activity recaps after each
# session. The same values the hosted agent sets (QUIET_OPENCLAW in the control plane's machine_agent.py). Set only
# where the owner set nothing, and each only once, so a value they choose later (or remove) stays theirs.
QUIET_OPENCLAW = {
    'agents.defaults.heartbeat.every': '0m',
    'skills.workshop.autonomous.mode': 'off',
    'agents.defaults.utilityModel': '',
}
# Each Gateway session keeps its MCP tool connections until it is stopped or reset, unless an idle time is set, and the
# Gateway holds at most 256: past that every new turn fails (2026-10-30, after three days of to-do chats and reviews on
# one Gateway). Idle sessions let theirs go after 30 minutes; they reconnect on their next turn. Same rules as above.
OPENCLAW_UPKEEP = {
    'mcp.sessionIdleTtlMs': 30 * 60 * 1000,
}
# Telegram's servers fetch a preview of the first link in a message as soon as it arrives, before anyone taps it. The
# to-dos sent there and the assistant's replies carry text a model wrote from incoming messages, so a link it was talked
# into writing (with something private in the address) would reach that site by itself. Previews off; links stay
# tappable. Only once Telegram is set up (a channel with nothing in it would be a half-made one), and only where unset.
TELEGRAM_NO_PREVIEWS = {
    'channels.telegram.linkPreview': False,
}
# OpenClaw's own AGENTS.md in the workspace asks for daily notes but names no single file per day, and the
# session-memory hook leaves a dated file of its own on every reset, so notes for one day end up spread over many.
# These rules go at the end of it once (memory_rules); the path is the one OpenClaw loads at the start of a session.
# The Machine's own results stay in memory/assistant/ (PREPARATION.md), which these rules leave alone.
# What the owner states that stays true is saved as a fact in The Machine (under Learning, where they edit, undo or
# forget it, and where reviews and drafts read it), not in MEMORY.md or USER.md, which nothing of The Machine's reads
# back as facts. Those two files stay as they are and stay readable. The chats without the tool keep using them.
# What they already hold is offered to the owner once, line by line, under Learning (Bring these in, bring_in.py).
MEMORY_RULES_BEGIN, MEMORY_RULES_END = '<!-- the-machine:memory-rules -->', '<!-- /the-machine:memory-rules -->'
MEMORY_RULES = f"""{MEMORY_RULES_BEGIN}
## Daily memory

- Keep one daily note per day at `memory/YYYY-MM-DD.md`, dated in the owner's time zone. Append to it; never rewrite or reorder what is already there.
- The session-memory hook leaves `memory/YYYY-MM-DD-HHMM.md` files on a reset. Merge each into that day's note, keeping unique content and where it came from and skipping exact duplicates.
- A durable fact, decision or lasting preference the owner states is saved as a fact in The Machine (`assistant_signals` `remember_fact`, with `about` for the person, organization or project it is about), never only in a daily note. It shows under Learning, where the owner can edit, undo or forget it. Add no new ones to `MEMORY.md` or `USER.md`, except in a chat without that tool; keep reading both.
- Results of to-dos stay in `memory/assistant/`; they are not daily notes.
{MEMORY_RULES_END}
"""
# The blocks earlier versions wrote, whole. A workspace that still has one of these byte for byte gets MEMORY_RULES in
# its place, once (memory_rules); one the owner changed in any way is theirs and is never touched. When MEMORY_RULES
# changes again, its old text goes in this list.
MEMORY_RULES_BEFORE = (
    f"""{MEMORY_RULES_BEGIN}
## Daily memory

- Keep one daily note per day at `memory/YYYY-MM-DD.md`, dated in the owner's time zone. Append to it; never rewrite or reorder what is already there.
- The session-memory hook leaves `memory/YYYY-MM-DD-HHMM.md` files on a reset. Merge each into that day's note, keeping unique content and where it came from and skipping exact duplicates.
- Durable decisions and facts go in `MEMORY.md` and lasting preferences in `USER.md`, never only in a daily note.
- Results of to-dos stay in `memory/assistant/`; they are not daily notes.
{MEMORY_RULES_END}
""",
)
MEMORY_RULES_VERSION = len(MEMORY_RULES_BEFORE) + 1  # kept in the stamp: which text this workspace was last offered


def quiet_openclaw(facts, stamp):
    """QUIET_OPENCLAW, OPENCLAW_UPKEEP and TELEGRAM_NO_PREVIEWS into openclaw.json where nothing is set yet (OpenClaw reloads these without a restart). The keys
    set once are kept in `stamp`. Returns the keys set now."""
    openclaw = facts.get('openclaw')
    if not openclaw:
        return []
    settings = onboarding.openclaw_settings()
    try:
        done = set(json.loads(stamp.read_text())) if stamp.exists() else set()
    except (OSError, ValueError, TypeError):
        done = set()
    changed = []
    telegram = TELEGRAM_NO_PREVIEWS if has_telegram(settings) else {}  # set up later: the next install or update sets it
    for key, value in {**QUIET_OPENCLAW, **OPENCLAW_UPKEEP, **telegram}.items():
        node = settings
        for part in key.split('.'):
            node = node.get(part, None) if isinstance(node, dict) else None
        if key in done or node is not None:
            done.add(key)
            continue
        result = run([openclaw, 'config', 'set', key, json.dumps(value), '--strict-json'], timeout=120)
        if result.returncode == 0:
            changed.append(key)
            done.add(key)
        else:
            say(f'  could not set {key} in OpenClaw: ' + (result.stderr or result.stdout).strip()[:200])
    try:
        stamp.parent.mkdir(parents=True, exist_ok=True)
        stamp.write_text(json.dumps(sorted(done)) + '\n')
    except OSError:
        pass
    quiet = [key for key in changed if key in QUIET_OPENCLAW]
    if quiet:
        say('OpenClaw background turns that only use your AI limits are off: ' + ', '.join(quiet))
    if any(key in OPENCLAW_UPKEEP for key in changed):
        say('Idle OpenClaw sessions release their tool connections after 30 minutes')
    if any(key in TELEGRAM_NO_PREVIEWS for key in changed):
        say('Telegram link previews are off, so no link in a message is opened before you tap it')
    return changed


# OpenClaw's Gateway unit lets systemd give up after 10 failed starts in 5 minutes (StartLimitBurst=10). Right after a
# boot the Gateway can fail its first starts while everything else starts too (a self-hosted Machine, 2026-11-02: ten
# failures in two minutes, then no AI for half an hour until a manual restart that worked at once). This drop-in keeps
# systemd retrying, 15 seconds apart. OpenClaw keeps it across its own unit rewrites; its file name is ours. Hosted
# Machines' agent writes the same bytes, so neither rewrites the other's.
# macOS needs nothing: OpenClaw's launchd agent has KeepAlive, which never stops retrying.
GATEWAY_RETRY_DROPIN = 'keep-retrying.conf'
GATEWAY_RETRY_TEXT = """# Written by The Machine: never give up after a bad boot, keep retrying every 15s.
[Unit]
StartLimitIntervalSec=0
[Service]
RestartSec=15
"""


def gateway_keep_retrying(paths):
    """GATEWAY_RETRY_TEXT as a drop-in for each OpenClaw Gateway systemd user unit here. Only next to a unit that is
    already there: OpenClaw refuses to write its unit the first time when drop-ins for it exist. Returns the drop-ins
    written now; a rerun with them in place changes nothing."""
    if service.manager() != 'systemd':
        return []
    written = []
    for unit in onboarding.gateway_units():
        if 'gateway' not in unit or not re.fullmatch(r'[A-Za-z0-9:_.@-]+\.service', unit) or '..' in unit:
            continue  # a unit name is one file name (systemd allows no slashes); anything else is not written to
        path = paths.home / '.config/systemd/user' / f'{unit}.d' / GATEWAY_RETRY_DROPIN
        try:
            if path.exists() and path.read_text() == GATEWAY_RETRY_TEXT:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(GATEWAY_RETRY_TEXT)
        except OSError as error:
            say(f'  could not write {path}: {error}')
            continue
        written.append(path)
    if written:
        run(['systemctl', '--user', 'daemon-reload'], timeout=120)  # read from the next (re)start; nothing restarts now
        say('OpenClaw Gateway: systemd keeps retrying it after failed starts (' + ', '.join(str(p) for p in written) + ')')
    return written


def memory_rules(workspace, stamp):
    """MEMORY_RULES at the end of the workspace's AGENTS.md, once. Not when the file isn't there yet (OpenClaw writes
    its own first; the next install or update adds them), and not when it already has rules for the session-memory
    hook's files (the owner's own). Once done it is kept in `stamp`, so rules the owner edits or removes stay that way.
    A workspace that got an earlier text is looked at once more per new text: only when the whole file still holds that
    earlier block byte for byte (MEMORY_RULES_BEFORE), and only once, does the new block take its place. Anything
    else (a word changed, a line gone, the block removed) is the owner's and the file is left as it is, for good.
    True when added or replaced now."""
    try:
        seen = json.loads(stamp.read_text()) if stamp.exists() else None
    except OSError:
        return False
    except (ValueError, UnicodeDecodeError):
        seen = {}
    seen = seen if isinstance(seen, dict) or seen is None else {}
    if seen is not None and seen.get('version', 1) >= MEMORY_RULES_VERSION:
        return False
    agents = Path(workspace) / 'AGENTS.md'
    try:
        text = agents.read_bytes().decode('utf-8')  # the bytes as they are: no newline translation on any system
    except (OSError, UnicodeDecodeError):
        return False
    fresh = seen is None and MEMORY_RULES_BEGIN not in text
    if fresh:
        added = 'session-memory' not in text.lower()
        after = text.rstrip('\n') + '\n\n' + MEMORY_RULES if added else None
    else:  # a block is there, or was offered before: only an untouched earlier one is replaced
        old = [b for b in MEMORY_RULES_BEFORE if text.count(b) == 1]
        added = len(old) == 1 and text.count(MEMORY_RULES_BEGIN) == 1 and text.count(MEMORY_RULES_END) == 1
        after = text.replace(old[0], MEMORY_RULES) if added else None
    if added:
        temp = agents.with_name('.AGENTS.md.the-machine.tmp')
        try:
            temp.write_bytes(after.encode('utf-8'))
            shutil.copymode(agents, temp)
            owner = agents.stat()
            if hasattr(os, 'chown') and (owner.st_uid, owner.st_gid) != (temp.stat().st_uid, temp.stat().st_gid):
                os.chown(temp, owner.st_uid, owner.st_gid)  # the file stays whose it was
            os.replace(temp, agents)
        except OSError as error:
            temp.unlink(missing_ok=True)
            say(f'  could not {"add the memory rules to" if fresh else "update the memory rules in"} {agents}: {error}')
            return False
        if fresh:
            say(f'Memory rules added to {agents} (edit or remove them there; they are not added again)')
        else:
            say(f'Memory rules in {agents} updated: what you tell your assistant to remember is now saved under Learning '
                '(the block was still as installed; one you changed is never touched)')
    try:
        stamp.parent.mkdir(parents=True, exist_ok=True)
        stamp.write_text(json.dumps({'added': added if fresh else bool((seen or {}).get('added')), 'version': MEMORY_RULES_VERSION,
                                     **({} if fresh else {'replaced': added}), 'at': time.strftime('%Y-%m-%d')}) + '\n')
    except OSError:
        pass
    return added


# A new install starts at this thinking level for chats and work (agents.defaults.thinkingDefault), as a new hosted
# Machine does (NEW_THINKING in the control plane's machine_agent.py): good results for much less of the owner's AI plan.
# Only where no level is set, and only when the main model is signed in and offers it (the running Gateway's model list
# says); a model without it keeps its own default. An existing install keeps its level: this runs on a first install only.
NEW_THINKING = 'low'


def start_thinking(facts):
    """NEW_THINKING for a new install, as above. Whether it was set."""
    openclaw = facts.get('openclaw')
    if not openclaw:
        return False
    defaults = (onboarding.openclaw_settings().get('agents') or {}).get('defaults') or {}
    if not isinstance(defaults, dict) or defaults.get('thinkingDefault'):
        return False
    main = defaults.get('model')
    main = main.get('primary') if isinstance(main, dict) else main
    if not isinstance(main, str) or '/' not in main:
        return False
    result = run([openclaw, 'gateway', 'call', 'models.list', '--json', '--timeout', '30000', '--params', '{"view":"configured"}'], timeout=60)
    try:
        rows = (json.loads(result.stdout or '{}').get('models') or []) if result.returncode == 0 else []
    except (ValueError, AttributeError):
        rows = []
    row = next((r for r in rows if isinstance(r, dict) and f"{r.get('provider')}/{r.get('id')}" == main.strip()), None)
    levels = [x.get('id') for x in (row or {}).get('thinkingLevels') or [] if isinstance(x, dict)]
    if not row or row.get('available') is not True or NEW_THINKING not in levels:
        return False
    result = run([openclaw, 'config', 'set', 'agents.defaults.thinkingDefault', json.dumps(NEW_THINKING), '--strict-json'], timeout=120)
    if result.returncode:
        say('  could not set the thinking level in OpenClaw: ' + (result.stderr or result.stdout).strip()[:200])
        return False
    say(f'Thinking starts at {NEW_THINKING} for chats and work (change it in Settings, Model)')
    return True


def gateway_health(openclaw):
    """The running Gateway's own health (with the plugins it loaded), or None when no Gateway answers."""
    result = run([openclaw, 'gateway', 'health', '--json', '--timeout', '20000'], timeout=60)
    try:
        found = json.loads(result.stdout or '{}')
    except ValueError:
        return None
    return found if isinstance(found, dict) and found.get('ok') else None


def load_in_gateway(openclaw, reload_error='', restart=True, recovery=False):
    """After a failed reload: True once the Gateway runs with the bridge loaded, None when no Gateway service runs
    here at all (the bridge is saved and loads when the owner starts one), False with the reason said otherwise.
    `restart` False (may_restart_gateway): the owner restarts this Gateway themself, so it says the command instead.
    During a rebuild on local embeddings (local_rebuild) it waits for that first, like a swap. A planned restart (to
    load the bridge) leaves the Gateway as it is when the rebuild outlasts the wait. A `recovery` one (the Gateway
    cannot run models; True, or a call that says it) restarts anyway: no models is worse than a stop that waits for
    the rebuild."""
    unit = (onboarding.gateway_units() or [None])[0]
    if not unit:
        if gateway_health(openclaw) is None:
            say('  The OpenClaw Gateway is not running here; the bridge is saved and loads when it starts (openclaw gateway start).')
            return None
        say('  plugin reload failed: ' + reload_error[:300])
        return False
    if not restart:
        say(f'  The OpenClaw Gateway did not take the bridge live ({reload_error[:200]}), and this install leaves restarting it to you'
            f' ("gateway_restart": false in config.json).\n  Restart it: systemctl --user restart {unit}')
        return False
    if local_rebuild() and not gateway_idle(f'restarting {unit}', '  '):
        if recovery() if callable(recovery) else recovery:
            say(f'  OpenClaw is still rebuilding its memory index after {swap_minutes(True)}, but the Gateway cannot run models:'
                f' restarting {unit} anyway (its stop may wait for the rebuild).')
        else:
            say(f'  Not restarting {unit}: OpenClaw is still rebuilding its memory index after {swap_minutes(True)}, and a Gateway stop'
                ' waits for that rebuild until systemd kills it. The bridge goes in when the rebuild is done: the next nightly update tries'
                f' again by itself, and so does ./install.sh.\n  Or restart it yourself once the rebuild is done: systemctl --user restart {unit}')
            return False
    say(f'  The OpenClaw Gateway did not take the bridge live; (re)starting {unit} so it loads it.')
    run(['systemctl', '--user', 'reset-failed', unit], timeout=30)  # after repeated failed starts systemd stops trying
    result = run(['systemctl', '--user', 'restart', unit], timeout=300)
    if result.returncode != 0:
        say(f'  Could not start the OpenClaw Gateway ({unit}): ' + (result.stderr or result.stdout).strip()[:300]
            + f'\n  Check: systemctl --user status {unit}; journalctl --user -u {unit} -n 50; openclaw doctor')
        return False
    deadline = time.time() + float(os.environ.get('ASSISTANT_GATEWAY_WAIT', 300))  # a first start on 4 GB takes a minute or more
    errors = []
    while True:
        live = gateway_health(openclaw)
        plugins = (live or {}).get('plugins') or {}
        if PLUGIN_ID in (plugins.get('loaded') or []):
            say(f'  The Gateway is running with {PLUGIN_ID} loaded.')
            return True
        errors = [e.get('error') for e in plugins.get('errors') or [] if isinstance(e, dict) and e.get('id') == PLUGIN_ID]
        if errors or time.time() >= deadline:
            break
        time.sleep(5)
    if not live:
        say('  The OpenClaw Gateway did not come up; the bridge is installed and loads when it starts.'
            f'\n  Check: systemctl --user status {unit}; journalctl --user -u {unit} -n 50; openclaw doctor')
        return False
    say(f'  The Gateway is running but did not load {PLUGIN_ID}' + (': ' + str(errors[0])[:300] if errors else '')
        + '\n  Check: openclaw plugins doctor')
    return False


def health(config, timeout):
    deadline = time.time() + timeout
    url = f"http://127.0.0.1:{config.get('port', 8787)}/health"
    while True:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                if json.loads(response.read()).get('ok'):
                    return True
        except (OSError, ValueError):
            pass
        if time.time() >= deadline:
            return False
        time.sleep(1)


def activate(paths):
    config = json.loads(paths.config.read_text())
    config['delivery_enabled'] = True
    config.setdefault('review_worker', {})['enabled'] = True
    write_private(paths.config, json.dumps(config, indent=2) + '\n')
    return config


def guided(paths, since, ui=None):
    """After a healthy start in a terminal: connect what is not set up, show the first sync, offer the
    dashboard and USER.md, then a preview and, after it, turning reviews on. Every step can be skipped."""
    ui = ui or onboarding.UI()
    config = json.loads(paths.config.read_text())
    todo = [a for a in config.get('accounts', []) if onboarding.missing(config, a)]
    connected = []
    if todo:
        say('\nConnect your sources now (a minute each; skip any and run `assistant connect <name>` later).')
    for account in todo:
        name = onboarding.connect_name(account, config)
        if not ui.yes(f'Connect {onboarding.label(account.get("service", "gmail"))} ({account["id"]}) now?', True):
            continue
        try:
            google_pair.connect(onboarding, paths.config, account.get('service', 'gmail'), ui, account['id'], restart=False)
            connected.append(account['id'])
        except onboarding.SetupError as error:
            say(f'  ✗ {error.message}' + (f'\n    fix: {error.fix}' if error.fix else '') + f'\n    later: assistant connect {name}')
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:  # one source's surprise should not end the whole setup
            say(f'  ✗ {account["id"]} failed unexpectedly: {type(error).__name__}: {str(error)[:200]}\n    later: assistant connect {name}')
    config = json.loads(paths.config.read_text())
    ready = [a['id'] for a in config.get('accounts', []) if not onboarding.missing(config, a)]
    if ready:
        if connected:
            onboarding.restart_and_sync(config, ready, ui, config_path=paths.config)
        else:
            onboarding.first_sync(config, ready, since, ui, wait=45)
    onboarding.serve_dashboard(config, ui)
    onboarding.offer_user_md(config, ui, paths.workspace)
    if ready and not onboarding.says_how_you_write(onboarding.user_md_path(paths.workspace)) and ui.yes(
            'Draft how you write and what matters to you from your own recent messages? Your agent reads them once;'
            ' you see the draft before USER.md changes', True):
        subprocess.call([sys.executable, str(ROOT / 'cli.py'), '--config', str(paths.config), 'profile', '--workspace', str(paths.workspace)])
    if config.get('delivery_enabled') and config.get('review_worker', {}).get('enabled'):
        return config
    if ready and ui.yes('Run a preview now? Your agent checks the last 7 days and shows the to-dos here and on the dashboard;'
                        ' nothing is sent and nothing is done in your accounts', True):
        previewed = subprocess.call([sys.executable, str(ROOT / 'cli.py'), '--config', str(paths.config), 'preview']) == 0
        if not previewed:
            say('  The preview did not finish; turn checks on once it works (./install.sh --preview, then --activate).')
        if ui.yes('Turn on checks and to-dos in Telegram now? (Do it acts with your accounts only when you tap it;'
                  ' see README "Security model")', previewed):
            config = activate(paths)
            restarted = service.restart(UNIT_NAME, run=run).returncode == 0
            say('  Checks and to-dos in Telegram are on.' if restarted else
                f'  Saved; restart to apply: {service.hint("restart")}')
    return config


def next_steps(config, healthy, started, paths=None):
    paths = paths or Paths()
    host, path = config.get('dashboard_host', ''), config.get('dashboard_path', '/assistant/')
    lines = ['', 'Your Machine is up. Next steps:' if started and healthy else 'Next steps:']
    if started:
        lines.append(f'  - Health: {"OK" if healthy else "not answering yet; check " + service.hint("logs")}')
    for account in config.get('accounts', []):
        if onboarding.missing(config, account):
            lines.append(f'  - Connect {onboarding.label(account.get("service", "gmail"))}: assistant connect {onboarding.connect_name(account, config)}')
    served = onboarding.dashboard_url(config)
    if served:
        lines.append(f'  - Dashboard: {served}')
    else:
        lines += [f'  - Dashboard on your tailnet: {" ".join(onboarding.serve_command(config))}',
                  f'    then open https://{host}{path} (custom domain instead: see deploy/Caddyfile)']
    user_md = onboarding.user_md_path(paths.workspace)
    if not user_md.exists() or onboarding.user_md_is_template(user_md):
        lines.append(f'  - Tell the agent about you: create USER.md in {paths.workspace} (name, companies, tone, preferences)')
    elif not onboarding.says_how_you_write(user_md):
        lines.append('  - Let your agent draft how you write and what matters to you from your own messages: assistant profile (you see it first)')
    if config.get('message_protection') is not False and config.get('database'):
        key = message_seal.key_path(Path(config['database']).expanduser())
        if message_seal.in_keyring(Path(config['database']).expanduser()):
            lines.append('  - Messages are encrypted in the database with a key in your keyring (assistant message-key status)')
        else:
            lines.append(f'  - Messages are encrypted in the database with the key {key}. Back it up with the database:'
                         ' without it they are lost')
    lines += ['  - Keep `Do it` in mind: it lets the agent act with your accounts. Read README "Security model".',
              '  - After editing config.json: ' + service.hint('restart')]
    if not config.get('delivery_enabled') or not config.get('review_worker', {}).get('enabled'):
        lines += ['  - See what it would suggest: ./install.sh --preview (one check of the last 7 days by your agent;',
                  '    the to-dos show here and on the dashboard; nothing is sent and nothing is done in your accounts)',
                  '  - Once sources are connected and Security model is understood: ./install.sh --activate']
    lines.append('  - Check everything any time: assistant doctor (each problem comes with its fix)')
    say('\n'.join(lines))


# ---------------------------------------------------------------- uninstall

def uninstall(paths, purge, interactive):
    launchd = service.manager() == 'launchd'
    if service.available():
        stopped = service.disable_now(UNIT_NAME, run=run)
        if stopped.returncode != 0 and paths.unit.exists():
            say('Could not stop the service; kept files and data. Check ' + service.hint('status'))
            return 1
    elif paths.unit.exists():
        say('Cannot stop the installed service without its service manager; kept files and data.')
        return 1
    if paths.unit.exists():
        paths.unit.unlink()
        say(f'Removed {paths.unit}')
    for name in (UPDATE_TIMER, UPDATE_UNIT):
        if (paths.unit.parent / name).exists():
            if service.available():
                service.disable_now(name, run=run)
            (paths.unit.parent / name).unlink()
            say(f'Removed {paths.unit.parent / name}')
    try:  # Telegram chats: each logged-in device is logged out at Telegram, and its store goes
        config = json.loads(paths.config.read_text()) if paths.config.exists() else {}
    except (OSError, ValueError):
        config = {}
    for account in config.get('accounts', []) if isinstance(config, dict) else []:
        if isinstance(account, dict) and account.get('service') == 'telegram' and account.get('id'):
            onboarding.telegram_remove(config, account)
            say(f'Logged out of Telegram: {account["id"]}')
        if isinstance(account, dict) and account.get('service') == 'signal' and account.get('id'):
            onboarding.signal_setup.signal_remove(config, account)  # its keys go; the phone lists it until removed there
            say(f'Removed Signal from this Machine: {account["id"]}')
    pattern = service.LABEL_PREFIX + 'wacli-*.plist' if launchd else 'the-machine-wacli-*.service'
    for sync in sorted(paths.unit.parent.glob(pattern)):
        # The WhatsApp syncs it started; the linked wacli store itself stays.
        if service.available():
            unit = 'the-machine-' + sync.stem.removeprefix(service.LABEL_PREFIX) + '.service' if launchd else sync.name
            service.disable_now(unit, run=run)
        sync.unlink()
        say(f'Removed {sync}')
    if shutil.which('systemctl') and not launchd:
        if run(['systemctl', '--user', 'daemon-reload']).returncode != 0:
            say('systemd daemon-reload failed; rerun uninstall after fixing the user service manager.')
            return 1
    openclaw = shutil.which('openclaw')
    if openclaw:
        result = run([openclaw, 'plugins', 'uninstall', PLUGIN_ID, '--force', '--keep-files'], timeout=120)
        say(f'OpenClaw plugin {PLUGIN_ID}: ' + ('uninstalled' if result.returncode == 0 else 'not removed (' + (result.stderr or '').strip()[:200] + ')'))
        if result.returncode != 0:
            say('Kept data because plugin removal failed.')
            return 1
    if paths.cli.is_symlink() and paths.cli.resolve() == ROOT / 'cli.py':
        paths.cli.unlink()
        say(f'Removed {paths.cli}')
    if purge:
        if interactive and ask(f'Delete {paths.data} with your config, database and secrets? Type "delete"') != 'delete':
            say('Kept the data directory.')
            return 0
        if paths.data.exists():
            shutil.rmtree(paths.data)
            say(f'Deleted {paths.data}')
    else:
        say(f'Kept your data in {paths.data} (use --purge to delete it)')
    return 0


# ---------------------------------------------------------------- main

def browser_viewer_setup(paths, install=None):
    """The optional viewer: its units and files, then the dashboard links stuck cards to it (`browser_url`) and
    brings tabs to the front through its DevTools port (`browser_cdp_url`)."""
    import browser_viewer
    url = (install or browser_viewer.install)(say=say)
    if not url:
        return 1
    config = onboarding.load(paths.config)
    config.update(browser_url=url, browser_cdp_url=browser_viewer.CDP_URL)
    onboarding.save(paths.config, config)
    restarted = service.try_restart(UNIT_NAME, run=run).returncode == 0
    say('  To-dos that wait on the browser now link to it.' if restarted else f'  Saved; restart to apply: {service.hint("restart")}')
    return 0


WINDOWS_ROUTE = ('On Windows, The Machine runs inside WSL2 (Linux), next to OpenClaw\'s Gateway. In PowerShell:\n'
                 '  irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex\n'
                 'See docs/getting-started.md, "Windows".')


def dry_run(paths):
    """What an install would do here, without writing or starting anything."""
    if os.name == 'nt':
        say(WINDOWS_ROUTE)
        return 0
    ok, facts = check_prerequisites()
    manager = service.manager()
    say(f'\nDry run: nothing written. Service manager: {manager}' + (' (inside WSL2)' if manager == 'systemd' and service.wsl() else ''))
    say(f'  config      {paths.config}' + (' (kept)' if paths.config.exists() else ' (new)'))
    say(f'  data        {paths.data} (mode 700; secrets mode 600)')
    say(f'  CLI         {paths.cli} -> {ROOT / "cli.py"}')
    say(f'  plugin      openclaw plugins install --link --force --accept-capabilities {ROOT / "openclaw-plugin"}')
    if manager == 'none':
        say('  service     none here: start it with `python3 assistant.py serve`')
    else:
        text = agent_text({}, facts, paths.config, paths) if manager == 'launchd' else unit_text({}, facts, paths.config)
        say(f'  service     {paths.unit}:\n' + '\n'.join('    ' + line for line in text.rstrip().splitlines()))
    say('\nReady to install.' if ok else '\nFix the FAIL items above before installing.')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--non-interactive', action='store_true', help='take answers from ASSISTANT_* environment variables')
    parser.add_argument('--uninstall', action='store_true', help='remove the service, plugin and CLI link (keeps data)')
    parser.add_argument('--purge', action='store_true', help='with --uninstall: also delete config, database and secrets')
    parser.add_argument('--no-start', action='store_true', help='install files but do not enable or start the service')
    parser.add_argument('--skip-plugin', action='store_true', help='do not install the OpenClaw plugin')
    parser.add_argument('--activate', action='store_true', help='enable checks and Telegram delivery on an existing install')
    parser.add_argument('--preview', action='store_true', help='existing install: one check of the last 7 days, shown only (assistant preview)')
    parser.add_argument('--browser-viewer', action='store_true', help='existing install: a browser of its own on a virtual display, viewed in yours (127.0.0.1 only)')
    parser.add_argument('--dry-run', action='store_true', help='check prerequisites and show what would be written; changes nothing')
    parser.add_argument('--if-bridge-waits', action='store_true', help='do nothing unless a changed bridge still waits to go into OpenClaw (the nightly update uses this)')
    parser.add_argument('--from-main', action='store_true', help='first install: this checkout as it is, not the newest signed release')
    parser.add_argument('--health-timeout', type=float, default=30)
    args = parser.parse_args(argv)
    interactive = not args.non_interactive and sys.stdin.isatty()
    paths = Paths()
    if args.if_bridge_waits and not (paths.data / BRIDGE_WAITING).exists():
        return 0
    if args.dry_run:
        return dry_run(paths)
    if os.name == 'nt':
        say(WINDOWS_ROUTE)
        return 1
    if args.purge and not args.uninstall:
        parser.error('--purge only works with --uninstall')
    if args.activate and (args.no_start or args.uninstall or not paths.config.exists()):
        parser.error('--activate needs an existing installation and a running service (no --no-start/--uninstall)')
    if args.preview:
        if args.activate or args.uninstall or not paths.config.exists():
            parser.error('--preview needs an existing installation and a running service (no --activate/--uninstall)')
        # Installs nothing and changes no config: the CLI asks the running service for one preview review.
        return subprocess.call([sys.executable, str(ROOT / 'cli.py'), '--config', str(paths.config), 'preview'])
    if args.browser_viewer:
        if args.uninstall or not paths.config.exists():
            parser.error('--browser-viewer needs an existing installation (no --uninstall)')
        if service.manager() != 'systemd':
            parser.error('--browser-viewer runs on Linux only (a virtual display with systemd units)')
        return browser_viewer_setup(paths)
    if args.uninstall:
        return uninstall(paths, args.purge, interactive)
    if not paths.config.exists() and not (args.from_main or os.environ.get('ASSISTANT_FROM_MAIN') == '1'):
        moved = to_signed_release()
        if moved is False:
            return 1
        if moved:  # the release's own installer from here on
            os.execv(sys.executable, [sys.executable, str(ROOT / 'installer.py'), *(sys.argv[1:] if argv is None else argv)])
    if not paths.config.exists():
        say('Setting up a Machine of your own on this computer.\n')
    if interactive:
        try:
            offer_openclaw(onboarding.UI())
        except (KeyboardInterrupt, EOFError):
            say('\nStopped; nothing of The Machine was written. Rerun ./install.sh to go on.')
            return 1
    ok, facts = check_prerequisites()
    if not ok:
        say('\nFix the FAIL items above and rerun ./install.sh')
        return 1
    fresh = not paths.config.exists()
    steps = (facts, paths, fresh, not args.no_start, args.skip_plugin)
    ahead = Ahead(prepare, *steps, True) if fresh and interactive else None  # only a first install asks questions
    try:
        config = setup_config(interactive, facts, paths)
    except (KeyboardInterrupt, EOFError):
        if ahead:
            say('\nStopped; your answers were not saved.')
            try:
                ahead.result()  # the OpenClaw steps already under way finish; nothing half done is left
            except Exception:
                pass
            say('Rerun ./install.sh to go on.')
            return 1
        say('\nStopped; nothing was written.')
        return 1
    setup_secrets(config, facts, paths)
    install_cli(paths)
    if not (ahead.result() if ahead else prepare(*steps)):
        return 1
    if args.activate:
        config = activate(paths)
    since = onboarding.now()
    started = install_unit(config, facts, paths, start=not args.no_start)
    install_updates(config, facts, paths, start=not args.no_start)
    healthy = started and health(config, args.health_timeout)
    if interactive and healthy:
        try:
            config = guided(paths, since)
        except (KeyboardInterrupt, EOFError):
            say('\nStopped the guided setup; everything done so far is saved. Pick it up with: assistant doctor')
            config = json.loads(paths.config.read_text())
    next_steps(config, healthy, started, paths)
    return 0 if (args.no_start and started is None) or (started and healthy) else 1


if __name__ == '__main__':
    sys.exit(main())
