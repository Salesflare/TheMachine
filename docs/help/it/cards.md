---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo ok. Scopri cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 4209ed807e753101
---
La tua Machine legge tutto ciò che arriva di nuovo e crea un’attività solo quando serve il tuo intervento. Un’attività per ogni questione, anche se coinvolge molti messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in cima, trovi un ultimo passaggio che hai confermato, come un modulo o una richiesta, completato mentre eri via. Resta qui finché non tocchi **Ho capito**, per un giorno al massimo, e ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che aspetta il tuo intervento, in ordine di urgenza. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima serve una tua decisione o una risposta; se il lavoro è fermo perché manca qualcosa che solo tu puoi fornire, come un’informazione, l’accesso o una scelta, una riga sotto il titolo spiega cosa manca), **In preparazione…** (la tua Machine ci sta lavorando) o **Da leggere** (un riepilogo o un breve aggiornamento, senza decisioni da prendere).
- **Più vecchie**: attività chiuse, senza novità da una settimana (vedi sotto).
- **In attesa di altri**: attività chiuse in cui il prossimo passaggio spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e quelle senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: le promesse che hai fatto e quelle che altri hanno fatto a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatto 5 minuti fa». Le attività che sembrano già completate sono contrassegnate come **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviata. Spostata in Fatte.» o «Inviata. Spostata in Più tardi fino a lunedì». Se la risposta si limita a promettere che il lavoro verrà fatto, per esempio «Te la mando entro martedì», l’attività resta aperta: «Inviata. Lasciata aperta». **Apri** ti porta all’attività. La ricerca trova un’attività in base al titolo o al destinatario, anche in Più tardi e Fatte.

In **Per te** vengono prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, i promemoria di una bacheca e infine il resto. All’interno di ogni gruppo, le più recenti vengono prima. Un’attività resta al suo posto mentre la tua Machine la prepara e quando è completata: cambia solo il contrassegno. Negli altri gruppi aperti, vengono prima quelle scadute o in scadenza entro domani, poi le altre dalla più recente. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede l’attività come completata, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e aiuta la tua Machine a imparare. Queste attività non risultano mai in ritardo. Se un messaggio ne indica il completamento, si chiude automaticamente dopo un giorno e puoi usare **Annulla**. Altrimenti, resta in attesa che tu tocchi **Segna come fatto**. Anche un’attività che hai già gestito da solo, per esempio rispondendo in Gmail o Slack, si chiude automaticamente.

Se un messaggio proviene da un indirizzo che somiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Questo non è Sam Lee». Mostra la persona con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica **In attesa di:** e il passaggio previsto. Si trova in **In attesa di altri**, chiusa sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso vale dopo che hai fatto una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se cade più tardi oggi, oppure la mattina successiva se la scadenza è già passata. Indica anche chi deve ancora rispondere.

Quando un’attività riguarda un risultato che deve fornire qualcun altro, per esempio un contratto firmato, **Dettagli** lo indica alla voce **Fatto quando**. Inviare la tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude automaticamente e puoi usare **Annulla**. Se non arriva nulla entro il momento in cui dovresti sollecitare, l’attività torna con **Scrivi un breve sollecito** nella chat. Per modificare cosa conta come completamento, scrivilo nella chat.

Un’attività senza novità da una settimana passa da Per te a **Più vecchie**, così dopo qualche giorno di assenza trovi prima quelle nuove. Per novità si intende un nuovo messaggio sull’attività o un’azione che hai fatto, come un messaggio in chat, una modifica o un posticipo. Aprirla e basta non conta.

Le attività urgenti, in scadenza a breve o con un invio in corso restano in Per te. **Scarta tutto** contrassegna tutte le attività in Più vecchie come non necessarie dopo una sola conferma, proprio come fa **Non serve** con una alla volta. Puoi usare **Annulla**. Una novità su un’attività la riporta in Per te.

Se nessuno interviene su un’attività per una settimana, viene chiesto una volta: **Serve ancora?** **Non serve** la chiude, con la possibilità di usare **Annulla**. **Tieni** la mantiene e non verrà più chiesto. Se non rispondi per un’altra settimana, l’attività viene chiusa in Torna più tardi e smette di essere conteggiata sul badge dell’app e nel riepilogo del mattino. Aprirla, inviare un messaggio in chat, modificarla, posticiparla o ricevere un nuovo messaggio la riporta nell’elenco.

Una volta alla settimana, un progetto rimasto inattivo e senza attività aperte può ricevere un’attività con un singolo passaggio successivo specifico, fino a un massimo di tre a settimana. Vedi [Progetti](projects.md).

Quando non serve il tuo intervento, la tua Machine resta in attesa con un elenco vuoto. Durante una verifica si riattiva e te lo comunica. Se una verifica non è riuscita o è in ritardo, la riga lo indica e mostra **Controlla ora**.

Le opzioni **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer viene applicata la stessa scelta. Quando è selezionato Lavoro o Personale, **Mostra tutto** torna alla vista completa. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima all’elenco permette anche di passare direttamente all’altra vista: in **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il titolo dell’ultimo riepilogo del mattino o della sera e il numero di elementi conteggiati, per esempio **Riepilogo di ieri sera** · 12 completate, 3 aperte. Toccalo per rileggere quel riepilogo e usare **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, resta disponibile su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non c’è un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per il filtro selezionato.

Un’attività collegata a un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. La voce **Progetto** in **Dettagli** permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

La voce **Area** in **Dettagli** sposta un’attività nell’altra area. Anche i messaggi che può leggere e da cui può inviare messaggi vengono spostati. **Annulla** sulla nota la riporta dov’era.

Se un’attività ha bisogno dell’altra area per proseguire e tutti i messaggi da cui proviene sono lì, viene spostata automaticamente e il lavoro continua. Altrimenti mostra **Sposta in Lavoro** e non viene spostata finché non la tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale viene spostata automaticamente quando trova l’area giusta. Nel frattempo non è assegnata né a Lavoro né a Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, ti chiede di usare **Usa questa email per questa attività**. Una casella di lavoro che hai etichettato Personale viene considerata Personale. Le email per un’altra delle tue aziende vanno alle attività di quell’azienda. Un’attività sulla tua vita privata, per esempio un messaggio di famiglia arrivato al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, per esempio un cliente su WhatsApp, un ordine nella tua casella personale o una [promessa](promises.md) di lavoro, è Lavoro fin dall’inizio.

Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. Lavoro o Personale determina dove compare un’attività e con chi viene condivisa, mai dove risponde: la risposta va sempre nella conversazione da cui proviene, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Anche se è Personale, un’attività di questo tipo risponde dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro o nel Graph del team.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta e Esc interrompe. L’intestazione indica quanto tempo serve al tuo ritmo, per esempio «circa 2 min».

Alla fine viene indicato quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Le attività che ti fanno una domanda non vengono incluse: richiedono una risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa o quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, la voce Controlli indica «In pausa per la notte, recupero alle 06:30». Se di notte clicchi, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non ti allontani per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per vedere i dettagli e aprire Controlli in Connessioni. Se hai attività aperte, la trovi in cima all’elenco sul computer. Una breve riga compare solo durante un controllo o se un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, una riga sopra le attività indica cosa ha trovato in ogni fonte letta, per esempio «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». Si riferisce solo a quel controllo: le attività già nell’elenco restano in attesa. Se una nuova attività aspetta un momento migliore, per esempio il riepilogo del mattino, viene indicato fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica con l’icona del servizio di provenienza, chi ha scritto, l’oggetto o le prime parole e la nuova attività oppure il motivo per cui non serviva farne una, per esempio «Solo in Cc, risponde un collega» o «Riunione già fissata per giovedì». Una conversazione non mostra il motivo se il controllo ne ha indicato uno vago. Tocca un elemento per leggerlo insieme al contesto.

Vengono mostrati i primi 10 elementi; toccando sotto, vedi gli altri. Un numero accanto a un nome, per esempio (3), indica quanti nuovi messaggi contiene quella chat. Una notifica sul telefono per un messaggio già nell’elenco compare una volta sola. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email ricevute. Le tue risposte vengono lette per avere contesto e tenere traccia delle promesse, ma non sono nuove email. Le email che la tua Machine invia a te, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email sulla fatturazione, sul periodo di prova o su un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il passaggio successivo, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. **Segna come fatto** indica che l’attività è stata gestita: è visibile su un’attività pronta senza bozza o su una che ti fa una domanda, altrimenti si trova in cima al menu **…**. L’attività scompare subito dall’elenco e nel messaggio compare **Annulla**. Per chiuderla prima, scorri via il messaggio o trascinalo fuori con il mouse. La modifica resta.

Per farla svolgere in un altro modo, scrivilo nella **Chat** dell’attività. La risposta indica solo cosa è cambiato, per esempio un posticipo e fino a quando. Se non è stato possibile modificare qualcosa, come la data di scadenza, te lo dice.

Nel menu **…**:

- **Passa…**: assegnala a un collega, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: l’attività [torna con una certa frequenza](recurring.md).
- **Non serve**: l’attività scompare. Puoi anche scegliere il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara da questa scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominarla. Puoi anche chiedere nella chat, per esempio «Rinominala in…». Il titolo che scegli resta invariato.

**Riapri** riporta un’attività chiusa nell’elenco. L’attività torna anche automaticamente quando succede qualcosa di nuovo, per esempio se arriva un nuovo messaggio da quella persona, ma non dopo una tua risposta. In quel caso indica quando è tornata e viene ordinata come nuova. La chat riprende da dove si era fermata, anche dopo settimane.

Una fattura che devi ancora pagare tu, di qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dati per il pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta salvata, non diventano attività. Se un’email successiva indica che è stata pagata, per esempio il mittente conferma di aver ricevuto il pagamento, l’attività si chiude automaticamente. **Annulla** la riporta nell’elenco per un giorno.

Un’attività che serve solo fino a un momento preciso, per esempio una conferma prima di una riunione, si chiude automaticamente dopo quel momento. Viene spostata in **Fatte / scartate** con la dicitura «Non serve più». **Annulla** la riporta nell’elenco per un giorno.

Prima che un messaggio o un passaggio per qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, comprese le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo indica che è già tutto fatto, per esempio perché è stato chiesto qualcosa e qualcuno ha risposto sì, l’attività si chiude automaticamente. **Annulla** la riporta nell’elenco per un giorno.

Se qualcun altro scrive nella stessa conversazione dopo la preparazione della bozza, **Invia** la mette in attesa: «Non inviata: nuovo messaggio nella conversazione». L’attività mostra quel messaggio con **Leggila** e **Rifai per questo messaggio**. Tocca di nuovo **Invia** per inviare la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna le attività autonomamente. Un’attività ancora necessaria segue i nuovi piani. Se non resta nulla da fare, viene spostata in **Fatte / scartate** con la dicitura «Non serve». Nella chat compare «Aggiornamento:» con il motivo e **Annulla** la riporta nell’elenco per un giorno.

Nelle prime attività, un breve suggerimento mostra le azioni principali: **Chiedi modifiche** e **Non serve**, e spiega che non viene inviato nulla finché non tocchi **Invia**. Il suggerimento scompare definitivamente quando usi il pulsante o tocchi ×.

Il primo giorno, in cima ad Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La bozza di quella risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica di chi si tratta, l’organizzazione se pertinente, mai solo perché la persona ci lavora, il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la pagina della persona nel Graph.

Se nel Graph sono disponibili, il nome e l’organizzazione mostrano una foto o un logo, altrimenti le iniziali. Se un logo è difficile da leggere in piccolo, per esempio perché è bianco su uno sfondo trasparente o perché è una scritta molto larga, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non è noto, per esempio «Ultimo contatto 12 giorni fa via email; nessun aggiornamento». Compare se l’ultimo contatto è lontano nel tempo o senza risposta e indica i canali non collegati, come WhatsApp. La tua Machine dice cosa non sa invece di fare supposizioni.

Quando viene indicato un canale non collegato, tocca **Connetti** accanto al nome per collegarlo.

Il titolo indica cosa va fatto e cambia solo se cambia l’attività. Un’attività completata mantiene il suo titolo e mostra sotto come si è conclusa, per esempio «Fatto: Sam l’ha firmato martedì».

Sopra la bozza, una riga tenue indica il messaggio da cui proviene, con il logo del servizio. Toccalo per leggere la conversazione. La bozza mostra il logo della destinazione, così vedi subito se è una risposta su Slack o un’email.

Se la bozza segue il contributo di qualcuno altrove, per esempio un suggerimento di un collega su Slack, una riga lo indica, per esempio «In base a Sam in #ops». Tocca la riga per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra un’unica conversazione in ordine cronologico, dal più vecchio: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal, i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato da «Questa attività» e si apre nella conversazione. **Mostra messaggi precedenti** aggiunge i messaggi più vecchi. In un’email, il resto della conversazione è chiuso sopra e sotto il messaggio.

Un messaggio si apre allo stesso modo dalla ricerca, dal Graph, dalle risposte di Ask o dall’ultimo controllo, con l’etichetta «Questo messaggio» o «Nuovi messaggi».

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android, la apre nell’app Gmail se è installata.

**Dettagli** di un’email mostra solo le informazioni non visibili nell’intestazione, come gli indirizzi Cc completi, i Bcc o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, non mostra nulla.

Una risposta in una conversazione Slack mostra anche cosa è stato detto prima dell’inizio della conversazione. Il link di un’attività al proprio messaggio lo apre anche qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area, che puoi modificare toccandoli, la tua ultima nota e il risultato di un agente di programmazione. Tocca il titolo per aprire la chat. Un’attività completata resta compatta; il messaggio da cui proviene si trova in **Dettagli**.

Un’attività «In attesa di» collega il tuo ultimo messaggio a quella persona, quello a cui stai aspettando una risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) aggiunge un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, viene assegnata all’area giusta in base alla persona e all’argomento. Trova anche l’email a cui si riferisce, comprese quelle meno recenti.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14:00» o «tra 2 ore», anche nella tua lingua. L’icona del calendario offre opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività torna con una certa frequenza. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega fino a 5 persone o aziende a cui si riferisce.
- Icona del messaggio: allega il messaggio a cui si riferisce, per esempio un’email o un messaggio di Slack, Teams, WhatsApp, Telegram o un altro servizio disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato mostra la provenienza, chi l’ha inviato e quando.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, l’icona della fotocamera accanto scatta una foto. Puoi allegare fino a 5 file, come nella chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano allegati all’attività e la tua Machine li legge mentre ci lavora. Puoi creare un’attività anche solo con dei file: la tua Machine la compila a partire da un PDF o da un file di testo. Una foto viene mostrata come immagine piccola: toccala per vederla a grandezza naturale.
