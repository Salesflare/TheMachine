---
title: Collega altre IA
area: connections
summary: Consenti a Claude, ChatGPT, Cursor, Codex o GBrain di leggere le tue attività e il tuo Graph. Con Lettura e modifica possono anche apportare modifiche, che puoi annullare.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: acdce4a5793f7c67
---
## Cosa può fare un'altra IA

Claude, ChatGPT, Cursor, Codex, GBrain e altre IA possono collegarsi alla tua Machine. Possono leggere le tue attività, le promesse, i briefing del team e le persone e le aziende nel tuo Graph.

Con **Lettura e modifica** possono anche aggiungere un'attività o una bozza di email e aggiornare il tuo Graph: salvare un'informazione, correggere dettagli, campi e tag oppure aggiungere una riga al riepilogo di una persona.

Ogni modifica compare in **Movimenti** con **Annulla**. Non uniscono, eliminano né condividono mai i record. Ciò che salvano è contrassegnato con **IA:** e il loro nome. La tua Machine lo considera una loro affermazione, mai una tua istruzione.

Una bozza resta in attesa finché non la leggi e premi tu stesso Invia. Un'IA collegata non invia mai nulla e non agisce mai per tuo conto.

Una bozza con un campo ancora da compilare, un file menzionato ma non disponibile o solo il tuo indirizzo viene rimandata all'IA perché la corregga. Se un'IA chiede la stessa attività o bozza due volte di seguito, ne ricevi una sola.

## Collegane una

Apri **Impostazioni**, **App**. Sotto **Le app di The Machine** trovi **Aggiungi in ChatGPT** e **Aggiungi in Claude**. In **Oppure aggiungila con un indirizzo** trovi l'unico indirizzo dell'app ufficiale per tutte le Machine, `https://mcp.themachine.computer/mcp`, e **Il tuo indirizzo**, `https://<your name>.mcp.themachine.computer/mcp`, entrambi con **Copia**.

Su una Machine installata sul tuo computer, premi prima **Configura** sotto **Richiedi il tuo indirizzo**. Si apre una pagina del tuo account: controlla che mostri lo stesso codice, conferma e scegli un nome. La tua Machine si abbina da sola, senza riavviarsi. Serve per entrambe le modalità.

La tua Machine configura poi da sola il suo indirizzo sicuro. Ci vogliono alcuni minuti.

Per Claude, premi **Aggiungi in Claude** oppure apri [The Machine nella directory di Claude](https://claude.ai/directory/the-machine), poi premi Connect. Nei piani Team ed Enterprise, l'owner lo aggiunge da Organization settings.

Per usare invece un indirizzo in Claude, apri Customize, Connectors, premi + Add, poi Add custom connector. Chiamalo The Machine, incolla l'indirizzo, premi Continue e poi Add.

Per ChatGPT, premi **Aggiungi in ChatGPT** oppure apri [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), poi premi Install plugin. Nei piani Business ed Enterprise, potrebbe essere necessario che un admin lo autorizzi prima.

L'app ufficiale raggiunge una Machine ospitata e una Machine sul tuo computer, una volta che ha il suo indirizzo.

Per usare il tuo indirizzo privato o una Machine non collegata alla Network, aggiungi invece un server MCP personalizzato in ChatGPT: apri chatgpt.com/plugins, premi +, poi Add custom MCP server. Chiamalo The Machine, incolla l'indirizzo e seleziona OAuth. Conferma l'avviso e premi Create as a plugin. Il tuo piano o spazio di lavoro deve consentire l'uso di server MCP personalizzati.

Con l'app ufficiale, l'IA ti chiede di accedere con il tuo account The Machine. Se ne hai più di una, scegli questa Machine, poi autorizzala dalla sua pagina. Con l'indirizzo privato, l'IA raggiunge direttamente la tua Machine.

Le IA su un dispositivo nella tua rete privata (Tailscale), come Claude Code o Cursor, possono usare anche l'indirizzo della tua dashboard seguito da `/mcp`. **Scollega questa Machine**, in fondo a **Impostazioni**, **Account**, scollega dal tuo account una Machine installata sul tuo computer.

La tua Machine mostra quale IA sta effettuando la richiesta. Se non riesce a identificarla, mostra da dove proviene la richiesta: collegala solo se hai appena avviato tu la procedura.

Scegli cosa può fare: **Leggi** o **Lettura e modifica**. Se hai un account Work e uno Personal, scegli cosa può vedere. Poi scegli per quanto tempo: **1 giorno**, **7 giorni**, **30 giorni** o **1 anno**. Premi **Collega** oppure **Annulla** per interrompere la procedura senza collegarla.

## App ufficiale o indirizzo privato

L'app ufficiale è la soluzione più semplice: un unico indirizzo per tutti e il tuo account trova la tua Machine. Il nostro cloud inoltra le richieste e non ne conserva mai il contenuto.

Con il tuo indirizzo privato, tutto è crittografato fino alla tua Machine. Il cloud si limita a inoltrare le richieste e non può leggerle.

In entrambi i casi decide la tua Machine. Può accedere solo un'IA che hai autorizzato dalla sua pagina, con i permessi che hai scelto. In **Impostazioni**, **App**, un'IA collegata tramite l'app ufficiale mostra **App ufficiale**.

## Cosa può vedere

Una connessione vede solo la propria area. Work include le attività e le promesse dei tuoi account di lavoro, le persone, le aziende e i progetti di lavoro, oltre al briefing del team della tua Fleet di lavoro. Personal include tutto il resto. Il testo dei messaggi resta sulla tua Machine, a meno che tu non attivi **Messaggi**: senza questa opzione, un'IA vede solo mittente, oggetto e data dei messaggi associati a un'attività.

I record del Team Graph dei tuoi colleghi non vengono mai condivisi con un'IA esterna.

## Messaggi

**Messaggi** permette a un'IA di cercare e leggere le tue email e le chat su Slack, WhatsApp e altri servizi. È disattivata finché non la attivi, dalla pagina in cui colleghi l'IA o più tardi in **Impostazioni**, **App**. L'IA può solo leggere: non invia, elimina o contrassegna mai nulla.

Può leggere solo i messaggi della propria area. Alcuni non vengono mai condivisi: codici monouso e link di accesso, messaggi di una bacheca o di un progetto **Solo tu**, conversazioni che The Machine ha identificato come sensibili (trattative, risorse umane, questioni legali, salute, denaro), conversazioni che hai mantenuto private e messaggi eliminati.

Ogni lettura compare nei **Movimenti** dell'IA, con il numero di messaggi e le conversazioni consultate, mai con il testo. La tua Machine passa il testo all'IA contrassegnandolo come dato, così l'IA non dovrebbe seguire le istruzioni contenute in un messaggio.

Quando Messaggi è attiva, le modifiche al Graph apportate da un'IA con **Lettura e modifica** restano in attesa della tua conferma. Premi **Applica** o **Scarta** sulla modifica in **Movimenti**.

## Nelle Impostazioni

Apri **Impostazioni**, **App** per vedere ogni IA che si è collegata, una sola volta, con i relativi permessi, area, data di scadenza e ultimo utilizzo. Puoi attivare o disattivare **Messaggi** da qui. Premi **Cambia** per modificare i permessi, l'area o la durata. Le modifiche si applicano alla richiesta successiva. **Movimenti** mostra tutte le richieste, anche quelle rifiutate. **Disattiva ora** sospende l'accesso e termina tutte le sessioni, ma conserva la cronologia. **Rimuovi** scollega l'IA e ne elimina la cronologia.

Quando accedi di nuovo alla stessa IA, la nuova autorizzazione sostituisce quella precedente. Se avevi già effettuato l'accesso a quell'IA, la connessione resta attiva con i nuovi permessi. Un'IA che usi resta collegata fino alla data di scadenza; se non la usi per 90 giorni, dovrai accedere di nuovo.

Un'IA che non può accedere da sola può usare una chiave. In **Aggiungi una chiave**, assegnale un nome, scegli i permessi e la durata, poi premi **Crea chiave**. Copia subito la chiave: verrà mostrata una sola volta. L'IA la invia come `Authorization: Bearer <key>`.

## Proteggi i tuoi dati

Ogni richiesta viene registrata, anche quelle rifiutate. Una connessione scaduta o disattivata viene rifiutata finché non la modifichi. La tua Machine conserva solo un'impronta digitale di ogni accesso, quindi una copia dei suoi dati non permette di accedere a nulla.
