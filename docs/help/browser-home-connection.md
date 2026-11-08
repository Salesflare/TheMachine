---
title: Your browser's home connection
area: troubleshooting
summary: Let your hosted Machine's browser go out through your home internet with Tailscale, so sites accept its sign-ins.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
---
Some sites, like LinkedIn, X and sites behind a Cloudflare check, refuse sign-ins from a browser in the cloud. Your setup page can send your hosted Machine's browser out through your home internet instead, with Tailscale. It's free, takes about 10 minutes, and most of it happens by itself.

## Set it up

1. On your setup page, under your Machine's browser, pick **Tailscale** and press **Sign in to Tailscale**. Sign in, or make a free account there.
2. Install Tailscale on a computer at home that stays on, and sign in there with the same account. Not a phone: it sleeps.
3. Make that computer an exit node. The setup page shows the menu for its system. On Linux, run `sudo tailscale set --advertise-exit-node`.
4. Press **Open it in Tailscale** and allow it: Machine settings, Edit route settings, Use as exit node, Save. In the same menu, choose Disable key expiry.

The setup page ticks off each step by itself. With one exit node, your browser starts using it right away. With more, pick one and press **Use this exit node**.

## Check it

Press **Test it**. The page shows where the web sees your browser: your city and internet provider.

## When your home computer is off

Your browser then goes out directly from your Machine, and back through your home once the computer is on again. Signed out of Tailscale? Press **Sign in again**. Tailscale signs devices out after 6 months unless key expiry is off. The setup page shows the date.

## Stop using it

Press **Stop using it** to go directly again. **Sign it out of Tailscale too** also signs your Machine's browser out of Tailscale. Tailscale's admin console then lists it as Expired, and you can remove it there.
