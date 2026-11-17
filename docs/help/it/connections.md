---
title: Connessioni
area: connections
summary: Tutte le tue fonti in un unico posto: controlla come vanno, aggiungine una o disconnettine una.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: ec53596a1636fee7
---
## Come stanno andando

La scheda **Connessioni** elenca le tue fonti per tipo, con **Accessi** e **Controlli** sotto una linea. Sul telefono, tocca un tipo per aprirlo e **Connessioni** per tornare indietro. Si apre per primo il tipo con una fonte che richiede il tuo intervento. Ogni fonte è una riga che mostra come sta andando (Connessa, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo intervento) e cosa è arrivato di recente. Toccala per aprire la sua scheda e **Dettagli**.

Una sincronizzazione non riuscita, recuperata da una successiva, viene mostrata in grigio. Solo un errore che è ancora il più recente viene segnalato come problema, con l'orario del prossimo tentativo.

I conteggi mostrano tutto ciò che la fonte ha importato, compresa la [cronologia](history.md), ciò che è arrivato nelle ultime 24 ore e ciò che non è ancora stato controllato. Per un calendario si contano gli eventi.

Ogni fonte ha il nome del suo account, nel formato usato dal servizio: il tuo indirizzo, un profilo X, uno spazio di lavoro Slack o il nome della persona a cui appartiene Signal o Telegram. Sotto il nome trovi prima **Lavoro** o **Personale**, poi l'indirizzo o il nome utente, se non è già indicato nel nome. Se due fonti dello stesso tipo hanno lo stesso nome, viene indicato anche un dettaglio che le distingue, come Slack o X, oppure l'indirizzo dello spazio di lavoro.

Ogni fonte spiega anche in una riga cosa importa e, se può agire, specifica che lo fa solo dopo che premi **Invia** o dai l'OK.

## Aggiungere una fonte

Apri un tipo (**Email**, **Calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**) e scegli una fonte sotto **Aggiungine un altro**, oppure sotto l'elenco se non hai ancora collegato nulla. In fondo trovi un'opzione generica: **Altra email** sotto Email, **Link del calendario (ICS)** e **Altro calendario** sotto Calendario. Exchange Server importa le riunioni, quindi si trova sotto Calendario.

**Suggerito per te** compare in cima a **Connessioni** quando la tua Machine rileva un motivo per aggiungere una fonte. Il motivo è indicato in una riga: email da Stripe, riunioni Zoom sul calendario, messaggi con link a Google Docs o una configurazione incompleta. La fonte rimane anche nel suo gruppo, contrassegnata come **Suggerito**. Questi dati vengono conteggiati sulla tua Machine, non escono da lì. Una fonte collegata non viene mai suggerita.

Microsoft Teams compare due volte: sotto **Chat** per le chat e sotto **Riunioni** come **Riunioni Teams** per le note delle riunioni. Entrambe usano lo stesso accesso Microsoft, quindi collegandone una colleghi anche l'altra.

Nell'elenco, le fonti che hai già collegato sono indicate con il relativo account. Selezionane una per aggiungerne un'altra accanto: il modulo lo specifica e include un link a quella che hai già.

Inserisci i dati richiesti, come una chiave o un indirizzo, scegli **Lavoro** e indica l'azienda oppure **Personale** (per email e calendari ti viene chiesto solo se l'indirizzo non lo indica), poi premi **Collegati**. Per siti come LinkedIn o X, si apre la schermata di accesso nel browser della tua Machine e la procedura prosegue automaticamente quando accedi. GitHub, WhatsApp e Codex mostrano un codice da inserire; Telegram e Signal mostrano un codice QR da scansionare.

**Annulla** interrompe l'aggiunta. Se sei uscito prima di finire, riapri **Connessioni** da qualsiasi dispositivo: la procedura riprenderà dal passaggio in cui ti eri fermato. Una volta collegata, la tua Machine inizia subito a leggerla e mostra l'andamento della prima sincronizzazione.

Su una Machine ospitata, puoi accedere direttamente qui alle fonti con un accesso dedicato: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Scegli **Lavoro** o **Personale** e premi il pulsante di accesso, ad esempio **Accedi con Google**. Tornerai a questo modulo, che mostrerà l'esito. GitHub, WhatsApp, Codex, Telegram e il tuo telefono Android mostrano qui anche il relativo codice.

Sul tuo computer, puoi accedere alle stesse fonti dopo aver abbinato la tua Machine al tuo account: la prima volta premi **Abbina questa Machine**. Alcune fonti offrono anche un altro metodo, come un'app personale o una chiave.

**Riconnetti**, sulla fonte o in **Serve il tuo intervento**, apre lo stesso modulo. Sul tuo computer, `assistant connect` fa la stessa cosa da terminale.

## Lavoro o personale

Ogni fonte è classificata come lavorativa, per un'azienda che indichi, o personale. Puoi modificare la classificazione in **Dettagli**. **Dedotto** significa che la tua Machine l'ha ricavata dall'indirizzo. Le attività di lavoro aspettano i tuoi giorni lavorativi.

Per le email e i calendari Google e Microsoft, la classificazione viene ricavata dall'indirizzo quando è chiara: un provider di posta come Gmail o Outlook.com indica **Personale**, il dominio della tua azienda indica **Lavoro**. Altrimenti ti viene chiesto una volta, subito dopo l'accesso. **Cambia** ti permette di impostare la classificazione manualmente. Se in seguito le email indicano l'altra opzione, l'attività **Ottieni di più da The Machine** ti chiede una volta se vuoi cambiarla.

## Funzionalità

Una fonte può importare segnali, che diventano attività, svolgere azioni per le tue attività (leggere un documento o inviare, rispondere o modificare qualcosa dopo la tua conferma) oppure fare entrambe le cose. Se fa entrambe, in **Dettagli** trovi un interruttore per ciascuna funzionalità: **Porta segnali** e **Può fare cose**. Una delle due deve restare attiva: per disattivarle entrambe, disconnetti la fonte. Per una chat è disponibile solo **Può fare cose**.

Se disattivi **Porta segnali**, la fonte non si sincronizza. Se disattivi **Può fare cose**, la tua Machine non legge, prepara bozze o modifica nulla tramite quella fonte.

## Rimuovere una fonte

Apri la fonte, poi **Dettagli** e **Disconnetti**. La tua Machine smette di leggerla, ma conserva ciò che aveva già importato. Su una Machine ospitata, per le fonti il cui accesso è gestito dalla pagina di configurazione (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce), compare **Disconnetti ↗**, che apre la pagina di configurazione.

**Disconnesso di recente** elenca gli account Google, Microsoft, Zoom, Slack, Stripe e Salesforce rimossi negli ultimi 30 giorni e indica quando li hai rimossi. Finché il servizio non conferma la rimozione, lo stato è In attesa e la Machine continua a riprovare. Un account Google compare una sola volta, anche se Google Meet o Docs aveva un accesso separato. Ogni account compare sotto il proprio tipo: un account Google o Microsoft sotto **Email**, Slack sotto **Chat**.

## Accessi salvati

Per siti come LinkedIn o X, seleziona **Salva per la prossima volta** quando accedi. Gli accessi compariranno in **Accessi**. Se un sito disconnette la tua Machine, potrai accedere di nuovo con un tocco. Le password restano crittografate sulla tua Machine. **Dimentica** rimuove un accesso.

Un sito può avere più account, ad esempio **Lavoro** e **Personale**. **Salva come** seleziona inizialmente la categoria dell'attività, mentre **Altro nome…** ti permette di assegnarle un nome personalizzato. Un'attività accede con l'account più adatto. Se non è chiaro quale usare, una finestra di dialogo ti chiede una volta quale preferisci e lo ricorda per quell'attività.

**Accessi** elenca una sola volta ogni sito, con i relativi account sotto. Gli accessi salvati prima che fossero disponibili più account compaiono come **Predefinito** finché non ne scegli la categoria.

**Importa** aggiunge gli accessi da un gestore di password: da un file CSV esportato da 1Password, LastPass, Bitwarden o Chrome, oppure direttamente dagli strumenti a riga di comando di 1Password e LastPass, se hai effettuato l'accesso su questo computer. Puoi selezionare quali accessi mantenere. La tua Machine non accede mai al gestore di password e non ti chiede mai la password principale. Elimina il file esportato una volta terminato.

Un accesso salvato viene usato solo per il suo indirizzo web: lo stesso sito, `https` e la stessa porta. Non viene usato per un indirizzo simile o per un altro sottodominio.

## Controlli

**Controlli** mostra come la tua Machine legge ciò che arriva: i controlli recenti e i risultati di ciascuno. Vedi [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha un articolo dedicato in questa sezione, con i dettagli su cosa legge e cosa può inviare.
