---
title: Microsoft OneDrive: file Word in OneDrive e SharePoint
area: connections
summary: Commenti, menzioni, revisioni e condivisioni sui tuoi file Word in OneDrive e SharePoint, più nuovi documenti privati, e modifiche che approvi.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Cosa legge

La connessione **Microsoft OneDrive** legge i file Word in OneDrive e SharePoint. Accedi con Microsoft apposta, con o senza Outlook collegato. Funziona su una Machine ospitata e sul tuo computer collegato al tuo account. Per Google Docs, vedi più sotto. Porta dentro:

- I documenti che qualcuno condivide con te.
- Commenti e risposte sui documenti di cui sei proprietario, e i commenti che ti menzionano.
- Le revisioni nei tuoi file Word.

La prima sincronizzazione guarda indietro di 30 giorni. Ogni elemento diventa un evento, collegato alle persone e ai progetti nel tuo [Graph](graph.md). Quando un commento richiede te, diventa un’attività.

## Cosa può fare

Quando un’attività ha bisogno del testo di un documento, la tua Machine legge solo quel documento, e solo mentre lavora su quell’attività.

Può preparare una bozza di risposta a un commento. Nei file Word non si può pubblicare una risposta dall’esterno di Word, quindi la risposta resta una bozza da copiare in Word.

Non accetta suggerimenti, non risolve commenti, non condivide file e non modifica mai un documento senza il tuo OK.

Una connessione documenti può solo fare cose: spegni **Porta segnali** in **Dettagli**, e trova e legge solo i documenti che servono ai tuoi to-do, e ne crea di nuovi. Una di Google senza accesso a tutto Drive legge i documenti dal loro link, e quelli creati dalla tua Machine.

## Creare e modificare documenti

La tua Machine può scrivere un nuovo documento, o modificare un documento di cui parla una delle tue attività:

- Un nuovo documento lo crea subito, quando l’attività o una skill dice di crearne uno: un documento privato nel tuo Google Drive o OneDrive, non condiviso con nessuno. L’attività lo mostra con **Apri il documento**. Condividerlo, o mandarne il link a qualcuno, aspetta il tuo OK.
- Una modifica a un documento esistente la prepara soltanto, ogni paragrafo prima e dopo. Tocca **Rivedi le modifiche**, leggi, poi **Salva**. Una modifica che chiedi nella chat dell’attività la fa subito.
- Scrive una modifica una sola volta, e solo nel documento come l’hai visto. Se qualcuno l’ha cambiato nel frattempo, non viene scritto nulla e l’attività lo dice. Chiedi una nuova bozza.
- In Talk legge ad alta voce tutta la modifica e aspetta un sì chiaro.
- Se Google o Microsoft rifiuta un nuovo documento, l’attività dice cosa è stato rifiutato e mostra **Rivedi e crea** per riprovare.

Sostituisce testo, aggiunge testo e aggiunge paragrafi e titoli. Lascia stare tabelle, immagini, revisioni e campi. Un nuovo documento finisce nel tuo Google Drive o OneDrive e resta privato finché non lo condividi.

Un nuovo documento va in un account dell’area dell’attività: il documento di un’attività di Lavoro nell’account di quell’azienda, quello della conversazione quando si può, mai in uno personale. Sul tuo computer, anche un account Google collegato per Gmail che ha già accesso a Drive può ricevere un nuovo Google Doc. Se nessun account va bene, l’attività dice cosa collegare per Lavoro: Microsoft OneDrive, o Google Docs dove la tua Machine può usarlo.

Quando il documento non è la fine dell’attività, come una risposta con il suo link, l’attività resta aperta e prepara quel passo successivo per il tuo OK.

Collegare Microsoft OneDrive lo consente già: non c’è un passaggio a parte. Una connessione Microsoft OneDrive di prima che legge soltanto mostra **Consenti le modifiche** sulla sua scheda in **Connessioni**. Toccalo una volta e accetta.

## Cosa chiede

Microsoft OneDrive chiede a Microsoft un solo OK, distinto dall’accesso alla posta: leggere e modificare i tuoi file, compresi quelli condivisi con te in OneDrive e SharePoint. Ogni modifica aspetta comunque il tuo OK nella sua attività. Il tuo accesso alla posta e al calendario resta com’è. Senza Outlook, l’accesso copre solo i tuoi file, mai la posta o il calendario.

Se in seguito quell’OK viene revocato, la scheda Microsoft OneDrive dice **In attesa del tuo OK per leggere i documenti**.

## Collegalo

Non serve avere Outlook collegato.

- Machine in hosting: nella dashboard, apri **Connessioni**, **+ Aggiungi**, scegli **Microsoft OneDrive** e premi **Accedi con Microsoft**. Microsoft ti chiede di consentire la lettura e la modifica dei tuoi file, poi torni alla dashboard.
- Il tuo computer, abbinato al tuo account: apri **Connessioni**, **+ Aggiungi**, scegli **Microsoft OneDrive** e premi **Accedi con Microsoft**.

Verifica che l’accesso possa leggere i documenti. Senza quell’OK non viene aggiunto. Se tocchi **Consenti le modifiche** e Microsoft non le consente, lo dice invece di mostrare Connesso.

## Google Docs

Su una Machine in hosting, apri **Connessioni**, poi **+ Aggiungi**, e scegli **Google Docs**. Google ti chiede di permetterle di vedere e modificare i documenti che le indichi, e di crearne di nuovi. Gmail non deve essere collegato, e il tuo accesso a Gmail non cambia.

Poi la tua Machine:

- Legge un documento Google collegato nei messaggi di un’attività, solo mentre lavora su quell’attività.
- Prepara modifiche a quel documento. Ognuna aspetta il tuo OK, come sopra.
- Crea nuovi documenti privati nel tuo Google Drive.

Non cerca nel tuo Drive. Vede commenti, condivisioni e suggerimenti solo sui documenti che ha creato lei. Per di più servirebbe l’accesso a tutto il tuo Drive, che non chiede.

Sul tuo computer, la tua Machine può creare un nuovo documento Google in un account Gmail collegato lì che ha già accesso a Drive. Non legge gli altri tuoi Google Docs né i loro commenti.

## Lavoro o personale

Microsoft OneDrive segue l’etichetta lavoro o personale della sua connessione, come la posta. I documenti di lavoro possono arrivare al Graph del tuo team secondo le tue [regole di condivisione](sharing-rules.md). Quelli personali mai.

## Rimuovilo

Nella dashboard: **Connessioni**, apri Microsoft OneDrive o Google Docs, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato dentro resta.
