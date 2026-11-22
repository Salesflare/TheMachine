---
title: Connessioni
area: connections
summary: Tutte le tue fonti in un unico posto: controlla come funzionano, aggiungine una o disconnettila.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 0896d8f689ca9699
---
## Come funzionano

La scheda **Connessioni** elenca le tue fonti per tipo, con **Accessi** e **Controlli** sotto una linea. Sul telefono, tocca un tipo per aprirlo e **Connessioni** per tornare indietro. Si apre per prima la categoria che contiene una fonte che richiede il tuo intervento. Ogni fonte è una riga: indica come funziona (Connessa, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo intervento) e cosa è arrivato di recente. Tocca la riga per aprire la scheda della fonte e **Dettagli**.

Una sincronizzazione non riuscita, recuperata da quella successiva, viene mostrata in grigio. Solo l’ultimo tentativo non riuscito viene segnalato come problema, con l’ora del prossimo tentativo.

I conteggi mostrano tutto ciò che la fonte ha importato, inclusa la [cronologia](history.md), quello che è arrivato nelle ultime 24 ore e ciò che non è ancora stato controllato. Per un calendario, vengono conteggiati gli eventi.

Ogni fonte ha il nome del relativo account, come lo visualizza il servizio: il tuo indirizzo, un profilo X, un’area di lavoro Slack o il nome della persona a cui appartiene l’account Signal o Telegram. Sotto il nome compare prima **Lavoro** o **Personale**, poi l’indirizzo o il nome utente, se non è già incluso nel nome. Se due fonti dello stesso tipo hanno lo stesso nome, viene indicato anche l’elemento che le distingue, ad esempio Slack o X, oppure l’indirizzo dell’area di lavoro.

Ogni fonte indica anche in una riga cosa importa e, se può eseguire azioni, che agisce solo dopo che premi **Invia** o dai l’OK.

## Aggiungere una fonte

Apri un tipo (**Email**, **Calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**) e scegli una fonte sotto **Aggiungine un altro**, oppure sotto l’elenco se non ne hai ancora collegate. In fondo trovi un’opzione generica: **Altra email** sotto Email, **Link del calendario (ICS)** e **Altro calendario** sotto Calendario. Exchange Server importa le riunioni, quindi si trova sotto Calendario.

**Suggerito per te** compare in cima a **Connessioni** quando la tua Machine rileva un motivo per aggiungere una fonte. Il motivo viene indicato in una riga: email da Stripe, riunioni Zoom nel calendario, messaggi con link a Google Docs o una configurazione non completata. La fonte resta anche nel suo gruppo, contrassegnata come **Suggerito**. La tua Machine elabora questi dati al suo interno, senza che escano da lì. Una fonte connessa non viene mai suggerita.

Microsoft Teams compare due volte: sotto **Chat** per le chat e sotto **Riunioni** come **Riunioni Teams** per gli appunti delle riunioni. Entrambi usano lo stesso accesso Microsoft, quindi collegandone uno colleghi anche l’altro.

Se hai già collegato una fonte, nell’elenco viene indicato il suo account. Selezionala per aggiungerne un’altra dello stesso tipo: il modulo lo specifica e include un link a quella già collegata.

Inserisci le informazioni richieste, come una chiave o un indirizzo, scegli **Lavoro** con il nome dell’azienda o **Personale** (per email e calendari ti viene chiesto solo se l’indirizzo non è sufficiente a stabilirlo), poi premi **Collegati**. Se si tratta di un sito come LinkedIn o X, si apre la pagina di accesso nel browser della tua Machine e la procedura prosegue automaticamente quando accedi. GitHub, WhatsApp e Codex mostrano un codice da inserire; per le chat Telegram e Signal mostrano un codice QR da scansionare.

Premi **Annulla** per interrompere l’aggiunta. Se esci prima di finire, riapri **Connessioni** da qualsiasi dispositivo e riprendi da dove avevi lasciato. Una volta connessa, la tua Machine inizia subito a leggerla e mostra come procede la prima sincronizzazione.

Su una Machine ospitata, le fonti con una procedura di accesso dedicata si collegano da qui: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Scegli **Lavoro** o **Personale** e premi il pulsante di accesso, ad esempio **Accedi con Google**. Tornerai a questo modulo, che ti mostrerà l’esito. Qui vengono mostrati anche i codici per GitHub, WhatsApp, Codex, le chat Telegram e il tuo telefono Android.

Sul tuo computer, le stesse fonti effettuano l’accesso dopo che hai abbinato la tua Machine al tuo account: premi **Abbina questa Machine** la prima volta. Alcune offrono anche un altro metodo, ad esempio la tua app o una chiave.

**Riconnetti**, nella fonte o in **Serve il tuo intervento**, apre lo stesso modulo. Sul tuo computer, `assistant connect` fa la stessa cosa da un terminale.

## Lavoro o personale

Ogni fonte è classificata come lavoro, per un’azienda che indichi, o personale. Puoi modificarla in **Dettagli**. **Ipotizzato** indica che la tua Machine ha dedotto la categoria dall’indirizzo. Le attività di lavoro attendono i tuoi giorni lavorativi.

Per le email e i calendari Google e Microsoft, la categoria viene dedotta dall’indirizzo, se è chiaro: un provider di posta come Gmail o Outlook.com indica Personale, il dominio della tua azienda indica Lavoro. Se non è chiaro, ti viene chiesto una volta, subito dopo l’accesso. **Cambia** ti permette di impostarla manualmente. Se in seguito le email indicano l’altra categoria, l’attività **Sfrutta al meglio The Machine** ti chiederà una volta se vuoi cambiarla.

## Funzioni

Una fonte può importare segnali (quello che arriva diventa un’attività), eseguire azioni per le tue attività (leggere un documento, inviare, rispondere o modificare qualcosa dopo la tua conferma) oppure fare entrambe le cose. Se fa entrambe, in **Dettagli** trovi un interruttore per ciascuna funzione: **Raccoglie segnali** e **Può fare cose**. Una delle due resta sempre attiva. Per disattivarle entrambe, disconnetti la fonte. Una chat ha solo **Può fare cose**.

Se disattivi **Raccoglie segnali**, la fonte non si sincronizza. Se disattivi **Può fare cose**, la tua Machine non legge, prepara bozze o modifica mai nulla tramite quella fonte.

## Rimuovere una fonte

Apri la fonte, vai a **Dettagli** e premi **Disconnetti**. La fonte smette di essere letta. I dati già importati restano. Su una Machine ospitata, per le fonti il cui accesso è gestito dalla pagina di configurazione (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) compare **Disconnetti ↗**, che apre la pagina di configurazione.

**Disconnesso di recente** elenca gli account Google, Microsoft, Zoom, Slack, Stripe e Salesforce che hai rimosso negli ultimi 30 giorni e indica quando li hai rimossi. Finché il servizio non conferma la rimozione, lo stato è In attesa e la Machine continua a riprovare. Un account Google compare una sola volta, anche se Google Meet o Docs aveva un accesso separato. Ogni account compare nel proprio gruppo: un account Google o Microsoft sotto **Email**, Slack sotto **Chat**.

## Accessi salvati

Per i siti come LinkedIn o X, seleziona **Salva per la prossima volta** quando accedi. Da quel momento, **Accessi** li elenca e, quando un sito disconnette la tua Machine, basta un tocco per accedere di nuovo. Le password restano cifrate sulla tua Machine. **Dimentica** rimuove un accesso.

Un sito può avere più account, ad esempio **Lavoro** e **Personale**. **Salva come** propone inizialmente la categoria dell’attività; **Altro nome…** ti permette di inserire un nome personalizzato. Un’attività accede con l’account più adatto. Se non è chiaro quale usare, una finestra di dialogo ti chiede una volta quale scegliere e lo ricorda per quell’attività.

**Accessi** elenca una sola volta ogni sito, con i relativi account sotto: il nome utente e un menu con la categoria. Puoi modificarla in qualsiasi momento. Gli accessi salvati prima dell’introduzione degli account mostrano **Lavoro o personale?** finché non ne scegli una. Se cambi la categoria di un accesso usato da un’attività, l’attività ti chiederà di sceglierlo di nuovo.

**Importa** importa gli accessi da un gestore di password. Scegline uno:

- **LastPass**, **Bitwarden** o **Google Password Manager**: si apre la pagina di esportazione nel browser della tua Machine, direttamente nella finestra di dialogo, come avviene con il comando **Fallo** di un’attività. Accedi e la tua Machine prosegue fino all’esportazione. Una riga indica cosa devi fare, ad esempio inserire la password principale. LastPass invia un link per confermare l’esportazione: la tua Machine la avvia una volta, apre il link quando l’email arriva in una casella connessa entro 10 minuti e, in caso contrario, ti chiede di confermare e ripetere l’esportazione. Sul telefono, la schermata si ingrandisce nel punto in cui devi digitare. Se la pagina è diversa da quella prevista, vengono mostrati i passaggi da completare manualmente. La tua Machine recupera il file, lo legge una volta e lo elimina.
- **1Password**: esporta un CSV dall’app 1Password su un computer, poi seleziona il file. Se `op` di 1Password è collegato alla tua Machine, i dati vengono importati da lì (lo stesso vale per `lpass` di LastPass).
- **Da un file esportato**: un CSV di 1Password, LastPass, Bitwarden o Chrome. Eliminalo quando hai finito.

Poi seleziona gli accessi da conservare. La tua Machine non accede mai al gestore di password al posto tuo, non inserisce né legge la password principale e non mostra la pagina all’assistente: la password la inserisci tu nella pagina.

Un accesso salvato viene usato solo per il suo indirizzo web: lo stesso sito, `https` e la stessa porta. Non viene usato per un indirizzo simile o per un altro sottodominio.

## Controlli

**Controlli** mostra come la tua Machine esamina i dati in arrivo: i controlli recenti e quello che ha rilevato in ciascuno. Vedi [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha un articolo dedicato in questa sezione, con i dati che legge e ciò che può inviare.
