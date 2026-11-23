---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per essere approvata. Scopri cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e0fd02e557e6daee
---
La tua Machine legge tutte le novità e crea un’attività solo quando serve il tuo intervento. Una per ogni questione, anche se coinvolge più messaggi.

## Dove si trovano le attività

La pagina **Attività** le organizza così:

- **Appena fatto**: in cima, trovi l’ultimo passaggio che hai confermato, come un modulo o una segnalazione, completato mentre non c’eri. Resta lì finché non tocchi **Ho capito**, per un giorno al massimo. Ricevi una notifica anche sul telefono.
- **Per te**: tutto quello che aspetta un tuo intervento, in ordine di urgenza. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e puoi completare l’azione con **Fallo** o **Invia**), **Serve il tuo intervento** (prima serve una tua decisione o risposta; se il lavoro si è fermato perché manca qualcosa che solo tu puoi fornire, come un’informazione, l’accesso o una scelta, una riga sotto il titolo ti spiega cosa manca), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un breve resoconto, senza decisioni da prendere).
- **Più vecchie**: attività chiuse in un gruppo, senza novità da una settimana (vedi sotto).
- **In attesa di altri**: attività chiuse in un gruppo, il cui prossimo passaggio spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: quello che hai promesso e quello che ti hanno promesso. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatto 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota ti dice dove è finita l’attività, per esempio «Inviato. Spostato in Fatte / scartate» oppure «Inviato. Spostato in Torna più tardi fino a lunedì». Se la risposta promette solo di svolgere il lavoro, per esempio «Lo invierò entro martedì», l’attività resta aperta: «Inviato. Lasciato aperto». **Apri** ti porta all’attività. Cerca un’attività per titolo o per destinatario, anche in Torna più tardi e Fatte / scartate.

In **Per te** trovi prima le attività scadute o in scadenza entro domani, poi le domande della tua Fleet, i promemoria di una bacheca e infine tutto il resto. All’interno di ogni gruppo, le più recenti vengono prima. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e quando è completata: cambia solo il contrassegno. Negli altri gruppi aperti, vengono prima le attività scadute o in scadenza entro domani, poi le più recenti. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine rileva che l’attività è completata, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e aiuta la tua Machine a imparare. Queste attività non risultano mai in ritardo. Se compare in un messaggio, si chiude da sola dopo un giorno, con **Annulla**. Altrimenti resta in attesa che tu scelga **Segna come fatto**. Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola.

Se un messaggio arriva da un indirizzo che somiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività te lo dice chiaramente: «Non è Sam Lee». La persona è indicata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, non con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica **In attesa di:** seguito dal passaggio. La trovi in **In attesa di altri**, in un gruppo chiuso sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso vale dopo che hai fatto una domanda: l’attività ricompare la mattina prima della scadenza, alla scadenza se cade più tardi oggi, oppure la mattina successiva se la scadenza è passata. Indica anche chi deve ancora rispondere.

Quando un’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, **Dettagli** indica il risultato in **Fatto quando**. L’invio della tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola, con **Annulla**. Se non arriva nulla entro il momento in cui è il caso di sollecitare, l’attività ricompare con **Scrivi un breve sollecito** nella chat. Per cambiare cosa significa che è completata, scrivilo nella chat.

Un’attività senza novità da una settimana passa da Per te a **Più vecchie**, così quando torni dopo qualche giorno trovi prima quelle nuove. Non ci sono novità se non è arrivato un nuovo messaggio e non hai fatto nulla, come scrivere in chat, modificare o posticipare l’attività. Aprirla non conta.

Le attività urgenti, in scadenza a breve o con un invio in corso restano in Per te. **Scarta tutto** contrassegna tutte le attività in Più vecchie come non necessarie dopo una sola conferma, come fa **Non serve** con una alla volta, con **Annulla**. Se arriva una novità, l’attività torna in Per te.

Se nessuno interviene su un’attività per una settimana, compare una volta la domanda **Serve ancora?**. **Non serve** la chiude, con **Annulla**. **Tieni** la mantiene e non te lo chiederà più. Se non rispondi per un’altra settimana, l’attività passa al gruppo chiuso Torna più tardi e non viene più conteggiata sul badge dell’app né nel riepilogo del mattino. Se la apri, scrivi in chat, la modifichi, la posticipi o arriva un nuovo messaggio, ricompare.

Una volta a settimana, un progetto che non ha novità e non ha attività aperte può ricevere un’attività con un prossimo passaggio specifico, fino a un massimo di tre a settimana. Vedi [Progetti](projects.md).

Quando non c’è nulla che richiede il tuo intervento, la tua Machine riposa e l’elenco resta vuoto. Durante un controllo, si riattiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, la relativa riga te lo indica e mostra **Controlla ora**.

Le opzioni **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer trovi la stessa selezione. Se hai selezionato Lavoro o Personale, **Mostra tutto** torna all’elenco completo. Un avviso relativo alla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima all’elenco ti permette anche di passare direttamente all’altra vista: in **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il tuo ultimo riepilogo del mattino o della sera e cosa includeva, per esempio **Riepilogo di ieri sera** · 12 completate, 3 aperte. Tocca la riga per rileggere il riepilogo e usa **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la **×**, il riepilogo resta su tutti i tuoi dispositivi fino al successivo.

Se non hai un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per la vista selezionata.

Un’attività di un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. Con **Progetto** in **Dettagli** puoi cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

Con **Area** in **Dettagli** puoi spostare un’attività nell’altra area. L’accesso ai messaggi da leggere e a cui rispondere si sposta insieme all’attività. **Annulla** nella nota la riporta indietro.

Se un’attività ha bisogno dell’altra area per proseguire e tutti i messaggi a cui si riferisce si trovano lì, viene spostata automaticamente e il lavoro continua. Altrimenti compare **Sposta in Lavoro** e non viene spostato nulla finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale viene spostata automaticamente quando la tua Machine capisce a quale area appartiene. Fino ad allora non indica né Lavoro né Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, ti chiede il permesso con **Usa questa email per questa attività**. Un indirizzo di lavoro che hai etichettato come Personale viene considerato personale. Le email destinate a un’altra delle tue aziende finiscono nelle attività di quell’azienda. Un’attività che riguarda la tua vita privata, per esempio un messaggio di famiglia arrivato al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, per esempio un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre nell’area che hai scelto. Lavoro o Personale determina dove compare l’attività e con chi viene condivisa, mai dove risponde: la risposta va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in una Fleet di lavoro o nel Graph del team.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le esamina una alla volta, nell’ordine dell’elenco. Mostra ogni bozza per intero, con **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. L’intestazione indica quanto tempo serve al tuo ritmo, per esempio «circa 2 min».

Alla fine, indica quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Un’attività che ti fa una domanda non viene inclusa in nessuno dei due gruppi: richiede una tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ne sono arrivati 40 o quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si fermano. I nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, i controlli indicano «In pausa per la notte, recupero alle 06:30». Se di notte clicchi, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono come al solito finché non resti inattivo per un’ora. **Controlla ora** avvia sempre un controllo immediato.

**Controlla ora** legge subito tutte le fonti. Se non ci sono attività aperte, tocca la riga della tua Machine per visualizzarla, con **Dettagli** che apre Controlli in Connessioni. Se ci sono attività aperte, il comando si trova in cima, sul computer. Una breve riga viene mostrata solo mentre è in corso un controllo oppure se un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i loro tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, una riga sopra le attività indica cosa ha trovato, tra tutte le fonti controllate. Per esempio: «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». La riga si riferisce solo a quel controllo: le attività già presenti nell’elenco restano invariate. Se una nuova attività viene tenuta da parte per un momento più adatto, per esempio il riepilogo del mattino, la riga indica fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni email, chat e notifica con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività oppure il motivo per cui non serviva crearne una, per esempio «Solo in copia, risponde un collega» o «Riunione già fissata per giovedì». Se il controllo indica un motivo generico, la conversazione non mostra alcuna spiegazione. Tocca una voce per leggerla e vedere cosa è stato detto nel contesto.

Vengono mostrate le prime 10 voci. Toccando sotto, puoi vedere le altre. Un numero dopo un nome, come (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già nell’elenco compare una sola volta. La riga resta visibile per 12 ore dal controllo.

Vengono conteggiate solo le email che hai ricevuto. Le tue risposte vengono lette per il contesto e per individuare le promesse, ma non sono considerate nuove email. Le email inviate dalla tua Machine, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email relative alla fatturazione, alla prova o a un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passaggio, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. **Segna come fatto** indica che l’attività è stata gestita: compare subito su un’attività pronta senza bozza o su una che ti fa una domanda, altrimenti si trova in cima a **…**. L’attività sparisce subito dall’elenco e nel messaggio compare **Annulla**. Scorri il messaggio per chiuderlo o trascinalo fuori con il mouse. La modifica resta.

Per far svolgere l’attività in un altro modo, scrivilo nella sua **Chat**. La risposta indica solo cosa è cambiato, per esempio il posticipo e fino a quando. Se non è stato possibile cambiare qualcosa, come la scadenza, te lo dice.

In **…**:

- **Passa…**: assegna l’attività a un collega, a [Claude Code o Codex](hand-to-agent.md) oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: l’attività [torna a intervalli regolari](recurring.md).
- **Non serve**: l’attività scompare. Se vuoi, puoi scegliere il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara da questa scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività, oppure chiedilo nella chat, per esempio «Rinominala in …». Il titolo scelto resta.

**Riapri** riporta nell’elenco un’attività chiusa. L’attività può anche ricomparire da sola quando succede qualcosa di nuovo, per esempio se la persona ti scrive, ma non dopo una tua risposta. In quel caso indica quando è ricomparsa e viene ordinata come nuova. La chat riprende da dove si era interrotta, anche dopo settimane.

Una fattura che devi pagare tu, da qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dati di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta salvata, non diventano attività. Quando un’email successiva conferma il pagamento, per esempio con una conferma di ricezione, l’attività si chiude da sola. **Annulla** la ripristina per un giorno.

Un’attività che serve solo fino a un momento preciso, come una conferma prima di una riunione, si chiude da sola allo scadere. Passa in **Fatte / scartate** con l’indicazione «Non serve più». **Annulla** la ripristina per un giorno.

Prima che un messaggio o un passaggio di consegne per qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, comprese le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che l’attività è già completata, per esempio perché la persona è stata interpellata e ha accettato, l’attività si chiude da sola. **Annulla** la ripristina per un giorno.

Se qualcun altro scrive nella stessa conversazione dopo che la bozza è stata creata, **Invia** la mette in attesa: «Non inviato: nuovo messaggio nella conversazione». L’attività mostra quel messaggio con **Leggila** e **Rifai per questo messaggio**. Tocca di nuovo **Invia** per inviare la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, la tua Machine aggiorna le attività da sola. Se è ancora necessaria, l’attività segue il nuovo piano. Se non c’è più nulla da fare, passa in **Fatte / scartate** con l’indicazione «Non serve». Nella chat compare «Aggiornamento:» con il motivo e **Annulla** la ripristina per un giorno.

Alla prima visita delle attività, un breve suggerimento mostra le azioni principali: **Chiedi modifiche** e **Non serve**. Ti ricorda anche che nulla viene inviato finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il relativo pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La risposta viene preparata per prima, così è pronta al tuo arrivo.

Ogni attività inizia con il titolo. La riga sotto indica chi è coinvolto, l’organizzazione se pertinente (non solo perché qualcuno ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se nel Graph è disponibile una foto o un logo, viene mostrato accanto al nome o all’organizzazione. Altrimenti compaiono le iniziali. Se un logo è illeggibile in piccolo, per esempio perché è bianco su uno sfondo trasparente o è una scritta larga, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessuna novità». Compare quando l’ultimo scambio è vecchio o senza risposta e indica i canali non collegati, come WhatsApp. La tua Machine dice cosa non sa invece di tirare a indovinare.

Se viene indicato un canale non collegato, tocca **Connetti** accanto al nome per aprire la relativa connessione.

Il titolo indica cosa bisogna fare e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo, con una nota sotto che spiega come si è conclusa, per esempio «Fatto: Sam l’ha firmato martedì».

Sopra la bozza, una riga in grigio tenue indica il messaggio da cui proviene, con il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo del servizio a cui è destinata, così capisci subito se è una risposta su Slack o un’email.

Se la bozza tiene conto di un contributo ricevuto altrove, per esempio un suggerimento di un collega su Slack, una riga lo indica, per esempio «Basato sul messaggio di Sam in #ops». Tocca la riga per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) viene mostrata come un’unica conversazione, dalla più vecchia alla più recente: prima i messaggi precedenti a quello a cui si riferisce l’attività, poi le risposte. In WhatsApp, Telegram o Signal i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e viene aperto in primo piano. **Mostra messaggi precedenti** aggiunge i messaggi più vecchi. In un’email, il resto della conversazione è raccolto in sezioni chiuse sopra e sotto il messaggio.

Un messaggio si apre nello stesso modo dalla ricerca, dal Graph, dalle risposte di Ask o dall’ultimo controllo, con l’indicazione «Questo messaggio» (o «Nuovi messaggi»).

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android, se hai l’app Gmail, la apre direttamente.

I **Dettagli** di un’email mostrano solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, Bcc o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, non vengono mostrati.

Una risposta in un thread di Slack mostra anche cosa è stato detto prima dell’inizio del thread. Il link al messaggio di origine dell’attività lo apre qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto, l’area (tocca una voce per modificarla), la tua ultima nota e il risultato di un agente di programmazione. Tocca il titolo per aprire la chat. Le attività completate restano compatte; il messaggio di origine si trova in **Dettagli**.

Un’attività «In attesa di» collega l’ultimo messaggio che hai inviato alla persona e la risposta che aspetti, per esempio «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, viene assegnata all’area giusta in base a chi e a cosa riguarda. La tua Machine trova anche l’email a cui si riferisce, comprese quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14:00» o «tra 2 ore», anche nella tua lingua. L’icona del calendario mostra le scelte rapide e **Scegli una data**.
- **Si ripete**: l’attività torna a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende interessate, fino a 5.
- Icona del messaggio: allega il messaggio a cui si riferisce l’attività, un’email, un messaggio di Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato mostra la fonte, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, la fotocamera accanto alla graffetta scatta una foto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungere file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano con l’attività e la tua Machine li legge mentre ci lavora. Puoi allegare solo i file: la tua Machine crea l’attività partendo da un PDF o da un file di testo. Una foto viene mostrata come immagine in miniatura. Tocca l’immagine per vederla a grandezza naturale.
