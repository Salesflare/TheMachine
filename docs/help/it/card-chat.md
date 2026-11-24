---
title: Chat dell’attività
area: cards
summary: Fai domande su un’attività o modifica la sua bozza nella chat dedicata.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 224f6163a84e80ca
---
## Aprila

Tocca **Chat** sull’attività oppure selezionala nell’elenco della barra laterale. Tocca o fai clic sul titolo per modificarlo.

## Email nella chat

Ogni email mostra solo le novità. I messaggi precedenti citati sono raccolti sotto **Messaggi precedenti**. **Leggi il thread** apre le email per intero.

## Cosa ha fatto

Mentre lavora al tuo messaggio, l’ultimo passaggio dell’assistente compare sopra i puntini di digitazione, per esempio «Lettura dell’email», come succede sull’attività mentre si prepara. Quando usa il browser, compare anche una piccola immagine della pagina.

Ogni esecuzione completata compare su una riga discreta, per esempio «Controllati 12 elementi». Aprila per vedere ogni tipo di passaggio una sola volta, con il numero di volte in cui è stato eseguito: «Usato il browser su example.com · 7». Indica il sito, mai l’indirizzo, un comando o un file.

Quando si ferma per farti una domanda, anche la domanda compare su una riga discreta, per esempio «Ha chiesto: inviarlo oggi o lunedì?». Sotto, il tuo messaggio mostra solo la tua risposta.

## Cosa chiedere

Prima che scrivi, la chat può suggerirti fino a tre opzioni basate sull’attività, come «Proponi martedì alle 10:00». Toccandone una, il testo viene inserito nel campo del messaggio, dove puoi inviarlo o modificarlo. Se non c’è nulla di specifico da suggerire, non compare nessuna opzione.

- Per chiedere informazioni sul thread, sulle persone o sul contesto: «Cosa mi hanno chiesto l’ultima volta?»
- Per modificare la bozza: «Accorciala» oppure «Menziona la nuova data».

Una domanda riceve una risposta e non modifica la bozza. Per inviare, usa i pulsanti dell’attività: la chat non invia mai una bozza nella stessa risposta in cui l’ha scritta. Le modifiche che chiedi e che non raggiungono nessun altro, come ripulire un documento, vengono applicate subito, senza una conferma aggiuntiva. Qualsiasi cosa vada oltre la tua richiesta resta in attesa del tuo OK. Un’attività con più passaggi resta aperta finché non sono stati completati tutti.

Su un computer, premi Invio o Ctrl+Invio (Cmd+Enter su Mac) per inviare e Maiusc+Invio per andare a capo. Su un telefono, usa il pulsante di invio.

## Se qualcosa non va

Segnalalo nella chat, per esempio: «Non è il CEO» oppure «Ha lasciato l’azienda». La Machine corregge il dato alla fonte: un ruolo, un’azienda, un titolo, la fase di un progetto, il progetto dell’attività o una regola appresa. La chat mostra cosa è cambiato, per esempio «Corretto: il ruolo di Sam è Head of Sales, come indicato nella firma dell’email», con **Annulla**. Annulla ripristina il valore precedente, a meno che non sia cambiato nel frattempo.

Le altre bozze basate sul valore errato vengono riscritte, una alla volta. Nella chat compare **Riscrittura della bozza dopo una correzione**. Le bozze che hai modificato o approvato e quelle in fase di invio restano come sono. La risposta indica quante bozze ci sono per ogni tipo.

In una pagina GBrain, cambia solo la sezione di The Machine. Quello che hai scritto tu resta invariato. Se non riesce a capire da dove proviene un’informazione, la usa per imparare dalla tua nota.

## Modello e ragionamento

Sotto il campo del messaggio, la chat mostra il modello e il livello di ragionamento, per esempio «GPT-6.2 Sol» e «Ragionamento basso». Tocca uno dei due per sceglierne un altro, solo per questa chat. Le nuove chat usano le impostazioni selezionate in **Impostazioni**, **Modello** (vedi [Modello](model.md)).

**Veloce**, in fondo al menu dei modelli, fa rispondere più in fretta le chat delle attività, a circa il doppio del costo (o consumando il doppio del tuo piano). Si applica ai messaggi che invii e a **Fallo**, in tutte le chat delle attività, ma mai al lavoro in background. È disattivato per impostazione predefinita e non è disponibile per i modelli che non lo supportano.

## Interrompere una risposta

Mentre viene scritta una risposta, il pulsante di invio diventa **Ferma**. Tocca **Ferma** per interromperla subito e conservare ciò che è stato scritto fino a quel momento, contrassegnato come **Interrotta**. Scrivi un nuovo messaggio per continuare oppure tocca **Riprova**.

## Aggiungere file

Tocca la graffetta, incolla uno screenshot oppure trascina i file nella chat. Ogni file compare sopra il campo del messaggio; tocca × per rimuoverlo. Puoi inviare un messaggio con solo file.

- Le immagini (PNG, JPEG, GIF, WebP) fino a 5 MB vengono inviate al modello come immagini.
- I PDF, i file di testo, i fogli di calcolo (CSV) e i file di Office fino a 10 MB vengono letti da The Machine e possono essere allegati a una bozza.
- Fino a 5 file per messaggio.

I file restano sulla tua Machine, crittografati come i tuoi messaggi. I file che aggiungi ma non invii vengono rimossi dopo un giorno. Puoi allegare file anche a una nuova attività, da **Nuova attività** (vedi [Creane una tu](cards.md#make-one-yourself)).
