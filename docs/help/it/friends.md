---
title: Amici e il Network
area: fleet
summary: Aggiungi amici per nome utente, trova le persone che conosci che hanno una Machine e associa una Machine sul tuo computer.
covers: friends
code: friends.py, network.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Amici

Aggiungi qualcuno con il suo nome utente esatto, nella scheda **Fleet** sotto Amici. Gli amici possono chiedere chi conosce qualcuno, ricevere il contesto di una riunione e presentazioni dirette, e vedere quando sei occupato (solo gli orari occupati, mai cosa fai). Puoi rimuovere o bloccare un amico in qualsiasi momento.

## Trova le persone che conosci

Nel pannello Network:

- "Controlla quali miei contatti hanno una Machine" ti suggerisce persone che conosci.
- "Permetti a chi ha la mia email di trovarmi" permette loro di trovarti.

Entrambi sono attivi per impostazione predefinita, e disattivati al livello di sicurezza Prudente. Puoi disattivarli quando vuoi; la tua scelta resta. Ti trovano tramite l’email di accesso e gli indirizzi collegati, tranne quelli condivisi come info@, che restano disattivati finché non li attivi.

Le persone che conosci e che sono nel Network ti vengono suggerite appena lo attivi, e quando qualcuno si unisce più tardi. Ogni corrispondenza arriva con Collegati, Non ora o **Non suggerire mai**. **Esci dal Network** ti toglie dal Network.

## Una Machine sul tuo computer

Per unirti al Network da una Machine che gestisci tu:

1. Nella pagina del tuo account su app.themachine.computer, premi **Associa una Machine self-hosted**. Il codice funziona una volta sola, per 15 minuti.
2. Sul tuo computer, esegui `assistant fleet-pair` con il codice e riavvia.

Fino a 5 Machine per account. Da lì puoi disconnettere ciascuna.
