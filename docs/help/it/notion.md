---
title: Notion
area: connections
summary: Commenti, menzioni e attività che ti sono assegnate in Notion. Risposte, nuove pagine, modifiche e attività segnate come completate aspettano la tua conferma.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 2e93c261cc09e401
---
## Cosa legge

Le pagine che la tua connessione a Notion può vedere. Raccoglie:

- Commenti sulle tue pagine, risposte alle discussioni a cui partecipi e commenti in cui ti menzionano. Quelli che richiedono il tuo intervento diventano un’attività.
- Elementi del database assegnati a te, con data di scadenza e stato. Ognuno diventa un’attività e la scadenza compare in **Calendario**. Quando l’elemento viene completato in Notion, l’attività si chiude da sola. **Annulla** la riapre.
- Nuove pagine che altre persone aggiungono e che puoi vedere.
- Un segnale discreto quando qualcuno modifica una pagina che avevi chiesto di far modificare. Non invia mai notifiche sonore.

La prima sincronizzazione include gli ultimi 7 giorni. Le persone vengono associate al tuo [Graph](graph.md) tramite indirizzo email. Se Notion non ne fornisce uno, vengono associate solo tramite il nome completo, se nel tuo Graph c’è una sola persona con quel nome.

Per usarla solo per eseguire azioni, disattiva **Raccoglie segnali** in **Dettagli**.

## Cosa può fare

Quando un’attività o una riunione ha bisogno del testo di una pagina, la tua Machine legge quella pagina, solo mentre ci lavora. Di un file presente nella pagina vede solo il nome. Trova le pagine tramite il titolo, non tramite i file che contengono.

Ognuna di queste azioni aspetta la tua conferma nell’attività corrispondente:

- Rispondere a un commento nella relativa discussione.
- Creare una nuova pagina. Resta privata finché non la condividi.
- Modificare una pagina. Premi **Rivedi le modifiche** per vedere ogni paragrafo prima e dopo, poi **Salva**. Scrive solo nella pagina che hai visualizzato. Se nel frattempo qualcuno l’ha modificata, non scrive nulla e l’attività te lo comunica.
- Segnare come completato un compito assegnato a te. Cambia solo il suo stato.

Non elimina, condivide né sposta mai una pagina.

## Collega Notion

1. Nella dashboard: **Connessioni**, **Documenti e file**, Notion. Oppure, nella pagina di configurazione di una Machine ospitata, all’indirizzo app.themachine.computer/setup: **Altre fonti**, Notion. Sul tuo computer, prima abbinala al tuo account.
2. Premi **Accedi con Notion**, scegli l’area di lavoro e le pagine che può vedere, poi autorizza l’accesso.
3. Tornando a The Machine, controlla subito l’accesso e mostra il nome dell’area di lavoro.

Per un’altra area di lavoro, aggiungi di nuovo Notion.

## Incolla un token

In **Oppure incolla un token di integrazione**, premi **Recupera il tuo token**. Notion apre la pagina delle integrazioni: crea un’integrazione interna, autorizza la lettura e l’inserimento di contenuti e commenti e la lettura delle informazioni utente, compresi gli indirizzi email. Copia il token, incollalo e premi **Collega**.

Poi, in Notion, condividi con l’integrazione le tue pagine, usando **Connessioni** in ciascuna pagina. Sul tuo computer, te lo chiede anche `assistant connect notion`.

## Rimuovi la connessione

- Nella dashboard: **Connessioni**, apri Notion, **Dettagli**, poi **Disconnetti**. I contenuti già raccolti restano.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a Notion nella pagina di configurazione.

## Revoca l’accesso in Notion

In Notion: **Impostazioni**, **Connessioni**, poi disconnetti The Machine. Per un token incollato, elimina l’integrazione dalla pagina delle integrazioni.
