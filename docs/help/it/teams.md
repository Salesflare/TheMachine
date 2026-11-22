---
title: Microsoft Teams
area: connections
summary: Chat di Teams, chat delle riunioni e note delle riunioni per un account aziendale o scolastico. Le risposte vengono inviate solo dopo la tua approvazione.
covers: connector:teams
code: connectors/teams.py, teams_send.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 9ca0bb08466b4d58
---
## Cosa legge

Le tue chat 1:1, di gruppo e delle riunioni in Teams: gli ultimi 7 giorni al momento della connessione, poi i nuovi messaggi ogni qualche minuto. Circa un anno di chat meno recenti e di thread nei canali, se autorizzati dal tuo amministratore, viene importato in seguito come [cronologia](history.md), poco alla volta e senza rallentare nulla.

Con l’autorizzazione del tuo amministratore, legge anche:

- I thread nei canali dei tuoi team.
- Le trascrizioni delle riunioni che hai organizzato.
- Le note delle riunioni e le attività di Copilot, se hai una licenza Microsoft 365 Copilot.

Ogni trascrizione o serie di note viene associata alla relativa riunione nel Calendario, con l’etichetta **Da Teams**. Anche senza trascrizioni o note, la chat della riunione resta disponibile.

I bot, le app e i messaggi di sistema vengono esclusi.

## Cosa può fare

Rispondere in una chat 1:1, di gruppo o di una riunione da cui proviene un’attività. The Machine prepara una bozza di risposta, che viene inviata a tuo nome e nella chat solo dopo che l’hai controllata e hai premuto **Invia ora**. Non avvia mai una nuova chat.

Non pubblica nei canali. Per rispondere in un thread di un canale, aprilo con **Apri in Teams**.

## Cosa richiede

Microsoft chiede di consentire a The Machine di leggere le tue chat e il tuo profilo e di inviare messaggi a tuo nome. Non serve l’autorizzazione dell’amministratore.

Se hai collegato Teams prima che potesse inviare messaggi, nella scheda compare **Riconnettiti per inviare le risposte.** Premi **Riconnetti** e autorizza di nuovo. Fino ad allora, la bozza resta disponibile per l’invio da Teams.

Per accedere ai canali, alle trascrizioni e alle note di Copilot, serve l’autorizzazione una tantum dell’amministratore della tua organizzazione. Fino a quel momento, nella scheda di Teams trovi ciò che non può ancora leggere e il motivo.

Funziona solo con un account Microsoft aziendale o scolastico. Con gli account personali non ci sono chat di Teams da leggere in questo modo.

## Collegalo

Su una Machine ospitata:

1. Nella dashboard, apri **Connessioni**, poi **Chat** per **Microsoft Teams** o **Riunioni** per **Riunioni Teams**. In entrambi i casi, l’accesso è lo stesso.
2. Premi **Accedi con Microsoft** e autorizza l’accesso. Tornerai alla dashboard.
3. Per i canali e le note delle riunioni, invia al tuo amministratore il link mostrato nella pagina di accesso. Dopo l’autorizzazione, collega di nuovo Teams.

Durante la configurazione, puoi anche trovare **Collega Microsoft Teams** nella pagina di configurazione.

Sul tuo computer, dopo averlo [associato al tuo account](friends.md#a-machine-on-your-own-computer): apri **Connessioni**, poi **Chat** o **Riunioni**, scegli **Microsoft Teams** o **Riunioni Teams** e premi **Accedi con Microsoft**. In questo caso legge le tue chat e le chat delle riunioni. I canali e le note delle riunioni non sono ancora disponibili.

## Rimuovilo

Nella dashboard: apri **Connessioni**, seleziona Microsoft Teams, poi **Dettagli** e **Disconnetti**. I contenuti già importati restano disponibili.

## Revoca l’accesso in Microsoft

Apri myapps.microsoft.com e rimuovi The Machine. Se Outlook è collegato con lo stesso indirizzo, verrà scollegato anche quello.
