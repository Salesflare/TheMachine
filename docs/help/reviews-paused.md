---
title: No new to-dos
area: troubleshooting
summary: Reviews are off, waiting, or stopped on your model's usage limit. How to tell and what to do.
covers: 
code: dashboard.html, assistant.py
order: 3
---
To-dos come from reviews: your Machine reads what came in, in small batches, within about an hour.

## Reviews are off

The top of Suggestions says "Reviews are off, so no suggestions arrive yet." On a hosted Machine, press **Turn on reviews**. On your own computer, run `./install.sh --activate`.

## Your model's limit

Reviews of what came in pause at about 65% of your plan's 5-hour limit and at 90% of its weekly limit, to keep room for your own chats. A board's look through your history goes slower, at about a seventh of the week a day.

While reviews wait, the top of the dashboard says until when, like "Reviews wait until 07:15 to save your ChatGPT week." **Review now** starts one right away. When a limit is reached, the top of the dashboard says which one and when it resets. **Connections**, then **Reviews**, shows it next to the run. **Settings**, **Model** shows your limits. See [Model](model.md).

Nothing is lost while it waits: what came in is reviewed once it can.

## A run failed

**Recent runs** under **Reviews** shows each run. A failed batch is tried again by itself.
