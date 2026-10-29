---
title: Google Meet
area: connections
summary: Transcripts en Gemini-notities van Meet-meetings die je organiseert. Het leest alleen.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
---
## Wat het leest

Transcripts en Gemini-notities van Google Meet-meetings die je organiseerde, zodra Meet ze gemaakt heeft: de laatste 7 dagen als je koppelt, daarna nieuwe zodra ze binnenkomen. Meet bewaart ze 30 dagen.

Meet maakt ze alleen als transcripts of Gemini-notities aanstonden tijdens de meeting.

Elk wordt gekoppeld aan de meeting in je agenda op hetzelfde moment. De Gemini-notities staan in Notities van die meeting en het transcript in Transcript, met **Van Google Meet** erbij, naast wat jij er toevoegde; ze vervangen het nooit.

## Wat het kan doen

Niets in Meet, Docs of Drive. Het leest alleen, en zet zelf nooit transcripts aan.

## Waar het om vraagt

Een eigen OK, los van je mail-login. Google vraagt of The Machine mag:

- Je Google Meet-meetings zien, met hun transcripts en Gemini-notities.
- Je Google Docs zien, om het document met de Gemini-notities te lezen.

Het vraagt nooit om je Drive. Je toegang tot Gmail en Agenda blijft zoals hij is.

## Koppelen

Gmail hoeft niet gekoppeld te zijn. Zo koppel je het:

- Gehoste Machine: open in het dashboard **Koppelingen**, **+ Toevoegen**, kies **Google Meet** en druk op **Inloggen met Google**. Google vraagt om de OK hierboven, daarna kom je terug in het dashboard.
- Je eigen computer, gekoppeld aan je account: dezelfde stappen. De login opent in een nieuw tabblad.

Hij controleert of de login Meet mag lezen. Zonder die OK wordt het niet toegevoegd. De login blijft werken: je hoeft niets te plakken of te vernieuwen.

Trek je de OK later in, dan vraagt de kaart van Google Meet om opnieuw in te loggen.

## Verwijderen

In het dashboard: **Koppelingen**, open Google Meet, **Details**, dan **Ontkoppelen**. Wat het al binnenhaalde, blijft.

## Intrekken bij Google

Open myaccount.google.com/permissions en verwijder de toegang van The Machine tot Google Meet. Gmail en Agenda blijven werken.
