---
title: Collegare altre IA
area: connections
summary: Fai leggere a Claude, ChatGPT, Cursor, Codex o GBrain le tue attività e il tuo Graph via MCP, ognuna con accesso e scadenza propri.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Cosa può fare un’altra IA

Altre IA possono collegarsi alla tua Machine via MCP: Claude, ChatGPT, Cursor, Codex, GBrain e altre. Possono leggere le tue attività, promesse, briefing del team e le persone e aziende nel tuo Graph.

Al massimo aggiungono un’attività, o un’attività con una bozza di email. Una bozza aspetta nella tua Machine finché non la leggi e premi tu **Invia**. Un’IA collegata non invia mai nulla e non agisce mai al posto tuo. Do it e gli agenti della tua Machine non ne fanno parte.

## Collegarne una

Nell’altra IA, aggiungi un connettore personalizzato o un server MCP con l’indirizzo della tua Machine seguito da `/mcp`. Su una Machine ospitata è `https://<tuo nome>.app.themachine.computer/mcp`. Su una Machine sul tuo computer è l’indirizzo della tua dashboard, che raggiungono solo i dispositivi nella tua tailnet.

L’IA ti manda alla tua Machine per accedere. La tua Machine mostra quale IA è. Un’IA che non riconosce mostra l’indirizzo da cui arriva: collega solo se l’hai appena avviato tu.

Scegli cosa può fare, **Leggi** o **Lettura e bozze**. Con account di lavoro e personali, scegli anche cosa può vedere. Poi scegli per quanto: **1 giorno**, **7 giorni**, **30 giorni** o **1 anno**. Premi **Collegati**, o **Annulla** per rimandarla indietro senza nulla.

## Cosa vede

Un collegamento vede solo la sua area. Lavoro copre attività e promesse dei tuoi account di lavoro, contatti di lavoro, aziende, progetti e il briefing del team della tua Work Fleet. Personale copre il resto. Il testo dei messaggi resta sulla tua Machine: un’IA vede le fonti di un’attività solo per mittente, oggetto e data.

I dati Team Graph dei tuoi colleghi non vanno mai a un’IA esterna.

## In Impostazioni

Apri **Impostazioni**, **IA** per vedere ogni IA collegata, con l’ultimo uso e quante chiamate ha fatto. Cambia lì il suo accesso, la sua area o la durata. La chiamata successiva lo usa già. **Disattiva ora** chiude tutti i suoi accessi in una volta. **Movimenti** elenca ogni chiamata, anche quelle rifiutate. **Rimuovi** la toglie.

Un’IA che non sa accedere da sola può usare una chiave. In **Aggiungi una chiave**, dalle un nome, scegli accesso e durata e premi **Crea chiave**. Copia subito la chiave: si vede una volta sola. L’IA la invia come `Authorization: Bearer <key>`.

## Sicurezza

Ogni chiamata viene registrata, anche quelle rifiutate. Un collegamento scaduto o disattivato viene rifiutato finché non lo cambi. L’accesso usa OAuth con PKCE. La tua Machine conserva solo un’impronta di ogni token, quindi una copia dei suoi dati non apre nulla.
