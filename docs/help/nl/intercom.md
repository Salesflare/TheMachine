---
title: Intercom
area: connections
summary: Klantgesprekken in je Intercom-workspace. Het antwoordt alleen nadat jij verstuurt, als jou.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
---
## Wat het leest

Klantgesprekken in je Intercom-workspace: de laatste 7 dagen als je koppelt, daarna nieuwe gesprekken zodra ze binnenkomen. Het leest ook bij welke workspace en welke beheerder de login hoort.

## Wat het kan doen

Het leest gesprekken. Met je eigen **Inloggen met Intercom** kan het ook als jou antwoorden in een gesprek, alleen nadat je op **Versturen** drukt voor precies die tekst. Het wijst nooit toe, sluit nooit, tagt nooit en schrijft geen notities. Een Intercom die via je Fleet met je gedeeld is, leest alleen.

## To-do's uit Intercom

Een to-do uit een Intercom-gesprek toont waar die vandaan komt: **Bericht lezen** opent het gesprek, met een link ernaar in Intercom, en de klant staat op de to-do. Het antwoord is een Intercom-antwoord in dat gesprek, tenzij je om een e-mail vraagt.

Alleen gesprekken die aan jou of nog aan niemand zijn toegewezen, worden to-do's, ook die in een teaminbox zonder iemand erop. Neemt een teamgenoot een gesprek over in Intercom, dan sluit de open to-do vanzelf, met **Ongedaan maken**. Bij een Intercom die met je gedeeld is, zijn jouw gesprekken die van de beheerder waarmee je schrijft.

Een Intercom-to-do sluit ook vanzelf zodra iemand van het team het gesprek in Intercom sluit, of antwoordt en de klant sindsdien niet meer schreef, als de to-do alleen om een antwoord vroeg. Dat telt ook als je net vóór de to-do antwoordde, voor The Machine je antwoord had gelezen. Een notitie, een snooze of het antwoord van een bot telt nooit.

Kan Intercom niet antwoorden vanaf je Machine (alleen-lezen met je gedeeld, antwoorden niet aangezet, of niet gekoppeld), dan gaat het concept per e-mail. De to-do zegt waarom, en de review vraagt **In plaats daarvan per e-mail versturen?** Wil je zelf in Intercom antwoorden, tik dan op **Koppel je eigen Intercom** op de to-do en log in. Daarna wordt de to-do opnieuw geschreven als antwoord in Intercom. Er gaat niets weg voor je het verstuurt.

Je eigen Intercom en een gedeelde voor dezelfde workspace lezen niet allebei: de gedeelde rust, en zijn gesprekken gaan naar de jouwe, elk één keer.

## Koppelen

1. In het dashboard: **Koppelingen**, **+ Toevoegen**, Intercom. Of op de setuppagina van een gehoste Machine op app.themachine.computer/setup: **Meer bronnen**, Intercom. Op je eigen computer koppel je hem eerst aan je account.
2. Druk op **Inloggen met Intercom**.
3. Keur The Machine goed in Intercom. Hij is gemaakt door Salesflare. Daarna ben je terug waar je begon.

Inloggen bij een andere workspace voegt een tweede Intercom-account toe.

Intercom telt altijd als werk, voor het bedrijf dat de workspace noemt.

## Verwijderen

- In het dashboard: **Koppelingen**, open Intercom, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Verwijderen op Intercom

Open in Intercom Settings, Apps, Installed apps, en verwijder The Machine.
