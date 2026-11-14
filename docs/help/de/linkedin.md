---
title: LinkedIn
area: connections
summary: Deine LinkedIn-Nachrichten, gelesen im eigenen angemeldeten Browser deiner Machine. Antworten erst nach deiner Freigabe.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: 850b91f79b9e23fc
---
## Was es liest

Deine LinkedIn-Nachrichten. Es liest sie in einem Tab des eigenen Browsers deiner Machine, mit dir angemeldet, ab und zu während deiner wachen Stunden. Es nutzt keinen API-Schlüssel und markiert nichts als gelesen. Antworten in Unterhaltungen, die du archiviert hast, und Nachrichtenanfragen kommen auch an; Spam bleibt draußen.

## Positionen und Firmen

Es hält auch die Positionen und Firmen deiner LinkedIn-Kontakte bei den Personen aktuell, die schon in deinem Graph sind, aus deiner Kontaktliste. Es öffnet keine Profile und legt keine neuen Personen an. Ändert sich die Position oder Firma von jemandem, steht das in der Zeitleiste, etwa "Jetzt Head of Sales bei Acme, vorher Sales Lead bei Acme".

Die Position kommt aus ihrem Profilslogan, etwa "Head of Sales bei Acme" oder "VP Sales and Strategy", nie aus einem Werbespruch. Es findet sie über ihren Profillink oder über Name und Firma. Gibt es keine Firma zum Vergleichen, reicht ein vollständiger Name, den nur eine Person in deinem Graph hat. Ihre Seite zeigt auch, seit wann ihr vernetzt seid.

Es liest sehr langsam: eine Seite auf einmal, Minuten auseinander, ein paar Dutzend Seiten am Tag, nur tagsüber. Rund 3.000 Kontakte dauern etwa vier Tage. Bremst LinkedIn, hört es bis zum nächsten Tag auf.

## Was es senden kann

Eine Antwort auf eine Nachricht oder eine neue Nachricht an ein Profil, das du nennst, und nur, nachdem du sie bei der Aufgabe freigegeben hast. Bis dahin entwirft es nur.

LinkedIn bietet dafür keinen offiziellen Weg. Lesen und ab und zu eine Nachricht, die du freigegeben hast, machen so gut wie nie Probleme; massenhaftes oder automatisches Senden kann zur Sperrung eines Kontos führen.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und geh zu **Weitere Quellen**.
2. Öffne LinkedIn, melde dich bei LinkedIn im Browser deiner Machine an, wenn es danach fragt, und tippe dann auf **Verbinden**.

Auf deinem eigenen Computer:

1. Öffne im Dashboard **Verbindungen**, dann **Chat**, und wähle LinkedIn.
2. Wähle **Arbeit** mit ihrer Firma oder **Privat** und tippe auf **Verbinden**.
3. Tippe auf **Bei LinkedIn anmelden** und melde dich im Browser deiner Machine an. Sobald du drin bist, verbindet es sich von selbst.

Oder führe `assistant connect linkedin` aus.

Ein zweites LinkedIn-Konto bekommt einen eigenen Browser. Wenn LinkedIn deine Machine abmeldet, siehe [Von einer Website abgemeldet](signed-out.md).

## Wenn LinkedIn nach einem Code fragt

Beim ersten Anmelden schickt LinkedIn oft einen Code per E-Mail. Gib ihn im Anmeldefenster unter **Code** ein und drück auf **Anmelden**. Die Seite bleibt stehen, während du tippst.

Geht LinkedIn zurück zum Anfang oder passiert zwei Minuten lang nichts, hat LinkedIn die Anmeldung gestoppt. Warte eine Minute und drück auf **Erneut versuchen**. Zeigt LinkedIn eine Roboterprüfung, erledige sie im Browser deiner Machine.

## Entfernen

- Im Dashboard: **Verbindungen**, LinkedIn öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei LinkedIn abmelden

Öffne in LinkedIn Einstellungen, Anmelden und Sicherheit, Wo du angemeldet bist, und melde die Sitzung des Browsers deiner Machine ab.
