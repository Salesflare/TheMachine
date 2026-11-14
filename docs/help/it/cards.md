---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via libera. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
La tua Machine legge ogni nuovo messaggio e crea un’attività solo quando qualcosa richiede il tuo intervento. Un’attività per ogni questione, anche se coinvolge molti messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa così:

- **Per te**: tutto ciò che aspetta una tua risposta, a partire dalle cose più urgenti. Ogni attività indica **Preparata** (il lavoro è pronto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima serve una tua decisione o una risposta) oppure **In preparazione…** (la tua Machine ci sta lavorando).
- **Appena fatto**: un ultimo passaggio che hai confermato, come un modulo o una segnalazione, è andato a buon fine mentre non c’eri. Rimane qui finché non tocchi **Ho capito**, al massimo per un giorno, e ricevi una notifica anche sul telefono.
- **Torna più tardi**: attività posticipate e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: le promesse che hai fatto e quelle che altri hanno fatto a te. Vedi [Promesse](promises.md).
- **Fatte / ignorate**: tutte le attività concluse, dalla più recente, con l’ora in cui sono state concluse, per esempio «Fatta 5 minuti fa». Le attività che sembrano già concluse sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviata. Spostata in Fatte.» o «Inviata. Spostata in Più tardi fino a lunedì». **Apri** ti porta all’attività. La ricerca trova un’attività in base al titolo o al destinatario, anche in Più tardi e in Fatte.

In **Per te** compaiono per prime le attività scadute o in scadenza entro domani, poi le domande della tua Fleet e infine le altre. In ogni gruppo, le più recenti vengono prima. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e quando è conclusa: cambia solo il contrassegno. Negli altri gruppi aperti, le attività scadute o in scadenza entro domani vengono prima, seguite dalle più recenti. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che l’attività è conclusa, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e la tua Machine impara da questa scelta. Queste attività non vengono mai indicate come in ritardo. Dopo un giorno si chiudono da sole, con **Annulla**. Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola.

Quando un messaggio arriva da un indirizzo che assomiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Non è Sam Lee». La persona viene mostrata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi ha scritto.

Un’attività che aspetta ancora un’altra persona, per esempio una revisione o una risposta, indica il passaggio con **In attesa di:**. Si trova in **In attesa di altri**, in un gruppo chiuso sopra Torna più tardi, finché un nuovo messaggio non la riporta tra le attività. Lo stesso vale dopo che hai risposto con una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se cade più tardi oggi oppure la mattina seguente se è già passata. Indica anche chi deve ancora rispondere.

Quando un’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, **Dettagli** lo mostra in **Fatto quando**. L’invio della tua parte non chiude l’attività: rimane in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola, con **Annulla**. Se non arriva nulla entro il momento in cui è ora di sollecitare, l’attività riappare con **Scrivi un breve sollecito** nella sua chat. Per cambiare cosa significa che è conclusa, scrivilo nella chat.

Un’attività che nessuno tocca per una settimana chiede una volta: **Serve ancora?** **Non serve** la chiude, con **Annulla**. **Tieni** la mantiene e non te lo chiede più. Se non rispondi per un’altra settimana, viene spostata nel gruppo chiuso Torna più tardi e non viene più conteggiata sul numero dell’icona dell’app né nel riepilogo del mattino. Se la apri, scrivi un messaggio nella chat, la modifichi, la posticipi o arriva un nuovo messaggio, torna tra le attività.

Una volta alla settimana, un progetto fermo e senza attività aperte può generare un’attività con un prossimo passo specifico, fino a tre a settimana. Vedi [Progetti](projects.md).

Quando niente richiede il tuo intervento, la tua Machine riposa e l’elenco rimane vuoto. Mentre esegue un controllo, si risveglia e te lo dice. Se un controllo non è riuscito o è in ritardo, la riga lo segnala e mostra **Controlla ora**.

Le viste **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività oppure solo quelle di un tipo. Sul telefono e sul computer trovi la stessa selezione. Quando è attiva la vista Lavoro o Personale, **Mostra tutto** ti riporta a tutte le attività. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

Anche la riga in cima all’elenco permette di passare direttamente a un’altra vista: **Solo Personale · Lavoro · Mostra tutto**.

La riga in cima all’elenco indica il tuo ultimo riepilogo del mattino o della sera e cosa comprende, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Toccala per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Una volta aperto o dopo aver toccato la sua **×**, rimane su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non hai un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato fatto oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per la vista che hai selezionato.

Un’attività relativa a un progetto mostra il nome del progetto sotto il titolo. Toccandolo, apri il progetto. **Progetto** in **Dettagli** permette di cambiarlo o rimuoverlo. Vedi [le attività di un progetto](projects.md#a-projects-to-dos).

**Area** in **Dettagli** sposta un’attività nell’altra area. Anche l’accesso ai messaggi che può leggere e a cui può rispondere si sposta con lei. **Annulla** nella nota la riporta indietro.

Quando per procedere un’attività deve passare all’altra area e tutti i messaggi da cui proviene sono già lì, si sposta da sola e prosegue. Altrimenti mostra **Sposta in Lavoro** e non si sposta finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola una volta individuata l’area giusta. Fino ad allora non è indicata né come Lavoro né come Personale e rimane privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se per procedere ha bisogno di altri messaggi dell’altra area, te lo chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai etichettato come Personale viene considerata Personale. I messaggi per un’altra delle tue aziende finiscono nelle attività di quell’azienda, mentre un’attività sulla tua vita personale, come una mail di famiglia arrivata al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu rimane sempre dove l’hai messa. Lavoro o Personale determina dove compare un’attività e con chi viene condivisa, mai dove risponde: la risposta va sempre nella conversazione da cui proviene, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata la sua email e non compare mai in una Fleet di lavoro o nel Graph del team.

Quando ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza completa e i pulsanti **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta e Esc interrompe. Sotto il titolo, l’intestazione indica anche quanto tempo serve al tuo ritmo, per esempio «circa 2 min».

Un’attività che ti fa una domanda non viene inclusa in nessuna delle due viste: aspetta una tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa oppure quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Controlli, sotto Connessioni, compare «In pausa per la notte, recupera alle 06:30». Se di notte apri l’app, scrivi nella chat o tocchi un’attività, i controlli riprendono normalmente finché non ti assenti per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla, con **Dettagli**, che apre Controlli sotto Connessioni. Se hai attività aperte, la trovi in cima all’elenco sul computer. La riga breve compare solo mentre è in corso un controllo o quando un controllo non è riuscito o è in ritardo. Puoi anche chiedere nella chat.

LinkedIn, X e Salesflare mantengono i propri ritmi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, una riga sopra le attività indica cosa ha trovato in ogni fonte letta, per esempio «Controllati 13 messaggi alle 16:11 · niente richiede il tuo intervento» oppure «· 2 nuove attività». Quando una nuova attività viene rimandata a un momento più adatto, per esempio al riepilogo del mattino, la riga indica fino a quando: «1 attività rimandata a domani alle 08:30».

Tocca la riga per vedere ogni thread email, chat e notifica, con l’icona del servizio corrispondente: chi ha scritto, l’oggetto o le prime parole, e la nuova attività oppure il motivo per cui non serviva farne una, per esempio «Sei solo in Cc, risponde un collega» o «Riunione già fissata per giovedì». Un thread non mostra il motivo quando il controllo ne ha trovato solo uno generico. Tocca un elemento per leggerlo.

Vengono mostrati i primi 10 elementi; tocca sotto per vedere gli altri. Un numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già nell’elenco viene mostrata una sola volta. La riga rimane visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email indirizzate a te. Le tue risposte vengono lette per avere contesto e seguire le promesse, ma non sono nuove email. Le email che la Machine invia a te, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email sulla fatturazione, sul periodo di prova o su un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il suo prossimo passaggio, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. **Segna come fatto** indica che è stata gestita: si trova in vista su un’attività pronta senza bozza, altrimenti in cima a **…**, anche su un’attività che richiede una tua decisione. L’attività lascia subito l’elenco e nel messaggio compare **Annulla**. Scorri il messaggio per eliminarlo oppure trascinalo fuori con il mouse per chiuderlo prima. La modifica viene mantenuta.

Per farla in un altro modo, scrivilo nella sua **Chat**.

Sotto **…**:

- **Passa…**: affidala a un collega, a [Claude Code o Codex](hand-to-agent.md) oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: l’attività [si ripresenta a intervalli regolari](recurring.md).
- **Non serve**: l’attività scompare. Se vuoi, scegli il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara da questa scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività. Il titolo che scegli rimane.

**Riapri** riporta un’attività chiusa nell’elenco. Può riapparire anche da sola quando succede qualcosa di nuovo, per esempio quando la persona ti scrive, ma non quando rispondi tu.

Una fattura che devi ancora pagare tu, di qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dati di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta salvata, non diventano attività. Quando un’email successiva indica che è stata pagata, per esempio una conferma del mittente che il pagamento è arrivato, l’attività si chiude da sola. **Annulla** la riporta tra le attività per un giorno.

Un’attività che serve solo fino a un momento preciso, come una conferma prima di una riunione, si chiude da sola dopo quell’ora. Viene spostata in **Fatte / ignorate** con la dicitura «Non serve più». **Annulla** la riporta tra le attività per un giorno.

Prima di indicare come pronta un’azione o un passaggio di consegne per qualcuno, la tua Machine controlla le chat recenti con le persone coinvolte, incluse le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che è già stato fatto, per esempio perché qualcuno ha ricevuto una richiesta e ha risposto di sì, l’attività si chiude da sola. **Annulla** la riporta tra le attività per un giorno.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna da sola le attività. Se un’attività serve ancora, segue i nuovi piani. Se non resta più nulla da fare, viene spostata in **Fatte / ignorate** con la dicitura «Non serve»; nella chat compare «Aggiornamento:» con il motivo e **Annulla** la riporta tra le attività per un giorno.

Tra le prime attività compare un breve suggerimento sulle azioni principali: **Chiedi modifiche** e **Non serve**, e sul fatto che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il relativo pulsante o premi ×.

Il primo giorno, in cima ad Attività compare un saluto e viene indicata la persona che aspetta più a lungo una tua risposta. La sua risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica di chi si tratta, l’organizzazione se l’attività riguarda un’organizzazione (mai solo perché una persona ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la pagina della persona nel Graph.

I nomi e le organizzazioni mostrano la foto o il logo, se il Graph ne ha uno, altrimenti le iniziali. Se un logo è difficile da leggere in piccolo, per esempio perché è bianco su sfondo trasparente o perché è un marchio con una scritta larga, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessun messaggio da allora». Compare quando l’ultimo scambio con quella persona è vecchio o senza risposta, e indica i canali non collegati, come WhatsApp. La tua Machine dice cosa non sa invece di tirare a indovinare.

Quando la riga indica un canale non collegato, accanto compare Connetti per aprire la relativa connessione.

Il titolo indica cosa bisogna fare e cambia solo se cambia l’attività. Un’attività conclusa mantiene il titolo e mostra sotto come si è conclusa, per esempio «Fatta: Sam l’ha firmata martedì».

Una riga discreta sopra la bozza indica il messaggio da cui proviene, con il logo del servizio. Toccala per leggere il thread. La bozza mostra il logo della destinazione, così vedi subito se è una risposta su Slack o un’email.

Se la bozza si basa su un contributo ricevuto altrove, per esempio un suggerimento di un collega su Slack, una riga lo indica, per esempio «Basata su un messaggio di Sam in #ops». Toccala per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra un’unica conversazione, dalla più vecchia alla più recente: i messaggi prima di quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e viene aperto direttamente. **Mostra messaggi precedenti** aggiunge quelli più vecchi. Le altre parti del thread email sono raccolte sopra e sotto il messaggio.

I **Dettagli** di un’email mostrano solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, il Bcc o un indirizzo diverso per le risposte. Se non c’è altro da aggiungere, i dettagli non compaiono.

Una risposta in un thread Slack mostra anche cosa è stato detto prima che iniziasse il thread. Anche il link dell’attività al suo messaggio apre il messaggio qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area (tocca uno di questi elementi per modificarlo), la tua ultima nota e il risultato di un agente di programmazione. **Chat ›** apre la chat. Un’attività conclusa rimane sintetica; il messaggio da cui proviene si trova in **Dettagli**.

Un’attività **In attesa di** collega il tuo ultimo messaggio a quella persona, quello a cui stai aspettando risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni Lavoro o Personale, l’attività va nell’area giusta in base alla persona e all’argomento. Trova anche l’email a cui fa seguito, comprese quelle meno recenti.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14:00» o «tra 2 ore», anche nella tua lingua. L’icona del calendario mostra alcune opzioni rapide e **Scegli una data**.
- **Messaggio**: allega il messaggio a cui si riferisce, che sia un’email, un messaggio su Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio presente nella tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, la fotocamera accanto scatta una foto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungi file](card-chat.md#add-files)). × rimuove un file.

I file rimangono associati all’attività e The Machine li legge mentre ci lavora. Puoi aggiungere anche solo dei file: ricava i dettagli dell’attività da un PDF o da un file di testo. Una foto viene mostrata come immagine piccola: toccala per vederla a grandezza naturale.
