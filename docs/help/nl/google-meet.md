---
title: Google Meet
area: connections
summary: Transcripts en Gemini-notities van Meet-meetings die je organiseert. Het leest alleen.
covers: connector:google_meet
code: connectors/google_meet.py
site: Connect, More sources, Remove
---
## Wat het leest

Transcripts en Gemini-notities van Google Meet-meetings die je organiseerde, zodra Meet ze gemaakt heeft: de laatste 7 dagen als je koppelt, daarna nieuwe zodra ze binnenkomen. Meet bewaart ze 30 dagen.

Meet maakt ze alleen als transcripts of Gemini-notities aanstonden tijdens de meeting.

## Wat het kan doen

Niets in Meet of Drive. Het leest alleen, en zet zelf nooit transcripts aan.

## Koppelen

1. Zet in Google Cloud de Google Meet API en de Google Drive API aan.
2. Haal in de OAuth Playground een toegangstoken met de twee alleen-lezen-scopes die het koppelscherm toont.
3. Op een gehoste Machine: open je setuppagina op app.themachine.computer/setup, ga naar **Meer bronnen** en open Google Meet. Op je eigen computer: **Koppelingen**, **+ Toevoegen**, Google Meet, of `assistant connect google_meet`.
4. Plak het token en druk op **Verbinden**.

Het token verloopt na ongeveer een uur. Als Koppelingen zegt dat het geweigerd is, plak je een nieuw.

## Verwijderen

- In het dashboard: **Koppelingen**, open Google Meet, **Details**, dan **Ontkoppelen**. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Intrekken bij Google

Open myaccount.google.com/permissions en verwijder de toegang van de OAuth Playground.
