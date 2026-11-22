---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via. Scopri cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fef065570d3fd972
---
La tua Machine legge tutto ciò che arriva e crea un’attività solo quando serve il tuo intervento. Una sola attività per ogni questione, anche se riguarda molti messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa così:

- **Appena fatto**: in alto, trovi l’ultimo passaggio che hai confermato, come l’invio di un modulo o la risoluzione di un problema, completato mentre non c’eri. Rimane qui finché non tocchi **Ho capito**, per un massimo di un giorno. La notifica arriva anche sul tuo telefono.
- **Per te**: tutto ciò che aspetta il tuo intervento, in ordine di urgenza. Ogni attività mostra **Preparata** (una bozza o un risultato è pronto e **Fallo** o **Invia** lo mette in atto), **Serve il tuo intervento** (prima serve una tua decisione o risposta; quando il lavoro si è fermato perché manca qualcosa che solo tu puoi dare, come un’informazione, l’accesso o una scelta, una riga sotto il titolo spiega cosa serve), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un breve aggiornamento, senza decisioni da prendere).
- **Più vecchie**: attività chiuse in un gruppo, senza novità da una settimana (vedi sotto).
- **In attesa di altri**: attività chiuse in un gruppo, in cui il prossimo passo spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e quelle senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: le promesse che hai fatto e quelle che gli altri hanno fatto a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatta 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviata. Spostata in Fatto» o «Inviata. Spostata in Più tardi fino a lunedì». Una risposta che si limita a promettere di fare il lavoro, per esempio «Te lo mando entro martedì», lascia aperta l’attività: «Inviata. Lasciata aperta». **Apri** ti porta all’attività. La ricerca trova un’attività per titolo o per destinatario, anche in Più tardi e Fatto.

In **Per te** vengono prima le attività scadute o in scadenza entro domani, poi le domande della tua Fleet, quindi i promemoria di una bacheca e infine le altre. All’interno di ogni gruppo, le più recenti vengono prima. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e quando è completata: cambia solo il suo contrassegno. Negli altri gruppi aperti, vengono prima le attività scadute o in scadenza entro domani, poi le più recenti. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che l’attività è stata completata, per esempio «PR #3451 unito», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e la tua Machine impara da questa scelta. Queste attività non risultano mai in ritardo. Se un messaggio ne segnala il completamento, si chiude automaticamente dopo un giorno, con **Annulla**. Altrimenti resta in attesa che tu scelga **Segna come completata**. Anche un’attività che hai già gestito da solo, per esempio rispondendo in Gmail o Slack, si chiude automaticamente.

Se un messaggio arriva da un indirizzo che somiglia soltanto a quello di qualcuno che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Non è Sam Lee». La persona viene mostrata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, mostra il passaggio in **In attesa di:**. Si trova in **In attesa di altri**, in un gruppo chiuso sopra Torna più tardi, finché un nuovo messaggio non la riporta tra le attività aperte. Lo stesso vale dopo che hai fatto una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è più tardi nella stessa giornata oppure la mattina successiva se la scadenza è già passata. Indica anche chi deve ancora rispondere.

Quando un’attività riguarda un risultato che deve fornire qualcun altro, per esempio un contratto firmato, in **Dettagli** lo trovi sotto **Fatto quando**. L’invio della tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude automaticamente, con **Annulla**. Se non arriva nulla entro il momento in cui è il caso di sollecitare, l’attività torna con **Scrivi un breve sollecito** nella chat. Per cambiare cosa conta come completamento, spiegalo nella chat.

Un’attività senza novità da una settimana passa da Per te a **Più vecchie**, così dopo qualche giorno di assenza le attività recenti vengono prima. Per novità si intende un nuovo messaggio sull’attività o qualcosa che hai fatto, per esempio un messaggio in chat, una modifica o un posticipo. Aprire l’attività non conta.

Le attività urgenti, in scadenza a breve o con un invio in corso restano in Per te. **Scarta tutto** contrassegna con **Non serve** tutte le attività in Più vecchie dopo una sola conferma, come fa **Non serve** per una singola attività, con **Annulla**. Se arriva una novità, l’attività torna in Per te.

Un’attività che nessuno ha toccato per una settimana chiede una volta: **Serve ancora?** **Non serve** la chiude, con **Annulla**. **Tieni** la mantiene aperta e non lo chiederà più. Se non rispondi per un’altra settimana, passa al gruppo Torna più tardi e non viene più conteggiata sul badge dell’app e nel riepilogo del mattino. Se la apri, scrivi in chat, la modifichi, la posticipi o arriva un nuovo messaggio, torna tra le attività aperte.

Una volta alla settimana, un progetto che non ha novità e non contiene attività aperte può ricevere un’attività con un prossimo passo preciso, al massimo tre volte a settimana. Vedi [Progetti](projects.md).

Quando niente richiede il tuo intervento, la tua Machine riposa e l’elenco è vuoto. Mentre controlla, si riattiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, la riga lo indica e mostra **Controlla ora**.

Le voci **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo un tipo. Sul telefono e sul computer trovi la stessa selezione. Quando è selezionato Lavoro o Personale, **Mostra tutto** riporta alla vista completa. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e appare solo sotto Tutti.

La riga in cima all’elenco passa direttamente anche all’altra vista: sotto **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il nome dell’ultimo riepilogo del mattino o della sera e cosa ha conteggiato, per esempio **Riepilogo di ieri sera** · 12 completate, 3 aperte. Toccalo per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la **×**, resta disponibile su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non ci sono riepiloghi recenti, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per la categoria selezionata.

Un’attività relativa a un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. **Progetto** sotto **Dettagli** permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

**Area** sotto **Dettagli** sposta un’attività nell’altra area. Anche l’accesso ai messaggi da cui può leggere e a cui può rispondere si sposta con essa. **Annulla** nella nota la riporta dov’era.

Se un’attività ha bisogno dell’altra area per proseguire e tutti i messaggi da cui proviene si trovano lì, si sposta e continua automaticamente. Altrimenti mostra **Sposta in Lavoro** e non si sposta finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola quando trova la categoria giusta. Fino ad allora non appartiene né a Lavoro né a Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, ti chiede il permesso con **Usa questa email per questa attività**. Una casella di lavoro che hai etichettato come Personale viene considerata personale. Le email per un’altra delle tue aziende finiscono nelle attività di quell’azienda. Un’attività che riguarda la tua vita privata, per esempio un messaggio di famiglia arrivato al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, per esempio un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre dov’è. Lavoro o Personale determina dove appare un’attività e con chi viene condivisa, mai dove risponde: la risposta va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non appare mai in una Fleet di lavoro o nel Graph del team.

Se hai almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza per intero e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. L’intestazione indica quanto tempo ci vuole al tuo ritmo, per esempio «circa 2 min».

Alla fine, mostra quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Un’attività che ti fa una domanda viene esclusa da entrambe le opzioni: serve la tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ne sono in attesa 40 o quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, da 00:00 a 06:30, i controlli si interrompono: i nuovi messaggi vengono comunque letti e conservati, poi controllati insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Controlli, sotto Connessioni, compare «In pausa per la notte, recupero alle 06:30». Se di notte fai clic, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge immediatamente tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla, con **Dettagli**, che apre Controlli sotto Connessioni. Se hai attività aperte, la trovi in cima, sul computer. La riga breve appare solo mentre è in corso un controllo, oppure se uno non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga che indica cosa ha trovato tra tutte le fonti controllate, per esempio «Controllati 13 messaggi alle 16:11 · niente richiede il tuo intervento» oppure «· 2 nuove attività». Se una nuova attività viene tenuta in attesa di un momento più adatto, per esempio il riepilogo del mattino, la riga indica fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività o il motivo per cui non era necessario fare nulla, per esempio «In copia, risponde un collega» o «Riunione già fissata per giovedì». Se il controllo ha dato un motivo poco chiaro, la conversazione non ne mostra uno. Toccane una per leggerla.

Vengono mostrate le prime 10. Tocca sotto per vedere le altre. Un numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già nell’elenco appare una volta sola. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email che hai ricevuto. Le tue risposte vengono lette per il contesto e per le promesse, ma non sono considerate nuove email. Le email che la tua Machine invia a te, come il riepilogo del mattino o una notifica di correzione, non vengono mai lette né elencate. Le email relative alla fatturazione, alla versione di prova o a un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passo, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando è pronta una bozza, cosa modificare al suo interno. **Segna come completata** indica che l’attività è stata gestita: è visibile su un’attività pronta senza bozza, altrimenti si trova in **…**, anche se richiede una tua decisione. L’attività lascia subito l’elenco e nel messaggio compare **Annulla**. Per chiuderla prima, scorri il messaggio fuori dallo schermo o trascinalo via con il mouse. La modifica resta.

Per farla in un altro modo, scrivilo nella **Chat**. La risposta indica solo cosa è cambiato, per esempio se è stata posticipata e fino a quando. Se non è stato possibile modificare qualcosa, per esempio la scadenza, te lo dice.

Sotto **…**:

- **Passa…**: assegna l’attività a un collega, a [Claude Code o Codex](hand-to-agent.md) oppure [chiedi a qualcuno di fare una revisione](ask-to-review.md).
- **Ripeti…**: l’attività [torna a intervalli regolari](recurring.md).
- **Non serve**: l’attività scompare. Puoi anche indicare il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara dalla scelta.

Tocca il titolo o **Nome** sotto **Dettagli** per rinominare l’attività, oppure chiedilo nella chat, per esempio «Rinominala …». Il titolo resta invariato.

**Riapri** riporta un’attività chiusa tra quelle aperte. Torna anche automaticamente se succede qualcosa di nuovo, per esempio un nuovo messaggio da quella persona, ma non quando rispondi tu. L’attività mostra quando è stata riaperta e viene ordinata come nuova. La chat riprende da dove era stata interrotta, anche dopo settimane.

Una fattura che devi ancora pagare tu, da qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dati di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta salvata, non diventano attività. Quando una successiva email conferma il pagamento, per esempio con un messaggio del mittente che conferma la ricezione, l’attività si chiude automaticamente. **Annulla** la riapre per un giorno.

Un’attività che serve solo fino a un momento preciso, per esempio una conferma prima di una riunione, si chiude automaticamente dopo quell’ora. Passa a **Fatte / scartate** con la dicitura «Non serve più». **Annulla** la riapre per un giorno.

Prima che un messaggio o un passaggio di consegne per qualcuno risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, incluse le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché la persona era stata avvisata e ha detto di sì, si chiude automaticamente. **Annulla** la riapre per un giorno.

Se qualcun altro ha scritto nella stessa conversazione dopo la creazione della bozza, **Invia** la mette in attesa: «Non inviata: nuovo messaggio nella conversazione». L’attività mostra quel messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per inviare la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna le attività automaticamente. Un’attività ancora utile segue i nuovi piani. Se non c’è più nulla da fare, passa a **Fatte / scartate** con la dicitura «Non serve», la chat mostra «Aggiornamento:» e il motivo, e **Annulla** la riapre per un giorno.

Tra le prime attività compare un breve suggerimento sulle azioni principali: **Chiedi modifiche** e **Non serve**, e sul fatto che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La bozza di quella risposta viene preparata per prima, così è pronta al tuo arrivo.

Ogni attività inizia con il titolo. La riga sotto indica chi è coinvolto, l’organizzazione se pertinente, il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la sua pagina nel Graph.

Se nel Graph è disponibile, accanto al nome o all’organizzazione compare una foto o un logo; altrimenti vengono mostrate le iniziali. Anche un logo difficile da leggere in piccolo, per esempio bianco su sfondo trasparente o con un marchio molto largo, viene sostituito dall’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessuna novità». Compare quando l’ultimo contatto è vecchio o senza risposta e segnala i canali non collegati, come WhatsApp. La tua Machine indica ciò che non sa invece di fare supposizioni.

Se viene indicato un canale non collegato, tocca **Connetti** accanto al suo nome per aprire la relativa connessione.

Il titolo indica cosa bisogna fare e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo, con sotto l’esito, per esempio «Completata: Sam l’ha firmata martedì».

Sopra la bozza, una riga in grigio indica il messaggio da cui proviene e mostra il logo del servizio. Toccalo per leggere la conversazione. La bozza mostra il logo della destinazione, così capisci subito se si tratta di una risposta su Slack o di un’email.

Se la bozza si basa su un contributo ricevuto altrove, per esempio un suggerimento di un collega su Slack, una riga lo indica, per esempio «In base a Sam in #ops». Tocca la riga per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra un’unica conversazione, dalla più vecchia alla più recente: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal, i tuoi messaggi appaiono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e si apre nella conversazione. **Mostra messaggi precedenti** aggiunge quelli più vecchi. In un’email, il resto della conversazione è raccolto in sezioni chiuse sopra e sotto il messaggio.

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android si apre nell’app Gmail, se è installata.

I **Dettagli** di un’email mostrano solo le informazioni non presenti nell’intestazione, per esempio gli indirizzi completi in Cc, quelli in Ccn o un indirizzo di risposta diverso. Se non c’è altro da mostrare, la sezione non compare.

Una risposta in un thread di Slack mostra anche cosa è stato detto prima dell’inizio del thread. Il link dell’attività al suo messaggio apre anche qui la conversazione, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area, che puoi modificare toccandoli, l’ultima nota e il risultato di un agente di programmazione. Tocca il titolo per aprire la chat. Un’attività completata resta compatta: il messaggio da cui proviene si trova in **Dettagli**.

Un’attività «In attesa di» collega il tuo ultimo messaggio a quella persona, la risposta che stai aspettando, per esempio «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) aggiunge un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, l’attività va nella categoria giusta in base a chi riguarda e all’argomento. Trova anche l’email a cui fa seguito, comprese quelle meno recenti.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore», anche nella tua lingua. L’icona del calendario mostra alcune opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività torna a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende coinvolte, fino a 5.
- Icona del messaggio: allega il messaggio a cui si riferisce l’attività: un’email, un messaggio di Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file sul modulo. Sul telefono, tocca l’icona della fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come in chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano con l’attività e la tua Machine li legge mentre ci lavora. Puoi anche aggiungere solo file: la tua Machine crea l’attività partendo da un PDF o da un file di testo. Una foto viene mostrata come immagine in miniatura. Tocca l’immagine per vederla a grandezza naturale.
