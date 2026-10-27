---
title: Intercom
area: connections
summary: Klantgesprekken in je Intercom-workspace. Het antwoordt alleen nadat jij verstuurt, als jou.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, Or paste an access token, Connect, More sources, Remove
---
## Wat het leest

Klantgesprekken in je Intercom-workspace: de laatste 7 dagen als je koppelt, daarna nieuwe gesprekken zodra ze binnenkomen. Het leest ook bij welke workspace en welke beheerder de login hoort.

## Wat het kan doen

Het leest gesprekken. Met je eigen **Inloggen met Intercom** kan het ook als jou antwoorden in een gesprek, alleen nadat je op **Versturen** drukt voor precies die tekst. Het wijst nooit toe, sluit nooit, tagt nooit en schrijft geen notities. Een Intercom die via je Fleet met je gedeeld is, leest alleen.

## To-do's uit Intercom

Een to-do uit een Intercom-gesprek toont waar die vandaan komt: **Bericht lezen** opent het gesprek, met een link ernaar in Intercom, en de klant staat op de to-do. Het antwoord is een Intercom-antwoord in dat gesprek, tenzij je om een e-mail vraagt.

Kan Intercom niet antwoorden vanaf je Machine (alleen-lezen met je gedeeld, antwoorden niet aangezet, of niet gekoppeld), dan gaat het concept per e-mail. De to-do zegt waarom, en de review vraagt **In plaats daarvan per e-mail versturen?** Wil je zelf in Intercom antwoorden, tik dan op **Koppel je eigen Intercom** op de to-do en log in. Er gaat niets weg voor je het verstuurt.

## Koppelen

Op een gehoste Machine:

1. Open je setuppagina op app.themachine.computer/setup en ga naar **Meer bronnen**.
2. Open Intercom en druk op **Inloggen met Intercom**.
3. Keur The Machine goed in Intercom. Het is gemaakt door Salesflare.

Past de login niet bij je workspace, open dan **Of plak een toegangstoken**, plak een token uit de Developer Hub van Intercom en druk op **Verbinden**.

Op je eigen computer:

1. Open in de Developer Hub van Intercom je app, dan Authentication, en kopieer het toegangstoken.
2. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies Intercom. Of voer `assistant connect intercom` uit.
3. Plak het token. Een token van een andere workspace wordt een tweede Intercom-account.

Intercom telt altijd als werk, voor het bedrijf dat de workspace noemt.

## Verwijderen

- In het dashboard: **Koppelingen**, open Intercom, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
- Op een gehoste Machine kun je ook op **Verwijderen** ernaast drukken op je setuppagina.

## Verwijderen op Intercom

- Ingelogd met Intercom: open in Intercom Settings, Apps, Installed apps, en verwijder The Machine.
- Een geplakt token: verwijder of vervang het in de Developer Hub, of verwijder de app waarin je het gemaakt hebt.
