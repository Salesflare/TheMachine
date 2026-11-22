---
title: Microsoft OneDrive
area: connections
summary: Commenti, menzioni, modifiche registrate e condivisioni dei tuoi file Word in OneDrive e SharePoint. I nuovi documenti e le modifiche aspettano il tuo OK.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: b06d8ca4f35e5a38
---
## Cosa legge

**Microsoft OneDrive** legge i tuoi file Word in OneDrive e SharePoint, su una Machine ospitata o sul tuo computer. Non serve collegare Outlook. Per Google Docs, vedi sotto. Importa:

- I documenti che qualcuno condivide con te.
- I commenti e le risposte sui tuoi documenti, e i commenti in cui ti menzionano.
- Le modifiche registrate nei tuoi file Word.

La prima sincronizzazione copre gli ultimi 7 giorni. Ogni elemento è collegato alle persone e ai progetti nel tuo [Graph](graph.md). Un commento che richiede il tuo intervento diventa un’attività.

## Cosa può fare

Quando un’attività richiede il testo di un documento, la tua Machine legge solo quel documento e solo mentre lavora all’attività.

Può preparare una bozza di risposta a un commento. Word non permette di pubblicare risposte dall’esterno, quindi copi tu la bozza in Word.

Non accetta mai un suggerimento, risolve un commento, condivide un file o modifica un documento senza il tuo OK.

Per usarlo solo per fare cose, disattiva **Raccoglie segnali** in **Dettagli**. In questo modo trova e legge solo i documenti necessari per le tue attività e ne crea di nuovi.

## Crea e modifica documenti

La tua Machine può creare un nuovo documento o modificare un documento relativo a un’attività:

- Può creare subito un nuovo documento quando lo richiedono l’attività o una skill. Il documento è privato, nel tuo OneDrive o Google Drive. Nell’attività trovi **Apri il documento**. La condivisione del documento o l’invio del relativo link aspettano il tuo OK.
- Per un documento esistente, prepara le modifiche senza applicarle. Premi **Rivedi le modifiche** per vedere ogni paragrafo prima e dopo, poi **Salva**. Se chiedi una modifica nella chat dell’attività, la applica subito.
- Scrive solo nel documento così come l’hai visto. Se nel frattempo qualcuno lo ha modificato, non scrive nulla e te lo segnala nell’attività. Chiedi una nuova bozza.
- In Talk legge ad alta voce tutte le modifiche e aspetta un sì esplicito.
- Se Microsoft o Google non consente di creare un nuovo documento, l’attività spiega il motivo e mostra **Rivedi e crea** per riprovare.

Può sostituire e aggiungere testo, paragrafi e titoli. Tabelle, immagini, modifiche registrate e campi restano invariati.

Il documento di un’attività di lavoro viene salvato nell’account dell’azienda, mai in uno personale. Sul tuo computer, anche un account Google collegato per Gmail con accesso a Drive può creare nuovi documenti Google. Se non è disponibile un account adatto, l’attività ti dice cosa collegare per il lavoro: Microsoft OneDrive o Google Docs, se la tua Machine può usarlo.

Se il documento non è l’ultimo passaggio, per esempio se devi inviare una risposta con il relativo link, l’attività resta aperta e prepara una bozza di quel passaggio per il tuo OK.

La modifica dei documenti è inclusa quando colleghi il servizio. Una connessione precedente che consente solo la lettura mostra **Consenti le modifiche** in **Connessioni**. Premilo una volta e accetta.

## Cosa ti chiede

Microsoft ti chiede un solo OK: leggere e modificare i tuoi file, compresi quelli condivisi con te. Ogni modifica aspetta comunque il tuo OK nell’attività corrispondente. L’accesso alla posta e al calendario non cambia.

Se in seguito revochi l’OK, in **Connessioni** Microsoft OneDrive mostra **In attesa del tuo OK per leggere i documenti**.

## Collegalo

Su una Machine ospitata o sul tuo computer abbinato al tuo account:

- Apri **Connessioni**, poi **Documenti e file**, e scegli **Microsoft OneDrive**.
- Premi **Accedi con Microsoft** e consenti la lettura e la modifica dei tuoi file.

Se Microsoft non consente la lettura, la connessione non viene aggiunta. Se premi **Consenti le modifiche** e Microsoft non le consente, te lo segnala.

## Google Docs

Su una Machine ospitata, apri **Connessioni**, poi **Documenti e file**, e scegli **Google Docs**. Google ti chiede di consentire l’accesso ai documenti che indichi e di modificarli, oltre a creare nuovi documenti. Non serve collegare Gmail e l’accesso a Gmail non cambia.

La tua Machine:

- Legge un documento Google collegato nei messaggi di un’attività, solo mentre lavora a quell’attività.
- Prepara le modifiche a quel documento. Ognuna aspetta il tuo OK, come descritto sopra.
- Crea nuovi documenti privati nel tuo Google Drive.

Non cerca nel tuo Drive. Vede commenti, condivisioni e suggerimenti solo sui documenti che ha creato. Per vedere altro servirebbe l’accesso a tutto il tuo Drive, che non chiede.

Sul tuo computer, la tua Machine può creare un nuovo documento Google in un account Gmail a cui hai già effettuato l’accesso e che dispone già dell’accesso a Drive. Non legge gli altri tuoi documenti Google né i relativi commenti. In **Documenti e file** compare come Google Docs per quell’account. Può anche modificare un documento creato lì per un’attività.

## Lavoro o personale

La tua Machine segue l’etichetta Lavoro o Personale della connessione, come per la posta. I documenti di lavoro possono comparire nel Graph del tuo team, secondo le tue [regole di condivisione](sharing-rules.md). Quelli personali non vi compaiono mai.

## Rimuovilo

Apri **Connessioni**, poi Microsoft OneDrive o Google Docs, **Dettagli** e **Disconnetti**. La tua Machine smette di leggere. I contenuti già importati restano. Su una Machine ospitata, **Disconnetti ↗** apre la pagina di configurazione, dove sono conservati i dati di accesso.
