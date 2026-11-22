---
title: Gmail
area: connections
summary: Liest deine E-Mails und entwirft Antworten in deinem Stil. E-Mails werden erst gesendet, wenn du sie freigibst.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Was gelesen wird

Alle deine E-Mails: die der letzten 7 Tage, wenn du Gmail verbindest, und danach alle neuen, eingehenden und ausgehenden. Auch gesendete E-Mails zählen dazu. So lernt die KI, wie du schreibst und was du versprochen hast.

Werbemails, Newsletter sowie E-Mails aus Updates und Foren werden zuerst kurz geprüft: Absender, Betreff und ein paar Wörter, oft mehrere auf einmal. Wenn eine E-Mail wichtig ist, wird sie vollständig gelesen und kann zu einer Aufgabe werden. Keine E-Mail bleibt ungesehen.

## Was gesendet werden kann

Eine E-Mail zu einer Aufgabe, und nur nachdem du sie freigegeben hast. Mit **Ausführen** wird ein Entwurf erstellt. **Prüfen und senden** öffnet ihn, damit du ihn bearbeiten kannst. Gesendet wird erst, wenn du **Jetzt senden** drückst. **Mit Google anmelden** bittet Google auch um die Berechtigung zum Senden. Wenn du deine eigene App auf deinem eigenen Computer nutzt, ist die Anmeldung schreibgeschützt, bis du selbst das Senden einrichtest.

**Von** in der Prüfung ist eine kleine Auswahlliste. Sie wird angezeigt, wenn Gmail dieses Postfach erlaubt, als dein Alias zu senden, also als eine deiner Adressen, die in den **Einstellungen** mit **Meine** markiert ist ([Deine Adressen](settings.md#your-addresses)). Eine Antwort auf eine E-Mail, die an diesen Alias ging, wird von dort aus gesendet. Neue E-Mails werden von deiner Postfachadresse gesendet. Unmittelbar vor dem Senden wird Gmail noch einmal gefragt. Wenn Gmail die Adresse nicht bestätigt, wird nichts gesendet.

Eine Antwort landet im Thread der E-Mail, auf die sie antwortet. Wenn sie von einem anderen deiner Postfächer gesendet wird als dem, an das die ursprüngliche E-Mail ging, weist die Aufgabe dich vor dem Senden darauf hin. Die Antwort landet trotzdem im Thread der ursprünglichen E-Mail.

Nach dem Senden einer Antwort wird der Thread für ein paar Tage aus deinem Posteingang in das Label **Zurückgestellt** verschoben. Standardmäßig sind es 3 Tage, außer die Aufgabe gibt etwas anderes an. Danach erscheint er wieder, oder früher, wenn jemand antwortet. Die Prüfung weist dich vor dem Senden darauf hin. Das gilt für dein Postfach: Eine Antwort, die nur die Arbeit verspricht, lässt die Aufgabe offen.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup.
2. Drücke unter **E-Mail und Kalender** auf **Google verbinden** und melde dich an. Auf Googles Anmeldeseite wird Salesflare als Anbieter von The Machine genannt.
3. Gmail und Google Calendar werden gemeinsam verbunden.

Wenn du dich mit Google angemeldet und auf diesem Bildschirm Gmail und Calendar freigegeben hast, werden sie automatisch verbunden. E-Mails werden nur gesendet, wenn du auf „Senden“ drückst.

Oder im Dashboard: Öffne **Verbindungen**, wähle **E-Mail**, dann Gmail und drücke **Mit Google anmelden**. Anschließend kehrst du zum Dashboard zurück.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt ist](friends.md#a-machine-on-your-own-computer):

1. Öffne im Dashboard **Verbindungen**, dann **E-Mail**, und wähle Gmail aus.
2. Drücke **Mit Google anmelden** und melde dich im neuen Tab an. Gmail und Google Calendar werden gemeinsam verbunden.

Wenn dein Computer nicht gekoppelt ist oder du deinen eigenen Google OAuth-Client verwendest, öffne dort **Eigene App nutzen** oder führe `assistant connect gmail` aus. Drücke **Google öffnen**, melde dich an und füge dann die Adresse ein, zu der Google dich weiterleitet. Google Calendar für dieselbe Adresse wird ebenfalls verbunden.

Möglicherweise muss ein Google Workspace-Administrator die App zuerst in der Admin-Konsole zulassen.

## Verbindung entfernen

- Auf einer gehosteten Machine: Drücke auf deiner Einrichtungsseite neben der Adresse **Trennen**. Dadurch werden Gmail und Calendar für diese Adresse getrennt und deine Machine vergisst die Anmeldung. Deine anderen Machines behalten ihre Anmeldungen. Mit **Trennen ↗** unter „Verbindungen“ im Dashboard gelangst du zur Einrichtungsseite. Mit **Neu verbinden** meldest du dich dort erneut an, ohne das Dashboard zu verlassen.
- Auf deinem eigenen Computer: Öffne **Verbindungen**, wähle Gmail und dann **Details** und drücke **Trennen**. Gmail wird dann nicht mehr gelesen. Bereits übertragene Inhalte bleiben erhalten. Wenn kein anderer Dienst diese Google-Anmeldung mehr nutzt, wird sie vergessen. Deine anderen Machines behalten ihre Anmeldungen.

## In Google deinstallieren

Öffne in deinem Google-Konto „Sicherheit“ und dann „Deine Verbindungen zu Drittanbieter-Apps und -Diensten“. Entferne Salesflare (bei „Mit Google anmelden“ oder auf einer gehosteten Machine) oder deine eigene App.
