---
title: Keine neuen Aufgaben
area: troubleshooting
summary: Prüfungen sind ausgeschaltet, warten oder wurden wegen des Nutzungslimits deines Modells angehalten. So erkennst du den Grund und weißt, was zu tun ist.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: 07aca53acc41694d
---
Aufgaben entstehen durch Prüfungen: Deine Machine prüft etwa alle 15 Minuten, was eingegangen ist.

## Gerade registriert

Bei einer neuen gehosteten Machine starten die Prüfungen automatisch, sobald deine KI und deine Mail verbunden sind. Während deine Machine deine Mails liest, steht bei Aufgaben: „Deine Mails werden gelesen. Die ersten Aufgaben kommen in ein paar Minuten.“ Sobald sie weiß, wie viel zu lesen ist, nennt sie eine ungefähre Dauer: „Die ersten Aufgaben kommen in etwa 10 Min.“ Fehlt noch ein Schritt, nennt **Braucht dich** ihn, zum Beispiel **Mail verbinden**, mit einem Link zu diesem Schritt.

Während deine Machine liest, zeigen Aufgaben an, wie weit sie ist („20 von 132 Nachrichten gelesen. Die nächsten 40 werden gelesen …“), einige Personen und Organisationen, auf die sie gestoßen ist, und deine erste Aufgabe, sobald sie vorliegt. Die Zahl zählt die Nachrichten, die sie bereits gelesen hat. Während sie die nächsten Nachrichten liest, bewegt sich der Fortschrittsbalken weiter. Die Namen stammen aus deinen Mails und sind nur für dich sichtbar.

Wenn der erste Durchlauf nichts für dich ergibt, steht dort, was gelesen wurde, und es werden nächste Schritte vorgeschlagen. Du kannst zum Beispiel einen Dienst verbinden, von dem du oft Mails bekommst, oder fragen, was sich diese Woche geändert hat.

## Prüfungen sind ausgeschaltet

Oben bei Aufgaben steht: „Prüfungen sind ausgeschaltet. Es kommen noch keine Aufgaben an.“ Auf einer gehosteten Machine tippe auf **Prüfungen einschalten**. Auf deinem eigenen Computer führe `./install.sh --activate` aus.

## Das Nutzungslimit deines Modells

Damit genug Kapazität für deine Chats bleibt, werden Prüfungen pausiert, sobald etwa 65 % des 5-Stunden-Limits oder 90 % des Wochenlimits deines KI-Tarifs erreicht sind. Wenn du ein Backup-Modell in einem anderen Tarif eingerichtet hast, warten die Prüfungen nicht. Weitere Informationen findest du unter [Modell](model.md).

Während die Prüfungen warten, steht oben im Dashboard, bis wann sie pausiert sind, zum Beispiel: „Prüfungen warten bis 07:15, damit dein ChatGPT-Wochenlimit geschont wird.“ Mit **Jetzt prüfen** kannst du trotzdem eine Prüfung starten. Unter **Einstellungen**, **Modell** siehst du deine Limits.

Es geht nichts verloren: Eingegangene Nachrichten werden geprüft, sobald es möglich ist.

## Nachts

Zwischen 00:00 und 06:30 pausieren die Prüfungen, und neue Nachrichten warten. Um 06:30 werden sie alle zusammen geprüft, bevor deine Morgenübersicht erstellt wird. Unter **Prüfungen** steht: „Nachts pausiert. Wird um 06:30 nachgeholt.“ Wenn du die App verwendest, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wieder, bis du eine Stunde lang abwesend warst. Mit **Jetzt prüfen** wird sofort geprüft.

## Ein Durchlauf ist fehlgeschlagen

Unter **Verbindungen**, **Prüfungen** zeigt **Letzte Durchläufe** jeden Durchlauf an. Ein fehlgeschlagener Durchlauf wird automatisch erneut versucht.

Bei einem Durchlauf, der wegen des Nutzungslimits deines KI-Tarifs angehalten wurde, steht **Das Nutzungslimit der KI wurde erreicht.** und wann es wieder aufgehoben wird. Das ist eine Pause, kein Fehler: Die Nachrichten warten und werden nach dem Zurücksetzen des Limits geprüft. Es wird nichts an [Fehlerberichte](error-reports.md) gesendet.

## Beiseitegelegt

Wenn eine Prüfung eine Nachricht zweimal zurückstellt, wird sie beiseitegelegt. Unter **Verbindungen**, **Prüfungen** siehst du, wie viele es sind. Unter **Beiseitegelegt** findest du die Nachrichten. Bei einer Nachricht von jemandem, der dir schreibt, den du kennst oder der Kunde ist, wird etwa 3 Tage nach Eingang noch einmal geprüft. Dabei wird eine Aufgabe erstellt oder die Nachricht geschlossen. Was du verworfen oder zurückgestellt hast, bleibt so.
