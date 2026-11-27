---
title: Collega altre IA
area: connections
summary: Consenti a Claude, ChatGPT, Cursor, Codex o GBrain di leggere le tue attività e il tuo Graph e, con **Lettura e modifica**, di apportare modifiche che puoi annullare.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 7681c632f712e93c
---
## Cosa può fare un’altra IA

Claude, ChatGPT, Cursor, Codex, GBrain e altre IA possono collegarsi alla tua Machine. Possono leggere le tue attività, le promesse, i brief del team e le persone e le aziende nel tuo Graph.

Con **Lettura e modifica** possono anche aggiungere un’attività o una bozza di email e aggiornare il tuo Graph: salvare un fatto, correggere dettagli, campi e tag oppure aggiungere una riga al riepilogo di una persona.

Ogni modifica compare in **Movimenti**, con **Annulla**. Non uniscono, eliminano né condividono mai i record. Ciò che salvano è contrassegnato da **IA:** e dal loro nome. La tua Machine lo considera una loro affermazione, mai una tua istruzione.

Una bozza resta in attesa finché non la leggi e premi tu Invia. Un’IA collegata non invia mai nulla e non agisce mai per conto tuo.

## Cosa impara da te

Quando avvii una chat, l’IA riceve un breve briefing: chi sei, le tue regole principali e cosa è cambiato dalla sua ultima visita. Può anche leggere ciò che contiene **Apprendimento**: le tue regole, le informazioni generali e il tuo modo di scrivere in ogni canale. Così scrive come faresti tu.

Con **Lettura e modifica**, può salvare ciò che decidi nella chat. Un fatto viene salvato subito, con **Annulla** in **Movimenti**. Una regola guida il lavoro della tua Machine, quindi resta in **Apprendimento** finché non premi **Approva** o **Scarta**. Non modifica mai il tuo stile di scrittura.

Una bozza con un campo da compilare, un file menzionato ma non disponibile o solo il tuo indirizzo, torna all’IA perché la corregga. Se un’IA richiede due volte di seguito la stessa attività o bozza, ne ricevi una sola.

## Collegane una

Apri **Impostazioni**, **App**. Sotto **Le app di The Machine** trovi **Aggiungi in ChatGPT** e **Aggiungi in Claude**. Sotto **Oppure aggiungila con un indirizzo** trovi l’indirizzo unico dell’app ufficiale per ogni Machine, `https://mcp.themachine.computer/mcp`, e **Il tuo indirizzo**, `https://<your name>.mcp.themachine.computer/mcp`, entrambi con **Copia**.

Su una Machine installata sul tuo computer, premi prima **Configura** sotto **Richiedi il tuo indirizzo**. Si apre una pagina del tuo account: controlla che mostri lo stesso codice, conferma e scegli un nome. La tua Machine si abbina da sola, senza riavviarsi. È necessario farlo in entrambi i casi.

Poi la tua Machine configura da sola il suo indirizzo sicuro. Ci vogliono alcuni minuti.

Per Claude, premi **Aggiungi in Claude** oppure apri [The Machine nella directory di Claude](https://claude.ai/directory/the-machine), poi premi Connect. Con i piani Team ed Enterprise, un proprietario deve aggiungerla nelle impostazioni dell’organizzazione.

La skill di The Machine dice a Claude quando usare la tua Machine: prima il briefing, poi le tue regole e il tuo stile, prima che prepari una bozza. Premi **Scarica** accanto a **skill di Claude**, poi in Claude apri Personalizza, Skill e carica il file.

Per usare un indirizzo in Claude, invece, apri Personalizza, Connettori, premi + Aggiungi, poi Aggiungi connettore personalizzato. Chiamalo The Machine, incolla l’indirizzo, premi Continua e poi Aggiungi.

Per ChatGPT, premi **Aggiungi in ChatGPT** oppure apri [The Machine in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), poi premi Installa plugin. Con i piani Business ed Enterprise, un amministratore potrebbe doverlo autorizzare prima.

L’app ufficiale si collega a una Machine ospitata e anche a una Machine installata sul tuo computer, una volta che ha il suo indirizzo.

Per usare il tuo indirizzo privato o una Machine che non è sul Network, aggiungi invece un server MCP personalizzato in ChatGPT: apri chatgpt.com/plugins, premi +, poi Aggiungi server MCP personalizzato. Chiamalo The Machine, incolla l’indirizzo e scegli OAuth. Conferma l’avviso e premi Crea come plugin. Il tuo piano o spazio di lavoro deve consentire l’uso di server MCP personalizzati.

Con l’app ufficiale, l’IA ti chiede di accedere con il tuo account The Machine. Se hai più di una Machine, scegli questa e poi approva dalla pagina della tua Machine. Con l’indirizzo privato, l’IA si collega direttamente alla tua Machine.

Anche le IA su un dispositivo nella tua rete privata (Tailscale), come Claude Code o Cursor, possono usare l’indirizzo della dashboard seguito da `/mcp`. **Scollega questa Machine**, in fondo a **Impostazioni**, **Account**, scollega dal tuo account una Machine installata sul tuo computer.

La tua Machine mostra quale IA sta facendo la richiesta. Se non riesce a identificarla, indica da dove arriva la richiesta: collegala solo se hai appena avviato tu la procedura.

Scegli cosa può fare, **Leggi** o **Lettura e modifica**. Se hai un account Work e uno Personal, scegli a cosa può accedere. Poi scegli per quanto tempo: **1 giorno**, **7 giorni**, **30 giorni** o **1 anno**. Premi **Collega** oppure **Annulla** per rifiutare la richiesta.

## App ufficiale o indirizzo privato

L’app ufficiale è la soluzione più semplice: un unico indirizzo per tutti e il tuo account trova la tua Machine. Il nostro cloud inoltra le richieste e non ne salva mai il contenuto.

Con il tuo indirizzo privato, tutto è cifrato fino alla tua Machine. Il cloud si limita a inoltrare le richieste e non può leggerle.

In entrambi i casi decide la tua Machine. Può accedere solo un’IA che hai approvato dalla sua pagina, con i permessi che hai scelto. In **Impostazioni**, **App**, un’IA collegata tramite l’app ufficiale mostra **App ufficiale**.

## Cosa può vedere

Una connessione vede solo la propria area. Work include le attività e le promesse dei tuoi account di lavoro, le persone, le aziende e i progetti di lavoro e il brief del team della tua Fleet di lavoro. Personal include tutto il resto. Il testo dei messaggi resta sulla tua Machine, a meno che tu non attivi **Messaggi**. Se non lo attivi, un’IA vede le fonti di un’attività solo per mittente, oggetto e data.

I record del Graph del team dei tuoi colleghi non vengono mai condivisi con un’IA esterna.

## Messaggi

**Messaggi** consente a un’IA di cercare e leggere le tue email, i messaggi Slack, WhatsApp e le altre chat. È disattivato finché non lo attivi, dalla pagina in cui colleghi l’IA o in seguito da **Impostazioni**, **App**. Può solo leggere: non invia, elimina né contrassegna mai nulla.

Legge solo i messaggi della propria area. Alcuni non vengono mai condivisi: i codici monouso e i link di accesso, i messaggi di una bacheca o di un progetto **Solo tu**, le conversazioni che The Machine ha identificato come sensibili (affari, risorse umane, questioni legali, salute, denaro), le conversazioni che hai mantenuto private e i messaggi eliminati.

Ogni lettura compare nei suoi **Movimenti**, con il numero di messaggi e le conversazioni coinvolte, mai il testo. La tua Machine consegna il testo contrassegnandolo come dato, così l’IA non dovrebbe seguire le istruzioni contenute in un messaggio.

Finché Messaggi è attivo, le modifiche al Graph fatte da un’IA con **Lettura e modifica** restano in attesa della tua approvazione. Premi **Applica** o **Scarta** sulla modifica in **Movimenti**.

## Nelle impostazioni

Apri **Impostazioni**, **App** per vedere ogni IA collegata, una sola volta, con i relativi permessi, area, data di scadenza e ultimo utilizzo. Puoi attivare e disattivare **Messaggi** da qui. Premi **Cambia** per modificare i permessi, l’area o la durata. La modifica si applica alla richiesta successiva. **Movimenti** elenca tutte le richieste, anche quelle rifiutate. **Disattiva ora** mette in pausa l’IA: tutte le sessioni di accesso terminano, ma la cronologia resta. **Rimuovi** la elimina insieme alla cronologia.

Quando accedi di nuovo alla stessa IA, la nuova approvazione sostituisce quella precedente. Se l’IA era già collegata, resta collegata con i nuovi permessi. Un’IA che usi resta collegata fino alla data di scadenza; se non la usi per 90 giorni, dovrai accedere di nuovo.

Un’IA che non può accedere da sola può usare una chiave. Sotto **Aggiungi una chiave**, assegnale un nome, scegli i permessi e la durata, poi premi **Crea chiave**. Copia subito la chiave: viene mostrata una sola volta. L’IA la invia come `Authorization: Bearer <key>`.

## Proteggi il tuo account

Ogni richiesta viene registrata, anche quelle rifiutate. Una connessione scaduta o disattivata viene rifiutata finché non la modifichi. La tua Machine conserva solo un’impronta di ogni accesso, quindi una copia dei suoi dati non permette di accedere.
