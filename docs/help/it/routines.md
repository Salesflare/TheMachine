---
title: Routine
area: cards
summary: Attività che la tua Machine svolge da sola e con regolarità, come un riepilogo del lunedì sulle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in
translated: 2be351a9cef42215
---
## Creane una

Apri **Routine** nella barra laterale e scrivi in una riga cosa deve fare e quando: "ogni lunedì alle 9, riepiloga le mie trattative aperte" oppure "ogni mattina nei giorni feriali, elenca le email a cui devo ancora rispondere". Poi tocca **Aggiungi**.

Se non specifichi un orario, viene eseguita alle 8:00. L’orario è quello della tua Machine. La prima esecuzione le assegna un nome breve.

**Aggiungi** avvia prima un’esecuzione di prova, così puoi vedere il risultato prima di tenerla. Non viene inviato né salvato nulla. Poi **Aggiungi** la mantiene attiva secondo la pianificazione, **Cambia** prova altre parole o un nuovo nome e **Annulla** la elimina.

## Modelli

In fondo a Routine, sotto **Modelli**, **Aggiungi** attiva una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30 (Pulizia spam ogni ora, Abbonamenti e prove una volta al mese). La scheda mostra le sue istruzioni, come per qualsiasi routine, e **Modifica** permette di cambiarle o di modificarne il nome.

Quando arrivano molte newsletter e Pulizia newsletter è disattivata (almeno 25 in una settimana, da almeno 5 mittenti), sopra le attività compare un messaggio che indica quante ne sono arrivate e cosa farebbe, con **Attivala** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo quando, in una settimana, hai spostato manualmente nello spam almeno 5 email. **Attivala** la aggiunge come **Aggiungi** qui. Se tocchi **No, grazie**, non verrà più proposta. Lo stesso vale per un modello che avevi già usato.

**Pulizia newsletter** crea un’attività per ogni area (lavoro e personale) con le newsletter dell’ultimo giorno, ciascuna con l’opzione **Tieni** o **Disiscriviti**. Per disiscriverti, usa il link con un clic della mailing list oppure, se l’invio è attivo, l’email di disiscrizione inviata dal tuo indirizzo. Altrimenti, The Machine si disiscrive dalla pagina della mailing list nel proprio browser. Se serve accedere, completare un CAPTCHA o fare delle scelte, dovrai farlo tu: la riga spiega il motivo e mostra **Apri la pagina di disiscrizione**.

Le ricevute, gli ordini e le notifiche di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come un Google Group, sono elencate sotto il nome di chi le ha scritte e non ti disiscrivono mai dal gruppo. Se il mittente non ha un sistema di disiscrizione, la riga mostra **Disiscriviti a mano**.

**Pulizia spam** crea un’attività per ogni area con le email di mittenti sconosciuti che sembrano spam, ciascuna con l’opzione **Spam** o **Non è spam**. Outlook sposta lo spam in Posta indesiderata e Gmail lo segna come spam. La routine controlla ogni ora, quindi di solito lo spam è già stato individuato quando lo vedi. Le nuove email di spam vengono aggiunte alla stessa attività finché resta aperta.

Se Gmail è collegato in sola lettura, come su una Machine ospitata, non è possibile spostare le email nello spam. In quel caso, **Spam** apre un link per segnalarle in Gmail e The Machine ricorda che il mittente è spam. Se non è collegato nessun account email, il modello mostra **Collega la posta** al posto di **Aggiungi**.

Un mittente è sconosciuto se non gli hai mai scritto. Un «Re:» conta come conversazione solo in una discussione a cui hai partecipato scrivendo. Se ricevi di nuovo un’email da un mittente che hai segnato come spam, nell’attività o nella casella di posta, la prossima attività la segnala con **Già segnato come spam**. Anche le email che hai spostato tu nello spam aiutano a riconoscere messaggi simili.

Non cambia nulla finché non confermi nell’attività. Tocca un mittente per leggere prima l’email: resta non letta e non cambia nulla. In Pulizia spam, le immagini dal web non vengono caricate, così il mittente non può vedere che hai aperto l’email. Non ti verrà chiesto di nuovo cosa fare dei mittenti che hai già valutato. Se in un giorno non arrivano newsletter o spam, non viene creata nessuna attività. Queste attività non inviano mai notifiche.

Quando hai deciso cosa fare con tutti i mittenti, l’attività risulta completata e mostra **Segna come fatto**.

**Riepilogo giornaliero** seleziona ogni giorno, in un’unica attività, le poche newsletter che vale la pena leggere. Per ognuna spiega in una riga perché è importante per te. Toccala per leggere l’email oppure usa **Apri nella tua posta**. La selezione comprende solo newsletter, mai email di persone, ricevute o mittenti da cui ti sei disiscritto, e mai contenuti che hai già letto. Se non c’è nulla di interessante, non viene creata nessuna attività.

La routine impara cosa ti interessa da quello che apri, aggiungi ai preferiti o archivi senza leggere, e dalle opzioni **Altri così** e **Meno così** su ogni selezione. Gli argomenti che prende in considerazione sono indicati nella scheda della routine, sotto **Più su** e **Meno su**. Rimuovine uno con × o aggiungine uno. Gli argomenti tratteggiati sono stati individuati dalla routine. Un nuovo riepilogo sostituisce quello ancora aperto e non invia mai notifiche.

Legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter, poi pone alla tua AI una breve domanda al giorno al massimo, per contenere i costi. **Cambia quando** permette di impostare l’orario. Dopo che modifichi le istruzioni, la routine funziona come qualsiasi altra, usando le tue istruzioni.

**Compleanni** crea un’attività per ogni persona a te vicina che compie gli anni oggi: persone a cui scrivi tu, come amici, familiari e contatti abituali. Per ciascuna prepara un breve messaggio di auguri nel posto in cui di solito parlate, ad esempio nella chat WhatsApp o nella vostra conversazione email, nella sua lingua. Il messaggio parte solo se lo invii tu. Se non ci sono compleanni, non viene creata nessuna attività.

I compleanni vengono presi dai tuoi calendari (gli eventi di compleanno di Google e il calendario Compleanni, letti ogni mattina anche se non sono sincronizzati, e il calendario Compleanni di Outlook), dai tuoi contatti Google su una Machine ospitata autonomamente e dal campo data Birthday di una persona nel Graph. Se non è ancora presente nessun compleanno, il risultato mostra «Non ci sono ancora informazioni sui compleanni» e spiega come aggiungerle.

**Importa i compleanni da Facebook**: quando Compleanni è attiva, un’attività ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e The Machine apre la pagina nel proprio browser, scorre fino a caricare tutti i mesi e legge il nome e il compleanno di ogni amico. Ti mostra quanti ne ha trovati e quali corrispondono a persone nel tuo Graph, in base al nome e al cognome. Se più persone hanno lo stesso nome, vengono ignorate e inserite nell’elenco.

I compleanni vengono salvati solo quando tocchi **Salva**, nella pagina di ogni persona: la data del compleanno e, se la persona non ha ancora una foto, la sua immagine del profilo Facebook. Le date e le immagini già impostate restano invariate e una foto già presente non viene mai sostituita. Non viene scritto nulla su Facebook.

La pagina non viene riletta automaticamente: per farlo, tocca **Importa di nuovo** nell’attività. Devi aver effettuato l’accesso a Facebook nel browser. Se non l’hai fatto, tocca **Accedi a Facebook** nell’attività e accedi da lì. Una volta effettuato l’accesso, la pagina viene letta automaticamente. The Machine non accede mai al tuo posto.

Le persone che non sono presenti nel Graph vengono conteggiate e ne vengono mostrati alcuni nomi. **Aggiungi … come contatti personali** le aggiunge tutte in una volta, anche dopo aver toccato Salva: ciascuna con il proprio nome e compleanno, senza condividerla mai con una Work Fleet. Una persona viene ignorata se qualcuno nel tuo Graph ha già quel nome o se l’avevi eliminata definitivamente. I promemoria dei compleanni vengono comunque creati solo per le persone a cui scrivi.

Toccando **Annulla** nell’attività, rimuovi esattamente quelle persone, anche dopo aver toccato **Importa di nuovo**.

**Abbonamenti e prove** legge ricevute, fatture e avvisi di rinnovo una volta al mese e raccoglie gli abbonamenti in un’unica attività. Per ciascuno mostra il costo, la prossima data di addebito e un avviso quando termina una prova o aumenta il prezzo. Elenca solo gli abbonamenti di cui è sicura. Se non ne trova, non viene creata nessuna attività.

Per ciascuno, scegli **Tieni** o **Disdici**. Non ti verrà chiesto di nuovo se tieni un abbonamento, a meno che il prezzo non cambi. Se scegli **Disdici**, viene mostrata la pagina di disdetta oppure una bozza in cui chiedi di annullare l’abbonamento. Il messaggio parte solo se lo invii tu. Tra un’esecuzione e l’altra, la routine controlla ogni giorno e crea un’attività se una prova o un rinnovo comporta un addebito entro 7 giorni.

**Restare in contatto** ti ricorda ogni tanto di farti sentire con una persona a te vicina, solo quando c’è un motivo concreto. Nella sua scheda, scegli da un breve elenco le persone con cui scambi messaggi direttamente in entrambe le direzioni da mesi. Rimuovi qualcuno con ×.

Ricevi un promemoria solo se è passato molto più tempo del solito dall’ultima conversazione e c’è qualcosa di specifico da dire: una novità che ti ha raccontato, una promessa ancora da mantenere o un messaggio a cui non hai mai risposto. L’attività include il motivo e un breve messaggio preparato nel posto in cui di solito parlate, nella sua lingua. Il messaggio parte solo se lo invii tu. Se non c’è niente da dire, non viene creata nessuna attività.

Invia al massimo due promemoria a settimana, uno per persona al mese, e nessuno a chi hai sentito di recente. Se scegli **Non serve** per un promemoria, la routine aspetta più a lungo prima di proporti quella persona, e aspetta ancora di più ogni volta che lo fai. Non invia mai notifiche e resta personale: non viene mai condivisa con una Work Fleet.

Finché le istruzioni del modello restano invariate, la routine usa il codice del modello e non il tuo piano AI (Pulizia spam prima elenca nel codice le nuove email di mittenti sconosciuti e pone alla tua AI una breve domanda solo se ne trova; Restare in contatto chiede informazioni solo sulle una o due persone che ha selezionato). Se cambi il nome, il codice resta invariato. Dopo che modifichi le istruzioni, la routine funziona come qualsiasi altra, usando le tue istruzioni.

Pulizia newsletter e Pulizia spam continuano a creare un’unica attività con una scelta per ogni email. Se modifichi Compleanni, la routine mostra il risultato e al massimo una bozza, non un’attività per ogni persona. **Torna al modello**, in **Modifica**, ripristina le istruzioni del modello.

## Cosa fa una routine

All’orario previsto, la tua Machine legge ciò che serve, come i messaggi, le riunioni e il Graph, e mostra il risultato nella pagina Routine. Ogni risultato indica **Pronta**, **Niente di nuovo** (con il motivo) oppure **Non è andato** (con il motivo). Un’esecuzione che termina senza un risultato è considerata non riuscita, mai completata.

Le routine si limitano a leggere: i tuoi messaggi, le pagine web, GitHub e siti come X nel browser. Non inviano, rispondono, pubblicano o modificano nulla. Solo un modello può modificare le email, e solo ciò che confermi nella sua attività.

Se l’attività di una routine termina con un post o un messaggio, la routine esegue tutto fino a quel passaggio e mostra la bozza, ad esempio **Pubblicheresti su X:**. Dopo un’esecuzione effettiva, la bozza compare come attività da approvare; l’esecuzione di prova la mostra soltanto. Il nome indica l’argomento e la destinazione, il pulsante descrive il passaggio, ad esempio **Pubblicalo**, e **Dalla tua routine** apre la routine.

L’attività viene creata nell’area dell’account da cui partirà, ad esempio Lavoro per l’account X della tua azienda, quindi non ti chiede mai di spostarla.

Un’esecuzione può seguire le tue [skill](skills.md) attive, selezionate in base a ciò che fa la routine: legge per intero solo quelle pertinenti. Il risultato le elenca sotto **Usate:**. Una skill non fa mai sì che una routine invii o modifichi qualcosa.

Le tue routine si trovano sotto **Le tue routine**, dopo gli eventuali suggerimenti. I risultati lunghi vengono ridotti a un’anteprima breve. Tocca **Mostra altro** o il risultato per aprirlo.

Ogni esecuzione conosce il risultato precedente, quindi può indicare cosa è cambiato da allora.

Dopo un’esecuzione riuscita, la tua Machine può creare automaticamente una procedura per le parti di lettura che si ripetono ogni volta, come le email o le modifiche di GitHub da controllare. Le esecuzioni successive le leggono prima in codice semplice; poi l’AI seleziona ciò che conta e lo scrive, usando meno token. Una procedura si limita a leggere. Se smette di funzionare, l’esecuzione procede da sola e la corregge. La procedura compare sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine era spenta o occupata, le esecuzioni saltate non si accumulano: ne viene eseguita una sola, la più recente. Ogni data viene elaborata una volta, anche dopo un riavvio.

Le routine vengono eseguite una alla volta e restano in attesa quando l’utilizzo del tuo piano AI è basso, come per tutte le attività in background. **Esegui ora** avvia subito la routine. Il risultato compare sulla scheda quando è pronto.

## Modificala o interrompila

Queste opzioni si trovano nel menu ⋯ della routine. **Modifica** cambia il nome e le istruzioni, ma lascia invariati la pianificazione e i risultati ottenuti finora. **Cambia quando** permette di impostare una nuova frequenza con parole tue, ad esempio «ogni giorno feriale alle 8». Entrambe le opzioni includono **Salva** e **Annulla**. Sul computer puoi anche annullare premendo Esc o facendo clic fuori dalla finestra.

In **Modifica**, **Provalo** esegue una volta le nuove istruzioni e mostra il risultato lì. La routine non cambia finché non tocchi **Salva**.

**Metti in pausa** interrompe le esecuzioni finché non tocchi **Riprendi** sulla scheda. Le routine in pausa si trovano sotto **In pausa**, dopo le tue routine, e le esecuzioni saltate durante la pausa non partono in seguito. **Ferma** interrompe definitivamente una routine.

Puoi avere fino a 20 routine, comprese quelle in pausa. Fermane una per aggiungerne un’altra.

Quando usi **Chiedi modifiche** sull’attività di una routine o scrivi nella sua chat e la tua nota riguarda tutte le esecuzioni, ad esempio «non usare mai emoji», l’attività ti propone **Cambia anche la routine**. L’opzione compare nell’attività e nella chat, sotto la risposta. Ti mostra cosa cambierà nelle istruzioni e la routine viene modificata solo quando tocchi **Cambiala**. **Lasciala così** non apporta modifiche. Se la correzione riguarda solo quella bozza, non viene proposta nessuna opzione.

## Avanzate: passaggi di script

Non serve uno script: descrivi con parole tue cosa deve fare una routine e la tua Machine penserà al resto.

Per gli utenti esperti, una routine può anche eseguire comandi personalizzati sulla tua Machine. Nel menu ⋯, scegli **Avanzate: passaggi di script**. **Modifica** mostra i passaggi solo se la routine ne ha già. **Recupera dati** esegue prima un comando nella sua cartella (la tua cartella home se non ne specifichi una) e lo fa attendere al massimo per il numero di secondi impostato. L’output del comando viene fornito all’esecuzione perché lo usi. Se non ci sono istruzioni, l’output diventa il risultato.

**Verifica** riceve il risultato come input al termine dell’esecuzione. Se il comando termina con un errore, il risultato mostra **Non è andato** e il messaggio della verifica. Anche un comando di Recupera dati non riuscito mostra lo stesso messaggio.

Un comando deve essere su una sola riga e viene eseguito senza shell: niente pipe o variabili. I passaggi di script sono tuoi e vengono impostati solo nella tua dashboard. Anche un’esecuzione di prova e **Provalo** eseguono Recupera dati e lo indicano, ma non inviano né salvano nulla. Una routine non invia mai nulla, quindi un passaggio di script dovrebbe solo leggere.

## Dai tuoi job di OpenClaw

Se prima avevi creato job pianificati in OpenClaw, la tua Machine li legge (non li modifica mai) e propone come routine quelli compatibili, sotto **Suggerito**. Ognuno è stato eseguito una volta, quindi puoi vedere un risultato effettivo.

Mantiene le correzioni che hai apportato al job e tralascia ciò che ha inviato o pubblicato. Se un job eseguiva uno script o leggeva dati raccolti da uno script, lo include come Recupera dati. **Aggiungi** lo trasforma in una routine, mentre **No, grazie** evita che ti venga proposto di nuovo. Se un job ti ricordava di fare qualcosa, compare invece come proposta di attività ricorrente in Attività.

Prima di aggiungere un suggerimento, puoi modificarlo come qualsiasi routine con **Modifica** e **Cambia quando** nel menu ⋯. **Esegui di nuovo** lo avvia subito con le istruzioni attuali, così puoi vedere risultati più recenti, ad esempio dopo un fine settimana tranquillo. Si limita a leggere, viene eseguito una volta per ogni tocco e il nuovo risultato sostituisce quello precedente.

Puoi avere al massimo tre suggerimenti in attesa. Dopo una settimana di esecuzioni riuscite, la routine ti chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se tocchi **Disattiva** e puoi riattivarlo in OpenClaw. **Tienilo** lascia attivi entrambi.

## In base a quello che fai

La tua Machine nota anche le attività che svolgi con regolarità e le propone come routine sotto **Suggerito**, anche se non usi OpenClaw. Cerca:

- la stessa richiesta, almeno tre volte di seguito, ad esempio «riepiloga i ticket di assistenza aperti» ogni lunedì;
- un’email che invii con regolarità, come un report settimanale al tuo team;
- newsletter e email di aggiornamento che arrivano ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una alla volta sempre alla stessa persona, come le email della scuola o di un club al tuo partner: un riepilogo settimanale gli evita di doverle inoltrare;
- la stessa richiesta a cui rispondi regolarmente, come un’approvazione mensile per la stessa persona.

Ogni suggerimento spiega cosa ha rilevato, ad esempio «Richiesta 4 volte di seguito» oppure «6 email inoltrate a Sam in 3 settimane». È stato eseguito una volta, quindi puoi vedere un risultato effettivo. Puoi creare, ad esempio, un riepilogo del team, un breve promemoria prima di una riunione settimanale, un riepilogo dell’assistenza o dello sviluppo, un aggiornamento sui tuoi numeri o un riepilogo delle newsletter che ricevi.

Suggerisce solo attività specifiche per te e chiaramente utili: un riepilogo delle notizie riguarda solo le newsletter che ricevi, mai notizie generiche. Se non trova nulla di adatto, non propone niente.

Controlla al massimo una volta al giorno e propone al massimo un nuovo suggerimento a settimana, senza inviare notifiche. **No, grazie** evita che quel suggerimento venga riproposto. Le email inoltrate e le risposte restano associate all’account da cui sono state inviate, quindi Lavoro e Personale non si mescolano. Tutto resta sulla tua Machine. Se completi regolarmente un’attività, viene proposta invece come attività ricorrente.

## Routine e attività ricorrenti

Un’[attività ricorrente](recurring.md) ti ricorda di fare qualcosa. Una routine è un’attività che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per «pagare l’affitto il primo del mese» e una routine per «ogni venerdì, dimmi quali trattative sono ferme».
