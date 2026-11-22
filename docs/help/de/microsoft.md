---
title: Microsoft Outlook und Kalender
area: connections
summary: Outlook-E-Mails und -Termine für Microsoft 365 und Outlook.com. E-Mails werden erst nach deiner Freigabe gesendet.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: c10bf70a327b8ec0
---
## Was gelesen wird

- **Outlook**: alle deine E-Mails, beim Verbinden die der letzten 7 Tage und danach alle neuen.
- **Outlook-Kalender**: deine Termine, nur lesend.

E-Mails unter „Other“ und Newsletter werden zuerst kurz geprüft: Absender, Betreff und ein paar Wörter. Wenn eine wichtig ist, wird sie vollständig gelesen und kann zu einer Aufgabe werden.

## Was gesendet und geändert werden kann

- Eine E-Mail aus einer Aufgabe, aber erst nachdem du sie freigegeben hast. Sie wird von der Adresse des Postfachs selbst gesendet, nicht von einem Alias.
- Eine Antwort landet in der Outlook-Unterhaltung der E-Mail, auf die sie antwortet.
- Nach dem Versand einer Antwort werden die Nachrichten des Threads für einige Tage (3, sofern in der Aufgabe nichts anderes steht) in Outlook in den Ordner „Zurückgestellt“ verschoben. Danach kommen sie zurück in den Posteingang oder früher, wenn jemand antwortet. In der Prüfung vor dem Senden wird darauf hingewiesen.

Der Kalender wird nie geändert.

## Fotos von Kolleginnen, Kollegen und Kontakten

Microsoft wird außerdem gebeten, grundlegende Profile in deiner Organisation (Name, E-Mail-Adresse und Foto) sowie deine Outlook-Kontakte zu lesen. Deine Machine nutzt diese Daten nur für Fotos, Berufsbezeichnungen und Unternehmen von Personen, die bereits in deinem Graph sind, mit höchstens 200 Fotos pro Tag. Personen ohne Foto werden nach 30 Tagen erneut geprüft.

Der Admin deiner Organisation muss die Fotos von Kolleginnen und Kollegen möglicherweise freigeben. Falls nicht, wird Outlook trotzdem verbunden, aber ohne diese Fotos. Ein Konto, das schon vorher verbunden wurde, erhält eine Aufgabe: Drücke **Neu verbinden** oder **Nicht nötig**, um sie endgültig zu schließen. Bei einem persönlichen Konto (Outlook.com, Hotmail) gibt es keine Kolleginnen und Kollegen. Die Aufgabe betrifft daher nur Fotos von Kontakten.

## Verbinden

Bei einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup.
2. Drücke **Microsoft verbinden** und melde dich an.
3. Wenn Microsoft eine Adminfreigabe verlangt, schicke deinem Microsoft 365-Admin den Link (**Link kopieren**). Sobald die Freigabe erteilt ist, kann sich jede Person in deiner Organisation verbinden. Wenn du der Admin bist, drücke **Ich bin der Admin: Jetzt freigeben**.

Oder im Dashboard: **Verbindungen**, **E-Mail**, wähle Outlook und drücke **Mit Microsoft anmelden**. Der Admin-Link steht direkt unter der Schaltfläche.

Auf deinem eigenen Computer: Sobald deine Machine [mit deinem Konto gekoppelt ist](friends.md#a-machine-on-your-own-computer), öffne **Verbindungen**, dann **E-Mail**, wähle Outlook und drücke **Mit Microsoft anmelden**. E-Mail und Kalender werden zusammen verbunden. Nach der Anmeldung bei Microsoft bist du wieder unter **Verbindungen** in deinem Dashboard.

Für IT-Teams mit einer eigenen Microsoft Entra-App: Öffne dort **Eigene App nutzen** oder führe `assistant connect outlook` aus.

## Verbindung trennen

- Bei einer gehosteten Machine: Drücke auf deiner Einrichtungsseite neben dem Konto **Trennen**. **Trennen ↗** unter Verbindungen bringt dich dorthin.
- Auf deinem eigenen Computer: **Verbindungen**, öffne das Konto, **Details**, dann **Trennen**.

## In Microsoft deinstallieren

Microsoft erlaubt uns nicht, eine Anmeldung zu widerrufen. Entferne die Verbindung daher auch dort:

- Geschäfts- oder Schulkonto: myapps.microsoft.com
- Persönliches Konto: account.live.com/consent/Manage
