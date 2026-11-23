---
title: Intercom
area: connections
summary: Klantgesprekken in je Intercom-werkruimte. Hij reageert pas nadat je zelf iets verstuurt.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 5a6938dd6c220a43
---
## Wat hij leest

Klantgesprekken in je Intercom-werkruimte: de afgelopen 7 dagen wanneer je koppelt, en daarna nieuwe gesprekken zodra ze binnenkomen. Hij leest ook bij welke werkruimte en teamgenoot de login hoort.

## Wat hij kan doen

Met je eigen **Inloggen met Intercom** kan hij in een gesprek namens jou reageren, maar alleen nadat je bij die specifieke tekst op **Versturen** drukt. Hij wijst nooit gesprekken toe, sluit ze niet, voegt geen tags toe en schrijft geen notities. Een Intercom die via je Fleet met je is gedeeld, kan alleen lezen.

## To-do's uit Intercom

Bij een to-do uit Intercom zie je de klant. Met **Bericht lezen** open je het gesprek, met een link naar Intercom. Elk bericht staat onder de naam van de schrijver: de klant aan de ene kant, en je team en de bot aan de andere kant. Dat geldt ook als een teamgenoot of campagne het gesprek is begonnen. Het antwoord wordt in dat gesprek verstuurd, tenzij je om een e-mail vraagt.

Alleen gesprekken die aan jou of nog aan niemand zijn toegewezen, worden to-do's. Zodra een teamgenoot een gesprek in Intercom oppakt, wordt de bijbehorende to-do automatisch gesloten. Je kunt dit ongedaan maken met **Ongedaan maken**. In een Intercom die met je is gedeeld, zijn jouw gesprekken de gesprekken die zijn toegewezen aan de teamgenoot namens wie je schrijft.

Een to-do uit Intercom wordt ook automatisch gesloten zodra iemand uit het team het gesprek in Intercom sluit, of erop antwoordt en de klant sindsdien niets meer heeft geschreven, als de to-do alleen om een antwoord vroeg. Dit geldt ook als je net voordat de to-do binnenkwam al had geantwoord, voordat The Machine je antwoord had gelezen. Een notitie, een snooze of een antwoord van een bot telt niet mee.

Als je Machine niet in Intercom kan antwoorden (de Intercom is alleen met je gedeeld om te lezen, antwoorden zijn niet ingeschakeld of de Intercom is niet gekoppeld), wordt het concept in plaats daarvan per e-mail verstuurd. In de to-do staat waarom en wordt gevraagd **In plaats daarvan per e-mail versturen?** Tik op de to-do op **Koppel je eigen Intercom** en log in om in Intercom te antwoorden. De to-do wordt dan opnieuw aangemaakt als antwoord in Intercom. Er wordt niets verstuurd voordat je het zelf verstuurt.

Je eigen Intercom en een Intercom die met je is gedeeld, lezen niet allebei dezelfde werkruimte. De gedeelde Intercom blijft inactief en de gesprekken worden naar je eigen Intercom verplaatst, elk één keer.

## Koppelen

1. In het dashboard: **Koppelingen**, **Klanten**, Intercom. Of op de installatiepagina van een gehoste Machine op app.themachine.computer/setup: **Meer bronnen**, Intercom. Koppel je eigen computer eerst aan je account.
2. Druk op **Inloggen met Intercom**.
3. Geef The Machine (gemaakt door Salesflare) toestemming in Intercom. Je keert terug naar waar je begon.

Als je inlogt op een andere werkruimte, wordt er een tweede Intercom-account toegevoegd.

Intercom telt altijd als werk voor het bedrijf dat in de naam van de werkruimte staat.

## Verwijderen

- In het dashboard: **Koppelingen**, open Intercom en kies **Details** en daarna **Ontkoppelen**. Hij stopt met lezen. Wat hij al heeft opgehaald, blijft staan.
- Op een gehoste Machine kun je ook op de installatiepagina op **Verwijderen** drukken, naast Intercom.

## Intercom verwijderen

Open in Intercom **Instellingen**, **Apps**, **Geïnstalleerde apps** en verwijder The Machine.
