---
title: Keine neue Aufgabe
area: troubleshooting
summary: Prüfungen sind ausgeschaltet, warten oder wurden wegen des Nutzungslimits deines Modells angehalten. So erkennst du den Grund und weißt, was du tun kannst.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: 40617b8ac692660b
---
Aufgaben entstehen durch Prüfungen: Deine Machine sieht sich ungefähr alle 15 Minuten an, was eingegangen ist.

## Gerade angemeldet

Bei einer neuen gehosteten Machine starten die Prüfungen automatisch, sobald deine KI und deine Mail verbunden sind. Während deine Machine deine Mail liest, steht unter „Aufgaben“: „Deine Mail wird gelesen. Die ersten Aufgaben folgen in wenigen Minuten.“ Sobald sie weiß, wie viel zu lesen ist, zeigt sie ungefähr an, wie lange es dauert: „Die ersten Aufgaben folgen in etwa 10 Min.“ Fehlt noch ein Schritt, nennt **Braucht dich** den nächsten Schritt, zum Beispiel **Mail verbinden**, und verlinkt ihn.

Während des Lesens zeigt „Aufgaben“, wie weit die Machine gekommen ist („20 von 132 Nachrichten gelesen. Die nächsten 40 werden gelesen …“), einige Personen und Organisationen, auf die sie gestoßen ist, und die erste Aufgabe, sobald sie vorliegt. Die Zahl zählt die Nachrichten, die sie fertig gelesen hat. Der Balken bewegt sich weiter, während sie die nächsten Nachrichten liest. Die Namen stammen aus deiner eigenen Mail und sind nur für dich sichtbar.

Wenn die erste Prüfung nichts für dich findet, steht dort, was gelesen wurde, und es werden nächste Schritte vorgeschlagen, zum Beispiel einen Dienst zu verbinden, von dem du oft Mails bekommst, oder zu fragen, was sich diese Woche geändert hat.

## Prüfungen sind ausgeschaltet

Oben in „Aufgaben“ steht: „Prüfungen sind ausgeschaltet. Es kommen noch keine Aufgaben an.“ Auf einer gehosteten Machine drückst du **Prüfungen einschalten**. Auf deinem eigenen Computer führst du `./install.sh --activate` aus.

## Nutzungslimit deines Modells

Damit genug Spielraum für deine eigenen Chats bleibt, pausieren Prüfungen bei etwa 65 % des 5-Stunden-Limits deines KI-Tarifs und bei 90 % des Wochenlimits. Wenn du ein Backup-Modell mit einem anderen Tarif eingerichtet hast, warten die Prüfungen nicht. Weitere Infos findest du unter [Modell](model.md).

Während Prüfungen warten, steht oben im Dashboard, bis wann, zum Beispiel: „Prüfungen warten bis 07:15, damit dein ChatGPT-Wochenlimit geschont wird.“ Mit **Jetzt prüfen** startest du trotzdem eine Prüfung. Unter **Einstellungen** und **Modell** siehst du deine Limits.

Es geht nichts verloren: Sobald es wieder möglich ist, werden eingegangene Nachrichten geprüft. Nach einer längeren Wartezeit kommen aktuelle Nachrichten von Personen zuerst dran. Ein Teil jeder Prüfung arbeitet außerdem die ältesten Nachrichten ab.

Bis alles aufgeholt ist, kommen neue Aufgaben ohne Entwurf an, damit dein Tarif zuerst für deine Nachrichten genutzt wird. Die Entwürfe folgen später. Dringende Aufgaben warten nicht darauf. Drücke **Ausführen**, um sofort einen Entwurf zu erstellen.

## Nachts

Von 00:00 bis 06:30 pausieren die Prüfungen und neue Nachrichten warten. Um 06:30 werden sie zusammen geprüft, bevor deine morgendliche Zusammenfassung kommt. Unter **Prüfungen** steht: „Nachts pausiert. Wird um 06:30 nachgeholt.“ Wenn du die App verwendest, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wieder. Sie pausieren erst, wenn du eine Stunde lang inaktiv warst. Mit **Jetzt prüfen** wird sofort geprüft.

## Ein Durchlauf ist fehlgeschlagen

Unter **Verbindungen** und **Prüfungen** zeigt **Letzte Durchläufe** jeden Durchlauf an. Ein fehlgeschlagener Durchlauf wird automatisch erneut versucht.

Bei einem Durchlauf, der wegen des Nutzungslimits deines KI-Tarifs angehalten wurde, steht **Das KI-Nutzungslimit wurde erreicht.** und wann das Limit zurückgesetzt wird. Das ist eine Pause, kein Fehler: Die Nachrichten warten und werden nach dem Zurücksetzen geprüft. Es wird nichts an [Fehlerberichte](error-reports.md) gesendet.

## Beiseitegelegt

Wenn eine Prüfung eine Nachricht zweimal zurückstellt, wird sie beiseitegelegt. Unter **Verbindungen** und **Prüfungen** siehst du, wie viele es sind. Unter **Beiseitegelegt** findest du die Nachrichten. Nachrichten von einer Person, die dir schreibt, jemandem, den du kennst, oder einem Kunden werden etwa 3 Tage nach ihrem Eingang noch einmal geprüft. Dabei wird eine Aufgabe erstellt oder die Nachricht geschlossen. Was du verworfen oder zurückgestellt hast, bleibt so.
