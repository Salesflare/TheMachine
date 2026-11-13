---
title: Microsoft Teams
area: connections
summary: Chat di Teams, chat delle riunioni e note delle riunioni per un account aziendale o scolastico. Legge soltanto.
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
---
## Cosa legge

Le tue chat individuali, di gruppo e delle riunioni in Teams: gli ultimi 7 giorni quando lo colleghi, poi i nuovi messaggi ogni pochi minuti. Circa un anno di chat più vecchie, e di thread dei canali con l’ok del tuo admin, arriva dopo come [cronologia](history.md), un po’ alla volta, senza bloccare nulla.

Con l’OK del tuo admin legge anche:

- I thread dei canali dei tuoi team.
- Le trascrizioni delle riunioni che hai organizzato.
- Le note delle riunioni e le azioni di Copilot, se hai una licenza Microsoft 365 Copilot.

Ogni trascrizione o insieme di note finisce sulla sua riunione nel tuo calendario, segnata **Da Teams**. Senza di esse, la chat della riunione resta lì.

Bot, app e messaggi di sistema restano fuori.

## Cosa può fare

Niente in Teams. Legge soltanto. Per rispondere, apri la chat con **Apri in Teams**.

## Cosa chiede

Microsoft chiede di lasciare che The Machine legga le tue chat e il tuo profilo. Non serve un admin.

Canali, trascrizioni e note di Copilot richiedono una volta l’OK dell’admin della tua organizzazione. Fino ad allora, la scheda di Teams dice cosa non può ancora leggere e perché.

Funziona solo con un account Microsoft aziendale o scolastico. Gli account personali non hanno chat di Teams leggibili in questo modo.

## Collegalo

Su una Machine in hosting:

1. Nella dashboard, apri **Connessioni**, **+ Aggiungi** e scegli **Microsoft Teams** (sotto Chat) o **Riunioni Teams** (sotto Riunioni). Sono lo stesso accesso.
2. Premi **Accedi con Microsoft** e dai l’OK. Torni alla dashboard.
3. Per canali e note delle riunioni, manda al tuo admin il link che mostra la pagina di accesso. Quando approva, collega di nuovo Teams.

Durante la configurazione, anche la pagina di configurazione ha **Connect Microsoft Teams**.

Sul tuo computer, quando è [abbinato al tuo account](friends.md#a-machine-on-your-own-computer): apri **Connessioni**, poi **+ Aggiungi**, scegli **Microsoft Teams** o **Riunioni Teams** e premi **Accedi con Microsoft**.

## Rimuovilo

Nella dashboard: **Connessioni**, apri Microsoft Teams, **Dettagli**, poi **Disconnetti**. Quello che ha già portato resta.

## Revocalo in Microsoft

Apri myapps.microsoft.com e rimuovi The Machine. Se Outlook è collegato con lo stesso indirizzo, viene scollegato anche lui.
