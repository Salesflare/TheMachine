---
title: Google Meet
area: connections
summary: Transkripte und Gemini-Notizen von Meet-Meetings, die du organisierst. Es liest nur.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
---
## Was es liest

Transkripte und Gemini-Notizen von Google-Meet-Meetings, die du organisiert hast, sobald Meet sie erstellt hat: die letzten 7 Tage beim Verbinden, danach neue, sobald sie reinkommen. Meet bewahrt sie 30 Tage auf.

Meet erstellt sie nur, wenn Transkripte oder Gemini-Notizen während des Meetings eingeschaltet waren.

Jedes wird dem Meeting in deinem Kalender zur selben Zeit zugeordnet. Die Gemini-Notizen stehen in den Notizen dieses Meetings und das Transkript in Transkript, markiert mit **Von Google Meet**, neben dem, was du dort hinzugefügt hast; sie ersetzen es nie.

## Was es tun kann

Nichts in Meet, Docs oder Drive. Es liest nur und schaltet nie selbst Transkripte ein.

## Worum es fragt

Um ein eigenes OK, getrennt von deiner Mail-Anmeldung. Google fragt, ob The Machine:

- Deine Google Meet-Meetings mit ihren Transkripten und Gemini-Notizen sehen darf.
- Deine Google Docs sehen darf, um das Dokument mit den Gemini-Notizen zu lesen.

Es fragt nie nach deinem Drive. Dein Zugriff auf Gmail und Kalender bleibt, wie er ist.

## Verbinden

Gmail muss dafür nicht verbunden sein. So verbindest du es:

- Gehostete Machine: Öffne im Dashboard **Verbindungen**, **+ Hinzufügen**, wähle **Google Meet** und tippe auf **Mit Google anmelden**. Google fragt nach dem OK oben, dann kommst du zurück zum Dashboard.
- Dein eigener Computer, gekoppelt mit deinem Konto: dieselben Schritte. Die Anmeldung öffnet sich in einem neuen Tab.

Es prüft, ob die Anmeldung Meet lesen darf. Ohne dieses OK wird es nicht hinzugefügt. Die Anmeldung bleibt gültig: Du musst nichts einfügen oder erneuern.

Ziehst du das OK später zurück, bittet die Karte von Google Meet dich, dich erneut anzumelden.

## Entfernen

Im Dashboard: **Verbindungen**, Google Meet öffnen, **Details**, dann **Trennen**. Was es schon geholt hat, bleibt.

## Bei Google widerrufen

Öffne myaccount.google.com/permissions und entferne den Zugriff von The Machine auf Google Meet. Gmail und Kalender laufen weiter.
