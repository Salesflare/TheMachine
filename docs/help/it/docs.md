---
title: Google Docs e Word
area: connections
summary: Commenti, menzioni, modifiche suggerite e condivisioni sui tuoi file Google Docs o Word. Legge, e pubblica una risposta a un commento solo quando dai l’OK.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
site: More sources, Connect documents, Sign in with Microsoft
---
## Cosa legge

Docs usa l’accesso Google o Microsoft che hai già per quell’indirizzo. Porta dentro:

- I documenti che qualcuno condivide con te.
- Commenti e risposte sui documenti di cui sei proprietario, e i commenti che ti menzionano.
- Le modifiche suggerite sui tuoi Google Docs, e le revisioni nei tuoi file Word.

La prima sincronizzazione guarda indietro di 30 giorni. Ogni elemento diventa un evento, collegato alle persone e ai progetti nel tuo [Graph](graph.md). Quando un commento richiede te, diventa un’attività.

## Cosa può fare

Quando un’attività ha bisogno del testo di un documento, la tua Machine legge solo quel documento, e solo mentre lavora su quell’attività.

Può preparare una bozza di risposta a un commento. Su Google Docs, la risposta aspetta nell’attività: premi **Rivedi e pubblica**, controllala, poi **Pubblica ora**. Non viene pubblicato nulla finché non lo fai tu. Nei file Word non si può pubblicare una risposta dall’esterno di Word, quindi quelle risposte restano bozze da copiare in Word.

Non modifica mai un documento, non accetta suggerimenti, non risolve commenti e non condivide file.

## Cosa chiede

Leggere i documenti richiede un OK a parte, distinto dall’accesso alla posta. Il tuo accesso a Gmail e al calendario resta com’è.

- Google: accesso in sola lettura ai file e ai commenti del tuo Drive. Pubblicare le risposte richiede un altro OK, che puoi saltare.
- Microsoft: accesso in lettura ai tuoi file, compresi quelli condivisi con te in OneDrive e SharePoint.

Se in seguito quell’OK viene revocato, la scheda Docs dice **In attesa del tuo OK per leggere i documenti**.

## Collegalo

Collega prima Outlook per quell’indirizzo. Poi:

- Machine in hosting: nella tua pagina di configurazione, apri **Documenti** sotto **Altre fonti** e premi **Collega documenti** accanto a quell’indirizzo. Microsoft ti chiede di consentire la lettura dei tuoi file.
- Il tuo computer, abbinato al tuo account: apri **Connessioni**, **+ Aggiungi**, scegli **Documenti** e premi **Accedi con Microsoft**.

Verifica che l’accesso possa leggere i documenti. Senza quell’OK non viene aggiunto. I Google Docs non sono ancora disponibili tramite l’accesso di The Machine.

## Lavoro o personale

Docs segue l’etichetta lavoro o personale della sua connessione, come la posta. I documenti di lavoro possono arrivare al Graph del tuo team secondo le tue [regole di condivisione](sharing-rules.md). Quelli personali mai.

## Rimuovilo

Nella dashboard: **Connessioni**, apri Docs, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato dentro resta.
