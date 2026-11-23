---
title: Routine
area: cards
summary: Attività che la tua Machine svolge da sola, con regolarità, come un riepilogo del lunedì delle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: e0d519d5927cdde0
---
## Creare una routine

Apri **Routine** nella barra laterale e scrivi in una riga cosa deve fare e quando: "ogni lunedì alle 9, riepiloga le mie trattative aperte" oppure "ogni mattina nei giorni feriali, elenca le email a cui devo ancora rispondere". Poi tocca **Aggiungi**.

Se non indichi un orario, la routine viene eseguita alle 8:00. L’orario è quello della tua Machine. Alla prima esecuzione, la routine riceve un nome breve.

Con **Aggiungi** viene prima eseguita una prova, così puoi vedere il risultato prima di attivare la routine. Non viene inviato né salvato nulla. Poi **Aggiungi** la mantiene attiva con la frequenza scelta, **Cambia** prova altre parole o un nuovo nome e **Annulla** la elimina.

## Modelli

In fondo a Routine, nella sezione **Modelli**, tocca **Aggiungi** per attivare una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30 (Pulizia spam ogni ora, Occasioni di seconda mano ogni 3 ore, Abbonamenti e prove una volta al mese). La scheda mostra le istruzioni, come per qualsiasi routine, e **Modifica** permette di cambiarle o modificare il nome.

Quando arrivano molte newsletter e Pulizia newsletter è disattivata (25 o più in una settimana, da almeno 5 mittenti), sopra le attività compare un messaggio che indica quante ne sono arrivate e cosa farebbe la routine, con le opzioni **Attiva** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo quando in una settimana hai spostato manualmente almeno 5 email nella cartella spam. **Attiva** la aggiunge come fa **Aggiungi** qui. Se tocchi **No, grazie**, non verrà proposta di nuovo. Non verrà proposta neanche una routine modello che avevi già usato in precedenza.

**Pulizia newsletter** crea un’attività per ogni area, lavoro e personale, con le newsletter dell’ultimo giorno. Per ognuna puoi scegliere **Tieni** o **Disiscriviti**. Per disiscriverti, usa il link con un clic della mailing list oppure, se l’invio è attivo, invia l’email di disiscrizione dal tuo indirizzo. Altrimenti, The Machine si disiscrive dalla pagina della lista usando il proprio browser. Se serve accedere, completare un captcha o scegliere un’opzione, te lo segnala nella riga con **Apri la pagina di disiscrizione**.

Le ricevute, gli ordini e le notifiche di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come Google Group, vengono elencate sotto il nome di chi le ha scritte e non ti disiscrivono mai dal gruppo. Se il mittente non offre una procedura per disiscriverti, nella riga compare **Disiscriviti a mano**.

**Pulizia spam** crea un’attività per ogni area, con le email di mittenti sconosciuti che sembrano spam. Per ciascuna puoi scegliere **Spam** o **Non è spam**. Outlook sposta le email nella posta indesiderata, mentre Gmail le contrassegna come spam. La routine controlla ogni ora, quindi di solito lo spam viene individuato prima che tu lo veda. Le nuove email di spam vengono aggiunte alla stessa attività finché è aperta.

Gmail collegato in sola lettura, come su una Machine ospitata, non può spostare le email nella cartella spam. In questo caso, **Spam** mostra un link per contrassegnare l’email in Gmail e The Machine ricorda che il mittente è spam. Se non è collegato nessun account email, al posto di **Aggiungi** il modello mostra **Collega la posta**.

Per «sconosciuto» si intende un mittente a cui non hai mai scritto. Un «Re:» viene considerato parte di una conversazione solo in una discussione a cui hai scritto. Se ricevi di nuovo un’email da un mittente che hai contrassegnato come spam, nell’attività o nella posta, la troverai nell’attività successiva con l’etichetta **Già segnato come spam**. Anche le email che hai spostato manualmente nella cartella spam aiutano la routine a individuare messaggi simili.

Non cambia nulla finché non confermi nell’attività. Tocca il mittente per leggere prima l’email: resterà non letta e non cambierà nulla. In Pulizia spam, le immagini dal web non vengono caricate, così il mittente non può sapere che l’hai aperta. Non ti verrà chiesto di nuovo per i mittenti che hai già valutato. Se in un giorno non arrivano newsletter o spam, non viene creata un’attività. Queste attività non inviano mai notifiche.

Quando hai valutato tutti i mittenti, l’attività risulta completata e mostra **Segna come completata**.

**Riepilogo giornaliero** seleziona le poche newsletter che vale la pena leggere e le raccoglie in un’unica attività al giorno. Per ciascuna spiega in una riga perché potrebbe interessarti. Tocca una newsletter per leggere l’email oppure usa **Apri nella tua posta**. La routine considera solo le newsletter: mai email di persone, ricevute o mittenti da cui ti sei disiscritto, e mai email che hai già letto. Se non trova nulla di interessante, non crea un’attività.

Impara cosa ti interessa da ciò che apri, metti in evidenza o archivi senza leggere, e da **Altri così** e **Meno così** su ogni selezione. Gli argomenti usati per le selezioni sono nella scheda della routine, sotto **Più su** e **Meno su**. Rimuovi un argomento con × oppure aggiungine uno. Quelli tratteggiati sono stati individuati dalla routine. Un nuovo riepilogo sostituisce quello ancora aperto e non invia mai notifiche.

Legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter e fa una breve domanda alla tua IA, entro un limite giornaliero, per contenere i costi. Con **Cambia quando** imposti l’orario. Se modifichi le istruzioni, la routine viene eseguita come qualsiasi altra, seguendo le tue istruzioni.

**Compleanni** crea un’attività per ogni persona a te vicina che compie gli anni oggi: persone a cui scrivi tu, come amici, familiari e contatti abituali. Per ognuna prepara un breve messaggio di auguri nel canale che usi di solito con quella persona, come la chat di WhatsApp o la conversazione email, nella sua lingua. Il messaggio viene inviato solo quando lo invii tu. Se non ci sono compleanni, non viene creata un’attività.

I compleanni vengono presi dai tuoi calendari (gli eventi di compleanno di Google e il calendario Compleanni, che vengono letti ogni mattina anche se non sono sincronizzati, e il calendario Compleanni di Outlook), dai contatti Google su una Machine autogestita e da un campo data chiamato Birthday per una persona nel Graph. Se non è ancora registrato nessun compleanno, il risultato mostra **Non ci sono ancora informazioni sui compleanni** e spiega come aggiungerne.

**Importa i compleanni da Facebook**: dopo aver attivato Compleanni, un’attività ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e The Machine aprirà la pagina nel proprio browser, scorrerà fino a caricare tutti i mesi e leggerà il nome e il compleanno di ogni amico. Ti mostra quanti ne ha trovati e chi corrisponde a persone nel tuo Graph in base al nome e al cognome. I nomi condivisi da più persone vengono ignorati e inseriti nell’elenco.

Solo **Salva** registra i dati, nella pagina di ogni persona: il compleanno e, se la persona non ha ancora una foto, l’immagine del profilo Facebook. Un compleanno o una foto che hai già impostato non vengono modificati, e una foto già presente non viene mai sostituita. Non viene scritto nulla su Facebook.

La routine non esegue di nuovo l’importazione da sola: per farlo, tocca **Importa di nuovo** nell’attività. Il browser deve avere una sessione Facebook attiva. In caso contrario, tocca **Accedi a Facebook** nell’attività e accedi da lì. Una volta effettuato l’accesso, la pagina viene letta automaticamente. The Machine non accede mai al posto tuo.

Gli amici che non sono presenti nel tuo Graph vengono conteggiati e vengono mostrati alcuni nomi. **Aggiungi … come contatti personali** li aggiunge tutti insieme, anche dopo aver toccato Salva: ciascuno con il proprio nome e compleanno, senza condividerli con una Fleet di lavoro. I nomi già presenti nel Graph o appartenuti a persone che hai eliminato definitivamente vengono ignorati. I promemoria di compleanno vengono comunque creati solo per le persone a cui scrivi.

Con **Annulla** nell’attività puoi rimuovere esattamente quelle persone, anche dopo aver toccato **Importa di nuovo**.

**Abbonamenti e prove** legge una volta al mese le ricevute, le fatture e gli avvisi di rinnovo e raccoglie gli abbonamenti in un’unica attività: il costo, la prossima data di addebito e un avviso se una prova sta per terminare o il prezzo aumenta. Vengono elencati solo gli abbonamenti identificati con certezza. Se non ne trova, non crea un’attività.

Per ogni abbonamento, scegli **Tieni** o **Disdici**. Non ti verrà chiesto di nuovo per quelli che tieni, a meno che il prezzo non cambi. **Disdici** mostra la pagina per annullare l’abbonamento oppure prepara una bozza in cui chiedi di annullarlo. La bozza viene inviata solo quando la invii tu. Tra un’esecuzione e l’altra, la routine controlla ogni giorno e crea un’attività quando una prova o un rinnovo comporta un addebito entro 7 giorni.

**Restare in contatto** ti ricorda ogni tanto di farti sentire con qualcuno a cui tieni, solo quando c’è un motivo concreto. Nella scheda, scegli chi includere da un breve elenco di persone con cui scambi messaggi da mesi, in entrambe le direzioni. Rimuovi una persona con ×.

Ricevi un promemoria solo se è passato molto più tempo del solito dall’ultima conversazione e c’è qualcosa di preciso da dire: una notizia che ti ha condiviso, una promessa ancora in sospeso o un messaggio a cui non hai mai risposto. Il promemoria è un’unica attività, con il motivo e un breve messaggio preparato nel canale che usi di solito con quella persona, nella sua lingua. Il messaggio viene inviato solo quando lo invii tu. Se non c’è nulla da dire, non viene creata un’attività.

Vengono inviati al massimo due promemoria a settimana e uno per persona al mese. Non ne ricevi per chi hai sentito di recente. Se tocchi **Non serve** su un promemoria, la routine aspetta più a lungo prima di segnalare di nuovo quella persona, e aspetta ancora di più ogni volta. Non invia mai notifiche e resta personale: non viene mai condivisa con una Fleet di lavoro.

**Occasioni di seconda mano** tiene d’occhio una ricerca su un sito di annunci di seconda mano, come Marktplaats, Vinted, eBay o Facebook Marketplace. Cerca sul sito con i filtri che vuoi, copia l’indirizzo dei risultati e incollalo dopo aver toccato **Aggiungi**. Se vuoi, aggiungi filtri con parole tue, per esempio «sotto i 300, entro 30 km, senza “per pezzi di ricambio”». Ogni ricerca è una routine a sé, quindi aggiungila di nuovo per crearne un’altra.

Ogni 3 ore apre la ricerca nel browser di The Machine e cerca annunci che non ha ancora visto. Prezzo, distanza e parole da escludere vengono controllati prima, con codice semplice.

Ogni nuovo annuncio che supera i filtri viene aperto e la tua IA ne valuta le condizioni dalla foto e dalla descrizione, e il venditore dalle recensioni, dalla valutazione e dall’età dell’account. Gli annunci migliori vengono raccolti in un’unica attività, ciascuno con foto, titolo, prezzo e un breve giudizio. Tocca un annuncio per aprirlo nel browser di The Machine.

Mentre l’attività è aperta, le nuove occasioni vengono aggiunte in cima, il conteggio aumenta e ricevi di nuovo una notifica, perché le buone offerte finiscono in fretta. Segna l’attività come completata e la prossima occasione ne avvia una nuova. Se un’esecuzione non trova nulla di interessante, non cambia nulla.

La routine è prudente e contenuta nei costi: legge la ricerca una volta per esecuzione, apre al massimo 6 annunci per esecuzione con una pausa tra uno e l’altro e controlla al massimo 40 annunci al giorno per tutte le tue ricerche. Ogni controllo consiste in una breve domanda alla tua IA con una foto. Alla prima esecuzione controlla gli annunci più recenti e segna gli altri come già visti, così le esecuzioni successive mostrano solo le novità.

Se il sito chiede di accedere, mostra una verifica per i robot o impedisce la lettura, un’attività te lo segnala e mostra **Apri** per vedere la pagina nel browser di The Machine. Accedi o completa la verifica personalmente da lì: all’esecuzione successiva la pagina verrà letta di nuovo. The Machine non accede né supera verifiche al posto tuo e non contatta mai i venditori, non fa offerte e non acquista.

Con **Modifica ricerca** nella scheda della routine puoi inserire un nuovo indirizzo o modificare i filtri. Con **Cambia quando** puoi scegliere un’altra frequenza, per esempio «ogni 6 ore».

**Riordini** legge le email di conferma degli ordini dei negozi online e individua i prodotti che acquisti regolarmente, come caffè, cibo per animali o vitamine. Quando è probabile che tu debba ricomprarne uno, crea un’attività con il prodotto, il negozio, l’ultimo prezzo e la data dell’ultimo acquisto. Con **Apri nel negozio** puoi visitare la pagina del prodotto e acquistarlo tu. Non viene mai fatto un acquisto al posto tuo.

Servono almeno tre ordini dello stesso prodotto a intervalli regolari, quindi un acquisto singolo o un intervallo insolito non genera un’attività. Al momento la routine legge i negozi che usano Shopify. A ogni esecuzione, la tua IA legge solo le nuove email d’ordine di questi negozi, con una breve domanda. Queste attività non inviano notifiche e un nuovo ordine dello stesso prodotto chiude l’attività aperta.

Finché una routine modello mantiene le istruzioni originali, viene eseguita con il proprio codice, senza usare il tuo piano IA (Pulizia spam elenca prima con il codice le nuove email di mittenti sconosciuti e pone una breve domanda alla tua IA solo se ne trova; Restare in contatto pone domande solo sulle una o due persone selezionate). Se cambi il nome, la routine continua a funzionare allo stesso modo. Quando modifichi le istruzioni, viene eseguita come qualsiasi altra routine, seguendo le tue istruzioni.

Pulizia newsletter e Pulizia spam continuano a creare la stessa attività, con una scelta per ogni email. Se modifichi Compleanni, il risultato mostra al massimo una bozza, non un’attività per persona. In **Modifica**, tocca **Torna al modello** per ripristinare le istruzioni originali.

## Cosa fa una routine

All’orario impostato, la tua Machine legge ciò che serve, per esempio i messaggi, le riunioni e il Graph, e mostra il risultato nella pagina Routine. Ogni risultato indica **Pronta**, **Niente di nuovo** con il motivo oppure **Non ha funzionato** con il motivo. Se un’esecuzione termina senza un risultato, viene considerata non riuscita, mai completata.

Le routine si limitano a leggere: messaggi, pagine web, GitHub e siti come X nel browser. Non inviano messaggi, non rispondono, non pubblicano e non modificano nulla. Aprono le pagine trovate in ciò che hanno letto o in una ricerca, gli indirizzi di pagine semplici e i siti conosciuti, mai un indirizzo creato per trasmettere ciò che hanno letto. Solo un modello può modificare la posta, e solo dopo una tua conferma nell’attività.

Se il lavoro di una routine dovrebbe concludersi con un post o un messaggio, la routine esegue tutti i passaggi fino a quello e mostra la bozza, per esempio **Pubblicheresti su X:**. Dopo un’esecuzione effettiva, la bozza diventa un’attività da approvare. Un’esecuzione di prova la mostra soltanto.

Il nome indica l’argomento e dove va il risultato. **Dalla tua routine** apre la routine. Il pulsante indica il passaggio, per esempio **Prepara il post**: prepara il post, ma non pubblica nulla. Puoi pubblicarlo dal risultato. Se The Machine non può farlo al posto tuo, il pulsante apre la pagina in cui puoi pubblicarlo.

L’attività inizia nell’area dell’account da cui verrà inviata, per esempio Lavoro per l’account X della tua azienda, quindi non ti chiede mai di spostarla.

Un’esecuzione può seguire le tue [skill](skills.md) attive, scelte in base a ciò che fa la routine: vengono lette per intero solo quelle pertinenti. Il risultato le elenca sotto **Usate:**. Una skill non fa mai sì che una routine invii o modifichi qualcosa.

Le tue routine si trovano in **Le tue routine**, sotto gli eventuali suggerimenti. I risultati lunghi vengono ridotti a un’anteprima breve. Tocca **Mostra altro** o il risultato per aprirlo.

Ogni esecuzione conosce il risultato precedente e può indicare cosa è cambiato da allora.

Dopo un’esecuzione riuscita, la tua Machine può scriversi una ricetta per la parte di lettura che si ripete, per esempio quali email o modifiche di GitHub controllare. Le esecuzioni successive controllano prima quelle informazioni con codice semplice, mentre l’IA seleziona e scrive solo ciò che conta, usando meno token. La ricetta si limita a leggere. Se smette di funzionare, la routine torna a leggere da sola e la corregge. La ricetta compare sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine era spenta o occupata, le esecuzioni saltate non si accumulano: viene eseguita una sola volta la più recente. Ogni data viene eseguita una sola volta, anche dopo un riavvio.

Le routine vengono eseguite una alla volta e aspettano quando l’utilizzo del tuo piano IA è basso, come tutti i lavori in background. **Esegui ora** avvia subito la routine; il risultato compare sulla scheda quando è pronto.

## Modificare o interrompere una routine

Le opzioni si trovano nel menu ⋯ della routine. **Modifica** cambia il nome e le istruzioni, ma mantiene la frequenza e i risultati precedenti. **Cambia quando** imposta una nuova frequenza usando parole tue, per esempio «ogni giorno feriale alle 8». Entrambe le opzioni mostrano **Salva** e **Annulla**. Su un computer puoi annullare anche premendo Esc o facendo clic fuori.

In **Modifica**, **Provalo** esegue una volta le nuove istruzioni e mostra il risultato. La routine resta invariata finché non tocchi **Salva**.

**Metti in pausa** interrompe le esecuzioni finché non tocchi **Riprendi** sulla scheda. Le routine in pausa si trovano sotto **In pausa**, dopo le tue routine, e le esecuzioni saltate durante la pausa non verranno recuperate. **Ferma** interrompe definitivamente una routine.

Puoi avere fino a 20 routine, comprese quelle in pausa. Ferma una routine per aggiungerne un’altra.

Quando tocchi **Chiedi modifiche** sull’attività di una routine, oppure scrivi nella chat della routine, e la richiesta vale per tutte le esecuzioni, per esempio «non usare mai emoji», l’attività ti propone **Cambia anche la routine**. La trovi nell’attività e nella chat, sotto la risposta. Viene mostrato cosa cambierebbe nelle istruzioni della routine, che cambia solo quando tocchi **Cambiala**. **Lasciala così** mantiene le istruzioni attuali. Se correggi solo quella bozza, non viene proposta alcuna modifica.

## Avanzate: passaggi di script

Non serve scrivere script: spiega con parole tue cosa deve fare una routine e la tua Machine penserà al resto.

Per chi vuole più controllo, una routine può anche eseguire comandi personalizzati sulla tua Machine. Dal menu ⋯, scegli **Avanzate: passaggi di script**. **Modifica** li mostra solo quando la routine ne contiene. **Recupera dati** esegue prima un comando, nella sua cartella, oppure nella tua cartella home se non ne indichi una, per un massimo di secondi prestabilito. Ciò che stampa viene passato alla routine per l’elaborazione. Se non specifichi istruzioni, il risultato è ciò che stampa.

**Verifica** riceve come input il risultato al termine dell’esecuzione. Se il comando termina con un errore, la routine mostra **Non ha funzionato** e il messaggio della verifica. Un comando di Recupera dati non riuscito mostra lo stesso messaggio.

Ogni comando deve essere scritto su una sola riga e viene eseguito senza shell: non sono ammessi pipe o variabili. I passaggi di script sono impostati da te solo nella dashboard. Anche un’esecuzione di prova e **Provalo** eseguono Recupera dati e lo indicano. Non inviano né conservano nulla. Una routine non invia mai nulla, quindi i passaggi di script devono limitarsi a leggere.

## Dai tuoi job di OpenClaw

Se in precedenza hai creato job programmati in OpenClaw, la tua Machine li legge, senza modificarli, e propone come routine quelli compatibili, sotto **Suggerito**. Ogni job viene eseguito una volta, così puoi vedere un risultato effettivo.

La routine mantiene le correzioni che hai apportato al job ed esclude ciò che ha inviato o pubblicato. Se un job eseguiva uno script o leggeva dati raccolti da un job con script, lo script viene aggiunto come Recupera dati. **Aggiungi** lo trasforma in una routine, mentre **No, grazie** fa sì che il job non venga più proposto. Un job che ti ricordava di fare qualcosa viene invece proposto in To-do come attività ricorrente.

Prima di aggiungere un suggerimento, puoi modificarlo dal menu ⋯ con **Modifica** e **Cambia quando**, come per qualsiasi routine. **Esegui di nuovo** lo avvia subito con le istruzioni attuali, per vedere risultati più recenti, per esempio dopo un fine settimana tranquillo. La routine si limita a leggere, viene eseguita una volta per tocco e sostituisce il risultato precedente con quello nuovo.

Puoi avere al massimo tre suggerimenti in attesa. Dopo una settimana di esecuzioni riuscite, la routine chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se tocchi **Disattiva**. Puoi riattivarlo in OpenClaw. **Tienilo** lascia attivi entrambi.

## In base alle tue attività

La tua Machine rileva anche le attività che svolgi con regolarità e le propone come routine sotto **Suggerito**, anche senza OpenClaw. Cerca:

- la stessa richiesta almeno tre volte di fila, per esempio «riepiloga i ticket di assistenza aperti» ogni lunedì;
- un’email che invii regolarmente, per esempio un resoconto settimanale al tuo team;
- newsletter e email di aggiornamento che arrivano ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una alla volta sempre alla stessa persona, per esempio le email della scuola e delle attività extrascolastiche al tuo partner: un riepilogo settimanale evita di doverle inoltrare;
- la stessa richiesta a cui rispondi regolarmente, per esempio un’approvazione mensile per la stessa persona.

Ogni suggerimento spiega cosa ha rilevato, per esempio «Richiesto 4 volte di fila» o «Inoltrate 6 email a Sam in 3 settimane», e viene eseguito una volta così puoi vedere un risultato effettivo. Può essere un riepilogo del team, un aggiornamento prima di una chiamata settimanale, un riepilogo dell’assistenza o dello sviluppo, un controllo dei tuoi numeri o un riepilogo delle newsletter che ricevi.

Vengono suggerite solo routine specifiche per te e chiaramente utili: un riepilogo di notizie può includere solo le tue newsletter, mai contenuti generici. Se non trova nulla di adatto, non mostra suggerimenti.

La tua Machine controlla al massimo una volta al giorno e propone al massimo un nuovo suggerimento a settimana, senza inviare notifiche. Se tocchi **No, grazie**, quel suggerimento non verrà più proposto. Le email inoltrate e le risposte restano associate all’account da cui sono state inviate, quindi Lavoro e Personale non si mescolano. Tutto resta sulla tua Machine. Un’attività che completi con regolarità viene invece proposta come attività ricorrente.

## Routine e attività ricorrenti

Un’[attività ricorrente](recurring.md) ti ricorda di fare qualcosa. Una routine è un’attività che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per «pagare l’affitto il primo del mese» e una routine per «ogni venerdì, dimmi quali trattative sono ferme».
