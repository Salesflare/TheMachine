"""One-click pairing: a self-hosted Machine pairs with its owner's account from its own dashboard, no code to copy and
no restart (docs/ai-connections.md, Pairing). The code way (`cli.py fleet-pair`, fleet.pair) keeps working.

1. start(): POST /api/fleet/pair-request with this Machine's public keys (network_crypto, the same keys the Network
   pins), signed with its own sign key. The control plane answers with a page on the account (/pair/<id>) and a short
   code; the dashboard opens the page and shows the code, so the owner can match the two.
2. On that page the signed-in owner confirms (and picks a name for the account when it has none). The control plane
   then seals this Machine's new token for its box key, bound to the request.
3. pickup(): POST /api/fleet/pair-pickup, signed again, until it says paired (or gone). The sealed token opens only
   with this Machine's private box key; keep() writes it 0600 next to the database and into the config, like the CLI.

Nothing here logs the token, the request id or the page."""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import re
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import fleet
import network
import onboarding

LOG = logging.getLogger('personal-assistant')
nc = network.nc

REQUEST_PREFIX = b'tm-device-pair/1\n'           # what a pair request is signed as (the control plane checks it)
PICKUP_PREFIX = b'tm-device-pair-pickup/1\n'     # and a pickup
BOX_INFO = b'tm-device-pair/1'                   # the sealing of the token, bound to the request: {'p': 'pair', 'r': id}
EXPIRES = 600                                    # seconds a request waits for the owner
PICKUP_EVERY = 2                                 # seconds between pickups while it waits
REQUEST_ID = re.compile(r'[A-Za-z0-9_-]{16,64}')
TOKEN_FILE = 'fleet-token'


def keys(config):
    """This Machine's private keys (the Network's: network.keys_path), made once when missing."""
    path = network.keys_path(config)
    if not path:
        raise ValueError('This Machine has no place to keep its keys')
    return nc.load_or_make(path)


def code(sign_public):
    """The short code the account's page shows too: base32 of sha256 of the raw sign key, 8 characters as XXXX-XXXX."""
    text = base64.b32encode(hashlib.sha256(sign_public).digest()).decode()[:8]
    return text[:4] + '-' + text[4:]


def _signed(private, prefix, body):
    message = prefix + json.dumps(body, sort_keys=True, separators=(',', ':')).encode()
    return {**body, 'sig': nc.b64(nc.ed25519_sign(nc.unb64(private['sign'], 32), message))}


def request_body(private, label, emails, clock=None):
    """The signed pair request: label, the owner's addresses, both public keys. keys_sig is the Network's own
    signature of the keys (network_crypto.public_keys), so the control plane can publish them for this Machine."""
    public = nc.public_keys(private)
    body = {'label': str(label or 'My Machine')[:80], 'emails': list(emails or [])[:20], 'sign': public['sign'], 'box': public['box'],
            'nonce': secrets.token_hex(16), 'at': int((clock or time.time)())}
    return {**_signed(private, REQUEST_PREFIX, body), 'keys_sig': public['sig']}


def pickup_body(private, request_id, clock=None):
    return _signed(private, PICKUP_PREFIX, {'id': request_id, 'nonce': secrets.token_hex(16), 'at': int((clock or time.time)())})


def _post(path, body, timeout=20):
    """POST to the Network's public pairing routes: NETWORK first, its old address RELAY when that can't be reached."""
    for base in (fleet.NETWORK, fleet.RELAY):
        request = urllib.request.Request(base + '/api/fleet' + path, method='POST', headers={'Content-Type': 'application/json'},
                                         data=json.dumps(body).encode())
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                found = json.loads(response.read() or b'{}')
            return found if isinstance(found, dict) else {}
        except urllib.error.HTTPError as error:
            with error:
                try:
                    found = json.loads(error.read() or b'{}')
                except ValueError:
                    found = {}
            found = found if isinstance(found, dict) else {}
            if error.code == 404:
                raise ValueError('Your account can’t pair this way yet. Try again later.') from None
            if error.code == 429:
                raise fleet.Limited(str(found.get('error') or 'Not now; try again later.')) from None
            raise ValueError(str(found.get('error') or f'The Network said {error.code}')) from None
        except (urllib.error.URLError, OSError):
            if base == fleet.RELAY:
                raise ValueError('The Network did not answer. Try again in a minute.') from None
    return {}


def page_ok(url, request_id):
    """Only the account's own pair page for this request: https on one of the Network's main hosts."""
    link = urllib.parse.urlsplit(str(url or ''))
    return link.scheme == 'https' and link.hostname in fleet.MAIN_HOSTS and link.path == '/pair/' + request_id and not link.query


def start(config, label, post=None, clock=None):
    """Asks the account for a pair page: {id, url, code, until}. ValueError when it can't."""
    private = keys(config)
    found = (post or _post)('/pair-request', request_body(private, label, fleet.account_emails(config), clock))
    request_id = str(found.get('id') or '')
    if not REQUEST_ID.fullmatch(request_id) or not page_ok(found.get('url'), request_id):
        raise ValueError('Your account gave no pair page. Try again.')
    mine = code(nc.unb64(nc.public_keys(private)['sign'], 32))
    try:
        wait = max(30, min(int(found.get('expires_in') or EXPIRES), EXPIRES))
    except (TypeError, ValueError):
        wait = EXPIRES
    return {'id': request_id, 'url': found['url'], 'code': mine, 'until': (clock or time.time)() + wait}


def pickup(config, request_id, post=None, clock=None):
    """One look: {'state': 'waiting'} or {'state': 'gone'}, or {'state': 'paired', 'token', 'label', 'device'} with
    the token opened. A sealed token that doesn't open here (not for this Machine, or changed) counts as gone."""
    private = keys(config)
    found = (post or _post)('/pair-pickup', pickup_body(private, request_id, clock))
    state = found.get('state')
    if state != 'paired':
        return {'state': 'waiting' if state == 'waiting' else 'gone'}
    try:
        body = nc.open_box(found.get('sealed'), private, {'p': 'pair', 'r': request_id}, info=BOX_INFO)
    except nc.SealError:
        LOG.warning('pairing token not opened')
        return {'state': 'gone'}
    token = body.get('token') if isinstance(body, dict) else None
    if not isinstance(token, str) or not re.fullmatch(r'[A-Za-z0-9_.~-]{16,200}', token):
        return {'state': 'gone'}
    return {'state': 'paired', 'token': token, 'label': str(body.get('label') or found.get('label') or '')[:80],
            'device': str(body.get('device') or found.get('device') or '')[:80]}


def keep(config, config_path, token):
    """The token into <database folder>/fleet-token (0600) and the saved config's `fleet` credential, as cmd_fleet_pair
    does; the running config too, so the Fleet can start now. Returns the token file's path."""
    path = Path(config['database']).expanduser().parent / TOKEN_FILE
    onboarding.write_private(path, token + '\n')
    if config_path:
        saved = onboarding.load(config_path)
        saved.pop('fleet_relay_url', None)
        saved.setdefault('credentials', {})['fleet'] = str(path)
        onboarding.save(config_path, saved)
    config.setdefault('credentials', {})['fleet'] = str(path)
    return path


def forget(config, config_path):
    """Unpair here: the `fleet` credential out of the saved and the running config, and its token file gone."""
    found = (config.get('credentials') or {}).pop('fleet', None)
    if config_path:
        saved = onboarding.load(config_path)
        (saved.get('credentials') or {}).pop('fleet', None)
        onboarding.save(config_path, saved)
    if isinstance(found, str) and Path(found).expanduser().name == TOKEN_FILE:
        Path(found).expanduser().unlink(missing_ok=True)
