---
title: Salesflare CRM
area: connections
summary: Accounts, Kontakte und Deals, damit es weiß, wer wichtig ist. Es liest mit deinem API-Schlüssel.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
---
## Was es liest

Deine Accounts, Kontakte und Deals in Salesflare und die Account-Feeds: E-Mails von Kolleginnen und Kollegen, an denen du nicht beteiligt bist, und Meetings mit Notizen.

## Was es ändern kann

Nichts, außer du setzt `join_pipelines` in der Einstellungsdatei deiner Machine. Dann fügt es dich von selbst zu Accounts in diesen Pipelines hinzu. Standardmäßig ist das leer.

## Verbinden

1. Öffne in Salesflare [Settings, API keys](https://app.salesflare.com/#/settings/apikeys) und erstelle einen Schlüssel.
2. Auf einer gehosteten Machine: Öffne deine Einrichtungsseite unter app.themachine.computer/setup, geh zu **Weitere Quellen**, öffne Salesflare CRM, füge den Schlüssel ein und tippe auf **Verbinden**.
3. Auf deinem eigenen Computer: Führe `assistant connect crm` aus, oder **Verbindungen**, **+ Hinzufügen**, Salesflare CRM. Nach **Verbinden** startet deine Machine neu und öffnet die Salesflare-Karte. Die sagt zuerst, dass sie die Accounts mit aktuellen E-Mails und Meetings sucht, und dann, wie viele sie gelesen hat.

## Details zur Synchronisierung

Seine Karte unter **Verbindungen**, **Andere Quellen** zeigt, wie weit es ist: wie viele Accounts es in dieser Runde gelesen hat und wie viele es übersprungen hat, weil Salesflare zu langsam geantwortet hat. Eine Runde, die stundenlang läuft, meldet, dass sie vielleicht festhängt.

- **Stopp**: Nichts Neues kommt rein, bis du auf **Starten** tippst. Es macht dort weiter, wo es war.
- **Sync neu starten**: verwirft die aktuelle Runde samt Fehlern und liest jetzt die letzte Woche neu. Nichts, was es reingebracht hat, geht verloren.
- **API-Schlüssel**: öffnet die Seite für API-Schlüssel in Salesflare, um einen neuen Schlüssel zu erstellen.

## Entfernen

- Im Dashboard: **Verbindungen**, Salesflare öffnen, **Details**, dann **Trennen**. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## In Salesflare widerrufen

Lösche den API-Schlüssel in Salesflare, unter Settings, API keys.
