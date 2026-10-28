---
title: Android-meldingen
area: connections
summary: De meldingen op je Android-telefoon, via de OpenClaw-app. Het leest alleen.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, More sources, Remove
---
## Wat het leest

De meldingen die binnenkomen op je Android-telefoon, via de OpenClaw-app. Eenmalige codes worden weggelaten, net als meldingen van WhatsApp, Telegram, Signal en Discord.

## Wat het kan doen

Niets op je telefoon. Het leest alleen meldingen.

## Koppelen

Op een gehoste Machine:

1. Installeer de OpenClaw-app op je telefoon.
2. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, kies Android-telefoon en druk op **Toon een instelcode**.
3. Scan hem in de OpenClaw-app en druk dan op **Goedkeuren** om te koppelen.
4. Zet in de OpenClaw-app Forward Notification Events aan, en sta toegang tot meldingen toe als Android erom vraagt.

Op je eigen computer koppel je de telefoon aan je OpenClaw Gateway en voer je daarna `assistant connect android` uit.

## Verwijderen

- In het dashboard: **Koppelingen**, open Android, **Details**, dan **Ontkoppelen**.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Verwijderen op de telefoon

Zet in de instellingen van Android de toegang tot meldingen voor de OpenClaw-app uit, of ontkoppel de telefoon in de OpenClaw-app.
