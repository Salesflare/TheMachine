# GBrain

[GBrain](https://github.com/garrytan/gbrain) is an open-source agent memory (MIT) that many OpenClaw users run. The Machine works with it as an optional add-on: off by default, no cost or background work when off.

## Turning it on

On a self-hosted Machine: **Connections**, **+ Add**, **GBrain**.

1. Install GBrain if it isn't there yet: `bun install -g github:garrytan/gbrain`. The Machine finds `gbrain` from `gbrain.bin` in `config.json`, `GBRAIN_BIN`, `~/.bun/bin/gbrain` or `PATH`.
2. Read the consent step and check **I agree**. Nothing goes into GBrain before that.
3. **Connect GBrain**. The Machine adds GBrain to OpenClaw as an MCP server (`openclaw mcp add gbrain ... serve`) with only its read tools. When GBrain is already set up in OpenClaw (as an MCP server or its OpenClaw plugin), The Machine uses that one and never changes or removes it.

Settings live under `gbrain` in `config.json`: `on`, `consent_at`, `work`, `linked` (`machine` or `existing`) and `bin`.

## What reviews may use

With GBrain on, inbox reviews may also call GBrain's read tools: `search`, `query`, `get_page`, `list_pages`, `get_links`, `get_backlinks`, `get_timeline`, `get_tags`, `whois`, `recall`, `resolve_slugs` and `get_brain_identity`. Never a tool that writes or deletes. Off, the review tool list is exactly as before.

## Sync

Every 30 minutes, through the `gbrain` CLI:

- **Out**: people (closeness 0.3 or more, or added by hand), projects and companies from the Graph, and learnings (`the-machine/learnings`). Each page gets one section between `<!-- the-machine:start -->` and `<!-- the-machine:end -->`, with a link back to the Graph. The Machine finds existing pages by email or name first. Unchanged records cost no calls. Writes use GBrain's revision check, so a page edited at the same time is retried, not overwritten.
- **Owner edits win**: when the owner edits or removes The Machine's section, it's left as they made it. A deleted page stays deleted.
- **In**: the owner's own text on those pages (outside The Machine's section) shows next to that person in the Graph and in reviews, as data.
- **Never**: message bodies, sealed content, owner-only notes on projects, or Team Graph data from teammates. Work people, companies and work projects go out only with `work` on. When a record no longer qualifies, its section is taken out.

## Turning it off

**Turn off** keeps the brain and every page. It removes the OpenClaw MCP entry only if The Machine added it, and forgets the notes it pulled in.
