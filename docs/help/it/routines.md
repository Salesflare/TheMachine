---
title: Routine
area: cards
summary: Attività che la tua Machine svolge da sola, a intervalli regolari, come un riepilogo del lunedì sulle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: b5704836b00227a5
---
## Creane una

Apri **Routine** nella barra laterale e scrivi in una riga cosa deve fare e quando: «ogni lunedì alle 9, riepiloga le trattative aperte» oppure «ogni mattina nei giorni feriali, elenca le email a cui devo ancora rispondere». Poi tocca **Aggiungi**.

Se non indichi un orario, la routine viene eseguita alle 8:00. L’orario è quello della tua Machine. La prima volta che viene eseguita, le viene assegnato un nome breve.

Quando tocchi **Aggiungi**, prima viene eseguita una prova, così puoi vedere il risultato prima di salvarla. Non viene inviato né salvato nulla. Poi **Aggiungi** la attiva e la fa seguire il suo ritmo, **Cambia** prova altre parole o un nuovo nome e **Annulla** la elimina.

## Modelli

Nella sezione **Modelli**, in fondo a Routine, **Aggiungi** attiva una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30 (Pulizia spam ogni ora, Occasioni di seconda mano ogni 3 ore, Abbonamenti e prove una volta al mese). La sua scheda mostra le parole che la descrivono, come per qualsiasi routine, e **Modifica** permette di cambiarle o di darle un altro nome.

Quando arrivano molte newsletter e Pulizia newsletter è disattivata (almeno 25 in una settimana, da almeno 5 mittenti), sopra le attività compare un messaggio che indica quante ne sono arrivate e cosa farebbe la routine, con le opzioni **Attivala** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo quando in una settimana hai spostato manualmente nello spam almeno 5 email. **Attivala** la aggiunge, proprio come **Aggiungi** qui. Se tocchi **No, grazie**, non verrà più proposta. Nemmeno un modello che avevi già usato verrà riproposto.

**Pulizia newsletter** crea un’attività per ogni area, lavoro e personale, con le newsletter arrivate nell’ultimo giorno. Per ciascuna puoi scegliere **Tieni** o **Disiscriviti**. Per disiscriverti, la routine usa il link per la disiscrizione con un solo clic oppure invia un’email di disiscrizione dal tuo indirizzo, se l’invio è attivo. Altrimenti, la tua Machine si disiscrive dalla pagina della mailing list nel suo browser. Se per accedere serve un login, un captcha o una scelta, devi occupartene tu: la riga spiega perché e mostra **Apri la pagina di disiscrizione**.

Ricevute, ordini e avvisi di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come un Google Group, vengono elencate sotto il nome di chi le ha scritte e non ti disiscrivono mai dal gruppo. Se il mittente non offre una procedura di disiscrizione, la riga mostra **Disiscriviti a mano**.

**Pulizia spam** crea un’attività per ogni area con le email che sembrano spam e provengono da mittenti sconosciuti. Per ciascuna puoi scegliere **Spam** o **Non è spam**. Outlook sposta le email nella Posta indesiderata e Gmail le contrassegna come spam. La routine controlla ogni ora, così di solito lo spam viene individuato prima che tu lo veda. Quando l’attività è ancora aperta, le nuove email di spam vengono aggiunte alla stessa attività.

Se Gmail è collegato in modalità di sola lettura, come su una Machine ospitata, non è possibile spostare le email nello spam. In questo caso, **Spam** mostra un link per contrassegnare l’email come spam in Gmail e la tua Machine ricorda il mittente come spam. Se non hai collegato un account email, al posto di **Aggiungi** il modello mostra **Collega la posta**.

Un mittente è sconosciuto se non gli hai mai scritto. Un «Re:» viene considerato una conversazione solo in una discussione a cui hai partecipato. Se ricevi di nuovo un’email da un mittente che hai contrassegnato come spam, nell’attività o nella tua casella di posta, la prossima attività mostrerà **Già segnato come spam**. Anche le email che hai spostato manualmente nello spam aiutano la routine a individuare messaggi simili.

Non cambia nulla finché non confermi le tue scelte nell’attività. Tocca il mittente per leggere prima l’email: resterà non letta e non cambierà nulla. Nelle attività di Pulizia spam, le immagini dal web non vengono caricate, così il mittente non può sapere che hai aperto l’email. Non ti verrà chiesto di nuovo di decidere sui mittenti già valutati. Se in un giorno non arrivano newsletter o spam, non viene creata alcuna attività. Queste attività non inviano mai notifiche.

Quando hai deciso per tutti i mittenti, l’attività risulta completata e mostra **Segna come fatto**.

**Riepilogo giornaliero** seleziona una volta al giorno, in un’unica attività, le poche newsletter che meritano la tua attenzione. Per ciascuna spiega in una riga perché è rilevante per te. Tocca una newsletter per leggere l’email oppure usa **Apri nella tua posta**. La routine considera solo le newsletter, mai le email di persone, le ricevute o i mittenti da cui ti sei disiscritto, e mai le email che hai già letto. Se non trova nulla di interessante, non crea un’attività.

La routine impara cosa ti interessa da ciò che apri, aggiungi ai preferiti o archivi senza leggere, e dalle opzioni **Altri così** e **Meno così** per ogni suggerimento. Gli argomenti che seleziona sono indicati nella scheda della routine, sotto **Più su** e **Meno su**. Tocca × per rimuovere un argomento o aggiungine uno tu. Gli argomenti tratteggiati sono stati individuati dalla routine. Un nuovo riepilogo sostituisce quello aperto e non invia mai notifiche.

La routine legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter, poi pone all’IA una breve domanda al giorno, con un limite giornaliero, per contenere i costi. **Cambia quando** permette di modificarne l’orario. Dopo che cambi le parole, la routine viene eseguita come qualsiasi altra, seguendo le tue indicazioni.

**Compleanni** crea un’attività per ogni persona a te vicina che compie gli anni oggi e a cui scrivi personalmente, come amici, familiari e contatti abituali. Per ciascuna prepara una breve bozza di auguri nel canale che usi di solito con quella persona, per esempio nella chat di WhatsApp o nella conversazione email, nella sua lingua. Il messaggio parte solo quando lo invii tu. Se nessuno compie gli anni, non viene creata alcuna attività.

I compleanni possono arrivare dai tuoi calendari (gli eventi compleanno di Google e il calendario Compleanni, che vengono letti ogni mattina anche se non sono sincronizzati, e il calendario Compleanni di Outlook), dai contatti Google su una Machine che ospiti tu e da un campo data chiamato Compleanno assegnato a una persona nel Graph. Se nessuna di queste fonti contiene ancora un compleanno, il risultato mostra **Non ci sono ancora informazioni sui compleanni** e spiega come aggiungerle.

**Importa i compleanni da Facebook**: quando Compleanni è attiva, un’attività ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e la tua Machine apre la pagina nel suo browser, scorre finché non ha caricato tutti i mesi e legge il nome e il compleanno di ogni amico. Ti mostra quanti ne ha trovati e quali corrispondono a persone nel tuo Graph in base al nome e al cognome. Se più persone hanno lo stesso nome, vengono escluse e indicate nell’elenco.

Solo **Salva** conserva i dati nella pagina di ciascuna persona: il compleanno e la foto del profilo Facebook, se la persona non ha ancora una foto. Un compleanno o una foto che hai impostato lì restano invariati, e una foto già presente non viene mai sostituita. Non viene scritto nulla su Facebook.

La routine non legge di nuovo i dati da sola: per farlo, tocca **Importa di nuovo** nell’attività. Il browser deve aver effettuato l’accesso a Facebook. Se non lo ha fatto, tocca **Accedi a Facebook** nell’attività e accedi da lì. Una volta effettuato l’accesso, la routine legge la pagina da sola. La tua Machine non accede mai al posto tuo.

Gli amici che non sono presenti nel tuo Graph vengono conteggiati e ne vengono mostrati alcuni nomi. **Aggiungi … come contatti personali** li aggiunge tutti in una volta, anche dopo aver toccato Salva. Ognuno avrà un nome e un compleanno, e non verrà mai condiviso con una Fleet di lavoro. Le persone con un nome già presente nel tuo Graph, o che avevi eliminato definitivamente, vengono escluse. I promemoria dei compleanni continuano ad arrivare solo per le persone a cui scrivi.

Toccando **Annulla** nell’attività, rimuovi esattamente le persone aggiunte, anche dopo aver toccato **Importa di nuovo**.

**Abbonamenti e prove** legge una volta al mese ricevute, fatture e avvisi di rinnovo che trovi nella posta, poi raccoglie gli abbonamenti in un’unica attività. Per ciascuno indica il costo, la prossima data di addebito e un avviso se una prova sta per finire o il prezzo aumenta. Elenca solo gli abbonamenti di cui è sicura. Se non trova nulla, non crea un’attività.

Per ciascuno, scegli **Tieni** o **Disdici**. Non ti verrà chiesto di nuovo di un abbonamento che hai deciso di tenere, a meno che il prezzo non cambi. **Disdici** mostra la pagina per annullare l’abbonamento oppure una bozza in cui chiedi di annullarlo. Il messaggio parte solo quando lo invii tu. Tra un controllo e l’altro, la routine verifica ogni giorno e crea un’attività se una prova o un rinnovo verrà addebitato entro 7 giorni.

**Restare in contatto** ti ricorda ogni tanto di farti sentire con una persona a te vicina, solo se c’è un motivo concreto. Nella scheda, scegli le persone da includere da un breve elenco di contatti con cui scrivi personalmente da mesi, in entrambe le direzioni. Tocca × per rimuovere una persona.

Ricevi un promemoria solo quando è passato molto più tempo del solito dall’ultima conversazione e c’è qualcosa di specifico da dire: una notizia che ti ha raccontato, una promessa ancora in sospeso o un messaggio a cui non hai mai risposto. Il promemoria è un’unica attività con il motivo e un breve messaggio preparato nel canale che usi di solito con quella persona, nella sua lingua. Il messaggio parte solo quando lo invii tu. Se non c’è niente da dire, non viene creata alcuna attività.

La routine invia al massimo due promemoria a settimana, uno al mese per persona, e nessuno a chi hai sentito di recente. **Non serve** su un promemoria fa aspettare più a lungo prima di riproporlo per quella persona, e ogni volta l’attesa aumenta. Non invia mai notifiche e resta Personale: non viene mai condivisa con una Fleet di lavoro.

**Occasioni di seconda mano** controlla le ricerche su siti di seconda mano come Marktplaats, Vinted, eBay o Facebook Marketplace. Cerca sul sito con i filtri che vuoi, copia l’indirizzo dei risultati e incollalo dopo aver toccato **Aggiungi**. Se vuoi, aggiungi filtri a parole tue, per esempio «sotto i 300, entro 30 km, escludi “per pezzi di ricambio”». Ogni ricerca ha una sua routine, quindi aggiungila di nuovo per quella successiva.

Ogni 3 ore, la tua Machine apre la ricerca nel proprio browser e cerca annunci che non ha ancora visto. Prezzo, distanza e parole da escludere vengono controllati prima, con semplice codice.

Ogni nuovo annuncio che supera questi controlli viene aperto e la tua IA ne valuta le condizioni in base alla foto e alla descrizione, e il venditore in base alle recensioni, alla valutazione e all’età dell’account. Quelli più interessanti vengono raccolti in un’unica attività, ciascuno con foto, titolo, prezzo e un breve giudizio. Tocca un annuncio per aprirlo nel browser della tua Machine.

Finché l’attività è aperta, i nuovi annunci vengono aggiunti in cima, il conteggio aumenta e ricevi un’altra notifica, perché le occasioni migliori finiscono in fretta. Quando la contrassegni come completata, il prossimo annuncio trovato avvia una nuova attività. Se una ricerca non trova nulla di interessante, non cambia niente.

La routine limita l’impatto sul sito e sui costi: legge la ricerca una sola volta per esecuzione, apre al massimo 6 annunci con una pausa tra uno e l’altro e controlla al massimo 40 annunci al giorno in tutte le tue ricerche. Per ogni controllo, la tua IA riceve una breve domanda e una foto. La prima esecuzione controlla gli annunci più recenti e segna gli altri come già visti, così quelle successive mostrano solo le novità.

Se il sito ti chiede di accedere, mostra un controllo anti-robot o impedisce la lettura, un’attività te lo segnala e mostra **Apri** per vedere la pagina nel browser della tua Machine. Accedi o supera il controllo da lì: alla prossima esecuzione la routine riproverà a leggere la pagina. La tua Machine non accede e non supera i controlli al posto tuo, e non contatta mai i venditori, non fa offerte e non compra nulla.

**Modifica ricerca** nella scheda della routine permette di inserire un nuovo indirizzo o nuovi filtri, mentre **Cambia quando** permette di impostare un altro ritmo, per esempio «ogni 6 ore».

**Riordini** legge le conferme degli ordini dei negozi online nella tua posta e individua ciò che compri più volte, come caffè, cibo per animali o vitamine. Quando pensa che sia arrivato il momento di ricomprarlo, crea un’attività con il prodotto, il negozio, l’ultimo prezzo e la data dell’ultimo acquisto. **Apri nel negozio** apre la pagina del prodotto, dove puoi comprarlo tu. La routine non acquista nulla al posto tuo.

La routine ha bisogno di almeno tre ordini dello stesso prodotto, effettuati a intervalli regolari. Un acquisto isolato o un intervallo insolito non genera un’attività. Per ora controlla i negozi basati su Shopify. La tua IA legge solo le nuove email di conferma d’ordine provenienti da quei negozi, con una breve domanda per esecuzione. Queste attività non inviano mai notifiche e un nuovo ordine dello stesso prodotto chiude quella aperta.

Finché una routine di un modello mantiene le parole originali del modello, viene eseguita con il proprio codice, senza usare il piano IA. Per esempio, Pulizia spam elenca prima con il codice le nuove email di mittenti sconosciuti e pone all’IA una breve domanda solo se ne trova. Restare in contatto chiede informazioni solo su una o due persone selezionate. Se cambi il nome, le impostazioni restano. Dopo che cambi le parole, la routine viene eseguita come qualsiasi altra, seguendo le tue indicazioni.

Pulizia newsletter e Pulizia spam continuano a creare un’unica attività con una scelta per ogni email. Se modifichi Compleanni, la routine mostra il risultato e al massimo una bozza, non un’attività per ogni persona. In **Modifica**, **Torna al modello** ripristina le parole originali.

## Cosa fa una routine

All’orario previsto, la tua Machine legge ciò che serve, come i tuoi messaggi, le riunioni e il Graph, poi mostra il risultato nella pagina Routine. Ogni risultato indica **Pronta**, **Niente di nuovo** con una spiegazione oppure **Non è andato** con una spiegazione. Se un’esecuzione termina senza risultato, viene considerata non riuscita, mai completata.

Le routine si limitano a leggere: i tuoi messaggi, le pagine web, GitHub e siti come X nel browser. Non inviano messaggi, non rispondono, non pubblicano e non modificano nulla. Aprono le pagine trovate in ciò che leggono o in una ricerca, gli indirizzi di pagine semplici e i siti più noti. Non aprono mai un indirizzo creato apposta per contenere ciò che hanno letto. Solo un modello può modificare la posta, e solo dopo che hai confermato nell’attività.

Se il lavoro di una routine prevede un post o un messaggio, la routine completa tutti i passaggi fino a quel punto e mostra la bozza, per esempio **Vuole pubblicare su X:**. Dopo un’esecuzione effettiva, la bozza diventa un’attività da approvare. Un’esecuzione di prova la mostra soltanto. Il nome indica l’argomento e la destinazione, il pulsante indica il passaggio da fare, per esempio **Pubblicalo**, e **Dalla tua routine** sotto la bozza apre la routine.

L’attività inizia nell’area dell’account da cui verrà inviato il messaggio, per esempio Lavoro per l’account X della tua azienda, così non ti viene mai chiesto di spostarla.

Un’esecuzione può seguire le tue [skill](skills.md) attive, selezionate in base a ciò che fa la routine. Vengono lette per intero solo quelle pertinenti. Il risultato le indica sotto **Usate:**. Una skill non fa mai inviare messaggi o modificare elementi a una routine.

Le tue routine sono raccolte sotto **Le tue routine**, dopo eventuali suggerimenti. Se il risultato è lungo, viene mostrata un’anteprima breve. **Mostra altro**, oppure un tocco sul risultato, lo apre per intero.

Ogni esecuzione conosce il risultato precedente e può indicare cosa è cambiato da allora.

Dopo un’esecuzione riuscita, la tua Machine può scrivere da sola una procedura per le operazioni di lettura che si ripetono ogni volta, per esempio quali email o modifiche a GitHub controllare. Le esecuzioni successive controllano prima questi elementi con semplice codice. Poi l’IA seleziona ciò che conta e lo scrive, usando meno token. La procedura si limita a leggere. Se smette di funzionare, la routine legge da sola e la corregge. La trovi sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine era spenta o occupata, le esecuzioni saltate non si accumulano: viene eseguita una sola volta la più recente. Ogni data viene eseguita una volta sola, anche dopo un riavvio.

Le routine vengono eseguite una alla volta e attendono quando l’utilizzo del tuo piano IA è basso, come per tutte le attività in background. **Esegui ora** avvia subito la routine. Quando il risultato è pronto, viene mostrato sulla scheda.

## Modificala o interrompila

Queste opzioni si trovano nel menu ⋯ della routine. **Modifica** cambia il nome e le istruzioni, ma non l’orario di esecuzione né i risultati già ottenuti. **Cambia quando** permette di impostare un nuovo ritmo a parole tue, per esempio «ogni giorno feriale alle 8». Entrambe le opzioni includono **Salva** e **Annulla**. Sul computer puoi annullare anche premendo Esc o facendo clic fuori.

In **Modifica**, **Provalo** esegue una volta le nuove istruzioni e mostra il risultato. La routine resta com’era fino a quando non tocchi **Salva**.

**Metti in pausa** interrompe le esecuzioni finché non tocchi **Riprendi** sulla scheda. Le routine in pausa si trovano sotto **In pausa**, dopo le altre routine, e le esecuzioni saltate durante la pausa non verranno recuperate. **Ferma** interrompe definitivamente una routine.

Puoi avere fino a 20 routine, incluse quelle in pausa. Ferma una routine per aggiungerne un’altra.

Quando usi **Chiedi modifiche** sull’attività di una routine, oppure scrivi nella sua chat, e la tua nota vale per tutte le esecuzioni, per esempio «non usare mai emoji», l’attività propone **Cambia anche la routine**. L’opzione compare nell’attività e nella chat, sotto la risposta. Ti mostra cosa cambierà nelle istruzioni della routine, che verranno modificate solo quando tocchi **Cambiala**. **Lasciala così** mantiene tutto com’è. Se la correzione riguarda solo quella bozza, non viene mostrata alcuna opzione.

## Avanzate: passaggi di script

Non serve scrivere script: descrivi a parole tue cosa deve fare una routine e la tua Machine si occupa del resto.

Per chi ha più esperienza, una routine può anche eseguire comandi personalizzati sulla tua Machine. Dal menu ⋯, scegli **Avanzate: passaggi di script**. **Modifica** mostra i passaggi solo se la routine ne ha già. **Recupera dati** esegue prima un comando, nella sua cartella o, se non ne indichi una, nella cartella Home. Il comando può durare al massimo il numero di secondi impostato. Ciò che stampa viene passato all’esecuzione per essere elaborato. Se non ci sono istruzioni, il risultato è quello che stampa il comando.

**Verifica** riceve il risultato come input al termine dell’esecuzione. Se il comando termina con un errore, l’esecuzione mostra **Non è andato** e il messaggio restituito dal controllo. Anche un comando di Recupera dati non riuscito viene segnalato allo stesso modo.

I comandi devono stare su una riga e vengono eseguiti senza una shell: non puoi usare pipe o variabili. I passaggi di script sono tuoi e si impostano solo dalla dashboard. Anche un’esecuzione di prova e **Provalo** eseguono Recupera dati e lo indicano. Non inviano né conservano comunque nulla. Una routine non invia mai nulla, quindi un passaggio di script deve limitarsi a leggere.

## Dai tuoi job di OpenClaw

Se in precedenza avevi programmato dei job in OpenClaw, la tua Machine li legge, senza modificarli, e propone come routine quelli adatti, sotto **Suggerito**. Ogni job è stato eseguito una volta, quindi puoi vedere un risultato effettivo.

La tua Machine conserva le correzioni che hai apportato al job ed esclude ciò che ha inviato o pubblicato. Se un job eseguiva uno script o leggeva dati raccolti da un job con script, questi vengono aggiunti come Recupera dati. **Aggiungi** lo trasforma in una routine, mentre **No, grazie** impedisce che ti venga proposto di nuovo. Se un job ti ricordava di fare qualcosa, su Attività viene proposta invece un’attività ricorrente.

Prima di aggiungere un suggerimento, puoi modificarlo come qualsiasi routine con **Modifica** e **Cambia quando** nel menu ⋯. **Esegui di nuovo** lo avvia subito con le istruzioni attuali, così puoi vedere risultati più recenti, per esempio dopo un weekend tranquillo. La routine si limita a leggere, viene eseguita una volta per ogni tocco e il nuovo risultato sostituisce quello precedente.

Possono esserci al massimo tre suggerimenti in attesa. Dopo una settimana di esecuzioni riuscite, la routine chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se tocchi **Disattiva**. Puoi riattivarlo in OpenClaw. **Tienilo** lascia attivi entrambi.

## Da quello che fai

La tua Machine individua anche le attività che svolgi con regolarità e te le propone come routine sotto **Suggerito**, anche se non usi OpenClaw. Cerca:

- la stessa richiesta almeno tre volte di fila, per esempio «riepiloga le richieste di assistenza aperte» ogni lunedì;
- un’email che invii regolarmente, come un resoconto settimanale al tuo team;
- newsletter e aggiornamenti che ricevi ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una alla volta sempre alla stessa persona, come le email della scuola o delle attività dei figli che inoltri al partner. Un riepilogo settimanale evita di doverle inoltrare;
- la stessa richiesta a cui rispondi con regolarità, come un’approvazione mensile per la stessa persona.

Ogni suggerimento spiega cosa ha notato, per esempio «Richiesto 4 volte di fila» o «Inoltrate 6 email a Sam in 3 settimane», ed è già stato eseguito una volta, così puoi vedere un risultato effettivo. Può trattarsi di un riepilogo per il team, un briefing prima di una riunione settimanale, un riepilogo dell’assistenza o dello sviluppo, un aggiornamento sui tuoi numeri o un riepilogo delle newsletter che ricevi.

La routine suggerisce solo attività specifiche per te e chiaramente utili: per esempio, un riepilogo delle notizie solo sulle newsletter che ricevi tu, mai uno generico. Se non trova nulla di adatto, non mostra alcun suggerimento.

Controlla al massimo una volta al giorno e aggiunge al massimo un nuovo suggerimento a settimana, senza inviare notifiche. **No, grazie** non ripropone quel suggerimento. Gli inoltri e le risposte restano nell’account da cui sono stati inviati, così Lavoro e Personale non si mescolano. Tutto resta sulla tua Machine. Se chiudi un’attività con regolarità, ti viene proposta un’attività ricorrente.

## Routine e attività ricorrenti

Un’[attività ricorrente](recurring.md) ti ricorda di fare qualcosa. Una routine è un lavoro che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per «pagare l’affitto il primo del mese» e una routine per «ogni venerdì, dimmi quali trattative si sono bloccate».
