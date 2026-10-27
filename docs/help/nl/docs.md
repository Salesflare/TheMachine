---
title: Google Docs en Word
area: connections
summary: Reacties, vermeldingen, voorgestelde wijzigingen en gedeelde bestanden in je Google Docs of Word-bestanden. Het leest, en plaatst alleen een antwoord op een reactie als jij het goedkeurt.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
site: More sources, Connect documents, Sign in with Microsoft
---
## Wat het leest

Docs gebruikt de login bij Google of Microsoft die je al hebt voor dat adres. Het haalt binnen:

- Documenten die iemand met je deelt.
- Reacties en antwoorden op documenten van jou, en reacties die jou vermelden.
- Voorgestelde wijzigingen in Google Docs van jou, en bijgehouden wijzigingen in Word-bestanden van jou.

De eerste sync kijkt 30 dagen terug. Elk item wordt een gebeurtenis, gekoppeld aan de personen en projecten in je [Graph](graph.md). Als een reactie jou nodig heeft, wordt ze een to-do.

## Wat het kan doen

Als een to-do de tekst van een document nodig heeft, leest je Machine dat ene document, en alleen terwijl hij aan die to-do werkt.

Hij kan een antwoord op een reactie schrijven. Bij Google Docs wacht het antwoord op de to-do: druk op **Nakijken en plaatsen**, controleer het en dan **Nu plaatsen**. Er wordt niets geplaatst tot je dat doet. Bij Word-bestanden kan een antwoord niet van buiten Word geplaatst worden, dus die antwoorden blijven concepten die je zelf naar Word kopieert.

Hij bewerkt nooit een document, aanvaardt nooit een suggestie, sluit nooit een reactie af en deelt nooit een bestand.

## Waar het om vraagt

Documenten lezen heeft een eigen OK nodig, los van je login voor mail. Je toegang tot Gmail en je agenda blijft zoals ze is.

- Google: alleen-lezentoegang tot je bestanden en reacties in Drive. Antwoorden plaatsen vraagt nog een OK, die je kunt overslaan.
- Microsoft: leestoegang tot je bestanden, ook die met je gedeeld zijn in OneDrive en SharePoint.

Wordt die OK later ingetrokken, dan zegt de kaart van Docs **Wacht op je OK om documenten te lezen**.

## Koppelen

Koppel eerst Outlook voor het adres. Dan:

- Gehoste Machine: open op je setuppagina **Documenten** onder **Meer bronnen** en druk op **Documenten koppelen** naast dat adres. Microsoft vraagt je om het lezen van je bestanden toe te staan.
- Je eigen computer, gekoppeld aan je account: open **Koppelingen**, **+ Toevoegen**, kies **Documenten** en druk op **Inloggen met Microsoft**.

Hij controleert of de login documenten mag lezen. Zonder die OK wordt het niet toegevoegd. Google Docs zijn nog niet beschikbaar via de login van The Machine.

## Werk of privé

Docs volgt het label werk of privé van de koppeling, net als mail. Werkdocumenten kunnen in de Graph van je team terechtkomen volgens je [deelregels](sharing-rules.md). Privédocumenten nooit.

## Verwijderen

In het dashboard: **Koppelingen**, open Docs, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
