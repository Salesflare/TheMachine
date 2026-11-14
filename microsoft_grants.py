"""Microsoft sign-ins delivered to a paired self-hosted Machine for Docs or Teams (onboarding.connect_delivered).

Each comes from its own consent through the control plane, sealed for this Machine. With Outlook for that address
signed in the same way (onboarding.connect_grant), it replaces that one's sign-in kept here (mail_grants.py), which then
also reads files or chats; without it, it is a sign-in of its own (own_grant) and no Outlook account comes with it. The
new connection is checked with a real read before it is saved; when that does not check out, the sign-in kept before
comes back and nothing is added.

`ob` is the onboarding module its caller already loaded (as in google_pair.py)."""
import datetime as dt
import re


def docs(ob, config_path, args):
    """Docs for a Microsoft account: {source: microsoft_docs or microsoft_docs_write, grant: {provider, email,
    refresh_token, scopes}}, a sign-in that reads and edits files (Files.ReadWrite.All; Files.Read.All for a connection
    from before). microsoft_docs_write (Allow edits) without Files.ReadWrite.All granted is refused: it never says
    Connected for edits it can't make. Returns {'ok', 'name'}."""
    config, email, refresh, scopes, mail = _grant(ob, config_path, args)
    if args.get('source') == 'microsoft_docs_write' and scopes is not None and 'Files.ReadWrite.All' not in scopes:
        raise ob.SetupError("Microsoft didn't allow edits", 'press Allow edits again and accept')

    def fresh():
        same = [a for a in config.get('accounts', []) if str(a.get('email', '')).lower() == email and a.get('boundary')]
        boundary = (mail or {}).get('boundary') or (same[0]['boundary'] if same else ob.boundary_label(ob.company_of(email) or 'personal'))
        return boundary, ob.new_account(config, 'docs', ui=ob.AnswersUI({'part of your life': boundary, 'company': boundary}))

    def failed(error):
        return f"Docs for {email} didn't check out ({error})"
    return _add(ob, config_path, config, email, refresh, mail, 'docs', fresh, failed, {'provider': 'microsoft'})


def teams(ob, config_path, args):
    """Microsoft Teams for a work account: {source: microsoft_teams, grant: {provider, email, refresh_token, scopes}},
    the sign-in from Teams' own consent (Chat.Read, the hosted one's scopes). Work: that address's mail's, else its
    company, as on a hosted Machine. Returns {'ok', 'name'}."""
    config, email, refresh, scopes, mail = _grant(ob, config_path, args)
    if scopes is not None and 'Chat.Read' not in scopes:
        raise ob.SetupError("Microsoft didn't allow reading Teams chats", 'sign in again from Connections, + Add and accept')

    def fresh():
        boundary = (mail or {}).get('boundary') or ob.boundary_label(ob.company_of(email) or 'work')
        return boundary, ob.new_account(config, 'teams', ui=ob.AnswersUI({'part of your life': boundary, 'company': boundary, 'address': email}))

    def failed(error):
        return 'Teams needs a work or school Microsoft account' if 'teams_work_only' in error else f"Teams for {email} didn't check out ({error})"
    return _add(ob, config_path, config, email, refresh, mail, 'teams', fresh, failed, {})


def _grant(ob, config_path, args):
    """(config, email, refresh token, scopes or None, its Outlook account signed in the same way or None), or
    SetupError."""
    import fleet  # on first use, as onboarding does
    grant =args.get('grant') if isinstance(args.get('grant'), dict) else {}
    email = str(grant.get('email') or '').strip().lower()
    refresh = grant.get('refresh_token')
    if (grant.get('provider') != 'microsoft' or not re.fullmatch(r'[^@\s]{1,200}@[^@\s]{1,200}\.[^@\s]{2,63}', email)
            or not isinstance(refresh, str) or not 8 <= len(refresh) <= 4096):
        raise ob.SetupError('No Microsoft sign-in came with it', 'sign in again from Connections, + Add')
    config = ob.load(config_path)
    home = fleet.settings(config)
    if not home or not (config.get('credentials') or {}).get('fleet') or config.get('manage_url'):
        raise ob.SetupError('Only a paired self-hosted Machine signs in this way', 'pair this Machine first')
    scopes = grant.get('scopes') if isinstance(grant.get('scopes'), list) else None
    url = home['url'].rstrip('/') + '/microsoft-token'
    paired = (config.get('microsoft_broker') or {}).get('url') == url
    # its Outlook signed in the same way, so the new sign-in refreshes at the same place
    mail = next((a for a in config.get('accounts', []) if a.get('service') in ob.GRANT_SERVICES['microsoft'] and a.get('transport') == 'broker'
                 and str(a.get('email', '')).lower() == email), None) if paired else None
    if not mail:  # Docs or Teams alone: the same broker as Outlook's would use, and no Outlook account
        if (config.get('microsoft_broker') or {}).get('url') not in (None, url):
            raise ob.SetupError('This Machine gets Microsoft access from another place', 'disconnect those Microsoft accounts first')
        config['microsoft_broker'] = {'url': url}
        config.setdefault('credentials', {})['microsoft-broker'] = config['credentials']['fleet']  # its own device token
    return config, email, refresh, scopes, mail


def _add(ob, config_path, config, email, refresh, mail, service, fresh, failed, more):
    """Keeps the new sign-in in place of the one before, then adds or updates that address's `service` connection
    (fresh(): (boundary, new account)) and checks it; failed(error) says why it didn't check out. On any failure the
    sign-in kept before comes back."""
    import timeutil
    import mail_grants
    try:
        previous = mail_grants.get(config, 'microsoft', email)
    except mail_grants.GrantError:
        raise ob.SetupError("This Machine can't keep sign-ins yet", 'try again in a minute') from None
    mail_grants.put(config, 'microsoft', email, refresh)
    try:
        account = next((a for a in config.get('accounts', []) if a.get('service') == service and str(a.get('email', '')).lower() == email), None)
        if account is None:
            boundary, account = fresh()
            account['boundary'], account['boundary_by'] = boundary, (mail or {}).get('boundary_by') or 'guess'
        account = {**account, **more, 'email': email, 'transport': 'broker',
                   'connected_at': timeutil.clock().strftime('%Y-%m-%dT%H:%M:%S+00:00')}
        if mail:
            account.pop('own_grant', None)  # Outlook's sign-in, which now also reads files or chats
        else:
            account['own_grant'] = True  # its own sign-in (connectors/docs.py, connectors/teams.py signin)
        error = ob.check(config, account)
        if error and not error.startswith(ob.BUSY):
            raise ob.SetupError(failed(error), 'sign in again from Connections, + Add')
        known = any(a.get('id') == account['id'] for a in config.get('accounts', []))
        config['accounts'] = [account if a.get('id') == account['id'] else a for a in config.get('accounts', [])] + ([] if known else [account])
        ob.save(config_path, config)
    except BaseException:
        if previous:
            mail_grants.put(config, 'microsoft', email, previous)
        else:
            mail_grants.forget(config, 'microsoft', email, revoke=False)
        raise
    return {'ok': True, 'name': email}
