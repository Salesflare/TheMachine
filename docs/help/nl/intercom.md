---
title: Intercom
area: connections
summary: Klantgesprekken in je Intercom-workspace. Er worden pas antwoorden verstuurd als jij dat doet, namens jou.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 2cbee87e6d24c0a9
---
## Wat hij leest

Klantgesprekken in je Intercom-workspace: de laatste 7 dagen op het moment dat je koppelt, en daarna nieuwe gesprekken zodra ze binnenkomen. Hij leest ook bij welke workspace en teamgenoot de aanmelding hoort.

## Wat hij kan doen

Met je eigen **Inloggen met Intercom** kan hij namens jou antwoorden in een gesprek, maar pas nadat je voor die specifieke tekst op **Versturen** drukt. Hij wijst nooit gesprekken toe, sluit ze niet, voegt geen tags toe en schrijft geen notities. Een Intercom-koppeling die via je Fleet met je is gedeeld, kan alleen lezen.

## To-do's vanuit Intercom

Een to-do vanuit Intercom toont de klant. Met **Bericht lezen** open je het gesprek en de link ernaartoe in Intercom. Het antwoord wordt in dat gesprek verstuurd, tenzij je om een e-mail vraagt.

Alleen gesprekken die aan jou zijn toegewezen of nog aan niemand zijn toegewezen, worden to-do's. Zodra een teamgenoot een gesprek in Intercom oppakt, wordt de bijbehorende to-do automatisch gesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Bij een Intercom-koppeling die met je is gedeeld, zijn jouw gesprekken de gesprekken die zijn toegewezen aan de teamgenoot namens wie je schrijft.

Een Intercom-to-do wordt ook automatisch gesloten zodra iemand in het team het gesprek in Intercom sluit, of erop antwoordt en de klant daarna niets meer heeft geschreven, als de to-do alleen om een antwoord vroeg. Dat geldt ook als je zelf al antwoordde vlak voordat de to-do binnenkwam, voordat The Machine je antwoord had gelezen. Een notitie, snooze of antwoord van een bot telt niet.

Als je Machine niet kan antwoorden in Intercom (de koppeling is alleen-lezen, antwoorden zijn niet ingeschakeld of Intercom is niet gekoppeld), wordt het concept klaargezet om per e-mail te versturen. In de to-do staat waarom en wordt gevraagd **In plaats daarvan per e-mail versturen?** Tik op de to-do op **Koppel je eigen Intercom** en meld je aan om in Intercom te antwoorden. De to-do wordt dan opnieuw aangemaakt als antwoord in Intercom. Er wordt niets verstuurd voordat je het verstuurt.

Je eigen Intercom en een Intercom-koppeling die met je is gedeeld, lezen niet allebei dezelfde workspace: de gedeelde koppeling blijft ongebruikt en de gesprekken worden één keer naar je eigen koppeling verplaatst.

## Koppelen

1. In het dashboard: **Koppelingen**, **Klanten**, Intercom. Of op de instellingenpagina van een gehoste Machine op app.themachine.computer/setup: **Meer bronnen**, Intercom. Koppel een Machine op je eigen computer eerst aan je account.
2. Druk op **Inloggen met Intercom**.
3. Geef The Machine (gemaakt door Salesflare) toestemming in Intercom. Je komt terug op de plek waar je begon.

Als je je aanmeldt bij een andere workspace, wordt een tweede Intercom-account toegevoegd.

Intercom telt altijd als werk, voor het bedrijf dat bij de workspace hoort.

## Verwijderen

- In het dashboard: **Koppelingen**, open Intercom en kies **Details** en daarna **Ontkoppelen**. Intercom wordt dan niet meer gelezen. Wat al is binnengehaald, blijft staan.
- Op een gehoste Machine kun je ook op de instellingenpagina naast Intercom op **Verwijderen** drukken.

## Intercom verwijderen

Open in Intercom Settings, Apps, Installed apps en verwijder The Machine.
