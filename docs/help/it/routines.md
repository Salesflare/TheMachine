---
title: Routine
area: cards
summary: Attività che la tua Machine svolge da sola, con una certa frequenza, come un riepilogo del lunedì sulle trattative aperte. Si limita a leggere.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: ed2171ef31eb6213
---
## Creane una

Apri **Routine** nella barra laterale e descrivi in una riga cosa deve fare e quando: "ogni lunedì alle 9, riassumi le mie trattative aperte" oppure "ogni mattina dei giorni feriali, elenca le email a cui devo ancora rispondere". Poi tocca **Aggiungi**.

Se non specifichi un orario, la routine viene eseguita alle 8:00. L’orario si basa su quello della tua Machine. Alla prima esecuzione viene assegnato un nome breve.

Per prima cosa, **Aggiungi** esegue un test, così puoi vedere il risultato prima di conservarla. Non viene inviato né salvato nulla. Poi **Aggiungi** la mantiene attiva secondo la frequenza impostata, **Cambia** prova altre parole o un nuovo nome e **Annulla** la elimina.

## Modelli

In fondo a Routine, sotto **Modelli**, tocca **Aggiungi** per attivare una routine già pronta. Viene eseguita subito una volta, poi ogni mattina alle 7:30 (Pulizia spam ogni ora, Abbonamenti e prove una volta al mese). La scheda ne mostra il testo, come per qualsiasi routine, e **Modifica** permette di cambiarne il testo o il nome.

Se arrivano molte newsletter e Pulizia newsletter è disattivata (almeno 25 in una settimana, da almeno 5 mittenti), sopra le attività da fare appare un messaggio con il numero di newsletter ricevute e l’azione prevista, insieme a **Attivala** e **No, grazie**.

Pulizia spam viene proposta allo stesso modo se in una settimana hai spostato manualmente nello spam almeno 5 email. **Attivala** la aggiunge come farebbe **Aggiungi** qui. Se tocchi **No, grazie**, non verrà più proposta. Lo stesso vale per un modello che avevi già usato in precedenza.

**Pulizia newsletter** crea un’attività da fare per ogni area, lavoro e personale, con le newsletter ricevute nell’ultimo giorno. Per ognuna puoi scegliere **Tieni** o **Disiscriviti**. Per disiscriverti, usa il link per la disiscrizione con un clic, oppure l’email di disiscrizione inviata dal tuo indirizzo, se l’invio è attivo. Altrimenti, The Machine si disiscrive dalla pagina della lista usando il proprio browser. Se la pagina richiede l’accesso, un captcha o una scelta, dovrai occupartene tu: la riga spiega il motivo e mostra **Apri la pagina di disiscrizione**.

Le ricevute, gli ordini e le notifiche di pagamento vengono esclusi. Le email ricevute tramite un indirizzo di gruppo, come un Google Group, sono elencate sotto il nome di chi le ha scritte e non ti disiscrivono mai dal gruppo. Se il mittente non ha un sistema di disiscrizione, la riga mostra **Disiscriviti a mano**.

**Pulizia spam** crea un’attività da fare per ogni area, con le email di mittenti sconosciuti che sembrano spam. Per ognuna puoi scegliere **Spam** o **Non è spam**. Outlook sposta le email nella posta indesiderata, mentre Gmail le contrassegna come spam. Il controllo avviene ogni ora, quindi di solito lo spam viene individuato prima che tu lo veda. Le nuove email di spam vengono aggiunte alla stessa attività finché è aperta.

Se Gmail è collegato in sola lettura, come su una Machine ospitata, non è possibile spostare le email nello spam. In questo caso, **Spam** mostra un link per contrassegnare l’email come spam in Gmail e The Machine memorizza il mittente come spam. Se non è collegato nessun account email, al posto di **Aggiungi** il modello mostra **Collega la posta**.

Un mittente è sconosciuto se non gli hai mai scritto. Un oggetto che inizia con "Re:" viene considerato una conversazione solo se hai scritto tu nella conversazione. Se ricevi di nuovo un’email da un mittente che hai contrassegnato come spam, nell’attività o nella posta, comparirà nella prossima attività con l’etichetta **Già segnato come spam**. Le email che hai spostato manualmente nello spam aiutano anche a individuare email simili.

Non cambia nulla finché non confermi nell’attività da fare. Tocca un mittente per leggere prima l’email: resterà non letta e non cambierà nulla. Da Pulizia spam, le immagini dal web non vengono caricate, così il mittente non può sapere che hai aperto l’email. Non ti verrà chiesto di nuovo cosa fare con i mittenti per cui hai già scelto. Se in un giorno non arrivano newsletter o spam, non viene creata nessuna attività. Queste attività non inviano mai notifiche.

Quando hai scelto cosa fare per tutti i mittenti, l’attività indica che è completata e mostra **Segna come fatto**.

**Riepilogo giornaliero** seleziona le poche newsletter che meritano la tua attenzione e le raccoglie ogni giorno in un’unica attività. Per ognuna indica brevemente perché potrebbe interessarti. Toccala per leggere l’email oppure usa **Apri nella tua posta**. Include solo newsletter, mai email di persone, ricevute o mittenti da cui ti sei disiscritto, e mai contenuti che hai già letto. Se non trova niente di interessante, non crea nessuna attività.

Impara cosa ti interessa in base a ciò che apri, aggiungi ai preferiti o archivi senza leggere, e a **Altri così** e **Meno così** su ogni selezione. Gli argomenti che usa per scegliere sono indicati nella scheda della routine, sotto **Più su** e **Meno su**. Tocca × per rimuovere un argomento o aggiungine uno. Quelli tratteggiati sono stati individuati automaticamente. Un nuovo riepilogo sostituisce quello ancora aperto e non invia mai notifiche.

Legge solo il mittente, l’oggetto e l’inizio di ogni nuova newsletter, poi pone alla tua AI una breve domanda al giorno per contenere i costi. **Cambia quando** permette di impostare l’orario. Dopo che ne modifichi il testo, la routine funziona come qualsiasi altra e usa le tue indicazioni.

**Compleanni** crea un’attività da fare per ogni persona a te vicina che compie gli anni oggi: persone a cui scrivi tu, come amici, familiari e contatti abituali. Per ognuna prepara un breve messaggio di auguri nella chat o nella conversazione email che usi di solito, per esempio nella chat WhatsApp o nella tua conversazione email, e nella sua lingua. Il messaggio viene inviato solo quando lo invii tu. Se non ci sono compleanni quel giorno, non viene creata nessuna attività.

I compleanni vengono recuperati dai tuoi calendari (gli eventi di compleanno di Google e il calendario Compleanni, letto ogni mattina anche se non è sincronizzato, e il calendario Compleanni di Outlook), dai tuoi contatti Google su una Machine autogestita e da un campo data chiamato Birthday associato a una persona nel Graph. Se nessuna di queste fonti contiene ancora un compleanno, il risultato mostra **Non ci sono ancora informazioni sui compleanni** e spiega come aggiungerne.

**Importa i compleanni da Facebook**: dopo aver attivato Compleanni, un’attività da fare ti propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e The Machine la apre nel proprio browser, scorre la pagina finché non sono stati caricati tutti i mesi e legge il nome e il compleanno di ogni amico. Ti mostra quanti ne ha trovati e quali corrispondono a persone nel tuo Graph, in base a nome e cognome. I nomi associati a più di una persona vengono ignorati e indicati nell’elenco.

Solo toccando **Salva** i dati vengono conservati nella pagina di ogni persona: la data di compleanno e, per chi non ha ancora una foto, l’immagine del profilo Facebook. Le date di compleanno e le foto che imposti lì restano. Una foto già presente non viene mai sostituita. Non viene scritto nulla su Facebook.

La pagina non viene riletta automaticamente: per farlo, tocca **Importa di nuovo** nell’attività da fare. Il browser deve aver effettuato l’accesso a Facebook. Se non hai ancora effettuato l’accesso, tocca **Accedi a Facebook** nell’attività e accedi da lì. Una volta effettuato l’accesso, la pagina viene letta automaticamente. The Machine non effettua mai l’accesso al posto tuo.

Il sistema conta anche gli amici che non corrispondono a nessuna persona nel tuo Graph e ne mostra alcuni nomi. **Aggiungi … come contatti personali** li aggiunge tutti insieme, anche dopo aver toccato Salva. Per ognuno vengono aggiunti il nome e il compleanno, che non vengono mai condivisi con una Fleet di lavoro. Vengono ignorati i nomi già presenti nel tuo Graph e quelli di persone che avevi eliminato definitivamente. I promemoria di compleanno vengono comunque creati solo per le persone a cui scrivi.

Toccando **Annulla** nell’attività da fare, rimuovi esattamente le persone importate, anche dopo aver usato **Importa di nuovo**.

**Abbonamenti e prove** controlla una volta al mese le tue ricevute, fatture e notifiche di rinnovo, poi raccoglie gli abbonamenti in un’unica attività da fare. Per ognuno indica il costo, la data del prossimo addebito e se sta per terminare un periodo di prova o aumentare il prezzo. Elenca solo gli abbonamenti di cui è certa. Se non ne trova, non crea nessuna attività.

Scegli **Tieni** o **Disdici** per ogni abbonamento. Non ti verrà chiesto di nuovo se vuoi tenere un abbonamento, a meno che il prezzo non cambi. Se scegli **Disdici**, viene mostrata la pagina per annullare l’abbonamento oppure una bozza con la richiesta di annullamento, che verrà inviata solo se la invii tu. Tra un controllo mensile e l’altro, verifica ogni giorno e crea un’attività se un periodo di prova o un rinnovo verrà addebitato entro 7 giorni.

Finché una routine di un modello mantiene il testo del modello, viene eseguita con il proprio codice, senza usare il tuo piano AI. Pulizia spam, per esempio, individua prima nel codice le nuove email di mittenti sconosciuti e pone alla tua AI una breve domanda solo se ne trova. Se cambi il nome, il codice resta invariato. Dopo che modifichi il testo, la routine funziona come qualsiasi altra e usa le tue indicazioni.

Pulizia newsletter e Pulizia spam continuano a creare la stessa attività da fare, con una scelta per ogni email. Se modifichi Compleanni, il risultato mostra al massimo una bozza, non un’attività per ogni persona. Tocca **Torna al modello** in **Modifica** per ripristinare il testo originale.

## Cosa fa una routine

All’orario impostato, la tua Machine legge ciò che serve, per esempio messaggi, riunioni e Graph, e mostra il risultato nella pagina Routine. Ogni risultato indica **Pronta**, **Niente di nuovo** con il motivo oppure **Non è andato** con il motivo. Un’esecuzione che termina senza produrre un risultato viene considerata non riuscita, mai completata.

Le routine si limitano a leggere: messaggi, pagine web, GitHub e siti come X nel browser. Non inviano messaggi, non rispondono, non pubblicano e non modificano nulla. Solo un modello può modificare le email, e solo dopo la tua conferma nell’attività da fare.

Se un’attività della routine termina con un post o un messaggio, la routine esegue tutti i passaggi precedenti e mostra una bozza, per esempio **Pubblicheresti su X:**. Dopo un’esecuzione effettiva, la bozza viene mostrata come attività da fare da approvare; un’esecuzione di prova mostra solo il risultato. Il nome indica di cosa si tratta e dove verrà pubblicato o inviato, il pulsante indica il passaggio, per esempio **Pubblicalo**, e la voce **Dalla tua routine** sotto apre la routine.

L’attività da fare appare nell’area dell’account da cui verrà inviata, per esempio Lavoro per l’account X della tua azienda, così non ti verrà mai chiesto di spostarla.

Un’esecuzione può seguire le tue [skill](skills.md) attive, selezionate in base a ciò che fa la routine: vengono lette per intero solo quelle pertinenti. Il risultato le elenca sotto **Usate:**. Una skill non fa mai inviare messaggi o modificare dati a una routine.

Le tue routine si trovano sotto **Le tue routine**, dopo eventuali suggerimenti. I risultati lunghi vengono ridotti a un’anteprima breve. Tocca **Mostra altro** o il risultato per aprirlo.

Ogni esecuzione conosce il risultato precedente, così può indicare cosa è cambiato.

Dopo un’esecuzione riuscita, la tua Machine può scriversi una ricetta per le operazioni di lettura che si ripetono, come quali email o modifiche di GitHub controllare. Le esecuzioni successive partono da queste operazioni, scritte in codice semplice, e usano l’AI solo per scegliere cosa è importante e scriverlo, con meno token. Una ricetta si limita a leggere. Se smette di funzionare, la routine esegue la lettura autonomamente e la corregge. La ricetta compare sotto **Avanzate: passaggi di script** nel menu ⋯.

## Giorni saltati

Se la tua Machine era spenta o occupata, le esecuzioni saltate non si accumulano: viene eseguita una sola volta la più recente. Ogni data viene elaborata una sola volta, anche dopo il riavvio.

Le routine vengono eseguite una alla volta e attendono se l’utilizzo del tuo piano AI è basso, come tutte le attività in background. **Esegui ora** avvia subito la routine. Il risultato compare sulla scheda quando è pronto.

## Modificala o fermala

Le opzioni si trovano nel menu ⋯ della routine. **Modifica** permette di cambiare il nome e le attività, senza modificare la frequenza o i risultati ottenuti. **Cambia quando** permette di impostare una nuova frequenza con parole tue, per esempio "ogni giorno feriale alle 8". Entrambe le opzioni mostrano **Salva** e **Annulla**. Su un computer puoi anche premere Esc o fare clic fuori per annullare.

In **Modifica**, tocca **Provalo** per eseguire una volta la routine con il nuovo testo e vedere il risultato. La routine resta com’è finché non tocchi **Salva**.

**Metti in pausa** interrompe le esecuzioni fino a quando non tocchi **Riprendi** sulla scheda. Le routine in pausa si trovano sotto **In pausa**, dopo le tue routine, e le esecuzioni saltate durante la pausa non verranno recuperate. **Ferma** interrompe definitivamente una routine.

Puoi avere fino a 20 routine, comprese quelle in pausa. Fermane una per aggiungerne un’altra.

Quando usi **Chiedi modifiche** nell’attività da fare di una routine o scrivi nella chat della routine, e le tue indicazioni valgono per tutte le esecuzioni, per esempio "non usare mai emoji", l’attività da fare ti propone **Cambia anche la routine**. L’opzione compare nell’attività e nella chat, sotto la risposta. Viene mostrato cosa cambierebbe nel testo della routine, che cambia solo se tocchi **Cambiala**. **Lasciala così** la lascia invariata. Se chiedi una modifica solo alla bozza, non viene proposta nessuna modifica alla routine.

## Avanzate: passaggi di script

Non serve scrivere uno script: descrivi con parole tue cosa deve fare una routine e la tua Machine si occupa del resto.

Per chi ha più esperienza, una routine può anche eseguire comandi personalizzati sulla tua Machine: dal menu ⋯, scegli **Avanzate: passaggi di script**. **Modifica** mostra i passaggi solo se la routine ne contiene già. **Recupera dati** esegue prima un comando, nella sua cartella o, se il campo è vuoto, nella cartella home, per un massimo di secondi specificato. Il risultato stampato viene passato all’esecuzione. Se non inserisci testo, il risultato stampato diventa il risultato della routine.

**Verifica** riceve il risultato come input al termine dell’esecuzione. Se il comando termina con un errore, il risultato mostra **Non è andato** e il messaggio restituito dal controllo. Anche un comando di Recupera dati non riuscito mostra lo stesso messaggio.

Un comando deve stare su una sola riga e viene eseguito senza shell: niente pipe o variabili. Gli script sono impostati solo nella tua dashboard. Un’esecuzione di prova e **Provalo** eseguono anche Recupera dati e te lo indicano, ma non inviano né conservano nulla. Una routine non invia mai nulla, quindi un passaggio di script dovrebbe limitarsi a leggere.

## Dai tuoi job di OpenClaw

Se in passato hai creato job programmati in OpenClaw, la tua Machine li legge, senza modificarli, e propone quelli adatti come routine sotto **Suggerito**. Ogni job è stato eseguito una volta, quindi puoi vedere un risultato reale.

La routine conserva le correzioni apportate al job ed esclude ciò che il job ha inviato o pubblicato. Se un job eseguiva uno script o leggeva dati raccolti da uno script, lo script viene aggiunto come Recupera dati. **Aggiungi** lo trasforma in una routine, mentre **No, grazie** fa sì che quel job non venga più proposto. Se un job ti ricordava di fare qualcosa, viene proposto in To-do come attività ricorrente.

Prima di aggiungere un suggerimento, puoi modificarlo come qualsiasi routine da **Modifica** e **Cambia quando** nel menu ⋯. **Esegui di nuovo** lo avvia subito con il testo corrente, così puoi vedere risultati più recenti, per esempio dopo un fine settimana tranquillo. Si limita a leggere, viene eseguito una volta per tocco e il nuovo risultato sostituisce quello precedente.

Possono esserci al massimo tre suggerimenti in attesa. Dopo una settimana di esecuzioni riuscite, la routine chiede **Disattivare il vecchio job di OpenClaw?**. Il job viene disattivato solo se tocchi **Disattiva**. Puoi riattivarlo in OpenClaw. **Tienilo** lascia attivi entrambi.

## In base a quello che fai

La tua Machine nota anche le attività che svolgi con regolarità e le propone come routine sotto **Suggerito**, anche senza OpenClaw. Cerca:

- la stessa richiesta almeno tre volte di fila, per esempio "riassumi i ticket di assistenza aperti" ogni lunedì;
- un’email che invii regolarmente, come un rapporto settimanale al tuo team;
- newsletter e email di aggiornamento che arrivano ogni settimana;
- un canale Slack molto attivo in cui altre persone scrivono ogni settimana;
- email che inoltri una alla volta alla stessa persona, come quelle della scuola o del club al tuo partner: un riepilogo settimanale evita di doverle inoltrare;
- la stessa richiesta a cui rispondi regolarmente, come un’approvazione mensile per la stessa persona.

Ogni suggerimento spiega cosa ha rilevato, per esempio "Richiesto 4 volte di fila" oppure "Inoltrate 6 email a Sam in 3 settimane", ed è stato eseguito una volta per mostrarti un risultato reale. Potrebbe trattarsi di un riepilogo del team, di un breve resoconto prima di una chiamata settimanale, di un riepilogo delle attività di assistenza o sviluppo, di un aggiornamento sui tuoi numeri o di un riepilogo delle newsletter che ricevi.

Vengono proposte solo routine specifiche per te e chiaramente utili: per esempio, un riepilogo delle notizie basato solo sulle tue newsletter, mai un riepilogo generico. Se non trova niente di adatto, non viene mostrato nessun suggerimento.

La ricerca avviene al massimo una volta al giorno e viene proposto al massimo un nuovo suggerimento alla settimana, senza inviare notifiche. Toccando **No, grazie**, il suggerimento non viene più riproposto. Gli inoltri e le risposte restano associati all’account da cui sono stati inviati, così Lavoro e Personale non si mescolano. Tutto resta sulla tua Machine. Un’attività da fare che completi regolarmente viene invece proposta come attività ricorrente.

## Routine e attività ricorrenti

Un’[attività ricorrente](recurring.md) ti ricorda di fare qualcosa. Una routine è un’attività che la tua Machine svolge da sola e ti mostra. Usa un’attività ricorrente per "pagare l’affitto il primo del mese" e una routine per "ogni venerdì, dimmi quali trattative si sono arenate".
