---
title: Microsoft Word: Word-bestanden in OneDrive en SharePoint
area: connections
summary: Reacties, vermeldingen, bijgehouden wijzigingen en gedeelde bestanden in je Word-bestanden in OneDrive en SharePoint, plus nieuwe documenten en wijzigingen die je goedkeurt. Google Docs komen later.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Wat het leest

De koppeling **Microsoft Word** leest Word-bestanden in OneDrive en SharePoint. Je logt er apart voor in met Microsoft, met of zonder gekoppelde Outlook. Dat werkt op een gehoste Machine en op je eigen computer die aan je account gekoppeld is. Google Docs komen later: de Google-login van The Machine kan nog geen documenten lezen. Het haalt binnen:

- Documenten die iemand met je deelt.
- Reacties en antwoorden op documenten van jou, en reacties die jou vermelden.
- Bijgehouden wijzigingen in Word-bestanden van jou.

De eerste sync kijkt 30 dagen terug. Elk item wordt een gebeurtenis, gekoppeld aan de personen en projecten in je [Graph](graph.md). Als een reactie jou nodig heeft, wordt ze een to-do.

## Wat het kan doen

Als een to-do de tekst van een document nodig heeft, leest je Machine dat ene document, en alleen terwijl hij aan die to-do werkt.

Hij kan een antwoord op een reactie schrijven. Bij Word-bestanden kan een antwoord niet van buiten Word geplaatst worden, dus het antwoord blijft een concept dat je zelf naar Word kopieert.

Hij aanvaardt nooit een suggestie, sluit nooit een reactie af, deelt nooit een bestand en wijzigt nooit een document zonder je OK.

## Documenten maken en bewerken

Je Machine kan een nieuw Word-document schrijven, of een document aanpassen waar een van je to-do's over gaat. Hij schrijft nooit uit zichzelf:

- Hij bereidt de wijziging voor op de to-do. Een nieuw document zie je helemaal. Een bewerking toont elke alinea voor en na.
- Tik op **Nakijken en maken** of **Wijzigingen nakijken**, lees het en dan **Maken** of **Opslaan**.
- Hij schrijft één keer, en alleen in het document zoals je het zag. Heeft iemand het intussen aangepast, dan wordt er niets geschreven en zegt de to-do dat. Vraag dan een nieuw concept.
- In Talk leest hij de hele wijziging voor en wacht op een duidelijk ja.

Hij vervangt tekst, voegt tekst toe en voegt alinea's en koppen toe. Tabellen, afbeeldingen, bijgehouden wijzigingen en velden laat hij met rust. Een nieuw document komt in je OneDrive en blijft privé tot je het deelt.

Een nieuw document gaat naar een account in het eigen gebied van de taak: een document voor een Werk-taak naar het account van dat bedrijf, het account van het gesprek als dat kan, nooit naar een privé-account. Op je eigen computer kan ook een Google-account dat voor Gmail is aangemeld en al toegang tot Drive heeft een nieuw Google-document krijgen. Past geen enkel account, dan zegt de taak **Koppel Google Docs of Microsoft Word voor Werk**.

Is het document niet het einde van de taak, zoals een antwoord met de link, dan blijft de taak open en maakt hij die volgende stap klaar voor je OK.

Microsoft Word koppelen staat dit al toe: er is geen aparte stap. Een oudere koppeling van Microsoft Word die alleen leest, toont **Bewerken toestaan** op haar kaart bij **Koppelingen**. Druk er één keer op en accepteer.

## Waar het om vraagt

Microsoft Word vraagt Microsoft om één OK, los van je login voor mail: om je bestanden te lezen en te wijzigen, ook die met je gedeeld zijn in OneDrive en SharePoint. Elke wijziging wacht nog altijd op je OK in haar taak. Je toegang tot je mail en je agenda blijft zoals ze is. Zonder Outlook geldt de login alleen voor je bestanden, nooit voor je mail of agenda.

Wordt die OK later ingetrokken, dan zegt de kaart van Microsoft Word **Wacht op je OK om documenten te lezen**.

## Koppelen

Je hebt er geen gekoppelde Outlook voor nodig.

- Gehoste Machine: open in het dashboard **Koppelingen**, **+ Toevoegen**, kies **Microsoft Word** en druk op **Inloggen met Microsoft**. Microsoft vraagt je om het lezen en bewerken van je bestanden toe te staan, daarna kom je terug in het dashboard.
- Je eigen computer, gekoppeld aan je account: open **Koppelingen**, **+ Toevoegen**, kies **Microsoft Word** en druk op **Inloggen met Microsoft**.

Hij controleert of de login documenten mag lezen. Zonder die OK wordt het niet toegevoegd. Druk je op **Bewerken toestaan** en staat Microsoft bewerken niet toe, dan zegt hij dat in plaats van Gekoppeld.

## Werk of privé

Microsoft Word volgt het label werk of privé van de koppeling, net als mail. Werkdocumenten kunnen in de Graph van je team terechtkomen volgens je [deelregels](sharing-rules.md). Privédocumenten nooit.

## Verwijderen

In het dashboard: **Koppelingen**, open Microsoft Word, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
