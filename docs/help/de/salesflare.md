---
title: Salesflare CRM
area: connections
summary: Accounts, Kontakte und Deals, damit sie weiß, wer wichtig ist. Sie liest sie mit deinem API-Schlüssel aus.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 8051c61777603a7e
---
## Was sie ausliest

Deine Accounts, Kontakte und Deals in Salesflare sowie den Feed jedes Accounts: E-Mails von Kolleginnen und Kollegen, bei denen du nicht dabei warst, und Meetings mit Notizen.

## Was sie ändern kann

Nichts. (Auf deinem eigenen Computer kann die Einstellung `join_pipelines` dafür sorgen, dass sie dich zu Accounts in ausgewählten Pipelines hinzufügt. Standardmäßig ist sie deaktiviert.)

## Verbinden

1. Öffne in Salesflare [Einstellungen, API-Schlüssel](https://app.salesflare.com/#/settings/apikeys) und erstelle einen Schlüssel.
2. Auf einer gehosteten Machine: Öffne deine Einrichtungsseite unter app.themachine.computer/setup, gehe zu **Weitere Quellen**, öffne Salesflare CRM, füge den Schlüssel ein und drücke **Verbinden**.
3. Im Dashboard: **Verbindungen**, **Kunden**, Salesflare CRM, füge den Schlüssel ein und drücke **Verbinden**. Auf der Karte siehst du dann den Fortschritt.

## Sync-Details

Unter **Verbindungen**, **Kunden** zeigt Salesflare den Fortschritt an: die Accounts, die in diesem Durchlauf geprüft wurden, die übersprungenen, weil Salesflare zu langsam war, und die, auf die dein API-Schlüssel nicht zugreifen kann (**kein Zugriff**). Dauert ein Durchlauf mehrere Stunden, wird angezeigt, dass er möglicherweise feststeckt.

Die Kacheln zählen die Accounts, die sie diese Woche ausgelesen hat, sowie die E-Mails und Meetings, die sie übernommen hat.

Ein paar Accounts ohne Zugriff sind kein Problem: Der Rest wird wie gewohnt übernommen. Kann dein API-Schlüssel auf keinen Account zugreifen, zeigt die Karte **Braucht deine Hilfe** an: Verwende den Schlüssel eines Users, der die Accounts sehen kann. Mit einem neuen Schlüssel beginnt sie von vorn und liest die letzte Woche erneut aus. Wenn Salesflare immer wieder eine Zeitüberschreitung verursacht, der nächste Versuch aber jeweils klappt, wird angezeigt, dass Salesflare **manchmal langsam** ist.

Wenn Salesflare den Feed-Zugriff für API-Schlüssel in deinem Team nicht aktiviert hat, wird das auf der Karte angezeigt: Es werden keine E-Mails oder Meetings übernommen, bis der Salesflare-Support den Zugriff aktiviert. Am ersten Tag prüft sie alle 10 Minuten erneut, danach ungefähr einmal pro Stunde. Sobald es funktioniert, macht sie von selbst weiter.

- **Stoppen**: Es werden keine neuen Daten übernommen, bis du **Starten** drückst. Danach geht es an der bisherigen Stelle weiter.
- **Sync neu starten**: Beginnt von vorn und liest die letzte Woche erneut aus. Bereits übernommene Daten gehen nicht verloren.
- **API-Schlüssel**: Öffnet die API-Schlüsselseite von Salesflare, um einen neuen Schlüssel zu erstellen.

## Verbindung entfernen

- Im Dashboard: **Verbindungen**, öffne Salesflare, **Details** und dann **Trennen**. Bereits übernommene Daten bleiben erhalten.
- Auf einer gehosteten Machine kannst du sie auch über **Entfernen** neben Salesflare auf deiner Einrichtungsseite entfernen.

## API-Schlüssel in Salesflare widerrufen

Lösche den API-Schlüssel in Salesflare unter Einstellungen, API-Schlüssel.
