---
title: Routine
area: cards
summary: Lavoro che la tua Machine fa da sola, con un ritmo, come un riepilogo del lunedì dei tuoi deal aperti. Legge soltanto.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, dashboard/routines-page.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays
---
## Crearne una

Apri **Routine** nella barra laterale e di’ in una riga cosa deve fare e quando: "ogni lunedì alle 9, riassumi i miei deal aperti" o "ogni giorno feriale al mattino, elenca le email a cui devo ancora rispondere". Poi **Aggiungi**.

Senza un orario, gira alle 8:00. L’orario è quello dell’orologio della tua Machine.

## Modelli

In **Modelli**, in fondo a Routine, **Aggiungi** attiva una routine già pronta. Parte subito una volta e poi ogni mattina alle 7:30 (Pulizia spam ogni ora). La sua scheda mostra le sue parole come ogni routine, e **Modifica** cambia le parole o il nome.

**Pulizia newsletter** crea un’attività per area (lavoro e personale) con le newsletter dell’ultimo giorno, ognuna con **Tieni** o **Disiscriviti**. La disiscrizione usa il link a un clic della lista, o la sua email di disiscrizione dal tuo indirizzo se l’invio è attivo. Altrimenti mostra **Apri la pagina di disiscrizione**.

Ricevute, ordini e avvisi di pagamento restano fuori. Una email arrivata tramite un indirizzo di gruppo, come un Google Group, è elencata sotto chi l’ha scritta e non ti disiscrive mai dal gruppo.

**Pulizia spam** crea un’attività per area con la posta di mittenti sconosciuti che sembra spam, ognuna con **Spam** o **Non è spam**. Outlook sposta lo spam in Posta indesiderata e Gmail lo segna come spam. C’è solo per la posta che The Machine può spostare: Gmail collegato in sola lettura non ce l’ha. Controlla ogni ora, così lo spam di solito è lì prima che tu ci arrivi. Il nuovo spam va nella stessa attività finché è aperta.

Sconosciuto vuol dire che non gli hai mai scritto, e un “Re:” conta come conversazione solo in un thread in cui hai scritto. Se passa di nuovo posta da un mittente che hai segnato come spam, nell’attività o nella tua casella, è nella prossima attività come **Già segnato come spam**. Quello che hai spostato tu nello spam la aiuta anche a riconoscere posta simile.

Nulla cambia finché non confermi sull’attività. Tocca un mittente per leggere prima l’email: resta da leggere e non cambia nulla. Da Pulizia spam le sue immagini dal web non si caricano, così il mittente non vede che è stata aperta. I mittenti già decisi non tornano. Un giorno senza newsletter né spam non crea attività, e queste attività non mandano mai una notifica.

**Compleanni** crea un’attività per ogni contatto stretto che compie gli anni oggi: le persone a cui scrivi tu, come amici, famiglia e contatti abituali. Ognuna ha un breve augurio scritto dove di solito parlate, come la loro chat WhatsApp o il tuo thread email, nella loro lingua. Parte solo quando lo invii tu. Un giorno senza compleanni non crea attività.

I compleanni vengono dai tuoi calendari (i compleanni e il calendario Compleanni di Google, letti ogni mattina anche se non sono sincronizzati, e il calendario Compleanni di Outlook), dai tuoi contatti Google su una Machine self-hosted e da un campo data chiamato Compleanno su una persona del Graph. Se nessuno ha ancora un compleanno, il risultato dice **Ancora nessun compleanno** e come aggiungerne.

**Importa i compleanni da Facebook**: con Compleanni attivo, un’attività propone di leggere la pagina dei compleanni di Facebook. Tocca **Importa** e The Machine la apre nel suo browser, scorre finché ogni mese è caricato e legge nome e compleanno di ogni amico. Mostra quanti ne ha trovati e chi corrisponde per nome e cognome a persone del tuo Graph. Un nome che ha più di una persona viene saltato ed elencato.

Solo **Salva** li conserva, e solo il compleanno, sulla pagina di ogni persona. Un compleanno che hai inserito lì resta. Non rilegge mai da sola: lo fa **Importa di nuovo** sull’attività. Il browser deve avere l’accesso a Facebook. Se non ce l’ha, tocca **Accedi a Facebook** sull’attività e accedi lì; poi legge la pagina da sola. The Machine non accede mai al posto tuo.

Gli amici che nessuno nel tuo Graph ha vengono contati, con alcuni nomi. **Aggiungi … come contatti personali** li aggiunge tutti insieme, anche dopo Salva: ognuno con nome e compleanno, mai condiviso con una Work Fleet. Un nome che ha già qualcuno nel tuo Graph, o che aveva qualcuno eliminato definitivamente, viene saltato. I promemoria di compleanno arrivano sempre solo per le persone a cui scrivi.

**Annulla** sull’attività toglie esattamente quelle persone, anche dopo **Importa di nuovo**.

Finché le sue parole sono quelle del modello, gira con il suo codice, senza il tuo piano di IA (Pulizia spam elenca prima con il codice la posta nuova di mittenti sconosciuti, e fa una breve domanda alla tua IA solo quando ce n’è). Un nuovo nome non cambia nulla. Se cambi le sue parole, gira come ogni routine sulle tue parole.

Pulizia newsletter e Pulizia spam finiscono sempre nella stessa attività con una scelta per email. Compleanni modificato dà il suo risultato e al massimo una bozza, non un’attività per persona. **Torna al modello** in **Modifica** rimette le sue parole.

## Cosa fa una routine

All’orario stabilito, la tua Machine legge ciò che le serve, come i tuoi messaggi, le riunioni e il Graph, e mette il risultato nella pagina Routine. Ogni risultato dice **Pronta**, **Niente di nuovo** (con il perché) o **Non è andato** (con il perché). Un’esecuzione che finisce senza risultato conta come non riuscita, mai come fatta.

Le routine leggono soltanto: i tuoi messaggi, pagine web, GitHub e siti come X nel browser. Non inviano, rispondono, pubblicano né cambiano nulla. Solo un modello cambia la posta, e solo ciò che confermi sulla sua attività.

Quando il compito di una routine finisce con un post o un messaggio, fa tutto fino a quel passo e mostra la bozza, come **Pubblicherebbe su X:**. Dopo un’esecuzione vera la ricevi come attività da approvare; un’esecuzione di prova la mostra soltanto. Il nome dice di cosa si tratta e dove va, il pulsante nomina il passo, come **Pubblicalo**, e **Dalla tua routine** sotto apre la routine.

L’attività parte nell’area dell’account da cui esce, come Lavoro per l’account X della tua azienda, quindi non chiede mai di spostarla.

Ogni esecuzione conosce l’ultimo risultato, così può dire cosa è cambiato da allora.

Dopo una buona esecuzione, la tua Machine può scriversi una ricetta per la lettura che è uguale ogni volta, come quali email o modifiche GitHub guardare. Le esecuzioni successive leggono prima quello, con codice semplice, e l’IA sceglie solo ciò che conta e lo scrive, con meno token. Una ricetta legge soltanto; se smette di funzionare, l’esecuzione legge da sé e la ripara. La vedi in **Avanzate: passaggi di script** nel menu ⋯.

## Giorni persi

Se la tua Machine era spenta o occupata, le esecuzioni perse non si accumulano: gira solo la più recente, una volta. Ogni data gira una volta, anche dopo un riavvio.

Le routine girano una alla volta e aspettano quando l’uso del tuo piano IA è basso, come tutto il lavoro in background. **Esegui ora** la esegue subito.

## Cambiarla o fermarla

È nel menu ⋯ della routine. **Cambia quando** prende un nuovo ritmo con parole tue, come "ogni giorno feriale alle 8". **Metti in pausa** ferma le esecuzioni fino a **Riprendi**; ciò che è stato perso durante la pausa non gira dopo. **Ferma** chiude una routine per sempre.

Quando usi **Chiedi modifiche** su un’attività di una routine, o scrivi nella sua chat, e la tua nota vale per ogni esecuzione, come "mai emoji", l’attività offre **Cambia anche la routine**, sull’attività e nella sua chat sotto la risposta. Mostra cosa cambia nelle parole della routine, e la routine cambia solo quando tocchi **Cambiala**. **Lasciala così** la lascia com’è. Una correzione solo di quella bozza non offre nulla.

## Avanzate: passaggi di script

Non ti serve mai uno script: di’ con parole tue cosa deve fare una routine.

Per gli utenti esperti, una routine può anche eseguire i tuoi comandi sulla tua Machine: nel menu ⋯, scegli **Avanzate: passaggi di script**. **Modifica** li mostra solo se una routine ne ha già. **Recupera dati** esegue prima un comando, nella sua cartella (vuota: la tua cartella home) e al massimo per i suoi secondi. Ciò che stampa va all’esecuzione per lavorarci. Senza parole, ciò che stampa è il risultato.

**Verifica** riceve il risultato come input dopo l’esecuzione. Se termina con un errore, l’esecuzione mostra **Non è andato** con ciò che ha detto la verifica. Un comando di Recupera dati che fallisce si mostra allo stesso modo.

Un comando è una riga e gira senza shell: niente pipe né variabili. I passaggi di script sono tuoi, si impostano solo sulla tua dashboard. Un’esecuzione di prova e **Provalo** eseguono anche Recupera dati e lo dicono; comunque non inviano e non tengono nulla. Una routine non invia mai, quindi un passaggio di script dovrebbe solo leggere.

## Dai tuoi job di OpenClaw

Se prima avevi creato job pianificati in OpenClaw, la tua Machine li legge (non li cambia mai) e propone quelli adatti come routine in **Suggerito**. Ognuno è stato eseguito una volta, così vedi un risultato vero.

Tiene le tue correzioni al job e lascia fuori ciò che inviava o pubblicava. Un job che eseguiva uno script, o leggeva ciò che raccoglieva un job di script, lo porta come Recupera dati. **Aggiungi** ne fa una routine, **No, grazie** non chiede mai più di quel job. Un job che ti ricordava di fare qualcosa arriva invece come offerta di attività ricorrente in Attività.

Prima di aggiungere un suggerimento, **Modifica** e **Cambia quando** nel suo menu ⋯ lo cambiano come qualsiasi routine. **Esegui di nuovo** lo esegue ora con le sue parole attuali, per vedere risultati più recenti, per esempio dopo un fine settimana tranquillo. Legge soltanto, gira una volta per tocco e il nuovo risultato sostituisce quello vecchio.

Aspettano al massimo tre suggerimenti alla volta. Dopo una settimana di buone esecuzioni, la routine chiede **Disattivare il vecchio job di OpenClaw?** Si disattiva solo quando tocchi **Disattiva**, e puoi riattivarlo in OpenClaw.

## Da quello che fai

La tua Machine nota anche il lavoro che fai con un ritmo e lo propone come routine in **Suggerito**, anche senza OpenClaw. Cerca:

- la stessa richiesta, tre volte o più di fila, come "riassumi i ticket di supporto aperti" ogni lunedì;
- un’email che invii con un ritmo, come un report settimanale al tuo team;
- newsletter ed email di aggiornamento che arrivano ogni settimana;
- un canale Slack molto attivo dove altri scrivono ogni settimana;
- email che inoltri una per una alla stessa persona, come quelle della scuola e del club al tuo partner: un riepilogo settimanale per quella persona ti risparmia gli inoltri;
- la stessa richiesta a cui rispondi con un ritmo, come un’approvazione mensile per la stessa persona.

Ogni suggerimento dice cosa ha visto, come "Chiesto 4 volte di fila" o "6 email inoltrate a Sam in 3 settimane", ed è stato eseguito una volta perché tu veda un risultato vero. Pensa a un riepilogo del team, un brief prima di una call settimanale, un riepilogo del supporto o dello sviluppo, il polso dei tuoi numeri o un riassunto delle newsletter che ricevi.

Propone solo ciò che è tuo e chiaramente utile: un riassunto di notizie solo sulle tue newsletter, mai uno generico. Quando niente va bene, non c’è nessun suggerimento.

Guarda al massimo una volta al giorno e porta al massimo un nuovo suggerimento a settimana, senza notifica. **No, grazie** non lo riporta mai. Inoltri e risposte restano con l’account da cui sono partiti, così Lavoro e Personale non si mescolano. Tutto resta sulla tua Machine. Un’attività che chiudi con un ritmo arriva invece come offerta di attività ricorrente.

## Routine e attività ricorrenti

Un’attività ricorrente (recurring.md) ti ricorda di fare qualcosa. Una routine è lavoro che la tua Machine fa da sola e ti mostra. Usa un’attività ricorrente per "pagare l’affitto il primo del mese", e una routine per "ogni venerdì, dimmi quali deal si sono fermati".
