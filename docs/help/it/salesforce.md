---
title: Salesforce
area: connections
summary: Offerte, compiti e attività di Salesforce sulle persone e sui progetti. Se attivi l’opzione, può tenere aggiornati i dati di contatto lì.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## Cosa legge

Le nuove offerte e quelle che passano a un’altra fase o cambiano importo. I tuoi compiti aperti, le chiamate e gli altri compiti registrati come completati con note, oltre alle riunioni con una descrizione. I dati degli ultimi 7 giorni al momento della connessione, poi quelli nuovi ogni 15 minuti.

Ogni offerta diventa un progetto nel tuo Graph e i contatti associati compaiono nelle rispettive schede delle persone, come contatti Salesforce collegati alla loro azienda.

## Cosa può modificare

Niente, finché non attivi **Aggiorna i dati di contatto**. Le credenziali di accesso a Salesforce restano sulla tua Machine.

## Collegarlo

Su una Machine ospitata:

1. Apri la pagina di configurazione su app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri Salesforce e premi **Collega Salesforce**.
3. Accedi a Salesforce e autorizza The Machine (creata da Salesflare).

Oppure, nella dashboard: **Connessioni**, **Clienti**, seleziona Salesforce e premi **Accedi con Salesforce**. Sul tuo computer, prima associala al tuo account.

Il tuo utente Salesforce deve avere accesso API, incluso nella maggior parte delle edizioni.

## Aggiornare i dati di contatto

Quando la tua Machine trova dati più aggiornati per uno dei tuoi contatti Salesforce, può aggiornarli lì: qualifica, telefono e link LinkedIn, se la tua organizzazione ha un campo LinkedIn nei contatti.

1. In **Connessioni**, apri Salesforce e premi **Mostra cosa cambierebbe**.
2. Controlla l’elenco, poi premi **Attiva** oppure **Non ora**.

Ecco cosa tiene in considerazione:

- Solo i dati che la persona ha condiviso direttamente, per esempio sul suo profilo LinkedIn o Slack, o quelli che hai inserito nella sua scheda. Mai supposizioni.
- Solo i dati più recenti dell’ultima modifica del contatto in Salesforce. Le modifiche fatte lì hanno la precedenza.
- Solo i campi diversi, mai quelli vuoti. Non modifica mai l’indirizzo email né l’azienda.
- Ogni modifica appare come una riga datata nella scheda della persona.

Premi **Disattiva** per interrompere. Una connessione condivisa dalla tua Fleet consente solo la lettura.

## Rimuoverlo

- Nella dashboard: **Connessioni**, apri Salesforce, **Dettagli**, poi **Disconnetti**. I dati già importati restano.
- Su una Machine ospitata, **Disconnetti ↗** apre la pagina di configurazione: premi **Rimuovi** accanto a Salesforce.

## Revocare l’accesso in Salesforce

In Salesforce, apri le impostazioni personali, poi Connected Apps OAuth Usage, oppure chiedi all’amministratore di revocare l’accesso di The Machine. A quel punto non potrà più leggere né modificare nulla.
