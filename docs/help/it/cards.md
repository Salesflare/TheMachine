---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per la tua approvazione. Scopri cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: b218e3423a2162c5
---
La tua Machine legge tutto ciò che arriva e crea un’attività solo quando serve il tuo intervento. Un’attività per ogni questione, anche se riguarda più messaggi.

## Dove si trovano le attività

La pagina **Attività** le raggruppa così:

- **Appena fatto**: in cima, mostra un ultimo passaggio che hai confermato, per esempio l’invio di un modulo o la risoluzione di un problema mentre eri via. Resta lì finché non tocchi **Ho capito**, al massimo per un giorno. Ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che aspetta te, prima le attività in scadenza entro domani. Ognuna ha uno di questi stati: **Preparata** (una bozza o un risultato è pronto e con **Fallo** o **Invia** puoi completare l’operazione), **Serve il tuo intervento** (prima serve una tua decisione o una risposta; se il lavoro non può proseguire o essere usato senza qualcosa che solo tu puoi fornire, come un prezzo, un’informazione o una scelta, una riga sotto il titolo spiega cosa serve), **In preparazione…** (la tua Machine ci sta lavorando) o **Da leggere** (un riepilogo o un breve testo, senza decisioni da prendere).
- **Più vecchie**: attività ripiegate su cui non ci sono novità da una settimana (vedi sotto).
- **In attesa di altri**: attività ripiegate in cui il prossimo passaggio spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate, messaggi che [verranno inviati più tardi](send-later.md) e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: ciò che hai promesso e ciò che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatta 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviata. Spostata in Fatte» oppure «Inviata. Spostata in Più tardi fino a lunedì». Se una risposta si limita a promettere di fare qualcosa, come «Te lo invio entro martedì», l’attività resta aperta: «Inviata. Lasciata aperta». **Apri** ti porta all’attività. La ricerca trova le attività per titolo o per destinatario, anche in Più tardi e Fatte.

In **Per te** compaiono prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, quindi i promemoria di una bacheca e infine le altre. In ogni gruppo, le più recenti vengono prima. Un’attività resta al suo posto mentre la tua Machine la prepara e quando viene completata: cambia solo il contrassegno. Negli altri gruppi aperti compaiono prima le attività scadute o in scadenza entro domani, poi le altre in ordine dalla più recente. Anche la barra laterale segue lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che l’attività è stata completata, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e la tua Machine impara da questa scelta. Queste attività non risultano mai in ritardo. Se un messaggio mostra che è stata completata, si chiude automaticamente dopo un giorno e compare **Annulla**. Altrimenti resta in attesa che tu scelga **Segna come fatto**.

Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude automaticamente. Una risposta che dice che un file è allegato quando invece non lo è, non la chiude.

Se un messaggio arriva da un indirizzo che somiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Questo non è Sam Lee». La persona viene indicata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica il passaggio con **In attesa di:**. Si trova in **In attesa di altri**, ripiegata sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso vale dopo che hai fatto una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è prevista più tardi in giornata, oppure la mattina successiva se la scadenza è già passata. Indica anche chi deve ancora rispondere.

Se l’attività riguarda un risultato che deve fornire qualcun altro, per esempio un contratto firmato, in **Dettagli** lo trovi indicato come **Fatto quando**. Inviare la tua parte non la chiude: resta in **In attesa di altri** finché un messaggio non mostra il risultato, poi si chiude automaticamente e mostra il risultato e **Annulla**. Se il risultato non arriva entro il momento in cui è ora di sollecitare, l’attività torna con **Scrivi un breve sollecito** nella chat. Per cambiare i criteri di completamento, scrivilo nella chat.

Prima di chiudere l’attività, la tua Machine confronta il risultato con quanto concordato nella conversazione, per esempio il prezzo, il testo o il link che hai inviato. La chiude solo se corrispondono e indica cosa ha controllato. Se qualcosa non coincide, se hanno saltato la tua approvazione o se la tua parte di uno scambio è ancora in sospeso, l’attività torna e spiega il motivo.

Se il risultato deve comparire su una pagina web pubblica indicata nei messaggi, per esempio un articolo in cui comparirai, quando è il momento di sollecitare la tua Machine controlla la pagina. Se il risultato è presente e non lo era quando l’attività ha iniziato ad aspettare, la pagina viene verificata allo stesso modo prima della chiusura. La Machine si limita a leggere la pagina, come farebbe qualsiasi visitatore, e non invia mai nulla.

Se il risultato non compare sulla pagina e la scadenza non è ancora arrivata, la tua Machine la controlla di nuovo la mattina dopo la scadenza. Altrimenti l’attività torna come prima, con «Controllata» o «Impossibile aprirla» e la pagina nella chat.

Dopo una settimana senza novità, un’attività passa da Per te a **Più vecchie**, così dopo qualche giorno di assenza le attività nuove vengono mostrate per prime. Per novità si intende un nuovo messaggio o una tua azione, come un messaggio in chat, una modifica o un posticipo. Aprire l’attività non conta.

Le attività urgenti, quelle in scadenza a breve e quelle con un invio in corso restano in Per te. **Scarta tutto** contrassegna come non necessarie tutte le attività in Più vecchie, dopo una sola conferma. Per le singole attività puoi usare **Non serve**. In entrambi i casi puoi usare **Annulla**. Se arriva una novità, l’attività torna in Per te.

Dopo una settimana senza che nessuno intervenga, un’attività chiede una volta: **Serve ancora?** **Non serve** la chiude, con la possibilità di usare **Annulla**. **Tieni** la mantiene aperta e la domanda non verrà ripetuta. Se non rispondi per un’altra settimana, l’attività viene ripiegata in Torna più tardi e non viene più conteggiata sul badge dell’app né nel riepilogo del mattino. Aprirla, inviare un messaggio in chat, modificarla, posticiparla o ricevere un nuovo messaggio la riporta nell’elenco.

Una volta alla settimana, un progetto rimasto inattivo e senza attività aperte può generare un’attività con un prossimo passaggio specifico, fino a un massimo di tre alla settimana. Vedi [Progetti](projects.md).

Quando non serve il tuo intervento, la tua Machine resta inattiva e l’elenco è vuoto. Durante un controllo, si riattiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, lo indica con **Controlla ora** sotto.

I filtri **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer trovi la stessa selezione. Quando è attivo Lavoro o Personale, **Mostra tutto** riporta alla visualizzazione completa. Gli avvisi che riguardano la tua Machine, per esempio un componente che continua a riavviarsi, non sono né di Lavoro né Personali e compaiono solo in Tutti.

La riga in cima all’elenco permette anche di passare direttamente all’altra visualizzazione: in **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il riepilogo del mattino o della sera più recente e il numero di attività conteggiate, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Toccala per rileggere il riepilogo, con **Copia** per copiarlo e incollarlo dove vuoi. Dopo averlo aperto o aver toccato la **×**, il riepilogo resta disponibile su tutti i tuoi dispositivi fino al successivo.

Se non hai un riepilogo recente, compare **Oggi finora**: ciò che è stato completato oggi e ciò che è ancora aperto, per Lavoro e Personale oppure solo per il filtro attivo.

Sotto il titolo, un’attività di un progetto mostra il nome del progetto. Toccala per aprirlo. **Progetto** in **Dettagli** permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

**Area** in **Dettagli** sposta un’attività nell’altra area. Anche le fonti da cui può leggere e a cui può inviare contenuti si spostano con l’attività. **Annulla** nella nota la riporta dov’era.

Se un’attività ha bisogno dell’altra area per proseguire e tutti i messaggi da cui proviene si trovano lì, si sposta automaticamente e continua. Altrimenti compare **Sposta in Lavoro** e non viene spostato nulla finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta automaticamente non appena trova la sua area. Fino ad allora non è contrassegnata né come Lavoro né come Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se per proseguire ha bisogno di altri messaggi dell’altra area, compare **Usa questa email per questa attività**. Una casella di lavoro che hai contrassegnato come Personale viene considerata Personale. Le email destinate a un’altra delle tue aziende vanno nelle attività di quell’azienda. Un’attività che riguarda la tua vita privata, per esempio un familiare che scrive al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, per esempio un cliente su WhatsApp, un ordine nella tua casella personale o una [promessa](promises.md) di lavoro, è considerato Lavoro fin dall’inizio.

Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. L’impostazione Lavoro o Personale determina dove compare l’attività e con chi viene condivisa, ma non dove viene inviata la risposta: questa va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro canale.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro o nel Graph del team.

Se hai almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco e con ogni bozza completa. Puoi scegliere **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** o **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta e Esc interrompe. L’intestazione indica quanto tempo ci vorrà al tuo ritmo, per esempio «circa 2 min».

Alla fine viene indicato quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Le attività che ti fanno una domanda non vengono incluse: richiedono una risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa o quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, da 00:00 a 06:30, i controlli si fermano. I nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, sotto Controlli, compare «In pausa per la notte, recupero alle 06:30». Se di notte fai clic, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla, con **Dettagli**, che apre Controlli in Connessioni. Se hai attività aperte, sul computer trovi il comando in cima all’elenco. Una breve riga compare solo durante un controllo o quando un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, una riga sopra le attività indica cosa ha trovato tra tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». Riguarda solo quel controllo: le attività già presenti nell’elenco restano invariate. Se una nuova attività viene messa in attesa del momento giusto, per esempio del riepilogo del mattino, viene indicato fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica, con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività oppure il motivo per cui non serviva farne una, per esempio «Solo in copia, risponde una persona del team» o «Riunione già fissata per giovedì». Se il controllo ha restituito solo un motivo generico, la conversazione non mostra alcuna spiegazione. Tocca una voce per leggerla, insieme al contesto.

Vengono mostrate le prime 10 voci. Toccando sotto, puoi vedere le altre. Un numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Su Android, una notifica relativa a un messaggio già nell’elenco viene mostrata una volta sola. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email ricevute. Le tue risposte vengono lette per ricostruire il contesto e le promesse, ma non sono nuove email. Le email della tua Machine, come il riepilogo del mattino o una notifica di correzione, non vengono mai lette né elencate. Le email di fatturazione, di prova o di invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il passaggio successivo, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** permette di indicare cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. Se lasci il testo a metà, lo ritrovi quando torni. **Annulla** lo elimina.

**Segna come fatto** indica che l’attività è stata gestita. Sul computer compare accanto agli altri pulsanti, se c’è spazio su una riga. Sul telefono è visibile per un’attività pronta senza bozza o per una che ti fa una domanda; altrimenti si trova in cima al menu **…**. L’attività sparisce subito dall’elenco e nel messaggio compare **Annulla**. Per chiuderla più rapidamente, fai scorrere il messaggio o trascinalo fuori con il mouse. La modifica viene mantenuta.

Per farla completare in un altro modo, scrivilo nella **Chat** dell’attività. La risposta indica solo cosa è cambiato, per esempio il posticipo e fino a quando. Se non è stato possibile modificare qualcosa, come una data di scadenza, te lo dice.

Nel menu **…**:

- **Passa…**: assegnala a una persona del team, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di controllarla](ask-to-review.md).
- **Ripeti…**: l’attività [si ripresenta a intervalli regolari](recurring.md).
- **Non serve**: l’attività viene rimossa. Se vuoi, puoi indicare il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara dalla scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività. Puoi anche chiederlo nella chat, per esempio «Rinominala …». Il titolo che scegli resta invariato.

**Riapri** riporta nell’elenco un’attività chiusa. Si riapre automaticamente anche quando succede qualcosa di nuovo, per esempio se la persona ti scrive, ma non quando rispondi tu. L’attività indica quando è tornata e viene ordinata come nuova. La chat riprende da dove si era interrotta, anche dopo settimane.

Una bolletta che devi pagare tu, da qualsiasi Paese, diventa un’attività con l’importo, la scadenza e i dati di pagamento indicati nella bolletta. Le bollette pagate automaticamente, per esempio con addebito diretto o una carta salvata, non diventano attività. Se un’email successiva conferma il pagamento, per esempio perché il mittente dice che il pagamento è arrivato, l’attività si chiude automaticamente. **Annulla** la riapre per un giorno.

Un’attività che serve solo fino a un certo momento, per esempio una conferma prima di una riunione, si chiude automaticamente dopo quell’ora. Viene spostata in **Fatte / scartate** con la dicitura «Non serve più». **Annulla** la riapre per un giorno.

Prima che un messaggio o un passaggio di consegne per qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, comprese le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché qualcuno ha fatto una richiesta e ha ricevuto un sì, si chiude automaticamente. **Annulla** la riapre per un giorno.

Se qualcun altro scrive nella stessa conversazione dopo che la bozza è stata creata, **Invia** la mette in attesa: «Non inviata: nuovo messaggio nella conversazione». L’attività mostra il messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per inviare la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa viene spostata in un’altra location o una prenotazione viene annullata, The Machine aggiorna da sola le attività. Se è ancora necessaria, l’attività segue i nuovi piani. Se non c’è più nulla da fare, viene spostata in **Fatte / scartate** con la dicitura «Non serve», la chat indica «Aggiornamento:» e il motivo, e **Annulla** la riapre per un giorno.

Nelle prime attività compare un breve suggerimento con le azioni principali: **Chiedi modifiche** e **Non serve**, e con l’indicazione che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica a chi si riferisce, l’organizzazione se pertinente e non solo perché la persona ci lavora, il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se nel Graph sono disponibili, accanto al nome e all’organizzazione compaiono la foto o il logo; altrimenti vengono mostrate le iniziali. Se un logo non è leggibile in piccolo, per esempio perché è bianco su sfondo trasparente o è un wordmark largo, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto 12 giorni fa via email, nessuna novità da allora». Compare quando l’ultimo scambio con la persona è lontano nel tempo o senza risposta e indica anche i canali non collegati, per esempio WhatsApp. La tua Machine ti dice cosa non sa invece di tirare a indovinare.

Quando viene indicato un canale non collegato, tocca **Connetti** accanto per aprire quella connessione.

Il titolo indica cosa va fatto e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo e mostra sotto come si è conclusa, per esempio «Fatta: Sam l’ha firmato martedì».

Sopra la bozza, una riga in grigio indica il messaggio da cui proviene, con il logo del servizio. Toccala per leggere la conversazione. La bozza mostra il logo del servizio a cui è destinata, così capisci subito se si tratta di una risposta Slack o di un’email.

Se la bozza tiene conto del contributo di qualcuno in un’altra conversazione, per esempio un suggerimento di una persona del team su Slack, una riga lo indica, per esempio «Basata sul messaggio di Sam in #ops». Toccala per leggere il messaggio. La riga scompare quando la bozza viene sostituita da un aggiornamento.

Una chat (Slack, WhatsApp, Telegram, Intercom…) viene mostrata come un’unica conversazione, dalla più vecchia alla più recente: prima i messaggi precedenti a quello a cui si riferisce l’attività, poi le risposte. In WhatsApp, Telegram o Signal i tuoi messaggi compaiono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e viene aperto direttamente. **Mostra messaggi precedenti** aggiunge quelli più vecchi. In un’email, il resto della conversazione è ripiegato sopra e sotto il messaggio.

Un messaggio si apre nello stesso modo dalla ricerca, dal Graph, dalle risposte di Ask o dall’ultimo controllo, con l’indicazione «Questo messaggio» (o «Nuovi messaggi»).

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android, se hai installato l’app Gmail, l’email si apre lì.

In **Dettagli** di un’email trovi solo le informazioni che non compaiono nell’intestazione, come gli indirizzi completi in Cc, i destinatari in Ccn o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, la sezione non compare.

Una risposta in un thread Slack mostra anche i messaggi precedenti all’inizio del thread. Il link dell’attività al suo messaggio apre anche qui la conversazione, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area, che puoi toccare per modificarli, la tua ultima nota e il risultato di un agente di programmazione. Tocca il titolo per aprire la chat. Le attività completate restano compatte; il messaggio di origine si trova in **Dettagli**.

Un’attività «In attesa di» collega al tuo ultimo messaggio alla persona, quello a cui aspetti una risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, l’attività viene assegnata all’area corretta in base a chi riguarda e all’argomento. La Machine trova anche l’email a cui si riferisce, incluse quelle meno recenti.

Se chiudi il modulo prima di aggiungere l’attività, il testo e le scelte restano salvati per la prossima volta. I file no. **Scarta** nel messaggio li elimina.

- **Scadenza**: scrivi un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore», anche nella tua lingua. L’icona del calendario mostra alcune scelte rapide e **Scegli una data**.
- **Si ripete**: l’attività torna a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, per esempio un’email, un messaggio Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio presente nella tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, la fotocamera accanto scatta una foto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano nell’attività e la tua Machine li legge mentre ci lavora. Puoi creare un’attività anche solo con dei file: la Machine ricava i dettagli da un PDF o da un file di testo. Una foto appare come immagine in miniatura: toccala per vederla a grandezza naturale.
