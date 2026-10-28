---
title: Docs: Word, OneDrive e SharePoint
area: connections
summary: Commenti, menzioni, revisioni e condivisioni sui tuoi file Word in OneDrive e SharePoint. Google Docs arriverà più avanti.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
site: More sources, Connect documents, Sign in with Microsoft
---
## Cosa legge

Docs legge i file Word in OneDrive e SharePoint, con l’accesso Microsoft che hai già per quell’indirizzo. Funziona su una Machine ospitata e sul tuo computer collegato al tuo account. Google Docs arriverà più avanti: l’accesso Google di The Machine non può ancora leggere i documenti. Porta dentro:

- I documenti che qualcuno condivide con te.
- Commenti e risposte sui documenti di cui sei proprietario, e i commenti che ti menzionano.
- Le revisioni nei tuoi file Word.

La prima sincronizzazione guarda indietro di 30 giorni. Ogni elemento diventa un evento, collegato alle persone e ai progetti nel tuo [Graph](graph.md). Quando un commento richiede te, diventa un’attività.

## Cosa può fare

Quando un’attività ha bisogno del testo di un documento, la tua Machine legge solo quel documento, e solo mentre lavora su quell’attività.

Può preparare una bozza di risposta a un commento. Nei file Word non si può pubblicare una risposta dall’esterno di Word, quindi la risposta resta una bozza da copiare in Word.

Non modifica mai un documento, non accetta suggerimenti, non risolve commenti e non condivide file.

## Cosa chiede

Leggere i documenti richiede un OK a parte, distinto dall’accesso alla posta: Microsoft ti chiede di consentire la lettura dei tuoi file, compresi quelli condivisi con te in OneDrive e SharePoint. Il tuo accesso alla posta e al calendario resta com’è.

Se in seguito quell’OK viene revocato, la scheda Docs dice **In attesa del tuo OK per leggere i documenti**.

## Collegalo

Collega prima Outlook per quell’indirizzo. Poi:

- Machine in hosting: nella tua pagina di configurazione, apri **Documenti** sotto **Altre fonti** e premi **Collega documenti** accanto a quell’indirizzo. Microsoft ti chiede di consentire la lettura dei tuoi file.
- Il tuo computer, abbinato al tuo account: apri **Connessioni**, **+ Aggiungi**, scegli **Documenti** e premi **Accedi con Microsoft**.

Verifica che l’accesso possa leggere i documenti. Senza quell’OK non viene aggiunto.

## Lavoro o personale

Docs segue l’etichetta lavoro o personale della sua connessione, come la posta. I documenti di lavoro possono arrivare al Graph del tuo team secondo le tue [regole di condivisione](sharing-rules.md). Quelli personali mai.

## Rimuovilo

Nella dashboard: **Connessioni**, apri Docs, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato dentro resta.
