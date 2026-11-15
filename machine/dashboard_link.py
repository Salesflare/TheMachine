"""The dashboard's own https address, for links in messages, pushes and pages: one place builds it from `dashboard_host`
and `dashboard_path` (a leaf)."""

LAYER = 0  # the dashboard's own address for links (a leaf)


def dashboard_link(config, fragment=''):
    """https://<dashboard_host><dashboard_path><fragment>, as the config spells them ('#card=...' for a fragment), or ''
    when the Machine has no dashboard_host (only reachable on this computer). An empty or missing dashboard_path is /."""
    host = str((config or {}).get('dashboard_host') or '')
    if not host:
        return ''
    return 'https://' + host + str(config.get('dashboard_path') or '/') + fragment


def dashboard_address(config):
    """The dashboard's own address tidied up: the host trimmed and in lower case, the path with one / on each side
    (https://machine.example/assistant/); None when it has no dashboard_host."""
    host = str((config or {}).get('dashboard_host') or '').strip().lower()
    if not host:
        return None
    return f"https://{host}/{str(config.get('dashboard_path') or '/').strip('/')}".rstrip('/') + '/'
