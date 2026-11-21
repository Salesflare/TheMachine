---
title: Connessioni
area: connections
summary: Tutte le tue fonti in un unico posto: scopri come funzionano, aggiungine una o disconnettine una.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 353fdfaa67678a1f
---
## Come funzionano

La scheda **Connessioni** elenca le tue fonti per categoria, con **Accessi** e **Controlli** sotto una linea. Sul telefono, tocca una categoria per aprirla e **Connessioni** per tornare indietro. Si apre per prima la categoria con una fonte che ha bisogno del tuo intervento. Ogni fonte è una riga: indica come funziona (Connessa, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo aiuto) e cosa è arrivato di recente. Toccala per aprire la scheda e **Dettagli**.

Una sincronizzazione non riuscita, recuperata da quella successiva, viene mostrata in grigio. Solo un errore ancora presente nell'ultima sincronizzazione viene mostrato come problema, insieme all'orario del prossimo tentativo.

I conteggi mostrano tutto quello che ha importato, anche la [cronologia](history.md), quello che è arrivato nelle ultime 24 ore e quello che non è ancora stato controllato. Per un calendario, viene conteggiato il numero di eventi.

Ogni fonte prende il nome dal relativo account, secondo le convenzioni del servizio: il tuo indirizzo, un profilo X, un'area di lavoro Slack o la persona a cui appartiene l'account Signal o Telegram. Sotto il nome trovi prima **Lavoro** o **Personale**, poi l'indirizzo o il nome utente, se non è già indicato nel nome. Se due fonti della stessa categoria hanno lo stesso nome, viene aggiunto un dettaglio che le distingue, come Slack o X, oppure l'indirizzo dell'area di lavoro.

Ogni fonte indica anche, in una riga, cosa importa e, se può eseguire azioni, che lo fa solo dopo che premi **Invia** o dai l'OK.

## Aggiungere una fonte

Apri una categoria (**Email**, **Calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**) e scegli una fonte sotto **Aggiungine un altro**, oppure sotto l'elenco se non ne hai ancora collegata nessuna. In fondo trovi un'opzione generica: **Altra email** sotto Email, **Link del calendario (ICS)** e **Altro calendario** sotto Calendario. Exchange Server importa le riunioni, quindi si trova sotto Calendario.

**Suggerito per te** appare in cima a **Connessioni** quando la tua Machine rileva un motivo per aggiungere una fonte. Il motivo è indicato in una riga: email da Stripe, riunioni Zoom nel tuo calendario, messaggi con link a Google Docs o una configurazione non completata. La fonte resta anche nel suo gruppo, contrassegnata come **Suggerito**. La tua Machine esegue questi conteggi al suo interno: non viene inviato nulla all'esterno. Una fonte già connessa non viene mai suggerita.

Microsoft Teams appare due volte: sotto **Chat** per le chat e sotto **Riunioni** come **Riunioni Teams** per le note delle riunioni. Entrambe usano lo stesso accesso Microsoft, quindi collegandone una si collega anche l'altra.

Nell'elenco, le fonti che hai già collegato sono contrassegnate come tali e riportano il relativo account. Selezionale per aggiungerne un'altra accanto: il modulo lo specifica e include un link a quella che hai già.

Inserisci i dati richiesti (una chiave, un indirizzo), scegli **Lavoro** con il nome dell'azienda oppure **Personale** (per email e calendari ti viene chiesto solo se l'indirizzo non basta a capirlo) e premi **Collegati**. Se si tratta di un sito come LinkedIn o X, si apre la pagina di accesso nel browser della tua Machine e la procedura continua automaticamente una volta effettuato l'accesso. GitHub, WhatsApp e Codex mostrano un codice da inserire; le chat Telegram e Signal mostrano un codice QR da scansionare.

Premi **Annulla** per interrompere l'aggiunta. Hai chiuso la procedura prima di finirla? Riapri **Connessioni** da qualsiasi dispositivo e riprenderai dallo stesso punto. Una volta collegata, la tua Machine inizia subito a leggerla e mostra l'andamento della prima sincronizzazione.

Su una Machine ospitata, puoi accedere direttamente qui alle fonti che richiedono un accesso dedicato: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Scegli **Lavoro** o **Personale** e premi il pulsante di accesso, ad esempio **Accedi con Google**. Tornerai a questo modulo, che mostra l'esito della procedura. Qui vengono mostrati anche i codici di GitHub, WhatsApp, Codex, le chat Telegram e il tuo telefono Android.

Sul tuo computer, per accedere alle stesse fonti devi prima abbinare la tua Machine al tuo account: la prima volta premi **Abbina questa Machine**. Alcune fonti offrono anche un altro metodo, ad esempio un'app o una chiave personale.

Premendo **Riconnetti** su una fonte o in **Serve il tuo intervento** si apre lo stesso modulo. Sul tuo computer, `assistant connect` fa la stessa cosa da un terminale.

## Lavoro o personale

Ogni fonte è classificata come lavorativa (per un'azienda che indichi) o personale. Puoi cambiarne la categoria in **Dettagli**. **Dedotto** indica che la tua Machine l'ha scelta in base all'indirizzo. Le attività di lavoro aspettano i tuoi giorni lavorativi.

Per le email e i calendari Google e Microsoft, la categoria viene dedotta dall'indirizzo quando è chiaro: un servizio di posta come Gmail o Outlook.com è **Personale**, mentre il dominio della tua azienda è **Lavoro**. Altrimenti ti viene chiesto una volta sola, subito dopo l'accesso. Con **Cambia** puoi impostarla tu. Se in seguito le email indicano l'altra categoria, l'attività **Ottieni di più da The Machine** ti chiede una volta sola se vuoi cambiarla.

## Funzionalità

Una fonte può importare segnali (quello che arriva diventa un'attività), svolgere azioni per le tue attività (leggere un documento, inviare o rispondere a un messaggio oppure modificare qualcosa dopo il tuo OK) o fare entrambe le cose. Se fa entrambe le cose, in **Dettagli** trovi un interruttore per ciascuna: **Porta segnali** e **Può fare cose**. Almeno una delle due opzioni resta attiva. Per disattivarle entrambe, disconnetti la fonte. Una chat ha solo l'opzione **Può fare cose**.

Se **Porta segnali** è disattivato, la fonte non si sincronizza. Se **Può fare cose** è disattivato, la tua Machine non legge, prepara bozze o modifica nulla con quella fonte.

## Rimuovere una fonte

Apri la fonte, vai su **Dettagli** e premi **Disconnetti**. La fonte smette di essere letta. Quello che ha già importato resta. Su una Machine ospitata, per le fonti il cui accesso è gestito dalla pagina di configurazione (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) appare **Disconnetti ↗**, che apre la pagina di configurazione.

**Disconnesso di recente** elenca gli account Google, Microsoft, Zoom, Slack, Stripe e Salesforce che hai rimosso negli ultimi 30 giorni, con la data. In attesa di conferma da parte del servizio, compare lo stato In attesa e il tentativo continua. Un account Google appare una sola volta, anche quando Google Meet o Docs aveva un accesso separato. Ogni account appare nella sua categoria: un account Google o Microsoft sotto **Email**, Slack sotto **Chat**.

## Accessi salvati

Per i siti come LinkedIn o X, seleziona **Salva per la prossima volta** quando accedi. Poi li trovi in **Accessi** e, quando un sito disconnette la tua Machine, puoi farla accedere di nuovo con un tocco. Le password restano criptate sulla tua Machine. Premi **Dimentica** per rimuovere un accesso.

Un sito può avere più account, ad esempio **Lavoro** e **Personale**. **Salva come** propone la categoria dell'attività. Con **Altro nome…** puoi inserire un nome personalizzato. Un'attività accede con l'account più adatto. Se non è chiaro quale usare, la finestra di dialogo ti chiede una volta quale scegliere e ricorda la scelta per quell'attività.

**Accessi** elenca ogni sito una sola volta, con i relativi account sotto: il nome utente e un menu con la categoria. Puoi cambiarla in qualsiasi momento da quel menu. Gli accessi salvati prima che fossero disponibili più account mostrano **Lavoro o personale?** finché non ne scegli una. Se cambi la categoria di un accesso usato da un'attività, l'attività ti chiede di nuovo quale usare.

Con **Importa** puoi importare gli accessi da un gestore di password. Scegline uno:

- **LastPass**, **Bitwarden** o **Google Password Manager**: nel browser della tua Machine si apre la pagina di esportazione del servizio, direttamente nella finestra di dialogo, come quando usi **Fallo** per un'attività. Accedi lì e la tua Machine prosegue fino all'esportazione. Una riga indica cosa devi ancora fare, ad esempio inserire la password principale. Sul telefono la pagina si ingrandisce nel punto in cui devi digitare. Se la pagina è diversa da quella prevista, vengono mostrate le istruzioni per completare la procedura manualmente. La tua Machine recupera il file, lo legge una volta e lo elimina.
- **1Password**: esporta un CSV dall'app 1Password su un computer, poi seleziona il file. Se `op` di 1Password è collegato alla tua Machine, importa i dati direttamente da lì (lo stesso vale per `lpass` di LastPass).
- **Da un file esportato**: un CSV di 1Password, LastPass, Bitwarden o Chrome. Eliminalo quando hai finito.

Poi seleziona gli accessi da conservare. La tua Machine non accede mai al tuo gestore di password, non inserisce né legge la password principale e non mostra la pagina all'assistente: inserisci tu la password direttamente nella pagina.

Un accesso salvato viene usato solo per il suo indirizzo web: lo stesso sito, `https` e la stessa porta. Non viene usato per un indirizzo simile né per un altro sottodominio.

## Controlli

**Controlli** mostra come la tua Machine legge i contenuti in arrivo: i controlli recenti e cosa ha trovato ciascuno. Consulta [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha un articolo dedicato in questa sezione, che spiega cosa legge e cosa può inviare.
