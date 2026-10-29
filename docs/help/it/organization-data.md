---
title: Dettagli dell'organizzazione
area: graph
summary: Settore, dimensioni, sede e un logo accanto a ogni organizzazione, cercati in base al suo indirizzo web.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 2
---
## Da dove vengono

- Su una Machine in hosting, i dettagli delle organizzazioni vengono cercati per te, senza costi.
- Sul tuo computer, è disattivato finché non aggiungi una chiave per un servizio di ricerca che usi, come Apollo, People Data Labs o Hunter. Vedi la [guida alla configurazione](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Viene inviato solo l'indirizzo web dell'organizzazione, mai i tuoi messaggi o chi conosci lì. Ne vengono cercate poche alla volta, al massimo 50 al giorno, e aggiornate ogni 90 giorni. Le persone hanno una ricerca a parte: vedi [Qualifica e foto](graph.md#job-title-and-photo). Hosting condivisi e provider di posta, come google.com, sites.google.com o gmail.com, non vengono mai cercati: non sono il sito di una singola azienda.

Se la ricerca non trova un logo, o non c'è ricerca, il logo arriva dal sito dell'organizzazione stessa: l'icona indicata dalla sua home page. Viene salvato sulla tua Machine, così nessun servizio di loghi sa con chi hai a che fare. Un sito senza icona viene interpellato di nuovo dopo 30 giorni. Se la ricerca ha trovato l'organizzazione ma non un logo, viene ripetuta una volta dopo una settimana, e il logo che trova allora sostituisce l'icona del sito.

## Correggi un dettaglio sbagliato

Nella pagina dell'organizzazione:

- **Modifica** per cambiare nome, settore, dimensioni, sede, anno di fondazione, descrizione, sito web, LinkedIn e cosa rappresenta per te. Le tue modifiche restano. Svuota un campo per usare di nuovo il valore trovato.
- **Azienda sbagliata, cancella i dettagli** se ha scelto l'azienda sbagliata.
- **Cercalo di nuovo** per recuperare dettagli aggiornati.
