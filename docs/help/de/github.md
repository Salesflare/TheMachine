---
title: GitHub
area: connections
summary: Prüfe Review-Anfragen, Erwähnungen, Zuweisungen und fehlgeschlagene CI-Läufe. Issues werden nur nach deiner Bestätigung erstellt.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## Was gelesen wird

Deine GitHub-Benachrichtigungen: Review-Anfragen, Erwähnungen, Zuweisungen, Antworten und fehlgeschlagene CI-Läufe. Sie werden nie als gelesen markiert.

## Was möglich ist

Beim Lesen wird auf GitHub nichts geändert. Wenn eine Aufgabe mit einem GitHub-Schritt endet, etwa dem Erstellen eines Issues, weist die Aufgabe darauf hin. Der Schritt wird erst ausgeführt, wenn du auf **Bestätigen** tippst oder im zugehörigen Chat genau darum gebeten hast. Screenshots werden über den Browser deiner Machine hochgeladen. Wenn GitHub nicht verbunden ist, weist die Aufgabe darauf hin, dass der Browser verwendet wird, und zeigt **GitHub verbinden** an.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne **Verbindungen**, dann **Projekte und Code**, und wähle GitHub aus.
2. Wähle **Arbeit** oder **Privat** und klicke auf **Bei GitHub anmelden**.
3. Klicke auf **GitHub öffnen ↗**, gib den angezeigten Code ein und erteile die Berechtigung. Die Verbindung wird automatisch hergestellt.

Auf deiner Einrichtungsseite unter app.themachine.computer/setup findest du dieselbe Anmeldung unter **Weitere Quellen**.

Auf deinem eigenen Computer:

1. Öffne **Verbindungen**, dann **Projekte und Code**, und wähle GitHub aus.
2. Wähle **Arbeit** mit dem zugehörigen Unternehmen oder **Privat** und klicke auf **Verbinden**.
3. Wenn du dazu aufgefordert wirst, klicke auf **GitHub öffnen ↗**, gib den Code ein und erteile die Berechtigung. Die Verbindung wird automatisch hergestellt.

Oder führe `assistant connect github` aus und bestätige deine GitHub-Anmeldung.

## Verbindung trennen

- Öffne **Verbindungen**, dann GitHub, **Details** und **Trennen**. Die Verbindung liest dann nichts mehr. Bereits übernommene Inhalte bleiben erhalten.
- Auf einer gehosteten Machine kannst du GitHub auch über **Entfernen** neben dem Eintrag auf deiner Einrichtungsseite entfernen.

## Auf GitHub deinstallieren

Öffne auf GitHub Einstellungen, Anwendungen und Autorisierte OAuth-Apps und widerrufe die Berechtigung für GitHub CLI. Auf deinem eigenen Computer meldet `gh auth logout` dich ebenfalls ab.
