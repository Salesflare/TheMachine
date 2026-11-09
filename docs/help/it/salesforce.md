---
title: Salesforce
area: connections
summary: Trattative, attività e cronologia da Salesforce sulle tue persone e sui tuoi progetti. Se lo attivi, tiene aggiornati lì i dati di contatto.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
---
## Cosa legge

Le nuove trattative, e quelle che passano a un’altra fase o cambiano importo. Le tue attività aperte, chiamate e altre attività registrate come fatte con note, e riunioni con una descrizione. Gli ultimi 7 giorni quando colleghi, poi le nuove ogni 15 minuti.

Ogni trattativa diventa un progetto nel tuo Graph, e i suoi contatti compaiono sulle loro persone, come contatto Salesforce presso il loro account.

## Cosa può cambiare

Niente, finché non attivi **Aggiorna dati di contatto**. Il tuo accesso a Salesforce resta sulla tua Machine.

## Collegalo

Su una Machine in hosting:

1. Apri la tua pagina di configurazione su app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri Salesforce e premi **Collega Salesforce**.
3. Accedi a Salesforce e consenti The Machine (fatta da Salesflare).

Oppure nella dashboard: **Connessioni**, **+ Aggiungi**, scegli Salesforce e premi **Accedi con Salesforce**.

Il tuo utente Salesforce ha bisogno dell’accesso API, incluso nella maggior parte delle edizioni.

## Aggiorna dati di contatto

Quando la tua Machine conosce dati più recenti di uno dei tuoi contatti Salesforce, può aggiornare quel contatto lì: ruolo, telefono, e il link LinkedIn se la tua org ha un campo LinkedIn sui contatti.

1. In **Connessioni**, apri Salesforce e premi **Mostra cosa cambierebbe**.
2. Controlla l’elenco, poi premi **Attiva** o **Non ora**.

Cosa rispetta:

- Solo dati nelle parole della persona stessa, come il suo profilo LinkedIn o Slack, o quelli che hai messo tu sulla sua pagina. Mai un’ipotesi.
- Solo quando il dato è più recente dell’ultima modifica del contatto in Salesforce. Una modifica fatta lì vince.
- Solo i campi diversi, e mai un valore vuoto. Non cambia mai l’indirizzo email né l’account.
- Ogni modifica è una riga datata sulla pagina della persona.

Premi **Disattiva** per smettere. Una connessione condivisa dal tuo Fleet legge soltanto.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Salesforce, **Dettagli**, poi **Disconnetti**. Quello che ha già portato resta.
- Su una Machine in hosting puoi anche premere **Rimuovi** accanto nella tua pagina di configurazione.

## Revocalo in Salesforce

In Salesforce, apri le tue impostazioni personali, poi Connected Apps OAuth Usage, o chiedi al tuo admin, e revoca The Machine. Non può più leggere né cambiare nulla.
