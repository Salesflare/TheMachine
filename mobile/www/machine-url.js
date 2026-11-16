// Which addresses the app opens as "your Machine", in one place for the connect screen, the injected script and the
// tests (mobile/tests). The native side (MachineShellPlugin) checks the same rules again before it saves or loads one.
//  - hosted: https://<name>.app.themachine.computer/ (reached through the account's sign-in, never typed)
//  - self-hosted: https://<machine>.<tailnet>.ts.net[/path/] on the owner's Tailscale network, or the dashboard's own
//    https domain (https://my.example.com[/path/]), on 443 or 8443. Before one is saved the app asks it for its
//    manifest (isMachine), so a typo or another site is told apart from a Machine.
(function (root) {
  'use strict';
  const HOSTED = 'app.themachine.computer';
  const LABEL = /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/;

  function labels(host) {
    const parts = host.split('.');
    return parts.every(p => LABEL.test(p)) ? parts : null;
  }

  function hostedHost(host) {
    if (!host.endsWith('.' + HOSTED)) return false;
    const name = host.slice(0, -HOSTED.length - 1);
    return !name.includes('.') && LABEL.test(name);
  }

  const OWN_PORT = '8443';

  function tailnetHost(host) {
    const parts = labels(host);
    return !!parts && parts.length >= 4 && host.endsWith('.ts.net');
  }

  // A self-hosted Machine's host: a tailnet name, or a public DNS name (two labels or more, a top level of letters,
  // so never an IP address or a bare name like localhost). Never a hosted Machine's: those come through sign-in.
  function ownHost(host) {
    if (host.endsWith('.ts.net')) return tailnetHost(host);
    const parts = host.length <= 253 && labels(host);
    return !!parts && parts.length >= 2 && /^[a-z]{2,63}$/.test(parts[parts.length - 1]) &&
      host !== HOSTED && !host.endsWith('.' + HOSTED);
  }

  // Whether what an address answered for <address>manifest.webmanifest is a Machine's dashboard: its manifest, or
  // (someone not its owner on that tailnet) the dashboard's own refusal. Anything else is another site.
  function isMachine(status, body) {
    let data;
    try { data = JSON.parse(String(body || '')); } catch (e) { return false; }
    if (!data || typeof data !== 'object') return false;
    if (status === 200) return data.name === 'The Machine' && typeof data.start_url === 'string' && Array.isArray(data.icons);
    if (status === 403) return data.error === 'Use the owner-authenticated Tailscale dashboard';
    return false;
  }

  // What the owner typed (or a scanned link carried) as a Machine address, or null with the reason.
  // Returns {url, kind: 'hosted'|'own'} or {error: 'address'}.
  function parse(input) {
    let text = String(input || '').trim();
    if (!text) return {error: 'address'};
    if (!/^[a-z][a-z0-9+.-]*:\/\//i.test(text)) text = 'https://' + text;
    let url;
    try { url = new URL(text); } catch (e) { return {error: 'address'}; }
    // https on 443 (the URL parser drops it) or 8443, a self-hosted Machine's default port; no other port.
    if (url.protocol !== 'https:' || url.username || url.password || (url.port && url.port !== OWN_PORT)) return {error: 'address'};
    const host = url.hostname.toLowerCase();
    if (host === HOSTED || hostedHost(host)) return url.port ? {error: 'address'} : {url: 'https://' + HOSTED + '/', kind: 'hosted'};
    if (!ownHost(host)) return {error: 'address'};
    let path = url.pathname || '/';
    if (!path.endsWith('/')) path += '/';
    if (!/^\/(?:[A-Za-z0-9._~-]+\/)*$/.test(path)) return {error: 'address'};
    return {url: 'https://' + host + (url.port ? ':' + url.port : '') + path, kind: 'own'};
  }

  // Whether a saved Machine URL may be opened: the same rules, and already in its normal form.
  function valid(saved) {
    if (typeof saved !== 'string') return false;
    try {
      const host = new URL(saved).hostname;
      if (hostedHost(host)) return saved === 'https://' + host + '/';
    } catch (e) { return false; }
    const parsed = parse(saved);
    return parsed.kind === 'own' && parsed.url === saved;
  }

  // The dashboard address an app sign-in came back with (computer.themachine.app://signed-in?u=...): only a hosted
  // Machine's own /_machine/auth with a handoff token, nothing else.
  function signinTarget(u) {
    let url;
    try { url = new URL(String(u || '')); } catch (e) { return null; }
    if (url.protocol !== 'https:' || url.port || url.username || !hostedHost(url.hostname)) return null;
    if (url.pathname !== '/_machine/auth' || !/^[A-Za-z0-9_-]{20,100}$/.test(url.searchParams.get('t') || '')) return null;
    return {auth: url.href, machine: 'https://' + url.hostname + '/'};
  }

  // A connection's sign-in the Machine's page starts ("Sign in with Shortcut"): the hosted dashboard's hop to the account
  // (/hop?t=...&app=1, which the account gives the app's WebView only) or a self-hosted Machine's start link
  // (/connect/start/<id>). The address to open in the system's sign-in sheet, with app=1, or null for anything else
  // (the account's other pages keep opening in the phone's browser).
  function connectionStart(u) {
    let url;
    try { url = new URL(String(u || '')); } catch (e) { return null; }
    if (url.protocol !== 'https:' || url.hostname !== HOSTED || url.port || url.username || url.password) return null;
    const t = url.searchParams.get('t') || '';
    if (url.pathname === '/hop' && url.search === '?t=' + t + '&app=1' && /^[A-Za-z0-9_-]{20,100}$/.test(t)) return url.href;
    if (/^\/connect\/start\/[A-Za-z0-9_-]{32}$/.test(url.pathname) && !url.search) return url.href + '?app=1';
    return null;
  }

  // Where such a sign-in ends (computer.themachine.app://connected?h=...): the part of the saved Machine's dashboard to
  // open, + Add's form (connect=<source>[/<ref>|/stopped]) or "connected" (signed-in=<source>[/again]); null otherwise.
  const PART = /^(?:connect=[a-z_]{1,32}(?:\/(?:[cf]_[0-9a-f]{16}|stopped))?|signed-in=[a-z_]{1,32}(?:\/again)?)$/;
  function connectedPart(h) {
    return typeof h === 'string' && PART.test(h) ? h : null;
  }

  const api = {HOSTED, parse, valid, signinTarget, connectionStart, connectedPart, hostedHost, tailnetHost, ownHost, isMachine};
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.MachineUrl = api;
})(typeof self !== 'undefined' ? self : this);
