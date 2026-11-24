---
title: Microsoft OneDrive
area: connections
summary: Commenti, menzioni e modifiche rilevate nei tuoi file Word in OneDrive. I nuovi documenti e le modifiche aspettano il tuo OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: d79388a1c8811d5f
---
## Cosa legge

**Microsoft OneDrive** legge i tuoi file Word in OneDrive, su una Machine ospitata e sul tuo computer. Non serve collegare Outlook. Per Google Docs, vedi sotto. Raccoglie:

- Commenti e risposte sui tuoi file Word, compresi i commenti in cui ti menzionano.
- Modifiche rilevate nei tuoi file Word.

La prima sincronizzazione risale a 7 giorni prima. Ogni elemento è collegato alle persone e ai progetti nel tuo [Graph](graph.md). Un commento che richiede il tuo intervento diventa un’attività.

## File condivisi con te

A novembre 2026 Microsoft smetterà di mostrarli nell’elenco. Da quel momento, le condivisioni e le menzioni nei file di altre persone raggiungeranno la tua Machine solo tramite le email di Microsoft. Collega anche [Outlook](microsoft.md) e lascia attive quelle email. Un’attività creata da una di queste email la apre, e il relativo pulsante apre il file. Le condivisioni o le menzioni senza email non vengono rilevate.

## Cosa può fare

Quando per un’attività serve il testo di un documento, la tua Machine legge quel documento solo mentre lavora sull’attività. Può leggere file Word, PDF e di testo.

Cerca anche file di qualsiasi tipo nel tuo OneDrive personale e ti fornisce il link. Non cerca nei siti SharePoint né nei file condivisi con te. Non può leggere il testo di un PDF scansionato.

Può preparare una risposta a un commento. Word non permette di pubblicare risposte dall’esterno, quindi devi copiare la bozza in Word.

Non accetta mai un suggerimento, risolve un commento, condivide un file o modifica un documento senza il tuo OK.

Per usarla solo per svolgere attività, disattiva **Raccoglie segnali** in **Dettagli**. In questo modo trova e legge solo i file necessari per le tue attività e ne crea di nuovi.

## Crea e modifica documenti

La tua Machine può creare un nuovo documento o modificare un documento a cui si riferisce un’attività:

- Crea subito un nuovo documento quando lo richiede l’attività o una skill. Il documento è privato e viene salvato nel tuo OneDrive o Google Drive personale. Nell’attività compare **Apri il documento**. La condivisione del documento o l’invio del link aspettano il tuo OK.
- Prepara le modifiche a un documento esistente. Premi **Rivedi le modifiche** per vedere ogni paragrafo prima e dopo, poi premi **Salva**. Se chiedi una modifica nella chat dell’attività, la applica subito.
- Scrive solo nel documento che hai visto. Se nel frattempo qualcuno lo ha modificato, non scrive nulla e te lo segnala nell’attività. Chiedi una nuova bozza.
- In Talk legge ad alta voce l’intera modifica e aspetta un sì esplicito.
- Se Microsoft o Google non consente di creare un nuovo documento, l’attività spiega il motivo e mostra **Rivedi e crea** per riprovare.

Può sostituire e aggiungere testo, paragrafi e titoli. Tabelle, immagini, modifiche rilevate e campi restano invariati.

Il documento di un’attività di lavoro viene salvato nell’account dell’azienda, mai in un account personale. Sul tuo computer, anche un account Google collegato per Gmail e con accesso a Drive può creare nuovi Google Docs. Se nessun account è adatto, l’attività ti dice cosa collegare per il lavoro: Microsoft OneDrive o Google Docs, se la tua Machine può usarlo.

Se il documento non è l’ultimo passaggio, per esempio quando devi inviare una risposta con il relativo link, l’attività resta aperta e prepara quel passaggio in attesa del tuo OK.

La possibilità di modificare viene attivata quando colleghi l’account. Se una connessione precedente consente solo la lettura, in **Connessioni** compare **Consenti le modifiche**. Premilo una volta e accetta.

## Quali autorizzazioni richiede

Microsoft ti chiede un solo OK: leggere e modificare i tuoi file, compresi quelli condivisi con te. Ogni modifica aspetta comunque il tuo OK nell’attività. L’accesso alla posta e al calendario non cambia.

Se in seguito ritiri l’autorizzazione, in **Connessioni** Microsoft OneDrive mostra **In attesa del tuo OK per leggere i documenti**.

## Collega Microsoft OneDrive

Su una Machine ospitata o sul tuo computer, se è associato al tuo account:

- Apri **Connessioni**, poi **Documenti e file**, e scegli **Microsoft OneDrive**.
- Premi **Accedi con Microsoft** e consenti di leggere e modificare i tuoi file.

Se Microsoft non consente la lettura, l’account non viene aggiunto. Se premi **Consenti le modifiche** e Microsoft non le consente, te lo segnala.

## Google Docs

Su una Machine ospitata, apri **Connessioni**, poi **Documenti e file**, e scegli **Google Docs**. Google ti chiede di consentire alla tua Machine di vedere e modificare i documenti che le indichi e di crearne di nuovi. Non serve collegare Gmail e l’accesso a Gmail non cambia.

A quel punto, la tua Machine:

- Legge un Google Doc linkato nei messaggi di un’attività o incollato nella chat dell’attività, solo mentre ci lavora.
- Prepara le modifiche a quel documento. Ognuna aspetta il tuo OK, come descritto sopra.
- Crea nuovi documenti privati nel tuo Google Drive.

Non cerca nel tuo Drive. Vede commenti, condivisioni e suggerimenti solo sui documenti che ha creato. Per accedere ad altro dovrebbe poter consultare tutto il tuo Drive, ma non lo richiede.

## Google Sheets e Slides

Se in **Connessioni**, accanto a Google Docs, compare **Consenti l’accesso a Sheets e Slides**, premilo e consenti l’accesso a entrambi. Google chiede di consentire alla tua Machine di vedere i tuoi file Sheets e Slides. Non può modificarli.

A quel punto, la tua Machine legge anche un file Google Sheets o Slides linkato nei messaggi di un’attività o incollato nella chat dell’attività, solo mentre ci lavora:

- Da un foglio, legge prima la scheda o le celle linkate, poi le altre schede, fino a 2.000 celle. Le formule vengono mostrate come valori. Le schede nascoste vengono lette solo se sono linkate o se lo chiedi.
- Dalle presentazioni, legge il testo e le note del relatore, in ordine. Non legge immagini e grafici.

Per un file grande, indica nella chat la scheda, le celle o le diapositive che ti interessano. Se il file è privato di un’altra persona, è stato eliminato o è un file Excel o PowerPoint, l’attività te lo segnala. Un link di Google Drive funziona allo stesso modo se rimanda a un file Google Docs, Sheets o Slides.

## Google Docs sul tuo computer

Sul tuo computer, la tua Machine può creare un nuovo Google Doc in un account Gmail a cui hai già effettuato l’accesso e che ha accesso a Drive. Non legge gli altri tuoi Google Docs né i relativi commenti. In **Documenti e file** lo trovi come Google Docs su quell’account. Può anche modificare un documento che ha creato lì per un’attività.

Legge anche un file Google Sheets o Slides linkato in un’attività o incollato nella chat, se quell’account Google ha già accesso a Drive, Sheets o Slides. Non chiede mai a Google altri permessi. Se Google nega l’accesso, attiva l’API di Google Sheets o Slides nel progetto Google di quell’account.

## Lavoro o personale

Segue l’etichetta Lavoro o Personale della connessione, come per la posta. I documenti di lavoro possono raggiungere il Graph del tuo team in base alle [regole di condivisione](sharing-rules.md). Quelli personali non lo raggiungono mai.

## Rimuovi la connessione

Apri **Connessioni**, poi Microsoft OneDrive o Google Docs, **Dettagli** e **Disconnetti**. La tua Machine smette di leggere. I contenuti già acquisiti restano. Su una Machine ospitata, **Disconnetti ↗** apre la pagina di configurazione, dove è salvato l’accesso.
