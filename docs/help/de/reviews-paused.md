---
title: Keine neue Aufgabe
area: troubleshooting
summary: Prüfungen sind deaktiviert, warten oder wurden wegen des Nutzungslimits deines Modells angehalten. So erkennst du den Grund und kannst handeln.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: d8a15909ab8164e8
---
Aufgaben entstehen durch Prüfungen: Deine Machine prüft, was in den letzten ungefähr 15 Minuten eingegangen ist.

## Gerade angemeldet

Auf einer neuen gehosteten Machine starten die Prüfungen automatisch, sobald deine KI und deine Mail verbunden sind. Während deine Machine deine Mails liest, steht bei „Aufgaben“: „Deine Mails werden gelesen. Die ersten Aufgaben kommen in wenigen Minuten.“ Sobald klar ist, wie viel es zu lesen gibt, steht dort ungefähr, wie lange es dauert: „Die ersten Aufgaben kommen in etwa 10 Min.“ Fehlt ein Schritt, nennt **Braucht dich** den nächsten Schritt, zum Beispiel **Mail verbinden**, und verlinkt ihn.

Während des Lesens zeigt „Aufgaben“, wie weit die Machine ist („20 von 132 Nachrichten gelesen. Die nächsten 40 werden gelesen …“), einige der Personen und Organisationen, auf die sie gestoßen ist, und deine erste Aufgabe, sobald sie da ist. Die Zahl gibt an, wie viele Nachrichten bereits gelesen wurden. Der Balken bewegt sich weiter, während die nächsten Nachrichten gelesen werden. Die Namen stammen aus deinen eigenen Mails und sind nur für dich sichtbar.

Wenn die erste Prüfung nichts für dich findet, steht dort, was gelesen wurde, und es werden nächste Schritte vorgeschlagen. Zum Beispiel kannst du einen Dienst verbinden, von dem du oft Mails erhältst, oder fragen, was sich diese Woche geändert hat.

## Prüfungen sind deaktiviert

Oben bei „Aufgaben“ steht: „Prüfungen sind deaktiviert. Deshalb kommen noch keine Aufgaben.“ Auf einer gehosteten Machine kannst du **Prüfungen einschalten**. Auf deinem eigenen Computer führst du `./install.sh --activate` aus.

## Nutzungslimit deines Modells

Damit genug Kapazität für deine eigenen Chats bleibt, pausieren die Prüfungen bei ungefähr 65 % des 5-Stunden-Limits und 90 % des Wochenlimits deines KI-Tarifs. Mit einem Backup-Modell in einem anderen Tarif müssen die Prüfungen nicht warten. Weitere Informationen findest du unter [Modell](model.md).

Während die Prüfungen warten, steht oben im Dashboard, bis wann sie warten, zum Beispiel: „Prüfungen warten bis 07:15, damit dein ChatGPT-Wochenkontingent reicht.“ **Jetzt prüfen** startet trotzdem eine Prüfung. Unter **Einstellungen**, **Modell** siehst du deine Limits.

Es geht nichts verloren: Sobald es wieder möglich ist, werden die eingegangenen Nachrichten geprüft. Nach einer längeren Wartezeit kommen zuerst die neuesten Nachrichten von Personen dran. Ein Teil jeder Prüfung arbeitet außerdem die ältesten Nachrichten ab.

Bis alles aufgeholt ist, kommen neue Aufgaben ohne Entwurf. So wird dein Kontingent zuerst für deine Nachrichten genutzt. Die Entwürfe kommen später, dringende Aufgaben warten nicht darauf. Drücke **Ausführen**, um jetzt einen Entwurf zu erhalten.

## Nachts

Von 00:00 bis 06:30 pausieren die Prüfungen und neue Nachrichten warten. Um 06:30 werden sie zusammen geprüft, bevor deine morgendliche Zusammenfassung kommt. Unter **Prüfungen** steht: „Nachts pausiert. Wird um 06:30 nachgeholt.“ Nutze die App, schreibe im Chat oder tippe auf eine Aufgabe. Dann laufen die Prüfungen wieder, bis du eine Stunde lang nicht aktiv warst. **Jetzt prüfen** startet sofort eine Prüfung.

## Ein Durchlauf ist fehlgeschlagen

Unter **Verbindungen**, **Prüfungen** zeigt **Letzte Durchläufe** alle Durchläufe an. Ein fehlgeschlagener Durchlauf wird automatisch erneut gestartet. Wenn deine KI nicht mehr antwortet, zum Beispiel weil deine Anmeldung abgelaufen ist, melde dich wieder unter **Einstellungen**, **Modell** an. Die Prüfungen starten dann sofort wieder.

Bei einem Durchlauf, der wegen des Nutzungslimits deines KI-Tarifs angehalten wurde, steht **Das Nutzungslimit deines KI-Tarifs wurde erreicht.** und wann das Limit zurückgesetzt wird. Das ist eine Pause, kein Fehler. Die Nachrichten warten und werden nach dem Zurücksetzen geprüft. Es wird nichts an [Fehlerberichte](error-reports.md) gesendet.

## Beiseitegelegt

Wenn eine Prüfung eine Nachricht zweimal zurückstellt, wird sie beiseitegelegt. Unter **Verbindungen**, **Prüfungen** siehst du, wie viele es sind. Unter **Beiseitegelegt** findest du diese Nachrichten.

Eine Nachricht, die jeden Durchlauf fehlschlagen lässt, obwohl deine KI funktioniert, wird ebenfalls beiseitegelegt, damit die übrigen Nachrichten geprüft werden.

Eine Nachricht von jemandem, der dir schreibt, den du kennst oder der Kunde ist, wird etwa 3 Tage nach Eingang noch einmal geprüft. Dabei wird eine Aufgabe erstellt oder die Nachricht geschlossen. Was du verworfen oder zurückgestellt hast, bleibt so.
