---
title: Microsoft OneDrive
area: connections
summary: Commenti, menzioni e modifiche rilevate nei tuoi file Word su OneDrive. I nuovi documenti e le modifiche attendono il tuo OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: e931920c74158c98
---
## Cosa legge

**Microsoft OneDrive** legge i tuoi file Word su OneDrive, sia su una Machine ospitata sia sul tuo computer. Non è necessario collegare Outlook. Per Google Docs, vedi sotto. Raccoglie:

- Commenti e risposte sui tuoi file Word, inclusi i commenti in cui ti menzionano.
- Le modifiche rilevate nei tuoi file Word.

La prima sincronizzazione copre gli ultimi 7 giorni. Ogni elemento rimanda alle persone e ai progetti nel tuo [Graph](graph.md). Un commento che richiede il tuo intervento diventa un’attività.

## File condivisi da altre persone

Da novembre 2026 Microsoft non mostrerà più questi file nell’elenco. Le condivisioni e le menzioni nei file di altre persone arriveranno alla tua Machine solo tramite le email inviate da Microsoft. Collega anche [Outlook](microsoft.md) e lascia attive queste email. Un’attività creata da un’email apre il messaggio, e il pulsante nell’email apre il file. Le condivisioni e le menzioni senza email non vengono rilevate.

## Cosa può fare

Quando un’attività richiede il testo di un documento, la tua Machine legge quel documento solo mentre lavora all’attività. Può leggere file Word, PDF e di testo.

Cerca anche file di qualsiasi tipo nel tuo OneDrive personale e ti fornisce il link. Non cerca nei siti SharePoint né nei file condivisi con te. Non può leggere il testo di un PDF scansionato.

Può preparare una risposta a un commento. Word non permette di pubblicare risposte da altre app, quindi dovrai copiare la bozza in Word.

Non accetta mai un suggerimento, risolve un commento, condivide un file o modifica un documento senza il tuo OK.

Per usarla solo per svolgere attività, disattiva **Raccoglie segnali** in **Dettagli**. In questo modo trova e legge solo i file necessari per le tue attività e ne crea di nuovi.

## Creare e modificare documenti

La tua Machine può creare un nuovo documento o modificare un documento a cui si riferisce un’attività:

- Crea subito un nuovo documento se l’attività o una skill lo richiede. È privato e viene salvato nel tuo OneDrive o Google Drive personale. Nell’attività compare **Apri il documento**. La condivisione del documento o l’invio del link attendono il tuo OK.
- Per modificare un documento esistente, prepara le modifiche senza applicarle. Premi **Rivedi le modifiche** per vedere ogni paragrafo prima e dopo, poi premi **Salva**. Le modifiche che chiedi nella chat dell’attività vengono applicate subito.
- Scrive solo nel documento che hai visualizzato. Se nel frattempo qualcuno lo ha modificato, non viene scritto nulla e l’attività te lo comunica. Chiedi di preparare una nuova bozza.
- In Talk legge ad alta voce l’intera modifica e aspetta un sì esplicito.
- Se Microsoft o Google non consentono di creare un nuovo documento, l’attività spiega il motivo e mostra **Rivedi e crea** per riprovare.

Può sostituire e aggiungere testo, paragrafi e titoli. In Google Docs può anche applicare formattazione: grassetto, corsivo, sottolineato, link, titoli, elenchi puntati e numerati e interruzioni di pagina. **Rivedi le modifiche** mostra ogni modifica. Non può creare tabelle e lascia invariati immagini, modifiche rilevate e campi.

Il documento di un’attività di lavoro viene salvato nell’account dell’azienda, mai in un account personale. Sul tuo computer, anche un account Google collegato per Gmail con accesso a Drive può ricevere nuovi documenti Google Docs. Se non c’è un account adatto, l’attività ti dice cosa collegare per il lavoro: Microsoft OneDrive o Google Docs, se la tua Machine può usarlo.

Quando il documento non è l’ultimo passaggio, per esempio se devi inviare una risposta con il link, l’attività resta aperta e prepara quel passaggio per il tuo OK.

La possibilità di modificare viene attivata quando colleghi l’account. Se una connessione esistente consente solo la lettura, in **Connessioni** compare **Consenti le modifiche**. Premilo una volta e accetta.

## Cosa richiede

Microsoft ti chiede un solo OK per leggere e modificare i tuoi file, inclusi quelli condivisi con te. Ogni modifica attende comunque il tuo OK nell’attività corrispondente. L’accesso alla posta e al calendario non cambia.

Se in seguito revochi il consenso, in **Connessioni** Microsoft OneDrive mostra **In attesa del tuo OK per leggere i documenti**.

## Collegare

Su una Machine ospitata o sul tuo computer associato al tuo account:

- Apri **Connessioni**, poi **Documenti e file**, e seleziona **Microsoft OneDrive**.
- Premi **Accedi con Microsoft** e consenti la lettura e la modifica dei tuoi file.

Se Microsoft non consente la lettura, la connessione non viene aggiunta. Se premi **Consenti le modifiche** e Microsoft non consente di modificare i file, ti verrà mostrato un messaggio.

## Google Docs

Su una Machine ospitata, apri **Connessioni**, poi **Documenti e file**, e seleziona **Google Docs**. Google ti chiede di consentire alla tua Machine di visualizzare e modificare i documenti che le indichi e di crearne di nuovi. Non è necessario collegare Gmail e l’accesso a Gmail non cambia.

La tua Machine:

- Legge un documento Google Docs collegato nei messaggi di un’attività o incollato nella relativa chat, solo mentre lavora a quell’attività.
- Prepara le modifiche al documento. Ognuna attende il tuo OK, come descritto sopra.
- Crea nuovi documenti privati nel tuo Google Drive.

Se nell’area di un’attività sono collegate più connessioni Google Docs, la tua Machine legge e modifica un file tramite una connessione che può aprirlo e modificarlo.

Non cerca nel tuo Drive. Vede commenti, condivisioni e suggerimenti solo nei documenti che ha creato. Per vedere altro dovrebbe accedere all’intero Drive, ma non te lo chiede.

## Google Sheets e Slides

Se in **Connessioni**, accanto a Google Docs, compare **Consenti l’accesso a Sheets e Slides**, premilo e consenti entrambi gli accessi. Google chiede di consentire alla tua Machine di visualizzare i file Sheets e Slides. Non può modificarli.

La tua Machine può anche leggere un file Google Sheets o Slides collegato nei messaggi di un’attività o incollato nella relativa chat, solo mentre lavora a quell’attività:

- Da un foglio, legge prima la scheda o le celle collegate, poi le altre schede, fino a 2.000 celle. Le formule vengono mostrate come valori. Le schede nascoste vengono lette solo se sono collegate o se lo chiedi.
- Dalle presentazioni, legge il testo e le note del relatore, nell’ordine. Non legge immagini e grafici.

### Modificare Sheets e Slides

Dopo che la tua Machine li ha letti, in Google Docs potrebbe comparire **Consenti modifiche a Sheets e Slides**. Premilo e consenti entrambe le modifiche. La tua Machine può così modificare un file Sheets o Slides collegato a un’attività o incollato nella relativa chat, come fa con un documento: prepara la modifica, **Rivedi le modifiche** la mostra e non viene scritto nulla finché non premi **Salva**.

- In un foglio: nuovi valori per le celle di una scheda, righe aggiunte dopo l’ultima riga o una nuova scheda. Per ogni cella vengono mostrati il valore precedente e quello nuovo. I valori vengono inseriti come testo; una formula viene inserita come formula solo se lo specifica l’attività.
- Nelle presentazioni: testo sostituito in una diapositiva, con il prima e il dopo, oppure una nuova diapositiva con titolo e testo.
- Scrive solo nel file che hai visualizzato. Se nel frattempo qualcuno ha modificato quelle celle o le diapositive, non viene scritto nulla e l’attività te lo comunica.

La formattazione, i grafici, le immagini e i file Excel o PowerPoint restano invariati.

Se il file è grande, specifica nella chat la scheda, le celle o le diapositive che intendi. Se il file è privato di un’altra persona, è stato eliminato o è un file Excel o PowerPoint, l’attività te lo comunica. Un link di Google Drive funziona allo stesso modo se rimanda a un file Google Docs, Sheets o Slides.

## Google Docs sul tuo computer

Sul tuo computer, la tua Machine può creare un nuovo documento Google Docs in un account Gmail con cui hai effettuato l’accesso e che ha già accesso a Drive. Non legge gli altri tuoi documenti Google Docs né i relativi commenti. In **Documenti e file** compare come Google Docs associato a quell’account. Può anche modificare un documento creato lì per un’attività.

Legge anche un file Google Sheets o Slides collegato a un’attività o incollato nella relativa chat, se quell’account Google ha già accesso a Drive, Sheets o Slides. Non chiede mai a Google ulteriori autorizzazioni e non modifica questi file. Se Google nega l’accesso, attiva l’API di Google Sheets o Slides nel progetto Google dell’account.

## Lavoro o personale

Come per la posta, la Machine segue l’etichetta Lavoro o Personale della connessione. I documenti di lavoro possono raggiungere il Graph del tuo team in base alle [regole di condivisione](sharing-rules.md). Quelli personali non lo raggiungono mai.

## Rimuovere la connessione

Apri **Connessioni**, poi Microsoft OneDrive o Google Docs, **Dettagli** e **Disconnetti**. La Machine smette di leggere. I contenuti già importati restano. Su una Machine ospitata, **Disconnetti ↗** apre la pagina di configurazione, dove è salvato l’accesso.
