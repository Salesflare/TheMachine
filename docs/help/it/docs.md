---
title: Microsoft OneDrive
area: connections
summary: Commenti, menzioni e modifiche rilevate nei tuoi file Word su OneDrive. I nuovi documenti e le modifiche aspettano il tuo OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 057429e4c3b6408c
---
## Cosa legge

**Microsoft OneDrive** legge i tuoi file Word in OneDrive, sia su una Machine ospitata sia sul tuo computer. Non serve collegare Outlook. Per Google Docs, vedi sotto. Raccoglie:

- Commenti e risposte sui tuoi file Word, compresi i commenti che ti menzionano.
- Modifiche rilevate nei tuoi file Word.

La prima sincronizzazione copre gli ultimi 7 giorni. Ogni elemento rimanda alle persone e ai progetti del tuo [Graph](graph.md). Un commento che richiede il tuo intervento diventa un’attività.

## File che altri condividono con te

Da novembre 2026 Microsoft non mostrerà più questi file nell’elenco. Le condivisioni e le menzioni nei file di altre persone arriveranno quindi alla tua Machine solo tramite le email di Microsoft. Collega anche [Outlook](microsoft.md) e lascia attive quelle email. Un’attività generata da un’email apre il messaggio, e il pulsante nel messaggio apre il file. Le condivisioni e le menzioni senza un’email non vengono rilevate.

## Cosa può fare

Quando per un’attività serve il testo di un documento, la tua Machine legge solo quel documento e solo mentre svolge l’attività. Può leggere file Word, PDF e di testo.

Cerca anche file di qualsiasi tipo nel tuo OneDrive personale e ti fornisce il link. Non cerca nei siti SharePoint né nei file condivisi con te. Non può leggere il testo dei PDF scansionati.

Può preparare una risposta a un commento. Word non consente di pubblicare risposte dall’esterno, quindi devi copiare la bozza in Word.

Non accetta mai un suggerimento, risolve un commento, condivide un file o modifica un documento senza il tuo OK.

Per usarla solo per svolgere attività, disattiva **Raccoglie segnali** in **Dettagli**. In questo modo trova e legge solo i file necessari alle tue attività e ne crea di nuovi.

## Crea e modifica documenti

La tua Machine può creare un nuovo documento o modificare un documento di cui parla un’attività:

- Crea subito un nuovo documento se l’attività o una skill lo richiede. È privato e si trova nel tuo OneDrive o Google Drive personale. Nell’attività trovi **Apri il documento**. La condivisione del documento o l’invio del suo link aspetta il tuo OK.
- Prepara le modifiche a un documento esistente senza applicarle. Premi **Rivedi le modifiche** per vedere ogni paragrafo prima e dopo, poi **Salva**. Se chiedi una modifica nella chat dell’attività, la applica subito.
- Scrive solo nel documento che hai visto. Se nel frattempo qualcuno lo ha modificato, non viene scritto nulla e l’attività te lo segnala. Chiedi una nuova bozza.
- In Talk, legge ad alta voce tutte le modifiche e aspetta un sì esplicito.
- Se Microsoft o Google non consentono di creare un documento, l’attività spiega il motivo e mostra **Rivedi e crea** per riprovare.

Può sostituire e aggiungere testo, paragrafi e titoli. In Google Docs può anche applicare la formattazione: grassetto, corsivo, sottolineato, link, titoli, elenchi puntati e numerati e interruzioni di pagina. **Rivedi le modifiche** mostra ogni modifica. Non può creare tabelle, e immagini, modifiche rilevate e campi restano invariati.

Il documento di un’attività di lavoro viene salvato nell’account dell’azienda, mai in un account personale. Sul tuo computer, anche un account Google collegato per Gmail con accesso a Drive può ricevere nuovi documenti Google. Se non c’è un account adatto, l’attività ti indica cosa collegare per il lavoro: Microsoft OneDrive o Google Docs, se la tua Machine può usarlo.

Se il documento non è l’ultimo passaggio, per esempio se serve una risposta con il relativo link, l’attività resta aperta e prepara quel passaggio per il tuo OK.

La modifica dei documenti è inclusa quando colleghi il servizio. Se una connessione precedente consente solo la lettura, in **Connessioni** compare **Consenti le modifiche**. Premilo una volta e conferma.

## Cosa richiede

Microsoft ti chiede un solo OK: leggere e modificare i tuoi file, compresi quelli condivisi con te. Ogni modifica aspetta comunque il tuo OK nell’attività corrispondente. L’accesso alla posta e al calendario non cambia.

Se in seguito revochi quel consenso, in **Connessioni** Microsoft OneDrive mostra **In attesa del tuo OK per leggere i documenti**.

## Collegalo

Su una Machine ospitata, oppure sul tuo computer abbinato al tuo account:

- Apri **Connessioni**, poi **Documenti e file**, e seleziona **Microsoft OneDrive**.
- Premi **Accedi con Microsoft** e consenti di leggere e modificare i tuoi file.

Se Microsoft non consente la lettura, il servizio non viene aggiunto. Se premi **Consenti le modifiche** e Microsoft non le consente, te lo segnala.

## Google Docs

Su una Machine ospitata, apri **Connessioni**, poi **Documenti e file**, e seleziona **Google Docs**. Google ti chiede di consentire alla tua Machine di vedere e modificare i documenti che le indichi e di crearne di nuovi. Non serve collegare Gmail e l’accesso a Gmail non cambia.

La tua Machine quindi:

- Legge un documento Google collegato ai messaggi di un’attività o incollato nella chat dell’attività, solo mentre la svolge.
- Prepara le modifiche a quel documento. Ognuna aspetta il tuo OK, come descritto sopra.
- Crea nuovi documenti privati nel tuo Google Drive.

Non cerca nel tuo Drive. Vede commenti, condivisioni e suggerimenti solo nei documenti che ha creato. Per vedere altro dovrebbe accedere a tutto il tuo Drive, ma non te lo chiede.

## Google Sheets e Slides

Se in **Connessioni**, accanto a Google Docs, vedi **Consenti l’accesso a Sheets e Slides**, premilo e consenti l’accesso a entrambi. Google chiede di consentire alla tua Machine di vedere i tuoi file Sheets e Slides. Non può modificarli.

La tua Machine legge anche un file Google Sheets o Slides collegato ai messaggi di un’attività o incollato nella sua chat, solo mentre svolge l’attività:

- Nei fogli, legge prima la scheda o le celle collegate, poi le altre schede, fino a 2.000 celle. Le formule vengono mostrate come valori. Le schede nascoste vengono lette solo se sono collegate o se lo chiedi.
- Nelle presentazioni, legge il testo e le note del relatore, nell’ordine. Non legge immagini e grafici.

### Modifica Sheets e Slides

Dopo che la tua Machine li ha letti, in Google Docs potrebbe comparire anche **Consenti modifiche a Sheets e Slides**. Premilo e consenti le modifiche a entrambi. La tua Machine può quindi modificare un file Sheets o Slides collegato, proprio come un documento: prepara le modifiche, **Rivedi le modifiche** le mostra e non viene scritto nulla finché non premi **Salva**.

- In un foglio: nuovi valori nelle celle di una scheda, righe aggiunte dopo l’ultima riga o una nuova scheda. Ogni cella mostra il prima e il dopo. I valori vengono inseriti come testo; una formula viene inserita come formula solo se lo indica l’attività.
- Nelle presentazioni: testo sostituito in una slide, con il prima e il dopo, oppure una nuova slide con titolo e testo.
- Scrive solo nel file che hai visto. Se nel frattempo qualcuno ha modificato le celle o le slide, non viene scritto nulla e l’attività te lo segnala.

La formattazione, i grafici, le immagini e i file Excel o PowerPoint restano invariati.

Se il file è grande, specifica nella chat la scheda, le celle o le slide a cui ti riferisci. Se il file è privato di un’altra persona, è stato eliminato o è un file Excel o PowerPoint, l’attività te lo segnala. Un link di Google Drive funziona allo stesso modo se rimanda a un file Google Docs, Sheets o Slides.

## Google Docs sul tuo computer

Sul tuo computer, la tua Machine può creare un nuovo documento Google in un account Gmail a cui hai effettuato l’accesso e che ha già accesso a Drive. Non legge gli altri tuoi documenti Google né i relativi commenti. In **Documenti e file** compare come Google Docs, associato a quell’account. Può anche modificare un documento creato lì per un’attività.

Legge anche un file Google Sheets o Slides collegato a un’attività o incollato nella sua chat, se quell’account Google ha già accesso a Drive, Sheets o Slides. Non chiede mai altro accesso a Google e non modifica questi file. Se Google rifiuta l’accesso, attiva l’API di Google Sheets o Slides nel progetto Google associato a quell’account.

## Lavoro o personale

Come per la posta, segue l’etichetta Lavoro o Personale della connessione. I documenti di lavoro possono raggiungere il Graph del tuo team in base alle [regole di condivisione](sharing-rules.md). Quelli personali non lo raggiungono mai.

## Rimuovilo

Apri **Connessioni**, poi Microsoft OneDrive o Google Docs, **Dettagli** e **Disconnetti**. Il servizio smette di leggere i tuoi file. Quelli che ha già importato restano. Su una Machine ospitata, **Disconnetti ↗** apre la pagina di configurazione, dove è memorizzato l’accesso.
