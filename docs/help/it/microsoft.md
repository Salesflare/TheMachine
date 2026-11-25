---
title: Microsoft Outlook e Calendario
area: connections
summary: Email e riunioni di Outlook per Microsoft 365 e Outlook.com. L’email viene inviata solo dopo la tua approvazione.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 7229063d9365735d
---
## Cosa legge

- **Outlook**: tutte le tue email, quelle degli ultimi 7 giorni quando ti connetti e, da quel momento, tutte le nuove.
- **Calendario Outlook**: le tue riunioni, solo in lettura.

Le email in Altro e le newsletter vengono prima controllate rapidamente: mittente, oggetto e qualche parola. Se una è importante, viene letta per intero e può diventare un’attività.

## Cosa può inviare e modificare

- Un’email da un’attività, solo dopo la tua approvazione. Viene inviata dall’indirizzo della casella, non da un alias.
- Una risposta viene aggiunta alla conversazione di Outlook dell’email a cui risponde.
- Dopo l’invio di una risposta, i messaggi della conversazione vengono spostati in una cartella Posticipati di Outlook per alcuni giorni (3, a meno che l’attività non indichi diversamente) e poi tornano nella Posta in arrivo, oppure prima se qualcuno risponde. Non restano mai fuori oltre la scadenza dell’attività. La revisione te lo segnala prima dell’invio.

Il calendario non viene mai modificato.

## Foto di colleghi e contatti

A Microsoft viene chiesto anche di leggere i profili di base della tua organizzazione (nome, email e foto) e i tuoi contatti di Outlook. La tua Machine li usa solo per mostrare foto, ruoli e aziende delle persone già presenti nel tuo Graph, fino a 200 foto al giorno. Se una persona non ha una foto, viene ricontrollata dopo 30 giorni.

L’amministratore della tua organizzazione potrebbe dover approvare le foto dei colleghi. Se non lo fa, Outlook si connette comunque, ma senza queste foto. Per un account già connesso prima di questa modifica, viene creata un’attività: premi **Riconnetti** oppure **Non serve** per chiuderla definitivamente. Un account personale (Outlook.com, Hotmail) non ha colleghi, quindi l’attività chiede solo le foto dei contatti.

## Connetti Outlook

Su una Machine ospitata:

1. Apri la pagina di configurazione su app.themachine.computer/setup.
2. Premi **Collega Microsoft** e accedi.
3. Se Microsoft chiede l’approvazione dell’amministratore, invia il link all’amministratore di Microsoft 365 (**Copia link**). Dopo l’approvazione, chiunque nella tua organizzazione potrà connettersi. Se sei l’amministratore, premi **Sono l’amministratore: approva ora**.

In alternativa, dalla dashboard: apri **Connessioni**, poi **Email**, scegli Outlook e premi **Accedi con Microsoft**. Il link per l’amministratore è subito sotto il pulsante.

Sul tuo computer, dopo averla [associata al tuo account](friends.md#a-machine-on-your-own-computer): apri **Connessioni**, poi **Email**, scegli Outlook e premi **Accedi con Microsoft**. Email e calendario si connettono insieme. Dopo il passaggio su Microsoft, tornerai a **Connessioni** nella dashboard.

Per i team IT che usano una propria app Microsoft Entra: apri **Usa la tua app** lì oppure esegui `assistant connect outlook`.

## Rimuovi la connessione

- Su una Machine ospitata: premi **Disconnetti** accanto all’account nella pagina di configurazione. **Disconnetti ↗** in Connessioni ti porta a quella pagina.
- Sul tuo computer: apri **Connessioni**, seleziona l’account, poi **Dettagli** e **Disconnetti**.

## Disinstalla da Microsoft

Microsoft non ci consente di revocare un accesso, quindi rimuovi la connessione anche da lì:

- Account aziendale o scolastico: myapps.microsoft.com
- Account personale: account.live.com/consent/Manage
