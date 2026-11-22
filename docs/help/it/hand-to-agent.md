---
title: Passa a Claude Code o Codex
area: cards
summary: Invia un’attività di programmazione a Claude Code o Codex. Il risultato torna nell’attività.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 22e1b9b950988a58
---
## Passa un’attività

1. Nell’attività, apri **…**, poi **Passa…** e scegli **Codex** o **Claude Code**. Vengono mostrati solo gli strumenti che hai configurato.
2. Controlla il riepilogo e cosa riceverà, aggiungi una nota se vuoi e premi **Passa**. **Vedi il lavoro completo** mostra tutte le istruzioni.

L’attività mostra che è in corso, poi il risultato, con **Cosa ha fatto** e **Mostra modifiche**. **Chiedi modifiche** indica cosa cambiare. **Passa…** nel menu **…** ricomincia da capo. **Nascondi** nasconde il risultato. Quando passi un’attività bloccata, durante l’esecuzione del lavoro mostra **In corso…** invece di **Bloccata**.

Il lavoro non invia mai nulla per conto tuo. Se lascia a te un passaggio di pubblicazione o distribuzione, **Fallo** nell’attività esegue quel passaggio. La risposta che scrive resta una bozza da inviare tu.

## Nell’app Codex

- **Apri in Codex** apre la conversazione del lavoro nell’app Codex, una volta terminato.
- **Chiedi modifiche** continua nella stessa conversazione di Codex e l’attività segue la conversazione.
- Il lavoro si interrompe dopo 30 minuti senza progressi o dopo 6 ore complessive. Un riavvio non lo interrompe.

## Configurazione

In **Impostazioni**, **Modello**, sotto **Codex e Claude Code**:

- **Codex**: dove viene eseguito. Sulla tua Machine o sul tuo computer non serve configurare altro qui; **Cambia** apre la pagina di configurazione.
- **Codex cloud**: l’ID dell’ambiente, da Codex, e, se vuoi, un **Branch** da cui partire.
- **Claude Code**: il link a una sessione di Claude Code.

Claude invia il risultato tramite il connettore di The Machine. Aggiungilo una volta in claude.ai, in Impostazioni, Connettori, Aggiungi connettore personalizzato, usando l’indirizzo mostrato sotto la sessione.

## Dove viene eseguito Codex

Su una Machine ospitata, seleziona questa opzione nella pagina di configurazione, sotto **Aggiungi altro quando vuoi**, **Codex**:

- **Sulla tua Machine** (opzione predefinita): premi **Collega Codex** e inserisci il codice mostrato da OpenAI. Usa lo stesso piano ChatGPT del tuo modello e i lavori vengono eseguiti sulla tua Machine. Non serve un terminale. Se hai effettuato l’accesso allo stesso account ChatGPT, la tua Machine può anche vedere e usare i ripristini del limite di utilizzo.
- **Altri modi**, **Sul mio computer**: il lavoro viene eseguito sul tuo computer, con Codex già collegato. La connessione è crittografata e vale solo per quel computer. Installa The Machine sul computer, associala dalla pagina Account, esegui `codex login` e lascia The Machine in esecuzione. Il risultato torna nell’attività. Se il computer è spento, i lavori restano in attesa.
- **Altri modi**, **Codex cloud**: il lavoro viene eseguito nel cloud di OpenAI. Premi **Collega Codex**. Usa lo stesso piano ChatGPT del tuo modello e OpenAI chiede un altro codice, per Codex. Poi inserisci l’ambiente Codex cloud nelle Impostazioni.

Oppure accedi dalla dashboard: **Connessioni**, **Progetti e codice**, **Codex**, **Ricevi un codice**. Una Machine self-hosted esegue autonomamente la stessa procedura di accesso.

Su una Machine ospitata, **Codex e Claude Code** compare nelle Impostazioni una volta collegato GitHub o Codex. Per gli sviluppatori: la [guida per gli agenti](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
