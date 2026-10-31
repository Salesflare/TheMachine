---
title: Collegare altre IA
area: connections
summary: Fai leggere a Claude, ChatGPT, Cursor, Codex o GBrain le tue attività e il tuo Graph via MCP, ognuna con accesso e scadenza propri.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Cosa può fare un’altra IA

Altre IA possono collegarsi alla tua Machine via MCP: Claude, ChatGPT, Cursor, Codex, GBrain e altre. Possono leggere le tue attività, promesse, briefing del team e le persone e aziende nel tuo Graph.

Con **Lettura e modifica** possono anche aggiungere un’attività, o un’attività con una bozza di email, e modificare il tuo Graph: salvare un fatto su una persona o un’azienda, correggerne dettagli, campi e tag, o aggiungere una riga al riepilogo di una persona.

Ogni modifica compare in **Attività** con **Annulla**. Non uniscono, eliminano né condividono mai schede. Ciò che salvano mostra **IA:** e il loro nome, nella loro area. Puoi modificarlo o toglierlo, e The Machine può riscrivere una riga del riepilogo più avanti. La tua Machine lo tratta come una loro affermazione, mai come una tua istruzione.

Una bozza aspetta nella tua Machine finché non la leggi e premi tu **Invia**. Un’IA collegata non invia mai nulla e non agisce mai al posto tuo. Do it e gli agenti della tua Machine non ne fanno parte.

## Collegarne una

Apri **Impostazioni**, **IA**. In alto c’è l’indirizzo della tua Machine per le IA, `https://<il tuo nome>.mcp.themachine.computer/mcp`, con **Copia**. Su una Machine sul tuo computer, premi prima **Ottieni il tuo indirizzo**. Si apre una pagina del tuo account: controlla che mostri lo stesso codice, conferma e scegli un nome. La tua Machine si abbina da sola, senza riavvio.

Poi ottiene il proprio certificato per l’indirizzo. Ci vogliono alcuni minuti e serve il pacchetto `cryptography` per Python.

In ChatGPT, apri chatgpt.com/plugins, premi + e poi Add custom MCP server. Chiamalo The Machine, incolla l’indirizzo e scegli OAuth. Conferma l’avviso e premi Create as a plugin. Il tuo piano o workspace deve consentire server MCP personalizzati.

In Claude, apri Customize, Connectors, premi + Add e poi Add custom connector. Chiamalo The Machine, incolla l’indirizzo, premi Continue e poi Add. Su Team ed Enterprise, un owner lo aggiunge in Organization settings.

Le IA su un dispositivo nella tua tailnet, come Claude Code o Cursor, possono usare anche l’indirizzo della tua dashboard seguito da `/mcp`. **Scollega** toglie dal tuo account una Machine sul tuo computer.

L’IA ti manda alla tua Machine per accedere. La tua Machine mostra quale IA è. Un’IA che non riconosce mostra l’indirizzo da cui arriva: collega solo se l’hai appena avviato tu.

Scegli cosa può fare, **Leggi** o **Lettura e modifica**. Con account di lavoro e personali, scegli anche cosa può vedere. Poi scegli per quanto: **1 giorno**, **7 giorni**, **30 giorni** o **1 anno**. Premi **Collegati**, o **Annulla** per rimandarla indietro senza nulla.

## Cosa vede

Un collegamento vede solo la sua area. Lavoro copre attività e promesse dei tuoi account di lavoro, contatti di lavoro, aziende, progetti e il briefing del team della tua Work Fleet. Personale copre il resto. Il testo dei messaggi resta sulla tua Machine: un’IA vede le fonti di un’attività solo per mittente, oggetto e data.

I dati Team Graph dei tuoi colleghi non vanno mai a un’IA esterna.

## In Impostazioni

Apri **Impostazioni**, **IA** per vedere ogni IA collegata, con l’ultimo uso e quante chiamate ha fatto. Cambia lì il suo accesso, la sua area o la durata. La chiamata successiva lo usa già. **Disattiva ora** chiude tutti i suoi accessi in una volta. **Movimenti** elenca ogni chiamata, anche quelle rifiutate. **Rimuovi** la toglie.

Un’IA che non sa accedere da sola può usare una chiave. In **Aggiungi una chiave**, dalle un nome, scegli accesso e durata e premi **Crea chiave**. Copia subito la chiave: si vede una volta sola. L’IA la invia come `Authorization: Bearer <key>`.

## Sicurezza

Ogni chiamata viene registrata, anche quelle rifiutate. Un collegamento scaduto o disattivato viene rifiutato finché non lo cambi. L’accesso usa OAuth con PKCE. La tua Machine conserva solo un’impronta di ogni token, quindi una copia dei suoi dati non apre nulla.
