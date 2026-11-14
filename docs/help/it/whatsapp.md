---
title: WhatsApp
area: connections
summary: Le tue chat WhatsApp, lette come su un dispositivo collegato. Le risposte vengono inviate solo dopo la tua approvazione.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 881c555219a98f0f
---
## Cosa legge

Le tue chat WhatsApp, come su un dispositivo collegato al WhatsApp del tuo telefono, proprio come WhatsApp su un computer. Quando la colleghi, WhatsApp invia anche le chat meno recenti, a volte vecchie di anni. La tua Machine conserva tutto, ma solo i messaggi degli ultimi 7 giorni diventano attività.

Una foto, un messaggio vocale o un file senza didascalia viene mostrato per quello che è, ad esempio «Foto», con la relativa icona. Gli avvisi di WhatsApp, come quello sulla crittografia o sull'ingresso di qualcuno in un gruppo, non contengono testo e vengono esclusi.

## Leggi le foto

Questa funzione è disattivata finché non la attivi. In **Connessioni**, apri WhatsApp, poi **Dettagli**, e attiva **Leggi le foto**. The Machine leggerà le foto nelle tue chat di lavoro: una ricevuta, uno screenshot, la foto di una lettera o di un modulo. **Anche nelle chat personali** permette di leggere anche le foto nelle tue chat personali. Una chat è considerata di lavoro o personale in base a come la classifica la condivisione, quindi una chat con la famiglia resta personale.

The Machine scarica ogni foto una sola volta e la conserva sulla tua Machine come un allegato email: crittografata quando la protezione dei messaggi è attiva ed eliminata quando viene eliminato il messaggio. Il suo modello legge cosa mostra la foto e il testo al suo interno. Questi contenuti vengono considerati parte del messaggio, mai istruzioni. Sono supportati JPEG, PNG e WebP fino a 5 MB. Un codice monouso in una foto viene escluso.

L'attività e il messaggio mostrano la foto. Toccala per ingrandirla.

## Cosa può inviare

Un testo in una chat esistente, solo dopo che lo approvi nell'attività. Una risposta al messaggio WhatsApp da cui proviene un'attività cita quel messaggio se qualcuno ha scritto altro dopo, oppure se si tratta di un gruppo. La bozza indica **Come risposta**.

Se un'attività è arrivata via email, ma parli con quella persona su WhatsApp, dillo nella chat dell'attività. The Machine trova la chat esistente con quella persona e passa la bozza a WhatsApp, così puoi controllarla e inviarla. Non avvia mai una nuova chat.

WhatsApp non offre un modo ufficiale per farlo. Leggere e inviare ogni tanto una risposta che hai approvato difficilmente causerà problemi; gli invii di massa o automatici possono far bloccare un account.

## Collegalo

Su una Machine ospitata:

1. Nella dashboard, apri **Connessioni**, poi **Chat** e scegli WhatsApp.
2. Premi **Mostra il codice QR**.
3. Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, Collega un dispositivo e scansiona il codice QR.
4. WhatsApp risulterà collegato entro un minuto. La cronologia delle chat continuerà a essere importata e la relativa scheda conterà i messaggi man mano che arrivano.
   Se il collegamento richiede troppo tempo, vedrai un avviso dopo qualche minuto. Premi **Riprova** per riprendere da dove si era interrotto.

Stai configurando WhatsApp sul telefono e non hai un secondo schermo da cui scansionare il codice? Apri **Sei sul telefono? Collega con un codice**, inserisci il tuo numero e premi **Ottieni un codice**. WhatsApp ti chiederà quel codice.

Sul tuo computer: apri **Connessioni**, poi **Chat**, scegli WhatsApp, inserisci il tuo numero di telefono con il prefisso internazionale e premi **Collegati**. Verrà mostrato un codice. Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, Collega un dispositivo, poi **Collega con il numero di telefono** e inserisci il codice.

Oppure esegui `assistant connect whatsapp` e scansiona il codice mostrato nel terminale. La prima volta, ti verrà proposto di installare il connettore WhatsApp, una build bloccata verificata con il relativo checksum ([codice sorgente](https://github.com/Salesflare/wacli)).

In Dispositivi collegati, apparirà come The Machine. Una Machine collegata in precedenza manterrà il vecchio nome finché non la colleghi di nuovo.

## Foto del profilo

The Machine chiede a WhatsApp le foto del profilo delle persone nel tuo Graph che non ne hanno una, fino a un massimo di 50 al giorno, tramite la sincronizzazione che mantiene WhatsApp aggiornato. Non viene inviato loro nulla. Chi nasconde la propria foto a te continuerà a non averne una.

## Rimuovilo

- Su una Machine ospitata: premi **Rimuovi** accanto a WhatsApp nella pagina di configurazione. La tua Machine si scollega ed elimina i dati conservati per WhatsApp.
- Sul tuo computer: apri **Connessioni**, seleziona WhatsApp, poi **Dettagli** e **Disconnetti**. Scollega poi WhatsApp anche dal telefono.

## Scollegalo in WhatsApp

Sul telefono, apri WhatsApp, vai su Impostazioni, Dispositivi collegati, tocca la tua Machine e disconnettila.
