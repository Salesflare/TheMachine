---
title: Gmail
area: connections
summary: Liest deine E-Mails und entwirft Antworten in deinem Stil. E-Mails werden erst gesendet, wenn du sie freigibst.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: c1f2362cd496840e
---
## Was gelesen wird

Alle deine E-Mails: die der letzten 7 Tage, wenn du die Verbindung herstellst, und danach alle neuen, ein- und ausgehenden. Auch gesendete E-Mails zählen. So lernt The Machine, wie du schreibst und was du versprochen hast.

Werbung, Newsletter, Updates und E-Mails aus Foren werden zuerst kurz geprüft: Absender, Betreff und ein paar Wörter, oft mehrere auf einmal. Wenn eine E-Mail wichtig ist, wird sie vollständig gelesen und kann zu einer Aufgabe werden. Nichts wird ungesehen übersprungen.

## Was gesendet werden kann

Eine E-Mail zu einer Aufgabe, und erst, nachdem du sie freigegeben hast. Mit **Ausführen** wird ein Entwurf vorbereitet. **Prüfen und senden** öffnet ihn, damit du ihn bearbeiten kannst. Gesendet wird erst, wenn du auf **Jetzt senden** drückst. **Mit Google anmelden** bittet Google auch um die Berechtigung zum Senden. Wenn du deine eigene App auf deinem eigenen Computer verwendest, ist die Anmeldung nur lesend, bis du selbst den Versand einrichtest.

**Von** in der Prüfung ist ein kleines Auswahlmenü. Es wird angezeigt, wenn Gmail für dieses Postfach den Versand über einen deiner Aliasse zulässt, der in den **Einstellungen** unter [Deine Adressen](settings.md#your-addresses) mit **Meine** gekennzeichnet ist. Eine Antwort auf eine E-Mail, die an diesen Alias geschickt wurde, wird von dieser Adresse aus gesendet. Neue E-Mails werden von deiner Postfachadresse aus gesendet. Unmittelbar vor dem Senden wird Gmail noch einmal gefragt. Wenn Gmail die Adresse nicht bestätigt, wird nichts gesendet.

Eine Antwort wird in den Thread der E-Mail eingefügt, auf die sie antwortet. Wenn sie von einem anderen deiner Postfächer gesendet wird als dem, an das die E-Mail ging, weist dich die Aufgabe darauf hin, bevor du sendest. Die Antwort landet trotzdem im Thread der ursprünglichen E-Mail.

Nachdem eine Antwort gesendet wurde, wird der Thread für ein paar Tage (3, sofern in der Aufgabe nichts anderes steht) mit dem Label „Zurückgestellt“ aus deinem Posteingang verschoben. Danach kommt er zurück oder früher, wenn jemand antwortet. Die Prüfung weist dich darauf hin, bevor du sendest.

## Verbindung herstellen

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup.
2. Drücke unter **E-Mail und Kalender** auf **Google verbinden** und melde dich an. Auf dem Google-Bildschirm wird Salesflare genannt, das Unternehmen hinter The Machine.
3. Gmail und Google Kalender werden gemeinsam verbunden.

Wenn du dich mit Google angemeldet und auf diesem Bildschirm den Zugriff auf Gmail und Kalender erlaubt hast, werden sie automatisch verbunden. E-Mails werden nur gesendet, wenn du auf „Senden“ drückst.

Oder im Dashboard: **Verbindungen**, **E-Mail**, Gmail auswählen und auf **Mit Google anmelden** drücken. Danach kehrst du zum Dashboard zurück.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt ist](friends.md#a-machine-on-your-own-computer):

1. Öffne im Dashboard **Verbindungen**, dann **E-Mail**, und wähle Gmail aus.
2. Drücke auf **Mit Google anmelden** und melde dich im geöffneten Tab an. Gmail und Google Kalender werden gemeinsam verbunden.

Wenn dein Computer nicht gekoppelt ist oder du deinen eigenen Google OAuth-Client verwendest, öffne dort **Eigene App nutzen** oder führe `assistant connect gmail` aus. Drücke auf **Google öffnen**, melde dich an und füge dann die Adresse ein, zu der Google dich weiterleitet. Google Kalender für dieselbe Adresse wird ebenfalls verbunden.

Möglicherweise muss ein Google Workspace-Administrator die App zuerst in der Admin-Konsole zulassen.

## Verbindung entfernen

- Auf einer gehosteten Machine: Drücke auf deiner Einrichtungsseite neben der Adresse auf **Trennen**. Gmail und Kalender für diese Adresse werden entfernt und deine Machine vergisst die Anmeldung. Auf deinen anderen Machines bleibt ihre Anmeldung bestehen. Über **Trennen ↗** bei Verbindungen im Dashboard gelangst du zur Einrichtungsseite. Über **Neu verbinden** kannst du dich dort erneut anmelden, ohne das Dashboard zu verlassen.
- Auf deinem eigenen Computer: Öffne **Verbindungen**, wähle Gmail und dann **Details**. Drücke anschließend auf **Trennen**. Danach wird nichts mehr gelesen. Was bereits importiert wurde, bleibt erhalten. Wenn nichts anderes auf diesem Computer diese Google-Anmeldung verwendet, wird sie vergessen. Auf deinen anderen Machines bleibt ihre Anmeldung bestehen.

## App bei Google deinstallieren

Öffne in deinem Google-Konto den Bereich „Sicherheit“, dann „Deine Verbindungen zu Drittanbieter-Apps und -Diensten“, und entferne Salesflare (Mit Google anmelden oder gehostet) oder deine eigene App.
