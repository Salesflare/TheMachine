---
title: Movimenti
area: settings
summary: Un unico elenco di tutto quello che The Machine ha fatto per te, dal più recente: messaggi, documenti, risposte di Fleet, apprendimenti, connessioni e altro.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: ebb6a4cf0474a020
---
## Cosa mostra

Apri **Impostazioni**, **Movimenti**. Ogni riga mostra un’attività svolta da The Machine, dalla più recente, suddivisa per giorno:

- cosa ha fatto e com’è andata: inviata, rifiutata, non riuscita o annullata
- quando, quale account o app ha usato e [cosa l’ha autorizzata](activity.md#what-allowed-it)
- un link alla relativa attività, se presente
- per un’IA che hai collegato, come ChatGPT o Claude: il suo nome con **(connected AI)**, così puoi distinguerla da The Machine

L’elenco include messaggi e risposte, modifiche a documenti e calendari, azioni sul web, correzioni unite, agenti di coding, domande e risposte di Fleet, apprendimenti inviati al team di The Machine, skill, importazioni di Graph, informazioni che hai chiesto alla tua chat di dimenticare (con **Annulla**), connessioni aggiunte o rimosse e ogni accesso del nostro team indicato in [Accesso dell’assistenza](get-support.md#support-access), compresi quelli rifiutati.

## Cosa l’ha autorizzata

Per ogni messaggio, modifica a documenti o calendari, azione sul web e correzione unita, trovi cosa ne ha permesso l’esecuzione, così com’è avvenuta:

- **Approvato nell’attività** o **Approvato in Telegram**: hai toccato **Invia**, **Conferma** o **Unisci**
- **Approvato a voce**: hai detto sì in Talk
- **Toccato «Fallo»**: hai toccato **Fallo** nell’attività
- **Chiesto in chat**: l’hai chiesto a parole, con l’inizio del tuo messaggio tra virgolette. La citazione resta visibile solo finché quelle parole sono ancora nel tuo messaggio.
- **Ricontatto che ha inviato da sola**, **Piccola correzione, unita da sola**, **Nuovo documento privato, creato da sola** o **Preparata in anticipo, da sola**: una tua impostazione o una regola di The Machine
- **Nessuna approvazione registrata**: non è stata registrata alcuna approvazione. L’attività compare anche nelle nostre [segnalazioni di errore](error-reports.md), così possiamo trovare il passaggio che l’ha saltata.

Le azioni sul web mostrano anche l’esecuzione di un’attività che ha fatto clic o digitato su una pagina, insieme a cosa l’ha autorizzata. Il lavoro che prosegue dopo un posticipo mantiene l’autorizzazione che aveva prima.

Le righe più vecchie, registrate prima di questa modifica, mantengono le diciture precedenti, come **Dopo il tuo OK**.

## Filtra l’elenco

Scegli un tipo dall’elenco in alto, come **Messaggi** o **Fleet**. **Rifiutato o bloccato** mostra solo le attività non completate e il motivo. **Mostra altro** carica le righe meno recenti.

## Altri punti di accesso

La chat di un’attività racconta ancora la sua storia; Movimenti contiene un link per aprirla. In Fleet, **Movimenti** mostra le stesse righe relative ai tuoi Fleet e agli apprendimenti, con l’opzione **Ritira** per un apprendimento. In **Impostazioni**, **Sicurezza**, **Vedi ogni accesso in Movimenti** apre l’elenco degli accessi del nostro team.

Movimenti mostra solo quello che è successo. Non cambia mai cosa può fare The Machine.
