---
title: Routine
area: cards
summary: Attività che la tua Machine svolge da sola a intervalli regolari, come un riepilogo del lunedì sulle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 6d74cb93df1bf494
---
## Creane una

Apri **Routine** nella barra laterale e descrivi in una riga cosa deve fare e quando: «ogni lunedì alle 9, riepiloga le mie trattative aperte» oppure «ogni mattina nei giorni feriali, elenca le email a cui devo ancora rispondere». Poi tocca **Aggiungi**.

Se non indichi un orario, la routine viene eseguita alle 8:00. Fa fede l’orologio della tua Machine. La prima esecuzione le assegna un nome breve.

Quando tocchi **Aggiungi**, prima viene eseguito un test, così puoi vedere il risultato prima di confermare. Non viene inviato né salvato nulla. Poi **Aggiungi** la attiva con la frequenza scelta, **Cambia** prova altre parole o un nuovo nome e **Annulla** la elimina.

## Modelli

Nella sezione **Modelli**, in fondo a Routine, tocca **Aggiungi** per attivare una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30 (Pulizia spam ogni ora, Occasioni di seconda mano ogni 3 ore, Abbonamenti e prove una volta al mese). La scheda mostra le istruzioni, come per qualsiasi routine, e **Modifica** permette di cambiarle o di modificarne il nome.

Quando arrivano molte newsletter e Pulizia newsletter è disattivata (almeno 25 in una settimana, da almeno 5 mittenti), sopra le tue attività compare un messaggio con il numero di newsletter ricevute e quello che farebbe la routine, con le opzioni **Attiva** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo quando, in una settimana, hai spostato manualmente almeno 5 email nella cartella dello spam. **Attiva** la aggiunge come farebbe **Aggiungi** qui. Se scegli **No, grazie**, non verrà più proposta. Lo stesso vale per un modello che avevi già attivato in precedenza.

**Pulizia newsletter** crea un’attività per ogni area (lavoro e personale) con le newsletter ricevute nell’ultimo giorno. Per ciascuna puoi scegliere **Tieni** o **Disiscriviti**. Per disiscriverti, usa il link per la disiscrizione con un clic della lista oppure, se l’invio è attivo, invia la richiesta dall’indirizzo associato. Altrimenti, la tua Machine si disiscrive dalla pagina della lista usando il proprio browser. Se la pagina richiede l’accesso, un captcha o una scelta, dovrai occupartene tu: la riga spiega il motivo e mostra **Apri la pagina di disiscrizione**.

Se vuoi solo evitare che una lista generi attività, ma continuare a riceverne le email, scrivi «Questa lista non deve generare attività» nella chat di una delle email.

Le ricevute, gli ordini e gli avvisi di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come Google Group, sono elencate sotto il nome di chi le ha scritte e non ti disiscrivono mai dal gruppo. Se il mittente non offre una modalità per disiscriversi, la riga mostra **Disiscriviti a mano**.

**Pulizia spam** crea un’attività per ogni area con le email che sembrano spam e provengono da mittenti sconosciuti. Per ciascuna puoi scegliere **Spam** o **Non è spam**. Outlook sposta i messaggi nella cartella Posta indesiderata, mentre Gmail li contrassegna come spam. La routine controlla ogni ora, quindi di solito lo spam è già stato individuato prima che tu lo veda. Le nuove email di spam vengono aggiunte alla stessa attività finché è aperta.

Se Gmail è collegato in sola lettura, come su una Machine ospitata, non è possibile spostare le email nello spam. In quel caso, **Spam** mostra un link per contrassegnare il messaggio in Gmail e la tua Machine memorizza il mittente come spam. Se non hai collegato un account email, al posto di **Aggiungi** il modello mostra **Collega la posta**.

Un mittente è sconosciuto se non gli hai mai scritto. «Re:» conta come conversazione solo in una discussione a cui hai partecipato. Se ricevi di nuovo un’email da un mittente che hai contrassegnato come spam, nell’attività o nella posta, la prossima attività mostra **Già segnato come spam**. Anche le email che hai spostato manualmente nello spam aiutano la routine a riconoscere messaggi simili.

Non cambia nulla finché non confermi la scelta nell’attività. Tocca il mittente per leggere prima l’email: resterà non letta e non cambierà nulla. Pulizia spam non carica le immagini dal web, quindi il mittente non può sapere che hai aperto il messaggio. Non ti verrà chiesto di nuovo cosa fare per i mittenti su cui hai già deciso. Se in un giorno non arrivano newsletter o spam, non viene creata alcuna attività. Queste attività non inviano mai notifiche.

Quando hai deciso cosa fare con tutti i mittenti, l’attività risulta completata e mostra **Segna come completata**.

**Riepilogo giornaliero** seleziona le poche newsletter che meritano la tua attenzione e le raccoglie una volta al giorno in un’unica attività. Per ciascuna spiega in una riga perché potrebbe interessarti. Tocca una newsletter per leggerla oppure scegli **Apri nella tua posta**. Include solo newsletter, mai email di persone, ricevute o mittenti da cui ti sei disiscritto. Esclude anche le email che hai già letto. Se non trova nulla di interessante, non crea un’attività.

La routine impara cosa ti interessa in base a ciò che apri, aggiungi ai preferiti o archivi senza leggere, e alle opzioni **Altri così** e **Meno così** disponibili per ogni proposta. Nella scheda della routine trovi gli argomenti selezionati, sotto **Più su** e **Meno su**. Tocca × per rimuovere un argomento o aggiungine uno. Gli argomenti tratteggiati sono stati individuati dalla routine. Un nuovo riepilogo sostituisce quello ancora aperto e non invia mai notifiche.

Legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter, poi pone alla tua IA una breve domanda al giorno, con un limite giornaliero, per contenere i costi. **Cambia quando** permette di impostare l’orario. Dopo che ne modifichi le istruzioni, la routine funziona come tutte le altre e segue le tue istruzioni.

**Compleanni** crea un’attività per ogni persona a te vicina che compie gli anni oggi: persone a cui scrivi direttamente, come amici, familiari e contatti abituali. Per ciascuna prepara un breve messaggio di auguri nel luogo in cui di solito vi sentite, come la chat WhatsApp o la discussione email, e nella sua lingua. Il messaggio parte solo quando lo invii tu. Se non ci sono compleanni, non viene creata alcuna attività.

I compleanni vengono recuperati dai tuoi calendari (gli eventi compleanno di Google e il calendario Compleanni, letti ogni mattina anche se non sono sincronizzati, e il calendario Compleanni di Outlook), dai tuoi contatti Google su una Machine ospitata in autonomia e da un campo data chiamato Birthday nella scheda di una persona in Graph. Se non è ancora registrato alcun compleanno, il risultato mostra **Ancora nessuna informazione sui compleanni** e spiega come aggiungerne.

**Importa i compleanni da Facebook**: dopo aver attivato Compleanni, un’attività ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e la tua Machine apre la pagina nel proprio browser, scorre finché non vengono caricati tutti i mesi e legge il nome e il compleanno di ogni amico. Ti mostra quanti ne ha trovati e quali corrispondono a persone in Graph, in base al nome e al cognome. I nomi associati a più di una persona vengono ignorati e mostrati nell’elenco.

Solo **Salva** importa i dati, nella pagina di ogni persona: il compleanno e, se la persona non ha ancora una foto, la sua immagine del profilo Facebook. I compleanni e le immagini che imposti lì rimangono invariati, e una foto già presente non viene mai sostituita. Non viene scritto nulla su Facebook.

La pagina non viene letta di nuovo automaticamente: per farlo, tocca **Importa di nuovo** nell’attività. Devi aver effettuato l’accesso a Facebook nel browser. Se non l’hai fatto, tocca **Accedi a Facebook** nell’attività e accedi da lì. Una volta effettuato l’accesso, la pagina viene letta automaticamente. La tua Machine non accede mai al posto tuo.

Le persone che non sono presenti in Graph vengono conteggiate e ne vengono mostrati alcuni nomi. **Aggiungi … come contatti personali** le aggiunge tutte insieme, anche dopo aver toccato Salva: ciascuna con il proprio nome e compleanno, mai condivisi con un Fleet di lavoro. Se una persona è già presente in Graph, oppure è stata eliminata definitivamente, viene ignorata. Continuerai a ricevere promemoria di compleanno solo per le persone a cui scrivi.

Tocca **Annulla** nell’attività per rimuovere esattamente le persone importate, anche dopo aver scelto **Importa di nuovo**.

**Abbonamenti e prove** legge una volta al mese le ricevute, le fatture e gli avvisi di rinnovo e raccoglie gli abbonamenti in un’unica attività. Per ciascuno mostra il costo, la data del prossimo addebito e un avviso se sta per terminare una prova o se il prezzo è aumentato. Elenca solo gli abbonamenti che riesce a identificare con certezza. Se non ne trova, non crea un’attività.

Per ciascuno, scegli **Tieni** o **Disdici**. Non ti verrà chiesto di nuovo se hai scelto di tenerlo, a meno che il prezzo non cambi. **Disdici** apre la pagina per annullare l’abbonamento oppure prepara una bozza con la richiesta di disdetta, che viene inviata solo se la invii tu. Tra un controllo e l’altro, la routine verifica ogni giorno e crea un’attività se una prova o un rinnovo verrà addebitato entro 7 giorni.

**Restare in contatto** ti ricorda ogni tanto di farti sentire con una persona a te vicina, solo quando c’è un motivo concreto. Nella scheda della routine, scegli le persone da includere da un breve elenco di chi senti direttamente, in entrambe le direzioni, da diversi mesi. Tocca × per rimuovere una persona.

Ricevi un promemoria solo se è passato molto più tempo del solito dall’ultima conversazione e c’è qualcosa di specifico di cui parlare: una novità che ti ha raccontato, anche nel riepilogo sulla sua pagina, una promessa ancora da mantenere o un messaggio a cui non hai mai risposto.

Se una novità riguarda una data futura, come un trasloco il mese prossimo, la routine la ricontrolla subito dopo quella data, insieme ai messaggi più recenti. Crea un’unica attività con il motivo e un breve messaggio preparato nel luogo in cui di solito vi sentite, nella lingua della persona. Il messaggio parte solo quando lo invii tu. Se non c’è nulla da dire, non viene creata un’attività.

Invia al massimo due promemoria a settimana e uno al mese per persona. Non ne invia a chi hai sentito di recente. Scegliendo **Non serve** per un promemoria, la routine aspetta più a lungo prima di riproporti quella persona, e prolunga l’attesa ogni volta.

Non invia mai notifiche e rimane nell’area Personale: non viene mai condivisa con un Fleet di lavoro, non si basa mai su attività lavorative (ciò che arriva sui tuoi account di lavoro, o una promessa o un fatto di lavoro) e, se possibile, prepara il messaggio in una conversazione personale.

**Occasioni di seconda mano** controlla una ricerca su un sito di articoli di seconda mano, come Marktplaats, Vinted, eBay o Facebook Marketplace. Fai una ricerca sul sito con i filtri che vuoi, copia l’indirizzo dei risultati e incollalo dopo aver toccato **Aggiungi**. Se vuoi, aggiungi filtri con parole tue, come «sotto i 300, entro 30 km, senza “da riparare”». Ogni ricerca è una routine a sé, quindi aggiungila separatamente.

Ogni 3 ore apre la ricerca nel browser della tua Machine e cerca annunci che non ha ancora visto. Prima controlla prezzo, distanza e parole da escludere, usando codice semplice.

Apre ogni nuovo annuncio che supera i filtri. La tua IA ne valuta le condizioni dalle foto e dalla descrizione, e il venditore in base alle recensioni, alla valutazione e all’anzianità dell’account. Gli annunci più interessanti vengono raccolti in un’unica attività, con foto, titolo, prezzo e un breve giudizio per ciascuno. Tocca un annuncio per aprirlo nel browser della tua Machine.

Finché l’attività è aperta, le nuove occasioni vengono aggiunte in cima, il conteggio aumenta e ricevi un’altra notifica, perché le buone offerte durano poco. Quando la contrassegni come completata, la prossima occasione crea una nuova attività. Se una ricerca non trova nulla di interessante, non cambia nulla.

La routine limita le richieste per non sovraccaricare i siti e contenere i costi: legge la ricerca una sola volta per esecuzione, apre al massimo 6 annunci per esecuzione con una pausa tra uno e l’altro e controlla al massimo 40 annunci al giorno in tutte le tue ricerche. Ogni controllo consiste in una breve domanda alla tua IA e una foto. La prima esecuzione controlla gli annunci più recenti e considera già visti gli altri, così le esecuzioni successive mostrano solo le novità.

Se il sito ti chiede di accedere, mostra una verifica per i robot o impedisce la lettura, un’attività te lo segnala e mostra **Apri** per visualizzare la pagina nel browser della tua Machine. Accedi o supera la verifica da lì; la routine leggerà di nuovo il sito alla prossima esecuzione. La tua Machine non accede mai al posto tuo, non supera le verifiche per te e non contatta, non fa offerte e non acquista mai nulla dai venditori.

**Modifica ricerca** nella scheda della routine permette di inserire un nuovo indirizzo o modificare i filtri. Con **Cambia quando** puoi impostare un’altra frequenza, ad esempio «ogni 6 ore».

**Riordini** legge le conferme d’ordine dei negozi online nella tua posta e individua gli acquisti ricorrenti, come caffè, cibo per animali o vitamine. Quando è probabile che un prodotto stia per finire, crea un’attività con il prodotto, il negozio, l’ultimo prezzo e la data dell’ultimo acquisto. **Apri nel negozio** ti porta alla pagina del prodotto, dove puoi acquistarlo tu. Non viene mai acquistato nulla per te.

Servono almeno tre ordini dello stesso prodotto a intervalli regolari. Un acquisto isolato o un intervallo insolito non genera un’attività. Per ora la routine legge gli ordini dei negozi che usano Shopify. A ogni esecuzione, la tua IA legge solo le nuove email d’ordine di questi negozi e pone un’unica domanda breve. Queste attività non inviano mai notifiche. Un nuovo ordine dello stesso prodotto chiude l’attività ancora aperta.

Finché una routine usa le istruzioni del modello, viene eseguita con il proprio codice, senza usare il piano IA (Pulizia spam elenca prima con codice le nuove email di mittenti sconosciuti e pone una breve domanda alla tua IA solo se ne trova; Restare in contatto chiede informazioni solo sulle una o due persone selezionate). Se le dai un nuovo nome, continua a funzionare così. Dopo che ne modifichi le istruzioni, funziona come tutte le altre e segue le tue istruzioni.

Pulizia newsletter e Pulizia spam continuano a creare la stessa attività, con una scelta per ogni email. Se modifichi Compleanni, la routine mostra il risultato e al massimo una bozza, non un’attività per persona. Tocca **Torna al modello** in **Modifica** per ripristinare le istruzioni originali.

## Cosa fa una routine

All’orario stabilito, la tua Machine legge ciò che le serve, come i messaggi, gli appuntamenti e Graph, e mostra il risultato nella pagina Routine. Ogni risultato indica **Pronta**, **Niente di nuovo** (con il motivo) oppure **Non ha funzionato** (con il motivo). Un’esecuzione che termina senza un risultato conta come non riuscita, mai come completata.

Le routine si limitano a leggere: messaggi, pagine web, GitHub e siti come X nel browser. Non inviano messaggi, non rispondono, non pubblicano e non modificano nulla. Aprono le pagine trovate in ciò che leggono o in una ricerca, indirizzi semplici e siti conosciuti, mai un indirizzo creato per trasmettere ciò che hanno letto. Solo un modello può modificare la posta, e solo dopo la tua conferma nell’attività.

Se il lavoro di una routine prevede la pubblicazione di un post o l’invio di un messaggio, la routine svolge tutti i passaggi fino a quel punto e mostra una bozza, come **Pubblicherebbe su X:**. Dopo un’esecuzione effettiva, la bozza diventa un’attività che puoi approvare. Un’esecuzione di prova la mostra soltanto.

Il nome indica l’argomento e dove va il risultato. Sotto, **Dalla tua routine** apre la routine. Il pulsante indica il passaggio, ad esempio **Prepara il post**: prepara il contenuto, ma non pubblica nulla. Puoi pubblicarlo dal risultato. Se la tua Machine non può farlo per te, il pulsante apre la pagina da cui puoi pubblicarlo.

L’attività viene creata nell’area dell’account da cui partirà il contenuto, ad esempio Lavoro per l’account X della tua azienda, così non dovrai spostarla.

Un’esecuzione può usare le [skill](skills.md) attive, selezionate in base a ciò che fa la routine: legge per intero solo quelle pertinenti. Il risultato le elenca sotto **Usate:**. Una skill non fa mai inviare o modificare nulla a una routine.

Le tue routine si trovano sotto **Le tue routine**, dopo gli eventuali suggerimenti. I risultati lunghi vengono ridotti a un’anteprima breve. Tocca **Mostra altro** o il risultato per aprirlo.

Ogni esecuzione tiene conto del risultato precedente, così può indicare cosa è cambiato da allora.

Dopo un’esecuzione riuscita, la tua Machine può preparare una ricetta per le operazioni di lettura che si ripetono sempre, ad esempio quali email o modifiche di GitHub controllare. Nelle esecuzioni successive, le legge prima usando codice semplice. Poi l’IA seleziona le informazioni rilevanti e le riassume, usando meno token. La ricetta si limita a leggere. Se smette di funzionare, la routine riprende a leggere da sola e la corregge. La ricetta compare sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine è spenta o occupata, le esecuzioni saltate non si accumulano: viene eseguita una sola volta la più recente. Ogni data viene elaborata una sola volta, anche dopo un riavvio.

Le routine vengono eseguite una alla volta e aspettano se il tuo piano IA ha poco utilizzo disponibile, come tutti i lavori in background. **Esegui ora** avvia subito la routine. Quando il risultato è pronto, compare sulla scheda.

## Modifica o interrompi una routine

Trovi queste opzioni nel menu ⋯ della routine. **Modifica** permette di cambiarne il nome e le istruzioni; l’orario e i risultati già ottenuti rimangono invariati. **Cambia quando** permette di impostare una nuova frequenza con parole tue, ad esempio «ogni giorno feriale alle 8». Entrambe le opzioni mostrano **Salva** e **Annulla**. Su un computer, anche Esc o un clic all’esterno annullano le modifiche.

In **Modifica**, **Provalo** esegue una volta le nuove istruzioni e mostra il risultato. La routine rimane invariata finché non tocchi **Salva**.

**Metti in pausa** interrompe le esecuzioni finché non tocchi **Riprendi** sulla scheda. Le routine in pausa si trovano sotto **In pausa**, dopo le tue routine, e le esecuzioni saltate durante la pausa non vengono recuperate. **Ferma** interrompe definitivamente una routine.

Puoi avere al massimo 20 routine, incluse quelle in pausa. Fermane una per aggiungerne un’altra.

Se scegli **Chiedi modifiche** nell’attività di una routine o scrivi nella sua chat, e la richiesta vale per tutte le esecuzioni, come «non usare mai le emoji», l’attività ti propone **Cambia anche la routine**. L’opzione compare nell’attività e nella chat, sotto la risposta. Vengono mostrate le modifiche alle istruzioni della routine, che cambieranno solo se tocchi **Cambiala**. **Lasciala così** mantiene tutto com’è. Se chiedi di correggere solo la bozza, l’opzione non viene proposta.

## Avanzate: passaggi di script

Non serve scrivere script: descrivi con parole tue cosa deve fare una routine e la tua Machine si occupa del resto.

Se hai esperienza, una routine può anche eseguire comandi personalizzati sulla tua Machine. Nel menu ⋯, scegli **Avanzate: passaggi di script**. **Modifica** mostra i passaggi solo se la routine ne contiene già. **Recupera dati** esegue prima un comando nella sua cartella (la tua cartella Inizio se il campo è vuoto), per il numero di secondi indicato. Il risultato del comando viene passato all’esecuzione per elaborarlo. Se non specifichi istruzioni, il risultato del comando diventa il risultato dell’esecuzione.

**Verifica** riceve il risultato come input dopo l’esecuzione. Se termina con un errore, l’esecuzione mostra **Non ha funzionato** e il messaggio restituito dalla verifica. Lo stesso succede se non riesce il comando Recupera dati.

Un comando deve stare su una sola riga e viene eseguito senza shell: non puoi usare pipe o variabili. I passaggi di script sono personalizzati e si impostano solo nella tua dashboard. Anche le esecuzioni di prova e **Provalo** eseguono Recupera dati e lo indicano, ma non inviano né salvano nulla. Una routine non invia mai nulla, quindi i passaggi di script dovrebbero limitarsi a leggere.

## Dai tuoi job di OpenClaw

Se in passato hai creato job pianificati in OpenClaw, la tua Machine li legge senza modificarli e propone come routine quelli compatibili, sotto **Suggerito**. Ogni job viene eseguito una volta, così puoi vedere un risultato reale.

La tua Machine conserva le correzioni apportate al job ed esclude ciò che ha inviato o pubblicato. Se un job eseguiva uno script o leggeva i dati raccolti da un job con script, lo script viene aggiunto come Recupera dati. **Aggiungi** trasforma il job in una routine. Se scegli **No, grazie**, il job non ti verrà più proposto. Un job che ti ricordava di fare qualcosa viene invece proposto come attività ricorrente nella sezione Attività.

Prima di aggiungere un suggerimento, puoi modificarlo dal menu ⋯: **Modifica** e **Cambia quando** funzionano come per qualsiasi routine. **Esegui di nuovo** lo esegue subito con le istruzioni attuali, così puoi vedere risultati più recenti, ad esempio dopo un fine settimana tranquillo. La routine si limita a leggere, viene eseguita una volta per tocco e il nuovo risultato sostituisce quello precedente.

Puoi avere al massimo tre suggerimenti in attesa. Dopo una settimana di esecuzioni riuscite, la routine ti chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se tocchi **Disattiva**. Puoi riattivarlo in OpenClaw. **Tienilo** lascia attivi entrambi.

## In base a ciò che fai

La tua Machine individua anche le attività lavorative che svolgi a intervalli regolari e le propone come routine sotto **Suggerito**, anche se non usi OpenClaw. Cerca:

- la stessa richiesta almeno tre volte di fila, ad esempio «riepiloga le richieste di assistenza aperte» ogni lunedì;
- un’email che invii regolarmente, come un rapporto settimanale al tuo team;
- newsletter e email di aggiornamento che arrivano ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una alla volta alla stessa persona, come i messaggi della scuola e delle attività extrascolastiche al tuo partner: un riepilogo settimanale evita di doverle inoltrare;
- la stessa richiesta a cui rispondi regolarmente, come un’approvazione mensile per la stessa persona.

Ogni suggerimento spiega cosa ha notato, ad esempio «Richiesto 4 volte di fila» o «Inoltrate 6 email a Sam in 3 settimane», e viene eseguito una volta, così puoi vedere un risultato reale. Può trattarsi, ad esempio, di un riepilogo del team, un promemoria prima della riunione settimanale, un riepilogo delle richieste di assistenza o delle attività di sviluppo, un aggiornamento sui tuoi numeri o un riepilogo delle newsletter che ricevi.

Vengono proposte solo attività specifiche per te e chiaramente utili: ad esempio, un riepilogo di notizie basato solo sulle tue newsletter, mai un riepilogo generico. Se non trova nulla di adatto, non propone niente.

La tua Machine controlla al massimo una volta al giorno e propone al massimo un nuovo suggerimento a settimana, senza inviare notifiche. Se scegli **No, grazie**, quel suggerimento non verrà più riproposto. Gli inoltri e le risposte rimangono associati all’account da cui sono stati inviati, quindi gli account di lavoro e personali non si mescolano. Tutto rimane sulla tua Machine. Un’attività che completi regolarmente viene proposta come attività ricorrente.

## Routine e attività ricorrenti

Un’[attività ricorrente](recurring.md) ti ricorda di fare qualcosa. Una routine è un lavoro che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per «pagare l’affitto il primo del mese» e una routine per «ogni venerdì, dimmi quali trattative sono ferme».
