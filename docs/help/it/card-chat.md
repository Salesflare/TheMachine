---
title: Chat dell’attività
area: cards
summary: Fai domande su un’attività o modifica la sua bozza nella chat dedicata.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 18a428fbe38a70e7
---
## Apri la chat

Seleziona **Chat** sull’attività o scegli l’attività dall’elenco nella barra laterale. Tocca o fai clic sul titolo per modificarlo.

## Email nella chat

Ogni email mostra solo le novità. I messaggi precedenti citati sono raccolti sotto **Messaggi precedenti**. **Leggi il thread** apre le email per intero.

## Cosa ha fatto

Mentre lavora, sopra la casella dei messaggi appare **Ci sto lavorando…** e nella chat vedi i puntini di digitazione. Quando usa il browser, appare anche una piccola immagine della pagina.

Quello che fa durante ogni esecuzione appare in un’unica riga discreta, con un conteggio che avanza, per esempio «Controllati 12 elementi». Aprila per vedere ogni tipo di passaggio una volta sola, con il numero di volte: «Browser usato su example.com · 7». Viene indicato il nome del sito, mai l’indirizzo, un comando o un file.

Con Claude Code, i passaggi non compaiono nella chat mentre lavora. L’ultimo passaggio appare invece sopra i puntini di digitazione, per esempio «Lettura delle email», e non compare nulla sopra la casella dei messaggi.

Se si ferma per chiederti qualcosa, anche la domanda appare in una riga discreta, per esempio «Ha chiesto: inviarlo oggi o lunedì?». Sotto, il tuo messaggio mostra solo la risposta.

## Cosa chiedere

Prima che tu scriva, la chat può suggerirti fino a tre messaggi da toccare, basati sull’attività, per esempio «Proponi invece martedì alle 10:00». Toccane uno per inserirlo nella casella dei messaggi, poi invialo o modificalo. Se non c’è nulla di pertinente, non vedrai suggerimenti.

- Sul thread, sulle persone o sul contesto: «Cosa hanno chiesto l’ultima volta?»
- Per modificare la bozza: «Rendila più breve» o «Menziona la nuova data».

Una domanda riceve risposta senza modificare la bozza. Per inviare, usa i pulsanti dell’attività: la chat non invia mai una bozza nella stessa risposta in cui l’ha scritta. Le modifiche che chiedi e che non raggiungono nessun altro, come una correzione in un documento, vengono applicate subito, senza una conferma aggiuntiva. Tutto ciò che va oltre la tua richiesta aspetta la tua approvazione. Un’attività con più passaggi resta aperta finché non sono stati completati tutti.

Su computer, premi Invio o Ctrl+Invio (Cmd+Invio su Mac) per inviare e Maiusc+Invio per andare a capo. Sul telefono, usa il pulsante di invio.

## Se c’è qualcosa che non va

Dillo nella chat, per esempio «Non è l’amministratore delegato» o «Ha lasciato l’azienda». The Machine corregge l’informazione alla fonte: un ruolo, un’azienda, un titolo, la fase di un progetto, il progetto dell’attività o una regola appresa. La chat mostra cosa è cambiato, per esempio «Corretto: il ruolo di Sam è Responsabile vendite, come indicato nella firma dell’email», con **Annulla**. Annulla ripristina il valore precedente, a meno che non sia cambiato nel frattempo.

Le altre bozze basate sul valore errato vengono rigenerate, una alla volta. Nella chat appare **Rigenerazione della bozza dopo una correzione**. Le bozze che hai modificato o approvato e quelle in fase di invio restano invariate. La risposta indica quante sono per ciascun tipo.

In una pagina GBrain, cambierà solo la sezione di The Machine. Quello che hai scritto tu resterà com’è. Se non riesce a capire da dove proviene un’informazione, la impara dalla tua nota.

## Modello e ragionamento

Sotto la casella dei messaggi, la chat mostra il modello e il livello di ragionamento, per esempio «GPT-6.2 Sol» e «Ragionamento basso». Tocca l’uno o l’altro per sceglierne un altro, solo per questa chat. Le nuove chat usano le impostazioni scelte in **Impostazioni**, **Modello** (vedi [Modello](model.md)).

**Veloce**, in fondo al menu dei modelli, fa rispondere più rapidamente le chat delle attività, a un costo circa doppio (o consumando il doppio del tuo piano). Vale per i messaggi che invii e per Fallo, in tutte le chat delle tue attività, ma mai per il lavoro in background. È disattivato per impostazione predefinita e non è selezionabile per i modelli che non lo supportano.

## Interrompi una risposta

Mentre viene scritta una risposta, il pulsante di invio diventa **Ferma**. Seleziona Ferma per interromperla subito e conservare quello che ha scritto fino a quel momento, contrassegnato come **Interrotta**. Scrivi un nuovo messaggio per continuare oppure tocca **Riprova**.

## Aggiungi file

Tocca la graffetta, incolla uno screenshot o trascina i file nella chat. Ogni file appare sopra la casella dei messaggi; tocca × per rimuoverlo. Un messaggio può contenere solo file.

- Le immagini (PNG, JPEG, GIF, WebP) fino a 5 MB vengono inviate al modello come immagini.
- PDF, file di testo, fogli di calcolo (CSV) e file Office fino a 10 MB: The Machine li legge e può allegarli a una bozza.
- Fino a 5 file per messaggio.

I file restano sulla tua Machine, crittografati come i tuoi messaggi. I file che aggiungi ma non invii vengono rimossi dopo un giorno. Puoi aggiungere file anche a una nuova attività da **Nuova attività** (vedi [Crea un’attività](cards.md#make-one-yourself)).
