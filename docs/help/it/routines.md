---
title: Routine
area: cards
summary: Attività che la tua Machine svolge da sola, a intervalli regolari, come un riepilogo del lunedì sulle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 57b97c44b031845f
---
## Creane una

Apri **Routine** nella barra laterale e scrivi in una riga cosa deve fare e quando: «ogni lunedì alle 9, riepiloga le trattative aperte» oppure «ogni mattina nei giorni feriali, elenca le email a cui devo ancora rispondere». Poi tocca **Aggiungi**.

Se non specifichi un orario, la routine viene eseguita alle 8:00, secondo l’ora della tua Machine. La prima volta che viene eseguita, le viene assegnato un nome breve.

**Aggiungi** esegue prima una prova, così puoi vedere il risultato prima di confermare. Non viene inviato né salvato nulla. Poi **Aggiungi** la imposta per essere eseguita a intervalli regolari, **Cambia** prova altre parole o un nuovo nome e **Annulla** la elimina.

## Modelli

In fondo a Routine, sotto **Modelli**, tocca **Aggiungi** per attivare una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30 (Pulizia spam ogni ora, Occasioni di seconda mano ogni 3 ore, Abbonamenti e prove una volta al mese). La scheda mostra le parole usate, come per qualsiasi routine, e **Modifica** permette di cambiarle o di cambiare il nome.

Quando arrivano molte newsletter e Pulizia newsletter è disattivata (almeno 25 in una settimana, da almeno 5 mittenti), sopra le tue attività compare una riga che indica quante ne sono arrivate e cosa farebbe la routine, con **Attiva** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo quando, in una settimana, hai spostato manualmente almeno 5 email nella cartella spam. **Attiva** la aggiunge come **Aggiungi** qui. Se tocchi **No, grazie**, non ti verrà proposta di nuovo. Lo stesso vale per un modello che avevi già usato.

**Pulizia newsletter** crea un’attività per ogni area, lavoro e personale, con le newsletter arrivate nell’ultimo giorno. Per ognuna puoi scegliere **Tieni** o **Disiscriviti**. Per disiscriverti, usa il link per farlo con un clic incluso nella mailing list, oppure invia un’email di disiscrizione dal tuo indirizzo, se l’invio è attivo. Altrimenti, la tua Machine si disiscrive dalla pagina della mailing list usando il suo browser. Se serve accedere, completare un captcha o scegliere un’opzione, lo fai tu: la riga spiega il motivo e mostra **Apri la pagina di disiscrizione**.

Vuoi evitare di creare attività per una mailing list, ma continuare a ricevere le sue email? Scrivi «Niente da questa lista deve creare un’attività» nella chat di una delle sue email.

Le ricevute, gli ordini e gli avvisi di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come un Google Group, vengono elencate sotto il nome di chi le ha scritte e non ti disiscrivono mai dal gruppo. Se il mittente non offre un modo per disiscriversi, la riga mostra **Disiscriviti a mano**.

**Pulizia spam** crea un’attività per ogni area con le email che sembrano spam e provengono da mittenti sconosciuti. Per ognuna puoi scegliere **Spam** o **Non è spam**. Outlook sposta lo spam nella cartella Posta indesiderata e Gmail lo contrassegna come spam. La routine controlla ogni ora, quindi di solito lo spam è già lì quando arrivi. Le nuove email di spam vengono aggiunte alla stessa attività finché è aperta.

Se Gmail è collegato in sola lettura, come su una Machine ospitata, non è possibile spostare le email nella cartella spam. In questo caso, **Spam** apre un link per contrassegnare l’email come spam in Gmail e la tua Machine ricorda il mittente come spam. Se non hai collegato un account email, al posto di **Aggiungi** il modello mostra **Collega la posta**.

Un mittente è sconosciuto se non gli hai mai scritto. Un «Re:» conta come conversazione solo in una discussione a cui hai partecipato. Se un’email di un mittente che hai contrassegnato come spam, nell’attività o nella tua casella di posta, riesce a passare di nuovo, compare nell’attività successiva con l’indicazione **Già segnato come spam**. Anche le email che hai spostato tu nello spam aiutano la routine a individuare messaggi simili.

Non cambia nulla finché non confermi nell’attività. Tocca il mittente per leggere prima l’email: resta non letta e non cambia nulla. Nelle attività di Pulizia spam, le immagini dal web non vengono caricate, così il mittente non può vedere che hai aperto l’email. Non ti verrà chiesto di nuovo dei mittenti per cui hai già deciso. Se in un giorno non ci sono newsletter o spam, non viene creata nessuna attività. Queste attività non inviano mai notifiche.

Quando hai deciso per tutti i mittenti, l’attività risulta completata e mostra **Segna come completata**.

**Riepilogo giornaliero** raccoglie, una volta al giorno e in un’unica attività, le poche newsletter che meritano il tuo tempo. Per ognuna spiega in una riga perché potrebbe interessarti. Toccala per leggere l’email oppure scegli **Apri nella tua posta**. Include solo newsletter: mai email di persone, ricevute o mittenti da cui ti sei disiscritto, e mai email che hai già letto. Se non c’è niente di interessante, non viene creata nessuna attività.

La routine impara cosa ti interessa da ciò che apri, contrassegni con una stella o archivi senza leggere, e dalle opzioni **Altri così** e **Meno così** su ogni suggerimento. Gli argomenti che seleziona sono indicati nella scheda della routine, sotto **Più su** e **Meno su**. Rimuovine uno con × o aggiungine uno. Quelli tratteggiati sono stati individuati autonomamente. Un nuovo riepilogo sostituisce quello ancora aperto e non invia mai notifiche.

La routine legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter, poi pone alla tua IA una breve domanda su ciascuna, con un limite giornaliero per contenere i costi. **Cambia quando** modifica l’orario. Una volta modificate le parole, la routine viene eseguita come qualsiasi altra, seguendo le tue indicazioni.

**Compleanni** crea un’attività per ogni persona a te vicina che compie gli anni oggi: persone a cui scrivi direttamente, come amici, familiari e contatti abituali. Per ognuna prepara un breve messaggio di auguri nel canale che usi di solito con quella persona, per esempio nella sua chat di WhatsApp o nella conversazione email, e nella sua lingua. Il messaggio parte solo quando lo invii tu. Se non ci sono compleanni, non viene creata nessuna attività.

I compleanni vengono recuperati dai tuoi calendari (gli eventi di compleanno di Google e il calendario Compleanni, letti ogni mattina anche se non sono sincronizzati, e il calendario Compleanni di Outlook), dai tuoi contatti Google su una Machine ospitata autonomamente e da un campo data chiamato Birthday nella scheda di una persona in Graph. Se non è ancora presente nessun compleanno, il risultato mostra **Nessuna informazione sui compleanni** e spiega come aggiungerne.

**Importa i compleanni da Facebook**: dopo aver attivato Compleanni, un’attività ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e la tua Machine apre la pagina nel suo browser, scorre finché non sono caricati tutti i mesi e legge il nome e il compleanno di ogni amico. Mostra quanti ne ha trovati e quali corrispondono alle persone in Graph in base al nome e al cognome. Se più persone hanno lo stesso nome, vengono ignorate e indicate nell’elenco.

Solo **Salva** li aggiunge alla scheda di ogni persona: il compleanno e, se non ha già una foto, la foto del profilo Facebook. Un compleanno o una foto già impostati non vengono modificati e una foto esistente non viene mai sostituita. Non viene scritto nulla su Facebook.

La routine non rilegge la pagina da sola: per farlo, tocca **Importa di nuovo** nell’attività. Devi aver effettuato l’accesso a Facebook nel browser. Se non hai effettuato l’accesso, tocca **Accedi a Facebook** nell’attività e accedi da lì. Una volta effettuato l’accesso, la pagina viene letta automaticamente. La tua Machine non accede mai al posto tuo.

Gli amici che non sono presenti in Graph vengono conteggiati e accompagnati da alcuni nomi. **Aggiungi … come contatti personali** li aggiunge tutti insieme, anche dopo aver toccato Salva: per ognuno crea una scheda con nome e compleanno, che non vengono mai condivisi con una Fleet di lavoro. Le persone con un nome già presente in Graph, o che erano state eliminate definitivamente, vengono ignorate. I promemoria dei compleanni continuano ad arrivare solo per le persone a cui scrivi.

Con **Annulla** nell’attività vengono rimosse esattamente le persone aggiunte, anche dopo aver toccato **Importa di nuovo**.

**Abbonamenti e prove** legge una volta al mese le ricevute, le fatture e gli avvisi di rinnovo e raccoglie gli abbonamenti in un’unica attività: il costo di ciascuno, la prossima data di addebito e un avviso se una prova sta per scadere o il prezzo aumenta. Elenca solo quelli di cui è sicura. Se non trova nulla, non viene creata nessuna attività.

Per ognuno, scegli **Tieni** o **Disdici**. Se scegli di tenerlo, non ti verrà chiesto di nuovo, a meno che il prezzo non cambi. **Disdici** apre la pagina per annullare l’abbonamento oppure prepara un messaggio per chiederne l’annullamento, che parte solo quando lo invii tu. Tra un’esecuzione e l’altra, la routine controlla ogni giorno e crea un’attività se una prova o un rinnovo verrà addebitato entro 7 giorni.

**Restare in contatto** ti ricorda ogni tanto di farti sentire con una persona a te vicina, ma solo quando c’è un motivo concreto. Nella scheda, scegli chi includere da un breve elenco di persone con cui comunichi direttamente, in entrambe le direzioni, da diversi mesi. Tocca × per rimuovere una persona.

Ricevi un promemoria solo se è passato molto più tempo del solito dall’ultima conversazione e c’è qualcosa di preciso da dire: una novità che la persona ha condiviso, anche nel riepilogo sulla sua scheda, una promessa ancora in sospeso o un messaggio a cui non hai mai risposto.

Se una novità riguarda una data futura, come un trasloco il mese prossimo, la routine la ricontrolla subito dopo quella data, insieme ai messaggi più recenti. Crea un’unica attività con il motivo e un breve messaggio preparato nel canale che usi di solito con quella persona, nella sua lingua. Il messaggio parte solo quando lo invii tu. Se non c’è niente da dire, non viene creata nessuna attività.

La routine invia al massimo due promemoria a settimana, uno per persona al mese, e non ne invia a chi hai sentito di recente. Se tocchi **Non serve** su un promemoria, la routine aspetta più a lungo prima di riproporlo per quella persona, e aspetta ancora di più ogni volta successiva. Non invia mai notifiche e resta personale: non viene mai condivisa con una Fleet di lavoro e non si basa mai su contenuti arrivati nei tuoi account di lavoro.

**Occasioni di seconda mano** monitora una ricerca su un sito di articoli usati, come Marktplaats, Vinted, eBay o Facebook Marketplace. Cerca sul sito con i filtri che vuoi, copia l’indirizzo dei risultati e incollalo dopo aver toccato **Aggiungi**. Se vuoi, aggiungi filtri con parole tue, per esempio «meno di 300, entro 30 km, niente “per ricambi”». Ogni ricerca è una routine a sé, quindi aggiungila di nuovo per la ricerca successiva.

Ogni 3 ore, la tua Machine apre la ricerca nel suo browser e cerca gli annunci che non ha ancora visto. Prima controlla in codice semplice il prezzo, la distanza e le parole che hai escluso.

Ogni nuovo annuncio che supera questi controlli viene aperto e la tua IA ne valuta le condizioni in base alla foto e alla descrizione, e il venditore in base alle recensioni, alla valutazione e all’età dell’account. Gli annunci migliori vengono raccolti in un’unica attività, ognuno con foto, titolo, prezzo e un breve giudizio. Tocca un annuncio per aprirlo nel browser della tua Machine.

Mentre l’attività è aperta, le nuove occasioni vengono aggiunte in cima, il conteggio aumenta e ricevi un’altra notifica, perché le buone offerte durano poco. Segna l’attività come completata e la prossima occasione ne avvia una nuova. Se un’esecuzione non trova nulla di interessante, non cambia nulla.

La routine è discreta e contenuta nei costi: legge la ricerca una sola volta per esecuzione, apre al massimo 6 annunci per esecuzione con una pausa tra uno e l’altro e controlla al massimo 40 annunci al giorno in tutte le ricerche. Per ogni controllo, pone alla tua IA una sola domanda breve con una sola foto. La prima esecuzione controlla gli annunci più recenti e considera già visti gli altri, così le successive mostrano solo le novità.

Se il sito ti chiede di accedere, mostra un controllo per verificare che tu non sia un robot o impedisce la lettura, un’attività te lo segnala e mostra **Apri** per visualizzare la pagina nel browser della tua Machine. Accedi o completa il controllo personalmente: l’esecuzione successiva riproverà a leggere la pagina. La tua Machine non accede mai al posto tuo, non risolve i controlli e non contatta mai i venditori, non fa offerte e non acquista nulla.

**Modifica ricerca** nella scheda della routine permette di inserire un nuovo indirizzo o nuovi filtri. **Cambia quando** imposta un’altra frequenza, per esempio «ogni 6 ore».

**Riordini** legge le conferme d’ordine dei negozi online nella tua posta e nota cosa compri più volte, come caffè, cibo per animali o vitamine. Quando è probabile che sia ora di ricomprarlo, crea un’attività con l’articolo, il negozio, l’ultimo prezzo e la data dell’ultimo acquisto. **Apri nel negozio** porta alla pagina dell’articolo, dove puoi acquistarlo tu. Non viene acquistato nulla al posto tuo.

La routine deve trovare almeno tre ordini dello stesso articolo, effettuati con regolarità, quindi un acquisto occasionale o un intervallo insolito non crea un’attività. Per ora legge i negozi che usano Shopify. A ogni esecuzione, la tua IA legge solo le nuove email d’ordine di questi negozi, con una sola domanda breve. Queste attività non inviano mai notifiche e un nuovo ordine dello stesso articolo chiude l’attività aperta.

Finché una routine di un modello mantiene le parole del modello, viene eseguita usando il proprio codice, senza il tuo piano IA (Pulizia spam elenca prima in codice le nuove email di mittenti sconosciuti e pone alla tua IA una sola domanda breve solo se ne trova; Restare in contatto chiede informazioni solo sulle una o due persone selezionate). Se le dai un nuovo nome, questo comportamento non cambia. Una volta modificate le parole, viene eseguita come qualsiasi routine, seguendo le tue indicazioni.

Pulizia newsletter e Pulizia spam continuano a creare la stessa attività, con una scelta per ogni email. Una versione modificata di Compleanni mostra il risultato e al massimo una bozza, non un’attività per persona. In **Modifica**, tocca **Torna al modello** per ripristinare le parole originali.

## Cosa fa una routine

All’orario stabilito, la tua Machine legge ciò che serve, per esempio i tuoi messaggi, le riunioni e Graph, e mostra il risultato nella pagina Routine. Ogni risultato indica **Pronta**, **Niente di nuovo** con il motivo oppure **Non ha funzionato** con il motivo. Un’esecuzione che termina senza un risultato conta come non riuscita, mai come completata.

Le routine si limitano a leggere: i tuoi messaggi, le pagine web, GitHub e siti come X nel browser. Non inviano messaggi, non rispondono, non pubblicano e non modificano nulla. Aprono le pagine trovate in ciò che leggono o in una ricerca, indirizzi di pagine semplici e siti noti, mai un indirizzo creato per contenere ciò che hanno letto. Solo un modello può modificare le email, e solo ciò che confermi nella relativa attività.

Se il lavoro di una routine dovrebbe concludersi con un post o un messaggio, la routine esegue tutti i passaggi fino a quello e mostra la bozza, per esempio **Pubblicheresti su X:**. Dopo un’esecuzione reale, la bozza compare come attività da approvare; un’esecuzione di prova la mostra soltanto.

Il nome indica l’argomento e la destinazione, mentre **Dalla tua routine** sotto il nome apre la routine. Il pulsante indica il passaggio da eseguire, per esempio **Prepara il post**: prepara il contenuto, ma non pubblica nulla. Pubblicalo dal risultato. Se la tua Machine non può pubblicarlo al posto tuo, il pulsante apre la pagina in cui puoi farlo.

L’attività viene creata nell’area dell’account da cui verrà inviata, per esempio Lavoro per l’account X della tua azienda, così non ti viene mai chiesto di spostarla.

Un’esecuzione può seguire le tue [skill](skills.md) attive, selezionate in base a ciò che fa la routine: vengono lette per intero solo quelle pertinenti. Il risultato le elenca sotto **Usate:**. Una skill non fa mai inviare o modificare nulla a una routine.

Le tue routine si trovano sotto **Le tue routine**, dopo gli eventuali suggerimenti. I risultati lunghi vengono ridotti a un’anteprima breve: tocca **Mostra altro** o il risultato per aprirli.

Ogni esecuzione tiene conto del risultato precedente, così può indicare cosa è cambiato da allora.

Dopo un’esecuzione riuscita, la tua Machine può creare da sola una ricetta per le letture che si ripetono ogni volta, come le email o le modifiche a GitHub da controllare. Le esecuzioni successive leggono prima questi dati in codice semplice, poi l’IA seleziona quelli importanti e li riassume, usando meno token. La ricetta si limita a leggere. Se smette di funzionare, l’esecuzione legge autonomamente i dati e la corregge. La ricetta compare sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine era spenta o occupata, le esecuzioni saltate non si accumulano: ne viene eseguita una sola, la più recente. Ogni data viene eseguita una volta sola, anche dopo un riavvio.

Le routine vengono eseguite una alla volta e aspettano quando le risorse del tuo piano IA sono scarse, come tutti i processi in background. **Esegui ora** avvia subito la routine. Il risultato compare sulla scheda quando è pronto.

## Modifica o interrompi

Trovi queste opzioni nel menu ⋯ della routine. **Modifica** cambia il nome e cosa fa la routine, ma lascia invariati l’orario di esecuzione e i risultati ottenuti finora. **Cambia quando** imposta una nuova frequenza con parole tue, per esempio «ogni giorno feriale alle 8». Entrambe le opzioni mostrano **Salva** e **Annulla**. Da computer, puoi annullare anche premendo Esc o facendo clic all’esterno.

In **Modifica**, **Provalo** esegue una volta la routine con le nuove parole e ne mostra il risultato. La routine resta com’era fino a quando non tocchi **Salva**.

**Metti in pausa** interrompe le esecuzioni fino a quando non tocchi **Riprendi** sulla scheda. Le routine in pausa restano sotto **In pausa**, dopo le tue routine, e le esecuzioni saltate durante la pausa non vengono recuperate. **Ferma** interrompe definitivamente una routine.

Puoi avere fino a 20 routine, comprese quelle in pausa. Fermane una per aggiungerne un’altra.

Quando scegli **Chiedi modifiche** sull’attività di una routine o scrivi nella sua chat, e la tua nota vale per tutte le esecuzioni, per esempio «non usare mai emoji», l’attività propone **Cambia anche la routine**. L’opzione compare nell’attività e nella chat, sotto la risposta. Mostra quali parole della routine verranno modificate. La routine cambia solo quando tocchi **Cambiala**. **Lasciala così** non apporta modifiche. Se la correzione riguarda solo quella bozza, l’opzione non viene proposta.

## Avanzate: passaggi di script

Non serve uno script: descrivi con parole tue cosa deve fare una routine e la tua Machine penserà al resto.

Per chi ha più esperienza, una routine può anche eseguire comandi personalizzati sulla tua Machine. Nel menu ⋯, scegli **Avanzate: passaggi di script**. **Modifica** mostra i passaggi solo se la routine ne contiene già. **Recupera dati** esegue prima un comando, nella sua cartella (se vuota, nella cartella iniziale dell’utente), per il numero di secondi specificato. Ciò che il comando stampa viene passato all’esecuzione, che può usarlo. Se non ci sono altre istruzioni, il risultato è ciò che il comando stampa.

**Verifica** riceve il risultato come input al termine dell’esecuzione. Se termina con un errore, il risultato mostra **Non ha funzionato** e il messaggio restituito dal controllo. Se un comando di Recupera dati non riesce, viene mostrato lo stesso messaggio.

Un comando deve stare su una sola riga e viene eseguito senza shell: niente pipe o variabili. I passaggi di script sono tuoi e si impostano solo nella tua dashboard. Anche le esecuzioni di prova e **Provalo** eseguono Recupera dati e lo indicano. Non inviano né conservano nulla. Una routine non invia mai nulla, quindi un passaggio di script dovrebbe limitarsi a leggere.

## Dai tuoi job di OpenClaw

Se in passato hai creato job programmati in OpenClaw, la tua Machine li legge senza modificarli e propone come routine quelli più adatti, sotto **Suggerito**. Ognuno è stato eseguito una volta, quindi puoi vedere un risultato reale.

La routine conserva le tue correzioni al job ed esclude ciò che il job ha inviato o pubblicato. Se il job eseguiva uno script o leggeva dati raccolti da uno script, li include come Recupera dati. **Aggiungi** lo trasforma in una routine; **No, grazie** evita che il job ti venga proposto di nuovo. Se un job ti ricordava di fare qualcosa, comparirà invece su Attività come proposta di attività ricorrente.

Prima di aggiungere un suggerimento, puoi modificarlo come qualsiasi routine con **Modifica** e **Cambia quando** nel menu ⋯. **Esegui di nuovo** lo avvia subito con le parole attuali per vedere risultati più recenti, per esempio dopo un fine settimana tranquillo. Si limita a leggere, viene eseguito una volta per ogni tocco e il nuovo risultato sostituisce quello precedente.

Puoi avere al massimo tre suggerimenti in attesa. Dopo una settimana di esecuzioni riuscite, la routine chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se tocchi **Disattiva**. Puoi riattivarlo in OpenClaw. **Tienilo** lascia attivi entrambi.

## In base a quello che fai

La tua Machine rileva anche le attività che svolgi con regolarità e le propone come routine sotto **Suggerito**, anche se non usi OpenClaw. Cerca:

- la stessa richiesta almeno tre volte di seguito, per esempio «riepiloga i ticket di assistenza aperti» ogni lunedì;
- un’email che invii regolarmente, come un rapporto settimanale al tuo team;
- newsletter ed email di aggiornamento che arrivano ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una per una alla stessa persona, per esempio email della scuola o di un club al tuo partner: un riepilogo settimanale evita di doverle inoltrare;
- la stessa richiesta a cui rispondi con regolarità, come un’approvazione mensile per la stessa persona.

Ogni suggerimento spiega cosa ha rilevato, per esempio «Richiesto 4 volte di seguito» o «Inoltrate 6 email a Sam in 3 settimane», ed è stato eseguito una volta, così puoi vedere un risultato reale. Può essere un riepilogo del team, una breve preparazione prima di una riunione settimanale, un riepilogo dell’assistenza o dello sviluppo, un aggiornamento sui tuoi numeri o un riepilogo delle newsletter che ricevi.

La routine propone solo attività specifiche per te e chiaramente utili: un riepilogo di notizie può basarsi solo sulle tue newsletter, mai su notizie generiche. Se non trova nulla di adatto, non mostra suggerimenti.

Controlla al massimo una volta al giorno e propone al massimo un nuovo suggerimento a settimana, senza inviare notifiche. **No, grazie** evita che quel suggerimento ricompaia. Gli inoltri e le risposte restano associati all’account da cui sono stati inviati, così Lavoro e Personale non si mescolano. Tutto resta sulla tua Machine. Se completi regolarmente un’attività, viene proposta invece come attività ricorrente.

## Routine e attività ricorrenti

Un’[attività ricorrente](recurring.md) ti ricorda di fare qualcosa. Una routine è un’attività che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per «pagare l’affitto il primo del mese» e una routine per «ogni venerdì, dimmi quali trattative si sono fermate».
