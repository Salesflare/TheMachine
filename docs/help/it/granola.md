---
title: Granola
area: connections
summary: Note e trascrizioni delle riunioni a cui hai partecipato in Granola. Legge soltanto.
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## Cosa legge

Le note e le trascrizioni delle riunioni a cui hai partecipato in Granola: quelle degli ultimi 7 giorni al momento della connessione, poi le nuove man mano che arrivano. Le note ancora in fase di scrittura vengono importate quando Granola ha finito di prepararle.

Ognuna viene associata alla relativa riunione nel tuo Calendario, quella indicata da Granola oppure, in mancanza, quella alla stessa ora. Le note di Granola vengono inserite in Note e la trascrizione in Trascrizione, con l’etichetta **Da Granola**. Quello che hai aggiunto tu resta invariato.

Dopo la riunione, The Machine legge le note per capire cosa è stato promesso, deciso o è ancora in sospeso, per esempio "Ti mando la presentazione", e crea attività solo per i prossimi passi chiari. Le persone presenti alla riunione vengono collegate al tuo [Graph](graph.md) tramite il loro indirizzo email.

## Cosa può fare

Niente in Granola. Legge soltanto e non modifica, condivide né elimina le note.

## Cosa serve

Una chiave API personale di Granola. Granola offre le chiavi API nei piani Business ed Enterprise. La chiave legge le tue note e quelle condivise con te, così come le vedi in Granola.

## Collegare Granola

1. Nell’app desktop di Granola: **Impostazioni**, **Connectors**, **API keys**. Crea una chiave con accesso alle note personali e copiala.
2. Nella dashboard: **Connessioni**, **Riunioni**, Granola. Oppure, nella pagina di configurazione di una Machine ospitata, su app.themachine.computer/setup: **Altre fonti**, Granola. Sul tuo computer, `assistant connect granola` te lo chiede a sua volta.
3. Incolla la chiave, scegli **Lavoro** o **Personale** e premi **Collega**.

La chiave viene verificata subito. Se in seguito Granola la rifiuta, Granola in **Connessioni** ti chiederà una nuova chiave.

## Rimuovere Granola

- Nella dashboard: **Connessioni**, apri Granola, **Dettagli**, poi **Disconnetti**. I dati già importati restano.
- Su una Machine ospitata puoi anche premere **Rimuovi** accanto a Granola nella pagina di configurazione.

## Revocare la chiave in Granola

Nell’app desktop di Granola: **Impostazioni**, **Connectors**, **API keys**, poi elimina la chiave.
