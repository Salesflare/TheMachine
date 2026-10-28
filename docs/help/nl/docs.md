---
title: Docs: Word, OneDrive en SharePoint
area: connections
summary: Reacties, vermeldingen, bijgehouden wijzigingen en gedeelde bestanden in je Word-bestanden in OneDrive en SharePoint. Google Docs komen later.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Wat het leest

Docs leest Word-bestanden in OneDrive en SharePoint, met de Microsoft-login die je al hebt voor dat adres. Dat werkt op een gehoste Machine en op je eigen computer die aan je account gekoppeld is. Google Docs komen later: de Google-login van The Machine kan nog geen documenten lezen. Het haalt binnen:

- Documenten die iemand met je deelt.
- Reacties en antwoorden op documenten van jou, en reacties die jou vermelden.
- Bijgehouden wijzigingen in Word-bestanden van jou.

De eerste sync kijkt 30 dagen terug. Elk item wordt een gebeurtenis, gekoppeld aan de personen en projecten in je [Graph](graph.md). Als een reactie jou nodig heeft, wordt ze een to-do.

## Wat het kan doen

Als een to-do de tekst van een document nodig heeft, leest je Machine dat ene document, en alleen terwijl hij aan die to-do werkt.

Hij kan een antwoord op een reactie schrijven. Bij Word-bestanden kan een antwoord niet van buiten Word geplaatst worden, dus het antwoord blijft een concept dat je zelf naar Word kopieert.

Hij bewerkt nooit een document, aanvaardt nooit een suggestie, sluit nooit een reactie af en deelt nooit een bestand.

## Waar het om vraagt

Documenten lezen heeft een eigen OK nodig, los van je login voor mail: Microsoft vraagt je om het lezen van je bestanden toe te staan, ook die met je gedeeld zijn in OneDrive en SharePoint. Je toegang tot je mail en je agenda blijft zoals ze is.

Wordt die OK later ingetrokken, dan zegt de kaart van Docs **Wacht op je OK om documenten te lezen**.

## Koppelen

Koppel eerst Outlook voor het adres. Dan:

- Gehoste Machine: open in het dashboard **Koppelingen**, **+ Toevoegen**, kies **Documenten** en druk op **Inloggen met Microsoft**. Microsoft vraagt je om het lezen van je bestanden toe te staan, daarna kom je terug in het dashboard.
- Je eigen computer, gekoppeld aan je account: open **Koppelingen**, **+ Toevoegen**, kies **Documenten** en druk op **Inloggen met Microsoft**.

Hij controleert of de login documenten mag lezen. Zonder die OK wordt het niet toegevoegd.

## Werk of privé

Docs volgt het label werk of privé van de koppeling, net als mail. Werkdocumenten kunnen in de Graph van je team terechtkomen volgens je [deelregels](sharing-rules.md). Privédocumenten nooit.

## Verwijderen

In het dashboard: **Koppelingen**, open Docs, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
