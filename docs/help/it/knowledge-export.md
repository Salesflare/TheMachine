---
title: Conoscenze per un’altra IA
area: settings
summary: Porta ciò che la tua Machine ha imparato a qualsiasi altra IA, in semplici file Markdown, JSONL e CSV.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
Tutto ciò che la tua Machine impara è tuo. Portalo a un’altra IA, o tienilo, anche se smetti di usare The Machine.

## Esportare

1. In **Impostazioni** › **Generale**, premi **Esporta** accanto a **Conoscenze per un’altra IA**.
2. Lascia **Testo dei messaggi** disattivato per esportare solo da dove viene ogni cosa, e quando. Attivalo per aggiungere il testo.
3. **Privato e Prudente** resta disattivato, a meno che tu non voglia anche i progetti solo per te, le conversazioni private e le Fleet in modalità Prudente.
4. Se vuoi, imposta una **Passphrase** di almeno 10 caratteri per cifrare il file.
5. Premi **Scarica**. Il file viene creato sulla tua Machine e si può scaricare una volta.

Su una Machine in hosting funziona allo stesso modo, dalle Impostazioni della tua Machine. Sul tuo computer, `assistant export-knowledge` crea lo stesso file.

## Cosa contiene

- Persone, organizzazioni e progetti: una pagina Markdown ciascuno, con i loro legami.
- Fatti e preferenze: ciò che la tua Machine sa, su di te e su di loro.
- Fatti passati: ciò che non vale più (finito, messo da parte o sostituito), con ciò che lo ha sostituito. I fatti che hai rimosso restano fuori.
- Regole, come scrivi e firme: ciò che seguono le tue bozze.
- Skill: le tue guide, attive e no.
- Contesto: brief del team, righe di riepilogo, promesse e attività aperte.
- Fonti: da dove viene ogni cosa, con id e data.

I record sono JSONL, contatti e attività anche CSV. Un README.md in cima spiega la struttura e dice a un’IA come usarlo. Dai la cartella, o lo zip, all’IA come file di conoscenza o progetto.

## Cosa resta fuori

Password, chiavi e accessi non entrano mai. Ciò che sembra una chiave viene sostituito. Anche i dati dei colleghi e di altre Machine, le impostazioni e le foto restano fuori. Per una copia completa con cui spostare la tua Machine, vedi [Passa al tuo computer](moving.md).

Il formato è aperto e con versioni: vedi [lo schema](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
