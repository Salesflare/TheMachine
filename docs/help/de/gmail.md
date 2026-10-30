---
title: Gmail
area: connections
summary: Liest deine Mails und entwirft Antworten in deinem Ton. Sendet eine E-Mail erst, nachdem du sie freigegeben hast.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
---
## Was es liest

Alle deine Mails: die letzten 7 Tage beim Verbinden, danach alles Neue, eingehend und ausgehend. Mails, die du sendest, zählen auch, damit es lernt, wie du schreibst und was du versprochen hast.

Mails aus Werbung, Newslettern, Benachrichtigungen und Foren werden zuerst kurz angesehen: Absender, Betreff und ein paar Wörter, viele auf einmal. Wenn eine wichtig ist, wird sie ganz gelesen und kann zu einer Aufgabe werden. Nichts wird ungesehen übersprungen.

## Was es senden kann

Eine E-Mail aus einer Aufgabe, und nur, nachdem du sie freigegeben hast. **Ausführen** bereitet einen Entwurf vor. **Prüfen und senden** öffnet ihn, bereit zum Bearbeiten, und nichts geht raus, bis du auf **Jetzt senden** tippst. **Mit Google anmelden** bittet Google auch um das Senden. Mit deiner eigenen App auf deinem eigenen Computer ist die Anmeldung nur lesend, bis du das Senden selbst hinzufügst.

Eine Antwort landet im Verlauf der E-Mail, auf die sie antwortet. Geht sie von einem anderen Postfach raus als dem, in dem die E-Mail ankam, sagt die Aufgabe das vor dem Senden: Bei der Gegenseite landet sie trotzdem im selben Verlauf.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup.
2. Tippe unter **Mail und Kalender** auf **Google verbinden** und melde dich an. Auf dem Google-Bildschirm steht Salesflare, die Firma hinter The Machine.
3. Gmail und Google Calendar werden zusammen verbunden.

Oder im Dashboard: **Verbindungen**, **+ Hinzufügen**, wähle Gmail und tippe auf **Mit Google anmelden**. Danach bist du zurück im Dashboard.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt](fleet.md) ist:

1. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle Gmail.
2. Tippe auf **Mit Google anmelden** und melde dich in dem Tab an, der sich öffnet. Gmail und Google Calendar werden zusammen verbunden.

Nicht gekoppelt, oder mit deinem eigenen Google-OAuth-Client: Öffne dort **Eigene App nutzen** oder führe `assistant connect gmail` aus. Es nutzt gog. Öffne die angezeigte Adresse und melde dich an.

Ein Google-Workspace-Admin muss die App unter Umständen zuerst in der Admin-Konsole erlauben.

## Entfernen

- Auf einer gehosteten Machine: Tippe auf deiner Einrichtungsseite neben der Adresse auf **Trennen**. Das entfernt Gmail und Kalender für diese Adresse und widerruft die Anmeldung bei Google. Im Dashboard bringt dich **Trennen ↗** unter Verbindungen dorthin. **Neu verbinden** dort meldet dich erneut an, ohne das Dashboard zu verlassen.
- Auf deinem eigenen Computer: **Verbindungen**, Gmail öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt. Wenn nichts anderes diese Google-Anmeldung nutzt, wird sie bei Google widerrufen.

## Bei Google deinstallieren

Öffne in deinem Google-Konto Sicherheit, dann Deine Verbindungen zu Drittanbieter-Apps und -Diensten, und entferne Salesflare (Mit Google anmelden oder gehostet) oder deine eigene App.
