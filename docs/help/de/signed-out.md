---
title: Von einer Website abgemeldet
area: troubleshooting
summary: LinkedIn oder X hat deine Machine abgemeldet. Melde sie einmalig oder dauerhaft wieder an.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js
order: 2
translated: 060f7ca4f870ad0a
---
Websites wie LinkedIn und X werden im eigenen Browser deiner Machine geöffnet. Manchmal meldet eine Website sie ab.

## Wieder anmelden

Unter **Verbindungen** und oben bei deinen Aufgaben steht, dass sie abgemeldet ist. Klicke auf **Hier anmelden** und melde dich in einem kleinen Fenster auf dem Dashboard an.

Aktiviere **Für nächstes Mal speichern**, um dich beim nächsten Mal mit einem Tippen wieder anzumelden. Das Passwort bleibt auf deiner Machine verschlüsselt, und die KI sieht es nie. Bei mehreren Konten auf einer Website kannst du dieses Konto mit **Speichern unter** benennen (Arbeit, Privat). Wenn in der Aufgabe nicht steht, welches Konto verwendet werden soll, fragt der Dialog nach.

## Passwörter und Codes

Gib Passwörter selbst ein. Auch Codes für die Zwei-Faktor-Authentifizierung musst du selbst eingeben.

Gespeicherte Anmeldungen findest du unter **Verbindungen** und **Anmeldungen**. Mit **Vergessen** entfernst du eine Anmeldung. Mit **Importieren** übernimmst du Anmeldungen aus einem Passwortmanager.

## Wenn die Website die Anmeldung ablehnt oder eine Roboterprüfung verlangt

LinkedIn, X und Websites mit einer Cloudflare-Prüfung lehnen Anmeldungen über einen Browser in der Cloud oft ab. Auf einer gehosteten Machine wird dann bei der Anmeldung **Über deine Verbindung zu Hause anmelden** angezeigt. Damit öffnest du deine Einrichtungsseite. Dort kann der Browser deiner Machine über Tailscale oder deinen eigenen Proxy auf das Internet zu Hause zugreifen. Melde dich danach erneut an.

Auf deinem eigenen Computer brauchst du das nicht: Der Browser ist dort bereits mit deinem heimischen Internet verbunden.
