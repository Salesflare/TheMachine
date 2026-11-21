---
title: Connessioni
area: connections
summary: Tutte le tue fonti in un unico posto: controlla come funzionano, aggiungine una o disconnettila.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 38d682b69cab758d
---
## Come funzionano

La scheda **Connessioni** mostra le tue fonti divise per tipo, con **Accessi** e **Controlli** in fondo, sotto una linea. Sul telefono, tocca un tipo per aprirlo e **Connessioni** per tornare indietro. Si apre per prima la categoria che contiene una fonte che richiede il tuo intervento. Ogni fonte è una riga che indica come funziona (Connessa, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo aiuto) e cosa ha acquisito di recente. Tocca la riga per aprire la scheda della fonte e **Dettagli**.

Una sincronizzazione non riuscita, ma recuperata da quella successiva, appare in grigio. Viene segnalato come problema solo un errore che è ancora il più recente, con l’indicazione di quando verrà fatto un nuovo tentativo.

I conteggi mostrano tutto ciò che la fonte ha acquisito, compresa la [cronologia](history.md), cosa è arrivato nelle ultime 24 ore e cosa non è ancora stato controllato. Per i calendari viene conteggiato il numero di eventi.

Ogni fonte prende il nome dal relativo account, così come lo identifica il servizio: il tuo indirizzo, un profilo X, uno spazio di lavoro Slack oppure la persona a cui appartiene l’account Signal o Telegram. Sotto il nome trovi prima **Lavoro** o **Personale**, poi l’indirizzo o il nome utente, se non è già incluso nel nome. Se due fonti dello stesso tipo hanno lo stesso nome, viene indicato anche ciò che le distingue, come Slack o X oppure l’indirizzo dello spazio di lavoro.

Ogni fonte spiega anche in una riga cosa acquisisce e, se può eseguire operazioni, che agirà solo dopo che avrai premuto **Invia** o dato l’autorizzazione.

## Aggiungere una fonte

Apri un tipo (**Email**, **Calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**) e scegli una fonte sotto **Aggiungine un altro**, oppure sotto l’elenco se non ne hai ancora connesse. In fondo trovi le opzioni generiche: **Altra email** sotto Email, **Link del calendario (ICS)** e **Altro calendario** sotto Calendario. Exchange Server acquisisce le riunioni, quindi lo trovi sotto Calendario.

Quando la tua Machine riconosce un motivo per aggiungere una fonte, sopra **Connessioni** compare **Suggerito per te**, con una breve spiegazione: email da Stripe, riunioni Zoom nel tuo calendario, messaggi con link a Google Docs oppure una configurazione non completata. La fonte resta anche nel suo gruppo, contrassegnata come **Suggerito**. Questi elementi vengono conteggiati sulla tua Machine e non escono da lì. Una fonte connessa non viene mai suggerita.

Microsoft Teams compare in due punti: sotto **Chat** per le chat e sotto **Riunioni** come **Riunioni Teams** per gli appunti delle riunioni. Entrambe le opzioni usano lo stesso accesso Microsoft, quindi connettendone una si connette anche l’altra.

Se hai già connesso una fonte, nell’elenco compare il relativo account. Selezionala per aggiungerne un’altra accanto: il modulo lo specifica e include un link a quella già connessa.

Inserisci le informazioni richieste, come una chiave o un indirizzo, scegli **Lavoro** con il nome dell’azienda oppure **Personale** (per email e calendari ti viene chiesto solo se l’indirizzo non basta a capirlo) e premi **Collegati**. Per siti come LinkedIn o X, si apre la pagina di accesso nel browser della tua Machine e la procedura continua da sola una volta effettuato l’accesso. GitHub, WhatsApp e Codex mostrano un codice da inserire; le chat di Telegram e Signal mostrano un codice QR da scansionare.

Premi **Annulla** per interrompere l’aggiunta. Se hai chiuso prima di completarla, riapri **Connessioni** da qualsiasi dispositivo e riprenderai dallo stesso passaggio. Una volta connessa, la tua Machine inizia subito a leggerla e mostra lo stato della prima sincronizzazione.

Su una Machine ospitata, puoi accedere direttamente qui alle fonti che richiedono un accesso dedicato: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Scegli **Lavoro** o **Personale** e premi il pulsante di accesso, per esempio **Accedi con Google**. Tornerai a questo modulo, che ti mostrerà com’è andata. Qui vengono mostrati anche i codici di GitHub, WhatsApp, Codex, le chat di Telegram e il tuo telefono Android.

Sul tuo computer, le stesse fonti richiedono l’accesso dopo aver associato la tua Machine al tuo account: la prima volta premi **Abbina questa Machine**. Alcune offrono anche un’altra modalità, per esempio tramite la tua app o una chiave.

Premendo **Riconnetti** su una fonte oppure in **Serve il tuo intervento** si apre lo stesso modulo. Sul tuo computer, `assistant connect` fa la stessa cosa dal terminale.

## Lavoro o personale

Ogni fonte è classificata come di lavoro (per un’azienda che indichi) o personale. Puoi modificarla da **Dettagli**. **Indovinato** indica che la tua Machine l’ha dedotto dall’indirizzo. Le attività di lavoro aspettano i tuoi giorni lavorativi.

Per le email e i calendari Google e Microsoft, la categoria viene dedotta dall’indirizzo, se è chiaro: un servizio email come Gmail o Outlook.com è Personale, mentre il dominio della tua azienda è Lavoro. In caso contrario, ti viene chiesto una volta sola, subito dopo l’accesso. Premi **Cambia** per impostarla tu. Se in seguito le email indicano l’altra categoria, l’attività **Ottieni di più da The Machine** ti chiederà una volta se vuoi cambiarla.

## Funzionalità

Una fonte può acquisire segnali (che diventano attività), eseguire operazioni per le tue attività (leggere un documento oppure inviare, rispondere o modificare qualcosa dopo la tua approvazione) o fare entrambe le cose. Se fa entrambe le cose, in **Dettagli** trovi un interruttore per ciascuna: **Porta segnali** e **Può fare cose**. Uno dei due deve restare attivo. Per disattivarli entrambi, disconnetti la fonte. Una chat ha solo **Può fare cose**.

Con **Porta segnali** disattivato, la fonte non si sincronizza. Con **Può fare cose** disattivato, la tua Machine non la legge, non crea bozze e non apporta modifiche.

## Rimuovere una fonte

Apri la fonte, seleziona **Dettagli**, poi **Disconnetti**. La tua Machine smette di leggerla, ma conserva ciò che ha già acquisito. Su una Machine ospitata, per le fonti il cui accesso è gestito dalla pagina di configurazione (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) appare **Disconnetti ↗**, che apre quella pagina.

**Disconnesso di recente** mostra gli account Google, Microsoft, Zoom, Slack, Stripe e Salesforce che hai rimosso negli ultimi 30 giorni e la data della rimozione. Finché il servizio non la conferma, la richiesta resta in attesa e viene riprovata. Un account Google compare una sola volta, anche se Google Meet o Docs avevano un proprio accesso. Ogni account compare sotto il suo tipo: un account Google o Microsoft sotto **Email**, Slack sotto **Chat**.

## Accessi salvati

Per siti come LinkedIn o X, seleziona **Salva per la prossima volta** quando accedi. Poi li trovi in **Accessi** e, quando un sito disconnette la tua Machine, puoi farle accedere di nuovo con un solo tocco. Le password restano crittografate sulla tua Machine. **Dimentica** rimuove un accesso salvato.

Un sito può avere più account, per esempio **Lavoro** e **Personale**. **Salva come** propone per prima la categoria dell’attività; con **Altro nome…** puoi scegliere un nome personalizzato. Un’attività accede con l’account più adatto. Se non è chiaro quale usare, una finestra di dialogo ti chiede una volta quale scegliere e memorizza la scelta per quell’attività.

In **Accessi** ogni sito compare una volta, con i relativi account sotto: il nome utente e un menu con la categoria. Puoi cambiarla quando vuoi da quel menu. Gli accessi salvati prima che fossero disponibili gli account mostrano **Lavoro o personale?** finché non scegli una categoria. Se cambi la categoria, l’attività che usava quell’accesso ti chiederà di scegliere di nuovo.

Con **Importa** puoi importare gli accessi da un gestore di password. Scegline uno:

- **LastPass**, **Bitwarden** o **Google Password Manager**: la pagina di esportazione si apre nel browser della tua Machine. Accedi e la tua Machine avvierà l’esportazione. Una riga ti indica cosa resta da fare, per esempio inserire la password principale. Sul telefono, la schermata si ingrandisce sul campo in cui devi scrivere. Se la pagina è diversa da quella prevista, vengono mostrate le istruzioni per completare l’operazione a mano. La tua Machine acquisisce il file, lo legge una volta e lo elimina.
- **1Password**: esporta un file CSV dall’app 1Password su un computer, poi seleziona quel file. Se `op` di 1Password ha già effettuato l’accesso sulla tua Machine, gli accessi vengono letti direttamente da lì (anche per `lpass` di LastPass).
- **Da un file esportato**: un file CSV di 1Password, LastPass, Bitwarden o Chrome. Eliminalo una volta terminata l’operazione.

Poi seleziona gli accessi da conservare. La tua Machine non accede mai al tuo gestore di password al posto tuo, non inserisce né legge la password principale e non mostra la pagina all’assistente. La password nella pagina la inserisci tu.

Un accesso salvato viene usato solo per il suo indirizzo web: lo stesso sito, `https` e la stessa porta. Non viene usato per un indirizzo simile o per un altro sottodominio.

## Controlli

**Controlli** mostra come la tua Machine legge ciò che arriva: i controlli recenti e i risultati di ciascuno. Vedi [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha un articolo dedicato in questa sezione, con i dettagli su cosa legge e cosa può inviare.
