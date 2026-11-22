---
title: Linear
area: connections
summary: I tuoi ticket, menzioni, commenti, revisioni e date di scadenza in Linear. Commenti, modifiche allo stato e all’assegnatario e nuovi ticket restano in attesa della tua approvazione.
covers: connector:linear
code: connectors/linear.py, linear_writes.py
site: Sign in with Linear, Connect, More sources, Remove
translated: 1e16b6abdf4fefad
---
## Cosa legge

La tua inbox di Linear e i ticket assegnati a te. Importa:

- I ticket assegnati a te: quelli nuovi e quelli con stato, data di scadenza o titolo modificati. Quando un ticket viene completato o annullato in Linear, la relativa attività si chiude automaticamente. **Annulla** la riapre.
- Le menzioni che ti riguardano e i commenti e le risposte sui ticket che segui.
- Le richieste di revisione e i ticket aggiunti al triage.
- I promemoria per le date di scadenza.

Ogni elemento diventa un’attività solo quando richiede il tuo intervento, in base al suo contenuto. Le modifiche che apporti tu non vengono importate. La prima sincronizzazione include gli ultimi 7 giorni. Le persone vengono collegate al tuo [Graph](graph.md) tramite l’indirizzo email che Linear mostra per loro.

Per usarlo solo per fare cose, disattiva **Raccoglie segnali** in **Dettagli**.

## Cosa può fare

Ognuna di queste azioni resta in attesa della tua approvazione nell’attività:

- Commentare il ticket a cui si riferisce l’attività o rispondere nel thread di un commento. Il commento viene pubblicato a tuo nome.
- Modificare lo stato del ticket, scegliendone uno tra quelli disponibili per il suo team.
- Assegnare il ticket a una persona del suo team o a te.
- Creare un nuovo ticket in uno dei tuoi team.

Non elimina né archivia mai un ticket e non lo sposta in un altro team.

## Collegalo

1. Nella dashboard: **Connessioni**, **+ Aggiungi**, Linear. Oppure, nella pagina di configurazione di una Machine ospitata su app.themachine.computer/setup: **Altre fonti**, Linear. Sul tuo computer, prima abbina la tua Machine al tuo account.
2. Premi **Accedi con Linear**, scegli l’area di lavoro e consenti l’accesso.
3. Quando torni in The Machine, la connessione verifica subito l’accesso e mostra il nome dell’area di lavoro.

Per aggiungere un’altra area di lavoro, aggiungi di nuovo Linear. Scegli **Lavoro** o **Personale**, come per qualsiasi altra connessione.

## Incolla invece una chiave API

In **Oppure incolla una chiave API**, premi **Recupera il tuo token**. Linear apre **Impostazioni**, **Sicurezza e accesso**: crea una chiave API personale, copiala, incollala e premi **Collega**. Anche sul tuo computer, `assistant connect linear` te la chiede.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Linear, **Dettagli**, poi **Disconnetti**. I dati già importati restano.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a Linear nella pagina di configurazione.

## Revoca l’accesso in Linear

In Linear: **Impostazioni**, **Sicurezza e accesso**, poi revoca l’accesso di The Machine tra le applicazioni autorizzate. Se hai incollato una chiave, revocala nella stessa pagina.
