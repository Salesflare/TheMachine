---
title: Keine neuen Aufgaben
area: troubleshooting
summary: Prüfungen sind ausgeschaltet, warten oder wurden wegen des Nutzungslimits deines Modells angehalten. So erkennst du den Grund und weißt, was zu tun ist.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: d265e540d9ecef0e
---
Aufgaben entstehen durch Prüfungen: Deine Machine schaut sich an, was in den letzten etwa 15 Minuten eingegangen ist.

## Gerade angemeldet

Auf einer neuen gehosteten Machine starten Prüfungen automatisch, sobald deine KI und Mail verbunden sind. Während deine Machine deine Mails liest, steht unter Aufgaben: „Deine Mails werden gelesen. Die ersten Aufgaben kommen in wenigen Minuten.“ Sobald deine Machine weiß, wie viel es zu lesen gibt, nennt sie die ungefähre Dauer: „Die ersten Aufgaben kommen in etwa 10 Minuten.“ Fehlt ein Schritt, nennt **Braucht dich** ihn, zum Beispiel **Mail verbinden**, und verlinkt direkt dorthin.

Während deine Machine liest, zeigt Aufgaben, wie weit sie ist („20 von 132 Nachrichten gelesen. Die nächsten 40 werden gelesen …“), einige Personen und Organisationen, auf die sie gestoßen ist, und deine erste Aufgabe, sobald sie da ist. Die Zahl zählt die Nachrichten, die sie fertig gelesen hat. Der Balken bewegt sich weiter, während sie die nächsten Nachrichten liest. Die Namen stammen aus deinen eigenen Mails und sind nur für dich sichtbar.

Wenn beim ersten Durchsehen nichts für dich dabei ist, steht dort, was gelesen wurde, und es werden nächste Schritte vorgeschlagen, zum Beispiel einen Dienst zu verbinden, der dir oft Mails schickt, oder zu fragen, was sich diese Woche geändert hat.

## Prüfungen sind ausgeschaltet

Oben unter Aufgaben steht: „Prüfungen sind ausgeschaltet. Deshalb kommen noch keine Aufgaben an.“ Auf einer gehosteten Machine drückst du **Prüfung einschalten**. Auf deinem eigenen Computer führst du `./install.sh --activate` aus.

## Das Limit deines Modells

Damit genug Spielraum für deine eigenen Chats bleibt, werden Prüfungen bei etwa 65 % des 5-Stunden-Limits und 90 % des Wochenlimits deines KI-Tarifs pausiert. Mit einem Backup-Modell in einem anderen Tarif werden Prüfungen nicht angehalten. Weitere Infos findest du unter [Modell](model.md).

Während Prüfungen warten, steht oben im Dashboard, bis wann sie warten, zum Beispiel: „Prüfungen warten bis 07:15, damit dein ChatGPT-Wochenlimit geschont wird.“ **Jetzt prüfen** startet trotzdem eine Prüfung. Unter **Einstellungen**, **Modell** findest du deine Limits.

Es geht nichts verloren: Sobald es möglich ist, werden die eingegangenen Nachrichten geprüft.

## Nachts

Von 00:00 bis 06:30 pausieren Prüfungen, und neue Nachrichten warten. Um 06:30 werden sie zusammen geprüft, bevor deine morgendliche Zusammenfassung erstellt wird. Unter **Prüfungen** steht: „Nachts pausiert. Aufholen um 06:30.“ Wenn du die App nutzt, im Chat schreibst oder eine Aufgabe antippst, laufen Prüfungen wieder, bis du eine Stunde lang nicht aktiv warst. **Jetzt prüfen** prüft sofort.

## Ein Durchlauf ist fehlgeschlagen

Unter **Verbindungen**, **Prüfungen** zeigt **Letzte Durchläufe** jeden Durchlauf an. Ein fehlgeschlagener Durchlauf wird automatisch erneut versucht.

## Zurückgestellt

Wenn eine Prüfung eine Nachricht zweimal zurückstellt, wird sie zurückgestellt abgelegt. Unter **Verbindungen**, **Prüfungen** siehst du, wie viele es sind. Unter **Zurückgestellt** findest du sie. Eine Nachricht von jemandem, der dir schreibt, einer Person, die du kennst, oder einem Kunden wird etwa 3 Tage nach Eingang noch einmal geprüft. Dabei wird eine Aufgabe erstellt oder die Nachricht geschlossen. Was du verworfen oder zurückgestellt hast, bleibt so.
