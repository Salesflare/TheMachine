---
title: Microsoft Outlook e Calendario
area: connections
summary: Email e riunioni di Outlook, per Microsoft 365 e Outlook.com. Le email vengono inviate solo dopo la tua approvazione.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: c10bf70a327b8ec0
---
## Cosa legge

- **Outlook**: tutte le tue email degli ultimi 7 giorni quando lo colleghi, poi tutte le nuove email.
- **Calendario Outlook**: le tue riunioni, in sola lettura.

Le email in Altro e le newsletter vengono prima controllate rapidamente: mittente, oggetto e poche parole. Se una è importante, viene letta per intero e può diventare un’attività.

## Cosa può inviare e modificare

- Un’email da un’attività, solo dopo la tua approvazione. Viene inviata dall’indirizzo della casella di posta, non da un alias.
- Una risposta viene aggiunta alla conversazione di Outlook dell’email a cui risponde.
- Dopo l’invio di una risposta, i messaggi della conversazione vengono spostati in una cartella Posticipati in Outlook per alcuni giorni (3, a meno che l’attività non indichi diversamente), poi tornano nella Posta in arrivo o prima se qualcuno risponde. La revisione te lo segnala prima dell’invio.

Il calendario non viene mai modificato.

## Foto di colleghi e contatti

A Microsoft viene chiesta anche l’autorizzazione a leggere i profili di base delle persone della tua organizzazione (nome, email e foto) e i tuoi contatti di Outlook. La tua Machine li usa solo per recuperare foto, qualifiche e aziende delle persone già presenti nel tuo Graph, fino a 200 foto al giorno. Le persone senza foto vengono ricontrollate dopo 30 giorni.

L’amministratore della tua organizzazione potrebbe dover approvare le foto dei colleghi. Se non lo fa, Outlook si collega comunque, ma senza queste foto. Un account collegato in precedenza riceve un’attività: premi **Riconnetti** oppure **Non serve** per chiuderla definitivamente. Un account personale (Outlook.com, Hotmail) non ha colleghi, quindi la sua attività riguarda solo le foto dei contatti.

## Collegalo

Su una Machine ospitata:

1. Apri la pagina di configurazione all’indirizzo app.themachine.computer/setup.
2. Premi **Collega Microsoft** e accedi.
3. Se Microsoft chiede l’approvazione di un amministratore, invia il link al tuo amministratore di Microsoft 365 (**Copia link**). Dopo l’approvazione, tutti i membri della tua organizzazione potranno collegarsi. Se sei l’amministratore, premi **Sono l’amministratore: approva ora**.

Oppure, nella dashboard: **Connessioni**, **Email**, scegli Outlook e premi **Accedi con Microsoft**. Il link per l’amministratore si trova subito sotto il pulsante.

Sul tuo computer, dopo averlo [abbinato al tuo account](friends.md#a-machine-on-your-own-computer): apri **Connessioni**, poi **Email**, scegli Outlook e premi **Accedi con Microsoft**. La posta e il calendario si collegano insieme. Dopo aver completato l’accesso a Microsoft, torni in **Connessioni** nella dashboard.

Per i team IT che usano una propria app Microsoft Entra: apri **Usa la tua app** oppure esegui `assistant connect outlook`.

## Rimuovilo

- Su una Machine ospitata: premi **Disconnetti** accanto all’account nella pagina di configurazione. **Disconnetti ↗** in Connessioni ti porta lì.
- Sul tuo computer: **Connessioni**, apri l’account, **Dettagli**, poi **Disconnetti**.

## Disinstalla l’app da Microsoft

Microsoft non ci permette di revocare un accesso, quindi rimuovilo anche da lì:

- Account aziendale o dell’istituto di istruzione: myapps.microsoft.com
- Account personale: account.live.com/consent/Manage
