---
title: The Graph
area: graph
summary: The people, organizations and projects in your messages, kept up to date by themselves.
covers: tab:people
code: graph.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
---
Your Machine builds a map of who you deal with and what's going on, from your messages, meetings and decisions. Nothing to set up, and it stays on your Machine.

- [People](people.md): everyone you're in touch with, with a summary and timeline for each.
- [Organizations](organizations.md): the companies they work at, with their people and projects.
- [Projects](projects.md): what's going on, on boards with stages, like deals in a CRM.

## Filter and sort

**Filter**, next to the tabs, narrows the list. Each list has its own filters. People: closeness, last contact, organization, owner, tag and **Has an open project**. Organizations: industry, size, country, last contact, owner, tag and **Has an open project**. Projects: owner, board, stage, tag, organization, value, expected close date and **No reply in 10+ days**.

The filters you picked show above the list, with **Clear**. On Projects, the list and the board share one Filter. On a phone they open as a sheet.

The order menu sorts the list, also by **Value** and **Close date**. **Download CSV**, under the order menu, saves the tab you're on as a spreadsheet.

## Fields and tags

Under Fields on a person, organization or project, click a value to change it: **Save** or Enter keeps it, **Cancel** or Escape leaves it, **Remove** empties it.

**Manage fields** adds or removes fields for all records of that kind. **New field** adds one: text, number, date or a choice from a list.

**+ Tag** adds a tag, like VIP or partner; **×** takes it off. Tags show in the lists and **Filter** finds them.

## Birthday

A person's birthday shows under Contact, with where it came from: their Google contact, a birthday on Google Calendar (the Birthdays routine saves it for a close contact), a Facebook import, or you. **Edit** sets or corrects it: a month and a day, and the year if you know it (then their age shows too). Yours wins over every source and stays. **Remove** takes it off; a contact or an import doesn't bring it back.

Without one, **Add birthday** under Fields adds it. The Birthdays routine reads the same birthday the page shows. A birthday is personal: it never goes to your team, also on a shared record.

## Import a spreadsheet

**Import CSV…**, under the order menu of People, Organizations or Projects, adds a spreadsheet saved as CSV.

1. Check the columns. Your Machine guesses which is which from the headers and what's in them; change any of them. When your model can run, it checks them too, with a short reason where it isn't sure. It sees only the headers, a few values per column and the cells the rules couldn't read.
2. Check the fixes. **Review** lists them as before and after: extra spaces, names in capitals, phone numbers in international form, email typos (gmial.com), websites as their domain, dates and values in any format ("€12k" is 12000), several tags in one cell, a stage spelled differently and the same row twice. Untick a kind or a row to leave it as it is.
3. Check the preview. Each row is new, matches one already in your Graph, or is skipped, with why. A person matches on email (else name and organization), an organization on website or name, a project on name.
4. **Import** adds the new ones and fills in the matches. An empty cell changes nothing.

**Undo** right after, or **Undo last import** under the order menu, takes the last import back while those records haven't changed since. If it would overwrite a later correction, it says why instead. The file stays on your Machine.

## Owner

In a Work Fleet, each person, organization and project has an owner: **Owner** under With you on its page. It's you, unless you pick someone from your Work Fleet. **Owner** in Filter shows only yours. Each change shows in its timeline.

## Team

**Team**, next to Mine, shows what your teammates share, with the same tabs and order menu. **Filter** narrows it by who shared it, an organization (People) or state (Projects). What you add there is yours.

Client work is shared with your teammates' Machines, with its owner, fields and tags, and theirs shows in yours. Each thread shows **Team** or **Only you**. See [Team Graph](team-graph.md).
