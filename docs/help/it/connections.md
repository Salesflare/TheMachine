---
title: Connessioni
area: connections
summary: Tutte le tue fonti in un unico posto: scopri come stanno andando, aggiungine una o disconnettila.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 9f2a2162fe015e0b
---
## Come stanno andando

La scheda **Connessioni** mostra le tue fonti divise per categoria, con **Accessi** e **Controlli** sotto una linea. Sul telefono, tocca una categoria per aprirla e **Connessioni** per tornare indietro. Si apre per prima la categoria con una fonte che richiede il tuo intervento. Ogni fonte è una riga che mostra come sta andando (Connessa, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo aiuto) e cosa ha ricevuto di recente. Tocca la riga per aprire la scheda della fonte e **Dettagli**.

Una sincronizzazione non riuscita, poi recuperata da una successiva, appare in grigio. Viene segnalato come problema solo un errore che è ancora il più recente, con l'indicazione di quando verrà fatto un nuovo tentativo.

I conteggi mostrano tutto ciò che la fonte ha importato, compresa la [cronologia](history.md), ciò che è arrivato nelle ultime 24 ore e gli elementi non ancora controllati. Per un calendario vengono conteggiati gli eventi.

Ogni fonte prende il nome dal suo account, come lo chiama il servizio: il tuo indirizzo, un profilo X, un'area di lavoro Slack o la persona a cui appartiene l'account Signal o Telegram. Sotto il nome trovi prima **Lavoro** o **Personale**, poi l'indirizzo o il nome utente, se non è già indicato nel nome. Se due fonti della stessa categoria hanno lo stesso nome, viene aggiunto anche un dettaglio per distinguerle, ad esempio Slack o X, oppure l'indirizzo dell'area di lavoro.

Ogni fonte indica anche in una riga cosa importa e, se può eseguire azioni, specifica che lo fa solo dopo che premi **Invia** o dai l'OK.

## Aggiungi una fonte

Apri una categoria (**Email**, **Calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**) e scegli una fonte in **Aggiungine un altro**, oppure sotto l'elenco se non ne hai ancora collegate. In fondo trovi un'opzione generica: **Altra email** in Email, **Link del calendario (ICS)** e **Altro calendario** in Calendario. Exchange Server importa le riunioni, quindi si trova in Calendario.

**Suggerito per te** appare in cima a **Connessioni** quando la tua Machine rileva un motivo per consigliarti una fonte. Il motivo è indicato in una riga, ad esempio email da Stripe, riunioni Zoom nel calendario, messaggi con link a Google Docs o una configurazione non completata. La fonte resta anche nel suo gruppo, contrassegnata come **Suggerito**. Questi dati vengono conteggiati sulla tua Machine, senza inviarli altrove. Una fonte già collegata non viene mai suggerita.

Microsoft Teams compare due volte: in **Chat** per le chat e in **Riunioni** come **Riunioni Teams** per le note delle riunioni. Entrambe usano lo stesso accesso Microsoft, quindi collegandone una colleghi anche l'altra.

Nell'elenco, le fonti che hai già collegato sono indicate insieme al relativo account. Selezionale per aggiungerne un'altra accanto: il modulo lo specifica e include un link a quella che hai già.

Inserisci le informazioni richieste, come una chiave o un indirizzo, scegli **Lavoro** con il nome dell'azienda oppure **Personale** (per email e calendari ti verrà chiesto solo se dall'indirizzo non si capisce), poi premi **Collegati**. Per un sito come LinkedIn o X, si apre la pagina di accesso nel browser della tua Machine e la procedura continua in automatico una volta effettuato l'accesso. GitHub, WhatsApp e Codex mostrano un codice da inserire; Telegram e Signal mostrano un codice QR da scansionare.

**Annulla** interrompe l'aggiunta. Se sei uscito prima di completarla, riapri **Connessioni** da qualsiasi dispositivo: la procedura riprenderà dallo stesso passaggio. Una volta collegata, la tua Machine inizia subito a leggerla e mostra come procede la prima sincronizzazione.

Su una Machine ospitata, puoi accedere da qui alle fonti che richiedono un accesso: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Scegli **Lavoro** o **Personale** e premi il pulsante di accesso, ad esempio **Accedi con Google**. Tornerai a questo modulo, che mostrerà com'è andata. Anche i codici di GitHub, WhatsApp, Codex, Telegram e del tuo telefono Android vengono mostrati qui.

Sul tuo computer, le stesse fonti richiedono l'accesso dopo aver abbinato la tua Machine al tuo account. La prima volta, premi **Abbina questa Machine**. Alcune offrono anche un'altra modalità, ad esempio con la tua app o una chiave.

**Riconnetti**, sulla fonte o in **Serve il tuo intervento**, apre lo stesso modulo. Sul tuo computer, `assistant connect` fa la stessa cosa da un terminale.

## Lavoro o personale

Ogni fonte è considerata di lavoro, per un'azienda che indichi, o personale. Puoi cambiare questa impostazione in **Dettagli**. **Indovinato** significa che la tua Machine ha dedotto l'impostazione dall'indirizzo. Le attività di lavoro aspettano i tuoi giorni lavorativi.

Per le email e i calendari Google e Microsoft, l'impostazione viene dedotta dall'indirizzo quando è chiaro: un provider di posta come Gmail o Outlook.com è Personale, mentre il dominio della tua azienda è Lavoro. In caso contrario, ti verrà chiesto una volta sola, subito dopo l'accesso. **Cambia** ti permette di impostarla manualmente. Se in seguito la posta indica l'opposto, l'attività **Ottieni di più da The Machine** ti chiederà una volta se vuoi cambiarla.

## Funzioni

Una fonte può importare segnali (ciò che arriva diventa attività), svolgere azioni per le tue attività (leggere un documento, inviare, rispondere o modificare qualcosa dopo la tua conferma) oppure fare entrambe le cose. Se fa entrambe, in **Dettagli** trovi un interruttore per ciascuna funzione: **Porta segnali** e **Può fare cose**. Una delle due resta attiva: per disattivarle entrambe, disconnetti la fonte. Una chat ha solo **Può fare cose**.

Se **Porta segnali** è disattivato, la fonte non si sincronizza. Se **Può fare cose** è disattivato, la tua Machine non la legge, non prepara bozze e non modifica nulla.

## Rimuovi una fonte

Apri la fonte, poi **Dettagli** e **Disconnetti**. La tua Machine smette di leggerla. Ciò che ha già importato resta disponibile. Su una Machine ospitata, le fonti il cui accesso è gestito dalla pagina di configurazione (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) mostrano **Disconnetti ↗**. Selezionalo per aprire la pagina di configurazione.

**Disconnesso di recente** mostra gli account Google, Microsoft, Zoom, Slack, Stripe e Salesforce che hai rimosso negli ultimi 30 giorni e la data della rimozione. Finché il servizio non la conferma, viene mostrato lo stato In attesa e la Machine continua a riprovare. Un account Google compare una sola volta, anche se Google Meet o Docs avevano un accesso separato. Ogni account appare nella propria categoria: un account Google o Microsoft in **Email**, Slack in **Chat**.

## Accessi salvati

Per siti come LinkedIn o X, seleziona **Salva per la prossima volta** quando accedi. L'elenco **Accessi** mostrerà questi siti e, quando un sito disconnette la tua Machine, potrai accedere di nuovo con un solo tocco. Le password restano crittografate sulla tua Machine. **Dimentica** rimuove un accesso.

Un sito può avere più account, ad esempio **Lavoro** e **Personale**. **Salva come** propone come opzione iniziale il contesto dell'attività; **Altro nome…** ti permette di scegliere un nome. Un'attività accede con l'account più adatto. Se non è chiaro quale usare, la finestra di dialogo te lo chiederà una volta sola e ricorderà la scelta per quell'attività.

**Accessi** mostra una sola voce per sito, con i relativi account sotto: il nome utente e un menu con il contesto. Puoi cambiarlo in qualsiasi momento. Gli accessi salvati prima che fossero disponibili gli account mostrano **Lavoro o personale?** finché non ne scegli uno. Se cambi il contesto di un accesso già usato da un'attività, l'attività ti chiederà di selezionarlo di nuovo.

**Importa** aggiunge gli accessi da un gestore di password: un'esportazione CSV da 1Password, LastPass, Bitwarden o Chrome, oppure direttamente da 1Password e LastPass tramite gli strumenti da riga di comando, se hai effettuato l'accesso su questo computer. Puoi selezionare quali accessi mantenere. La tua Machine non accede mai al gestore di password e non ti chiede la password principale. Elimina il file esportato una volta terminato.

Un accesso salvato viene usato solo per il suo indirizzo web: stesso sito, `https` e stessa porta. Non viene usato per un indirizzo simile né per un altro sottodominio.

## Controlli

**Controlli** mostra come la tua Machine legge ciò che arriva: i controlli recenti e i risultati di ciascuno. Vedi [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha un articolo dedicato in questa sezione, con informazioni su cosa legge e cosa può inviare.
