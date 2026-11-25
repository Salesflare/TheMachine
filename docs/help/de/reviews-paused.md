---
title: Keine neue Aufgabe
area: troubleshooting
summary: Prüfungen sind ausgeschaltet, warten oder wurden wegen des Nutzungslimits deines Modells angehalten. So erkennst du den Grund und weißt, was zu tun ist.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: f0e9e4dc6c850b25
---
Aufgaben entstehen durch Prüfungen: Deine Machine prüft etwa alle 15 Minuten, was eingegangen ist.

## Gerade angemeldet

Bei einer neuen gehosteten Machine starten die Prüfungen automatisch, sobald deine KI und deine Mail verbunden sind. Während deine Machine deine Mails liest, steht unter „Aufgaben“: „Deine Mails werden gelesen. Die ersten Aufgaben folgen in wenigen Minuten.“ Sobald sie weiß, wie viele Mails es gibt, zeigt sie ungefähr an, wie lange es dauert: „Die ersten Aufgaben gibt es in etwa 10 Min.“ Fehlt noch ein Schritt, steht unter **Braucht dich**, was zu tun ist, zum Beispiel **Mail verbinden**, mit einem Link zu diesem Schritt.

Während deine Machine liest, zeigt „Aufgaben“, wie weit sie ist („20 von 132 Nachrichten gelesen. Die nächsten 40 werden gelesen …“), einige der Personen und Organisationen, auf die sie gestoßen ist, und deine erste Aufgabe, sobald sie da ist. Die Zahl zählt die Nachrichten, die sie fertig gelesen hat. Der Balken bewegt sich weiter, während sie die nächsten Nachrichten liest. Die Namen stammen aus deinen Mails und sind nur für dich sichtbar.

Wenn die erste Prüfung nichts für dich findet, steht dort, was gelesen wurde. Außerdem werden nächste Schritte vorgeschlagen, zum Beispiel einen Dienst zu verbinden, von dem du oft Mails bekommst, oder im Chat zu fragen, was sich diese Woche geändert hat.

## Prüfungen sind ausgeschaltet

Oben unter „Aufgaben“ steht: „Prüfungen sind ausgeschaltet. Es kommen also noch keine Aufgaben an.“ Auf einer gehosteten Machine drückst du **Prüfungen einschalten**. Auf deinem eigenen Computer führst du `./install.sh --activate` aus.

## Das Nutzungslimit deines Modells

Damit genug Spielraum für deine Chats bleibt, pausieren Prüfungen bei etwa 65 % des 5-Stunden-Limits und 90 % des Wochenlimits deines KI-Tarifs. Mit einem Backup-Modell in einem anderen Tarif müssen Prüfungen nicht warten. Weitere Infos findest du unter [Modell](model.md).

Während Prüfungen warten, steht oben im Dashboard, bis wann sie warten, zum Beispiel: „Prüfungen warten bis 07:15, damit du dein ChatGPT-Wochenlimit schonst.“ **Jetzt prüfen** startet trotzdem eine Prüfung. Unter **Einstellungen**, **Modell** siehst du deine Limits.

Es geht nichts verloren: Sobald es wieder möglich ist, werden die eingegangenen Nachrichten geprüft. Nach einer längeren Wartezeit werden zuerst die neuesten Nachrichten von Personen geprüft. Bei jeder Prüfung wird außerdem ein Teil der ältesten Nachrichten bearbeitet.

## Nachts

Von 00:00 bis 06:30 pausieren Prüfungen und neue Nachrichten warten. Um 06:30 werden sie gemeinsam geprüft, bevor deine Morgenübersicht bereitsteht. Unter **Prüfungen** steht: „Nachts pausiert. Um 06:30 werden die Prüfungen nachgeholt.“ Wenn du die App verwendest, im Chat schreibst oder auf eine Aufgabe tippst, laufen die Prüfungen wieder, bis du eine Stunde lang inaktiv warst. **Jetzt prüfen** startet sofort eine Prüfung.

## Eine Prüfung ist fehlgeschlagen

Unter **Verbindungen**, **Prüfungen** zeigt **Letzte Durchläufe** jede Prüfung an. Fehlgeschlagene Prüfungen werden automatisch erneut versucht.

Wenn eine Prüfung wegen des Nutzungslimits deines KI-Tarifs angehalten wurde, steht dort **Das KI-Nutzungslimit wurde erreicht.** und wann es wieder aufgehoben wird. Das ist eine Pause, kein Fehler: Die Nachrichten warten und werden nach dem Zurücksetzen des Limits geprüft. Nichts wird an [Fehlerberichte](error-reports.md) gesendet.

## Beiseitegelegt

Wenn eine Prüfung eine Nachricht zweimal zurückstellt, wird sie beiseitegelegt. Unter **Verbindungen**, **Prüfungen** siehst du, wie viele es sind. Unter **Beiseitegelegt** findest du diese Nachrichten. Eine Nachricht von einer Person, die dir schreibt, einer Person, die du kennst, oder einem Kunden wird etwa 3 Tage nach ihrem Eingang noch einmal geprüft. Dabei wird eine Aufgabe erstellt oder die Nachricht geschlossen. Was du verworfen oder zurückgestellt hast, bleibt so.
