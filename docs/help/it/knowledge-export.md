---
title: Conoscenze per un’altra IA
area: settings
summary: Porta ciò che la tua Machine ha imparato in qualsiasi altra IA, in semplici file leggibili da ogni IA.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: db1c7f4768a71630
---
Tutto ciò che impara la tua Machine appartiene a te. Condividilo con un’altra IA, come ChatGPT o Claude, oppure conservalo.

## Esportare

1. In **Impostazioni** › **Generale** › **Esporta**, premi **Esporta** accanto a **Conoscenze per un’altra IA**.
2. **Testo dei messaggi** è disattivato per impostazione predefinita: vengono incluse solo la provenienza e la data di ogni elemento. Attivalo per aggiungere anche il testo.
3. Attiva **Privato e Prudente** solo per includere i progetti riservati solo a te, le chat private e le Fleet prudenti.
4. Se vuoi, imposta una **Passphrase** (di almeno 10 caratteri) per cifrare il file.
5. Premi **Scarica**. Puoi scaricare il file una sola volta.

Funziona allo stesso modo con una Machine ospitata e sul tuo computer.

## Cosa contiene

- Persone, organizzazioni e progetti: una pagina Markdown per ciascuno, con le relative connessioni.
- Fatti e preferenze: ciò che la tua Machine sa su di te e su di loro.
- Fatti passati: ciò che non è più valido (perché terminato o sostituito) e da cosa è stato sostituito. I fatti che hai rimosso non vengono inclusi.
- Regole, il tuo modo di scrivere e firme: ciò a cui si attengono le tue bozze.
- Skill: le tue procedure, attive o disattivate.
- Contesto: brief del team, righe di riepilogo, promesse e attività in sospeso.
- Fonti: la provenienza di ogni elemento, con ID e data.

I contatti e le attività sono inclusi anche in fogli di calcolo (CSV). Un README in cima spiega all’IA come leggere tutti i file. Carica lo zip nell’IA come file di conoscenze o progetto.

## Cosa non è incluso

Password, chiavi e dati di accesso non vengono mai inclusi. Anche i dati, le impostazioni e le foto dei tuoi colleghi restano esclusi. Per trasferire tutta la tua Machine, consulta [Passare a un altro computer](moving.md).

Per gli sviluppatori: [il formato dei file](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
