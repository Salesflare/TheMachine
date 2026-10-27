---
title: Microsoft Outlook und Kalender
area: connections
summary: Outlook-Mails und Meetings, für Microsoft 365 und Outlook.com. Sendet eine E-Mail erst, nachdem du sie freigegeben hast.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, onboarding.py
site: Connect Microsoft, Copy link for your admin, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
---
## Was es liest

- **Outlook**: alle deine Mails, die letzten 7 Tage beim Verbinden, danach alles Neue.
- **Outlook-Kalender**: deine Meetings, nur lesend.

Mails unter Sonstige und Newsletter werden zuerst kurz angesehen: Absender, Betreff und ein paar Wörter, viele auf einmal. Wenn eine wichtig ist, wird sie ganz gelesen und kann zu einer Aufgabe werden. Nichts wird ungesehen übersprungen.

## Was es senden und ändern kann

- Eine E-Mail aus einer Aufgabe, erst nachdem du sie in der Vorschau freigegeben hast.
- Wenn du eine Aufgabe zu einer E-Mail zurückstellst, wandern die Nachrichten des Threads in Outlook in einen Ordner Snoozed und kommen zurück, wenn die Aufgabe zurückkommt.

Der Kalender wird nie geändert.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup.
2. Tippe auf **Microsoft verbinden** und melde dich an.
3. Wenn Microsoft nach einer Admin-Freigabe fragt, tippe auf **Link für deinen Admin kopieren**, oder auf **Ich bin der Admin: jetzt freigeben**, wenn du das bist.

Oder im Dashboard: **Verbindungen**, **+ Hinzufügen**, wähle Outlook und tippe auf **Mit Microsoft anmelden**. Danach bist du zurück im Dashboard.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt](fleet.md) ist: Öffne **Verbindungen**, dann **+ Hinzufügen**, wähle Outlook und tippe auf **Mit Microsoft anmelden**. Mail und Kalender werden zusammen verbunden.

Mit deiner eigenen App: Öffne dort **Eigene App nutzen** oder führe `assistant connect outlook` oder `assistant connect outlook_calendar` aus. Es nutzt deine eigene App-Registrierung in Microsoft Entra und einen Anmeldecode. Es fragt, ob es auch senden soll, was du freigibst.

## Entfernen

- Auf einer gehosteten Machine: Tippe auf deiner Einrichtungsseite neben dem Konto auf **Trennen**. Im Dashboard bringt dich **Neu verbinden oder trennen ↗** unter Verbindungen dorthin.
- Auf deinem eigenen Computer: **Verbindungen**, das Konto öffnen, **Details**, dann **Trennen**.

## Bei Microsoft deinstallieren

Microsoft bietet uns keinen Weg, eine Anmeldung zu widerrufen. Entferne sie also auch dort:

- Geschäfts- oder Schulkonto: myapps.microsoft.com
- Privates Konto: account.live.com/consent/Manage
