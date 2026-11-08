---
title: WhatsApp
area: connections
summary: Le tue chat WhatsApp, lette come dispositivo collegato. Risponde solo dopo la tua approvazione.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## Cosa legge

Le tue chat WhatsApp, come dispositivo collegato al WhatsApp del tuo telefono, come WhatsApp su un computer. Quando lo colleghi, WhatsApp invia anche le chat più vecchie, spesso di anni. La tua Machine conserva tutto, e solo i messaggi degli ultimi 7 giorni diventano attività.

Una foto, un messaggio vocale o un file senza didascalia compare per ciò che è, come "Immagine inviata". Gli avvisi di WhatsApp, come quello sulla crittografia o qualcuno che entra in un gruppo, non hanno testo e vengono esclusi.

## Leggi le foto

Spento finché non lo accendi. In **Connessioni**, apri WhatsApp, poi **Dettagli**, e attiva **Leggi le foto** e The Machine legge le foto nelle tue chat di lavoro: una ricevuta, uno screenshot, la foto di una lettera o di un modulo. **Anche nelle chat personali** legge anche quelle delle tue chat personali. Una chat è di lavoro o personale come la vede la condivisione, quindi una chat con la famiglia resta personale.

The Machine scarica ogni foto una volta e la tiene sulla tua Machine come un allegato email: cifrata quando la protezione dei messaggi è attiva, ed eliminata quando il suo messaggio sparisce. Il suo modello legge cosa mostra la foto e il testo che contiene. Conta come parte del messaggio, mai come istruzioni. JPEG, PNG e WebP fino a 5 MB. Un codice monouso in una foto viene omesso.

L’attività e il messaggio mostrano la foto. Toccala per vederla in grande.

## Cosa può inviare

Un testo in una chat che esiste già, solo dopo che l'hai approvato sull'attività. Una risposta al messaggio WhatsApp da cui è nata un’attività cita quel messaggio quando dopo ne sono arrivati altri, o in un gruppo; la bozza dice **Come risposta**.

Se un'attività è arrivata via email ma con quella persona parli su WhatsApp, dillo nella chat dell'attività. The Machine trova la chat che hai già con lei e sposta la bozza su WhatsApp, da rivedere e inviare. Non apre mai una nuova chat.

WhatsApp non offre un modo ufficiale per farlo. Leggere e inviare ogni tanto una risposta che hai approvato difficilmente crea problemi; inviare in massa o in automatico può far bloccare un account.

## Collegalo

Su una Machine ospitata:

1. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli WhatsApp.
2. Premi **Mostra il codice QR**.
3. Sul telefono, in WhatsApp, apri Impostazioni, Dispositivi collegati, Collega un dispositivo, e scansiona il codice QR.
4. WhatsApp risulta collegato entro un minuto. La tua cronologia chat continua ad arrivare dopo, e la sua scheda conta i messaggi mentre arrivano.
   Se il collegamento richiede troppo, lo dice dopo qualche minuto. Premi **Riprova** per riprendere da dove si è fermato.

Stai configurando dal telefono, senza un secondo schermo da cui scansionare? Apri **Sei sul telefono? Collegati con un codice**, inserisci il tuo numero e premi **Ottieni un codice**. WhatsApp poi ti chiede quel codice.

Sul tuo computer, esegui `assistant connect whatsapp` e scansiona il codice che mostra nel terminale. La prima volta, si offre di installare il connettore di WhatsApp, una build fissata verificata con il suo checksum ([sorgente](https://github.com/Salesflare/wacli)).

In Dispositivi collegati appare come The Machine. Una Machine collegata prima mantiene lì il suo vecchio nome finché non la colleghi di nuovo.

## Foto

The Machine chiede a WhatsApp le foto profilo delle persone nel tuo graph che non ne hanno una, al massimo 50 al giorno, tramite la sincronizzazione che tiene aggiornato WhatsApp. Non viene inviato nulla a loro. Chi ti nasconde la propria foto resta senza.

## Rimuovilo

- Su una Machine ospitata: premi **Rimuovi** accanto a WhatsApp nella tua pagina di configurazione. La tua Machine si scollega da sola ed elimina ciò che aveva conservato per WhatsApp.
- Sul tuo computer: **Connessioni**, apri WhatsApp, **Dettagli**, poi **Disconnetti**. Poi scollegalo anche dal telefono.

## Scollegalo in WhatsApp

Sul telefono, in WhatsApp, apri Impostazioni, Dispositivi collegati, tocca la tua Machine ed esci.
