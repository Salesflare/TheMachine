---
title: RSS feeds
area: connections
summary: Posts from an RSS or Atom feed you follow.
covers: connector:rss
code: connectors/rss.py
site: More sources
---
## What it reads

New posts from one RSS or Atom feed per connection. Add it again for each feed.

It reads the feed every 30 minutes, and never more often than every 15 minutes. It only reads public https:// addresses.

## What it can do

Nothing. It only reads the feed.

## Connect it

1. In the dashboard, open **Connections**, then **Other**, and pick RSS feed. On a hosted Machine, the setup page has it too, under **More sources**. On your own computer, you can also run `assistant connect rss`.
2. Paste the feed's address.

## Remove it

In the dashboard: **Connections**, open the feed, **Details**, then **Disconnect**. There is nothing to uninstall anywhere else.
