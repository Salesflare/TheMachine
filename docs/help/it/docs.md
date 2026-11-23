---
title: Microsoft OneDrive
area: connections
summary: Commenti, menzioni e revisioni tracciate nei tuoi file Word su OneDrive. I nuovi documenti e le modifiche restano in attesa del tuo OK.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 41e5651f29782588
---
## Cosa legge

**Microsoft OneDrive** legge i tuoi file Word su OneDrive, su una Machine ospitata e sul tuo computer. Non serve collegare Outlook. Per Google Docs, vedi sotto. Raccoglie:

- Commenti e risposte nei tuoi file Word, compresi i commenti in cui ti menzionano.
- Le revisioni tracciate nei tuoi file Word.

La prima sincronizzazione copre i 7 giorni precedenti. Ogni elemento rimanda alle persone e ai progetti nel tuo [Graph](graph.md). Un commento che richiede il tuo intervento diventa un’attività.

## File condivisi da altre persone

Da novembre 2026, Microsoft non li elencherà più. Le condivisioni e le menzioni nei file di altre persone arriveranno alla tua Machine solo tramite le email di Microsoft. Collega anche [Outlook](microsoft.md) e lascia attive quelle email. L’attività creata da una di queste email la apre, e il relativo pulsante apre il file. Le condivisioni e le menzioni senza email non vengono rilevate.

## Cosa può fare

Quando un’attività richiede il testo di un documento, la tua Machine legge quel documento solo mentre lavora sull’attività. Può leggere file Word, PDF e di testo.

Cerca anche file di qualsiasi tipo nel tuo OneDrive personale e ti fornisce il link. Non cerca nei siti SharePoint né nei file condivisi con te. Non può leggere il testo di un PDF scansionato.

Può preparare una risposta a un commento. Word non permette di pubblicare risposte dall’esterno, quindi devi copiare la bozza in Word.

Non accetta mai un suggerimento, risolve un commento, condivide un file o modifica un documento senza il tuo OK.

Per usarla solo per svolgere attività, disattiva **Raccoglie segnali** in **Dettagli**. Da quel momento trova e legge solo i file necessari alle tue attività e ne crea di nuovi.

## Creare e modificare documenti

La tua Machine può creare un nuovo documento o modificare un documento a cui si riferisce un’attività:

- Crea subito un nuovo documento quando l’attività o una skill lo richiede. Il documento è privato e si trova nel tuo OneDrive o Google Drive personale. Nell’attività compare **Apri il documento**. La condivisione del documento o l’invio del link restano in attesa del tuo OK.
- Prepara le modifiche a un documento esistente. Premi **Rivedi le modifiche** per vedere ogni paragrafo prima e dopo, poi premi **Salva**. Se chiedi una modifica nella chat dell’attività, la applica subito.
- Scrive solo nel documento nella versione che hai visto. Se nel frattempo qualcuno lo ha modificato, non viene scritto nulla e l’attività te lo segnala. Chiedi una nuova bozza.
- In Talk, legge ad alta voce l’intera modifica e aspetta un sì esplicito.
- Se Microsoft o Google non consentono di creare un nuovo documento, l’attività spiega il motivo e mostra **Rivedi e crea** per riprovare.

Può sostituire e aggiungere testo, paragrafi e titoli. Tabelle, immagini, revisioni tracciate e campi restano invariati.

Il documento di un’attività di lavoro viene salvato nell’account dell’azienda, mai in un account personale. Sul tuo computer, un account Google collegato per Gmail con accesso a Drive può creare anche nuovi documenti Google. Se nessun account è adatto, l’attività indica cosa collegare per il lavoro: Microsoft OneDrive o Google Docs, se la tua Machine può usarlo.

Se il documento non è l’ultimo passaggio, per esempio quando bisogna inviare una risposta con il relativo link, l’attività resta aperta e prepara quel passaggio in attesa del tuo OK.

La modifica dei documenti è inclusa quando li colleghi. Una connessione precedente con solo accesso in lettura mostra **Consenti le modifiche** in **Connessioni**. Premilo una volta e accetta.

## Cosa ti chiede

Microsoft ti chiede un solo OK: leggere e modificare i tuoi file, compresi quelli condivisi con te. Ogni modifica resta comunque in attesa del tuo OK nell’attività corrispondente. L’accesso alla posta e al calendario non cambia.

Se in seguito ritiri il tuo OK, Microsoft OneDrive mostra **In attesa del tuo OK per leggere i documenti** in **Connessioni**.

## Collegarlo

Su una Machine ospitata o sul tuo computer associato al tuo account:

- Apri **Connessioni**, poi **Documenti e file**, e scegli **Microsoft OneDrive**.
- Premi **Accedi con Microsoft** e consenti di leggere e modificare i tuoi file.

Se Microsoft non consente la lettura, la connessione non viene aggiunta. Se premi **Consenti le modifiche** e Microsoft non le consente, te lo segnala.

## Google Docs

Su una Machine ospitata, apri **Connessioni**, poi **Documenti e file**, e scegli **Google Docs**. Google ti chiede di consentirle di vedere e modificare i documenti che le indichi e di crearne di nuovi. Non serve collegare Gmail e l’accesso a Gmail non cambia.

A quel punto, la tua Machine:

- Legge un Google Doc collegato nei messaggi di un’attività, solo mentre lavora su quell’attività.
- Prepara le modifiche al documento. Ognuna resta in attesa del tuo OK, come descritto sopra.
- Crea nuovi documenti privati nel tuo Google Drive.

Non cerca nel tuo Drive. Vede commenti, condivisioni e suggerimenti solo nei documenti che ha creato. Per accedere ad altro dovrebbe poter accedere all’intero Drive, cosa che non chiede.

Sul tuo computer, la tua Machine può creare un nuovo Google Doc in un account Gmail già aperto che abbia accesso a Drive. Non legge gli altri tuoi Google Docs né i relativi commenti. In **Documenti e file** compare come Google Docs, associato a quell’account. Può anche modificare un documento creato lì per un’attività.

## Lavoro o personale

La tua Machine segue l’etichetta Lavoro o Personale della connessione, come per la posta. I documenti di lavoro possono essere visibili al Graph del tuo team in base alle tue [regole di condivisione](sharing-rules.md). Quelli personali non lo sono mai.

## Rimuoverlo

Apri **Connessioni**, poi Microsoft OneDrive o Google Docs, **Dettagli** e **Disconnetti**. Smetterà di leggere i documenti. Quelli già importati restano. Su una Machine ospitata, **Disconnetti ↗** apre la pagina di configurazione che contiene i dati di accesso.
