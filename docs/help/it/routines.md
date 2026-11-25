---
title: Routine
area: cards
summary: Attività che la tua Machine svolge da sola, con regolarità, come un riepilogo del lunedì sulle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 3b0405616881de74
---
## Creane una

Apri **Routine** nella barra laterale e scrivi in una riga cosa deve fare e quando: «ogni lunedì alle 9, riepiloga le trattative aperte» oppure «ogni mattina nei giorni feriali, elenca le email a cui devo ancora rispondere». Poi tocca **Aggiungi**.

Se non indichi un orario, la routine viene eseguita alle 8:00. L’orario si basa sull’ora della tua Machine. La prima esecuzione le assegna un nome breve.

Prima, **Aggiungi** esegue una prova, così puoi vedere il risultato prima di conservarla. Non viene inviato né salvato nulla. Poi **Aggiungi** la mantiene attiva con la frequenza scelta, **Cambia** prova altre parole o un nuovo nome e **Annulla** la elimina.

## Modelli

In fondo a Routine, nella sezione **Modelli**, tocca **Aggiungi** per attivare una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30. Pulizia spam viene eseguita ogni ora, Occasioni di seconda mano ogni 3 ore e Abbonamenti e prove una volta al mese. La scheda mostra le parole usate, come per qualsiasi routine, e **Modifica** permette di cambiarle o di cambiarne il nome.

Quando ricevi molte newsletter e Pulizia newsletter è disattivata, ovvero 25 o più in una settimana da almeno 5 mittenti, sopra le tue attività compare una riga con il numero ricevuto e cosa farebbe la routine, con **Attiva** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo quando in una settimana hai spostato manualmente nello spam almeno 5 email. **Attiva** la aggiunge proprio come **Aggiungi** qui. Se tocchi **No, grazie**, non verrà più proposta. Lo stesso vale per un modello che avevi già usato.

**Pulizia newsletter** crea un’attività per ogni area, lavoro e personale, con le newsletter ricevute nell’ultimo giorno. Per ognuna puoi scegliere **Tieni** o **Disiscriviti**. Per disiscriverti, la routine usa il link diretto nell’email oppure invia un’email di disiscrizione dal tuo indirizzo, se l’invio è attivo. Altrimenti, The Machine si disiscrive dalla pagina della lista usando il proprio browser. Se devi accedere, completare un captcha o fare una scelta, tocca **Apri la pagina di disiscrizione** per vedere il motivo indicato nella riga.

Se non vuoi attività da una lista, ma vuoi continuare a ricevere le sue email, scrivi «Da questa lista non serve creare attività» nella chat di una delle email.

Le ricevute, gli ordini e gli avvisi di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come un Google Group, vengono elencate sotto il nome di chi le ha scritte e non ti disiscrivono mai dal gruppo. Se il mittente non ha un’opzione per disiscriversi, nella riga trovi **Disiscriviti a mano**.

**Pulizia spam** crea un’attività per ogni area con le email di mittenti sconosciuti che sembrano spam. Per ciascuna puoi scegliere **Spam** o **Non è spam**. Outlook sposta lo spam nella cartella Posta indesiderata, mentre Gmail lo contrassegna come spam. La routine controlla ogni ora, quindi di solito lo spam viene rilevato prima che tu lo veda. Quando l’attività è ancora aperta, il nuovo spam viene aggiunto alla stessa attività.

Se Gmail è collegato in sola lettura, come su una Machine ospitata, non è possibile spostare le email nello spam. In questo caso, **Spam** mostra un link per contrassegnare l’email come spam in Gmail e The Machine ricorda che il mittente è spam. Se non hai collegato un account email, al posto di **Aggiungi** il modello mostra **Collega la posta**.

Un mittente è sconosciuto se non gli hai mai scritto. Un «Re:» conta come conversazione solo in una discussione a cui hai partecipato. Se ricevi di nuovo un’email da un mittente che hai contrassegnato come spam, nell’attività o nella tua casella di posta, la prossima attività riporta **Già segnato come spam**. Anche le email che sposti tu nello spam aiutano la routine a riconoscerne di simili.

Non cambia nulla finché non confermi nell’attività. Tocca il mittente per leggere prima l’email: rimane non letta e non cambia nulla. Con Pulizia spam, le immagini dal web non vengono caricate, così il mittente non può sapere che l’hai aperta. Non ti verrà chiesto di nuovo cosa fare con i mittenti per cui hai già scelto. Se in un giorno non ci sono newsletter o spam, non viene creata alcuna attività. Queste attività non inviano mai notifiche.

Quando hai scelto cosa fare per tutti i mittenti, l’attività risulta completata e mostra **Segna come completata**.

**Riepilogo giornaliero** seleziona una volta al giorno, in un’unica attività, le poche newsletter che vale la pena leggere. Ogni elemento spiega in una riga perché è rilevante per te. Toccalo per leggere l’email oppure usa **Apri nella tua posta**. La routine considera solo le newsletter, mai le email di altre persone, le ricevute o le email di mittenti da cui ti sei disiscritto, e mai quelle che hai già letto. Se non trova nulla di interessante, non crea un’attività.

La routine impara cosa ti interessa da ciò che apri, contrassegni con una stella o archivi senza leggere, oltre che dalle opzioni **Altri così** e **Meno così** su ogni selezione. Gli argomenti che usa per scegliere sono nella scheda della routine, sotto **Più su** e **Meno su**. Rimuovi un argomento con × oppure aggiungine uno. Quelli tratteggiati sono stati individuati dalla routine. Un nuovo riepilogo sostituisce quello ancora aperto e non invia mai notifiche.

La routine legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter, poi pone alla tua IA una breve domanda su ciascuna, rispettando un limite giornaliero per contenere i costi. **Cambia quando** permette di impostare l’orario. Se modifichi le parole usate, la routine funziona come qualsiasi altra e segue le tue istruzioni.

**Compleanni** crea un’attività per ogni contatto stretto che compie gli anni oggi: persone a cui scrivi direttamente, come amici, familiari e contatti abituali. Per ognuno prepara un breve messaggio di auguri nel canale che usi di solito, per esempio nella chat WhatsApp o nella conversazione email, nella lingua della persona. Il messaggio viene inviato solo quando lo invii tu. Se non ci sono compleanni quel giorno, non viene creata alcuna attività.

I compleanni provengono dai tuoi calendari: gli eventi e il calendario Compleanni di Google, letti ogni mattina anche se non sono sincronizzati, e il calendario Compleanni di Outlook. Possono provenire anche dai tuoi contatti Google su una Machine self-hosted e da un campo data chiamato Birthday su una persona nel Graph. Se non è ancora presente alcuna data di compleanno, il risultato mostra **Nessun compleanno trovato** e spiega come aggiungerne uno.

**Importa i compleanni da Facebook**: dopo aver attivato Compleanni, un’attività ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e The Machine apre la pagina nel proprio browser, scorre finché non ha caricato tutti i mesi e legge il nome e il compleanno di ogni amico. Ti mostra quanti ne ha trovati e quali corrispondono a persone nel tuo Graph in base a nome e cognome. Se più persone hanno lo stesso nome, vengono ignorate e indicate nell’elenco.

Solo **Salva** li aggiunge, nella pagina di ogni persona: la data del compleanno e, se la persona non ha ancora una foto, la sua immagine del profilo Facebook. La data o la foto che imposti qui rimangono, e una foto già presente non viene mai sostituita. Non viene scritto nulla su Facebook.

La routine non rilegge la pagina da sola: per farlo, tocca **Importa di nuovo** nell’attività. Il browser deve avere una sessione Facebook attiva. Se non ce l’ha, tocca **Accedi a Facebook** nell’attività e accedi da lì. Una volta effettuato l’accesso, la routine legge la pagina automaticamente. The Machine non accede mai al tuo posto.

Le persone che non sono nel tuo Graph vengono conteggiate e ne vengono mostrati alcuni nomi. **Aggiungi … come contatti personali** le aggiunge tutte insieme, anche dopo aver toccato Salva. Per ciascuna vengono aggiunti nome e compleanno, senza condividerli mai con una Fleet di lavoro. Vengono ignorate le persone con un nome già presente nel tuo Graph e quelle che avevi eliminato definitivamente. I promemoria dei compleanni continuano ad arrivare solo per le persone a cui scrivi.

Toccando **Annulla** nell’attività, rimuovi esattamente le persone aggiunte, anche dopo aver usato **Importa di nuovo**.

**Abbonamenti e prove** legge una volta al mese le ricevute, le fatture e gli avvisi di rinnovo, poi raccoglie gli abbonamenti in un’unica attività: quanto costa ciascuno, la prossima data di addebito e un avviso se una prova sta per finire o il prezzo aumenta. Elenca solo gli abbonamenti che riesce a identificare con certezza. Se non ne trova, non crea un’attività.

Per ciascuno, scegli **Tieni** o **Disdici**. Non ti verrà chiesto di nuovo cosa fare per un abbonamento che hai deciso di tenere, a meno che il prezzo non cambi. **Disdici** mostra la pagina per annullare l’abbonamento oppure prepara un messaggio con cui chiedere di annullarlo. Il messaggio viene inviato solo quando lo invii tu. Tra un controllo mensile e l’altro, la routine verifica ogni giorno e crea un’attività quando un addebito di prova o di rinnovo è previsto entro 7 giorni.

**Restare in contatto** ti ricorda ogni tanto di farti sentire con una persona a cui tieni, ma solo quando c’è un motivo concreto. Nella scheda scegli chi includere da un breve elenco di persone con cui scrivi direttamente da mesi, in entrambe le direzioni. Rimuovi una persona con ×.

Ricevi un promemoria solo quando è passato molto più tempo del solito dall’ultima conversazione e c’è qualcosa di preciso da dire: una notizia che la persona ha condiviso, una promessa ancora da mantenere o un messaggio a cui non hai mai risposto. La routine crea un’unica attività con il motivo e un breve messaggio, preparato nel canale che usi di solito e nella lingua della persona. Il messaggio viene inviato solo quando lo invii tu. Se non c’è niente da dire, non viene creata alcuna attività.

La routine invia al massimo due promemoria a settimana, uno per persona al mese, e non ne invia a chi hai sentito di recente. Se tocchi **Non serve** su un promemoria, la routine aspetta più a lungo prima di ricordartelo di nuovo per quella persona, e ogni volta aspetta ancora di più. Non invia mai notifiche e rimane personale: non viene mai condivisa con una Fleet di lavoro.

**Occasioni di seconda mano** controlla una ricerca su un sito di articoli usati, come Marktplaats, Vinted, eBay o Facebook Marketplace. Applica i filtri che vuoi sul sito, copia l’indirizzo dei risultati e incollalo dopo aver toccato **Aggiungi**. Se vuoi, aggiungi filtri con parole tue, per esempio «meno di 300, entro 30 km, niente “per pezzi di ricambio”». Ogni ricerca ha una routine separata, quindi per aggiungerne un’altra devi ripetere la procedura.

Ogni 3 ore la routine apre la ricerca nel browser di The Machine e controlla se ci sono annunci che non ha ancora visto. Prima verifica prezzo, distanza e parole da escludere, usando codice semplice.

Apre ogni nuovo annuncio che soddisfa i criteri e la tua IA valuta le condizioni dell’articolo in base alla foto e alla descrizione, e il venditore in base alle recensioni, alla valutazione e all’età dell’account. Gli annunci interessanti vengono raccolti in un’unica attività, con foto, titolo, prezzo e un breve giudizio per ciascuno. Tocca un annuncio per aprirlo nel browser di The Machine.

Quando l’attività è aperta, le nuove occasioni vengono aggiunte in cima, il conteggio aumenta e ricevi di nuovo una notifica, perché le buone occasioni spariscono in fretta. Quando segni l’attività come completata, la prossima occasione ne crea una nuova. Se un controllo non trova nulla di interessante, non cambia nulla.

La routine è progettata per essere leggera e rispettosa: legge la ricerca una volta per esecuzione, apre al massimo 6 annunci per esecuzione, con una pausa tra uno e l’altro, e controlla al massimo 40 annunci al giorno, considerando tutte le tue ricerche. Ogni controllo è una breve domanda alla tua IA con una foto. La prima esecuzione controlla i pochi annunci più recenti e considera già visti gli altri, così quelle successive mostrano solo le novità.

Se il sito ti chiede di accedere, mostra un controllo per verificare che tu non sia un robot o interrompe la lettura, un’attività te lo segnala e ti offre **Apri** per visualizzare la pagina nel browser di The Machine. Accedi o supera il controllo tu stesso da lì; la volta successiva la routine riprova a leggere la pagina. The Machine non accede mai né supera i controlli al posto tuo, e non contatta mai i venditori, non fa offerte e non compra nulla.

**Modifica ricerca** nella scheda della routine permette di inserire un nuovo indirizzo o cambiare i filtri. **Cambia quando** permette di impostare una frequenza diversa, per esempio «ogni 6 ore».

**Riordini** legge le conferme d’ordine dei negozi online nella tua posta e individua gli articoli che compri spesso, come caffè, cibo per animali o vitamine. Quando è probabile che tu debba ricomprarne uno, crea un’attività con il prodotto, il negozio, l’ultimo prezzo e la data dell’ultimo acquisto. **Apri nel negozio** ti porta alla pagina del prodotto, dove puoi acquistarlo tu. La routine non compra nulla al posto tuo.

Servono almeno tre ordini dello stesso prodotto a intervalli regolari, quindi un acquisto occasionale o un intervallo insolito non crea un’attività. Per ora la routine legge solo i negozi che usano Shopify. La tua IA legge solo le nuove email d’ordine di questi negozi, con una breve domanda per ogni esecuzione. Queste attività non inviano mai notifiche. Quando ordini di nuovo il prodotto, l’attività aperta viene chiusa.

Finché la routine di un modello mantiene le istruzioni originali, viene eseguita con il proprio codice, senza usare il tuo piano IA. Pulizia spam, per esempio, elenca prima con il codice le nuove email di mittenti sconosciuti e fa una breve domanda alla tua IA solo se ne trova. Restare in contatto chiede informazioni solo su una o due persone selezionate. Un nuovo nome non cambia questo comportamento. Se modifichi le istruzioni, la routine funziona come qualsiasi altra e segue le tue parole.

Pulizia newsletter e Pulizia spam continuano a creare un’unica attività con una scelta per ogni email. Compleanni, se modificata, mostra il risultato e al massimo una bozza, non un’attività per ogni persona. Tocca **Torna al modello** in **Modifica** per ripristinare le istruzioni originali.

## Cosa fa una routine

All’orario stabilito, la tua Machine legge ciò che le serve, come i messaggi, le riunioni e il Graph, e mostra il risultato nella pagina Routine. Ogni risultato è **Pronta**, **Niente di nuovo** con una spiegazione oppure **Non ha funzionato** con una spiegazione. Se l’esecuzione termina senza un risultato, viene considerata non riuscita, mai completata.

Le routine si limitano a leggere: i tuoi messaggi, le pagine web, GitHub e siti come X nel browser. Non inviano, non rispondono, non pubblicano e non modificano nulla. Aprono le pagine trovate nei contenuti letti o in una ricerca, gli indirizzi web normali e i siti conosciuti, mai un indirizzo inventato per trasmettere ciò che hanno letto. Solo un modello modifica la posta, e solo ciò che confermi nella relativa attività.

Se il lavoro di una routine prevede un post o un messaggio, la routine fa tutto fino a quel passaggio e mostra una bozza, per esempio **Pubblicheresti su X:**. Dopo un’esecuzione reale, la bozza diventa un’attività da approvare. Un’esecuzione di prova la mostra soltanto.

Il nome indica l’argomento e dove verrà pubblicato. Sotto, **Dalla tua routine** apre la routine. Il pulsante indica il passaggio, per esempio **Prepara il post**: prepara il post, ma non lo pubblica. Puoi pubblicarlo dal risultato. Se The Machine non può pubblicarlo al posto tuo, il pulsante apre la pagina in cui puoi farlo.

L’attività viene creata nell’area dell’account da cui partirà, per esempio Lavoro per l’account X della tua azienda, quindi non ti verrà mai chiesto di spostarla.

Un’esecuzione può seguire le tue [skill](skills.md) attive, selezionate in base al compito della routine: vengono lette per intero solo quelle pertinenti. Il risultato le elenca sotto **Usate:**. Una skill non fa mai inviare o modificare nulla a una routine.

Le tue routine si trovano sotto **Le tue routine**, dopo gli eventuali suggerimenti. I risultati lunghi vengono ridotti a un’anteprima breve. Tocca **Mostra altro**, oppure il risultato stesso, per aprirli.

Ogni esecuzione conosce il risultato precedente e può indicare cosa è cambiato da allora.

Dopo un’esecuzione riuscita, la tua Machine può creare da sola una ricetta per le letture che si ripetono sempre, come le email o le modifiche di GitHub da controllare. Le esecuzioni successive le leggono prima con codice semplice, poi l’IA seleziona ciò che conta e lo scrive, usando meno token. Una ricetta si limita a leggere. Se smette di funzionare, la routine torna a leggere autonomamente e la corregge. La ricetta si trova sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine era spenta o occupata, le esecuzioni saltate non si accumulano: ne viene eseguita una sola, la più recente. Ogni data viene eseguita una volta, anche dopo un riavvio.

Le routine vengono eseguite una alla volta e aspettano quando l’utilizzo del tuo piano IA è basso, come tutti i processi in background. **Esegui ora** avvia subito la routine. Quando il risultato è pronto, compare sulla scheda.

## Modificala o fermala

Trovi queste opzioni nel menu ⋯ della routine. **Modifica** cambia il nome e le istruzioni; l’orario di esecuzione e i risultati precedenti rimangono invariati. **Cambia quando** permette di impostare una nuova frequenza con parole tue, per esempio «ogni giorno feriale alle 8». Entrambe le opzioni hanno **Salva** e **Annulla**. Da computer puoi annullare anche con Esc o facendo clic fuori dal menu.

In **Modifica**, **Provalo** esegue una volta le nuove istruzioni e mostra il risultato. La routine rimane invariata finché non tocchi **Salva**.

**Metti in pausa** interrompe le esecuzioni fino a quando non tocchi **Riprendi** sulla scheda. Le routine in pausa si trovano sotto **In pausa**, dopo le tue routine. Le esecuzioni saltate durante la pausa non vengono recuperate. **Ferma** interrompe definitivamente una routine.

Puoi avere fino a 20 routine, comprese quelle in pausa. Fermane una per aggiungerne un’altra.

Se tocchi **Chiedi modifiche** nell’attività di una routine, oppure scrivi nella chat una nota valida per tutte le esecuzioni, come «non usare mai emoji», l’attività ti propone **Cambia anche la routine**. L’opzione appare nell’attività e nella chat, sotto la risposta. Vengono mostrate le modifiche alle istruzioni della routine, che cambiano solo quando tocchi **Cambiala**. **Lasciala così** la lascia invariata. Se chiedi di correggere solo quella bozza, non viene proposta alcuna modifica.

## Avanzate: passaggi di script

Non serve scrivere script: spiega con parole tue cosa deve fare una routine e la tua Machine penserà al resto.

Per chi vuole più controllo, una routine può anche eseguire comandi personalizzati sulla tua Machine. Nel menu ⋯, scegli **Avanzate: passaggi di script**. **Modifica** mostra i passaggi solo se la routine ne ha già. **Recupera dati** esegue prima un comando, nella relativa cartella, oppure nella cartella Home se non ne specifichi una, per un massimo di tanti secondi quanti ne hai indicati. Il risultato viene passato all’esecuzione perché lo usi. Se non hai scritto istruzioni, il risultato del comando diventa il risultato dell’esecuzione.

**Verifica** usa il risultato dell’esecuzione come input. Se il comando termina con un errore, l’esecuzione mostra **Non ha funzionato** e il messaggio restituito dal controllo. Lo stesso vale se non riesce un comando Recupera dati.

Un comando deve stare su una sola riga e viene eseguito senza shell: niente pipe o variabili. I passaggi di script sono tuoi e vengono configurati solo dalla tua dashboard. Anche un’esecuzione di prova o **Provalo** esegue Recupera dati e te lo segnala, ma non invia né conserva nulla. Una routine non invia mai nulla, quindi i passaggi di script devono limitarsi a leggere.

## Dai tuoi job di OpenClaw

Se in precedenza avevi creato job pianificati in OpenClaw, la tua Machine li legge, senza mai modificarli, e propone quelli adatti come routine sotto **Suggerito**. Ogni job viene eseguito una volta, così puoi vedere un risultato reale.

La routine conserva le tue correzioni al job, ma esclude ciò che il job ha inviato o pubblicato. Se un job eseguiva uno script o leggeva i dati raccolti da uno script, li importa come passaggio Recupera dati. **Aggiungi** lo trasforma in una routine, mentre **No, grazie** fa sì che quel job non venga più proposto. Se un job ti ricordava di fare qualcosa, viene invece proposto come attività ricorrente nella sezione Attività.

Prima di aggiungere un suggerimento, puoi modificarlo come qualsiasi altra routine usando **Modifica** e **Cambia quando** nel menu ⋯. **Esegui di nuovo** lo avvia subito con le istruzioni attuali, così puoi vedere i risultati più recenti, per esempio dopo un fine settimana tranquillo. La routine si limita a leggere, viene eseguita una volta per tocco e il nuovo risultato sostituisce quello precedente.

Puoi avere al massimo tre suggerimenti in attesa. Dopo una settimana di esecuzioni riuscite, la routine chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se tocchi **Disattiva**. Puoi riattivarlo in OpenClaw. **Tienilo** lascia attivi entrambi.

## In base a quello che fai

La tua Machine nota anche le attività che svolgi con regolarità e le propone come routine sotto **Suggerito**, anche senza OpenClaw. Cerca:

- la stessa richiesta ripetuta almeno tre volte di seguito, per esempio «riepiloga i ticket di assistenza aperti» ogni lunedì;
- un’email che invii con regolarità, come un rapporto settimanale al tuo team;
- newsletter e email di aggiornamento che ricevi ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una alla volta sempre alla stessa persona, per esempio le email di scuola e delle attività extrascolastiche al tuo partner. Un riepilogo settimanale può evitarti di inoltrarle;
- la stessa richiesta a cui rispondi regolarmente, come un’approvazione mensile per la stessa persona.

Ogni suggerimento spiega cosa ha rilevato, per esempio «Richiesto 4 volte di seguito» o «Inoltrate 6 email a Sam in 3 settimane», e viene eseguito una volta, così puoi vedere un risultato reale. Potrebbe trattarsi di un riepilogo del team, un breve resoconto prima di una riunione settimanale, un riepilogo dell’assistenza o dello sviluppo, un aggiornamento sui tuoi numeri oppure un riepilogo delle newsletter che ricevi.

La routine suggerisce solo attività specifiche per te e chiaramente utili: per esempio, un riepilogo di notizie solo sulle tue newsletter, mai uno generico. Se non trova nulla di adatto, non mostra suggerimenti.

La routine controlla al massimo una volta al giorno e aggiunge al massimo un nuovo suggerimento a settimana, senza inviare notifiche. **No, grazie** fa sì che quel suggerimento non venga più proposto. Gli inoltri e le risposte restano nell’account da cui sono stati inviati, quindi Lavoro e Personale non si mescolano. Tutto rimane sulla tua Machine. Se completi regolarmente un’attività, ti viene proposta come attività ricorrente.

## Routine e attività ricorrenti

Un’[attività ricorrente](recurring.md) ti ricorda di fare qualcosa. Una routine è un’attività che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per «pagare l’affitto il primo del mese» e una routine per «ogni venerdì, dimmi quali trattative si sono arenate».
