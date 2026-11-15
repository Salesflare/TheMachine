---
title: Von einer Website abgemeldet
area: troubleshooting
summary: LinkedIn oder X hat deine Machine abgemeldet. Melde dich wieder an, einmalig oder dauerhaft.
covers:
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: 96c09e57cd3dca62
---
Websites wie LinkedIn und X werden im eigenen Browser deiner Machine aufgerufen. Manchmal meldet dich eine Website ab.

## Wieder anmelden

Unter **Verbindungen** und oben in deinen Aufgaben steht, dass du abgemeldet bist. Klicke auf **Hier anmelden** und melde dich in einem kleinen Fenster auf dem Dashboard an.

Aktiviere **Für nächstes Mal speichern**, damit du dich beim nächsten Mal mit einem Klick wieder anmelden kannst. Das Passwort bleibt auf deiner Machine verschlüsselt und die KI sieht es nie.

## Passwörter und Codes

Gib Passwörter selbst ein. Auch Codes für die zweistufige Anmeldung musst du selbst eingeben.

Deine gespeicherten Anmeldungen findest du unter **Verbindungen** > **Anmeldungen**. Mit **Vergessen** kannst du eine davon entfernen.

## Wenn die Website die Anmeldung ablehnt oder eine Roboterprüfung verlangt

LinkedIn, X und Websites mit einer Cloudflare-Prüfung lehnen Anmeldungen über einen Browser in der Cloud oft ab. Bei einer gehosteten Machine wird dann **Über deine Verbindung zu Hause anmelden** angezeigt. Damit öffnest du deine Einrichtungsseite. Dort kann der Browser deiner Machine über Tailscale oder deinen eigenen Proxy auf das Internet über deinen Heimanschluss zugreifen. Melde dich anschließend erneut an.

Auf deinem eigenen Computer brauchst du das nicht: Der Browser ist bereits mit deinem Heimnetz verbunden.
