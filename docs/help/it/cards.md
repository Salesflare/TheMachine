---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo ok. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 32c3a3e62b74548f
---
La tua Machine legge tutte le novità e crea un’attività solo quando serve il tuo intervento. Un’attività per ogni questione, anche se coinvolge molti messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in cima, un ultimo passaggio che hai confermato, come un modulo o una segnalazione, è andato a buon fine mentre non c’eri. Resta qui finché non tocchi **Ho capito**, al massimo per un giorno, e ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che è in attesa del tuo intervento, prima le cose in scadenza entro domani. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima serve una tua decisione o una risposta; se il lavoro non può proseguire o essere usato senza qualcosa che solo tu puoi fornire, come un prezzo, un dato o una scelta, una riga sotto il titolo spiega cosa serve), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un breve testo, senza decisioni da prendere).
- **Più vecchie**: attività raccolte in un gruppo chiuso, senza novità da una settimana (vedi sotto).
- **In attesa di altri**: attività raccolte in un gruppo chiuso, in cui il prossimo passo spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: ciò che hai promesso e ciò che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, come «Fatto 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviato. Spostata in Fatto.» oppure «Inviato. Spostata in Più tardi fino a lunedì». Se la risposta si limita a promettere che il lavoro verrà fatto, come «Te lo invio entro martedì», l’attività resta aperta: «Inviato. Lasciata aperta.» **Apri** ti porta all’attività. La ricerca trova un’attività dal titolo o dal destinatario, anche in Più tardi e Fatto.

**Per te** mette prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, i promemoria di una bacheca e infine tutto il resto. All’interno di ogni gruppo, le più recenti vengono prima. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e quando è completata: cambia solo il contrassegno. Negli altri gruppi aperti, prima vengono le attività scadute o in scadenza entro domani, poi le altre dalla più recente. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che l’attività è completata, come «PR #3451 unito», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e la tua Machine impara da questa scelta. Queste attività non risultano mai in ritardo. Quando il messaggio indica che è completata, si chiude da sola dopo un giorno, con **Annulla**. Altrimenti resta in attesa di **Segna come fatto**.

Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola. Se una risposta dice che c’è un file allegato ma non è così, l’attività non si chiude.

Se un messaggio arriva da un indirizzo che somiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Questo non è Sam Lee». La persona viene mostrata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona dell’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica il passaggio con **In attesa di:**. Rimane in **In attesa di altri**, nel gruppo chiuso sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso succede dopo che hai risposto con una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è più tardi nello stesso giorno oppure la mattina successiva se la scadenza è passata. Indica anche chi deve ancora rispondere.

Se un’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, **Dettagli** lo mostra in **Fatto quando**. Inviare la tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola, con **Annulla**. Se non arriva nulla entro il momento in cui è ora di sollecitare, l’attività riappare con **Scrivi un breve sollecito** nella chat. Per modificare cosa conta come completamento, scrivilo nella chat.

Se per una settimana non arrivano novità su un’attività, questa passa da Per te a **Più vecchie**, così dopo qualche giorno di assenza trovi prima quelle nuove. Per novità si intende un nuovo messaggio sull’attività o un’azione che hai fatto, come un messaggio in chat, una modifica o un posticipo. Aprire l’attività non conta.

Le attività urgenti, quelle in scadenza a breve e quelle con un invio in corso restano in Per te. **Scarta tutto** contrassegna tutte le attività in Più vecchie come non necessarie con una sola conferma, proprio come fa **Non serve** per una singola attività, con **Annulla**. Se arriva una novità, l’attività torna in Per te.

Se nessuno interviene su un’attività per una settimana, viene chiesto una volta: **Serve ancora?** **Non serve** la chiude, con **Annulla**. **Tieni** la mantiene e la domanda non viene più ripetuta. Se non rispondi per un’altra settimana, l’attività passa nel gruppo chiuso Torna più tardi e non viene più conteggiata sul numero dell’icona dell’app né nel riepilogo del mattino. Aprirla, inviare un messaggio in chat, modificarla, posticiparla o ricevere un nuovo messaggio la fa tornare nell’elenco.

Una volta a settimana, un progetto che non ha avuto novità e non ha attività aperte può ricevere un’attività con un prossimo passo specifico, per un massimo di tre a settimana. Vedi [Progetti](projects.md).

Quando nulla richiede il tuo intervento, la tua Machine riposa e l’elenco resta vuoto. Durante un controllo si riattiva e te lo comunica. Se un controllo non è riuscito o è in ritardo, la riga lo indica e mostra **Controlla ora**.

Le opzioni **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. La scelta è la stessa sul telefono e sul computer. Quando è attiva la vista Lavoro o Personale, **Mostra tutto** riporta alla visualizzazione completa. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima all’elenco permette anche di passare direttamente all’altra vista: in **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il nome dell’ultimo riepilogo del mattino o della sera e cosa include, per esempio **Riepilogo di ieri sera** · 12 completate, 3 aperte. Toccalo per rileggere il riepilogo e usare **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, resta disponibile su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non hai un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per la vista selezionata.

Un’attività collegata a un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. **Progetto** in **Dettagli** permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

**Area** in **Dettagli** sposta un’attività nell’altra area. Con essa si sposta anche ciò che può leggere e inviare. **Annulla** nella nota la riporta dov’era.

Se un’attività deve passare all’altra area per poter proseguire e tutti i messaggi da cui proviene si trovano lì, si sposta da sola e continua. Altrimenti mostra **Sposta in Lavoro** e non viene spostata finché non la tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola quando trova l’area giusta. Fino ad allora non è contrassegnata né come Lavoro né come Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, chiede il permesso con **Usa questa email per questa attività**. Una casella di lavoro che hai contrassegnato come Personale viene considerata Personale. Le email relative a un’altra delle tue aziende vanno nelle attività di quell’azienda. Un’attività sulla tua vita personale, come un messaggio di famiglia al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp, un ordine nella tua casella personale o una [promessa](promises.md) di lavoro, è Lavoro fin dall’inizio.

Un’attività che hai spostato o collocato tu resta sempre dove l’hai messa. Lavoro o Personale decide dove compare un’attività e con chi viene condivisa, non dove risponde: la risposta va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro o nel Graph del team.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza per intero e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che vedi sullo schermo, `S` posticipa, `→` salta e Esc interrompe. Nell’intestazione trovi anche la durata stimata al tuo ritmo, per esempio «circa 2 min».

Alla fine viene indicato quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Le attività che ti fanno una domanda non vengono incluse: richiedono una risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa oppure quando il messaggio più vecchio di una persona è rimasto in attesa per 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si interrompono: i nuovi messaggi vengono comunque letti e conservati, poi controllati insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Controlli, sotto Connessioni, compare «In pausa per la notte, recupero alle 06:30». Se di notte fai clic, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre un controllo immediato.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per vederla, con **Dettagli**, che apre Controlli in Connessioni. Se hai attività aperte, sul computer l’opzione è in cima. La riga breve compare solo durante un controllo o quando un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, una riga sopra le attività indica cosa ha trovato in tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». La riga riguarda solo quel controllo: le attività già nell’elenco restano in attesa come prima. Se una nuova attività viene messa da parte per un momento più adatto, per esempio il riepilogo del mattino, viene indicato fino a quando: «1 attività messa da parte fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica con l’icona del servizio di origine: chi ha scritto, l’oggetto o le prime parole e la nuova attività oppure il motivo per cui non serviva fare nulla, per esempio «Solo in copia, risponde un collega» oppure «Riunione già fissata per giovedì». Una conversazione non mostra il motivo se il controllo ha restituito solo una spiegazione vaga. Tocca un elemento per leggerlo insieme ai messaggi che lo circondano.

Vengono mostrati i primi 10 elementi; toccando sotto, vedi il resto. Un numero dopo un nome, come (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono per un messaggio già nell’elenco compare una sola volta. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email ricevute. Le tue risposte vengono lette per avere il contesto e rilevare le promesse, ma non sono nuove email. Le email inviate dalla tua Machine, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né mostrate. Le email su fatturazione, prova o inviti vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passaggio, come **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** ti permette di indicare cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. **Segna come fatto** indica che l’attività è stata gestita: è visibile su un’attività pronta senza bozza o che ti pone una domanda; negli altri casi si trova in cima a **…**. L’attività viene subito rimossa dall’elenco e il messaggio mostra **Annulla**. Scorri il messaggio per eliminarlo oppure trascinalo fuori con il mouse per chiuderlo prima. La modifica resta.

Per completare l’attività in un altro modo, scrivilo nella sua **Chat**. La risposta indica solo cosa è cambiato, per esempio il posticipo e fino a quando. Se non è stato possibile cambiare qualcosa, come una scadenza, te lo dice.

In **…**:

- **Passa…**: assegnala a un collega, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: l’attività [si ripresenta con una certa frequenza](recurring.md).
- **Non serve**: rimuove l’attività. Se vuoi, scegli il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara dalla scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività, oppure chiedilo nella chat, per esempio «Rinominala in …». Il titolo che scegli resta.

**Riapri** riporta nell’elenco un’attività chiusa. L’attività può anche riapparire da sola quando succede qualcosa di nuovo, per esempio quando ricevi un nuovo messaggio da quella persona, ma non dopo una tua risposta. In quel caso mostra quando è ricomparsa e viene ordinata come nuova. La chat continua da dove era stata interrotta, anche dopo settimane.

Una fattura che devi pagare tu, da qualunque Paese, diventa un’attività con l’importo, la scadenza e i dettagli di pagamento indicati nella fattura. Non succede per le fatture pagate automaticamente, per esempio con un addebito diretto o una carta registrata. Quando un’email successiva conferma il pagamento, per esempio un messaggio del mittente che conferma la ricezione, l’attività si chiude da sola. **Annulla** la ripristina per un giorno.

Un’attività che serve solo fino a un certo momento, come una conferma prima di una riunione, si chiude da sola dopo quell’ora. Passa in **Fatte / scartate** con la dicitura «Non serve più». **Annulla** la ripristina per un giorno.

Prima di mostrare come pronta una bozza di messaggio o un passaggio di consegne, la tua Machine controlla le chat recenti con le persone coinvolte, incluse le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché è stata fatta una richiesta e la risposta è stata affermativa, l’attività si chiude da sola. **Annulla** la ripristina per un giorno.

Se qualcun altro scrive nella stessa conversazione dopo la creazione della bozza, **Invia** la blocca e mostra: «Non inviata: nuovo messaggio nella conversazione». L’attività mostra il messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per inviare la bozza così com’è.

Se un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna le attività autonomamente. Se un’attività è ancora utile, segue i nuovi piani. Se non resta nulla da fare, passa in **Fatte / scartate** con la dicitura «Non serve»; la chat spiega il motivo con «Aggiornamento:» e **Annulla** la ripristina per un giorno.

Tra le prime attività compare un breve suggerimento con le azioni principali: **Chiedi modifiche** e **Non serve**, e con l’indicazione che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La bozza di quella risposta viene preparata per prima, così è pronta al tuo arrivo.

Ogni attività inizia con il titolo. La riga sotto indica a chi si riferisce, l’organizzazione se pertinente (non solo perché una persona ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se nel Graph sono disponibili, il nome e l’organizzazione mostrano una foto o un logo; altrimenti, le iniziali. Se un logo non è leggibile in dimensioni ridotte, per esempio perché è bianco su sfondo trasparente o è un marchio molto largo, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non è noto, per esempio «Ultimo contatto 12 giorni fa via email; nessun aggiornamento da allora». Compare quando l’ultimo contatto è datato o senza risposta e indica i canali non collegati, come WhatsApp. La tua Machine specifica ciò che non sa invece di indovinare.

Se viene indicato un canale non collegato, tocca Connetti accanto al nome per aprire quella connessione.

Il titolo spiega cosa va fatto e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo e indica sotto come si è conclusa, per esempio «Fatto: Sam l’ha firmato martedì».

Sopra la bozza, una riga discreta indica il messaggio da cui proviene e mostra il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo del servizio a cui verrà inviata, così vedi subito se è una risposta su Slack o un’email.

Se la bozza si basa sul contributo di qualcuno in un altro luogo, come un suggerimento di un collega su Slack, una riga lo indica, per esempio «Basata sul messaggio di Sam in #ops». Tocca la riga per leggere il messaggio. La riga scompare quando un aggiornamento sostituisce la bozza.

Una chat (Slack, WhatsApp, Telegram, Intercom…) viene mostrata come un’unica conversazione, dalla più vecchia alla più recente: prima i messaggi precedenti a quello a cui si riferisce l’attività, poi le risposte. In WhatsApp, Telegram o Signal i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e si apre nella conversazione. **Mostra messaggi precedenti** aggiunge quelli più vecchi. Le email mostrano il resto della conversazione raccolto sopra e sotto il messaggio.

Un messaggio si apre allo stesso modo dalla ricerca, dal Graph, dalle risposte di Ask o dall’ultimo controllo, contrassegnato con «Questo messaggio» oppure «Nuovi messaggi».

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android, se hai l’app Gmail, l’email si apre lì.

In **Dettagli** di un’email trovi solo le informazioni non visibili nell’intestazione, come gli indirizzi completi in Cc, il campo Ccn o un indirizzo di risposta diverso. Se non c’è altro da mostrare, la sezione non compare.

Una risposta in un thread Slack mostra anche i messaggi precedenti all’inizio del thread. Il link al messaggio dell’attività apre anche la conversazione qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area (tocca uno di questi elementi per modificarlo), la tua ultima nota e il risultato di un agente di programmazione. Tocca il titolo per aprire la chat. Un’attività completata resta compatta; il messaggio da cui proviene è in **Dettagli**.

Un’attività «In attesa di» include un link all’ultimo messaggio che hai inviato alla persona, quello a cui aspetti una risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono oppure `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, l’attività viene collocata dove è più adatta, in base a chi e a cosa riguarda. La tua Machine trova anche l’email a cui si riferisce, comprese quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore». Puoi scriverlo anche nella tua lingua. L’icona del calendario include alcune opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività si ripresenta con una certa frequenza. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, che sia un’email, un messaggio Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile sulla tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file sul modulo. Sul telefono, la fotocamera accanto scatta una foto. Puoi aggiungere fino a 5 file, come in chat (vedi [Aggiungere file](card-chat.md#add-files)). Con × rimuovi un file.

I file restano associati all’attività e la tua Machine li legge mentre ci lavora. Puoi aggiungere anche solo dei file: l’attività viene compilata a partire da un PDF o da un file di testo. Una foto viene mostrata come miniatura: toccala per vederla a grandezza naturale.
