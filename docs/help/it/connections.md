---
title: Connessioni
area: connections
summary: Tutte le tue fonti in un unico posto: controlla come stanno, aggiungine una o disconnettila.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 60304f2504ee5676
---
## Come stanno

La scheda **Connessioni** elenca le tue fonti per tipo, con **Accessi** e **Controlli** sotto una linea. Sul telefono, tocca un tipo per aprirlo e **Connessioni** per tornare indietro. Si apre per prima la categoria con una fonte che richiede il tuo intervento. Ogni fonte è una riga: mostra come sta (Connessa, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo intervento) e cosa è arrivato di recente. Tocca la fonte per aprire la scheda e **Dettagli**.

Una sincronizzazione non riuscita, poi recuperata da una successiva, viene mostrata in grigio. Solo un errore ancora recente viene mostrato come problema, con l'indicazione di quando verrà fatto un nuovo tentativo.

I conteggi mostrano tutto ciò che la fonte ha importato, compresa la [cronologia](history.md), cosa è arrivato nelle ultime 24 ore e cosa non è ancora stato controllato. Per un calendario vengono conteggiati gli eventi.

Ogni fonte prende il nome dal suo account, così come lo chiama il servizio: il tuo indirizzo, un profilo X, uno spazio di lavoro Slack o la persona a cui appartiene l'account Signal o Telegram. Sotto il nome appare prima **Lavoro** o **Personale**, poi l'indirizzo o il nome utente, se il nome non li indica già. Se due fonti dello stesso tipo hanno lo stesso nome, viene indicato anche l'elemento che le distingue, come Slack o X, oppure l'indirizzo dello spazio di lavoro.

Ogni fonte indica anche in una riga cosa importa e, se può eseguire azioni, specifica che lo fa solo dopo che premi **Invia** o dai l'OK.

## Aggiungerne una

Apri un tipo (**Email**, **Calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**) e scegli una fonte sotto **Aggiungine un altro**, oppure sotto l'elenco se non ne hai ancora collegate. In fondo trovi un'opzione generica: **Altra email** sotto Email, **Link del calendario (ICS)** e **Altro calendario** sotto Calendario. Exchange Server importa le riunioni, quindi si trova sotto Calendario.

Se la tua Machine trova un motivo per suggerirti una fonte, in cima a **Connessioni** appare **Suggerito per te**, con una breve spiegazione: email da Stripe, riunioni Zoom nel calendario, messaggi con link a Google Docs o una configurazione non completata. La fonte resta anche nel suo gruppo, contrassegnata come **Suggerito**. Il conteggio viene fatto sulla tua Machine: non esce nulla da lì. Una fonte già collegata non viene mai suggerita.

Microsoft Teams compare due volte: sotto **Chat** per le chat e sotto **Riunioni** come **Riunioni Teams** per le note delle riunioni. Entrambe usano lo stesso accesso Microsoft, quindi collegandone una si collega anche l'altra.

Nell'elenco, le fonti che hai già collegato sono contrassegnate con il relativo account. Selezionale per aggiungerne un'altra accanto: il modulo lo indica e include un link a quella che hai già.

Inserisci i dati richiesti, come una chiave o un indirizzo, scegli **Lavoro** e il nome dell'azienda oppure **Personale** (per email e calendari ti viene chiesto solo se l'indirizzo non lo indica) e premi **Collegati**. Per un sito come LinkedIn o X, si apre la pagina di accesso nel browser della tua Machine e, una volta effettuato l'accesso, la procedura continua da sola. GitHub, WhatsApp e Codex mostrano un codice da inserire; Telegram e Signal mostrano un codice QR da scansionare.

Premi **Annulla** per interrompere l'aggiunta. Se hai chiuso prima di completarla, riapri **Connessioni** da qualsiasi dispositivo: riprenderai dallo stesso passaggio. Una volta collegata, la tua Machine inizia subito a leggerla e mostra l'andamento della prima sincronizzazione.

Su una Machine ospitata, accedi direttamente qui alle fonti che hanno un proprio accesso: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Scegli **Lavoro** o **Personale** e premi il pulsante di accesso, per esempio **Accedi con Google**. Tornerai a questo modulo, che mostrerà l'esito. Qui trovi anche i codici per GitHub, WhatsApp, Codex, le chat Telegram e il tuo telefono Android.

Sul tuo computer, puoi accedere agli stessi servizi dopo aver abbinato la tua Machine al tuo account: la prima volta premi **Abbina questa Machine**. Alcuni servizi offrono anche un altro metodo, come la tua app o una chiave.

Premendo **Riconnetti** su una fonte o in **Serve il tuo intervento**, si apre lo stesso modulo. Sul tuo computer, `assistant connect` fa la stessa cosa da terminale.

## Lavoro o personale

Ogni fonte è considerata di lavoro (per un'azienda che indichi) o personale. Puoi cambiarla in **Dettagli**. **Dedotto** significa che la tua Machine ha ricavato la categoria dall'indirizzo. Le attività di lavoro aspettano i tuoi giorni lavorativi.

Per le email e i calendari Google e Microsoft, la categoria viene dedotta dall'indirizzo quando è chiaro: un provider email come Gmail o Outlook.com è Personale, mentre il dominio del tuo team è Lavoro. Altrimenti, ti viene chiesto una volta sola, subito dopo l'accesso. Con **Cambia** puoi impostarla tu. Se in seguito le email indicano l'altra categoria, l'attività **Ottieni di più da The Machine** ti chiederà una volta se vuoi cambiarla.

## Funzioni

Una fonte può importare segnali (ciò che arriva diventa attività), eseguire azioni per le tue attività (leggere un documento, inviare o rispondere a un messaggio oppure modificare qualcosa dopo la tua conferma) o fare entrambe le cose. Se fa entrambe le cose, in **Dettagli** trovi un interruttore per ciascuna funzione: **Porta segnali** e **Può fare cose**. Una delle due deve restare attiva. Per disattivarle entrambe, disconnetti la fonte. Una chat ha solo **Può fare cose**.

Se disattivi **Porta segnali**, la fonte non si sincronizza. Se disattivi **Può fare cose**, la tua Machine non leggerà, preparerà bozze o modificherà nulla tramite quella fonte.

## Rimuoverne una

Apri la fonte, vai su **Dettagli** e poi premi **Disconnetti**. La fonte smette di essere letta, ma ciò che ha già importato resta. Su una Machine ospitata, per le fonti il cui accesso è gestito dalla pagina di configurazione (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) viene mostrato **Disconnetti ↗**, che apre la pagina di configurazione.

**Disconnesso di recente** elenca gli account Google, Microsoft, Zoom, Slack, Stripe e Salesforce che hai rimosso negli ultimi 30 giorni e indica quando. Finché il servizio non conferma la rimozione, lo stato è In attesa e la Machine continua a riprovare. Un account Google compare una sola volta, anche se Google Meet o Docs aveva un proprio accesso. Ogni account appare sotto il proprio tipo: un account Google o Microsoft sotto **Email**, Slack sotto **Chat**.

## Accessi salvati

Per siti come LinkedIn o X, seleziona **Salva per la prossima volta** quando accedi. Gli account compariranno in **Accessi** e, se un sito disconnette la tua Machine, potrai accedere di nuovo con un solo tocco. Le password restano crittografate sulla tua Machine. Premi **Dimentica** per rimuovere un accesso.

## Controlli

In **Controlli** trovi informazioni su come la tua Machine legge ciò che arriva: i controlli recenti e i risultati di ciascuno. Vedi [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha un articolo dedicato in questa sezione, con informazioni su cosa legge e cosa può inviare.
