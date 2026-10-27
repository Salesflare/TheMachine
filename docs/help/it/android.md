---
title: Notifiche Android
area: connections
summary: Le notifiche del tuo telefono Android, tramite l’app OpenClaw. Legge soltanto.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, More sources, Remove
---
## Cosa legge

Le notifiche che arrivano sul tuo telefono Android, tramite l’app OpenClaw. I codici monouso restano fuori, così come le notifiche di WhatsApp, Telegram, Signal e Discord.

## Cosa può fare

Niente sul tuo telefono. Legge solo le notifiche.

## Collegalo

Su una Machine in hosting:

1. Installa l’app OpenClaw sul telefono.
2. Nella tua pagina di configurazione, vai su **Altre fonti**, apri Notifiche Android e premi **Mostra un codice di configurazione**.
3. Scansionalo nell’app OpenClaw, poi premi **Approva** per l’abbinamento.
4. Nell’app OpenClaw, attiva Forward Notification Events e consenti l’accesso alle notifiche quando Android lo chiede.

Sul tuo computer, abbina il telefono al tuo OpenClaw Gateway, poi esegui `assistant connect android`.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Android, **Dettagli**, poi **Disconnetti**.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto ad Android nella tua pagina di configurazione.

## Rimuovilo dal telefono

Disattiva l’accesso alle notifiche per l’app OpenClaw nelle impostazioni di Android, oppure dissocia il telefono nell’app OpenClaw.
