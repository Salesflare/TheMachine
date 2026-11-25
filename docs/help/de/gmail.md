---
title: Gmail
area: connections
summary: Liest deine E-Mails und entwirft Antworten in deinem Stil. Eine E-Mail wird erst gesendet, wenn du sie freigibst.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: f0565a7bf839f49f
---
## Was gelesen wird

Alle deine E-Mails: die letzten 7 Tage ab dem Verbinden und danach alle neuen, eingehenden und ausgehenden. Auch gesendete E-Mails zählen, damit deine Machine lernt, wie du schreibst und was du versprochen hast.

Werbeaktionen, Newsletter sowie E-Mails aus den Kategorien „Aktualisierungen“ und „Foren“ werden zuerst kurz angesehen: Absender, Betreff und ein paar Wörter, viele auf einmal. Wenn eine davon wichtig ist, wird sie vollständig gelesen und kann zu einer Aufgabe werden. Nichts wird ungesehen übersprungen.

## Was gesendet werden kann

Eine E-Mail aus einer Aufgabe, und nur nachdem du sie freigegeben hast. **Ausführen** erstellt einen Entwurf. Mit **Prüfen und senden** öffnest du ihn und kannst ihn bearbeiten. Gesendet wird erst, wenn du **Jetzt senden** drückst. **Mit Google anmelden** bittet Google auch um die Berechtigung zum Senden. Wenn du deine eigene App auf deinem eigenen Computer verwendest, ist die Anmeldung zunächst schreibgeschützt. Das Senden musst du selbst hinzufügen.

**Von** in der Prüfung ist eine kleine Auswahlliste, wenn Gmail für dieses Postfach den Versand über einen deiner Aliasse erlaubt (einen, der in den Einstellungen als **Meine** markiert ist, unter [Deine Adressen](settings.md#your-addresses)). Eine Antwort auf eine E-Mail, die an diesen Alias ging, wird von dort gesendet. Neue E-Mails werden von deiner Postfachadresse gesendet. Unmittelbar vor dem Senden wird Gmail erneut gefragt. Bestätigt Gmail die Adresse nicht, wird nichts gesendet.

Eine Antwort erscheint im Thread der E-Mail, auf die sie antwortet. Wenn sie von einem anderen deiner Postfächer gesendet wird als dem, in dem die E-Mail eingegangen ist, weist die Aufgabe dich vor dem Senden darauf hin. Die Antwort erscheint trotzdem in ihrem Thread.

Nach dem Senden einer Antwort wird der Thread für einige Tage aus deinem Posteingang entfernt und mit dem Label „Zurückgestellt“ versehen (3 Tage, sofern in der Aufgabe nichts anderes steht). Danach erscheint er wieder oder früher, wenn jemand antwortet. Er bleibt nie länger als bis zum Fälligkeitsdatum der Aufgabe zurückgestellt: Am Arbeitstag davor erscheint er wieder. Ist die Aufgabe heute fällig, bleibt er in deinem Posteingang. Die Prüfung weist dich vor dem Senden darauf hin. Das ist dein Postfach: Eine Antwort, die die Aufgabe nur verspricht, lässt sie offen.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup.
2. Drücke unter **E-Mail und Kalender** auf **Google verbinden** und melde dich an. Auf der Google-Seite wird Salesflare als Anbieter von The Machine genannt.
3. Gmail und Google Calendar werden zusammen verbunden.

Wenn du dich mit Google registriert und auf diesem Bildschirm Gmail und Calendar erlaubt hast, werden sie automatisch verbunden. E-Mails werden nur gesendet, wenn du auf „Senden“ drückst.

Oder über das Dashboard: Öffne **Verbindungen**, dann **E-Mail**, wähle Gmail aus und drücke auf **Mit Google anmelden**. Danach kehrst du zum Dashboard zurück.

Auf deinem eigenen Computer, nachdem du ihn [mit deinem Konto gekoppelt hast](friends.md#a-machine-on-your-own-computer):

1. Öffne im Dashboard **Verbindungen**, dann **E-Mail**, und wähle Gmail aus.
2. Drücke auf **Mit Google anmelden** und melde dich im geöffneten Tab an. Gmail und Google Calendar werden zusammen verbunden.

Wenn dein Computer nicht gekoppelt ist oder du deinen eigenen Google OAuth-Client verwendest, öffne dort **Eigene App nutzen** oder führe `assistant connect gmail` aus. Drücke auf **Google öffnen**, melde dich an und füge dann die Adresse ein, zu der Google dich weiterleitet. Google Calendar für dieselbe Adresse wird ebenfalls verbunden.

Ein Google Workspace-Administrator muss die App möglicherweise zuerst in der Admin-Konsole zulassen.

## Trennen

- Auf einer gehosteten Machine: Drücke auf deiner Einrichtungsseite neben der Adresse auf **Trennen**. Gmail und Calendar werden für diese Adresse getrennt und deine Machine vergisst die Anmeldung. Deine anderen Machines behalten ihre Anmeldungen. Über **Trennen ↗** unter „Verbindungen“ im Dashboard gelangst du dorthin. Mit **Neu verbinden** meldest du dich dort erneut an, ohne das Dashboard zu verlassen.
- Auf deinem eigenen Computer: Öffne **Verbindungen**, dann Gmail und **Details**, und drücke auf **Trennen**. Gmail wird nicht mehr gelesen. Bereits importierte Inhalte bleiben erhalten. Wenn kein anderer Dienst diese Google-Anmeldung verwendet, wird sie vergessen. Deine anderen Machines behalten ihre Anmeldungen.

## In Google deinstallieren

Öffne in deinem Google-Konto „Sicherheit“ und dann „Verbindungen zu Drittanbieter-Apps und -Diensten“. Entferne dort Salesflare (bei „Mit Google anmelden“ oder gehosteter Nutzung) oder deine eigene App.
