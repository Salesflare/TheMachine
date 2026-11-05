"""Which way a confirmed GitHub step (an issue, a comment, a label) runs: GitHub's own gh tool when it is signed in on
this Machine, else a GitHub MCP server set up in OpenClaw, and the Machine's browser only when neither is there.

The preparation is told which one (prompt), the final step keeps it (`via`, set here, never by the model), the to-do
says it, and the confirmed run is held to it (finish_rule). Nothing here writes to GitHub: the owner's Confirm still
runs the step, as for any other final step. GitHub's API takes no image uploads, so screenshots go in through the
issue form in the browser even when gh files the issue.
"""
import json
import shutil
import subprocess
import time
from pathlib import Path
from urllib.parse import urlsplit

HOSTS = ('github.com', 'www.github.com')
WAYS = ('gh', 'mcp', 'browser')
CACHE_SECONDS = 600
_cache = {}


def targets_github(action):
    """A final step that happens on GitHub: its page is on github.com."""
    try:
        return action.get('kind') == 'finish' and (urlsplit(action.get('url') or '').hostname or '').lower() in HOSTS
    except ValueError:
        return False


def _gh_login(config, run):
    """The login of The Machine's GitHub connection (Connections, GitHub: gh signed in on this Machine), while gh is
    still signed in. Without that connection gh is never asked."""
    account = next((a for a in config.get('accounts') or () if a.get('service') == 'github' and a.get('transport', 'gh') == 'gh'
                    and a.get('enabled', True) is not False), None)
    gh = account and shutil.which(config.get('gh') or 'gh')
    if not gh:
        return None
    try:
        if run([gh, 'auth', 'status', '--hostname', 'github.com'], capture_output=True, text=True, timeout=20).returncode:
            return None
    except (OSError, subprocess.SubprocessError):
        return None
    login = str(account.get('login') or '').strip()
    return login if login and len(login) <= 39 and '\n' not in login else 'gh'


def _mcp_name(config):
    """The name of a GitHub MCP server in OpenClaw's config (mcp.servers), if there is one."""
    path = Path(config.get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json').expanduser()
    try:
        servers = (json.loads(path.read_text(encoding='utf-8')).get('mcp') or {}).get('servers') or {}
    except (OSError, ValueError, AttributeError):
        return None
    if not isinstance(servers, dict):
        return None
    for name, server in servers.items():
        if isinstance(server, dict) and server.get('enabled', True) is not False and 'github' in (
                str(name) + ' ' + str(server.get('command') or '') + ' ' + ' '.join(map(str, server.get('args') or ())) + ' ' + str(server.get('url') or '')).lower():
            return str(name)[:60]
    return None


def access(config, run=subprocess.run, clock=time.monotonic):
    """{'gh': the signed-in login or None, 'mcp': a GitHub MCP server's name or None}, checked at most every 10 minutes."""
    key = (config.get('gh') or 'gh', str(config.get('openclaw_config') or ''),
           tuple(str(a.get('login')) for a in config.get('accounts') or () if a.get('service') == 'github'))
    hit = _cache.get(key)
    if hit and clock() - hit[0] < CACHE_SECONDS:
        return dict(hit[1])
    found = {'gh': _gh_login(config, run), 'mcp': _mcp_name(config)}
    _cache[key] = (clock(), found)
    return dict(found)


def way(found):
    return 'gh' if found.get('gh') else 'mcp' if found.get('mcp') else 'browser'


def route(action, config, run=subprocess.run):
    """A final step on GitHub with its way set: via, and via_login for gh. Others come back as they were."""
    action = {k: v for k, v in action.items() if k not in ('via', 'via_login')}
    if not targets_github(action):
        return action
    found = access(config, run)
    action['via'] = way(found)
    if action['via'] == 'gh':
        action['via_login'] = found['gh']
    return action


def prompt(config, run=subprocess.run):
    """The preparation's line about GitHub writes, when gh or a GitHub MCP server is there."""
    found = access(config, run)
    if found['gh']:
        how = (f"GitHub's gh tool is signed in here as {found['gh']}: a GitHub write (an issue, a comment, labels) runs with gh, "
               "never in the browser: `gh issue create --repo <owner/repo> --title <title> --body-file <file> --label <label>`. "
               "GitHub's API takes no image uploads, so for screenshots open the repository's new-issue page in the browser, "
               "drop each file into the description only to get its link, don't submit there, and put those links in the body gh files")
    elif found['mcp']:
        how = (f"The GitHub MCP server {found['mcp']} is set up here: a GitHub write (an issue, a comment, labels) runs with its "
               "tools, never in the browser. Screenshots go in through the new-issue page in the browser, only to get their links")
    else:
        return ''  # the browser, as for any page; the to-do says GitHub isn't connected and how to connect it
    return ("\n- " + how + ". Offer it as the usual final step, {kind:'finish',url:<its github.com page>,...}: the service "
            "records which way it runs and the to-do shows it; nothing is filed before the owner's Confirm.")


def finish_rule(action):
    """The confirmed run's line: the way the owner saw on the to-do."""
    if not targets_github(action) or action.get('via') not in WAYS:
        return ''
    if action['via'] == 'gh':
        files = (" GitHub's API takes no image uploads: put the attached files into the new-issue page's description in "
                 "the browser only to get their links (don't submit there), then file with gh with those links in the body."
                 ) if action.get('attachments') else ''
        return (f"\nRun this step with GitHub's gh tool, signed in as {action.get('via_login') or 'the owner'}, not in the browser "
                f"(e.g. `gh issue create --repo <owner/repo> --title ... --body-file ... --label ...`), and check the result "
                f"with `gh issue view`.{files} If gh turns out signed out, don't switch to the browser: record a blocker saying GitHub's gh "
                f"tool is signed out on this Machine and that adding GitHub again in Connections signs it in.")
    if action['via'] == 'mcp':
        return "\nRun this step with the GitHub MCP server's tools, not in the browser; the attached files only through the new-issue page, for their links."
    return "\nNothing GitHub is connected on this Machine, so this step runs in the browser, as the owner saw on the to-do."
