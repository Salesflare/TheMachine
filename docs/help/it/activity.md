---
title: Movimenti
area: settings
summary: Un elenco di tutto ciò che The Machine ha fatto per te, dal più recente: messaggi, documenti, risposte del Fleet, apprendimenti, connessioni e altro.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
---
## Cosa mostra

Apri **Impostazioni**, **Movimenti**. Ogni riga è una cosa che The Machine ha fatto, dalla più recente, per giorno:

- cosa ha fatto e come è finita: inviato, rifiutato, non riuscito o annullato
- quando, l’account o l’app che ha usato e [cosa l’ha permessa](activity.md#what-allowed-it)
- un link alla sua attività, quando c’è
- per un’IA che hai collegato, come ChatGPT o Claude: il suo nome con **(IA collegata)**, per distinguerla da The Machine

Elenca messaggi e risposte, modifiche a documenti e calendario, passaggi sul web, correzioni che ha unito, agenti di programmazione, domande e risposte del Fleet, apprendimenti inviati al team di The Machine, skill, importazioni nel Graph, fatti che hai chiesto di dimenticare in chat (con **Annulla**), connessioni aggiunte o rimosse, e ogni accesso del nostro team con l’[Accesso per l’assistenza](get-support.md#support-access), anche quelli rifiutati.

## Cosa l’ha permessa

Ogni messaggio, modifica a documenti o calendario, passaggio sul web e correzione unita dice cosa l’ha lasciata partire, come è successo:

- **Approvato nell’attività** o **Approvato in Telegram**: il tuo tocco su Invia, Conferma o Unisci
- **Approvato a voce**: il tuo sì in Talk
- **Toccato «Fallo»**: il tuo Fallo sull’attività
- **Chiesto in chat**: l’hai chiesto a parole, con l’inizio del tuo messaggio tra virgolette. Una citazione appare solo finché quelle parole restano nel tuo messaggio.
- **Ricontatto che ha inviato da sola**, **Piccola correzione, unita da sola**, **Nuovo documento privato, creato da sola** o **Preparata in anticipo, da sola**: una tua impostazione o una regola propria di The Machine
- **Nessuna approvazione registrata**: non è stato registrato nulla. Va anche nei nostri [rapporti di errore](error-reports.md), così troviamo il percorso che l’ha mancata.

Passaggi sul web elenca anche l’esecuzione di un’attività che ha cliccato o scritto su una pagina, con cosa ha permesso quell’esecuzione.

Le righe più vecchie, di prima che venisse registrato, mantengono le parole di allora, come **Dopo il tuo OK**.

## Filtrare

Scegli un tipo nell’elenco in alto, come **Messaggi** o **Fleet**. **Rifiutato o bloccato** mostra solo ciò che non è partito, e perché. **Mostra altro** carica righe più vecchie.

## Altri posti

La chat di un’attività racconta sempre la propria storia; Movimenti rimanda lì. Fleet, **Movimenti** mostra le stesse righe per i tuoi Fleet e apprendimenti, con **Ritira** per un apprendimento. In Impostazioni, **Sicurezza**, **Vedi ogni accesso in Movimenti** apre gli accessi del nostro team.

Movimenti mostra solo ciò che è successo. Non cambia mai ciò che The Machine può fare.
