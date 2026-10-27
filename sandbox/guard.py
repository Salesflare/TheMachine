"""The sandbox's seal: once installed, this process can't reach anything but its own machine and can't start any
program. No email, Telegram, Slack, WhatsApp or X send can leave, whatever code path tries, because Python's audit hooks
refuse the connection or the process before it happens (they can't be removed again)."""
import sys

LOCAL = ('127.0.0.1', '::1', 'localhost')
BROWSER_PORTS = (9222, 9333)  # the DevTools of a browser on this computer, someone's own: never from the sandbox
BLOCKED = []  # what was refused, for the sandbox's own log and tests


def _local(host):
    return isinstance(host, str) and (host in LOCAL or host.startswith('127.'))


def _refuse(kind, target, why):
    BLOCKED.append((kind, target))
    print(f'sandbox: refused {kind} {target}', file=sys.stderr, flush=True)
    raise PermissionError('sandbox: ' + why)


def _hook(event, args):
    if event == 'socket.connect':
        address = args[1]
        if isinstance(address, tuple) and not _local(address[0]):
            _refuse('connect', str(address[0]), 'no network beyond this machine')
        if isinstance(address, tuple) and len(address) > 1 and address[1] in BROWSER_PORTS:
            _refuse('connect', f'browser port {address[1]}', 'not the browser on this computer')
        if isinstance(address, (str, bytes)):  # a local socket file: D-Bus, Tailscale, the Gateway
            _refuse('socket', 'unix', 'no local services')
    elif event == 'socket.getaddrinfo':
        if not _local(args[0]) and args[0] is not None:
            _refuse('dns', str(args[0]), 'no name lookups')
    elif event in ('subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty'):
        _refuse('process', str(args[0]).rsplit('/', 1)[-1] if args and event == 'subprocess.Popen' else event, 'no programs')


_installed = False


def install():
    global _installed
    if not _installed:
        sys.addaudithook(_hook)
        _installed = True
