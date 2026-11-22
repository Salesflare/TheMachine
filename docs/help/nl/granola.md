---
title: Granola
area: connections
summary: Notities en transcripties van de meetings die je in Granola had. De koppeling leest alleen.
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## Wat hij leest

De notities en transcripties van Granola van meetings waar je bij was: de afgelopen 7 dagen wanneer je koppelt, daarna nieuwe zodra ze binnenkomen. Notities die nog worden geschreven, worden ingelezen zodra Granola ermee klaar is.

Elke notitie komt bij de bijbehorende afspraak in je agenda te staan. Dat is de afspraak die Granola noemt, of anders de afspraak op hetzelfde tijdstip. De notities van Granola komen onder Notities te staan en het transcript onder Transcript, met het label **Van Granola**. Wat je zelf hebt toegevoegd, blijft staan.

Na de meeting leest The Machine de notities en transcripties om te zien wat is beloofd, besloten of nog openstaat, zoals "Ik stuur de presentatie". Hij maakt alleen to-do's aan voor duidelijke vervolgstappen. De mensen in de meeting worden op basis van hun e-mailadres gekoppeld aan je [Graph](graph.md).

## Wat hij kan

Hij kan niets doen in Granola. Hij leest alleen en wijzigt, deelt of verwijdert nooit notities.

## Wat hij nodig heeft

Een persoonlijke API-sleutel van Granola. API-sleutels zijn beschikbaar bij de Business- en Enterprise-abonnementen van Granola. Met de sleutel kan hij je eigen notities en de notities die met je zijn gedeeld lezen, precies zoals je ze in Granola ziet.

## Koppelen

1. Open de desktopapp van Granola en ga naar **Settings**, **Connectors**, **API keys**. Maak een sleutel aan met toegang tot Personal notes en kopieer die.
2. Ga in het dashboard naar **Koppelingen**, **Meetings**, Granola. Op de installatiepagina van een gehoste Machine op app.themachine.computer/setup ga je naar **Meer bronnen**, Granola. Op je eigen computer vraagt `assistant connect granola` er ook om.
3. Plak de sleutel, kies **Werk** of **Privé** en druk op **Koppelen**.

De sleutel wordt meteen gecontroleerd. Als Granola de sleutel later niet meer accepteert, vraagt Granola bij **Koppelingen** je om een nieuwe sleutel.

## Verwijderen

- Ga in het dashboard naar **Koppelingen**, open Granola en kies **Details**. Kies daarna **Ontkoppelen**. Wat al is ingelezen, blijft staan.
- Op een gehoste Machine kun je ook op **Verwijderen** naast Granola op de installatiepagina drukken.

## De sleutel intrekken in Granola

Open de desktopapp van Granola en ga naar **Settings**, **Connectors**, **API keys**. Verwijder de sleutel.
