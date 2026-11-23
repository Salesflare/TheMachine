---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo sì. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 88ccf5426e5a538f
---
La tua Machine legge tutto ciò che è nuovo e crea un’attività solo quando serve il tuo intervento. Un’attività per ogni questione, anche se coinvolge più messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in alto trovi l’ultimo passaggio che hai confermato, come un modulo o una segnalazione, completato mentre non c’eri. Rimane lì finché non tocchi **Ho capito**, per un giorno al massimo, e ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che aspetta il tuo intervento, a partire dalle cose più urgenti. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e puoi completare l’operazione con **Fallo** o **Invia**), **Serve il tuo intervento** (prima serve una tua decisione o una risposta; se il lavoro si è fermato per qualcosa che solo tu puoi fornire, come un dato, un accesso o una scelta, una riga sotto il titolo spiega cosa serve), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un brief, senza decisioni da prendere).
- **Più vecchie**: attività raccolte in un gruppo chiuso, senza novità da una settimana (vedi sotto).
- **In attesa di altri**: attività raccolte in un gruppo chiuso, in cui il prossimo passaggio spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: ciò che hai promesso e ciò che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatto 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviato. Spostata in Fatte.» o «Inviato. Spostata in Più tardi fino a lunedì». Se la risposta si limita a promettere che il lavoro verrà fatto, per esempio «Te lo mando entro martedì», l’attività resta aperta: «Inviato. Lasciata aperta». **Apri** ti porta all’attività. La ricerca trova le attività per titolo o per destinatario, anche in Più tardi e Fatte.

In **Per te** vengono prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, i follow-up di una bacheca e infine tutte le altre. All’interno di ogni gruppo, le più recenti vengono prima. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e anche quando è fatta: cambia solo il contrassegno. Negli altri gruppi aperti, prima vengono le attività scadute o in scadenza entro domani, poi le più recenti. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine ha rilevato che è stato completato, per esempio «PR #3451 unita», ma non è ancora chiuso. **Riapri** lo rimette nella tua lista e aiuta la tua Machine a imparare. Queste attività non risultano mai in ritardo. Quando un messaggio mostra che è stato completato, l’attività si chiude da sola dopo un giorno e puoi usare **Annulla**. Altrimenti resta in attesa che tu selezioni **Segna come fatto**. Si chiude da sola anche un’attività che hai già gestito, per esempio con una risposta in Gmail o Slack.

Se un messaggio arriva da un indirizzo che somiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Non è Sam Lee». La persona viene mostrata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica il passaggio con **In attesa di:**. Si trova in **In attesa di altri**, in un gruppo chiuso sopra Torna più tardi, finché un nuovo messaggio non la riporta nella lista. Lo stesso vale dopo che hai risposto a una domanda: l’attività torna la mattina prima della scadenza, il giorno stesso se la scadenza è più tardi, oppure la mattina successiva se è già passata. Indica anche chi deve ancora rispondere.

Quando un’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, **Dettagli** lo indica alla voce **Fatto quando**. Inviare la tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non mostra il risultato, poi si chiude da sola e puoi usare **Annulla**. Se non arriva nulla entro il momento in cui è il caso di sollecitare, l’attività torna con **Scrivi un breve sollecito** nella chat. Per modificare cosa conta come completamento, scrivilo nella chat.

Dopo una settimana senza novità, un’attività passa da Per te a **Più vecchie**, così, dopo qualche giorno di assenza, le attività nuove vengono prima. Non ci sono novità se non è arrivato un nuovo messaggio e non hai fatto nulla sull’attività, come scrivere in chat, modificarla o posticiparla. Aprirla non conta.

Le attività urgenti, quelle in scadenza a breve e quelle con un invio in corso restano in Per te. **Scarta tutto** contrassegna come non necessarie tutte le attività in Più vecchie dopo una sola conferma, proprio come fa **Non serve** con una sola attività. Puoi usare **Annulla**. Se arriva una novità, l’attività torna in Per te.

Dopo una settimana senza che nessuno abbia toccato un’attività, viene chiesto una volta: **Serve ancora?** Con **Non serve** l’attività si chiude e puoi usare **Annulla**. **Tieni** la mantiene e la domanda non viene più ripetuta. Se non rispondi per un’altra settimana, l’attività passa al gruppo chiuso Torna più tardi e non viene più conteggiata nel numero sull’icona dell’app né nel riepilogo del mattino. Se la apri, scrivi un messaggio in chat, la modifichi, la posticipi o arriva un nuovo messaggio, torna nella lista.

Una volta alla settimana, un progetto rimasto fermo e senza attività aperte può generare un’attività con un solo prossimo passaggio specifico, per un massimo di tre a settimana. Vedi [Progetti](projects.md).

Quando non c’è nulla che richiede il tuo intervento, la tua Machine si riposa e la lista resta vuota. Mentre controlla, si attiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, la riga lo indica e mostra **Controlla ora**.

Le voci **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività oppure solo quelle di un tipo. La scelta è la stessa su telefono e computer. Quando è attivo Lavoro o Personale, **Mostra tutto** riporta alla lista completa. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima alla lista permette anche di passare direttamente all’altra vista: con **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima alla lista mostra il tuo ultimo riepilogo del mattino o della sera e cosa conteggia, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Tocca la riga per rileggere il riepilogo e usare **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, resta su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non c’è un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato fatto oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per l’area selezionata.

Un’attività associata a un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. **Progetto** in **Dettagli** permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

Con **Area** in **Dettagli** puoi spostare un’attività nell’altra area. Anche le fonti che può leggere e da cui può inviare messaggi si spostano con lei. **Annulla** nella nota la riporta indietro.

Se per proseguire un’attività serve l’altra area e tutti i messaggi da cui proviene si trovano lì, l’attività si sposta da sola e continua. Altrimenti viene mostrato **Sposta in Lavoro** e non si sposta nulla finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola quando trova l’area giusta. Fino ad allora non è indicata né come Lavoro né come Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi della tua altra area, te lo chiede con **Usa questa email per questa attività**. Un account di lavoro che hai contrassegnato come Personale viene considerato Personale. Le email per un’altra delle tue aziende finiscono nelle attività di quell’azienda. Un’attività che riguarda la tua vita personale, per esempio un familiare che scrive al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. Lavoro o Personale determina dove compare un’attività e con chi è condivisa, mai dove viene inviata la risposta: la risposta va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Anche un’attività Personale di questo tipo risponde dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro o nel Graph del team.

Se hai almeno due attività in attesa, **Scorri** nell’intestazione di Per te le esamina una alla volta, nell’ordine della lista, mostrando ogni bozza per intero e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Su computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta e Esc interrompe. L’intestazione indica quanto tempo ci vuole al tuo ritmo, per esempio «circa 2 min».

Alla fine mostra quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Le attività che ti fanno una domanda non vengono incluse: aspettano una tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, di giorno e di notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa oppure quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, la voce Controlli indica «In pausa per la notte, recupero alle 06:30». Se di notte fai clic, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non ti assenti per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla con **Dettagli**, che apre Controlli in Connessioni. Se hai attività aperte, la trovi in alto su computer. La breve riga compare solo mentre è in corso un controllo o quando uno non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i loro ritmi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga con i risultati di tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». Si riferisce solo a quel controllo: le attività già presenti nella lista restano invariate. Se una nuova attività deve aspettare il momento giusto, per esempio il riepilogo del mattino, la riga indica fino a quando: «1 attività rimandata a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica, con l’icona della fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività, oppure il motivo per cui non serviva farne una, per esempio «Solo in cc, risponde un collega» o «Riunione già fissata per giovedì». Una conversazione non mostra il motivo se il controllo ne ha restituito uno vago. Tocca un elemento per leggerlo.

Vengono mostrati i primi 10 elementi. Toccando sotto, vedi gli altri. Il numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già in elenco viene mostrata una sola volta. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email che hai ricevuto. Le tue risposte vengono lette per capire il contesto e le promesse, ma non sono nuove email. Le email inviate dalla tua Machine, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email su fatturazione, periodo di prova o inviti vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passaggio, come **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

Con **Chiedi modifiche** puoi indicare cosa cambiare: come svolgere l’attività oppure, quando una bozza è pronta, cosa modificare nella bozza. **Segna come fatto** indica che è tutto gestito: compare subito su un’attività pronta senza bozza, altrimenti in cima al menu **…**, anche per quelle che richiedono una tua decisione. L’attività scompare subito dalla lista e puoi usare **Annulla** nel messaggio. Scorri il messaggio per chiuderlo oppure trascinalo fuori con il mouse. La modifica resta.

Per completare l’attività in un altro modo, scrivilo nella sua **Chat**. La risposta indica solo cosa è cambiato, per esempio il posticipo e fino a quando. Se non è stato possibile modificare qualcosa, come una data di scadenza, te lo dice.

Nel menu **…**:

- **Passa…**: assegnala a un collega, a [Claude Code o Codex](hand-to-agent.md) oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: l’attività [si ripresenta con una certa frequenza](recurring.md).
- **Non serve**: l’attività scompare. Puoi anche indicare il motivo: **Non pertinente**, **Fatti sbagliati** oppure **Già gestito**. La tua Machine impara da queste indicazioni.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività. Puoi anche chiederlo nella chat, per esempio «Rinominala …». Il titolo che scegli resta.

**Riapri** riporta nella lista un’attività chiusa. Può tornare anche da sola quando succede qualcosa di nuovo, per esempio se arriva un nuovo messaggio da quella persona, ma non per una tua risposta. A quel punto mostra quando è tornata e viene ordinata come nuova. La chat riprende da dove si era interrotta, anche dopo settimane.

Una bolletta che devi ancora pagare tu, da qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dati di pagamento indicati nella bolletta. Quelle pagate automaticamente, per esempio con un addebito diretto o una carta registrata, non diventano attività. Quando un’email successiva mostra che è stata pagata, per esempio una conferma di pagamento del mittente, l’attività si chiude da sola. Puoi usare **Annulla** per un giorno.

Un’attività utile solo fino a un determinato momento, come una conferma da ricevere prima di una riunione, si chiude da sola dopo quell’ora. Passa in **Fatte / scartate** con l’indicazione «Non serve più». Puoi usare **Annulla** per un giorno.

Prima che un messaggio o un passaggio a qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, comprese le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché qualcuno ha fatto una richiesta e ha ricevuto un sì, si chiude da sola. Puoi usare **Annulla** per un giorno.

Se qualcun altro scrive nella stessa conversazione dopo la creazione della bozza, **Invia** la blocca: «Non inviato: nuovo messaggio nella conversazione». L’attività mostra quel messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per spedire la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna da sola le attività. Quelle ancora utili seguono i nuovi piani. Quelle che non richiedono più alcuna azione passano in **Fatte / scartate** con l’indicazione «Non serve». Nella chat compare «Aggiornato:» seguito dal motivo e puoi usare **Annulla** per un giorno.

Alla prima apertura delle attività, un breve suggerimento mostra le azioni principali: **Chiedi modifiche** e **Non serve**, e ricorda che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente dopo che usi il pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un messaggio di benvenuto che indica chi aspetta da più tempo una tua risposta. La bozza di quella risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica di chi si tratta, l’organizzazione se pertinente, ma non solo perché qualcuno ci lavora, il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se il Graph ne ha una, accanto al nome e all’organizzazione compare la foto o il logo; altrimenti vengono mostrate le iniziali. Se un logo non si legge bene in piccolo, per esempio perché è bianco su sfondo trasparente o è un marchio lungo, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto via email 12 giorni fa, nessun’altra novità». Compare quando l’ultimo contatto è vecchio o senza risposta e indica i canali non collegati, come WhatsApp. La tua Machine dice cosa non sa invece di tirare a indovinare.

Se viene indicato un canale non collegato, tocca Connetti accanto al suo nome per aprire la relativa connessione.

Il titolo indica cosa bisogna fare e cambia solo se cambia l’attività. Un’attività completata mantiene il suo titolo e mostra sotto come è finita, per esempio «Fatto: Sam l’ha firmato martedì».

Sopra la bozza, una riga in grigio chiaro indica il messaggio da cui proviene e mostra il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo della destinazione, così vedi subito se si tratta di una risposta su Slack o di un’email.

Se la bozza segue un’indicazione ricevuta altrove, per esempio un suggerimento di un collega su Slack, una riga lo indica, per esempio «In base a Sam in #ops». Tocca la riga per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra un’unica conversazione, dalla più vecchia alla più recente: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal i tuoi messaggi sono sulla destra, come nell’app. Il messaggio relativo all’attività è contrassegnato con «Questa attività» e viene visualizzato. **Mostra messaggi precedenti** aggiunge i messaggi più vecchi. In un’email, il resto della conversazione è raccolto in sezioni chiuse sopra e sotto il messaggio.

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android si apre nell’app Gmail, se è installata.

In **Dettagli** di un’email trovi solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, i destinatari in Ccn o un indirizzo diverso per le risposte. Se non c’è altro da aggiungere, la sezione non compare.

Una risposta in una conversazione Slack mostra anche i messaggi precedenti all’inizio della conversazione. Il link di un’attività al suo messaggio apre anche quel messaggio, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area dell’attività, che puoi modificare toccandoli, la tua ultima nota e il risultato di un agente di programmazione. Tocca il titolo per aprire la chat. Le attività completate restano compatte; il messaggio da cui provengono si trova in **Dettagli**.

Un’attività «In attesa di» contiene il link al tuo ultimo messaggio per quella persona, quello a cui aspetti risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** su computer, **+** sul telefono o `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non scegli **Lavoro** o **Personale**, l’attività viene assegnata all’area giusta in base a chi e a cosa riguarda. Trova anche l’email a cui si riferisce, incluse quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore», anche nella tua lingua. L’icona del calendario mostra le date rapide e l’opzione **Scegli una data**.
- **Si ripete**: l’attività si ripresenta con una certa frequenza. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, come un’email, un messaggio su Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile alla tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina dei file nel modulo. Sul telefono, tocca la fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come in chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano associati all’attività e la tua Machine li legge mentre ci lavora. Puoi allegare solo i file: la tua Machine crea l’attività a partire da un PDF o da un file di testo. Una foto viene mostrata in piccolo: toccala per vederla a grandezza naturale.
