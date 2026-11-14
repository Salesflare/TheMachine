---
title: Watched web pages
area: connections
summary: A web page you watch. A to-do only when something that matters on it changes.
covers: connector:web_page
code: connectors/web_page.py
---
## What it reads

The text of one public web page per connection, every few hours and at most once an hour. Menus, footers, cookie notices and ads are left out. When the text changed, The Machine looks at what changed and makes a to-do only when it matters, like a new price or a changed policy. Dates, counters and small rewording never make a to-do. An unchanged page costs nothing.

It asks the site's robots.txt first and leaves the page alone when the site says no. Pages behind a sign-in or built only with JavaScript can't be watched.

## What it can do

Nothing. It only reads the page.

## Connect it

1. In the dashboard, open **Connections**, then **Other**, and pick Web page. Or run `assistant connect web_page`.
2. Paste the page's address.

Or ask in your chat: "Watch this page for price changes" with its address. Ask it which pages you watch, or to stop watching one.

## Remove it

In the dashboard: **Connections**, open the page, **Details**, then **Disconnect**. Or ask your chat to stop watching it.
