---
title: Microsoft Outlook e Calendario
area: connections
summary: Email e riunioni di Outlook, per Microsoft 365 e Outlook.com. Invia un'email solo dopo la tua approvazione.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
---
## Cosa legge

- **Outlook**: tutta la tua posta, gli ultimi 7 giorni quando lo colleghi, poi tutto ciò che arriva.
- **Calendario Outlook**: le tue riunioni, in sola lettura.

La posta in Altra e le newsletter ricevono prima una rapida occhiata: mittente, oggetto e qualche parola, molte alla volta. Quando una conta, viene letta per intero e può diventare un'attività. Niente viene saltato senza essere visto.

## Cosa può inviare e cambiare

- Un'email da un'attività, solo dopo che l'hai approvata nell'anteprima.
- Una risposta finisce nella conversazione Outlook dell’email a cui risponde.
- Quando posticipi un'attività su un'email, i messaggi del thread vanno in una cartella Posticipati in Outlook e tornano quando torna l'attività.

Il calendario non viene mai cambiato.

## Collegalo

Su una Machine ospitata:

1. Apri la tua pagina di configurazione su app.themachine.computer/setup.
2. Premi **Collega Microsoft** e accedi.
3. Se Microsoft chiede l'approvazione di un admin, manda questo link all'amministratore del tuo Microsoft 365: themachine.computer/m365-admin-consent. **Copia link** lo copia. Appena approva, tutti nella tua organizzazione possono collegarsi. Se sei tu, premi **Sono l'admin: approva ora**.

Oppure nella dashboard: **Connessioni**, **+ Aggiungi**, scegli Outlook e premi **Accedi con Microsoft**. Quando hai finito, torni alla dashboard. Serve l'approvazione del tuo amministratore? Lo stesso link è sotto il pulsante, con **Copia link**.

Sul tuo computer, quando è [abbinato al tuo account](friends.md#a-machine-on-your-own-computer): apri **Connessioni**, poi **+ Aggiungi**, scegli Outlook e premi **Accedi con Microsoft**. Posta e calendario si collegano insieme.

Con la tua app: apri **Usa la tua app** lì, oppure esegui `assistant connect outlook` o `assistant connect outlook_calendar`. Usa la registrazione della tua app in Microsoft Entra e un codice di accesso. Ti chiede se inviare anche ciò che approvi.

## Rimuovilo

- Su una Machine ospitata: premi **Disconnetti** accanto all'account nella tua pagina di configurazione. Nella dashboard, **Disconnetti ↗** in Connessioni ti porta lì. **Riconnetti** lì ti fa accedere di nuovo senza lasciare la dashboard.
- Sul tuo computer: **Connessioni**, apri l'account, **Dettagli**, poi **Disconnetti**.

## Disinstallalo su Microsoft

Microsoft non ci permette di revocare un accesso, quindi rimuovilo anche lì:

- Account di lavoro o scuola: myapps.microsoft.com
- Account personale: account.live.com/consent/Manage
