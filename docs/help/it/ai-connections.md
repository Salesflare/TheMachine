---
title: Collega altre IA
area: connections
summary: Permetti a Claude, ChatGPT, Cursor, Codex o GBrain di leggere le tue attività e il tuo Graph. Con Lettura e modifica possono anche apportare modifiche che puoi annullare.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: a8637260c99df309
---
## Cosa può fare un’altra IA

Claude, ChatGPT, Cursor, Codex, GBrain e altre IA possono collegarsi alla tua Machine. Possono leggere le tue attività, le promesse, i brief del team e le persone e le aziende del tuo Graph.

Con **Lettura e modifica** possono anche aggiungere un’attività o una bozza di email e aggiornare il tuo Graph: salvare un’informazione, correggere dettagli, campi e tag oppure aggiungere una riga al riepilogo di una persona.

Ogni modifica compare in **Movimenti** con **Annulla**. Non uniscono, eliminano né condividono mai i record. Quello che salvano è contrassegnato con **IA:** e il loro nome, e la tua Machine lo considera una loro affermazione, mai un’istruzione da parte tua.

Una bozza resta in attesa finché non la leggi e premi Invia. Un’IA collegata non invia mai nulla e non agisce mai per conto tuo.

## Collegane una

Apri **Impostazioni**, **App**. Sotto **Le app di The Machine** trovi **Aggiungi in ChatGPT** e **Aggiungi in Claude**. Sotto **Oppure aggiungila con un indirizzo** trovi l’indirizzo ufficiale dell’app, valido per ogni Machine, `https://mcp.themachine.computer/mcp`, e **Il tuo indirizzo**, `https://<your name>.mcp.themachine.computer/mcp`, entrambi con **Copia**.

Su una Machine installata sul tuo computer, prima premi **Configura** sotto **Richiedi il tuo indirizzo**. Si apre una pagina del tuo account: controlla che mostri lo stesso codice, conferma e scegli un nome. La tua Machine si abbina da sola, senza riavvio. Serve in entrambi i casi.

Poi la tua Machine configura da sola il suo indirizzo sicuro. Ci vogliono alcuni minuti.

Per Claude, premi **Aggiungi in Claude** oppure apri [The Machine nella directory di Claude](https://claude.ai/directory/the-machine), poi premi **Collega**. Nei piani Team ed Enterprise, chi amministra l’organizzazione deve aggiungerla nelle impostazioni dell’organizzazione.

Per usare un indirizzo in Claude, invece, apri Customize, Connectors, premi + Add e poi Add custom connector. Chiamalo The Machine, incolla l’indirizzo, premi Continue e poi Add.

Per ChatGPT, premi **Aggiungi in ChatGPT** oppure apri [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), poi premi **Installa plugin**. Nei piani Business ed Enterprise, un amministratore potrebbe doverlo autorizzare prima.

L’app ufficiale raggiunge una Machine ospitata e, una volta configurato il suo indirizzo, anche una Machine installata sul tuo computer.

Per il tuo indirizzo privato, o per una Machine non collegata al Network, aggiungi invece un server MCP personalizzato in ChatGPT: apri chatgpt.com/plugins, premi + e poi Add custom MCP server. Chiamalo The Machine, incolla l’indirizzo e scegli OAuth. Conferma l’avviso e premi Create as a plugin. Il tuo piano o spazio di lavoro deve consentire l’uso di server MCP personalizzati.

Con l’app ufficiale, l’IA ti chiede di accedere con il tuo account di The Machine. Se hai più di una Machine, scegli questa e approva dalla pagina della tua Machine. Con l’indirizzo privato, l’IA raggiunge direttamente la tua Machine.

Anche le IA su un dispositivo della tua rete privata (Tailscale), come Claude Code o Cursor, possono usare l’indirizzo della tua dashboard seguito da `/mcp`. **Scollega questa Machine**, in fondo a **Impostazioni**, **Account**, scollega di nuovo dal tuo account una Machine installata sul tuo computer.

La tua Machine mostra quale IA sta effettuando la richiesta. Se non riesce a identificarla, mostra da dove proviene la richiesta: collegala solo se hai appena avviato tu la procedura.

Scegli cosa può fare: **Leggi** o **Lettura e modifica**. Se hai un account Work e uno Personal, scegli cosa può vedere. Poi scegli per quanto tempo: **1 giorno**, **7 giorni**, **30 giorni** o **1 anno**. Premi **Collega** oppure **Annulla** per interrompere la procedura senza collegarla.

## App ufficiale o indirizzo privato

L’app ufficiale è il modo più semplice: un solo indirizzo per tutti e il tuo account trova la tua Machine. Il nostro cloud inoltra le richieste e non salva mai ciò che contengono.

Con il tuo indirizzo privato, tutto è crittografato fino alla tua Machine. Il cloud si limita a inoltrare le richieste e non può leggerle.

In entrambi i casi, decide la tua Machine. Può accedere solo un’IA che hai approvato dalla sua pagina, con il livello di accesso che hai scelto. In **Impostazioni**, **App**, un’IA collegata tramite l’app ufficiale è indicata come **App ufficiale**.

## Cosa può vedere

Una connessione vede solo la propria area. L’area Work include le attività e le promesse dei tuoi account di lavoro, le persone, le aziende e i progetti di lavoro, oltre al brief del team della tua Fleet di lavoro. L’area Personal include tutto il resto. I messaggi restano sulla tua Machine, a meno che tu non attivi **Messaggi**: in caso contrario, un’IA vede solo il mittente, l’oggetto e la data delle fonti di un’attività.

I record del Graph del team dei tuoi colleghi non vengono mai inviati a un’IA esterna.

## Messaggi

**Messaggi** permette a un’IA di cercare e leggere le tue email, i messaggi di Slack, WhatsApp e altre chat. È disattivata finché non la attivi, dalla pagina in cui colleghi l’IA oppure in seguito da **Impostazioni**, **App**. L’IA può solo leggere: non invia, elimina né contrassegna nulla.

Legge solo i messaggi della propria area. Alcuni non vengono mai inviati: codici monouso e link di accesso, messaggi di una bacheca o di un progetto **Solo tu**, conversazioni che The Machine ha giudicato sensibili (accordi, risorse umane, questioni legali, salute, denaro), conversazioni che hai mantenuto private e messaggi eliminati.

Ogni lettura compare nei **Movimenti** dell’IA con il numero di messaggi e le conversazioni coinvolte, mai con il testo. La tua Machine passa il testo contrassegnandolo come dato, così l’IA non dovrebbe seguire le istruzioni contenute in un messaggio.

Quando Messaggi è attivata, le modifiche al Graph apportate da un’IA con **Lettura e modifica** restano in attesa della tua conferma. Premi **Applica** o **Scarta** sulla modifica in **Movimenti**.

## Nelle impostazioni

Apri **Impostazioni**, **App** per vedere tutte le IA che si sono collegate, ognuna una sola volta, con il relativo accesso, l’area, la data di scadenza e l’ultimo utilizzo. Puoi attivare e disattivare **Messaggi** dalla stessa pagina. Premi **Cambia** per modificare l’accesso, l’area o la durata. Le modifiche valgono dalla richiesta successiva. **Movimenti** elenca tutte le richieste, comprese quelle rifiutate. **Disattiva ora** sospende l’accesso: tutte le sessioni terminano, ma la cronologia resta. **Rimuovi** elimina l’IA e la relativa cronologia.

Quando accedi di nuovo alla stessa IA, la nuova autorizzazione sostituisce quella precedente.

Un’IA che non può accedere da sola può usare una chiave. In **Aggiungi una chiave**, assegnale un nome, scegli l’accesso e la durata, poi premi **Crea chiave**. Copia subito la chiave: viene mostrata una sola volta. L’IA la invia come `Authorization: Bearer <key>`.

## Proteggi il tuo account

Ogni richiesta viene registrata, comprese quelle rifiutate. Le richieste da una connessione scaduta o disattivata vengono rifiutate finché non la modifichi. La tua Machine conserva solo un’impronta di ogni accesso, quindi una copia dei suoi dati non permette di accedere.
