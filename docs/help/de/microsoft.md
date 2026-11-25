---
title: Microsoft Outlook und Kalender
area: connections
summary: Outlook-E-Mails und -Termine für Microsoft 365 und Outlook.com. E-Mails werden erst nach deiner Freigabe gesendet.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 7229063d9365735d
---
## Was gelesen wird

- **Outlook**: alle deine E-Mails. Beim Verbinden die der letzten 7 Tage, danach alle neuen.
- **Outlook-Kalender**: deine Termine, nur lesend.

E-Mails in „Sonstiges“ und Newsletter werden zuerst kurz geprüft: Absender, Betreff und ein paar Wörter. Wenn eine E-Mail wichtig ist, wird sie vollständig gelesen und kann zu einer Aufgabe werden.

## Was gesendet und geändert werden kann

- Eine E-Mail zu einer Aufgabe, aber erst nachdem du sie freigegeben hast. Sie wird von der E-Mail-Adresse des Postfachs gesendet, nicht von einem Alias.
- Eine Antwort wird in der Outlook-Konversation der E-Mail abgelegt, auf die sie antwortet.
- Nach dem Versand einer Antwort werden die Nachrichten des Threads für einige Tage (3, sofern in der Aufgabe nichts anderes steht) in Outlook in den Ordner „Zurückgestellt“ verschoben. Danach kommen sie zurück in den Posteingang oder früher, wenn jemand antwortet. Sie bleiben nie länger als bis zum Fälligkeitsdatum der Aufgabe dort. Vor dem Senden wird dir das bei der Prüfung angezeigt.

Der Kalender wird nie geändert.

## Fotos von Kolleginnen, Kollegen und Kontakten

Microsoft wird außerdem gebeten, grundlegende Profile in deiner Organisation (Name, E-Mail-Adresse und Foto) sowie deine Outlook-Kontakte auszulesen. Deine Machine nutzt sie nur für Fotos, Berufsbezeichnungen und Unternehmen von Personen, die bereits in deinem Graph sind, und zwar für bis zu 200 Fotos pro Tag. Bei Personen ohne Foto wird nach 30 Tagen erneut danach gesucht.

Möglicherweise muss der Admin deiner Organisation die Fotos von Kolleginnen und Kollegen freigeben. Falls nicht, wird Outlook trotzdem verbunden, aber ohne diese Fotos. Für ein Konto, das schon vorher verbunden wurde, gibt es eine Aufgabe: Drück auf **Neu verbinden** oder auf **Nicht nötig**, um sie endgültig zu schließen. Bei einem persönlichen Konto (Outlook.com, Hotmail) gibt es keine Kolleginnen und Kollegen. Die Aufgabe fragt daher nur nach Fotos von Kontakten.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup.
2. Drück auf **Microsoft verbinden** und melde dich an.
3. Wenn Microsoft eine Adminfreigabe verlangt, schick deinem Microsoft 365-Admin den Link (**Link kopieren**). Nach der Freigabe können alle in deiner Organisation die Verbindung herstellen. Wenn du Admin bist, drück auf **Ich bin Admin: jetzt freigeben**.

Oder im Dashboard: **Verbindungen**, **E-Mail**, Outlook auswählen und auf **Mit Microsoft anmelden** drücken. Der Admin-Link steht direkt unter der Schaltfläche.

Auf deinem eigenen Computer, nachdem er [mit deinem Konto gekoppelt wurde](friends.md#a-machine-on-your-own-computer): Öffne **Verbindungen**, dann **E-Mail**, wähle Outlook aus und drück auf **Mit Microsoft anmelden**. E-Mail und Kalender werden zusammen verbunden. Nach der Anmeldung bei Microsoft bist du wieder unter **Verbindungen** in deinem Dashboard.

Für IT-Teams mit eigener Microsoft Entra-App: Öffne dort **Eigene App nutzen** oder führe `assistant connect outlook` aus.

## Verbindung entfernen

- Auf einer gehosteten Machine: Drück auf **Trennen** neben dem Konto auf deiner Einrichtungsseite. Über **Trennen ↗** unter „Verbindungen“ gelangst du dorthin.
- Auf deinem eigenen Computer: Öffne **Verbindungen**, wähle das Konto aus und dann **Details** und **Trennen**.

## In Microsoft deinstallieren

Microsoft lässt uns die Anmeldung nicht widerrufen. Entferne die Verbindung deshalb auch dort:

- Geschäfts- oder Schulkonto: myapps.microsoft.com
- Persönliches Konto: account.live.com/consent/Manage
