---
title: Von einer Website abgemeldet
area: troubleshooting
summary: LinkedIn oder X hat deine Machine abgemeldet. Melde sie wieder an, einmalig oder dauerhaft.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js, dashboard/connections-login-import.js
order: 2
translated: 9a9b91270954c031
---
Websites wie LinkedIn und X liest deine Machine in ihrem eigenen Browser. Manchmal meldet eine Website deine Machine ab.

## Wieder anmelden

Unter **Verbindungen** und oben in deinen Aufgaben wird angezeigt, dass deine Machine dort abgemeldet ist. Klicke auf **Hier anmelden** und melde dich in einem kleinen Fenster im Dashboard an.

Aktiviere **Für nächstes Mal speichern**, damit du dich beim nächsten Mal mit einem Klick wieder anmelden kannst. Das Passwort bleibt verschlüsselt auf deiner Machine und die KI sieht es nie. Wenn du mehrere Konten auf einer Website hast, kannst du mit **Speichern unter** diesem Konto einen Namen geben (Arbeit, Privat). Wenn in der Aufgabe nicht steht, welches Konto verwendet werden soll, fragt der Dialog danach.

## Passwörter und Codes

Gib Passwörter selbst ein. Auch Codes für die zweistufige Bestätigung musst du selbst eingeben.

Gespeicherte Anmeldungen findest du unter **Verbindungen**, **Anmeldungen**. Mit **Vergessen** entfernst du eine Anmeldung. Über **Importieren** kannst du Anmeldungen aus einem Passwortmanager importieren, entweder über dessen eigene Exportseite im Browser deiner Machine oder über eine Exportdatei.

## Wenn die Website die Anmeldung ablehnt oder eine Bot-Prüfung verlangt

LinkedIn, X und Websites mit einer Cloudflare-Prüfung lehnen Anmeldungen über einen Cloud-Browser häufig ab. Bei einer gehosteten Machine wird dann bei der Anmeldung **Über deine Verbindung zu Hause anmelden** angezeigt. Damit öffnest du deine Einrichtungsseite. Dort kann der Browser deiner Machine über deine Internetverbindung zu Hause, mit Tailscale oder über deinen eigenen Proxy, auf das Internet zugreifen. Melde dich danach erneut an.

Auf deinem eigenen Computer brauchst du das nicht: Der Browser ist bereits zu Hause.
