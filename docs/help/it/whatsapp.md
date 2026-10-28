---
title: WhatsApp
area: connections
summary: Le tue chat WhatsApp, lette come dispositivo collegato. Risponde solo dopo la tua approvazione.
covers: connector:whatsapp
code: onboarding.py, next_actions.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## Cosa legge

Le tue chat WhatsApp, come dispositivo collegato al WhatsApp del tuo telefono, come WhatsApp su un computer. Quando lo colleghi legge gli ultimi 7 giorni.

Una foto, un messaggio vocale o un file senza didascalia compare per ciò che è, come "Immagine inviata". Gli avvisi di WhatsApp, come quello sulla crittografia o qualcuno che entra in un gruppo, non hanno testo e vengono esclusi.

## Cosa può inviare

Un testo in una chat che esiste già, solo dopo che l'hai approvato sull'attività.

Se un'attività è arrivata via email ma con quella persona parli su WhatsApp, dillo nella chat dell'attività. The Machine trova la chat che hai già con lei e sposta la bozza su WhatsApp, da rivedere e inviare. Non apre mai una nuova chat.

## Collegalo

Su una Machine ospitata:

1. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli WhatsApp.
2. Premi **Mostra il codice QR**.
3. Sul telefono, in WhatsApp, apri Impostazioni, Dispositivi collegati, Collega un dispositivo, e scansiona il codice QR.

Stai configurando dal telefono, senza un secondo schermo da cui scansionare? Apri **Sei sul telefono? Collegati con un codice**, inserisci il tuo numero e premi **Ottieni un codice**. WhatsApp poi ti chiede quel codice.

Sul tuo computer, esegui `assistant connect whatsapp` e scansiona il codice che mostra nel terminale. Senza wacli, si offre di installare la build fissata da [Salesflare/wacli](https://github.com/Salesflare/wacli), verificata con il suo checksum.

## Foto

The Machine chiede a WhatsApp le foto profilo delle persone nel tuo graph che non ne hanno una, al massimo 50 al giorno, tramite la sincronizzazione che tiene aggiornato WhatsApp. Non viene inviato nulla a loro. Chi ti nasconde la propria foto resta senza.

## Rimuovilo

- Su una Machine ospitata: premi **Rimuovi** accanto a WhatsApp nella tua pagina di configurazione. Il server si scollega da solo ed elimina ciò che aveva conservato per WhatsApp.
- Sul tuo computer: **Connessioni**, apri WhatsApp, **Dettagli**, poi **Disconnetti**. Poi scollegalo anche dal telefono.

## Scollegalo in WhatsApp

Sul telefono, in WhatsApp, apri Impostazioni, Dispositivi collegati, tocca la tua Machine ed esci.
