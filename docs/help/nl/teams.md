---
title: Microsoft Teams
area: connections
summary: Teams-chats, meetingchats en meetingnotities voor een werk- of schoolaccount. Het leest alleen.
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
---
## Wat het leest

Je 1-op-1-, groeps- en meetingchats in Teams: de laatste 7 dagen bij het koppelen, daarna om de paar minuten nieuwe berichten. Oudere chats tot ongeveer een jaar terug, en met het OK van je admin ook kanaalthreads, komen later beetje bij beetje binnen als [geschiedenis](history.md), zonder iets op te houden.

Met het OK van je beheerder leest het ook:

- Kanaalthreads in je teams.
- Meetingtranscripts van meetings die je organiseerde.
- De meetingnotities en actiepunten van Copilot, als je een Microsoft 365 Copilot-licentie hebt.

Elk transcript of elke set notities komt bij de meeting in je Agenda, gemarkeerd met **Van Teams**. Zonder die blijft de meetingchat er gewoon.

Bots, apps en systeemberichten blijven erbuiten.

## Wat het kan doen

Niets in Teams. Het leest alleen. Om te antwoorden, open je de chat met **Openen in Teams**.

## Waar het om vraagt

Microsoft vraagt of The Machine je chats en je profiel mag lezen. Daar is geen beheerder voor nodig.

Kanalen, transcripts en Copilot-notities hebben één keer het OK van de beheerder van je organisatie nodig. Tot dan zegt de Teams-kaart wat het nog niet kan lezen en waarom.

Het werkt alleen met een Microsoft-werk- of schoolaccount. Persoonlijke accounts hebben geen Teams-chats die het zo kan lezen.

## Koppelen

Op een gehoste Machine:

1. Open in het dashboard **Koppelingen**, **+ Toevoegen** en kies **Microsoft Teams**.
2. Druk op **Inloggen met Microsoft** en geef het OK. Daarna ben je terug in het dashboard.
3. Voor kanalen en meetingnotities stuur je je beheerder de link die de inlogpagina toont. Zodra die goedkeurt, koppel je Teams opnieuw.

Tijdens het instellen heeft de instelpagina ook **Connect Microsoft Teams**.

Op je eigen computer is Teams nog niet beschikbaar.

## Verwijderen

In het dashboard: **Koppelingen**, open Microsoft Teams, **Details**, dan **Ontkoppelen**. Wat het al binnenhaalde, blijft.

## Intrekken bij Microsoft

Open myapps.microsoft.com en verwijder The Machine. Is Outlook met hetzelfde adres gekoppeld, dan wordt dat ook ontkoppeld.
