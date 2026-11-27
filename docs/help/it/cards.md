---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via libera. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: dfbc7ccc7313ecfe
---
La tua Machine legge tutto ciò che arriva e crea un’attività solo quando serve il tuo intervento. Una sola attività per ogni questione, anche se riguarda molti messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in cima trovi un ultimo passaggio che hai confermato, per esempio l’invio di un modulo o la risoluzione di un problema mentre non c’eri. Resta lì finché non tocchi **Ho capito**, per un giorno al massimo. Ricevi una notifica anche sul telefono.
- **Per te**: tutto quello che aspetta il tuo intervento, prima le attività in scadenza entro domani. Ognuna indica **Preparata** (una bozza o un risultato è pronto e **Fallo** o **Invia** lo rende effettivo), **Serve il tuo intervento** (prima serve una tua decisione o una risposta; se il lavoro non può proseguire o essere usato senza qualcosa che solo tu puoi dare, come un prezzo, un dato o una scelta, una riga sotto il titolo spiega cosa manca), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un breve aggiornamento, senza decisioni da prendere).
- **Più vecchie**: attività senza novità da una settimana, raccolte in una sezione chiusa (vedi sotto).
- **In attesa di altri**: attività in cui il prossimo passo spetta a qualcun altro, raccolte in una sezione chiusa (vedi sotto).
- **Torna più tardi**: attività posticipate, messaggi [programmati per dopo](send-later.md) e attività senza risposta alla domanda **Serve ancora?** (vedi sotto).
- **Promesse**: quello che hai promesso e quello che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatto 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviata. Spostata tra le attività fatte.» oppure «Inviata. Spostata tra quelle da riprendere lunedì». Se la risposta si limita a promettere che il lavoro sarà fatto, per esempio «Te lo mando entro martedì», l’attività resta aperta: «Inviata. Lasciata aperta». **Apri** ti porta all’attività. La ricerca trova un’attività per titolo o per destinatario, anche tra quelle da riprendere e quelle fatte.

In **Per te** trovi prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, i promemoria di una bacheca e infine il resto. All’interno di ogni gruppo, le più recenti sono in cima. Un’attività resta nello stesso posto mentre la tua Machine la prepara e quando è fatta: cambia solo la sua indicazione. Negli altri gruppi aperti, prima compaiono quelle scadute o in scadenza entro domani, poi le altre dalla più recente. Anche la barra laterale mantiene lo stesso ordine.

**Sembra fatto** indica che la tua Machine vede che l’attività è stata completata, per esempio «PR #3451 unito», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e aiuta la tua Machine a imparare. Queste attività non risultano mai in ritardo. Se compare in un messaggio, si chiude da sola dopo un giorno e puoi usare **Annulla**. Altrimenti resta in attesa che tu selezioni **Segna come fatto**.

Anche un’attività che hai già gestito, per esempio rispondendo in Gmail o Slack, si chiude da sola. Una risposta che dice che un file è allegato quando invece non lo è, non la chiude.

Se un messaggio proviene da un indirizzo che assomiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Questa persona non è Sam Lee». La persona viene mostrata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona associata all’indirizzo che hai già, mai con chi ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica il passaggio con **In attesa di:**. Si trova in **In attesa di altri**, in una sezione chiusa sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso vale dopo che hai fatto una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è più tardi nella stessa giornata, oppure la mattina successiva se la scadenza è passata. Indica anche chi deve ancora rispondere.

Se l’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, **Dettagli** lo indica come **Fatto quando**. L’invio della tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non mostra il risultato. A quel punto si chiude da sola e puoi usare **Annulla**. Se non arriva nulla entro il momento in cui è ora di sollecitare, l’attività torna con **Scrivi un breve sollecito** nella chat. Per cambiare i criteri di completamento, scrivilo nella chat.

Se il risultato apparirà su una pagina web pubblica indicata nei messaggi, per esempio un articolo in cui comparirai, la tua Machine controlla quella pagina quando è ora di sollecitare. Se il risultato compare e non era presente quando l’attività è passata in attesa, l’attività si chiude da sola e indica il risultato. Puoi usare **Annulla**. La tua Machine legge solo la pagina, come farebbe chiunque, e non invia nulla.

Se il risultato non compare e la scadenza è ancora lontana, la tua Machine controlla la pagina un’altra volta la mattina successiva alla scadenza. Altrimenti l’attività torna come prima, con l’indicazione «Controllata» o «Impossibile aprire» e la pagina nella chat.

Un’attività senza novità da una settimana passa da Per te a **Più vecchie**, così al tuo ritorno dopo qualche giorno trovi prima quelle nuove. Per novità si intende un nuovo messaggio sull’attività o qualcosa che hai fatto, come un messaggio in chat, una modifica o un rinvio. Aprirla e basta non conta.

Le attività urgenti, quelle in scadenza a breve e quelle con un invio in corso restano in Per te. **Scarta tutto** contrassegna tutte le attività in Più vecchie come non necessarie dopo una sola conferma, proprio come **Non serve** fa con una alla volta. Puoi usare **Annulla**. Se arriva una novità, l’attività torna in Per te.

Un’attività che nessuno ha toccato per una settimana chiede una volta: **Serve ancora?** **Non serve** la chiude. Puoi usare **Annulla**. **Tieni** la mantiene aperta e la domanda non viene ripetuta. Se non rispondi per un’altra settimana, l’attività passa a Torna più tardi e non viene più conteggiata sul badge dell’app né nel riepilogo del mattino. Se la apri, invii un messaggio in chat, la modifichi o la rinvii, oppure se arriva un nuovo messaggio, torna nell’elenco.

Una volta a settimana, un progetto che non registra attività e non ha elementi aperti può ricevere un’attività con un solo prossimo passo concreto, fino a un massimo di tre alla settimana. Vedi [Progetti](projects.md).

Quando nulla richiede il tuo intervento, la tua Machine riposa e l’elenco resta vuoto. Mentre controlla, si riattiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, la riga lo indica e sotto compare **Controlla ora**.

Le opzioni **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer viene applicata la stessa selezione. Quando è attivo Lavoro o Personale, **Mostra tutto** torna alla vista completa. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima all’elenco passa direttamente all’altra vista: da **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco indica l’ultimo riepilogo del mattino o della sera e cosa conteggia, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Tocca la riga per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, resta visibile su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non c’è un riepilogo recente, compare **Oggi finora**: ciò che è stato fatto oggi e ciò che è ancora aperto, per Lavoro e Personale oppure solo per la vista selezionata.

Un’attività associata a un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. Da **Progetto** sotto **Dettagli** puoi modificarlo o rimuovere l’associazione. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

Da **Area** sotto **Dettagli** puoi spostare un’attività nell’altra area. Anche le fonti che può leggere e da cui può inviare si spostano con lei. **Annulla** nella notifica la riporta dov’era.

Se un’attività ha bisogno dell’altra area per proseguire e tutti i messaggi da cui proviene si trovano lì, si sposta da sola e continua. Altrimenti compare **Sposta in Lavoro** e non si sposta nulla finché non lo tocchi. Un’attività che hai creato senza scegliere Lavoro o Personale si sposta da sola quando trova la sua area. Fino ad allora non appartiene né a Lavoro né a Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai etichettato come Personale viene considerata personale. Le email destinate a un’altra delle tue aziende finiscono nelle attività di quell’azienda. Un’attività sulla tua vita privata, per esempio un messaggio di famiglia al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che arriva su un account personale, per esempio un cliente su WhatsApp, un ordine nella tua casella personale o una [promessa](promises.md) di lavoro, è Lavoro fin dall’inizio.

Un’attività che hai spostato o assegnato a un’area resta sempre dove l’hai messa. Lavoro o Personale determina dove compare un’attività e con chi viene condivisa, mai dove invia la risposta: questa va sempre nella conversazione d’origine, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Anche un’attività Personale di questo tipo risponde dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro o nel Graph del team.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te ti permette di passarle in rassegna una alla volta, nell’ordine dell’elenco, con ogni bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. L’intestazione indica quanto tempo ci vuole al tuo ritmo, per esempio «circa 2 min».

Alla fine mostra quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Un’attività che ti fa una domanda non viene inclusa: richiede una risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa oppure quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, da 00:00 a 06:30, i controlli si fermano. I nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, la sezione Controlli mostra «In pausa per la notte, recupero alle 06:30». Se di notte clicchi, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non ti allontani per un’ora. **Controlla ora** esegue sempre un controllo immediato.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla, con **Dettagli**, che apre Controlli in Connessioni. Se hai attività aperte, l’opzione si trova in cima alla pagina sul computer. Una breve riga compare solo mentre è in corso un controllo o quando uno non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, una riga sopra le attività indica cosa ha trovato tra tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». Si riferisce solo a quel controllo: le attività già nell’elenco restano invariate. Se una nuova attività resta in attesa di un momento più adatto, per esempio il riepilogo del mattino, la riga indica fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica, con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole, e la nuova attività oppure il motivo per cui non serviva fare nulla, per esempio «Solo in Cc, risponde un collega» o «Riunione già fissata per giovedì». Una conversazione non mostra il motivo se il controllo ne ha dato uno generico. Tocca un elemento per leggerlo, insieme ai messaggi vicini.

Vengono mostrati i primi 10 elementi. Tocca sotto per vedere gli altri. Il numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica Android relativa a un messaggio già presente nell’elenco compare una volta sola. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email che hai ricevuto. Le tue risposte vengono lette per ricostruire il contesto e le promesse, ma non sono considerate nuove email. Le email della tua Machine, per esempio il riepilogo del mattino o un avviso di correzione, non vengono mai lette né mostrate nell’elenco. Le email relative alla fatturazione, alla prova o a un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passo, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** ti permette di specificare cosa cambiare: come svolgere l’attività oppure, quando una bozza è pronta, cosa modificare nella bozza. Se lasci il testo a metà, lo ritrovi quando torni. **Annulla** lo elimina.

**Segna come fatto** indica che l’attività è stata gestita. Sul computer compare accanto agli altri pulsanti quando c’è spazio su una riga. Sul telefono è visibile per le attività pronte senza bozza o per quelle che ti fanno una domanda; altrimenti si trova in cima al menu **…**. L’attività scompare subito dall’elenco e nel messaggio compare **Annulla**. Scorri il messaggio per chiuderlo oppure trascinalo fuori con il mouse. La modifica viene mantenuta.

Per completarla in un altro modo, scrivilo nella sua **Chat**. La risposta indica solo cosa è cambiato, per esempio il rinvio e fino a quando. Se non è stato possibile modificare qualcosa, come una scadenza, te lo dice.

Nel menu **…**:

- **Passa…**: affidala a un collega, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: l’attività [torna con una certa frequenza](recurring.md).
- **Non serve**: l’attività viene rimossa. Se vuoi, puoi scegliere un motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara da questa scelta.

Tocca il titolo o **Nome** sotto **Dettagli** per rinominarla. Puoi anche chiederlo nella chat, per esempio «Rinominala …». Il titolo scelto resta invariato.

**Riapri** riporta nell’elenco un’attività chiusa. Può riapparire anche da sola quando succede qualcosa di nuovo, per esempio quando arriva un nuovo messaggio da quella persona, ma non per una tua risposta. In quel caso indica quando è tornata e viene ordinata come nuova. La chat continua da dove si era interrotta, anche dopo settimane.

Una fattura che devi pagare tu, da qualunque paese provenga, diventa un’attività con l’importo, la scadenza e i dati di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta registrata, non diventano attività. Quando un’email successiva conferma il pagamento, per esempio il mittente conferma di averlo ricevuto, l’attività si chiude da sola. Puoi usare **Annulla** per un giorno.

Un’attività che serve solo fino a un momento preciso, per esempio una conferma da inviare prima di una riunione, si chiude da sola dopo quell’ora. Passa a **Fatte / scartate** con la dicitura «Non serve più». Puoi usare **Annulla** per un giorno.

Prima che un messaggio o un passaggio destinato a qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, comprese quelle di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che è già tutto fatto, per esempio perché qualcuno ha chiesto e ha ricevuto un sì, l’attività si chiude da sola. Puoi usare **Annulla** per un giorno.

Se qualcun altro scrive nella stessa conversazione dopo la creazione della bozza, **Invia** la mette in attesa: «Non inviata: nuovo messaggio nella conversazione». L’attività mostra quel messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per spedire la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna le attività da sola. Quelle ancora utili seguono i nuovi piani. Quelle che non richiedono più alcun intervento passano a **Fatte / scartate** con la dicitura «Non serve». Nella chat compare «Aggiornamento:» seguito dal motivo. Puoi usare **Annulla** per un giorno.

Nelle prime attività compare un breve suggerimento sulle azioni principali: **Chiedi modifiche** e **Non serve**. Ti ricorda anche che nulla viene inviato finché non premi **Invia**. Il suggerimento scompare definitivamente dopo che usi il pulsante o premi ×.

Il primo giorno, in cima alla pagina Attività compare un saluto e il nome della persona che aspetta da più tempo una tua risposta. La bozza di quella risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica di chi si tratta, l’organizzazione se è pertinente (non solo perché qualcuno ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se nel Graph sono disponibili, il nome e l’organizzazione mostrano la foto o il logo. Altrimenti mostrano le iniziali. Se un logo non si leggerebbe a quella dimensione, per esempio perché è bianco su sfondo trasparente o è una scritta molto larga, viene mostrata anche l’iniziale.

A volte una riga discreta indica ciò che non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessuna novità». Compare quando l’ultimo contatto risale a molto tempo fa o non ha ricevuto risposta e indica i canali non collegati, come WhatsApp. La tua Machine dice ciò che non sa invece di tirare a indovinare.

Quando viene indicato un canale non collegato, tocca **Connetti** accanto al suo nome per collegarlo.

Il titolo indica cosa bisogna fare e cambia solo se cambia l’attività. Un’attività completata mantiene il suo titolo e indica sotto come si è conclusa, per esempio «Fatto: Sam ha firmato martedì».

Sopra la bozza, una riga in grigio indica il messaggio da cui proviene, con il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo della destinazione, così capisci subito se si tratta di una risposta su Slack o di un’email.

Se la bozza tiene conto di un contributo ricevuto altrove, per esempio il suggerimento di un collega su Slack, una riga lo indica, per esempio «Basata sul messaggio di Sam in #ops». Tocca la riga per leggere il messaggio. La bozza viene sostituita quando arriva un aggiornamento.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra una conversazione unica, dalla più vecchia alla più recente: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal, i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e viene aperto direttamente. **Mostra messaggi precedenti** aggiunge quelli più vecchi. In un’email, il resto della conversazione è raccolto in sezioni chiuse sopra e sotto il messaggio.

Puoi aprire un messaggio anche dalla ricerca, dal Graph, dalle risposte di Ask o dall’ultimo controllo. È contrassegnato con «Questo messaggio» oppure «Nuovi messaggi».

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android, se hai l’app Gmail, l’email si apre lì.

**Dettagli** di un’email mostra solo le informazioni che non compaiono nell’intestazione, come gli indirizzi completi in Cc, quelli in Ccn o un indirizzo diverso per le risposte. Se non c’è altro da aggiungere, non compare nulla.

Una risposta in un thread di Slack mostra anche cosa è stato detto prima dell’inizio del thread. Anche il link dell’attività al messaggio originale lo apre qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area (tocca un elemento per modificarlo), la tua ultima nota e il risultato di un agente di programmazione. Tocca il titolo per aprire la chat. Un’attività completata resta breve; il messaggio da cui proviene si trova sotto **Dettagli**.

Un’attività «In attesa di» collega il tuo ultimo messaggio a quella persona, quello di cui aspetti una risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) aggiunge un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, l’attività viene assegnata all’area giusta in base a chi e a cosa riguarda. Trova anche l’email a cui si riferisce, comprese quelle più vecchie.

Se chiudi il modulo prima di aggiungere l’attività, il testo e le scelte restano disponibili la volta successiva. I file, invece, no. **Scarta** nel messaggio li elimina.

- **Scadenza**: scrivi un giorno o un orario, per esempio «domani», «venerdì prossimo», «3 nov», «14:00» o «tra 2 ore». Puoi scriverlo anche nella tua lingua. L’icona del calendario offre alcune opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività torna con una certa frequenza. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, per esempio un’email, un messaggio su Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, il mittente e quando è stato inviato.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, tocca la fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano associati all’attività e la tua Machine li legge mentre ci lavora. Puoi aggiungere solo file: la tua Machine crea l’attività partendo da un PDF o da un file di testo. Le foto vengono mostrate come immagini piccole. Toccale per vederle a grandezza naturale.
