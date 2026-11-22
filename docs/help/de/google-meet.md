---
title: Google Meet
area: connections
summary: Transkripte und Gemini-Notizen von Meet-Besprechungen, die du organisierst. Die Verbindung liest nur.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
translated: cea7230915b5a536
---
## Was gelesen wird

Transkripte und Gemini-Notizen von Google Meet-Besprechungen, die du organisiert hast, sobald Meet sie erstellt hat: die letzten 7 Tage beim Verbinden und danach neue, sobald sie verfügbar sind. Meet speichert sie 30 Tage lang.

Meet erstellt sie nur, wenn während der Besprechung Transkripte oder Gemini-Notizen aktiviert waren.

Jeder Eintrag erscheint bei der jeweiligen Besprechung in deinem Kalender: Gemini-Notizen unter „Notizen“, das Transkript unter „Transkript“, gekennzeichnet mit **Von Google Meet**. Was du selbst hinzugefügt hast, bleibt erhalten.

## Was möglich ist

Die Verbindung nimmt keine Änderungen in Meet, Docs oder Drive vor. Sie liest nur und aktiviert niemals selbst Transkripte.

## Welche Berechtigungen nötig sind

Die Verbindung braucht eine eigene Zustimmung, getrennt von der für deine Mails. Google bittet dich, The Machine Folgendes zu erlauben:

- Deine Google Meet-Besprechungen, ihre Transkripte und Gemini-Notizen anzusehen.
- Deine Google Docs anzusehen, um das Dokument mit den Gemini-Notizen zu lesen.

Die Verbindung fragt niemals nach Zugriff auf dein Drive. Der Zugriff auf Gmail und Kalender bleibt unverändert.

## Verbindung herstellen

Gmail muss dafür nicht verbunden sein. So stellst du die Verbindung her:

- Gehostete Machine: Öffne im Dashboard **Verbindungen**, **Meetings**, wähle **Google Meet** und klicke auf **Mit Google anmelden**. Erteile die oben genannten Berechtigungen. Danach gelangst du zurück zum Dashboard.
- Dein eigener Computer, mit deinem Konto gekoppelt: Führe dieselben Schritte aus. Die Anmeldung wird in einem neuen Tab geöffnet.

Ohne die Zustimmung für Meet wird die Verbindung nicht hinzugefügt. Du musst nichts einfügen oder erneuern.

Wenn du die Zustimmung später widerrufst, wirst du in **Verbindungen** bei Google Meet aufgefordert, dich erneut anzumelden.

## Verbindung entfernen

Öffne im Dashboard **Verbindungen**, wähle Google Meet und dann **Details** und klicke auf **Trennen**. Bereits übertragene Inhalte bleiben erhalten.

## Zugriff bei Google widerrufen

Öffne myaccount.google.com/permissions und entferne den Zugriff von The Machine auf Google Meet. Gmail und Kalender funktionieren weiterhin.
