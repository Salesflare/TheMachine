---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via libera. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e1656daff6fc566a
---
La tua Machine legge tutte le novità e crea un’attività solo quando qualcosa richiede il tuo intervento. Un’attività per ogni questione, indipendentemente da quanti messaggi coinvolge.

## Dove si trovano le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in alto, trovi l’ultimo passaggio che hai confermato, come l’invio di un modulo o la gestione di un problema, completato mentre non c’eri. Resta qui finché non tocchi **Ho capito**, per un giorno al massimo. Ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che aspetta il tuo intervento, in ordine di urgenza. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima serve una tua decisione o una risposta; se il lavoro non può proseguire o essere usato senza qualcosa che solo tu puoi fornire, come un prezzo, un dato o una scelta, una riga sotto il titolo specifica cosa serve), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o una nota informativa, senza decisioni da prendere).
- **Più vecchie**: attività senza novità da una settimana, raccolte in un gruppo chiuso (vedi sotto).
- **In attesa di altri**: attività in cui il prossimo passaggio spetta a qualcun altro, raccolte in un gruppo chiuso (vedi sotto).
- **Torna più tardi**: attività posticipate e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: ciò che hai promesso e ciò che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora del completamento, per esempio «Fatto 5 minuti fa». Le attività che sembrano già concluse sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviata. Spostata in Fatte.» oppure «Inviata. Spostata in Più tardi fino a lunedì». Una risposta che si limita a promettere di fare il lavoro, come «Te lo invio entro martedì», lascia aperta l’attività: «Inviata. Lasciata aperta». **Apri** ti porta all’attività. La ricerca trova le attività per titolo o per destinatario, anche in Più tardi e Fatte.

In **Per te** vengono prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, quindi i promemoria di una bacheca e infine le altre. All’interno di ogni gruppo, l’ordine è dalla più recente. Un’attività resta al suo posto mentre la tua Machine la prepara e anche quando è completata: cambia solo il contrassegno. Negli altri gruppi aperti, le attività scadute o in scadenza entro domani vengono prima, seguite dalle altre in ordine dalla più recente. Anche la barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede l’attività come conclusa, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e la tua Machine impara da questa scelta. Queste attività non risultano mai in ritardo. Se il contrassegno compare su un messaggio, l’attività si chiude da sola dopo un giorno e puoi usare **Annulla**. Altrimenti, resta in attesa che tu scelga **Segna come fatto**. Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola.

Se un messaggio proviene da un indirizzo che somiglia a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo indica chiaramente: «Questo non è Sam Lee». Mostra la persona con il suo vero indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica il passaggio con **In attesa di:**. Rimane nel gruppo chiuso **In attesa di altri**, sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso vale dopo che hai fatto una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è più tardi oggi oppure la mattina successiva se la scadenza è passata. Indica anche chi deve ancora rispondere.

Se l’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, in **Dettagli** trovi la voce **Fatto quando**. Inviare la tua parte non la chiude: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola e puoi usare **Annulla**. Se il risultato non arriva entro il momento in cui dovresti sollecitare, l’attività ricompare con **Scrivi un breve sollecito** nella chat. Per cambiare cosa significa che è completata, scrivilo nella chat.

Un’attività senza novità da una settimana passa da Per te a **Più vecchie**, così dopo qualche giorno di assenza trovi prima quelle nuove. Per novità si intende un nuovo messaggio o qualcosa che hai fatto sull’attività, come un messaggio in chat, una modifica o un posticipo. Aprire l’attività non conta.

Le attività urgenti, in scadenza a breve o con un invio in corso restano in Per te. **Scarta tutto** contrassegna come non necessarie tutte le attività in Più vecchie dopo una sola conferma, proprio come fa **Non serve** per una singola attività. Puoi usare **Annulla**. Se arriva una novità, l’attività torna in Per te.

Un’attività che nessuno ha toccato per una settimana chiede una volta: **Serve ancora?** **Non serve** la chiude e puoi usare **Annulla**. **Tieni** la mantiene aperta e non te lo chiederà più. Se non rispondi per un’altra settimana, viene raccolta in Torna più tardi e non viene più conteggiata sul badge dell’app né nel riepilogo del mattino. Se la apri, invii un messaggio in chat, la modifichi, la posticipi o arriva un nuovo messaggio, torna nell’elenco.

Una volta alla settimana, un progetto rimasto inattivo e senza attività aperte può generare un’attività con un prossimo passo specifico, al massimo tre a settimana. Vedi [Progetti](projects.md).

Quando niente richiede il tuo intervento, la tua Machine si riposa e l’elenco resta vuoto. Durante un controllo, si riattiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, la riga lo indica e mostra **Controlla ora**.

I filtri **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività oppure solo quelle di un tipo. Il telefono e il computer usano la stessa selezione. Se hai scelto Lavoro o Personale, **Mostra tutto** torna a visualizzare tutte le attività. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima all’elenco permette anche di passare direttamente all’altro filtro: con **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il nome del tuo ultimo riepilogo del mattino o della sera e il numero di attività conteggiate, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Tocca la riga per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Quando lo apri o tocchi la sua **×**, resta disponibile su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non hai un riepilogo recente, trovi **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per il filtro selezionato.

Un’attività di un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. La voce **Progetto** in **Dettagli** permette di cambiarlo o rimuoverlo. Vedi [le attività di un progetto](projects.md#a-project-s-to-dos).

La voce **Area** in **Dettagli** sposta un’attività nell’altra area. Anche le fonti che può leggere e da cui può inviare messaggi vengono spostate. **Annulla** nella nota la riporta indietro.

Quando un’attività ha bisogno dell’altra area per proseguire e tutti i messaggi da cui proviene sono lì, si sposta da sola e continua. Altrimenti mostra **Sposta in Lavoro** e non sposta nulla finché non la tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola appena trova l’area giusta. Fino a quel momento non è contrassegnata né come Lavoro né come Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, te lo chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai contrassegnato come Personale viene considerata personale. Le email indirizzate a un’altra delle tue aziende finiscono nelle attività di quell’azienda. Un’attività che riguarda la tua vita privata, come un messaggio di famiglia al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp, un ordine nella tua casella personale o una [promessa](promises.md) di lavoro, è Lavoro fin dall’inizio.

Un’attività che hai spostato o assegnato a un’area resta sempre dove l’hai messa. Lavoro o Personale determina dove compare e con chi viene condivisa, mai dove risponde: la risposta va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro o nel Graph del team.

Se hai almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza completa e i pulsanti **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Al computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta e Esc interrompe. L’intestazione indica quanto tempo richiede al tuo ritmo, per esempio «circa 2 min».

Alla fine, mostra quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Un’attività che ti fa una domanda non viene inclusa in nessuno dei due gruppi: richiede una risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa o quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si interrompono: i nuovi messaggi vengono comunque letti e conservati, poi controllati insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Controlli, sotto Connessioni, compare «Controlli in pausa per la notte. Recupero alle 06:30». Se di notte clicchi, digiti o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non ci sono attività aperte, tocca la riga della tua Machine per aprirla e trovare **Dettagli**, che apre Controlli sotto Connessioni. Se ci sono attività aperte, al computer la trovi in cima. La riga breve compare solo mentre è in corso un controllo o quando un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga con ciò che ha trovato in tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». La riga riguarda solo quel controllo: le attività già nell’elenco restano in attesa come prima. Se una nuova attività viene tenuta da parte per un momento più adatto, come il riepilogo del mattino, la riga indica fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica con l’icona della fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività o il motivo per cui non serviva farne una, per esempio «In copia, risponde un collega» oppure «Riunione già fissata per giovedì». Se il controllo ha fornito solo un motivo vago, la conversazione non ne mostra uno. Tocca un elemento per leggerlo insieme ai messaggi circostanti.

Vengono mostrati i primi 10 elementi. Tocca sotto per vedere gli altri. Un numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già elencato compare una volta sola. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email che hai ricevuto. Le tue risposte vengono lette per avere contesto e individuare promesse, ma non sono nuove email. Le email che la tua Machine invia a te, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email relative alla fatturazione, al periodo di prova o a un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il passaggio successivo, come **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. **Segna come fatto** indica che l’attività è stata gestita: è visibile su un’attività pronta senza bozza o su una che ti fa una domanda, altrimenti si trova in cima a **…**. L’attività lascia subito l’elenco e nel messaggio compare **Annulla**. Scorri via il messaggio o trascinalo fuori con il mouse per chiuderlo prima. La modifica resta.

Per farla svolgere in un altro modo, scrivilo nella sua **Chat**. La risposta indica solo cosa è cambiato, per esempio il posticipo e fino a quando. Se non è stato possibile modificare qualcosa, come la data di scadenza, te lo dice.

In **…**:

- **Passa…**: assegnala a un collega, a [Claude Code o Codex](hand-to-agent.md) oppure [chiedi a qualcuno di fare una revisione](ask-to-review.md).
- **Ripeti…**: l’attività [torna a intervalli regolari](recurring.md).
- **Non pertinente**: l’attività scompare. Puoi scegliere il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara dalla scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività. Puoi anche chiederlo nella chat, per esempio «Rinominala …». Il titolo che scegli resta invariato.

**Riapri** fa ricomparire un’attività chiusa. L’attività torna anche da sola quando succede qualcosa di nuovo, per esempio se arriva un nuovo messaggio da quella persona, ma non quando rispondi tu. In quel caso indica quando è tornata e viene ordinata come nuova. La chat riprende da dove si era interrotta, anche dopo settimane.

Una fattura che devi ancora pagare tu, di qualunque paese, diventa un’attività con l’importo, la data di scadenza e i dettagli di pagamento indicati nella fattura. Quelle pagate automaticamente, per esempio con un addebito diretto o una carta registrata, non diventano attività. Quando un’email successiva conferma il pagamento, per esempio con un messaggio del mittente che conferma di averlo ricevuto, l’attività si chiude da sola. Puoi usare **Annulla** per un giorno.

Un’attività utile solo fino a un certo momento, come una conferma da inviare prima di una riunione, si chiude da sola dopo quell’ora. Viene spostata in **Fatte / scartate** con la dicitura «Non serve più». Puoi usare **Annulla** per un giorno.

Prima che un messaggio o un passaggio di consegne per qualcuno risulti pronto, la tua Machine controlla le chat recenti che hai avuto con le persone coinvolte, comprese quelle di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che la questione è già risolta, per esempio perché qualcuno ha fatto la richiesta e ha ricevuto un sì, l’attività si chiude da sola. Puoi usare **Annulla** per un giorno.

Se qualcun altro scrive nella stessa conversazione dopo la preparazione della bozza, **Invia** la mette in pausa: «Non inviata: nuovo messaggio nella conversazione». L’attività mostra quel messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per inviare la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna le attività da sola. Se un’attività è ancora utile, segue i nuovi piani. Se non resta più nulla da fare, viene spostata in **Fatte / scartate** con la dicitura «Non serve». Nella chat compare «Aggiornamento:» seguito dal motivo. Puoi usare **Annulla** per un giorno.

Sulle prime attività, un breve suggerimento mostra le azioni principali: **Chiedi modifiche** e **Non serve**, e ti ricorda che non parte nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il relativo pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un messaggio di benvenuto che indica chi aspetta da più tempo una tua risposta. La bozza di quella risposta viene preparata per prima, così è pronta al tuo arrivo.

Ogni attività inizia con il titolo. La riga sotto indica a chi si riferisce, l’organizzazione se pertinente, il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

I nomi e le organizzazioni mostrano la foto o il logo, se disponibile nel Graph, altrimenti le iniziali. Se un logo non si legge bene in piccolo, per esempio perché è bianco su sfondo trasparente o è un marchio largo, viene mostrata anche l’iniziale.

A volte una riga discreta segnala cosa non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessuna novità da allora». Compare quando l’ultimo scambio è vecchio o senza risposta e indica i canali non collegati, come WhatsApp. La tua Machine dice cosa non sa invece di tirare a indovinare.

Se viene indicato un canale non collegato, **Connetti** accanto al suo nome apre la relativa connessione.

Il titolo indica cosa c’è da fare e cambia solo se cambia l’attività. Un’attività completata mantiene il suo titolo e mostra sotto come si è conclusa, per esempio «Fatto: Sam l’ha firmato martedì».

Sopra la bozza, una riga in grigio chiaro indica il messaggio da cui proviene, insieme al logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo del servizio a cui verrà inviata, così capisci subito se è una risposta Slack o un’email.

Se la bozza si basa su un contributo ricevuto altrove, per esempio il suggerimento di un collega su Slack, una riga lo indica, per esempio «In base al messaggio di Sam in #ops». Tocca la riga per leggere il messaggio. Se la bozza viene sostituita da un aggiornamento, il messaggio non viene inviato.

Una chat (Slack, WhatsApp, Telegram, Intercom…) viene mostrata come un’unica conversazione, dalla più vecchia alla più recente: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal, i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e si apre nella conversazione. **Mostra messaggi precedenti** aggiunge quelli più vecchi. Le altre email della conversazione vengono raccolte sopra e sotto quella selezionata.

Un messaggio si apre allo stesso modo dalla ricerca, dal Graph, dalle risposte di Ask o dall’ultimo controllo. È contrassegnato con «Questo messaggio» o «Nuovi messaggi».

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android, se hai l’app Gmail, la apre direttamente.

I **Dettagli** di un’email mostrano solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, i destinatari in Ccn o un indirizzo di risposta diverso. Se non c’è altro da mostrare, la sezione non compare.

Una risposta in un thread Slack mostra anche cosa è stato detto prima dell’inizio del thread. Puoi aprire qui anche il link al messaggio dell’attività, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area, che puoi modificare toccandoli, l’ultima nota e il risultato di un agente di programmazione. Il titolo apre la chat. Un’attività completata resta breve; il messaggio da cui proviene è in **Dettagli**.

Un’attività in attesa di qualcuno include il link al tuo ultimo messaggio a quella persona, quello a cui aspetti risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** al computer, con **+** sul telefono o con `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, viene assegnata all’area giusta in base alla persona e all’argomento. Trova anche l’email a cui fa seguito, comprese quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore». Puoi scriverlo anche nella tua lingua. L’icona del calendario mostra le opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività torna a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, per esempio un’email, un messaggio Slack, Teams, WhatsApp, Telegram o un altro messaggio disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, chi l’ha inviato e quando.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, usa la fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungi file](card-chat.md#add-files)). × rimuove un file.

I file restano allegati all’attività e la tua Machine li legge mentre ci lavora. Puoi aggiungere solo i file: la tua Machine crea l’attività a partire da un PDF o da un file di testo. Una foto viene mostrata come immagine in miniatura. Tocca l’immagine per vederla a grandezza naturale.
