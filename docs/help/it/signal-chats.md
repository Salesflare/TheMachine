---
title: Chat di Signal
area: connections
summary: Le tue chat e i gruppi di Signal, letti come un dispositivo collegato al tuo telefono. Risponde solo dopo la tua approvazione.
covers: connector:signal
code: onboarding.py, signal_setup.py, signal_mirror.py, signal_store.py, signal_send.py
keywords: Signal, linked device, QR code
---
## Cosa legge

Le tue chat e i gruppi, come un dispositivo collegato al tuo telefono, come Signal Desktop. Signal non dà messaggi precedenti a un nuovo dispositivo collegato, quindi legge dal momento in cui lo colleghi.

Foto, messaggi vocali e file appaiono per quello che sono ("Ha inviato una foto"), mai con il loro contenuto. I media visualizzabili una volta non conservano alcun contenuto. Modifiche ed eliminazioni seguono quello che è successo sul telefono, e i messaggi a scomparsa lasciano la tua Machine quando scade il loro tempo.

Storie, reazioni, chiamate e Note personali vengono saltate. Nulla viene segnato come letto.

## Cosa può inviare

Un testo in una chat che esiste già, solo dopo che lo approvi sull’attività. Una risposta cita il messaggio a cui risponde quando aiuta. Gli invii partono uno alla volta, con una pausa in mezzo.

Se un’attività è arrivata per email ma con quella persona parli su Signal, dillo nella chat dell’attività. The Machine trova la tua chat esistente con lei e sposta la bozza su Signal, perché tu la riveda e la invii. Non inizia mai una nuova chat.

## Collegala

1. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli Chat di Signal.
2. Sul telefono, in Signal, apri Impostazioni, **Dispositivi collegati**, **Collega nuovo dispositivo**, e scansiona il codice.

Ti serve un secondo schermo da cui scansionare: Signal collega un dispositivo solo con un codice QR. Oppure esegui `assistant connect signal` in un terminale e scansiona il codice che mostra.

La tua Machine tiene con sé le chiavi del dispositivo collegato. Non la lasciano mai.

## Quando si ferma

- **Signal ha scollegato questa Machine**: l’hai rimossa dal telefono, o Signal ha chiuso il collegamento. Tocca **Ricollega** in **Connessioni** e scansiona un nuovo codice.
- **Aggiorna The Machine per Signal**: Signal non accetta più il client Signal di questa Machine. Aggiorna The Machine.

## Rimuovila

**Connessioni**, apri Chat di Signal, **Dettagli**, poi **Disconnetti**. La tua Machine elimina le chiavi e ciò che aveva conservato per Signal. Poi rimuovila anche dal telefono: Signal, Impostazioni, **Dispositivi collegati**, tocca The Machine e scollegala.
