---
title: Microsoft Word: file Word in OneDrive e SharePoint
area: connections
summary: Commenti, menzioni, revisioni e condivisioni sui tuoi file Word in OneDrive e SharePoint, più nuovi documenti e modifiche che approvi. Google Docs arriverà più avanti.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Cosa legge

La connessione **Microsoft Word** legge i file Word in OneDrive e SharePoint. Accedi con Microsoft apposta, con o senza Outlook collegato. Funziona su una Machine ospitata e sul tuo computer collegato al tuo account. Google Docs arriverà più avanti: l’accesso Google di The Machine non può ancora leggere i documenti. Porta dentro:

- I documenti che qualcuno condivide con te.
- Commenti e risposte sui documenti di cui sei proprietario, e i commenti che ti menzionano.
- Le revisioni nei tuoi file Word.

La prima sincronizzazione guarda indietro di 30 giorni. Ogni elemento diventa un evento, collegato alle persone e ai progetti nel tuo [Graph](graph.md). Quando un commento richiede te, diventa un’attività.

## Cosa può fare

Quando un’attività ha bisogno del testo di un documento, la tua Machine legge solo quel documento, e solo mentre lavora su quell’attività.

Può preparare una bozza di risposta a un commento. Nei file Word non si può pubblicare una risposta dall’esterno di Word, quindi la risposta resta una bozza da copiare in Word.

Non accetta suggerimenti, non risolve commenti, non condivide file e non modifica mai un documento senza il tuo OK.

## Creare e modificare documenti

La tua Machine può scrivere un nuovo documento Word, o modificare un documento di cui parla una delle tue attività. Non scrive mai da sola:

- Prepara la modifica nell’attività. Un nuovo documento si vede per intero. Una modifica mostra ogni paragrafo prima e dopo.
- Tocca **Rivedi e crea** o **Rivedi le modifiche**, leggi, poi **Crea** o **Salva**.
- Scrive una sola volta, e solo nel documento come l’hai visto. Se qualcuno l’ha cambiato nel frattempo, non viene scritto nulla e l’attività lo dice. Chiedi una nuova bozza.
- In Talk legge ad alta voce tutta la modifica e aspetta un sì chiaro.

Sostituisce testo, aggiunge testo e aggiunge paragrafi e titoli. Lascia stare tabelle, immagini, revisioni e campi. Un nuovo documento finisce nel tuo OneDrive e resta privato finché non lo condividi.

Collegare Microsoft Word lo consente già: non c’è un passaggio a parte. Una connessione Microsoft Word di prima che legge soltanto mostra **Consenti le modifiche** sulla sua scheda in **Connessioni**. Toccalo una volta e accetta.

## Cosa chiede

Microsoft Word chiede a Microsoft un solo OK, distinto dall’accesso alla posta: leggere e modificare i tuoi file, compresi quelli condivisi con te in OneDrive e SharePoint. Ogni modifica aspetta comunque il tuo OK nella sua attività. Il tuo accesso alla posta e al calendario resta com’è. Senza Outlook, l’accesso copre solo i tuoi file, mai la posta o il calendario.

Se in seguito quell’OK viene revocato, la scheda Microsoft Word dice **In attesa del tuo OK per leggere i documenti**.

## Collegalo

Non serve avere Outlook collegato.

- Machine in hosting: nella dashboard, apri **Connessioni**, **+ Aggiungi**, scegli **Microsoft Word** e premi **Accedi con Microsoft**. Microsoft ti chiede di consentire la lettura e la modifica dei tuoi file, poi torni alla dashboard.
- Il tuo computer, abbinato al tuo account: apri **Connessioni**, **+ Aggiungi**, scegli **Microsoft Word** e premi **Accedi con Microsoft**.

Verifica che l’accesso possa leggere i documenti. Senza quell’OK non viene aggiunto. Se tocchi **Consenti le modifiche** e Microsoft non le consente, lo dice invece di mostrare Connesso.

## Lavoro o personale

Microsoft Word segue l’etichetta lavoro o personale della sua connessione, come la posta. I documenti di lavoro possono arrivare al Graph del tuo team secondo le tue [regole di condivisione](sharing-rules.md). Quelli personali mai.

## Rimuovilo

Nella dashboard: **Connessioni**, apri Microsoft Word, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato dentro resta.
