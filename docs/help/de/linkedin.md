---
title: LinkedIn
area: connections
summary: Deine LinkedIn-Nachrichten, gelesen im eigenen angemeldeten Browser deiner Machine. Antworten erst nach deiner Freigabe.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py
site: Connect, More sources, Remove
---
## Was es liest

Deine LinkedIn-Nachrichten. Es liest sie in einem Tab des eigenen Browsers deiner Machine, mit dir angemeldet, ab und zu während deiner wachen Stunden. Es nutzt keinen API-Schlüssel und markiert nichts als gelesen.

## Was es senden kann

Eine Antwort auf eine Nachricht, und nur, nachdem du sie bei der Aufgabe freigegeben hast. Bis dahin entwirft es nur.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und geh zu **Weitere Quellen**.
2. Öffne LinkedIn, melde dich bei LinkedIn im Browser deiner Machine an, wenn es danach fragt, und tippe dann auf **Verbinden**.

Auf deinem eigenen Computer:

1. Melde dich einmal im Browser deiner Machine bei LinkedIn an (Einstellungen, **Browser der Machine öffnen ↗**).
2. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle LinkedIn. Oder führe `assistant connect linkedin` aus.

Ein zweites LinkedIn-Konto bekommt einen eigenen Browser. Wenn LinkedIn deine Machine abmeldet, siehe [Von einer Website abgemeldet](signed-out.md).

## Wenn LinkedIn nach einem Code fragt

Beim ersten Anmelden schickt LinkedIn oft einen Code per E-Mail. Gib ihn im Anmeldefenster unter **Code** ein und drück auf **Anmelden**. Die Seite bleibt stehen, während du tippst.

Geht LinkedIn zurück zum Anfang oder passiert zwei Minuten lang nichts, hat LinkedIn die Anmeldung gestoppt. Warte eine Minute und drück auf **Erneut versuchen**. Zeigt LinkedIn eine Roboterprüfung, erledige sie im Browser deiner Machine.

## Entfernen

- Im Dashboard: **Verbindungen**, LinkedIn öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei LinkedIn abmelden

Öffne in LinkedIn Einstellungen, Anmelden und Sicherheit, Wo du angemeldet bist, und melde die Sitzung des Browsers deiner Machine ab.
