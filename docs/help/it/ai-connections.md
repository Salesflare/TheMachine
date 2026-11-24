---
title: Collegare altre IA
area: connections
summary: Consenti a Claude, ChatGPT, Cursor, Codex o GBrain di leggere le tue attività e il tuo Graph. Con Lettura e modifica, possono anche apportare modifiche che puoi annullare.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: cf0776c294917228
---
## Cosa può fare un’altra IA

Claude, ChatGPT, Cursor, Codex, GBrain e altre IA possono collegarsi alla tua Machine. Possono leggere le tue attività, le promesse, i brief del team e le persone e le aziende nel tuo Graph.

Con **Lettura e modifica** possono anche aggiungere un’attività o una bozza di email e aggiornare il tuo Graph: salvare un fatto, correggere dettagli, campi e tag o aggiungere una riga al riepilogo di una persona.

Ogni modifica compare in **Movimenti**, con **Annulla**. Non uniscono, eliminano né condividono mai i record. Quello che salvano è contrassegnato con **IA:** e il loro nome. La tua Machine lo considera una loro affermazione, mai una tua istruzione.

Una bozza resta in attesa finché non la leggi e premi Invia. Un’IA collegata non invia mai nulla e non agisce mai per te.

Se a una bozza manca qualcosa da compilare, se cita un file che non è disponibile o se ha come destinatario solo il tuo indirizzo, viene rimandata all’IA perché la corregga. Se un’IA richiede due volte di seguito la stessa attività o bozza, ne ricevi una sola.

## Collegarne una

Apri **Impostazioni**, **App**. Sotto **Le app di The Machine** trovi **Aggiungi in ChatGPT** e **Aggiungi in Claude**. Sotto **Oppure aggiungila con un indirizzo** trovi l’indirizzo ufficiale dell’app, uguale per tutte le Machine, `https://mcp.themachine.computer/mcp`, e **Il tuo indirizzo**, `https://<your name>.mcp.themachine.computer/mcp`, entrambi con **Copia**.

Se usi una Machine sul tuo computer, prima premi **Configura** sotto **Richiedi il tuo indirizzo**. Si apre una pagina del tuo account: controlla che mostri lo stesso codice, conferma e scegli un nome. La tua Machine si abbina da sola, senza riavviarsi. Serve in entrambi i casi.

La tua Machine configura poi da sola il suo indirizzo sicuro. Ci vogliono alcuni minuti.

Per Claude, premi **Aggiungi in Claude** oppure apri [The Machine nella directory di Claude](https://claude.ai/directory/the-machine), poi premi Connect. Con Team ed Enterprise, è il proprietario ad aggiungerla nelle impostazioni dell’organizzazione.

Per usare un indirizzo in Claude, invece, apri Customize, Connectors, premi + Add, poi Add custom connector. Chiamalo The Machine, incolla l’indirizzo, premi Continue e poi Add.

Per ChatGPT, premi **Aggiungi in ChatGPT** oppure apri [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), poi premi Install plugin. Con Business ed Enterprise, potrebbe essere necessario che un amministratore lo consenta prima.

L’app ufficiale raggiunge una Machine ospitata e anche una Machine sul tuo computer, una volta che ha il suo indirizzo.

Per usare il tuo indirizzo privato o una Machine che non è sulla Network, aggiungi invece un server MCP personalizzato in ChatGPT: apri chatgpt.com/plugins, premi +, poi Add custom MCP server. Chiamalo The Machine, incolla l’indirizzo e scegli OAuth. Conferma l’avviso e premi Create as a plugin. Il tuo piano o spazio di lavoro deve consentire l’uso di server MCP personalizzati.

Con l’app ufficiale, l’IA ti chiede di accedere con il tuo account The Machine. Se hai più di una Machine, scegli questa e approva dalla pagina della tua Machine. Con l’indirizzo privato, l’IA si collega direttamente alla tua Machine.

Anche le IA su un dispositivo nella tua rete privata (Tailscale), come Claude Code o Cursor, possono usare l’indirizzo della dashboard seguito da `/mcp`. **Scollega questa Machine**, in fondo a **Impostazioni**, **Account**, rimuove di nuovo dal tuo account una Machine sul tuo computer.

La tua Machine mostra quale IA sta inviando la richiesta. Se non riesce a identificarla, mostra da dove proviene la richiesta: collegala solo se l’hai appena avviata tu.

Scegli cosa può fare, **Leggi** o **Lettura e modifica**. Se hai account Work e Personal, scegli cosa può vedere. Poi scegli per quanto tempo: **1 giorno**, **7 giorni**, **30 giorni** o **1 anno**. Premi **Collega** oppure **Annulla** per rifiutare la richiesta senza concedere l’accesso.

## App ufficiale o indirizzo privato

L’app ufficiale è la soluzione più semplice: un unico indirizzo per tutti e il tuo account trova la tua Machine. Il nostro cloud inoltra le richieste e non ne salva mai il contenuto.

Con il tuo indirizzo privato, tutto è crittografato fino alla tua Machine. Il cloud si limita a inoltrare i dati e non può leggerli.

In entrambi i casi, decide la tua Machine. Può accedere solo un’IA che hai autorizzato dalla sua pagina, con i permessi che hai scelto. In **Impostazioni**, **App**, un’IA collegata tramite l’app ufficiale mostra **App ufficiale**.

## Cosa può vedere

Una connessione vede solo la propria area. Work include le attività e le promesse dei tuoi account di lavoro, le persone, le aziende e i progetti di lavoro, oltre al brief del team della tua Fleet di lavoro. Personal include tutto il resto. Il testo dei messaggi resta sulla tua Machine, a meno che tu non attivi **Messaggi**. Senza questa opzione, un’IA vede solo mittente, oggetto e data delle fonti di un’attività.

I record del Graph del team dei tuoi colleghi non vengono mai inviati a un’IA esterna.

## Messaggi

**Messaggi** consente a un’IA di cercare e leggere le tue email, i messaggi di Slack e WhatsApp e le tue altre chat. È disattivato finché non lo attivi, nella pagina in cui colleghi l’IA o in seguito in **Impostazioni**, **App**. L’IA può solo leggere: non invia, elimina né contrassegna mai nulla.

Può leggere solo i messaggi della propria area. Alcuni messaggi non vengono mai inviati: codici monouso e link di accesso, messaggi di una bacheca o di un progetto **Solo tu**, conversazioni che The Machine ha ritenuto sensibili (affari, risorse umane, aspetti legali, salute, denaro), conversazioni che hai mantenuto private e messaggi eliminati.

Ogni lettura compare in **Movimenti**, con il numero di messaggi e le conversazioni consultate, mai il testo. La tua Machine passa il testo contrassegnato come dato, quindi l’IA non dovrebbe seguire le istruzioni contenute in un messaggio.

Quando Messaggi è attivo, le modifiche al Graph apportate da un’IA con **Lettura e modifica** restano in attesa della tua conferma. Premi **Applica** o **Scarta** sulla modifica in **Movimenti**.

## Nelle impostazioni

Apri **Impostazioni**, **App** per vedere ogni IA che si è collegata, con i relativi permessi, area, data di scadenza e ultimo utilizzo. Puoi attivare o disattivare **Messaggi** direttamente da qui. Premi **Cambia** per modificare i permessi, l’area o la durata. Le modifiche si applicano alla chiamata successiva. **Movimenti** mostra tutte le chiamate, comprese quelle rifiutate. **Disattiva ora** mette in pausa l’accesso: tutte le sessioni terminano, ma la cronologia resta. **Rimuovi** elimina l’IA e la relativa cronologia.

Quando accedi di nuovo alla stessa IA, la nuova autorizzazione sostituisce quella precedente.

Un’IA che non può accedere da sola può usare una chiave. In **Aggiungi una chiave**, assegnale un nome, scegli i permessi e la durata, poi premi **Crea chiave**. Copia subito la chiave: viene mostrata una sola volta. L’IA la invia come `Authorization: Bearer <key>`.

## Proteggi il tuo account

Ogni chiamata viene registrata, comprese quelle rifiutate. Una connessione scaduta o disattivata viene rifiutata finché non la modifichi. La tua Machine conserva solo un’impronta di ogni accesso, quindi una copia dei suoi dati non permette di accedere.
