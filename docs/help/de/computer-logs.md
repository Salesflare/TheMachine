---
title: Probleme auf deinem Computer
area: troubleshooting
summary: Deine Machine liest die eigenen Logs ihres Computers und sagt dir bei echten Problemen Bescheid, mit Ursache und Lösung. Eine Lösung läuft nur, wenn du auf Do it tippst.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
---
## Was sie liest

Unter Linux mit systemd liest deine Machine das Log deiner eigenen Benutzersitzung: deine eigenen Dienste und die Absturzberichte deiner eigenen Programme. Unter Omarchy prüft sie auch Hyprland und die Leiste. Das Log des ganzen Systems liest sie nie, und sie fragt nie nach mehr Zugriff.

Sie liest, welcher Dienst gestoppt hat, wie er endete und welches Programm abgestürzt ist. Nie, was in einer Logzeile steht, also wird kein Logtext gespeichert und nichts davon verlässt deinen Computer.

## Was als Problem zählt

Ein Dienst, der immer wieder neu startet, einer, der an einem Tag mehrmals gescheitert ist oder aus bleibt, einer ohne Speicher und ein abgestürztes Programm. Unter Omarchy auch ein Absturz von Hyprland oder der Leiste und Fehler in deinen Hyprland-Einstellungen.

Ein einzelner Neustart oder ein einzelner gescheiterter Lauf ist normal und bleibt still.

## Was du bekommst

Eine Aufgabe, die in einfachen Worten sagt, was passiert ist, warum es wichtig ist und welcher Befehl es zeigt oder behebt. Frag in ihrem Chat, und The Machine sieht es sich an. Alles, was sie ändert, wartet auf dein OK, wie bei Do it.

Gibt es eine sichere Lösung, hat die Aufgabe Do it. Einen deiner Dienste, der aus bleibt, startet es neu, und auf Omarchy holt es die Leiste zurück. Do it führt nur diesen einen Befehl aus, und das Ergebnis steht im Chat der Aufgabe. Die Dienste von The Machine selbst und das OpenClaw Gateway fasst es nie an.

Dasselbe Problem bringt höchstens alle zwei Wochen eine Aufgabe und nie, solange seine Aufgabe noch offen ist. Höchstens zwei neue am Tag.

## Im Terminal

`assistant doctor` listet dieselben Probleme vom letzten Tag.

## Andere Computer

Unter macOS, Windows und auf Computern ohne systemd liest sie nichts und sagt das in `assistant doctor`.

## Ausschalten

Setz `"computer_logs": false` in config.json und starte den Dienst neu.
