---
title: Collega altre IA
area: connections
summary: Consenti a Claude, ChatGPT, Cursor, Codex o GBrain di leggere le tue attività e il tuo Graph. Con **Lettura e modifica** possono anche apportare modifiche che puoi annullare.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 3a7200b2a076c274
---
## Cosa può fare un’altra IA

Claude, ChatGPT, Cursor, Codex, GBrain e altre IA possono collegarsi alla tua Machine. Possono leggere le tue attività, le promesse, i brief del team e le persone e le aziende nel tuo Graph.

Con **Lettura e modifica** possono anche aggiungere un’attività o una bozza di email e aggiornare il tuo Graph: salvare un fatto, correggere dettagli, campi e tag oppure aggiungere una riga al riepilogo di una persona.

Ogni modifica compare in **Movimenti** con **Annulla**. Non uniscono, eliminano né condividono mai i record. Quello che salvano è contrassegnato con **IA:** e il loro nome, e la tua Machine lo considera un’affermazione di chi l’ha salvato, mai un’istruzione tua.

Una bozza resta in attesa finché non la leggi e premi tu Invia. Un’IA collegata non invia mai nulla e non agisce mai per te.

## Cosa impara da te

Quando inizia una chat, l’IA riceve un breve riepilogo: chi sei, le tue regole principali e cosa è cambiato dall’ultima volta. Può anche leggere quello che contiene **Apprendimento**: le tue regole, informazioni generali e il tuo modo di scrivere in ogni canale. Così scrive come faresti tu.

Con **Lettura e modifica**, può salvare ciò che definisci nella chat. Un fatto viene salvato subito, con **Annulla** in **Movimenti**. Una regola orienta il lavoro della tua Machine, quindi resta in **Apprendimento** finché non premi **Approva** o **Scarta**. Non cambia mai il tuo modo di scrivere.

Una bozza con qualcosa ancora da compilare, un file citato ma non disponibile o solo il tuo indirizzo viene rimandata all’IA perché la corregga. Se un’IA chiede la stessa attività o bozza due volte di fila, ne ricevi una sola.

## Collegane una

Apri **Impostazioni**, **App**. Sotto **Le app di The Machine** trovi **Aggiungi in ChatGPT** e **Aggiungi in Claude**. Sotto **Oppure aggiungila con un indirizzo** trovi l’indirizzo unico dell’app ufficiale per ogni Machine, `https://mcp.themachine.computer/mcp`, e **Il tuo indirizzo**, `https://<your name>.mcp.themachine.computer/mcp`, entrambi con **Copia**.

Su una Machine installata sul tuo computer, premi prima **Configura** sotto **Richiedi il tuo indirizzo**. Si apre una pagina del tuo account: controlla che mostri lo stesso codice, conferma e scegli un nome. La tua Machine si abbina da sola, senza riavviarsi. Serve in entrambi i casi.

La tua Machine configura poi da sola il suo indirizzo sicuro. Ci vogliono alcuni minuti.

Per Claude, premi **Aggiungi in Claude** o apri [The Machine nell’elenco di Claude](https://claude.ai/directory/the-machine), poi premi Collega. Con i piani Team ed Enterprise, un proprietario deve aggiungerla nelle impostazioni dell’organizzazione.

La skill di The Machine indica a Claude quando usare la tua Machine: prima il riepilogo, poi le tue regole e il tuo stile, prima di preparare qualsiasi bozza. Premi **Scarica** accanto a **skill di Claude**, poi in Claude apri Customize, Skills e carica il file.

Per usare un indirizzo in Claude, apri invece Customize, Connectors, premi + Add, poi Add custom connector. Dai il nome The Machine, incolla l’indirizzo, premi Continue e poi Add.

Per ChatGPT, premi **Aggiungi in ChatGPT** o apri [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), poi premi Install plugin. Con i piani Business ed Enterprise, potrebbe essere necessario che un amministratore la autorizzi prima.

L’app ufficiale raggiunge una Machine ospitata e anche una Machine sul tuo computer, una volta configurato il suo indirizzo.

Per usare il tuo indirizzo privato o una Machine non collegata al Network, aggiungi invece un server MCP personalizzato in ChatGPT: apri chatgpt.com/plugins, premi +, poi Add custom MCP server. Dai il nome The Machine, incolla l’indirizzo e scegli OAuth. Conferma l’avviso e premi Create as a plugin. Il tuo piano o spazio di lavoro deve consentire l’uso di server MCP personalizzati.

Con l’app ufficiale, l’IA ti chiede di accedere con il tuo account The Machine. Se hai più di una Machine, scegli quella giusta e approva la richiesta nella pagina della tua Machine. Con l’indirizzo privato, l’IA si collega direttamente alla tua Machine.

Anche le IA su un dispositivo nella tua rete privata (Tailscale), come Claude Code o Cursor, possono usare l’indirizzo della tua dashboard seguito da `/mcp`. **Scollega questa Machine**, in fondo a **Impostazioni**, **Account**, rimuove dal tuo account una Machine installata sul tuo computer.

La tua Machine mostra quale IA sta inviando la richiesta. Se non riesce a identificarla, mostra da dove proviene la richiesta: collegala solo se hai appena avviato tu la procedura.

Scegli cosa può fare, **Leggi** o **Lettura e modifica**. Se hai account di lavoro e personali, scegli a quali può accedere. Poi scegli per quanto tempo: **1 giorno**, **7 giorni**, **30 giorni** o **1 anno**. Premi **Collega** oppure **Annulla** per rifiutare la richiesta.

## App ufficiale o indirizzo privato

L’app ufficiale è la soluzione più semplice: un solo indirizzo per tutti e il tuo account trova la tua Machine. Il nostro cloud inoltra le richieste e non ne salva mai il contenuto.

Con il tuo indirizzo privato, tutto viene cifrato fino alla tua Machine. Il cloud si limita a inoltrarlo e non può leggerlo.

In entrambi i casi decide la tua Machine. Può accedere solo un’IA che hai approvato nella sua pagina, con i permessi che hai scelto. In **Impostazioni**, **App**, le IA collegate tramite l’app ufficiale mostrano **App ufficiale**.

## Cosa può vedere

Una connessione vede solo la propria area. L’area di lavoro include le attività e le promesse dei tuoi account di lavoro, le persone, le aziende, i progetti e il brief del team della tua Fleet di lavoro. L’area personale comprende tutto il resto. Il testo dei messaggi resta sulla tua Machine, a meno che tu non attivi **Messaggi**: senza questa opzione, un’IA vede solo il mittente, l’oggetto e la data delle fonti di un’attività.

I record del Graph del team dei tuoi colleghi non vengono mai condivisi con un’IA esterna.

## Messaggi

**Messaggi** permette a un’IA di cercare e leggere le tue email, i messaggi di Slack, WhatsApp e altre chat. È disattivata finché non la attivi, nella pagina in cui colleghi l’IA oppure in seguito da **Impostazioni**, **App**. L’IA può solo leggere: non invia, elimina né contrassegna nulla.

Legge solo i messaggi della propria area. Alcuni non vengono mai condivisi: codici monouso e link di accesso, messaggi di una bacheca o di un progetto **Solo tu**, conversazioni che The Machine ha identificato come sensibili (accordi, risorse umane, questioni legali, salute, denaro), conversazioni che hai mantenuto private e messaggi eliminati.

Ogni lettura compare in **Movimenti** con il numero di messaggi e le conversazioni interessate, mai con il testo. La tua Machine passa il testo all’IA contrassegnandolo come dato, così l’IA non dovrebbe seguire le istruzioni contenute in un messaggio.

Quando Messaggi è attiva, le modifiche al Graph apportate da un’IA con **Lettura e modifica** restano in attesa della tua conferma. Premi **Applica** o **Scarta** sulla modifica in **Movimenti**.

## Eventi

**Eventi** permette a un’IA come ChatGPT di avviarsi da sola quando succede qualcosa: una nuova attività, un briefing per una riunione di domani o una promessa in scadenza domani. Ogni evento è disattivato finché non lo attivi da **Cambia**. L’IA riceve quindi il titolo e una breve spiegazione, senza informazioni che non possa già leggere e senza dati precedenti all’attivazione.

L’IA non può comunque inviare nulla e le sue modifiche compaiono in **Movimenti** con **Annulla**. Se disattivi un evento o l’IA, l’attività si interrompe subito.

## Nelle Impostazioni

Apri **Impostazioni**, **App** per vedere ogni IA che si è collegata, con i relativi permessi, area, data di scadenza e ultimo utilizzo. Puoi attivare o disattivare **Messaggi** direttamente da qui. Premi **Cambia** per modificare i permessi, l’area o la durata dell’accesso. Le modifiche si applicano alla richiesta successiva. **Movimenti** elenca tutte le richieste, anche quelle rifiutate. **Disattiva ora** mette in pausa l’IA: tutte le sessioni di accesso terminano, ma la cronologia resta. **Rimuovi** la elimina insieme alla cronologia.

Quando accedi di nuovo alla stessa IA, la nuova autorizzazione sostituisce quella precedente. Se l’IA aveva già una sessione di accesso, resta collegata con i nuovi permessi. Le IA che usi restano connesse fino alla data di scadenza; se non ne usi una per 90 giorni, dovrai accedere di nuovo.

Un’IA che non può accedere da sola può usare una chiave. In **Aggiungi una chiave**, assegnale un nome, scegli i permessi e la durata, poi premi **Crea chiave**. Copia subito la chiave: verrà mostrata una sola volta. L’IA la invia come `Authorization: Bearer <key>`.

## Proteggi il tuo account

Ogni richiesta viene registrata, anche quelle rifiutate. Le richieste di una connessione scaduta o disattivata vengono rifiutate finché non la modifichi. La tua Machine conserva solo un’impronta digitale di ogni accesso, quindi una copia dei suoi dati non permette di accedere.
