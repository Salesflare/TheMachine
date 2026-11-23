---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 51db64e67403d2ea
---
La tua Machine legge tutte le novità e crea un’attività solo quando qualcosa richiede il tuo intervento. Una sola attività per ogni questione, anche se riguarda più messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa così:

- **Appena fatto**: in cima, mostra un ultimo passaggio che hai confermato, come l’invio di un modulo o la risoluzione di un problema mentre non c’eri. Resta lì finché non tocchi **Ho capito**, per un massimo di un giorno. Lo ricevi anche sul telefono.
- **Per te**: tutto ciò che aspetta una tua risposta, in ordine di urgenza. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e **Fallo** o **Invia** lo completano), **Serve il tuo intervento** (prima serve una tua decisione o risposta; se il lavoro si è fermato perché solo tu puoi fornire un’informazione, accedere o fare una scelta, sotto il titolo trovi una nota), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un resoconto che non richiede decisioni).
- **Più vecchie**: attività ripiegate su cui non ci sono novità da una settimana (vedi sotto).
- **In attesa di altri**: attività ripiegate in cui il prossimo passo spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e attività per cui non hai risposto a **Serve ancora?** (vedi sotto).
- **Promesse**: quello che hai promesso e quello che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatta 5 minuti fa». Le attività che sembrano già completate sono contrassegnate come **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviato. Spostata in Fatte» oppure «Inviato. Spostata in Più tardi fino a lunedì». Una risposta che si limita a promettere di fare qualcosa, come «Te lo mando entro martedì», lascia l’attività aperta: «Inviato. Lasciata aperta». **Apri** ti porta all’attività. La ricerca trova un’attività in base al titolo o al destinatario, anche in Più tardi e Fatte.

In **Per te** compaiono prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, i promemoria di una bacheca e infine le altre. All’interno di ogni gruppo, le più recenti vengono prima. L’attività mantiene la sua posizione mentre la tua Machine la prepara e quando è completata: cambia solo il contrassegno. Negli altri gruppi aperti, le attività scadute o in scadenza entro domani vengono prima, seguite dalle altre in ordine dalla più recente. Anche la barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che l’attività è stata completata, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e aiuta la tua Machine a imparare. Queste attività non risultano mai in ritardo. Se compare in un messaggio, si chiude da sola dopo un giorno e puoi usare **Annulla**. Altrimenti resta in attesa che tu selezioni **Segna come fatto**. Anche un’attività che hai già gestito, per esempio rispondendo in Gmail o Slack, si chiude da sola.

Se un messaggio arriva da un indirizzo che somiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo indica chiaramente: «Non è Sam Lee». Mostra la persona con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi lo ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio di una revisione o di una risposta, indica il passaggio con **In attesa di:**. Si trova in **In attesa di altri**, ripiegata sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso succede dopo che hai fatto una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è più tardi oggi, oppure la mattina dopo se la scadenza è già passata. Indica anche chi deve ancora rispondere.

Se l’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, in **Dettagli** trovi il risultato indicato in **Fatto quando**. L’invio della tua parte non la chiude: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola. Puoi usare **Annulla** per riaprirla. Se non arriva nulla entro il momento in cui è il caso di sollecitare, torna con **Scrivi un breve sollecito** nella chat. Per cambiare cosa conta come completamento, scrivilo nella chat.

Dopo una settimana senza novità, un’attività passa da Per te a **Più vecchie**, così al tuo ritorno trovi prima quelle nuove. Per novità si intende un nuovo messaggio o qualcosa che hai fatto sull’attività, come inviare un messaggio in chat, modificarla o posticiparla. Aprirla non conta.

Le attività urgenti, in scadenza a breve o con un invio in corso restano in Per te. **Scarta tutto** contrassegna tutte le attività in Più vecchie come non necessarie con una sola conferma. Puoi anche contrassegnarle una alla volta con **Non serve**. In entrambi i casi puoi usare **Annulla**. Se arriva una novità, l’attività torna in Per te.

Se nessuno interviene su un’attività per una settimana, viene chiesto una volta: **Serve ancora?** **Non serve** la chiude; puoi usare **Annulla**. **Tieni** la mantiene e non te lo chiederà più. Se non rispondi per un’altra settimana, viene ripiegata in Torna più tardi e non viene più conteggiata sul badge dell’app né nel riepilogo mattutino. Aprirla, inviare un messaggio in chat, modificarla, posticiparla o ricevere un nuovo messaggio la fa tornare nell’elenco.

Una volta a settimana, un progetto rimasto inattivo e senza attività aperte può generare un’attività con un prossimo passo preciso, per un massimo di tre a settimana. Vedi [Progetti](projects.md).

Quando nulla richiede il tuo intervento, la tua Machine si riposa e l’elenco resta vuoto. Mentre controlla, si riattiva e te lo comunica. Se un controllo non è riuscito o è in ritardo, la nota lo indica e mostra **Controlla ora**.

Le schede **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer trovi la stessa selezione. Quando è attivo Lavoro o Personale, **Mostra tutto** torna a mostrare tutte le attività. Un avviso che riguarda la tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La nota in cima all’elenco ti permette anche di passare direttamente all’altra sezione: in **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il nome dell’ultimo riepilogo mattutino o serale e cosa ha conteggiato, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Tocca la riga per rileggere il riepilogo e usare **Copia** per incollarlo dove vuoi. Una volta aperto o chiuso con **×**, resta visibile su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non ci sono riepiloghi recenti, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per la sezione selezionata.

Le attività di un progetto mostrano il nome del progetto sotto il titolo. Toccalo per aprire il progetto. **Progetto** in **Dettagli** ti permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

**Area** in **Dettagli** sposta un’attività nell’altra area. Con l’attività si spostano anche le informazioni che può leggere e da cui può inviare. **Annulla** nella nota la riporta dov’era.

Se un’attività ha bisogno dell’altra area per procedere e tutti i messaggi a cui si riferisce si trovano lì, si sposta da sola e continua. Altrimenti mostra **Sposta in Lavoro** e non si sposta finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale viene assegnata da sola all’area corretta, una volta individuata. Nel frattempo non risulta né Lavoro né Personale e resta privata.

Un’attività può sempre leggere i messaggi a cui si riferisce. Se ha bisogno di altri messaggi dell’altra area, ti chiede **Usa questa email per questa attività**. Un account di lavoro che hai contrassegnato come Personale viene considerato Personale. Le email di altre aziende per cui lavori vengono assegnate alle attività di quell’azienda. Un’attività sulla tua vita privata, per esempio un messaggio di famiglia arrivato al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, per esempio un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. Lavoro o Personale determina dove compare un’attività e con chi viene condivisa, mai dove risponde: la risposta va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro o nel Graph del team.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te permette di esaminarle una alla volta, nell’ordine dell’elenco. Per ciascuna mostra la bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. L’intestazione indica quanto tempo ci vuole al tuo ritmo, per esempio «circa 2 min».

Alla fine, mostra quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Un’attività che ti fa una domanda non viene inclusa: serve la tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, di giorno e di notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa oppure quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, da 00:00 a 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati insieme alle 06:30, così le attività sono pronte prima del riepilogo mattutino. In Connessioni, sotto Controlli, compare «In pausa per la notte. Recupero alle 06:30». Se di notte fai clic, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non ti allontani per un’ora. **Controlla ora** avvia sempre un controllo immediato.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla insieme a **Dettagli**, che apre Controlli in Connessioni. Se ci sono attività aperte, sul computer trovi Controlla ora in cima. La breve nota compare solo mentre è in corso un controllo, oppure se uno non è riuscito o è in ritardo. Puoi anche chiederlo in chat.

LinkedIn, X e Salesflare seguono i propri ritmi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una nota con quello che ha trovato in tutte le fonti controllate, per esempio «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». La nota riguarda solo quel controllo: le attività già nell’elenco restano in attesa come prima. Se una nuova attività viene tenuta da parte per un momento più opportuno, per esempio il riepilogo mattutino, viene indicato fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la nota per vedere ogni conversazione email, chat e notifica con l’icona della fonte. Mostra chi ha scritto, l’oggetto o le prime parole e l’attività creata o il motivo per cui non ne serviva una, per esempio «Solo in Cc, risponde una persona del team» oppure «Riunione già fissata per giovedì». Se il controllo ha restituito solo un motivo generico, non viene mostrato alcun motivo per la conversazione. Tocca una voce per leggerla.

Vengono mostrate le prime 10 voci. Tocca sotto per vedere le altre. Un numero dopo un nome, come (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già nell’elenco compare una sola volta. La nota resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email che ricevi. Le tue risposte vengono lette per capire il contesto e le promesse, ma non sono nuove email. Le email che The Machine invia a te, come il riepilogo mattutino o una notifica di correzione, non vengono mai lette né mostrate. Le email relative alla fatturazione, al periodo di prova o a un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passo, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando una bozza è pronta, cosa modificare al suo interno. **Segna come fatto** indica che l’attività è stata gestita. Compare subito su un’attività pronta senza bozza o su una che ti fa una domanda; negli altri casi si trova in cima a **…**. L’attività scompare subito dall’elenco e nel messaggio compare **Annulla**. Scorri il messaggio via oppure trascinalo fuori con il mouse per chiuderlo prima. La modifica resta.

Per completare l’attività in un altro modo, scrivilo nella sua **Chat**. La risposta indica solo cosa è cambiato, per esempio se è stata posticipata e fino a quando. Se non è stato possibile modificare qualcosa, come la data di scadenza, viene indicato.

In **…**:

- **Passa…**: assegnala a una persona del team, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: l’attività [torna a intervalli regolari](recurring.md).
- **Non serve**: l’attività scompare. Puoi anche indicare il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara da questa scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività. Puoi anche chiederlo nella chat, per esempio «Rinominala …». Il titolo che scegli resta.

**Riapri** riporta nell’elenco un’attività chiusa. Torna anche da sola quando succede qualcosa di nuovo, per esempio quando arriva un nuovo messaggio da quella persona, ma non se rispondi tu. Viene indicato quando è tornata e l’attività viene ordinata come nuova. La chat continua da dove si era interrotta, anche dopo settimane.

Una fattura che devi pagare tu, da qualsiasi paese, diventa un’attività con l’importo, la data di scadenza e i dettagli di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con addebito diretto o carta registrata, non diventano attività. Quando un’email successiva conferma il pagamento, per esempio perché il mittente ha ricevuto il pagamento, l’attività si chiude da sola. Puoi usare **Annulla** per riaprirla per un giorno.

Un’attività che serve solo fino a un momento preciso, per esempio una conferma prima di una riunione, si chiude da sola dopo quell’ora. In **Fatte / scartate** compare come «Non serve più». Puoi usare **Annulla** per riaprirla per un giorno.

Prima che un messaggio o un passaggio a qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, incluse le chat di gruppo, e aspetta che Slack le abbia lette. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché qualcuno ha fatto una richiesta e ha ricevuto un sì, l’attività si chiude da sola. Puoi usare **Annulla** per riaprirla per un giorno.

Se qualcun altro scrive nella stessa conversazione dopo che la bozza è stata preparata, **Invia** la blocca: «Non inviato: nuovo messaggio nella conversazione». L’attività mostra il messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per inviare la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio perché una festa è stata spostata o una prenotazione è saltata, The Machine aggiorna le attività da sola. Quelle ancora necessarie seguono i nuovi piani. Quelle che non richiedono più nulla passano a **Fatte / scartate** con la dicitura «Non serve». Nella chat compare «Aggiornamento:» seguito dal motivo. Puoi usare **Annulla** per riaprirle per un giorno.

Alla prima visita alle attività, un breve suggerimento mostra le azioni principali: **Chiedi modifiche** e **Non serve**. Spiega anche che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica a chi si riferisce, l’organizzazione se pertinente (non solo perché qualcuno ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se nel Graph sono presenti, accanto al nome e all’organizzazione compaiono la foto o il logo; altrimenti vengono mostrate le iniziali. Se un logo non si legge bene in piccolo, per esempio perché è bianco su sfondo trasparente o è un marchio allungato, viene mostrata anche l’iniziale.

A volte una nota discreta indica ciò che non è noto, per esempio «Ultimo contatto 12 giorni fa via email; nessuna novità da allora». Compare quando l’ultimo scambio è datato o senza risposta e indica anche i canali non collegati, come WhatsApp. La tua Machine dichiara ciò che non sa invece di tirare a indovinare.

Se viene indicato un canale non collegato, tocca **Connetti** accanto al suo nome per collegarlo.

Il titolo descrive cosa c’è da fare e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo e indica sotto come è terminata, per esempio «Fatta: Sam l’ha firmata martedì».

Sopra la bozza, una riga in grigio chiaro indica il messaggio da cui proviene e mostra il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo della destinazione, così puoi vedere subito se si tratta di una risposta su Slack o di un’email.

Se la bozza tiene conto del contributo di qualcuno altrove, per esempio un suggerimento di una persona del team su Slack, una nota lo indica, per esempio «Basata sul messaggio di Sam in #ops». Tocca la nota per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) viene mostrata come un’unica conversazione, dalla più vecchia alla più recente: include i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal i tuoi messaggi compaiono a destra, come nell’app. Il messaggio relativo all’attività è contrassegnato con «Questa attività» e viene visualizzato. **Mostra messaggi precedenti** aggiunge quelli più vecchi. Un’email mostra il resto della conversazione ripiegato sopra e sotto il messaggio.

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android si apre nell’app Gmail, se è installata.

In **Dettagli** di un’email compaiono solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, i destinatari in Ccn o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, non compare nulla.

Una risposta in un thread Slack mostra anche i messaggi precedenti all’inizio del thread. Il link dell’attività al proprio messaggio apre anche qui la conversazione, con **Apri in Slack** in fondo.

In **Dettagli** trovi il nome, il progetto e l’area (tocca una voce per modificarla), la tua ultima nota e il risultato di un agente di programmazione. Il titolo apre la chat. Un’attività completata resta breve; il messaggio da cui proviene si trova in **Dettagli**.

Un’attività in attesa di qualcuno include un link al tuo ultimo messaggio a quella persona, quello a cui aspetti una risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) aggiunge un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, l’attività viene assegnata all’area giusta in base alla persona e all’argomento. Trova anche l’email a cui si riferisce, comprese quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore», anche nella tua lingua. L’icona del calendario offre alcune opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività torna a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, da email, Slack, Teams, WhatsApp, Telegram o da qualsiasi altra fonte disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato mostra la fonte, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, tocca la fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come in chat (vedi [Aggiungere file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano allegati all’attività e la tua Machine li legge mentre ci lavora. Puoi anche allegare solo dei file: la tua Machine crea l’attività a partire da un PDF o un file di testo. Una foto viene mostrata come miniatura; toccala per vederla a grandezza naturale.
