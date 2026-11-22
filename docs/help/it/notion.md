---
title: Notion
area: connections
summary: Commenti, menzioni e attività che ti vengono assegnate in Notion. Le risposte, le nuove pagine, le modifiche e il completamento delle attività attendono la tua conferma.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 8544baf8c60cc40b
---
## Cosa legge

Le pagine che la tua connessione a Notion può vedere. Importa:

- I commenti sulle tue pagine, le risposte alle discussioni a cui partecipi e i commenti in cui ti menzionano. Se un commento richiede il tuo intervento, diventa un’attività.
- Gli elementi dei database assegnati a te, con la relativa scadenza e lo stato. Ognuno diventa un’attività e la scadenza appare in **Calendario**. Quando completi l’elemento in Notion, l’attività si chiude da sola. **Annulla** la riapre.
- Le nuove pagine che qualcun altro aggiunge e che puoi vedere.
- Una notifica discreta quando qualcuno modifica una pagina che avevi chiesto di modificare. Non emette mai suoni.

La prima sincronizzazione include gli ultimi 7 giorni. Le persone vengono collegate al tuo [Graph](graph.md) tramite il loro indirizzo email. Se Notion non ne fornisce uno, vengono collegate solo se nel tuo Graph c’è una sola persona con lo stesso nome completo.

Per usarla solo per eseguire azioni, disattiva **Raccoglie segnali** in **Dettagli**.

## Cosa può fare

Quando un’attività o una riunione ha bisogno del testo di una pagina, la tua Machine legge quella pagina solo mentre ci lavora.

Ognuna di queste azioni attende la tua conferma nell’attività corrispondente:

- Rispondere a un commento nella relativa discussione.
- Creare una nuova pagina. Rimane privata finché non la condividi.
- Modificare una pagina. Premi **Rivedi le modifiche** per vedere ogni paragrafo prima e dopo, poi **Salva**. La tua Machine scrive solo nella pagina che hai visto. Se nel frattempo qualcuno l’ha modificata, non scrive nulla e lo segnala nell’attività.
- Segnare come completata un’attività che ti è stata assegnata. Cambia solo lo stato.

Non elimina, condivide o sposta mai una pagina.

## Collegarla

1. Nella dashboard: **Connessioni**, **Documenti e file**, Notion. Oppure, nella pagina di configurazione di una Machine ospitata su app.themachine.computer/setup: **Altre fonti**, Notion. Sul tuo computer, prima devi associarla al tuo account.
2. Premi **Accedi con Notion**, scegli l’area di lavoro e le pagine che può vedere, poi autorizza l’accesso.
3. Quando torni in The Machine, l’accesso viene controllato subito e compare il nome dell’area di lavoro.

Per aggiungere un’altra area di lavoro, collega di nuovo Notion.

## Incollare un token

In **Oppure incolla un token di integrazione**, premi **Recupera il tuo token**. Notion apre la pagina delle integrazioni: crea un’integrazione interna, consenti la lettura e l’inserimento di contenuti e commenti, e la lettura delle informazioni utente, compresi gli indirizzi email. Copia il token, incollalo e premi **Collegati**.

Poi, in Notion, condividi le tue pagine con l’integrazione, selezionando **Connessioni** su ogni pagina. Sul tuo computer, anche `assistant connect notion` te lo chiede.

## Rimuoverla

- Nella dashboard: **Connessioni**, apri Notion, **Dettagli**, poi **Disconnetti**. I contenuti già importati restano.
- Se usi una Machine ospitata, puoi anche premere **Rimuovi** accanto a Notion nella pagina di configurazione.

## Revocare l’accesso in Notion

In Notion: **Impostazioni**, **Connessioni**, poi disconnetti The Machine. Se hai incollato un token, elimina l’integrazione dalla pagina delle integrazioni.
