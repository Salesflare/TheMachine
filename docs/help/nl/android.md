---
title: Android-meldingen
area: connections
summary: Meldingen van je Android-telefoon via de OpenClaw-app. Hij leest alleen mee.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## Wat hij leest

Meldingen van je Android-telefoon via de OpenClaw-app. Eenmalige codes en meldingen van WhatsApp, Telegram, Signal en Discord worden niet gelezen.

## Wat hij kan doen

Niets op je telefoon. Hij leest alleen meldingen.

## Koppelen

Op een gehoste Machine:

1. Installeer OpenClaw vanuit Google Play op je telefoon.
2. Open in het dashboard **Koppelingen** en daarna **Andere**. Kies Android-meldingen en tik op **Toon een instelcode**.
3. Voeg in de OpenClaw-app een Gateway toe en scan de code. Tik daarna in het dashboard op **Goedkeuren**.
4. Geef toegang tot meldingen wanneer de app daarom vraagt. Schakel daarna Forward Notification Events in bij de instellingen van de app, zodat meldingen binnenkomen zodra ze verschijnen en niet alleen bij de controle om de 10 minuten.

Op je eigen computer koppel je de telefoon in de OpenClaw-app en voer je daarna `assistant connect android` uit.

## Ontkoppelen

- In het dashboard: open **Koppelingen**, open Android en tik op **Details** en daarna op **Ontkoppelen**.
- Op een gehoste Machine kun je ook op je installatiepagina naast de koppeling op **Verwijderen** tikken.

## Verwijderen van je telefoon

Schakel in de Android-instellingen de toegang tot meldingen voor de OpenClaw-app uit, of ontkoppel de telefoon in de OpenClaw-app.
