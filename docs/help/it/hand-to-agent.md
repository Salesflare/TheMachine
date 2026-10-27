---
title: Passa a Claude Code o Codex
area: cards
summary: Invia un'attività di programmazione a Claude Code o Codex. Il risultato torna sull'attività.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time
order: 5
---
## Passa un'attività

1. Sull'attività, apri **Altro** e scegli **Passa a Codex** o **Passa a Claude Code**. Compare quando quello strumento è configurato.
2. Controlla il riepilogo e cosa riceve, aggiungi una nota se vuoi e premi **Passa**. **Vedi il lavoro completo** mostra tutte le istruzioni.

L'attività mostra poi che ci sta lavorando, e il risultato quando ha finito, con **Mostra modifiche**. **Cambia** gli chiede delle modifiche; **Passalo di nuovo** ricomincia da capo.

Un lavoro non invia mai nulla per te.

## Configuralo

In **Impostazioni**, **Generale**, sotto **Agenti di programmazione**:

- **Sessione Claude Code**: l'indirizzo di una sessione Claude Code.
- **Ambiente cloud Codex**: l'id del suo ambiente, per il cloud di Codex.
- **Gira su**, e facoltativamente un **Branch**.

Claude invia il risultato tramite il connettore di The Machine. Aggiungilo una volta in claude.ai, Settings, Connectors, Add custom connector, con l'indirizzo che vedi lì.

## Dove gira Codex

Su una Machine in hosting, sceglilo nella tua pagina di configurazione, sotto **Aggiungi altro quando vuoi**, **Codex**:

- **Sul mio computer** (l'impostazione predefinita): il lavoro gira sul tuo computer, con il Codex collegato lì. Niente di Codex è sul tuo server, e il lavoro è cifrato solo per quel computer: il Network lo inoltra ma non può leggerlo. Installa The Machine su quel computer, abbinalo nella pagina Account ed esegui `codex login` lì. Tieni The Machine in esecuzione su quel computer. Il lavoro compare come thread nell'app Codex su quel computer, e il risultato torna sull'attività. Quando il computer è spento, i lavori aspettano che torni.
- **Cloud di Codex**: il lavoro gira nel cloud di OpenAI. Premi **Collega Codex**. Usa lo stesso piano ChatGPT del tuo modello, e OpenAI chiede un altro codice, per Codex. Poi inserisci l'ambiente cloud Codex in Impostazioni.

Su una Machine in hosting, Agenti di programmazione compare quando GitHub o Codex è collegato. Compare anche sulle configurazioni che eseguono i lavori altrove. Altro nella [guida agli agenti](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
