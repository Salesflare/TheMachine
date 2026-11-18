---
title: Chat dell’attività
area: cards
summary: Fai domande su un’attività o modifica la bozza nella chat associata a quell’attività.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 340b9cfc0e3a424d
---
## Apri la chat

Sul telefono, tocca il titolo dell’attività. Sul computer, fai clic su **Vedi nella chat ›** o sul link alla chat dell’attività. Se fai clic sul titolo dal computer, rinomini l’attività.

## Email nella chat

Ogni email mostra solo le novità. I messaggi precedenti citati sono raccolti sotto **Messaggi precedenti**. **Leggi il thread** apre le email per intero.

## Cosa ha fatto

Ogni esecuzione compare su una sola riga discreta, per esempio «Controllati 12 elementi». Aprila per vedere ogni tipo di passaggio una sola volta, con il numero di occorrenze: «Usato il browser su example.com · 7». Indica il sito, mai l’indirizzo, un comando o un file.

Quando si è fermata per chiederti qualcosa, anche la domanda compare su una riga discreta, per esempio «Ha chiesto: inviarlo oggi o lunedì?». Il tuo messaggio sotto mostra solo la tua risposta.

## Cosa chiedere

Prima che tu scriva, la chat può proporti fino a tre suggerimenti da toccare, basati sull’attività, per esempio «Proponi invece martedì alle 10:00». Toccane uno per inserirlo nel campo del messaggio, dove puoi inviarlo o modificarlo. Se non c’è un suggerimento adatto, non ne viene mostrato nessuno.

- Sul thread, sulle persone o sul contesto: «Cosa hanno chiesto l’ultima volta?»
- Per modificare la bozza: «Accorciala» o «Aggiungi la nuova data».

Una domanda riceve una risposta e non modifica la bozza. Per inviare, usa i pulsanti dell’attività: la chat non invia mai una bozza nella stessa risposta in cui l’ha scritta. Le modifiche che chiedi e che non coinvolgono nessun altro, come riordinare un documento, vengono applicate subito, senza chiederti un’altra conferma. Qualsiasi modifica che va oltre la tua richiesta aspetta il tuo via libera. Un’attività con più passaggi resta aperta finché non sono stati completati tutti.

Sul computer, premi Invio o Ctrl+Invio (Cmd+Invio su Mac) per inviare, oppure Maiusc+Invio per iniziare una nuova riga. Sul telefono, usa il pulsante di invio.

## Quando qualcosa non va

Dillo nella chat, per esempio «Non è il CEO» o «Ha lasciato l’azienda». The Machine corregge il dato alla fonte: un ruolo, un’azienda, un titolo, la fase di un progetto, il progetto dell’attività o una regola che ha imparato. La chat mostra cosa è cambiato, per esempio «Corretto: il ruolo di Sam è Head of Sales, come indicato nella firma email», con **Annulla**. Annulla ripristina il valore precedente, a meno che nel frattempo non sia cambiato.

Le altre bozze basate sul valore errato vengono rielaborate, una alla volta. Nelle rispettive chat compare «Riscrittura della bozza dopo una correzione». Le bozze che hai modificato o approvato, e quelle in fase di invio, restano come sono. La risposta indica quante ce ne sono per ciascun tipo.

In una pagina GBrain cambia solo la sezione di The Machine. Quello che hai scritto tu resta com’è. Se non riesce a capire da dove provenga un’informazione, la impara invece dalla tua nota.

## Modello e ragionamento

Sotto il campo del messaggio, la chat mostra il modello e il livello di ragionamento, per esempio «GPT-6.2 Sol» e «Ragionamento basso». Tocca uno dei due per sceglierne un altro, solo per questa chat. Le nuove chat usano le impostazioni scelte in **Impostazioni**, **Modello** (vedi [Modello](model.md)).

**Veloce**, in fondo al menu del modello, fa rispondere più in fretta le chat delle attività, con un costo circa doppio (o usando il doppio del tuo piano). Si applica ai messaggi che invii e a **Fallo**, in tutte le chat delle tue attività, mai al lavoro in background. È disattivata per impostazione predefinita e non è selezionabile per i modelli che non la supportano.

## Interrompi una risposta

Mentre viene scritta una risposta, il pulsante di invio diventa **Ferma**. Ferma interrompe subito la risposta e conserva quanto scritto fino a quel momento, contrassegnandolo come **Interrotta**. Scrivi un nuovo messaggio per continuare oppure tocca **Riprova**.

## Aggiungi file

Tocca la graffetta, incolla uno screenshot o trascina i file nella chat. Ogni file compare sopra il campo del messaggio; tocca × per rimuoverlo. Un messaggio può contenere solo file.

- Le immagini (PNG, JPEG, GIF, WebP) fino a 5 MB vengono inviate al modello come immagini.
- I PDF, i file di testo, i fogli di calcolo (CSV) e i file di Office fino a 10 MB: The Machine li legge e può allegarli a una bozza.
- Fino a 5 file per messaggio.

I file restano sulla tua Machine, cifrati come i tuoi messaggi. I file che aggiungi ma non invii vengono rimossi dopo un giorno. Puoi aggiungere file anche a una nuova attività con **Nuova attività** (vedi [Creane una tu](cards.md#make-one-yourself)).
