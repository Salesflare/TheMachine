---
title: Gmail
area: connections
summary: Liest deine E-Mails und verfasst Antwortentwürfe in deinem Stil. E-Mails werden erst gesendet, wenn du sie freigibst.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Was gelesen wird

Alle deine E-Mails: die letzten 7 Tage, wenn du die Verbindung herstellst, danach alle neuen, eingehenden und ausgehenden. Auch gesendete E-Mails zählen. So lernt die KI, wie du schreibst und was du versprochen hast.

Werbung, Newsletter sowie E-Mails aus den Kategorien Updates und Foren werden zuerst kurz geprüft: Absender, Betreff und ein paar Wörter, oft mehrere auf einmal. Wenn eine Nachricht wichtig ist, wird sie vollständig gelesen und kann zu einer Aufgabe werden. Nichts wird ungesehen übersprungen.

## Was gesendet werden kann

Eine E-Mail zu einer Aufgabe, und erst, nachdem du sie freigegeben hast. **Ausführen** erstellt einen Entwurf. **Prüfen und senden** öffnet ihn zum Bearbeiten. Gesendet wird erst, wenn du **Jetzt senden** drückst. **Mit Google anmelden** bittet Google auch um die Berechtigung zum Senden. Mit deiner eigenen App auf deinem eigenen Computer ist der Zugriff zunächst nur lesend, bis du das Senden selbst hinzufügst.

**Von** ist in der Prüfung ein kleines Auswahlmenü, wenn Gmail dieses Postfach als deinen Alias senden lassen kann. Das ist in den Einstellungen unter [Deine Adressen](settings.md#your-addresses) mit **Meine** markiert. Eine Antwort auf eine E-Mail, die an diesen Alias ging, wird von dort gesendet. Neue E-Mails werden von deiner Postfachadresse gesendet. Direkt vor dem Senden wird Gmail erneut gefragt. Bestätigt Gmail die Adresse nicht, wird nichts gesendet.

Eine Antwort erscheint im Thread der E-Mail, auf die sie antwortet. Wenn sie von einem anderen deiner Postfächer gesendet wird als dem, an das die E-Mail ging, weist die Aufgabe vor dem Senden darauf hin. Die Antwort landet trotzdem im Thread der ursprünglichen E-Mail.

Nach dem Senden einer Antwort wird der Thread für einige Tage aus deinem Posteingang entfernt und mit dem Label „Zurückgestellt“ versehen. Standardmäßig sind es 3 Tage, sofern in der Aufgabe nichts anderes steht. Danach erscheint er wieder, oder früher, wenn jemand antwortet. Die Prüfung weist dich vor dem Senden darauf hin. So funktioniert dein Postfach: Eine Antwort, die die Erledigung nur verspricht, lässt die Aufgabe offen.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup.
2. Drücke unter **E-Mail und Kalender** auf **Google verbinden** und melde dich an. Auf dem Google-Bildschirm wird Salesflare als Anbieter von The Machine genannt.
3. Gmail und Google Kalender werden zusammen verbunden.

Hast du dich mit Google registriert und auf diesem Bildschirm den Zugriff auf Gmail und Google Kalender erlaubt? Dann werden beide automatisch verbunden. Gesendet wird nur, wenn du **Senden** drückst.

Oder im Dashboard: **Verbindungen**, **E-Mail**, Gmail auswählen und auf **Mit Google anmelden** drücken. Danach gelangst du zurück zum Dashboard.

Auf deinem eigenen Computer, sobald er [mit deinem Konto gekoppelt ist](friends.md#a-machine-on-your-own-computer):

1. Öffne im Dashboard **Verbindungen**, dann **E-Mail**, und wähle Gmail aus.
2. Drücke auf **Mit Google anmelden** und melde dich im geöffneten Tab an. Gmail und Google Kalender werden zusammen verbunden.

Nicht gekoppelt oder mit deinem eigenen Google-OAuth-Client? Öffne dort **Eigene App nutzen** oder führe `assistant connect gmail` aus. Drücke auf **Google öffnen**, melde dich an und füge dann die Adresse ein, zu der Google dich weiterleitet. Google Kalender für dieselbe Adresse wird ebenfalls verbunden.

Möglicherweise muss ein Google-Workspace-Administrator die App zuerst in der Admin-Konsole zulassen.

## Verbindung entfernen

- Auf einer gehosteten Machine: Drücke auf deiner Einrichtungsseite neben der Adresse auf **Trennen**. Dadurch werden Gmail und Kalender für diese Adresse getrennt und deine Machine vergisst die Anmeldung. Deine anderen Machines behalten ihre Anmeldungen. Im Dashboard gelangst du über **Trennen ↗** unter **Verbindungen** dorthin. Mit **Neu verbinden** meldest du dich dort wieder an, ohne das Dashboard zu verlassen.
- Auf deinem eigenen Computer: Öffne **Verbindungen**, wähle Gmail aus, dann **Details** und **Trennen**. Damit hört deine Machine auf, E-Mails zu lesen. Bereits importierte Inhalte bleiben erhalten. Wenn nichts anderes auf deiner Machine diese Google-Anmeldung nutzt, vergisst deine Machine sie. Deine anderen Machines behalten ihre Anmeldungen.

## Bei Google deinstallieren

Öffne in deinem Google-Konto den Bereich „Sicherheit“ und dann „Verbindungen zu Drittanbieter-Apps und -Diensten“. Entferne dort Salesflare (über „Mit Google anmelden“ oder die gehostete Version) oder deine eigene App.
