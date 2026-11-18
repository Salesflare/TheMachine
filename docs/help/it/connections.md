---
title: Connessioni
area: connections
summary: Tutte le tue fonti in un unico posto: controlla come va ciascuna, aggiungine una o disconnettila.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 809547189ccfa026
---
## Come stanno andando

La scheda **Connessioni** elenca le tue fonti per categoria, con **Accessi** e **Controlli** sotto una linea. Sul telefono, tocca una categoria per aprirla e **Connessioni** per tornare indietro. Si apre per prima la categoria con una fonte che richiede il tuo intervento. Ogni fonte è una riga: indica come sta andando (Connessa, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo aiuto) e cosa è arrivato di recente. Tocca una fonte per aprire la relativa scheda e **Dettagli**.

Una sincronizzazione non riuscita, recuperata da una successiva, viene mostrata in grigio. Solo un errore che è ancora il più recente viene segnalato come problema, insieme a quando verrà fatto un nuovo tentativo.

I conteggi mostrano tutto ciò che la fonte ha importato, compresa la [cronologia](history.md), quello che è arrivato nelle ultime 24 ore e ciò che non è ancora stato controllato. Per un calendario si contano gli eventi.

Ogni fonte prende il nome dal relativo account, secondo il nome usato dal servizio: il tuo indirizzo, un profilo X, un’area di lavoro Slack o la persona a cui appartiene l’account Signal o Telegram. Sotto il nome compare prima **Lavoro** o **Personale**, poi l’indirizzo o il nome utente, se non è già indicato nel nome. Se due fonti della stessa categoria hanno lo stesso nome, viene aggiunto un dettaglio che le distingue, come Slack o X, oppure l’indirizzo dell’area di lavoro.

Ogni fonte indica anche in una riga cosa importa e, se può eseguire azioni, che agisce solo dopo che premi **Invia** o dai la tua approvazione.

## Aggiungere una fonte

Apri una categoria (**Email**, **Calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**) e scegli una fonte sotto **Aggiungine un altro**, oppure sotto l’elenco se non ne hai ancora connesse. In fondo trovi un’opzione generica: **Altra email** sotto Email, **Link del calendario (ICS)** e **Altro calendario** sotto Calendario. Exchange Server importa le riunioni, quindi si trova sotto Calendario.

**Suggerito per te** compare in cima a **Connessioni** quando la tua Machine rileva un motivo per aggiungere una fonte. Il motivo è indicato in una riga: email da Stripe, riunioni Zoom sul calendario, messaggi con link a Google Docs o una configurazione non completata. La fonte resta anche nel suo gruppo, contrassegnata come **Suggerito**. Questi conteggi vengono calcolati sulla tua Machine: non esce nulla da lì. Una fonte connessa non viene mai suggerita.

Microsoft Teams compare due volte: sotto **Chat** per le chat e sotto **Riunioni** come **Riunioni Teams** per le note delle riunioni. Entrambe usano lo stesso accesso Microsoft, quindi connettendone una si connette anche l’altra.

Nell’elenco, le fonti che hai già connesso sono indicate insieme al relativo account. Selezionale per aggiungerne un’altra accanto: il modulo te lo segnala e include un link a quella già connessa.

Inserisci i dati richiesti, come una chiave o un indirizzo, scegli **Lavoro** con il nome dell’azienda oppure **Personale** (per email e calendari viene chiesto solo se l’indirizzo non basta a stabilirlo) e premi **Collegati**. Per un sito come LinkedIn o X, si apre la pagina di accesso nel browser della tua Machine e la procedura continua da sola dopo l’accesso. GitHub, WhatsApp e Codex mostrano un codice da inserire; per le chat di Telegram e Signal, invece, un codice QR da scansionare.

**Annulla** interrompe l’aggiunta. Se hai lasciato la procedura prima di terminarla, riapri **Connessioni** da qualsiasi dispositivo: riprenderà dallo stesso passaggio. Una volta connessa, la tua Machine inizia subito a leggerla e mostra come procede la prima sincronizzazione.

Su una Machine ospitata, accedi direttamente da qui alle fonti che hanno una propria procedura di accesso: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Scegli **Lavoro** o **Personale** e premi il pulsante di accesso, per esempio **Sign in with Google**. Tornerai a questo modulo, che ti mostrerà l’esito. Anche GitHub, WhatsApp, Codex, le chat di Telegram e il tuo telefono Android mostrano qui il codice.

Sul tuo computer, le stesse fonti permettono di accedere dopo aver abbinato la tua Machine al tuo account: la prima volta premi **Abbina questa Machine**. Alcune hanno anche un altro metodo, come un’app personale o una chiave.

**Riconnetti**, sulla fonte o in **Serve il tuo intervento**, apre lo stesso modulo. Sul tuo computer, `assistant connect` fa lo stesso in un terminale.

## Lavoro o personale

Ogni fonte è considerata di lavoro, per un’azienda che indichi, oppure personale. Puoi modificarlo in **Dettagli**. **Indovinato** significa che la tua Machine lo ha dedotto dall’indirizzo. Le attività di lavoro aspettano i tuoi giorni lavorativi.

Per le email e i calendari Google e Microsoft, la categoria viene dedotta dall’indirizzo quando è chiaro: un provider email come Gmail o Outlook.com è personale, il dominio del tuo team è di lavoro. Altrimenti ti viene chiesto una volta, subito dopo l’accesso. **Cambia** ti permette di impostarla manualmente. Se in seguito le email indicano l’altra categoria, l’attività **Ottieni di più da The Machine** ti chiederà una volta se vuoi cambiarla.

## Funzionalità

Una fonte può importare segnali, che diventano attività, eseguire azioni per le tue attività (leggere un documento o inviare, rispondere o modificare qualcosa dopo la tua approvazione), oppure fare entrambe le cose. Se fa entrambe le cose, in **Dettagli** trovi un interruttore per ciascuna: **Porta segnali** e **Può fare cose**. Uno dei due deve restare attivo: per disattivarli entrambi, disconnetti la fonte. Una chat ha solo **Può fare cose**.

Se **Porta segnali** è disattivato, la fonte non si sincronizza. Se **Può fare cose** è disattivato, la tua Machine non legge, prepara bozze o modifica nulla usando quella fonte.

## Rimuovere una fonte

Apri la fonte, poi **Dettagli** e **Disconnetti**. La fonte smette di essere letta, ma ciò che ha già importato resta. Su una Machine ospitata, per una fonte il cui accesso è gestito dalla pagina di configurazione (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce), compare **Disconnetti ↗**. Apre la pagina di configurazione.

**Disconnesso di recente** elenca gli account Google, Microsoft, Zoom, Slack, Stripe e Salesforce che hai rimosso negli ultimi 30 giorni, con la data della rimozione. Finché il servizio non conferma, viene mostrato «In attesa» e la Machine continua a riprovare. Un account Google viene mostrato una sola volta, anche se Google Meet o Docs avevano un accesso separato. Ogni account compare nella propria categoria: un account Google o Microsoft sotto **Email**, Slack sotto **Chat**.

## Accessi salvati

Per siti come LinkedIn o X, seleziona **Salva per la prossima volta** quando accedi. Gli account compariranno in **Accessi** e, se un sito disconnette la tua Machine, potrai accedere di nuovo con un tocco. Le password restano crittografate sulla tua Machine. **Dimentica** rimuove un account.

Un sito può avere più account, per esempio **Lavoro** e **Personale**. **Salva come** seleziona inizialmente la categoria dell’attività, mentre **Altro nome…** ti permette di assegnare un nome personalizzato. Un’attività accede con l’account più adatto. Se non è chiaro quale usare, una finestra ti chiede una volta quale scegliere e memorizza la scelta per quell’attività.

**Accessi** mostra una sola voce per ogni sito, con i relativi account sotto: il nome utente e un menu con la categoria. Puoi cambiarla dal menu in qualsiasi momento. Gli accessi salvati prima che fossero disponibili gli account mostrano **Lavoro o personale?** finché non ne scegli una. Se cambi la categoria, l’attività che usava quell’accesso la seleziona di nuovo.

**Importa** aggiunge gli accessi da un gestore di password. Scegline uno:

- **LastPass**, **Bitwarden** o **Google Password Manager**: si apre la pagina di esportazione nel browser della tua Machine. Accedi ed esporta da lì: trovi i passaggi accanto al servizio. La tua Machine individua il file, lo legge una volta e lo elimina.
- **1Password**: esporta un CSV dall’app 1Password su un computer, poi scegli il file. Se `op` di 1Password è connesso alla tua Machine, gli accessi vengono letti direttamente da lì (lo stesso vale per `lpass` di LastPass).
- **Da un file esportato**: un CSV di 1Password, LastPass, Bitwarden o Chrome. Eliminalo quando hai finito.

Poi seleziona gli accessi da conservare. La tua Machine non accede mai al gestore di password al posto tuo e non ti chiede la password principale: la inserisci tu nella pagina.

Un accesso salvato viene usato solo per il suo indirizzo web: lo stesso sito, `https` e la stessa porta. Non viene usato per un indirizzo simile o per un altro sottodominio.

## Controlli

**Controlli** mostra come la tua Machine legge ciò che arriva: i controlli recenti e cosa ha trovato ciascuno. Vedi [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha un articolo dedicato in questa sezione, con cosa legge e cosa può inviare.
