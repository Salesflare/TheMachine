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

1. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle GitHub.
2. Wähle **Arbeit** oder **Privat** und tippe auf **Mit GitHub anmelden**.
3. Es zeigt einen Code. Tippe auf **GitHub öffnen ↗**, gib den Code ein und erlaube den Zugriff. Danach geht es von selbst weiter.

Deine Einrichtungsseite unter app.themachine.computer/setup hat dieselbe Anmeldung unter **Weitere Quellen**.

Auf deinem eigenen Computer:

1. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle GitHub.
2. Wähle **Arbeit** mit ihrer Firma oder **Privat** und tippe auf **Verbinden**.
3. Ist deine Machine noch nicht bei GitHub angemeldet, zeigt sie einen Code. Tippe auf **GitHub öffnen ↗**, gib den Code ein und erlaube den Zugriff. Danach geht es von selbst weiter.

Oder führe `assistant connect github` aus und bestätige dein GitHub-Login. The Machine prüft bei jeder Synchronisierung, ob es passt.

## Entfernen

- Im Dashboard: **Verbindungen**, GitHub öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Auf GitHub deinstallieren

Entzieh der GitHub CLI den Zugriff in GitHub, unter Settings, Applications, Authorized OAuth Apps. Auf deinem eigenen Computer meldet `gh auth logout` die CLI ebenfalls ab.
