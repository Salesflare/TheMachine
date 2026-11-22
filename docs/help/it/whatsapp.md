---
title: WhatsApp
area: connections
summary: Le tue chat WhatsApp, lette tramite un dispositivo collegato. Risponde solo dopo la tua approvazione.
covers: connector:whatsapp
code: onboarding.py, whatsapp_setup.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 130c64388a71b7d1
---
## Cosa legge

Le tue chat WhatsApp, come se la tua Machine fosse un dispositivo collegato all’account WhatsApp del tuo telefono, proprio come WhatsApp su un computer. Quando la colleghi, WhatsApp invia anche le chat più vecchie, spesso di anni. La tua Machine conserva tutto, ma solo i messaggi degli ultimi 7 giorni diventano attività.

Una foto, un messaggio vocale o un file senza didascalia viene mostrato per quello che è, per esempio «Foto», con la relativa icona. Le notifiche di WhatsApp, come quella sulla crittografia o sull’ingresso di una persona in un gruppo, non contengono testo e vengono ignorate.

## Leggi le foto

La funzione è disattivata finché non la attivi. In **Connessioni**, apri WhatsApp, poi **Dettagli**, e attiva **Leggi le foto**. The Machine leggerà le foto nelle chat di lavoro: una ricevuta, uno screenshot, la foto di una lettera o di un modulo. **Anche nelle chat personali** legge anche le foto nelle chat personali. Una chat è di lavoro o personale in base a come viene classificata per la condivisione, quindi una chat con la famiglia resta personale.

The Machine scarica ogni foto una sola volta e la conserva sulla tua Machine come un allegato email: è crittografata quando la protezione dei messaggi è attiva e viene eliminata quando viene eliminato il messaggio. Il modello integrato legge ciò che mostra la foto e il testo che contiene. Questi elementi sono considerati parte del messaggio, mai istruzioni. Sono supportati JPEG, PNG e WebP fino a 5 MB. Un codice monouso contenuto in una foto viene ignorato.

L’attività e il messaggio mostrano la foto. Toccala per vederla ingrandita.

## Cosa può inviare

Un testo o un file con didascalia facoltativa, in una chat già esistente, solo dopo che approvi l’invio dall’attività. Prima dell’invio, l’attività mostra il file e puoi aprirlo. I file possono essere grandi fino a 18 MB. Se qualcuno ha scritto altri messaggi dopo quello da cui proviene un’attività, o se si tratta di un gruppo, una risposta cita il messaggio WhatsApp originale. La bozza indica **Come risposta**.

Se un’attività arriva via email, ma parli con quella persona su WhatsApp, dillo nella chat dell’attività. The Machine trova la chat esistente con quella persona e imposta WhatsApp come canale della bozza, così puoi controllarla e inviarla. Non avvia mai una nuova chat.

WhatsApp non offre un modo ufficiale per farlo. È molto improbabile che leggere i messaggi e inviare ogni tanto una risposta che hai approvato crei problemi. L’invio massivo o automatizzato può far bloccare un account.

## Collega WhatsApp

Su una Machine ospitata:

1. Nella dashboard, apri **Connessioni**, poi **Chat** e scegli WhatsApp.
2. Premi **Mostra il codice QR**.
3. Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, Collega un dispositivo e scansiona il codice QR.
4. Entro un minuto WhatsApp risulterà collegato. La cronologia delle chat continuerà a essere importata e la scheda mostrerà quanti messaggi sono stati ricevuti durante l’importazione.
   Se il collegamento richiede troppo tempo, te lo verrà segnalato dopo qualche minuto. Premi **Riprova** per riprendere da dove si era interrotto.

Stai configurando WhatsApp sul telefono e non hai un altro schermo da cui scansionare il codice? Apri **Sei sul telefono? Collega con un codice**, inserisci il tuo numero e premi **Ricevi un codice**. WhatsApp ti chiederà di inserire quel codice.

Sul tuo computer: apri **Connessioni**, poi **Chat**, scegli WhatsApp, inserisci il tuo numero di telefono con il prefisso internazionale e premi **Collega**. Verrà mostrato un codice. Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, Collega un dispositivo, poi **Collega invece con il numero di telefono** e inserisci il codice.

In alternativa, esegui `assistant connect whatsapp` e scansiona il codice mostrato nel terminale. La prima volta ti verrà proposto di installare il connettore WhatsApp, una versione fissata e verificata con il relativo checksum ([fonte](https://github.com/Salesflare/wacli)).

Nella sezione Dispositivi collegati, apparirà come The Machine. Una Machine collegata in precedenza manterrà il vecchio nome finché non la colleghi di nuovo.

Se WhatsApp disconnette la tua Machine, sulla scheda appare **WhatsApp ha scollegato questa Machine**. Premi **Riconnetti** e collegala di nuovo: inserisci il tuo numero di telefono e poi il codice mostrato da WhatsApp in Dispositivi collegati, **Collega invece con il numero di telefono**. The Machine si collegherà nello stesso posto di prima, quindi le tue chat resteranno al loro posto. Se hai configurato un tuo servizio per mantenere WhatsApp sincronizzato, si fermerà durante il collegamento e ripartirà al termine.

Se WhatsApp impiega troppo tempo a rispondere, la procedura di configurazione te lo segnalerà. Dopo un minuto, premi **Riprova** per ricevere un nuovo codice.

## Immagini

The Machine chiede a WhatsApp le foto del profilo delle persone nel tuo Graph che non ne hanno una, fino a un massimo di 50 al giorno, tramite la sincronizzazione che mantiene WhatsApp aggiornato. Non invia loro nulla. Se una persona ti nasconde la propria foto, continuerà a non essere mostrata.

## Rimuovi WhatsApp

- Su una Machine ospitata: premi **Rimuovi** accanto a WhatsApp nella pagina di configurazione. La tua Machine si scollega ed elimina i dati conservati per WhatsApp.
- Sul tuo computer: apri **Connessioni**, poi WhatsApp, **Dettagli** e **Disconnetti**. Poi scollega WhatsApp anche dal telefono.

## Scollega la Machine da WhatsApp

Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, tocca la tua Machine e scegli Esci.
