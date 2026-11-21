---
title: Probleme auf deinem Computer
area: troubleshooting
summary: Deine Machine liest die eigenen Protokolle des Computers und informiert dich über echte Probleme, ihre Ursache und eine Lösung. Eine Lösung wird nur ausgeführt, wenn du auf **Ausführen** tippst.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: b18e5f4989d6baff
---
## Was gelesen wird

Unter Linux mit systemd liest deine Machine das Protokoll deiner eigenen Benutzersitzung: deine eigenen Dienste und die Absturzberichte deiner eigenen Programme. Unter Omarchy prüft sie auch Hyprland und die Leiste. Sie liest nie das Protokoll des gesamten Systems und fordert nie zusätzliche Zugriffsrechte an.

Sie liest, welcher Dienst angehalten wurde, wie er beendet wurde und welches Programm abgestürzt ist. Den Inhalt einzelner Logzeilen liest sie nie. Daher werden keine Protokolltexte gespeichert oder verlassen deinen Computer.

## Was als Problem gilt

Ein Dienst, der immer wieder neu startet, mehrmals am Tag fehlschlägt oder dauerhaft ausgefallen ist, ein Dienst, dem der Arbeitsspeicher ausgeht, und ein abgestürztes Programm. Unter Omarchy außerdem ein Absturz von Hyprland oder der Leiste sowie Fehler in deinen Hyprland-Einstellungen.

Ein einzelner Neustart oder ein einzelner fehlgeschlagener Lauf ist normal und bleibt ohne Meldung. Dasselbe gilt für einen Dienst, der ein paar Mal fehlschlägt und danach wieder normal läuft, und für einen fehlgeschlagenen Dienst, den nichts zu starten versucht: einen, der nicht aktiviert ist und den auch kein anderer Dienst oder Timer startet.

Browser, die von Tests und Agenten gesteuert werden (headless, Playwright, Puppeteer, CI), bleiben ohne Meldung. Das gilt auch für ein Programm, das beendet wird, während sein Dienst angehalten oder neu gestartet wird. Dasselbe gilt für Entwicklerläufe: Programme, die ein Coding-Agent startet, Tests und Programme, die aus einem temporären Ordner oder einem Cache-Ordner gestartet werden. Stürzt ein Programm immer wieder ab, wird eine Aufgabe erstellt, die angibt, wie oft und wann das passiert ist.

Ein Skript wird unter seinem eigenen Namen aufgeführt, etwa backup.py, nicht unter python3 oder node.

## Was du bekommst

Eine Aufgabe, die in einfachen Worten erklärt, was passiert ist, warum es wichtig ist und was du tun kannst. Die Befehle, die den Grund zeigen, findest du unter **Mehr anzeigen**. Frag im zugehörigen Chat nach, und The Machine untersucht das Problem. Alles, was sie ändert, wartet auf deine Bestätigung, wie bei **Ausführen**.

Wenn es eine sichere Lösung gibt, enthält die Aufgabe die Schaltfläche **Ausführen**. Bei einem dauerhaft ausgefallenen Dienst von dir startet sie ihn erneut. Unter Omarchy bringt sie außerdem die Leiste zurück. **Ausführen** startet nur diesen Befehl. Das Ergebnis wird im Chat der Aufgabe angezeigt. The Machine greift nie in ihre eigenen Dienste oder das OpenClaw Gateway ein.

Für dasselbe Problem gibt es höchstens alle zwei Wochen eine Aufgabe und keine, solange die zugehörige Aufgabe noch offen ist. Pro Tag werden höchstens zwei neue Aufgaben erstellt. Eine Aufgabe zu einem ausgefallenen Dienst wird automatisch geschlossen, sobald er wieder läuft oder der Fehler behoben wurde.

## Im Terminal

`assistant doctor` listet dieselben Probleme der letzten 24 Stunden auf.

## Andere Computer

Unter macOS und Windows sowie auf Computern ohne systemd liest sie nichts und weist in `assistant doctor` darauf hin.

Bei einer gehosteten Machine kümmern wir uns darum, dass der Server läuft. Probleme damit gehen an das Team von The Machine und werden dir nicht als Aufgaben gemeldet.

## Deaktivieren

Setze `"computer_logs": false` in config.json und starte den Dienst neu.
