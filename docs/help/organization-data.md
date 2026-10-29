---
title: Organization details
area: graph
summary: Industry, size, location and a logo next to each organization, looked up by its web address.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 2
---
## Where they come from

- On a hosted Machine, organization details are looked up for you, at no cost.
- On your own computer, it's off until you add a key for a look-up service you use, like Apollo, People Data Labs or Hunter. See the [configuration guide](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Only an organization's web address is sent, never your messages or who you know there. A few are looked up at a time, at most 50 a day, and refreshed every 90 days. People get their own look-up: see [Job title and photo](graph.md#job-title-and-photo). Shared hosts and mail providers, like google.com, sites.google.com or gmail.com, are never looked up: they're no one company's website.

When the look-up has no logo, or there's no look-up, the logo comes from the organization's own website: the icon its home page names. It's saved on your Machine, so no logo service learns who you deal with. A site without one is asked again after 30 days. A look-up that found the organization but no logo is asked once more after a week, and a logo it brings then replaces the site's icon.

## Fix a wrong one

On the organization's page:

- **Edit** to change the name, industry, size, location, founding year, description, website, LinkedIn and what it is to you. Your edits stay. Empty a field to use the looked-up value again.
- **Wrong company, clear details** if it picked the wrong company.
- **Look it up again** to fetch fresh details.
