---
title: Connessioni
area: connections
summary: Tutte le tue fonti in un unico posto: controlla come vanno, aggiungine una o disconnettila.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 1ca62ab8f65b77ff
---
## Come vanno

La scheda **Connessioni** mostra le tue fonti divise per tipo, con **Accessi** e **Controlli** sotto una linea. Sul telefono, tocca un tipo per aprirlo e **Connessioni** per tornare indietro. Si apre per prima la categoria con una fonte che richiede il tuo intervento. Ogni fonte è una riga: mostra il suo stato (Connessa, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo intervento) e ciò che è arrivato di recente. Tocca una fonte per aprire la scheda e **Dettagli**.

Se una sincronizzazione non è riuscita ma una successiva ha recuperato i dati, l'errore appare in grigio. Viene segnalato come problema solo un errore ancora recente, insieme all'orario del prossimo tentativo.

I conteggi mostrano tutto ciò che la fonte ha importato, compresa la [cronologia](history.md), ciò che è arrivato nelle ultime 24 ore e ciò che non è ancora stato controllato. Per un calendario, vengono conteggiati gli eventi.

Ogni fonte prende il nome dal suo account, come lo chiama il servizio: il tuo indirizzo, un profilo X, uno spazio di lavoro Slack o la persona a cui appartiene l'account Signal o Telegram. Sotto il nome compare prima **Lavoro** o **Personale**, poi l'indirizzo o il nome utente se il nome non li include già. Se due fonti dello stesso tipo hanno lo stesso nome, viene indicato anche l'elemento che le distingue, ad esempio Slack o X, oppure l'indirizzo dello spazio di lavoro.

Ogni fonte indica anche, in una riga, cosa importa e, se può agire, che lo fa solo dopo che premi **Invia** o approvi l'azione.

## Aggiungerne una

Apri un tipo (**Email**, **Calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**) e scegli una fonte sotto **Aggiungine un altro** o, se non ne hai ancora collegate, sotto l'elenco. In fondo trovi le opzioni generiche: **Altra email** sotto Email, **Link del calendario (ICS)** e **Altro calendario** sotto Calendario. Exchange Server importa le riunioni, quindi si trova sotto Calendario.

Se la tua Machine rileva un motivo per aggiungere una fonte, in cima a **Connessioni** compare **Suggerito per te**, con una breve spiegazione: email da Stripe, riunioni Zoom nel tuo calendario, messaggi con link a Google Docs o una configurazione non completata. La fonte resta anche nel suo gruppo, contrassegnata come **Suggerito**. Questo conteggio viene calcolato sulla tua Machine: i dati non ne escono. Una fonte già connessa non viene mai suggerita.

Microsoft Teams compare due volte: sotto **Chat** per le chat e sotto **Riunioni** come **Riunioni Teams** per le note delle riunioni. Entrambe le opzioni usano lo stesso accesso Microsoft, quindi collegandone una si collega anche l'altra.

Nell'elenco, le fonti che hai già collegato sono indicate con il relativo account. Selezionale per aggiungerne un'altra accanto: il modulo lo specifica e include un link a quella che hai già.

Inserisci le informazioni richieste, come una chiave o un indirizzo, scegli **Lavoro** con il nome dell'azienda oppure **Personale**, poi premi **Collegati**. Per email e calendari, la scelta viene chiesta solo se l'indirizzo non basta a determinarla. Per servizi come LinkedIn o X, si apre la pagina di accesso nel browser della tua Machine e la procedura prosegue automaticamente dopo l'accesso. GitHub, WhatsApp e Codex mostrano un codice da inserire; le chat di Telegram mostrano un codice QR da scansionare.

Premi **Annulla** per interrompere la procedura. Se sei uscito prima di completarla, riapri **Connessioni** da qualsiasi dispositivo: la procedura riprende dal punto in cui eri arrivato. Dopo la connessione, la tua Machine inizia subito a leggere i dati e mostra lo stato della prima sincronizzazione.

Su una Machine ospitata, puoi accedere a Google, Microsoft, Microsoft OneDrive, Zoom, Stripe e Intercom direttamente qui: scegli **Lavoro** o **Personale** e premi **Accedi**. Tornerai a questo modulo, che mostrerà l'esito. Anche i codici di GitHub, WhatsApp, Codex, delle chat di Telegram e del tuo telefono Android vengono mostrati qui.

Premendo **Riconnetti** su una fonte o in **Serve il tuo intervento** si apre lo stesso modulo. Sul tuo computer, `assistant connect` fa lo stesso da un terminale.

## Lavoro o personale

Ogni fonte è classificata come lavorativa, per un'azienda che indichi, o personale. Puoi modificare la classificazione in **Dettagli**. **Indovinato** indica che la tua Machine l'ha dedotta dall'indirizzo. Le attività di lavoro aspettano i tuoi giorni lavorativi.

Per email e calendari Google e Microsoft, la classificazione viene dedotta dall'indirizzo quando è chiara: un provider di posta come Gmail o Outlook.com indica **Personale**, mentre il dominio della tua azienda indica **Lavoro**. Altrimenti, ti viene chiesto subito dopo l'accesso. Premi **Cambia** per impostarla tu. Se in seguito le email indicano l'altra opzione, l'attività **Ottieni di più da The Machine** ti chiederà una volta se vuoi cambiarla.

## Funzionalità

Una fonte può importare segnali, che diventano attività, eseguire azioni per le tue attività, come leggere un documento o inviare, rispondere o modificare qualcosa dopo la tua approvazione, oppure fare entrambe le cose. Se fa entrambe le cose, in **Dettagli** trovi un interruttore per ciascuna: **Porta segnali** e **Può fare cose**. Uno dei due deve restare attivo: per disattivarli entrambi, disconnetti la fonte. Una chat offre solo **Può fare cose**.

Se disattivi **Porta segnali**, la fonte non si sincronizza. Se disattivi **Può fare cose**, la tua Machine non legge, crea bozze o modifica mai nulla tramite quella fonte.

## Rimuoverne una

Apri la fonte, vai su **Dettagli** e premi **Disconnetti**. La fonte smette di essere letta, ma i dati già importati restano. Su una Machine ospitata, per Google, Microsoft, Microsoft OneDrive, Zoom e Stripe compare **Disconnetti ↗**, che apre la pagina di configurazione.

**Disconnesso di recente** elenca gli account Google, Microsoft, Zoom, Slack, Stripe e Salesforce che hai rimosso negli ultimi 30 giorni, con la data. Un account Google viene mostrato una sola volta, anche se Google Meet o Docs avevano un accesso separato. Ogni account compare sotto il proprio tipo: un account Google o Microsoft sotto **Email**, Slack sotto **Chat**.

## Accessi salvati

Per siti come LinkedIn o X, seleziona **Salva per la prossima volta** quando accedi. Gli account compaiono poi in **Accessi** e, quando un sito disconnette la tua Machine, puoi accedere di nuovo con un solo tocco. Le password restano crittografate sulla tua Machine. Premi **Dimentica** per rimuovere un account.

## Controlli

**Controlli** mostra come la tua Machine legge i dati in arrivo: i controlli recenti e ciò che è stato trovato. Consulta [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha una pagina dedicata in questa sezione, con i dati che legge e ciò che può inviare.
