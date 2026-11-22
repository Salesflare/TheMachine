---
title: Salesflare CRM
area: connections
summary: Konten, Kontakte und Deals, damit sie weiß, wer wichtig ist. Zum Lesen verwendet sie deinen API-Schlüssel.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 3d6041d568843d96
---
## Was sie liest

Deine Konten, Kontakte und Deals in Salesflare sowie den Feed jedes Kontos: E-Mails von Kolleginnen und Kollegen, bei denen du nicht dabei warst, und Meetings mit Notizen.

## Was sie ändern kann

Nichts. (Auf deinem eigenen Computer kann die Einstellung `join_pipelines` dafür sorgen, dass sie dich zu Konten in ausgewählten Pipelines hinzufügt. Standardmäßig ist sie deaktiviert.)

## Verbinden

1. Öffne in Salesflare [Einstellungen, API-Schlüssel](https://app.salesflare.com/#/settings/apikeys) und erstelle einen Schlüssel.
2. Bei einer gehosteten Machine: Öffne deine Einrichtungsseite unter app.themachine.computer/setup, gehe zu **Weitere Quellen**, öffne Salesflare CRM, füge den Schlüssel ein und klicke auf **Verbinden**.
3. Öffne im Dashboard **Verbindungen**, **Kunden** und Salesflare CRM, füge den Schlüssel ein und klicke auf **Verbinden**. Auf der Karte siehst du dann den Fortschritt.

## Sync-Details

Unter **Verbindungen**, **Kunden** zeigt Salesflare den Fortschritt an: wie viele Konten in dieser Runde gelesen wurden und welche übersprungen wurden, weil Salesflare zu langsam war. Dauert eine Runde mehrere Stunden, wird möglicherweise angezeigt, dass sie festhängt.

Die Kacheln zeigen, auf wie viele Konten sie zugreifen konnte und wie viele E-Mails und Meetings sie übernommen hat. Kann Salesflare mit deinem API-Schlüssel keines der Konten öffnen, steht auf der Karte **Braucht deine Hilfe**: Verwende den Schlüssel eines Benutzers, der sie sehen kann. Läuft Salesflare immer wieder in ein Zeitlimit, aber klappt jeder neue Versuch, steht dort, dass Salesflare **manchmal langsam** ist.

Hat Salesflare den Feed-Zugriff für API-Schlüssel in deinem Team noch nicht aktiviert, wird das auf der Karte angezeigt: Es werden keine E-Mails oder Meetings übernommen, bis der Salesflare-Support den Zugriff aktiviert. Am ersten Tag wird alle 10 Minuten erneut geprüft, danach etwa einmal pro Stunde. Sobald es funktioniert, läuft die Synchronisierung automatisch weiter.

- **Stoppen**: Es werden keine neuen Daten übernommen, bis du auf **Starten** klickst. Danach wird an der bisherigen Stelle fortgesetzt.
- **Sync neu starten**: Beginnt von vorn und liest die letzte Woche erneut ein. Bereits übernommene Daten gehen nicht verloren.
- **API-Schlüssel**: Öffnet die API-Schlüsselseite von Salesflare, auf der du einen neuen Schlüssel erstellen kannst.

## Entfernen

- Im Dashboard: Öffne **Verbindungen**, dann Salesflare und **Details**. Klicke anschließend auf **Trennen**. Bereits übernommene Daten bleiben erhalten.
- Bei einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** klicken.

## In Salesflare widerrufen

Lösche den API-Schlüssel in Salesflare unter Einstellungen, API-Schlüssel.
