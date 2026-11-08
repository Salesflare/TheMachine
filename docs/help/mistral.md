---
title: Mistral
area: connections
summary: Run your Machine on Mistral's models with an API key from Mistral. Le Chat Pro includes API credits.
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key
---
## What it is for

Mistral is a European AI provider. With a Mistral API key, your Machine reads and drafts with Mistral's models. The Machine has no AI of its own: requests go straight to Mistral, under your account and their terms.

## Get a key

Mistral has no sign-in for other apps, so it works with an API key. In the [Mistral console](https://console.mistral.ai/), open API keys and create one. Le Chat Pro includes monthly API credits; after those, Mistral bills per use.

## Connect it

On a hosted Machine, open your setup page, go to Your AI and open **Other AI services**. Pick Mistral as the provider, paste the key and press **Save key**. Your Machine tries the key with one tiny request first. A wrong key shows right there, and nothing is saved.

Mistral Large becomes the main model. Mistral Small is there too, a cheaper choice for chats or as a fallback.

On your own computer, see the [models guide](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).

## Usage

**Settings**, **Model** says "Uses your Mistral API key". An API key has no usage limits, so background work never pauses for one. See [Model](model.md).

## Remove it

Pick another main model on your setup page. To stop the key, delete it in the Mistral console.
