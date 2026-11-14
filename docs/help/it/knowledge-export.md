---
title: Conoscenze per un’altra IA
area: settings
summary: Porta ciò che la tua Machine ha imparato su qualsiasi altra IA, in file semplici che ogni IA può leggere.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: 6a917f8ee2aabaa9
---
Tutto ciò che la tua Machine impara è tuo. Puoi condividerlo con un’altra IA, come ChatGPT o Claude, oppure conservarlo.

## Esporta

1. In **Impostazioni** › **Generale** › **Esporta**, premi **Esporta** accanto a **Conoscenze per un’altra IA**.
2. **Testo dei messaggi** è disattivato per impostazione predefinita: vengono incluse solo la provenienza di ogni elemento e la data. Attivalo per includere anche il testo.
3. Attiva **Privato e Prudente** solo per includere i progetti solo per te, le chat private e le Fleet prudenti.
4. Se vuoi, imposta una **Passphrase** (di almeno 10 caratteri) per crittografare il file.
5. Premi **Scarica**. Il file può essere scaricato una sola volta.

Funziona allo stesso modo con una Machine ospitata e sul tuo computer.

## Cosa include

- Persone, organizzazioni e progetti: una pagina Markdown per ciascuno, con le relazioni tra loro.
- Fatti e preferenze: ciò che la tua Machine sa di te e di loro.
- Fatti passati: ciò che non è più valido (terminato, accantonato o sostituito) e cosa lo ha sostituito. I fatti che hai rimosso non vengono inclusi.
- Regole, stile di scrittura e firme: ciò che seguono le tue bozze.
- Skill: le tue guide pratiche, attivate o disattivate.
- Contesto: briefing del team, righe di riepilogo, promesse e attività aperte.
- Fonti: la provenienza di ogni elemento, con ID e data.

I contatti e le attività sono inclusi anche in fogli di calcolo (CSV). All’inizio trovi un README che spiega all’IA come leggere tutti i file. Carica lo zip nell’IA come file di conoscenze o progetto.

## Cosa non include

Le password, le chiavi e i dati di accesso non vengono mai inclusi. Sono esclusi anche i dati, le impostazioni e le foto dei compagni di team. Per trasferire tutta la tua Machine, consulta [Passare a un altro computer](moving.md).

Per gli sviluppatori: [il formato dei file](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
