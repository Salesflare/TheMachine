---
title: Signed out of a site
area: troubleshooting
summary: LinkedIn or X signed your Machine out. Sign it back in, once or for good.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
---
Sites like LinkedIn and X are read in your Machine's own browser. Sometimes a site signs it out.

## Sign back in

**Connections** and the top of your To-dos say it's signed out. Press **Sign in again** and sign in, in a small window on the dashboard.

Tick **Save for next time** to sign back in with one tap when it happens again. The password stays encrypted on your Machine, and the AI never sees it.

## Passwords and codes

Type passwords yourself. Two-step codes are yours to enter too.

Saved sign-ins are under **Connections**, **Sign-ins**. **Forget** removes one.

## If the site refuses or wants a robot check

LinkedIn, X and sites behind a Cloudflare check often refuse sign-ins from a browser in the cloud. On a hosted Machine, the sign-in then shows **Sign in from your home connection**. It opens your setup page, where your Machine's browser can go out through your home internet with Tailscale, or through your own proxy. Then sign in again.

On your own computer you don't need this: its browser is already at home.
