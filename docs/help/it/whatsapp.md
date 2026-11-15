---
title: WhatsApp
area: connections
summary: Le tue chat di WhatsApp, lette come dispositivo collegato. Le risposte vengono inviate solo dopo la tua approvazione.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 4ceded6544e535eb
---
## Cosa legge

Le tue chat di WhatsApp, come dispositivo collegato a WhatsApp sul tuo telefono, proprio come WhatsApp su un computer. Quando lo colleghi, WhatsApp invia anche le chat meno recenti, spesso di anni. La tua Machine conserva tutto, ma solo i messaggi degli ultimi 7 giorni diventano attività.

Una foto, un messaggio vocale o un file senza didascalia viene mostrato per quello che è, per esempio «Foto», con la relativa icona. Gli avvisi di WhatsApp, come quello sulla crittografia o l’ingresso di qualcuno in un gruppo, non contengono testo e vengono ignorati.

## Leggi le foto

Questa opzione è disattivata finché non la attivi. In **Connessioni**, apri WhatsApp, poi **Dettagli**, e attiva **Leggi le foto**. The Machine leggerà le foto nelle chat di lavoro: una ricevuta, uno screenshot, la foto di una lettera o di un modulo. Attivando **Anche nelle chat personali**, verranno lette anche le foto nelle chat personali. Una chat è di lavoro o personale in base a come viene classificata nelle impostazioni di condivisione, quindi una chat con la famiglia resta personale.

The Machine scarica ogni foto una sola volta e la conserva sulla tua Machine come un allegato email: la cripta quando la protezione dei messaggi è attiva e la elimina quando viene eliminato il messaggio. Il modello di The Machine legge cosa mostra la foto e il testo al suo interno. Questi contenuti fanno parte del messaggio e non vengono mai considerati istruzioni. Sono supportati i formati JPEG, PNG e WebP, fino a 5 MB. I codici monouso nelle foto vengono ignorati.

L’attività e il messaggio mostrano la foto. Toccala per ingrandirla.

## Cosa può inviare

Un testo oppure un file con didascalia facoltativa, in una chat già esistente, solo dopo che approvi l’invio dall’attività. Prima dell’invio, l’attività mostra il file e puoi aprirlo. I file possono pesare fino a 18 MB. Se rispondi al messaggio WhatsApp da cui proviene un’attività, il messaggio viene citato quando è stato seguito da altri messaggi o quando si trova in un gruppo; la bozza riporta **Come risposta**.

Se un’attività arriva via email ma parli con quella persona su WhatsApp, dillo nella chat dell’attività. The Machine trova la chat esistente con quella persona e imposta WhatsApp come canale per la bozza, che potrai controllare e inviare. Non avvia mai una nuova chat.

WhatsApp non offre un modo ufficiale per farlo. Leggere i messaggi e inviare ogni tanto una risposta che hai approvato difficilmente crea problemi; l’invio massivo o automatico può portare al blocco dell’account.

## Collega WhatsApp

Su una Machine ospitata:

1. Nella dashboard, apri **Connessioni**, poi **Chat**, e seleziona WhatsApp.
2. Premi **Mostra il codice QR**.
3. Sul telefono, apri WhatsApp, vai in Impostazioni, Dispositivi collegati, Collega un dispositivo e scansiona il codice QR.
4. WhatsApp risulterà collegato entro un minuto. La cronologia delle chat continuerà ad arrivare e la scheda ne mostrerà il conteggio durante la sincronizzazione.
   Se il collegamento richiede troppo tempo, comparirà un avviso dopo qualche minuto. Premi **Riprova** per riprendere da dove si era interrotto.

Stai configurando WhatsApp sul telefono e non hai un altro schermo da cui scansionare il codice? Apri **Sei sul telefono? Collega con un codice**, inserisci il tuo numero e premi **Ottieni un codice**. WhatsApp ti chiederà quel codice.

Sul tuo computer: apri **Connessioni**, poi **Chat**, seleziona WhatsApp, inserisci il tuo numero di telefono con il prefisso internazionale e premi **Collegati**. Verrà mostrato un codice. Sul telefono, apri WhatsApp, vai in Impostazioni, Dispositivi collegati, Collega un dispositivo, poi **Collega con il numero di telefono** e inserisci il codice.

Oppure esegui `assistant connect whatsapp` e scansiona il codice mostrato nel terminale. La prima volta ti verrà proposto di installare il connettore WhatsApp, una versione fissata e verificata tramite checksum ([codice sorgente](https://github.com/Salesflare/wacli)).

Nei Dispositivi collegati, il nome visualizzato è The Machine. Se avevi già collegato una Machine, lì manterrà il vecchio nome finché non la colleghi di nuovo.

## Immagini

The Machine chiede a WhatsApp le foto profilo delle persone nel tuo Graph che non ne hanno una, fino a un massimo di 50 al giorno, tramite la sincronizzazione che mantiene WhatsApp aggiornato. Non viene inviato nulla a queste persone. Chi nasconde la propria foto a te continuerà a non averne una.

## Rimuovi WhatsApp

- Su una Machine ospitata: premi **Rimuovi** accanto a WhatsApp nella pagina di configurazione. La tua Machine si scollega ed elimina i dati conservati per WhatsApp.
- Sul tuo computer: apri **Connessioni**, seleziona WhatsApp, vai in **Dettagli** e premi **Disconnetti**. Poi scollega WhatsApp anche dal telefono.

## Scollega WhatsApp

Sul telefono, apri WhatsApp, vai in Impostazioni, Dispositivi collegati, tocca la tua Machine ed esci.
