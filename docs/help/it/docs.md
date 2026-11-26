---
title: Microsoft OneDrive
area: connections
summary: Commenti, menzioni e modifiche rilevate nei tuoi file Word su OneDrive. I nuovi documenti e le modifiche aspettano il tuo OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: c8fca3cf0299e327
---
## Cosa legge

**Microsoft OneDrive** legge i tuoi file Word su OneDrive, su una Machine ospitata e sul tuo computer. Non è necessario collegare Outlook. Per Google Docs, vedi sotto. Raccoglie:

- Commenti e risposte sui tuoi file Word, e i commenti nei tuoi file in cui ti menzionano.
- Modifiche rilevate nei tuoi file Word.

La prima sincronizzazione risale a 7 giorni fa. Ogni elemento rimanda alle persone e ai progetti nel tuo [Graph](graph.md). Un commento che richiede il tuo intervento diventa un’attività.

## File condivisi con te da altre persone

A novembre 2026 Microsoft smetterà di elencare questi file. Da allora, le condivisioni e le menzioni nei file di altre persone arriveranno alla tua Machine solo tramite le email di Microsoft. Collega anche [Outlook](microsoft.md) e lascia attive queste email. Un’attività creata da una di queste email la apre, e il pulsante nell’email apre il file. Le condivisioni e le menzioni senza email non vengono rilevate.

## Cosa può fare

Quando per un’attività serve il testo di un documento, la tua Machine legge solo quel documento, e solo mentre lavora all’attività. Può leggere file Word, PDF e file di testo.

Cerca anche file di qualsiasi tipo nel tuo OneDrive e ti fornisce il link. Non cerca nei siti SharePoint né nei file condivisi con te. Non può leggere il testo di un PDF acquisito come scansione.

Può preparare una risposta a un commento. Word non permette di pubblicare risposte dall’esterno, quindi dovrai copiare la bozza in Word.

Non accetta mai un suggerimento, risolve un commento, condivide un file o modifica un documento senza il tuo OK.

Per usarla solo per svolgere attività, disattiva **Raccoglie segnali** in **Dettagli**. In questo modo trova e legge solo i file necessari per le tue attività e ne crea di nuovi.

## Crea e modifica documenti

La tua Machine può scrivere un nuovo documento o modificare un documento relativo a un’attività:

- Crea subito un nuovo documento quando l’attività o una skill lo richiede. Il documento è privato e si trova nel tuo OneDrive o Google Drive. Nell’attività compare **Apri il documento**. Condividerlo o inviarne il link aspetta il tuo OK.
- Prepara le modifiche a un documento esistente senza applicarle. Premi **Rivedi le modifiche** per vedere ogni paragrafo prima e dopo, poi **Salva**. Se chiedi una modifica nella chat dell’attività, la applica subito.
- Scrive solo nel documento nella versione che hai visto. Se nel frattempo qualcuno lo ha modificato, non viene scritto nulla e l’attività te lo comunica. Chiedi una nuova bozza.
- In Talk, legge ad alta voce tutte le modifiche e aspetta un sì esplicito.
- Se Microsoft o Google rifiuta di creare un documento, l’attività ti spiega perché e mostra **Rivedi e crea** per riprovare.

Può sostituire e aggiungere testo, paragrafi e titoli. In Google Docs può anche applicare la formattazione: grassetto, corsivo, sottolineato, link, titoli, elenchi puntati e numerati e interruzioni di pagina. **Rivedi le modifiche** mostra ogni intervento. Non può creare tabelle; immagini, modifiche rilevate e campi restano invariati.

Il documento di un’attività di lavoro viene salvato nell’account dell’azienda, mai in uno personale. Sul tuo computer, anche un account Google collegato a Gmail con accesso a Drive può essere usato per creare nuovi documenti Google. Se nessun account è adatto, l’attività ti indica cosa collegare per il lavoro: Microsoft OneDrive o Google Docs, se la tua Machine può usarlo.

Se il documento non è l’ultimo passaggio, per esempio se serve inviare una risposta con il relativo link, l’attività resta aperta e prepara quel passaggio per il tuo OK.

La possibilità di modificare è inclusa quando colleghi l’account. Una connessione precedente che consente solo la lettura mostra **Consenti le modifiche** in **Connessioni**. Premilo una volta e accetta.

## Cosa ti chiede

Microsoft ti chiede un solo OK: leggere e modificare i tuoi file, compresi quelli condivisi con te. Ogni modifica continua comunque ad aspettare il tuo OK nell’attività. L’accesso alla posta e al calendario non cambia.

Se in seguito revochi l’OK, Microsoft OneDrive mostra **In attesa del tuo OK per leggere i documenti** in **Connessioni**.

## Collegalo

Su una Machine ospitata o sul tuo computer abbinato al tuo account:

- Apri **Connessioni**, poi **Documenti e file**, e seleziona **Microsoft OneDrive**.
- Premi **Accedi con Microsoft** e consenti la lettura e la modifica dei tuoi file.

Se Microsoft non consente la lettura, l’account non viene aggiunto. Se premi **Consenti le modifiche** e Microsoft non le autorizza, te lo comunica.

## Google Docs

Su una Machine ospitata, apri **Connessioni**, poi **Documenti e file**, e seleziona **Google Docs**. Google ti chiede di consentire alla tua Machine di vedere e modificare i documenti che le indichi e di crearne di nuovi. Non è necessario collegare Gmail e l’accesso a Gmail non cambia.

A quel punto, la tua Machine:

- Legge un documento Google collegato ai messaggi di un’attività o incollato nella sua chat, solo mentre lavora all’attività.
- Prepara le modifiche al documento. Ognuna aspetta il tuo OK, come descritto sopra.
- Crea nuovi documenti privati nel tuo Google Drive.

Non cerca nel tuo Drive. Vede commenti, condivisioni e suggerimenti solo nei documenti che ha creato. Per accedere ad altro dovrebbe poter accedere a tutto il tuo Drive, ma non te lo chiede.

## Google Sheets e Slides

Se Google Docs in **Connessioni** mostra **Consenti l’accesso a Sheets e Slides**, premilo e autorizza entrambi. Google chiede di consentire alla tua Machine di vedere i tuoi file Sheets e Slides. Non può modificarli.

A quel punto, la tua Machine legge anche un file Google Sheets o Slides collegato ai messaggi di un’attività o incollato nella sua chat, solo mentre lavora all’attività:

- Dai fogli, prima le schede o le celle collegate, poi le altre schede, fino a 2.000 celle. Le formule vengono mostrate come valori. Le schede nascoste vengono lette solo se sono collegate o se lo chiedi.
- Dalle presentazioni, legge il testo e le note del relatore, in ordine. Non legge immagini e grafici.

Se il file è grande, specifica nella chat la scheda, le celle o le diapositive a cui ti riferisci. Se il file è privato di un’altra persona, è stato eliminato oppure è un file Excel o PowerPoint, l’attività te lo comunica. Un link di Google Drive funziona allo stesso modo se rimanda a un file Google Docs, Sheets o Slides.

## Google Docs sul tuo computer

Sul tuo computer, la tua Machine può creare un nuovo documento Google in un account Gmail a cui hai effettuato l’accesso e che ha già accesso a Drive. Non legge gli altri tuoi documenti Google né i relativi commenti. In **Documenti e file** compare come Google Docs per quell’account. Può anche modificare un documento creato lì per un’attività.

Legge anche un file Google Sheets o Slides collegato a un’attività o incollato nella sua chat, se quell’account Google ha già accesso a Drive, Sheets o Slides. Non chiede mai a Google ulteriori autorizzazioni. Se Google rifiuta, attiva l’API Google Sheets o Slides nel progetto Google di quell’account.

## Lavoro o personale

Segue l’etichetta Lavoro o Personale della connessione, come per la posta. I documenti di lavoro possono essere disponibili nel Graph del tuo team, in base alle [regole di condivisione](sharing-rules.md). Quelli personali non lo sono mai.

## Rimuovilo

Apri **Connessioni**, poi Microsoft OneDrive o Google Docs, **Dettagli** e **Disconnetti**. La tua Machine smette di leggere. I contenuti già acquisiti restano. Su una Machine ospitata, **Disconnetti ↗** apre la pagina di configurazione, dove si trova l’accesso.
