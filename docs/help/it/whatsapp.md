---
title: WhatsApp
area: connections
summary: Le tue chat di WhatsApp, lette come dispositivo collegato. Le risposte vengono inviate solo dopo la tua approvazione.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 9446d22f96229653
---
## Cosa legge

Le tue chat di WhatsApp, come su un dispositivo collegato al WhatsApp del tuo telefono, proprio come WhatsApp su un computer. Quando lo colleghi, WhatsApp invia anche le chat più vecchie, spesso di anni. La tua Machine conserva tutto, ma solo i messaggi degli ultimi 7 giorni diventano attività.

Una foto, un messaggio vocale o un file senza didascalia viene mostrato per quello che è, per esempio «Foto», con la relativa icona. Gli avvisi di WhatsApp, come quello sulla crittografia o sull’ingresso di qualcuno in un gruppo, non contengono testo e vengono ignorati.

## Leggi le foto

La funzione è disattivata finché non la attivi. In **Connessioni**, apri WhatsApp, poi **Dettagli**, e attiva **Leggi le foto**. The Machine leggerà le foto nelle chat di lavoro: una ricevuta, uno screenshot, la foto di una lettera o di un modulo. **Anche nelle chat personali** legge anche le foto nelle chat personali. Una chat è di lavoro o personale in base alle impostazioni di condivisione, quindi una chat con la famiglia resta personale.

The Machine scarica ogni foto una sola volta e la conserva sulla tua Machine come un allegato email: con crittografia quando la protezione dei messaggi è attiva, ed eliminata quando viene eliminato il messaggio. Il suo modello legge ciò che mostra la foto e il testo al suo interno. Questi contenuti vengono considerati parte del messaggio, mai istruzioni. Sono supportati JPEG, PNG e WebP fino a 5 MB. I codici monouso nelle foto vengono ignorati.

L’attività e il messaggio mostrano la foto. Toccala per vederla ingrandita.

## Cosa può inviare

Un testo o un file con una didascalia facoltativa, in una chat già esistente e solo dopo che approvi l’invio dall’attività. Prima dell’invio, l’attività mostra il file e puoi aprirlo. I file possono pesare fino a 18 MB. Se una risposta al messaggio WhatsApp da cui è nata un’attività cita quel messaggio, significa che nel frattempo sono stati inviati altri messaggi o che si tratta di un gruppo. La bozza indica **Come risposta**.

Se un’attività è arrivata via email, ma parli con quella persona su WhatsApp, dillo nella chat dell’attività. The Machine trova la chat esistente con quella persona e passa la bozza a WhatsApp, così puoi controllarla e inviarla. Non avvia mai una nuova chat.

WhatsApp non offre un modo ufficiale per farlo. Leggere i messaggi e inviare ogni tanto una risposta che hai approvato difficilmente causerà problemi. L’invio massivo o automatizzato può invece portare al blocco dell’account.

## Collega WhatsApp

Su una Machine ospitata:

1. Nella dashboard, apri **Connessioni**, poi **Chat** e scegli WhatsApp.
2. Premi **Mostra il codice QR**.
3. Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, Collega un dispositivo e scansiona il codice QR.
4. WhatsApp risulterà collegato entro un minuto. La cronologia delle chat continuerà ad arrivare e la relativa scheda mostrerà il conteggio dei messaggi man mano che arrivano.
   Se il collegamento richiede troppo tempo, dopo qualche minuto comparirà un avviso. Premi **Riprova** per riprendere da dove si era interrotto.

Stai configurando tutto sul telefono e non hai un secondo schermo da cui scansionare il codice? Apri **Sei sul telefono? Collega con un codice**, inserisci il tuo numero e premi **Ottieni un codice**. WhatsApp ti chiederà di inserire quel codice.

Sul tuo computer: apri **Connessioni**, poi **Chat**, scegli WhatsApp, inserisci il tuo numero di telefono con il prefisso internazionale e premi **Collegati**. Comparirà un codice. Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, Collega un dispositivo, poi **Collega con il numero di telefono** e inserisci il codice.

Oppure esegui `assistant connect whatsapp` e scansiona il codice che compare nel terminale. La prima volta ti verrà proposto di installare il connettore WhatsApp, una versione bloccata e verificata tramite checksum ([codice sorgente](https://github.com/Salesflare/wacli)).

Nei Dispositivi collegati, apparirà come The Machine. Se avevi già collegato una Machine, continuerà a comparire con il vecchio nome finché non la colleghi di nuovo.

Se WhatsApp disconnette la tua Machine, la scheda mostra **WhatsApp ha scollegato questa Machine**. Premi **Riconnetti** e collegala di nuovo.

## Immagini

The Machine chiede a WhatsApp le foto del profilo delle persone nel tuo grafo che non ne hanno una, fino a un massimo di 50 al giorno, tramite la sincronizzazione che mantiene WhatsApp aggiornato. Non viene inviato loro nulla. Se qualcuno nasconde la propria foto, continuerà a non essere visibile.

## Rimuovi WhatsApp

- Su una Machine ospitata: premi **Rimuovi** accanto a WhatsApp nella pagina di configurazione. La tua Machine si scollega ed elimina i dati conservati per WhatsApp.
- Sul tuo computer: apri WhatsApp in **Connessioni**, poi **Dettagli** e **Disconnetti**. Infine, scollega WhatsApp anche dal telefono.

## Scollega WhatsApp

Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, tocca la tua Machine e disconnettiti.
