---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via libera. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e7e5d78b3291e556
---
La tua Machine legge tutte le novità e crea un’attività solo quando serve il tuo intervento. Una sola attività per ogni questione, anche se coinvolge molti messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in alto trovi l’ultimo passaggio che hai confermato, per esempio l’invio di un modulo o la risoluzione di un problema mentre non c’eri. Resta qui finché non tocchi **Ho capito**, per un giorno al massimo. Ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che aspetta una tua risposta, dal più urgente. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima serve una tua decisione o risposta; se il lavoro si è fermato perché serve qualcosa che solo tu puoi fornire, come un’informazione, l’accesso o una scelta, trovi una nota sotto il titolo), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o una breve nota, senza decisioni da prendere).
- **Più vecchie**: attività chiuse in un gruppo, senza novità da una settimana (vedi sotto).
- **In attesa di altri**: attività chiuse in un gruppo, in cui il prossimo passaggio spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e quelle senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: ciò che hai promesso e ciò che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività concluse, dalla più recente, con l’ora in cui sono state concluse, per esempio «Fatto 5 minuti fa». Le attività che sembrano già concluse sono contrassegnate come **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviato. Spostato tra le attività fatte» o «Inviato. Spostato tra le attività successive fino a lunedì». Una risposta che si limita a promettere di fare qualcosa, come «Te lo invierò entro martedì», lascia aperta l’attività: «Inviato. Lasciato aperto». **Apri** ti porta all’attività. La ricerca trova le attività per titolo o per destinatario, anche tra quelle successive e quelle fatte.

**Per te** mostra prima ciò che è scaduto o scade entro domani, poi le domande della tua Fleet, poi i promemoria di una bacheca e infine il resto. All’interno di ogni gruppo, le attività sono ordinate dalla più recente. Un’attività resta nello stesso posto mentre la tua Machine la prepara e anche quando viene completata: cambia solo il contrassegno. Negli altri gruppi aperti, le attività scadute o in scadenza entro domani vengono prima, seguite dalle altre dalla più recente. Anche la barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine ha rilevato che l’attività è conclusa, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e la tua Machine ne tiene conto. Queste attività non risultano mai in ritardo. Dopo un giorno si chiudono da sole, con **Annulla** a disposizione. Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola.

Quando un messaggio arriva da un indirizzo che assomiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Questo non è Sam Lee». La persona viene indicata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio di una revisione o di una risposta, indica **In attesa di:** seguito dal passaggio. Si trova in **In attesa di altri**, nel gruppo chiuso sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso vale dopo che hai risposto con una domanda: l’attività ricompare la mattina prima della scadenza, alla scadenza se è più tardi nella stessa giornata oppure la mattina successiva se la scadenza è passata. Indica anche chi deve ancora rispondere.

Quando un’attività riguarda un risultato che deve fornire qualcun altro, per esempio un contratto firmato, **Dettagli** lo mostra alla voce **Fatto quando**. Inviare la tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola, con **Annulla** a disposizione. Se non arriva nulla entro il momento in cui è il caso di sollecitare, l’attività ricompare con **Scrivi un breve sollecito** nella chat. Per modificare cosa conta come concluso, scrivilo nella chat.

Se non ci sono novità per una settimana, un’attività passa da Per te a **Più vecchie**, così dopo qualche giorno di assenza trovi prima quelle nuove. Per novità si intende un nuovo messaggio sull’attività o qualcosa che hai fatto, come inviare un messaggio in chat, modificarla o posticiparla. Aprirla e basta non conta.

Le attività urgenti, quelle in scadenza a breve e quelle con un invio in corso restano in Per te. **Scarta tutto** contrassegna come non necessarie tutte le attività in Più vecchie dopo una sola conferma, proprio come fa **Non serve** per una singola attività, con **Annulla** a disposizione. Se arriva una novità, l’attività torna in Per te.

Se nessuno interviene su un’attività per una settimana, viene chiesto una volta: **Serve ancora?** **Non serve** la chiude, con **Annulla** a disposizione. **Tieni** la mantiene e non viene più fatta la domanda. Se non rispondi per un’altra settimana, l’attività viene spostata nel gruppo chiuso Torna più tardi e non viene più conteggiata sul numero dell’icona dell’app né nel riepilogo del mattino. Aprirla, inviare un messaggio in chat, modificarla, posticiparla o ricevere un nuovo messaggio la fa ricomparire.

Una volta a settimana, un progetto rimasto inattivo e senza attività aperte può ricevere un’attività con un prossimo passo specifico, fino a tre a settimana. Vedi [Progetti](projects.md).

Quando non c’è nulla che richiede il tuo intervento, la tua Machine si riposa e l’elenco è vuoto. Durante un controllo si riattiva e te lo dice. Se un controllo non è riuscito o è in ritardo, la nota lo segnala e mostra **Controlla ora**.

Le voci **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer trovi la stessa selezione. Quando è attivo Lavoro o Personale, **Mostra tutto** torna a tutte le attività. Un avviso sulla tua Machine, per esempio se un componente continua a riavviarsi, non è né Lavoro né Personale e appare solo in Tutti.

La riga in cima all’elenco ti permette anche di passare direttamente all’altro tipo: con **Solo personale** attivo, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il nome dell’ultimo riepilogo del mattino o della sera e il numero di attività conteggiate, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Toccalo per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, resta su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non hai un riepilogo recente, viene mostrato **Oggi finora**: ciò che è stato fatto oggi e ciò che è ancora aperto, per Lavoro e Personale o solo per il tipo che hai selezionato.

Le attività di un progetto mostrano il nome del progetto sotto il titolo. Toccalo per aprire il progetto. **Progetto** in **Dettagli** permette di modificarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

**Area** in **Dettagli** sposta un’attività nell’altra area. Con essa si spostano anche le fonti che può leggere e da cui può inviare messaggi. **Annulla** nella nota la riporta al suo posto.

Se per proseguire un’attività serve l’altra area e tutti i messaggi da cui proviene si trovano lì, l’attività si sposta da sola e continua. Altrimenti mostra **Sposta in Lavoro** e nulla si sposta finché non la tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola appena trova la sua area. Fino ad allora non è né Lavoro né Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, lo chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai contrassegnato come Personale viene considerata Personale. Le email di un’altra delle tue aziende finiscono nelle attività di quella società. Un’attività sulla tua vita privata, per esempio un messaggio di famiglia arrivato all’indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, per esempio un cliente su WhatsApp o un ordine nella casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. Lavoro o Personale determina dove appare un’attività e con chi viene condivisa, mai dove invia la risposta: questa va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Anche se è Personale, un’attività risponde dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in una Fleet di lavoro o nel Graph del team.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. Sotto il titolo, l’intestazione indica anche quanto tempo richiede, al tuo ritmo, per esempio «circa 2 min».

Un’attività che ti fa una domanda resta fuori da entrambe le liste: serve la tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa oppure quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Controlli, sotto Connessioni, compare «In pausa per la notte, recupera alle 06:30». Se di notte fai clic, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non ti assenti per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla, con **Dettagli** che apre Controlli in Connessioni. Se hai attività aperte, la trovi in cima sul computer. La breve nota appare solo mentre è in corso un controllo oppure se uno è fallito o in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga con ciò che ha trovato in tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · nulla richiede il tuo intervento» oppure «· 2 nuove attività». Se una nuova attività è in attesa di un momento più adatto, come il riepilogo del mattino, viene indicato fino a quando: «1 attività in pausa fino a domani alle 08:30».

Tocca la riga per vedere ogni email, chat e notifica con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività o il motivo per cui il messaggio non richiedeva interventi, per esempio «Sei solo in cc, risponde un collega» o «Riunione già fissata per giovedì». Se il controllo ha dato solo un motivo generico, la conversazione non ne mostra uno. Tocca un elemento per leggerlo.

Vengono mostrati i primi 10 elementi; tocca sotto per vedere gli altri. Un numero dopo un nome, per esempio (3), indica quanti nuovi messaggi contiene quella chat. Una notifica sul telefono relativa a un messaggio già nell’elenco appare una sola volta. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email indirizzate a te. Le tue risposte vengono lette per il contesto e per le promesse, ma non sono considerate nuove email. Le email inviate a te dalla Machine, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email relative alla fatturazione, alla prova o a un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il passaggio successivo, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando una bozza è pronta, cosa modificare. **Segna come fatto** indica che è stata gestita: si vede subito sulle attività pronte senza bozza, altrimenti si trova in cima a **…**, anche per un’attività che richiede una tua decisione. L’attività lascia subito l’elenco e nel messaggio compare **Annulla**. Scorri il messaggio per chiuderlo oppure trascinalo fuori con il mouse. La modifica resta.

Per farla in un altro modo, scrivilo nella **Chat** dell’attività.

In **…**:

- **Passa…**: affidala a un collega, a [Claude Code o Codex](hand-to-agent.md) oppure [chiedi a qualcuno di revisionarla](ask-to-review.md).
- **Ripeti…**: l’attività [si ripresenta a intervalli regolari](recurring.md).
- **Non serve**: l’attività scompare. Se vuoi, indica il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine ne tiene conto.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività, oppure chiedilo nella chat, per esempio «Rinominala …». Il titolo resta quello che hai scelto.

**Riapri** fa ricomparire un’attività chiusa. Ricompare anche da sola quando succede qualcosa di nuovo, per esempio arriva un loro messaggio, ma non dopo una tua risposta. Mostra quando è ricomparsa e viene ordinata come una nuova attività. La chat riprende da dove si era interrotta, anche dopo settimane.

Una bolletta che devi pagare tu, da qualsiasi paese, diventa un’attività con l’importo, la data di scadenza e i dettagli di pagamento indicati nella bolletta. Le bollette pagate automaticamente, per esempio con un addebito diretto o una carta registrata, non diventano attività. Quando un’email successiva conferma il pagamento, per esempio con un messaggio del mittente che conferma di averlo ricevuto, l’attività si chiude da sola. **Annulla** la fa ricomparire per un giorno.

Un’attività utile solo fino a un momento preciso, per esempio una conferma da inviare prima di una riunione, si chiude da sola dopo quel momento. Viene spostata in **Fatte / scartate** con la dicitura «Non serve più». **Annulla** la fa ricomparire per un giorno.

Prima che un messaggio o un passaggio di consegne per qualcuno risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, comprese quelle di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché è stata fatta una richiesta e l’altra persona ha risposto di sì, l’attività si chiude da sola. **Annulla** la fa ricomparire per un giorno.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna le attività da sola. Un’attività ancora necessaria segue i nuovi piani. Se non resta più nulla da fare, viene spostata in **Fatte / scartate** con la dicitura «Non serve», la chat indica «Aggiornamento:» e il motivo, e **Annulla** la fa ricomparire per un giorno.

Quando crei le prime attività, un breve suggerimento mostra le azioni principali: **Chiedi modifiche** e **Non serve**, e ricorda che nulla viene inviato finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il relativo pulsante o premi ×.

Il primo giorno, in cima alla pagina Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica di chi si tratta, l’organizzazione se pertinente, mai solo perché la persona ci lavora, il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Quando il Graph ha una foto o un logo, il nome e l’organizzazione li mostrano; altrimenti mostrano le iniziali. Se un logo non si legge bene in piccolo, per esempio perché è bianco su sfondo trasparente o è un marchio orizzontale, viene mostrata anche l’iniziale.

A volte una nota in grigio indica ciò che non si sa, per esempio «Ultimo contatto 12 giorni fa via email, nessuna novità da allora». Compare quando l’ultimo contatto risale a tempo fa o è rimasto senza risposta, e indica anche i canali non collegati, come WhatsApp. La tua Machine ti dice ciò che non sa invece di tirare a indovinare.

Quando viene indicato un canale non collegato, **Collega** accanto al suo nome apre la relativa connessione.

Il titolo indica cosa bisogna fare e cambia solo quando cambia l’attività. Un’attività completata mantiene il titolo e indica sotto come si è conclusa, per esempio «Fatto: Sam l’ha firmato martedì».

Sopra la bozza, una riga in grigio indica il messaggio da cui proviene, con il logo del servizio. Toccarla apre la conversazione. La bozza mostra il logo del servizio a cui è destinata, così vedi subito se è una risposta Slack o un’email.

Se la bozza si basa su un suggerimento ricevuto altrove, per esempio da un collega su Slack, una riga lo indica, per esempio «Basato sul messaggio di Sam in #ops». Toccarla apre il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra un’unica conversazione, dalla più vecchia alla più recente: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal, i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e viene visualizzato. **Mostra messaggi precedenti** aggiunge i messaggi più vecchi. In un’email, il resto della conversazione è raccolto sopra e sotto il messaggio.

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android si apre nell’app Gmail, se ce l’hai.

**Dettagli** di un’email mostrano solo le informazioni che non compaiono nell’intestazione, per esempio gli indirizzi completi in Cc, il campo Ccn o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, non mostra nulla.

Una risposta in una conversazione Slack mostra anche ciò che è stato detto prima che iniziasse. Il link dell’attività al suo messaggio apre anche la conversazione qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area dell’attività (tocca uno di questi elementi per modificarlo), la tua ultima nota e il risultato di un agente di programmazione. Il titolo apre la chat. Un’attività completata resta compatta; il messaggio da cui proviene si trova in **Dettagli**.

Un’attività «In attesa di» collega il tuo ultimo messaggio alla persona, quello a cui stai aspettando risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, viene assegnata all’area giusta in base a chi e a cosa riguarda. Trova anche l’email a cui dà seguito, comprese quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore», anche nella tua lingua. L’icona del calendario mostra alcune opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività si ripresenta a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, per esempio un’email, un messaggio Slack, Teams, WhatsApp, Telegram o un altro messaggio disponibile in The Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, chi l’ha inviato e quando.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file sul modulo. Sul telefono puoi scattare una foto con l’icona della fotocamera accanto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano con l’attività e The Machine li legge mentre ci lavora. Puoi allegare solo i file: la tua Machine crea l’attività a partire da un PDF o da un file di testo. Una foto viene mostrata come immagine piccola; toccala per vederla a grandezza intera.
