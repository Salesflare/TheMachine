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

Apri **Impostazioni**, **IA**. Ci sono due modi per entrare. Prima c’è **App ufficiale**: **Aggiungi in Claude** e un indirizzo per ogni Machine, `https://mcp.themachine.computer/mcp`, con **Copia**. Sotto c’è il tuo **Indirizzo privato (end-to-end)**, `https://<il tuo nome>.mcp.themachine.computer/mcp`.

Su una Machine sul tuo computer, premi prima **Ottieni il tuo indirizzo**. Si apre una pagina del tuo account: controlla che mostri lo stesso codice, conferma e scegli un nome. La tua Machine si abbina da sola, senza riavvio. Entrambi i modi ne hanno bisogno.

Poi ottiene il proprio certificato per l’indirizzo. Ci vogliono alcuni minuti e serve il pacchetto `cryptography` per Python.

Per Claude, premi **Aggiungi in Claude**, oppure apri [The Machine nella directory di Claude](https://claude.ai/directory/the-machine), e premi Connect. Su Team ed Enterprise, un owner lo aggiunge in Organization settings.

Per usare invece un indirizzo in Claude, apri Customize, Connectors, premi + Add e poi Add custom connector. Chiamalo The Machine, incolla l’indirizzo, premi Continue e poi Add.

In ChatGPT, apri chatgpt.com/plugins, premi + e poi Add custom MCP server. Chiamalo The Machine, incolla l’indirizzo e scegli OAuth. Conferma l’avviso e premi Create as a plugin. Il tuo piano o workspace deve consentire server MCP personalizzati.

Con l’app ufficiale, l’IA ti chiede di accedere con il tuo account The Machine. Scegli questa Machine se ne hai più di una, poi approva l’IA sulla pagina della tua Machine. Con l’indirizzo privato, l’IA arriva direttamente alla tua Machine.

Le IA su un dispositivo nella tua tailnet, come Claude Code o Cursor, possono usare anche l’indirizzo della tua dashboard seguito da `/mcp`. **Scollega** toglie dal tuo account una Machine sul tuo computer.

La tua Machine mostra quale IA è. Un’IA che non riconosce mostra l’indirizzo da cui arriva: collega solo se l’hai appena avviato tu.

Scegli cosa può fare, **Leggi** o **Lettura e modifica**. Con account di lavoro e personali, scegli anche cosa può vedere. Poi scegli per quanto: **1 giorno**, **7 giorni**, **30 giorni** o **1 anno**. Premi **Collegati**, o **Annulla** per rimandarla indietro senza nulla.

## App ufficiale o indirizzo privato

L’app ufficiale è la via facile: un indirizzo per tutti, e il tuo account trova la tua Machine. Il cloud instrada le sue richieste lungo il percorso ma non conserva nulla.

Con il tuo indirizzo privato, tutto è cifrato fino alla tua Machine. Il cloud lo passa soltanto e non può leggerlo.

In ogni caso decide la tua Machine. Entra solo un’IA che hai approvato sulla sua pagina, con l’accesso che hai scelto. In **Impostazioni**, **IA**, un’IA arrivata tramite l’app ufficiale mostra **App ufficiale**.

## Cosa vede

Un collegamento vede solo la sua area. Lavoro copre attività e promesse dei tuoi account di lavoro, contatti di lavoro, aziende, progetti e il briefing del team della tua Work Fleet. Personale copre il resto. Il testo dei messaggi resta sulla tua Machine, a meno che tu non attivi **Messaggi**: senza, un’IA vede le fonti di un’attività solo per mittente, oggetto e data.

I dati Team Graph dei tuoi colleghi non vanno mai a un’IA esterna.

## Messaggi

**Messaggi** permette a un’IA di cercare e leggere la tua email, Slack, WhatsApp e altre chat. È disattivato finché non lo attivi, nella pagina dove la colleghi o dopo in **Impostazioni**, **IA**. Legge soltanto: non invia, non elimina e non segna mai nulla.

Legge solo i messaggi della sua area. Alcuni non escono mai: codici monouso e link di accesso, messaggi di una bacheca o di un progetto **Solo tu**, conversazioni che The Machine ha giudicato delicate (trattative, HR, legale, salute, soldi), conversazioni che hai tenuto private e messaggi eliminati.

Ogni lettura compare nei suoi **Movimenti**, con quanti messaggi e quali conversazioni, mai il testo. La tua Machine passa il testo segnato come dati, così l’IA non segue istruzioni scritte in un messaggio.

Finché Messaggi è attivo, le modifiche al Graph di un’IA con **Lettura e modifica** aspettano il tuo ok. Tocca **Applica** o **Ignora** sulla modifica in **Movimenti**.

## In Impostazioni

Apri **Impostazioni**, **IA** per vedere ogni IA collegata, con l’ultimo uso e quante chiamate ha fatto. Cambia lì il suo accesso, la sua area o la durata. La chiamata successiva lo usa già. **Disattiva ora** chiude tutti i suoi accessi in una volta. **Movimenti** elenca ogni chiamata, anche quelle rifiutate. **Rimuovi** la toglie.

Un’IA che non sa accedere da sola può usare una chiave. In **Aggiungi una chiave**, dalle un nome, scegli accesso e durata e premi **Crea chiave**. Copia subito la chiave: si vede una volta sola. L’IA la invia come `Authorization: Bearer <key>`.

## Sicurezza

Ogni chiamata viene registrata, anche quelle rifiutate. Un collegamento scaduto o disattivato viene rifiutato finché non lo cambi. L’accesso usa OAuth con PKCE. La tua Machine conserva solo un’impronta di ogni token, quindi una copia dei suoi dati non apre nulla.
