---
title: Browse through your desktop app
area: troubleshooting
summary: Let your hosted Machine's browser go out through the computer the desktop app runs on, so sites see your own internet.
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
---
Some sites, like LinkedIn, refuse sign-ins from a browser in the cloud. With the [desktop app](desktop-app.md) signed in, your hosted Machine's browser can go out through that computer instead. Sites then see your home or office internet, not a data center.

## Turn it on

It's on by default once your Machine has it. In the desktop app's Settings, the switch is Let my Machine browse through this computer. Turn it off and your Machine's browser goes out directly again, right away.

While your Machine's browser is using it, the robot's box and the app's icon in the menu bar or taskbar say Your Machine is browsing through this computer.

## What goes through it

Only your Machine's browser, to websites: ports 80 and 443 on public internet addresses. The app never connects to this computer itself, your home or office network, or other private addresses, and it opens no port on your computer. It keeps to 4 MB/s down, 1 MB/s up and 2 GB a day.

## When the computer is off

Your Machine's browser goes out directly from your Machine, and back through the computer once the app runs again.
