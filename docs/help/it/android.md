---
title: Notifiche Android
area: connections
summary: Le notifiche del tuo telefono Android, tramite l’app OpenClaw. Legge soltanto le notifiche.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## Cosa legge

Le notifiche del tuo telefono Android, tramite l’app OpenClaw. I codici monouso non vengono inclusi, così come le notifiche di WhatsApp, Telegram, Signal e Discord.

## Cosa può fare

Non fa nulla sul tuo telefono. Legge soltanto le notifiche.

## Connettila

Su una Machine ospitata:

1. Installa OpenClaw da Google Play sul tuo telefono.
2. Nella dashboard, apri **Connessioni**, poi **Altro**, seleziona Android notifications e tocca **Mostra un codice di configurazione**.
3. Nell’app OpenClaw, aggiungi un Gateway e scansiona il codice. Torna alla dashboard e tocca **Approva**.
4. Quando l’app te lo chiede, consenti l’accesso alle notifiche. Poi attiva **Inoltra eventi di notifica** nelle impostazioni dell’app, così le notifiche arrivano appena vengono ricevute e non solo durante il controllo ogni 10 minuti.

Sul tuo computer, associa il telefono nell’app OpenClaw, poi esegui `assistant connect android`.

## Rimuovila

- Nella dashboard: apri **Connessioni**, seleziona Android, tocca **Dettagli**, poi **Disconnetti**.
- Su una Machine ospitata, puoi anche toccare **Rimuovi** accanto alla connessione nella pagina di configurazione.

## Rimuovila dal telefono

Disattiva l’accesso alle notifiche per l’app OpenClaw nelle impostazioni di Android, oppure scollega il telefono nell’app OpenClaw.
