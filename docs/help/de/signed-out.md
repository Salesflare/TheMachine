---
title: Von einer Website abgemeldet
area: troubleshooting
summary: LinkedIn oder X hat deine Machine abgemeldet. Melde sie wieder an, einmal oder dauerhaft.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: b77b372b9332ca2b
---
Websites wie LinkedIn und X werden im eigenen Browser deiner Machine gelesen. Manchmal meldet eine Website ihn ab.

## Wieder anmelden

Die Quelle unter **Verbindungen** und der obere Teil deiner Aufgaben zeigen, dass sie abgemeldet ist. Tippe auf **Erneut anmelden** und melde dich in einem kleinen Fenster im Dashboard an.

Setz beim Anmelden ein Häkchen bei **Für nächstes Mal speichern**. Wenn die Website deine Machine das nächste Mal abmeldet, meldet sie sich mit einem Tippen wieder an. Das Passwort bleibt verschlüsselt auf deiner Machine. Die KI sieht es nie.

## Passwörter und Codes

Gib Passwörter selbst ein. Codes für die Zwei-Schritt-Bestätigung gibst du ebenfalls selbst ein.

Gespeicherte Anmeldungen stehen unter **Verbindungen**, **Anmeldungen**. **Vergessen** entfernt eine.

## Wenn die Seite ablehnt oder eine Roboterprüfung will

LinkedIn, X und Seiten hinter einer Cloudflare-Prüfung lehnen Anmeldungen aus einem Browser in der Cloud oft ab. Auf einer gehosteten Machine zeigt die Anmeldung dann **Über deine Verbindung zu Hause anmelden**. Das öffnet deine Einrichtungsseite, wo der Browser deiner Machine über dein Internet zu Hause rausgehen kann, mit Tailscale oder über deinen eigenen Proxy. Melde dich danach erneut an.

Auf deinem eigenen Computer brauchst du das nicht: Sein Browser ist schon zu Hause.
