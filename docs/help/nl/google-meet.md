---
title: Google Meet
area: connections
summary: Transcripten en Gemini-notities van Google Meet-afspraken die je organiseert. The Machine leest alleen.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
translated: cea7230915b5a536
---
## Wat het leest

Transcripten en Gemini-notities van Google Meet-afspraken die je hebt georganiseerd, zodra Meet ze heeft gemaakt: de afgelopen 7 dagen wanneer je de koppeling maakt, en daarna nieuwe zodra ze beschikbaar zijn. Meet bewaart ze 30 dagen.

Meet maakt ze alleen als transcripten of Gemini-notities tijdens de afspraak waren ingeschakeld.

Elk item komt bij de bijbehorende afspraak in je agenda: Gemini-notities onder Notities, het transcript onder Transcript, met de markering **Van Google Meet**. Wat je zelf hebt toegevoegd, blijft staan.

## Wat het kan doen

Het doet niets in Meet, Docs of Drive. The Machine leest alleen en schakelt transcripten nooit zelf in.

## Waar het om vraagt

Een eigen toestemming, los van je mail. Google vraagt toestemming om The Machine:

- Je Google Meet-afspraken, de transcripten en Gemini-notities te laten bekijken.
- Je Google Docs te laten bekijken, zodat The Machine het document met Gemini-notities kan lezen.

The Machine vraagt nooit toegang tot je Drive. Je toegang tot Gmail en Agenda blijft ongewijzigd.

## Koppeling maken

Gmail hoeft niet gekoppeld te zijn. Zo maak je de koppeling:

- Gehoste Machine: open in het dashboard **Koppelingen**, **Afspraken**, kies **Google Meet** en klik op **Inloggen met Google**. Geef toestemming en je keert terug naar het dashboard.
- Je eigen computer, gekoppeld aan je account: volg dezelfde stappen. De inlogpagina wordt in een nieuw tabblad geopend.

Zonder toestemming voor Meet wordt de koppeling niet toegevoegd. Je hoeft niets te plakken of te vernieuwen.

Als je de toestemming later intrekt, vraagt Google Meet in **Koppelingen** je om opnieuw in te loggen.

## Koppeling verwijderen

Open in het dashboard **Koppelingen**, open Google Meet, kies **Details** en vervolgens **Ontkoppelen**. Wat al is opgehaald, blijft staan.

## Toegang intrekken via Google

Open myaccount.google.com/permissions en verwijder de toegang van The Machine tot Google Meet. Gmail en Agenda blijven werken.
