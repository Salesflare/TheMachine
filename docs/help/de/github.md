---
title: GitHub
area: connections
summary: Review-Anfragen, Erwähnungen, Zuweisungen und fehlgeschlagene CI-Läufe. Es liest nur.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## Was es liest

Deine GitHub-Benachrichtigungen: Review-Anfragen, Erwähnungen, Zuweisungen, Antworten und fehlgeschlagene CI-Läufe. Es markiert nie eine Benachrichtigung als gelesen.

## Was es tun kann

Nichts auf GitHub. Jeder Aufruf ist ein reiner Lesezugriff.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und geh zu **Weitere Quellen**.
2. Öffne GitHub und tippe auf **Mit GitHub anmelden**.
3. Gib den angezeigten Code bei GitHub ein, auf deinem Handy oder Computer.

Auf deinem eigenen Computer:

1. Melde dich zuerst bei der GitHub CLI an: `gh auth login`.
2. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle GitHub. Oder führe `assistant connect github` aus.
3. Bestätige dein GitHub-Login. The Machine prüft bei jeder Synchronisierung, ob es passt.

## Entfernen

- Im Dashboard: **Verbindungen**, GitHub öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Auf GitHub deinstallieren

Entzieh der GitHub CLI den Zugriff in GitHub, unter Settings, Applications, Authorized OAuth Apps. Auf deinem eigenen Computer meldet `gh auth logout` die CLI ebenfalls ab.
