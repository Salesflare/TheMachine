---
title: Routine
area: cards
summary: Il lavoro che la tua Machine svolge da sola, con regolarità, per esempio un riepilogo del lunedì sulle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: 9c3559a910b9dd37
---
## Creane una

Apri **Routine** nella barra laterale e scrivi in una riga cosa deve fare e quando: «ogni lunedì alle 9, riepiloga le trattative aperte» oppure «ogni mattina nei giorni feriali, elenca le email a cui devo ancora rispondere». Poi seleziona **Aggiungi**.

Se non indichi un orario, la routine viene eseguita alle 8:00, secondo l’orologio della tua Machine. Alla prima esecuzione, le viene assegnato un nome breve.

Con **Aggiungi** viene prima eseguita una prova, così puoi vedere il risultato prima di conservarla. Non viene inviato né salvato nulla. Poi **Aggiungi** la mantiene attiva con la frequenza scelta, **Cambia** prova altre parole o un nuovo nome e **Annulla** la elimina.

## Modelli

In fondo a Routine, nella sezione **Modelli**, seleziona **Aggiungi** per attivare una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30 (la Pulizia spam ogni ora, Abbonamenti e prove una volta al mese). La scheda mostra le istruzioni, come per qualsiasi routine. Con **Modifica** puoi cambiarle o modificare il nome.

Quando arrivano molte newsletter e Pulizia newsletter è disattivata (almeno 25 in una settimana, da almeno 5 mittenti), sopra le tue attività compare una riga che indica quante ne sono arrivate e cosa farebbe la routine, con le opzioni **Attivala** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo quando, in una settimana, hai spostato manualmente nello spam almeno 5 email. **Attivala** la aggiunge, come farebbe **Aggiungi** qui. Se selezioni **No, grazie**, non verrà più proposta. Lo stesso vale per un modello che avevi già usato.

**Pulizia newsletter** crea un’attività per ogni area (lavoro e personale) con le newsletter dell’ultimo giorno. Per ciascuna puoi scegliere **Tieni** o **Disiscriviti**. Per disiscriverti, la routine usa il link per la disiscrizione con un clic oppure, se è attivo l’invio, manda un’email di disiscrizione dal tuo indirizzo. Altrimenti, The Machine si disiscrive dalla pagina della lista usando il proprio browser. Se è necessario accedere, completare un captcha o effettuare delle scelte, dovrai farlo tu: la riga spiega il motivo e mostra **Apri la pagina di disiscrizione**.

Le ricevute, gli ordini e gli avvisi di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come un Google Group, vengono elencate sotto il nome di chi le ha scritte. Non ti disiscrivono mai dal gruppo. Se il mittente non offre un’opzione per disiscriversi, la riga mostra **Disiscriviti a mano**.

**Pulizia spam** crea un’attività per ogni area con le email che sembrano spam e provengono da mittenti sconosciuti. Per ciascuna puoi scegliere **Spam** o **Non è spam**. Outlook sposta le email nella cartella Posta indesiderata, mentre Gmail le contrassegna come spam. Il controllo avviene ogni ora, quindi di solito lo spam viene individuato prima che tu lo veda. Mentre l’attività è aperta, le nuove email di spam vengono aggiunte alla stessa attività.

Se Gmail è collegato in modalità di sola lettura, come su una Machine ospitata, non è possibile spostare le email nello spam. In questo caso, **Spam** mostra un link per contrassegnare l’email come spam in Gmail e The Machine ricorda il mittente come spam. Se non è collegato nessun account email, al posto di **Aggiungi** il modello mostra **Collega la posta**.

Un mittente è sconosciuto se non gli hai mai scritto. Un «Re:» viene considerato una conversazione solo in una conversazione a cui hai partecipato. Se ricevi di nuovo un’email da un mittente che avevi contrassegnato come spam, nell’attività o nella posta in arrivo, questa compare nell’attività successiva con l’etichetta **Già segnato come spam**. Anche le email che hai spostato tu nello spam aiutano la routine a individuare email simili.

Non cambia nulla finché non confermi nell’attività. Tocca il mittente per leggere prima l’email: resterà non letta e non cambierà nulla. Nella Pulizia spam, le immagini dal web non vengono caricate, così il mittente non può sapere che hai aperto l’email. Non ti verrà chiesto di nuovo cosa fare con i mittenti per cui hai già fatto una scelta. Se in un giorno non arrivano newsletter o spam, non viene creata nessuna attività. Queste attività non inviano mai notifiche.

Una volta presa una decisione per ogni mittente, l’attività risulta completata e mostra **Segna come fatto**.

**Riepilogo giornaliero** seleziona ogni giorno le poche newsletter che vale la pena leggere e le raccoglie in un’unica attività. Per ognuna, una riga spiega perché potrebbe interessarti. Tocca una newsletter per leggere l’email oppure seleziona **Apri nella tua posta**. La routine considera solo le newsletter: mai email personali, ricevute o email di mittenti da cui ti sei disiscritto, e mai quelle che hai già letto. Se non trova nulla di interessante, non crea un’attività.

Impara cosa ti interessa in base alle email che apri, aggiungi ai preferiti o archivi senza leggere, e alle opzioni **Altri così** e **Meno così** che selezioni per ogni elemento. Gli argomenti che prende in considerazione sono indicati nella scheda della routine, sotto **Più su** e **Meno su**. Tocca × per rimuovere un argomento o aggiungine uno tu. Gli argomenti tratteggiati sono stati individuati dalla routine. Un nuovo riepilogo sostituisce quello ancora aperto e non invia mai notifiche.

La routine legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter, poi fa una breve domanda alla tua AI, con un limite giornaliero per contenere i costi. Con **Cambia quando** puoi impostare l’orario. Se modifichi le istruzioni, la routine funziona come qualsiasi altra routine e le esegue.

**Compleanni** crea un’attività per ogni persona cara che compie gli anni oggi: persone a cui scrivi direttamente, come amici, familiari e contatti abituali. Per ognuna prepara un breve messaggio di auguri nel posto in cui di solito parli con quella persona, come la chat WhatsApp o la conversazione email, e nella sua lingua. Il messaggio viene inviato solo quando lo invii tu. Se non ci sono compleanni, non viene creata nessuna attività.

I compleanni vengono recuperati dai tuoi calendari (gli eventi di compleanno di Google e il calendario Compleanni, letti ogni mattina anche quando non sono sincronizzati, e il calendario Compleanni di Outlook), dai tuoi contatti Google su una Machine ospitata in proprio e da un campo data chiamato Birthday di una persona nel Graph. Se non è ancora stato trovato nessun compleanno, il risultato mostra **Nessuna informazione sui compleanni** e spiega come aggiungerla.

**Importa i compleanni da Facebook**: dopo aver attivato Compleanni, un’attività ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa**: The Machine apre la pagina nel proprio browser, scorre fino a caricare tutti i mesi e legge il nome e il compleanno di ogni amico. Ti mostra quanti compleanni ha trovato e quali persone corrispondono a persone nel tuo Graph in base a nome e cognome. Se più persone hanno lo stesso nome, vengono ignorate e mostrate in un elenco.

Solo selezionando **Salva** vengono salvati i dati nella pagina di ogni persona: il compleanno e, se la persona non ha ancora una foto, la sua immagine del profilo Facebook. I compleanni e le foto che hai già impostato restano invariati, e una foto già presente non viene mai sostituita. Non viene scritto nulla su Facebook.

La routine non legge di nuovo i dati da sola: per farlo, seleziona **Importa di nuovo** nell’attività. Il browser deve avere una sessione Facebook aperta. Se non hai effettuato l’accesso, tocca **Accedi a Facebook** nell’attività e accedi da lì. Una volta effettuato l’accesso, la pagina viene letta automaticamente. The Machine non accede mai al posto tuo.

Le persone che non sono presenti nel Graph vengono conteggiate e ne vengono mostrati alcuni nomi. **Aggiungi … come contatti personali** le aggiunge tutte in una volta, anche dopo aver selezionato Salva. Per ognuna vengono aggiunti nome e compleanno, senza condividerli con una Work Fleet. Le persone con un nome già presente nel Graph, o che erano state eliminate in modo permanente, vengono ignorate. I promemoria dei compleanni continuano a essere creati solo per le persone a cui scrivi.

Con **Annulla** nell’attività puoi rimuovere esattamente le persone aggiunte, anche dopo aver selezionato **Importa di nuovo**.

**Abbonamenti e prove** legge una volta al mese le ricevute, le fatture e gli avvisi di rinnovo, poi raccoglie gli abbonamenti in un’unica attività. Per ognuno mostra il costo, la data del prossimo addebito e un avviso quando sta per finire una prova o aumenta il prezzo. Vengono elencati solo gli abbonamenti che la routine riesce a identificare con certezza. Se non ne trova, non viene creata nessuna attività.

Per ogni abbonamento, scegli **Tieni** o **Disdici**. Non ti verrà più chiesto cosa fare con quelli che tieni, a meno che il prezzo non cambi. Se scegli **Disdici**, la routine mostra la pagina per annullare l’abbonamento oppure prepara una bozza per chiederne la disdetta. La bozza viene inviata solo quando la invii tu. Tra un’esecuzione e l’altra, la routine controlla ogni giorno e crea un’attività quando un addebito per una prova o un rinnovo è previsto entro 7 giorni.

Finché il modello mantiene le proprie istruzioni, la routine viene eseguita con codice dedicato, senza usare il tuo piano AI. La Pulizia spam, per esempio, trova prima nel codice le nuove email di mittenti sconosciuti e fa una breve domanda alla tua AI solo se ne trova. Se cambi il nome, il codice rimane invariato. Se modifichi le istruzioni, la routine funziona come qualsiasi altra routine e le esegue.

Pulizia newsletter e Pulizia spam continuano a creare la stessa attività, con una scelta per ogni email. Se modifichi Compleanni, la routine mostra il risultato e al massimo una bozza, non un’attività per ogni persona. In **Modifica**, seleziona **Torna al modello** per ripristinare le istruzioni originali.

## Cosa fa una routine

All’orario stabilito, la tua Machine legge ciò che le serve, come i tuoi messaggi, le riunioni e il Graph, e mostra il risultato nella pagina Routine. Ogni risultato mostra **Pronta**, **Niente di nuovo** (con il motivo) oppure **Non è andato** (con il motivo). Se un’esecuzione termina senza un risultato, viene considerata non riuscita, mai completata.

Le routine si limitano a leggere: i tuoi messaggi, le pagine web, GitHub e siti come X nel browser. Non inviano messaggi, non rispondono, non pubblicano e non modificano nulla. Solo un modello può modificare le email, e solo in base a ciò che confermi nella relativa attività.

Se il lavoro di una routine prevede di pubblicare un post o inviare un messaggio, la routine esegue tutti i passaggi fino a quello e mostra una bozza, per esempio **Pubblicheresti su X:**. Dopo un’esecuzione reale, la bozza viene proposta come attività da approvare. Con un’esecuzione di prova viene solo mostrata. Il nome indica l’argomento e dove verrà pubblicato, il pulsante indica il passaggio, per esempio **Pubblicalo**, e **Dalla tua routine**, sotto la bozza, apre la routine.

L’attività viene creata nell’area dell’account da cui sarà inviata, per esempio Lavoro per l’account X della tua azienda, quindi non ti verrà mai chiesto di spostarla.

Un’esecuzione può seguire le tue [skill](skills.md) attive, scelte in base a ciò che fa la routine: vengono lette per intero solo quelle pertinenti. Il risultato le elenca sotto **Usate:**. Una skill non può far sì che una routine invii o modifichi qualcosa.

Le tue routine si trovano sotto **Le tue routine**, dopo gli eventuali suggerimenti. I risultati lunghi vengono accorciati in un’anteprima. Seleziona **Mostra altro** o tocca l’anteprima per aprirli.

Ogni esecuzione tiene conto del risultato precedente, così può indicare cosa è cambiato.

Dopo un’esecuzione riuscita, la tua Machine potrebbe scrivere una procedura per le operazioni di lettura che si ripetono ogni volta, per esempio quali email o modifiche di GitHub controllare. Le esecuzioni successive iniziano da lì, usando semplice codice. L’AI si limita a scegliere ciò che conta e a scriverlo, usando meno token. La procedura si limita a leggere. Se smette di funzionare, l’esecuzione procede da sola e la corregge. La procedura si trova sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine era spenta o occupata, le esecuzioni saltate non si accumulano: viene eseguita solo la più recente, una volta. Ogni data viene gestita una sola volta, anche dopo un riavvio.

Le routine vengono eseguite una alla volta e restano in attesa quando l’utilizzo del tuo piano AI è basso, come tutti i lavori in background. **Esegui ora** avvia subito la routine. Il risultato compare nella scheda quando è pronto.

## Modifica o interrompi

Queste opzioni si trovano nel menu ⋯ della routine. **Modifica** cambia il nome e cosa fa la routine; la frequenza e i risultati ottenuti restano invariati. Con **Cambia quando** puoi impostare una nuova frequenza usando parole tue, per esempio «ogni giorno feriale alle 8». Entrambe le opzioni includono **Salva** e **Annulla**. Su un computer puoi anche premere Esc o fare clic fuori per annullare.

In **Modifica**, **Provalo** esegue una volta le nuove istruzioni e mostra il risultato. La routine resta com’era fino a quando non selezioni **Salva**.

**Metti in pausa** interrompe le esecuzioni fino a quando non selezioni **Riprendi**. Le routine in pausa si trovano sotto **In pausa**, in fondo alla pagina. Le esecuzioni saltate durante la pausa non verranno recuperate. **Ferma** interrompe definitivamente una routine.

Se selezioni **Chiedi modifiche** nell’attività di una routine o scrivi nella sua chat, e la nota riguarda tutte le esecuzioni, per esempio «non usare mai emoji», l’attività propone **Cambia anche la routine**. L’opzione compare nell’attività e nella chat, sotto la risposta. Vengono mostrate le modifiche alle istruzioni della routine, che cambierà solo se selezioni **Cambiala**. Seleziona **Lasciala così** per non modificarla. Se la modifica riguarda solo quella bozza, l’opzione non viene proposta.

## Avanzate: passaggi di script

Non serve scrivere script: descrivi con parole tue cosa deve fare una routine e la tua Machine penserà al resto.

Per gli utenti esperti, una routine può anche eseguire comandi personalizzati sulla tua Machine. Seleziona **Avanzate: passaggi di script** nel menu ⋯. **Modifica** mostra i passaggi solo quando la routine ne ha già. **Recupera dati** esegue prima un comando nella relativa cartella, oppure nella cartella principale se il campo è vuoto, per il numero di secondi specificato. Il risultato del comando viene fornito all’esecuzione. Se non ci sono istruzioni, il risultato del comando diventa il risultato dell’esecuzione.

**Verifica** riceve il risultato come input dopo l’esecuzione. Se termina con un errore, l’esecuzione mostra **Non è andato** e il messaggio restituito dalla verifica. Anche un comando di Recupera dati non riuscito viene mostrato allo stesso modo.

Un comando deve stare su una sola riga e viene eseguito senza shell: niente pipe o variabili. I passaggi di script sono tuoi e si impostano solo nella dashboard. Anche un’esecuzione di prova e **Provalo** eseguono Recupera dati e lo indicano. Non inviano né conservano nulla. Una routine non invia mai messaggi, quindi i passaggi di script dovrebbero limitarsi a leggere.

## Dai tuoi job di OpenClaw

Se in passato hai creato job pianificati in OpenClaw, la tua Machine li legge (non li modifica mai) e propone quelli adatti come routine sotto **Suggerito**. Ognuno è già stato eseguito una volta, quindi puoi vedere un risultato reale.

La routine mantiene le correzioni che hai apportato al job ed esclude ciò che il job ha inviato o pubblicato. Se un job ha eseguito uno script o ha letto i dati raccolti da un job script, lo mantiene come passaggio Recupera dati. **Aggiungi** crea una routine, mentre **No, grazie** impedisce che il job venga proposto di nuovo. Se un job ti ricordava di fare qualcosa, viene proposto in To-do come attività ricorrente.

Prima di aggiungere un suggerimento, puoi modificarlo come qualsiasi routine usando **Modifica** e **Cambia quando** nel menu ⋯. **Esegui di nuovo** lo esegue con le istruzioni attuali, così puoi vedere i risultati più recenti, per esempio dopo un fine settimana tranquillo. La routine si limita a leggere, viene eseguita una volta per tocco e il nuovo risultato sostituisce quello precedente.

Possono esserci al massimo tre suggerimenti in attesa alla volta. Dopo una settimana di esecuzioni riuscite, la routine chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se selezioni **Disattiva**. Puoi riattivarlo in OpenClaw.

## Da quello che fai

Anche senza OpenClaw, la tua Machine rileva le attività che svolgi con regolarità e le propone come routine sotto **Suggerito**. Cerca:

- la stessa richiesta per almeno tre volte di seguito, per esempio «riepiloga le richieste di assistenza aperte» ogni lunedì;
- un’email che invii con regolarità, per esempio un rapporto settimanale al tuo team;
- newsletter e email di aggiornamento che ricevi ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una alla volta alla stessa persona, per esempio email della scuola e del club al tuo partner: un riepilogo settimanale per quella persona evita di doverle inoltrare;
- la stessa richiesta a cui rispondi con regolarità, per esempio un’approvazione mensile per la stessa persona.

Ogni suggerimento spiega cosa ha notato, per esempio «Richiesto 4 volte di seguito» o «Inoltrate 6 email a Sam in 3 settimane», ed è già stato eseguito una volta, così puoi vedere un risultato reale. Potrebbe essere un riepilogo del team, un breve aggiornamento prima di una riunione settimanale, un riepilogo dell’assistenza o dello sviluppo, un aggiornamento sui tuoi numeri oppure un riepilogo delle newsletter che ricevi.

Vengono proposte solo attività specifiche per te e chiaramente utili: un riepilogo di notizie, per esempio, include solo le tue newsletter, mai notizie generiche. Se non trova nulla di adatto, non viene proposto nessun suggerimento.

La routine controlla al massimo una volta al giorno e propone al massimo un nuovo suggerimento a settimana, senza inviare notifiche. Se selezioni **No, grazie**, il suggerimento non verrà riproposto. Gli inoltri e le risposte restano nell’account da cui sono stati inviati, così Lavoro e Personale non si mescolano. Tutto resta sulla tua Machine. Se completi un’attività con regolarità, viene proposta invece come attività ricorrente.

## Routine e attività ricorrenti

Un’attività ricorrente (recurring.md) ti ricorda di fare qualcosa. Una routine è un lavoro che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per «pagare l’affitto il primo del mese» e una routine per «ogni venerdì, dimmi quali trattative sono ferme».
