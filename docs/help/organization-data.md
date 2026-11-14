---
title: Organization details
area: graph
summary: Industry, size, location and a logo next to each organization, looked up by its web address.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
---
## Where they come from

- On a hosted Machine, organization details are looked up for you, at no cost.
- On your own computer, it's off until you add a key for a look-up service, like Apollo, People Data Labs or Hunter. See the [configuration guide](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Only an organization's web address is sent, never your messages or who you know there. A hosted Machine, or one on The Machine Network, looks up to 1,000 a day; otherwise up to 50. Each is refreshed every 90 days. Shared sites and mail providers, like gmail.com, are never looked up. People have their own look-up: see [Job title and photo](people.md#job-title-and-photo).

Without a logo from the look-up, The Machine uses the icon from the organization's own website, saved on your Machine. No logo service learns who you deal with. When it has both, small spots like a to-do's line show the square icon.

When the look-up has them, up to 5 of the organization's specialties show under its description, and the Organizations list can be filtered by one: **Filter**, then **Specialty**. When a person's look-up brings their company's details along, those fill in the organization too, so it needs no look-up of its own. Details looked up in the last 90 days stay as they are.

## Fix a wrong one

On the organization's page:

- **Edit** to change the name, industry, size, location, founding year, description, website, LinkedIn, notes and what it is to you. Your edits stay. Empty a field to use the looked-up value again.
- **Wrong company, clear details**, in **Edit**, if it picked the wrong company.
- **Look it up again**, shown once they're cleared, fetches fresh details.
