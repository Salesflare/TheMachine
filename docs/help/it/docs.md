---
title: Google Docs e Word
area: connections
summary: Commenti, menzioni, modifiche suggerite e condivisioni sui tuoi file Google Docs o Word. Legge, e pubblica una risposta a un commento solo quando dai l’OK.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
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

Su una Machine in hosting, Docs compare sotto **+ Aggiungi** quando la tua pagina di configurazione lo offre.

Sul tuo computer:

1. Collega prima Gmail o Outlook per quell’indirizzo.
2. Apri **Connessioni**, poi **+ Aggiungi**, scegli Docs e inserisci quell’indirizzo. Oppure esegui `assistant connect docs`.
3. Verifica che il tuo accesso possa leggere i documenti. Senza quell’OK non viene aggiunto.

## Lavoro o personale

Docs segue l’etichetta lavoro o personale della sua connessione, come la posta. I documenti di lavoro possono arrivare al Graph del tuo team secondo le tue [regole di condivisione](sharing-rules.md). Quelli personali mai.

## Rimuovilo

Nella dashboard: **Connessioni**, apri Docs, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato dentro resta.
