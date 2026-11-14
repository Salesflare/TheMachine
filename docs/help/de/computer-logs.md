---
title: Probleme auf deinem Computer
area: troubleshooting
summary: Deine Machine liest ihre Systemprotokolle und weist dich auf echte Probleme hin, inklusive Ursache und Lösung. Eine Lösung wird erst ausgeführt, wenn du auf **Ausführen** tippst.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: 1a191d8433bfba2a
---
## Was sie liest

Unter Linux mit systemd liest deine Machine das Protokoll deiner eigenen Benutzersitzung: deine eigenen Dienste und die Absturzberichte deiner eigenen Programme. Unter Omarchy prüft sie außerdem Hyprland und die Statusleiste. Sie liest nie das Protokoll des gesamten Systems und fordert nie mehr Zugriff an.

Sie liest, welcher Dienst angehalten wurde, wie er beendet wurde und welches Programm abgestürzt ist. Den Inhalt einzelner Protokollzeilen liest sie nie. Es werden also keine Protokolltexte gespeichert oder von deinem Computer übertragen.

## Was als Problem gilt

Ein Dienst, der immer wieder neu startet, mehrmals am Tag ausfällt oder nicht mehr läuft, ein Dienst, dem der Arbeitsspeicher ausgeht, und ein Programm, das abstürzt. Unter Omarchy zählen auch Abstürze von Hyprland oder der Statusleiste sowie Fehler in deinen Hyprland-Einstellungen dazu.

Ein einzelner Neustart oder ein einzelner fehlgeschlagener Lauf ist normal und bleibt unbemerkt. Das gilt auch für einen Dienst, der ein paar Mal ausfällt und danach wieder problemlos läuft.

Browser, die von Tests und Agenten gesteuert werden (headless, Playwright, Puppeteer, CI), bleiben unbemerkt. Das gilt auch für ein Programm, das beendet wird, während sein Dienst angehalten oder neu gestartet wird. Entwicklerläufe bleiben ebenfalls unbemerkt: Was ein Coding-Agent ausführt, Tests und Programme aus einem temporären Ordner oder Cache-Ordner. Ein Programm, das immer wieder abstürzt, erstellt eine Aufgabe, in der steht, wie oft und wann es passiert ist.

Ein Skript wird unter seinem eigenen Namen aufgeführt, zum Beispiel backup.py, nicht als python3 oder node.

## Was du bekommst

Eine Aufgabe, die in einfachen Worten erklärt, was passiert ist, warum es wichtig ist und was du tun kannst. Unter **Mehr anzeigen** findest du die Befehle, die den Grund zeigen. Frag im zugehörigen Chat nach, und The Machine untersucht das Problem. Alles, was sie ändert, wartet auf deine Zustimmung, auch bei **Ausführen**.

Wenn es eine sichere Lösung gibt, enthält die Aufgabe die Schaltfläche **Ausführen**. Bei einem deiner Dienste, der nicht mehr läuft, startet sie ihn neu. Unter Omarchy stellt sie die Statusleiste wieder her. **Ausführen** führt nur diesen Befehl aus. Das Ergebnis erscheint im Chat der Aufgabe. The Machine greift nie in ihre eigenen Dienste oder das OpenClaw Gateway ein.

Dasselbe Problem führt höchstens alle zwei Wochen zu einer Aufgabe und nie, solange die entsprechende Aufgabe noch offen ist. Pro Tag gibt es höchstens zwei neue Aufgaben. Eine Aufgabe zu einem ausgefallenen Dienst wird automatisch geschlossen, sobald der Dienst wieder läuft oder der Ausfall behoben ist.

## Im Terminal

`assistant doctor` listet dieselben Probleme aus den letzten 24 Stunden auf.

## Andere Computer

Unter macOS und Windows sowie auf Computern ohne systemd liest sie nichts und weist dich in `assistant doctor` darauf hin.

Bei einer gehosteten Machine kümmern wir uns darum, dass der Server läuft. Seine Probleme gehen an das Team von The Machine, nicht als Aufgaben an dich.

## Ausschalten

Setze `"computer_logs": false` in config.json und starte den Dienst neu.
