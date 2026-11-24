---
title: Movimenti
area: settings
summary: Un unico elenco di tutto ciò che la tua Machine ha fatto per te, dal più recente: messaggi, documenti, risposte di Fleet, apprendimenti, connessioni e altro.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: 1ebeba09417a11e9
---
## Cosa mostra

Apri **Impostazioni**, **Movimenti**. Ogni riga mostra un’attività della tua Machine, in ordine cronologico inverso e raggruppata per giorno:

- cosa ha fatto e come è andata: inviata, rifiutata, non riuscita o annullata; per un messaggio [inviato più tardi](send-later.md), anche quando è stato programmato, modificato o annullato
- quando è successo e quale account o app ha usato, oltre a [cosa l’ha autorizzata](activity.md#what-allowed-it)
- un link all’attività corrispondente, se presente
- per un’IA a cui hai collegato la tua Machine, come ChatGPT o Claude: il nome seguito da **(IA collegata)**, così puoi distinguerla dalla tua Machine

L’elenco include messaggi e risposte, modifiche a documenti e calendari, passaggi sul web, correzioni unite, agenti di programmazione, domande e risposte di Fleet, apprendimenti inviati al team di The Machine, skill, importazioni da Graph, informazioni che hai chiesto alla tua chat di dimenticare (con **Annulla**), connessioni aggiunte o rimosse e ogni accesso del nostro team indicato in [Accesso dell’assistenza](get-support.md#support-access), anche quelli rifiutati.

## Cosa l’ha autorizzata

Per ogni messaggio, modifica a un documento o calendario, passaggio sul web e correzione unita, viene indicato cosa l’ha autorizzata, così com’è successo:

- **Approvato nell’attività** o **Approvato su Telegram**: hai toccato **Invia**, **Conferma** o **Unisci**
- **Approvato a voce**: hai detto di sì in Talk
- **Toccato «Fallo»**: hai toccato **Fallo** nell’attività
- **Chiesto in chat**: l’hai chiesto a parole, con l’inizio del tuo messaggio tra virgolette. La citazione viene mostrata solo finché quelle parole sono ancora nel tuo messaggio.
- **Ricontatto inviato da sola**, **Piccola correzione, unita da sola**, **Nuovo documento privato, creato da sola** o **Preparata in anticipo, da sola**: è stata un’impostazione tua o una regola della tua Machine
- **Nessuna approvazione registrata**: non è stata registrata alcuna autorizzazione. L’attività viene inclusa anche nelle nostre [segnalazioni di errore](error-reports.md), così possiamo individuare il passaggio che l’ha saltata.

I passaggi sul web includono anche l’esecuzione di un’attività che ha fatto clic o digitato su una pagina, con l’indicazione di cosa l’ha autorizzata. Il lavoro che continua dopo essere stato posticipato mantiene l’autorizzazione originale.

Le righe meno recenti, registrate prima che questa informazione fosse disponibile, mantengono la dicitura precedente, ad esempio **Dopo il tuo OK**.

## Filtra l’elenco

Scegli un tipo dall’elenco in alto, ad esempio **Messaggi** o **Fleet**. **Rifiutato o bloccato** mostra solo le attività che non sono andate a buon fine e il motivo. **Mostra altro** carica le righe meno recenti.

## Altri luoghi

La chat di un’attività racconta comunque la sua storia; Movimenti contiene un link. In Fleet, **Movimenti** mostra le stesse righe relative alle tue Fleet e ai tuoi apprendimenti, con **Ritira** per un apprendimento. In **Impostazioni**, **Sicurezza**, **Vedi ogni accesso in Movimenti** apre l’elenco degli accessi del nostro team.

Movimenti mostra solo ciò che è successo. Non cambia mai ciò che la tua Machine può fare.
