---
title: Routine
area: cards
summary: Attività che la tua Machine svolge da sola, con una certa frequenza, come un riepilogo del lunedì sulle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours
translated: 3e6d9d8d446a5dde
---
## Creane una

Apri **Routine** nella barra laterale e scrivi in una riga cosa deve fare e quando: "ogni lunedì alle 9, riepiloga le mie trattative aperte" oppure "ogni mattina nei giorni feriali, elenca le email a cui devo ancora rispondere". Poi seleziona **Aggiungi**.

Se non indichi un orario, la routine viene eseguita alle 8:00. L’orario si basa sull’orologio della tua Machine. Alla prima esecuzione, la routine riceve un nome breve.

Con **Aggiungi** viene prima eseguito un test, così puoi vedere il risultato prima di tenerla. Non viene inviato né salvato nulla. Poi **Aggiungi** la mantiene attiva con la frequenza scelta, **Cambia** prova altre parole o un nuovo nome, mentre **Annulla** la elimina.

## Modelli

In fondo a Routine, **Aggiungi** sotto **Modelli** attiva una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30 (Pulizia spam ogni ora, Occasioni di seconda mano ogni 3 ore, Abbonamenti e prove una volta al mese). La scheda mostra le istruzioni, come per qualsiasi routine. Con **Modifica** puoi cambiarle o modificare il nome.

Se ricevi molte newsletter e Pulizia newsletter è disattivata (almeno 25 in una settimana, da almeno 5 mittenti), sopra le attività appare una riga che indica quante ne hai ricevute e cosa farebbe la routine, con le opzioni **Attivala** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo se in una settimana hai spostato manualmente almeno 5 email nello spam. **Attivala** la aggiunge come **Aggiungi** qui. Se selezioni **No, grazie**, non verrà più proposta. Anche un modello che avevi già avuto non verrà più proposto.

**Pulizia newsletter** crea un’attività per ogni area (lavoro e personale) con le newsletter dell’ultimo giorno. Per ciascuna puoi scegliere **Tieni** o **Disiscriviti**. Per disiscriverti, usa il link diretto della mailing list oppure, se l’invio è attivo, l’email di disiscrizione dal tuo indirizzo. Altrimenti la tua Machine si disiscrive dalla pagina della mailing list nel suo browser. Se per farlo serve accedere, completare un captcha o scegliere un’opzione, dovrai pensarci tu: la riga spiega il motivo e mostra **Apri la pagina di disiscrizione**.

Le ricevute, gli ordini e le notifiche di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come un Google Group, vengono elencate sotto il nome di chi le ha scritte. Non ti disiscrivono mai dal gruppo. Se il mittente non offre una procedura di disiscrizione, la riga mostra **Disiscriviti a mano**.

**Pulizia spam** crea un’attività per ogni area con le email che sembrano spam e provengono da mittenti sconosciuti. Per ciascuna puoi scegliere **Spam** o **Non è spam**. Outlook sposta lo spam nella cartella Posta indesiderata, mentre Gmail lo segna come spam. La routine controlla ogni ora, quindi di solito troverai lo spam già individuato. Le nuove email di spam vengono aggiunte alla stessa attività finché è aperta.

Se Gmail è collegato in sola lettura, come su una Machine ospitata, non è possibile spostare le email nello spam. In quel caso, **Spam** mostra un link per segnalarle in Gmail e la tua Machine ricorda che il mittente è spam. Se non hai collegato un account email, al posto di **Aggiungi** il modello mostra **Collega la posta**.

Un mittente è sconosciuto se non gli hai mai scritto. Un oggetto che inizia con “Re:” conta come conversazione solo in una discussione a cui hai partecipato. Se ricevi di nuovo un’email da un mittente che hai segnato come spam, nell’attività o nella posta, la successiva attività la contrassegna con **Già segnato come spam**. Anche le email che hai spostato tu nello spam aiutano la routine a individuare messaggi simili.

Non cambia nulla finché non confermi nell’attività. Tocca il mittente per leggere prima l’email: rimane non letta e non cambia nulla. In Pulizia spam, le immagini dal web non vengono caricate, così il mittente non può sapere che l’hai aperta. Non ti verrà più chiesto cosa fare dei mittenti per cui hai già scelto. Se in un giorno non ricevi newsletter o spam, non viene creata alcuna attività. Queste attività non inviano mai notifiche.

Quando hai deciso cosa fare per tutti i mittenti, l’attività risulta completata e mostra **Segna come fatto**.

**Riepilogo giornaliero** seleziona una volta al giorno le poche newsletter che meritano il tuo tempo e le riunisce in un’unica attività. Per ciascuna spiega in una riga perché potrebbe interessarti. Tocca una newsletter per leggere l’email oppure seleziona **Apri nella tua posta**. La routine considera solo le newsletter: non le email di persone, le ricevute o i mittenti da cui ti sei disiscritto. Esclude anche quelle che hai già letto. Se non trova nulla di interessante, non crea alcuna attività.

La routine impara cosa ti interessa da ciò che apri, contrassegni con una stella o archivi senza leggere, e dalle opzioni **Altri così** e **Meno così** per ogni scelta. Gli argomenti che seleziona sono indicati nella scheda della routine, sotto **Più su** e **Meno su**. Rimuovine uno con × o aggiungine uno. Gli argomenti tratteggiati sono stati individuati dalla routine. Un nuovo riepilogo sostituisce quello ancora aperto e non invia mai notifiche.

La routine legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter, poi pone alla tua IA una breve domanda sulle email, con un limite giornaliero per contenere i costi. Con **Cambia quando** puoi impostare l’orario. Se modifichi le istruzioni, la routine viene eseguita come tutte le altre, seguendo le tue istruzioni.

**Compleanni** crea un’attività per ogni persona a te vicina che compie gli anni oggi: persone a cui scrivi tu, come amici, familiari e contatti abituali. Per ciascuna prepara una breve bozza di auguri nel luogo in cui di solito parli con quella persona, per esempio nella sua chat di WhatsApp o nella conversazione email, e nella sua lingua. Il messaggio parte solo quando lo invii tu. Se non ci sono compleanni, non viene creata alcuna attività.

I compleanni vengono recuperati dai tuoi calendari (gli eventi di compleanno e il calendario Compleanni di Google, letti ogni mattina anche se non sono sincronizzati, e il calendario Compleanni di Outlook), dai tuoi contatti Google su una Machine ospitata da te e da un campo data chiamato Birthday nella scheda di una persona in Graph. Se non è ancora stato trovato nessun compleanno, il risultato mostra **Non ci sono ancora informazioni sui compleanni** e spiega come aggiungerle.

**Importa i compleanni da Facebook**: quando Compleanni è attiva, un’attività ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e la tua Machine apre la pagina nel suo browser, scorre finché non sono caricati tutti i mesi e legge il nome e il compleanno di ogni amico. Ti mostra quanti ne ha trovati e quali corrispondono a persone nel tuo Graph in base al nome e al cognome. Se più persone hanno lo stesso nome, vengono escluse e indicate nell’elenco.

I compleanni vengono salvati solo quando selezioni **Salva**, nella pagina di ciascuna persona: vengono aggiunti il compleanno e, se la persona non ha ancora una foto, la sua immagine del profilo Facebook. I compleanni e le foto che hai aggiunto lì rimangono. Una foto già presente non viene mai sostituita. Non viene scritto nulla su Facebook.

La routine non rilegge la pagina da sola: per farlo, seleziona **Importa di nuovo** nell’attività. Il browser deve avere già effettuato l’accesso a Facebook. Se non è così, tocca **Accedi a Facebook** nell’attività e accedi. Una volta effettuato l’accesso, la routine legge la pagina da sola. La tua Machine non effettua mai l’accesso al posto tuo.

Le persone che non sono presenti nel tuo Graph vengono conteggiate e ne vengono mostrati alcuni nomi. **Aggiungi … come contatti personali** le aggiunge tutte insieme, anche dopo aver selezionato Salva. Per ciascuna vengono aggiunti il nome e il compleanno, che non vengono mai condivisi con una Work Fleet. Una persona viene esclusa se qualcuno nel tuo Graph ha già quel nome o se l’avevi eliminata definitivamente. I promemoria di compleanno vengono comunque creati solo per le persone a cui scrivi.

Con **Annulla** nell’attività, queste persone vengono rimosse. Anche se hai selezionato **Importa di nuovo**, vengono rimosse esattamente le persone aggiunte con l’importazione.

**Abbonamenti e prove** legge una volta al mese le ricevute, le fatture e le notifiche di rinnovo, poi riunisce gli abbonamenti in un’unica attività. Per ciascuno indica il costo, la data del prossimo addebito e un avviso se sta per finire una prova o se il prezzo aumenta. Vengono elencati solo gli abbonamenti identificati con sicurezza. Se non ne trova, non viene creata alcuna attività.

Per ciascun abbonamento, scegli **Tieni** o **Disdici**. Non ti verrà più chiesto di un abbonamento che hai deciso di tenere, a meno che il prezzo non cambi. Se selezioni **Disdici**, ricevi il link alla pagina per disdire oppure una bozza da inviare per chiedere la disdetta. Il messaggio parte solo quando lo invii tu. Tra un’esecuzione e l’altra, la routine controlla ogni giorno e crea un’attività se una prova o un rinnovo prevede un addebito entro 7 giorni.

**Restare in contatto** ti invita ogni tanto a farti sentire con una persona a te vicina, ma solo se c’è un motivo concreto. Nella scheda scegli le persone da includere da un breve elenco di contatti con cui scambi messaggi direttamente in entrambe le direzioni da mesi. Rimuovi una persona con ×.

Ricevi un promemoria solo se è passato molto più tempo del solito dall’ultima conversazione e c’è qualcosa di preciso da dire: una notizia che ti ha raccontato, una promessa ancora da mantenere o un messaggio a cui non hai mai risposto. Nell’attività trovi il motivo e una breve bozza nella lingua della persona, nel luogo in cui di solito parlate. Il messaggio parte solo quando lo invii tu. Se non c’è nulla da dire, non viene creata alcuna attività.

La routine invia al massimo due promemoria a settimana e uno al mese per persona. Non ne invia a chi hai sentito di recente. Se selezioni **Non serve** per un promemoria, la routine aspetta più a lungo prima di proporti di nuovo quella persona, e ogni volta attende ancora di più. Non invia mai notifiche e rimane personale: non viene mai condivisa con una Work Fleet.

**Occasioni di seconda mano** controlla una ricerca su un sito di seconda mano, come Marktplaats, Vinted, eBay o Facebook Marketplace. Applica i filtri che vuoi sul sito, copia l’indirizzo dei risultati e incollalo dopo aver selezionato **Aggiungi**. Se vuoi, aggiungi filtri con parole tue, per esempio “meno di 300, entro 30 km, niente ‘per ricambi’”. Ogni ricerca è una routine a sé, quindi aggiungila di nuovo per crearne un’altra.

Ogni 3 ore la tua Machine apre la ricerca nel suo browser e cerca gli annunci che non ha ancora visto. Prima controlla prezzo, distanza e parole da escludere, usando codice semplice.

Apre ogni nuovo annuncio che supera i filtri. La tua IA ne valuta le condizioni in base alla foto e alla descrizione, e valuta il venditore in base alle recensioni, alla valutazione e all’età dell’account. Gli annunci migliori vengono raccolti in un’unica attività, ciascuno con foto, titolo, prezzo e un breve giudizio. Tocca un annuncio per aprirlo nel browser della tua Machine.

Finché l’attività è aperta, le nuove occasioni vengono aggiunte in cima, il conteggio aumenta e ricevi una nuova notifica, perché le offerte migliori vanno a ruba. Quando la contrassegni come fatta, la prossima occasione avvia una nuova attività. Se un’esecuzione non trova nulla di interessante, non cambia nulla.

La routine limita il carico sul sito e i costi: legge la ricerca una volta per esecuzione, apre al massimo 6 annunci per esecuzione con una pausa tra l’uno e l’altro e controlla al massimo 40 annunci al giorno tra tutte le tue ricerche. Per ogni annuncio pone alla tua IA una breve domanda e le mostra una foto. La prima esecuzione controlla gli annunci più recenti e segna come già visti gli altri, così le esecuzioni successive mostrano solo quelli nuovi.

Se il sito ti chiede di accedere, mostra un controllo anti-robot o impedisce la lettura, un’attività te lo segnala e mostra **Apri** per visualizzare la pagina nel browser della tua Machine. Accedi o supera il controllo tu stesso. La lettura riprenderà alla prossima esecuzione. La tua Machine non accede mai al posto tuo, non risolve i controlli e non contatta i venditori, non fa offerte né acquista.

Con **Modifica ricerca** nella scheda della routine puoi inserire un nuovo indirizzo o modificare i filtri; con **Cambia quando** puoi impostare un’altra frequenza, per esempio “ogni 6 ore”.

Finché le istruzioni di una routine basata su un modello non cambiano, la routine usa il codice del modello senza consumare il tuo piano IA. Per esempio, Pulizia spam prima elenca in codice le nuove email di mittenti sconosciuti e pone una breve domanda alla tua IA solo se ne trova. Restare in contatto chiede informazioni solo sulle una o due persone che ha selezionato. Se cambi il nome, le istruzioni rimangono le stesse. Se modifichi le istruzioni, la routine viene eseguita come tutte le altre, seguendo le tue istruzioni.

Pulizia newsletter e Pulizia spam creano comunque la stessa attività, con una scelta per ogni email. Se modifichi Compleanni, la routine mostra il risultato e al massimo una bozza, non un’attività per ogni persona. Con **Torna al modello** in **Modifica** puoi ripristinare le istruzioni originali.

## Cosa fa una routine

All’orario previsto, la tua Machine legge le informazioni necessarie, per esempio i tuoi messaggi, le riunioni e Graph, e mostra il risultato nella pagina Routine. Ogni risultato indica **Pronta**, **Niente di nuovo** (con il motivo) oppure **Non è andato** (con il motivo). Un’esecuzione che finisce senza un risultato viene considerata non riuscita, mai completata.

Le routine si limitano a leggere: i tuoi messaggi, le pagine web, GitHub e siti come X nel browser. Non inviano, rispondono, pubblicano o modificano nulla. Solo un modello può modificare la posta, e solo dopo la tua conferma nell’attività.

Se l’esecuzione di una routine prevede un post o un messaggio, la routine svolge tutti i passaggi fino a quel punto e mostra la bozza, per esempio **Pubblica su X:**. Dopo un’esecuzione effettiva, la bozza viene mostrata in un’attività da approvare. Un’esecuzione di prova mostra solo la bozza. Il nome indica l’argomento e la destinazione, il pulsante indica il passaggio, per esempio **Pubblicalo**, e con **Dalla tua routine** puoi aprire la routine.

L’attività viene creata nell’area dell’account da cui partirà il contenuto, per esempio Lavoro per l’account X della tua azienda, quindi non ti verrà mai chiesto di spostarla.

Un’esecuzione può seguire le tue [skill](skills.md) attive, scelte in base a ciò che fa la routine. Vengono lette per intero solo quelle pertinenti. Il risultato le elenca sotto **Usate:**. Una skill non fa mai inviare o modificare nulla a una routine.

Trovi le routine sotto **Le tue routine**, dopo gli eventuali suggerimenti. Se il risultato è lungo, viene mostrata un’anteprima breve. Seleziona **Mostra altro** o tocca il risultato per aprirlo.

Ogni esecuzione conosce il risultato precedente, quindi può indicare cosa è cambiato.

Dopo un’esecuzione riuscita, la tua Machine potrebbe scrivere da sola una ricetta per le parti di lettura che si ripetono, per esempio quali email o modifiche di GitHub controllare. Le esecuzioni successive le leggono prima usando codice semplice, poi l’IA seleziona le informazioni importanti e le scrive, consumando meno token. Una ricetta si limita a leggere. Se smette di funzionare, l’esecuzione legge da sola e la corregge. La trovi sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine era spenta o occupata, le esecuzioni saltate non si accumulano: viene eseguita una sola volta solo l’ultima. Ogni data viene eseguita una sola volta, anche dopo un riavvio.

Le routine vengono eseguite una alla volta e attendono se il credito del tuo piano IA è basso, come tutti i processi in background. Con **Esegui ora** la routine parte subito. Il risultato appare nella scheda appena è pronto.

## Modifica o interrompi una routine

Trovi queste opzioni nel menu ⋯ della routine. **Modifica** permette di cambiare il nome e le istruzioni, senza modificare la frequenza o i risultati ottenuti finora. Con **Cambia quando** puoi impostare un’altra frequenza usando parole tue, per esempio "ogni giorno feriale alle 8". Entrambe le opzioni includono **Salva** e **Annulla**. Su un computer puoi annullare anche premendo Esc o facendo clic fuori dalla finestra.

In **Modifica**, **Provalo** esegue una volta le nuove istruzioni e mostra il risultato. La routine rimane invariata finché non selezioni **Salva**.

Con **Metti in pausa** interrompi le esecuzioni finché non selezioni **Riprendi** nella scheda. Le routine in pausa si trovano sotto **In pausa**, dopo le tue routine. Le esecuzioni saltate mentre la routine era in pausa non verranno recuperate. **Ferma** interrompe definitivamente una routine.

Puoi avere fino a 20 routine, incluse quelle in pausa. Interrompine una per aggiungerne un’altra.

Se usi **Chiedi modifiche** nell’attività di una routine o scrivi nella sua chat, e il tuo commento vale per tutte le esecuzioni, per esempio "non usare mai emoji", l’attività ti propone **Cambia anche la routine**. La trovi nell’attività e nella chat, sotto la risposta. Vengono mostrate le modifiche alle istruzioni della routine, che cambierà solo quando tocchi **Cambiala**. **Lasciala così** la mantiene invariata. Se chiedi di correggere solo quella bozza, non ti viene proposta questa opzione.

## Avanzate: passaggi di script

Non serve scrivere script: spiega con parole tue cosa deve fare una routine e la tua Machine penserà al resto.

Gli utenti esperti possono anche eseguire i propri comandi sulla propria Machine: seleziona **Avanzate: passaggi di script** nel menu ⋯. **Modifica** mostra i passaggi solo se la routine ne ha già. **Recupera dati** esegue prima un comando nella cartella specificata (se il campo è vuoto, usa la tua cartella home) e lo interrompe dopo il numero di secondi indicato. Il risultato del comando viene passato all’esecuzione perché lo usi. Se non aggiungi istruzioni, il risultato del comando viene usato come risultato dell’esecuzione.

**Verifica** riceve il risultato come input al termine dell’esecuzione. Se il comando restituisce un errore, l’esecuzione mostra **Non è andato** e il messaggio di errore. Se non riesce il comando di Recupera dati, viene mostrato lo stesso messaggio.

Ogni comando deve stare su una sola riga e viene eseguito senza shell: niente pipe o variabili. Gli script li gestisci tu e si configurano solo nella tua dashboard. Anche le esecuzioni di prova e quelle avviate con **Provalo** eseguono Recupera dati e lo indicano. Non inviano né salvano nulla. Una routine non invia mai nulla, quindi uno script deve limitarsi a leggere.

## Dalle tue attività di OpenClaw

Se in precedenza avevi creato attività programmate in OpenClaw, la tua Machine le legge senza modificarle e propone come routine quelle compatibili, sotto **Suggerito**. Le ha eseguite una volta, quindi puoi vedere un risultato effettivo.

Mantiene le correzioni che hai apportato all’attività ed esclude ciò che ha inviato o pubblicato. Se un’attività ha eseguito uno script o ha letto dati raccolti da uno script, lo aggiunge come Recupera dati. **Aggiungi** la trasforma in una routine, mentre **No, grazie** impedisce che l’attività venga proposta di nuovo. Se un’attività ti ricordava di fare qualcosa, viene proposta in To-do come attività ricorrente.

Prima di aggiungere un suggerimento, puoi modificarlo come qualsiasi routine con **Modifica** e **Cambia quando** nel menu ⋯. **Esegui di nuovo** lo avvia subito con le istruzioni attuali, così puoi vedere i risultati aggiornati, per esempio dopo un fine settimana tranquillo. Si limita a leggere, viene eseguito una volta per ogni tocco e il nuovo risultato sostituisce quello precedente.

Puoi avere al massimo tre suggerimenti in attesa. Dopo una settimana di esecuzioni riuscite, la routine chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se tocchi **Disattiva**. Puoi riattivarlo in OpenClaw. **Tienilo** lascia attivi entrambi.

## In base a quello che fai

La tua Machine rileva anche le attività che svolgi con una certa frequenza e le propone come routine sotto **Suggerito**, anche se non usi OpenClaw. Cerca:

- la stessa richiesta, almeno tre volte di seguito, per esempio "riepiloga le richieste di assistenza aperte" ogni lunedì;
- un’email che invii con regolarità, per esempio un rapporto settimanale al tuo team;
- newsletter ed email di aggiornamento che ricevi ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una alla volta sempre alla stessa persona, per esempio le email della scuola e delle attività extrascolastiche al tuo partner: un riepilogo settimanale evita di inoltrarle tutte;
- la stessa richiesta a cui rispondi regolarmente, per esempio una conferma mensile alla stessa persona.

Ogni suggerimento spiega cosa ha notato, per esempio "Richiesto 4 volte di seguito" oppure "Inoltrate 6 email a Sam in 3 settimane", ed è già stato eseguito una volta, così puoi vedere un risultato effettivo. Potrebbe trattarsi di un riepilogo per il team, un breve promemoria prima di una chiamata settimanale, un riepilogo delle richieste di assistenza o di sviluppo, un aggiornamento sui tuoi numeri o un riepilogo delle newsletter che ricevi.

La routine propone solo attività specifiche per te e chiaramente utili: un riepilogo delle notizie si basa solo sulle newsletter che ricevi tu, mai su notizie generiche. Se non trova nulla di adatto, non propone alcun suggerimento.

La routine controlla al massimo una volta al giorno e propone al massimo un nuovo suggerimento a settimana, senza inviare notifiche. Se selezioni **No, grazie**, il suggerimento non verrà più riproposto. Gli inoltri e le risposte rimangono associati all’account da cui sono stati inviati, così Lavoro e Personale non si mescolano. Tutto rimane sulla tua Machine. Un’attività che completi regolarmente viene proposta come attività ricorrente.

## Routine e attività ricorrenti

Un’[attività ricorrente](recurring.md) ti ricorda di fare qualcosa. Una routine è un’attività che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per "pagare l’affitto il primo del mese" e una routine per "ogni venerdì, dimmi quali trattative si sono arenate".
