---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via libera. Scopri il significato delle varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 84b8879d98f26aa2
---
La tua Machine legge tutto ciò che arriva e crea un’attività solo quando serve il tuo intervento. Una sola attività per ogni questione, anche se riguarda molti messaggi.

## Dove trovi le attività

La pagina **Attività** le organizza così:

- **Appena fatto**: in cima, mostra un ultimo passaggio che hai confermato, come l’invio di un modulo o la risoluzione di un problema mentre non c’eri. Resta qui finché non tocchi **Ho capito**, al massimo per un giorno, e ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che è in attesa di una tua risposta o decisione, a partire dalle attività più urgenti. Ognuna indica **Preparata** (il lavoro è pronto e **Fallo** o **Invia** lo completano), **Serve il tuo intervento** (prima serve una tua decisione o risposta), **In preparazione…** (la tua Machine ci sta lavorando) o **Da leggere** (un riepilogo o un breve resoconto, senza decisioni da prendere).
- **Meno recenti**: attività raccolte in una sezione chiusa, senza novità da una settimana (vedi sotto).
- **In attesa di altri**: attività raccolte in una sezione chiusa, in cui il prossimo passaggio spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: ciò che hai promesso e ciò che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatta 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviato. Spostata tra le attività fatte.» o «Inviato. Spostata tra quelle per più tardi fino a lunedì». Una risposta che si limita a promettere di fare il lavoro, come «Te lo mando entro martedì», lascia aperta l’attività: «Inviato. Attività ancora aperta». **Apri** ti porta all’attività. La ricerca trova un’attività in base al titolo o al destinatario, anche tra quelle per più tardi e quelle fatte.

In **Per te** vengono prima le attività scadute o in scadenza entro domani, poi le domande della tua Fleet, quindi i promemoria di una bacheca e infine tutte le altre. All’interno di ogni gruppo, le più recenti vengono prima. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e quando viene completata: cambia solo il contrassegno. Negli altri gruppi aperti, vengono prima le attività scadute o in scadenza entro domani, poi le altre, dalla più recente. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** indica che la tua Machine vede l’attività come completata, per esempio «PR #3451 unita», ma non è ancora chiusa. **Riapri** la rimette nell’elenco e permette alla tua Machine di imparare. Queste attività non risultano mai in ritardo. Dopo un giorno si chiudono da sole e puoi usare **Annulla**. Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola.

Se un messaggio arriva da un indirizzo che somiglia a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo segnala chiaramente: «Non è Sam Lee». Mostra la persona con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica **In attesa di:** quel passaggio. Resta in **In attesa di altri**, nella sezione chiusa sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso vale dopo che hai fatto una domanda: l’attività ricompare la mattina prima della scadenza, alla scadenza se è più tardi in giornata oppure la mattina successiva se la scadenza è già passata. Indica anche chi deve ancora rispondere.

Quando un’attività riguarda un risultato che deve fornire qualcun altro, per esempio un contratto firmato, in **Dettagli** trovi **Fatto quando**. Inviare la tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola e puoi usare **Annulla**. Se non arriva nulla entro il momento in cui devi sollecitare, l’attività ricompare con **Scrivi un breve sollecito** nella chat. Per modificare cosa conta come completamento, spiegalo nella chat.

Un’attività senza novità da una settimana passa da Per te a **Meno recenti**, così quando torni dopo qualche giorno trovi prima quelle nuove. Per novità si intende un nuovo messaggio sull’attività o un’azione che hai fatto, come un messaggio in chat, una modifica o un posticipo. Aprirla e basta non conta.

Le attività urgenti, quelle in scadenza a breve e quelle con un invio in corso restano in Per te. **Scarta tutto** contrassegna come non necessarie tutte le attività in Meno recenti dopo una sola conferma, proprio come fa **Non serve** per una singola attività. Puoi usare **Annulla**. Se arriva una novità, l’attività torna in Per te.

Se nessuno interviene su un’attività per una settimana, compare una volta la domanda **Serve ancora?**. **Non serve** la chiude; puoi usare **Annulla**. **Tieni** la mantiene aperta e la domanda non compare più. Se non rispondi per un’altra settimana, l’attività passa nella sezione Torna più tardi e non viene più conteggiata sul numero dell’icona dell’app né nel riepilogo del mattino. Aprirla, inviare un messaggio in chat, modificarla, posticiparla o ricevere un nuovo messaggio la riporta nell’elenco.

Una volta a settimana, un progetto rimasto inattivo e senza attività aperte può generare un’attività con un prossimo passaggio preciso, al massimo tre volte a settimana. Vedi [Progetti](projects.md).

Quando niente richiede il tuo intervento, la tua Machine fa un pisolino e mostra un elenco vuoto. Mentre controlla, si risveglia e te lo segnala. Se un controllo non è riuscito o è in ritardo, lo indica con **Controlla ora** sotto.

I filtri **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. La scelta è la stessa sul telefono e sul computer. Se è attivo il filtro Lavoro o Personale, **Mostra tutto** torna a mostrare ogni attività. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo sotto Tutti.

La riga in cima all’elenco permette anche di passare direttamente all’altro filtro: se è attivo **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il nome dell’ultimo riepilogo del mattino o della sera e cosa conteggia, per esempio **Riepilogo di ieri sera** · 12 completate, 3 aperte. Tocca la riga per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, resta su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non c’è un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per il filtro selezionato.

Le attività di un progetto mostrano il nome del progetto sotto il titolo. Toccalo per aprire il progetto. In **Dettagli**, **Progetto** permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

In **Dettagli**, **Area** sposta un’attività nell’altra area. Anche i messaggi che può leggere e da cui può inviare si spostano con lei. **Annulla** nella nota la riporta dov’era.

Quando un’attività deve passare all’altra area e tutti i messaggi da cui proviene si trovano lì, si sposta da sola e prosegue. Altrimenti compare **Sposta in Lavoro** e non si sposta nulla finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola nell’area corretta quando trova dove appartiene. Fino ad allora non è assegnata né a Lavoro né a Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi nell’altra area, te lo chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai etichettato come Personale viene considerata Personale. Le email per le altre tue aziende finiscono nelle attività di quelle aziende; un’attività sulla tua vita privata, per esempio un messaggio di famiglia arrivato al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, per esempio un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. Lavoro e Personale determinano dove compare l’attività e con chi viene condivisa, non dove risponde: la risposta va sempre nella conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Anche un’attività Personale di questo tipo risponde dall’indirizzo di lavoro a cui è arrivata la sua email e non compare mai in una Fleet di lavoro né nel Team Graph.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. Sotto il titolo, l’intestazione indica anche quanto tempo serve al tuo ritmo, per esempio «circa 2 min».

Le attività che ti fanno una domanda non vengono incluse: richiedono una risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i messaggi ricevuti quando ce ne sono 40 in attesa o quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, la sezione dei controlli mostra «In pausa per la notte. Recupero alle 06:30». Se di notte fai clic, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla e usare **Dettagli**, che apre i controlli in Connessioni. Se hai attività aperte, la trovi in cima sul computer. Una breve riga compare solo mentre è in corso un controllo o quando uno non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga con i risultati di tutte le fonti controllate, per esempio «Controllati 13 messaggi alle 16:11 · niente richiede il tuo intervento» oppure «· 2 nuove attività». Se una nuova attività viene messa in attesa di un momento migliore, per esempio il riepilogo del mattino, la riga indica fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni thread email, chat e notifica con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività o il motivo per cui non serviva fare nulla, per esempio «In copia, risponde un collega» o «Riunione già fissata per giovedì». Un thread non mostra il motivo se il controllo ne ha indicato uno vago. Toccalo per leggerlo.

Vengono mostrati i primi 10 risultati; tocca sotto per vedere gli altri. Un numero dopo un nome, come (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già nell’elenco compare una sola volta. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email indirizzate a te. Le tue risposte vengono lette per capire il contesto e le promesse, ma non sono considerate nuove email. Le email che la tua Machine ti invia, come il riepilogo del mattino o un avviso su una correzione, non vengono mai lette né elencate. Le email sulla fatturazione, la prova o un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il passaggio successivo, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** permette di specificare cosa cambiare: come svolgere l’attività oppure, quando una bozza è pronta, cosa modificarvi. **Segna come fatto** indica che l’attività è stata gestita: è visibile su un’attività pronta senza bozza, altrimenti in cima a **…**, anche su un’attività che richiede una tua decisione. La rimuove subito dall’elenco; puoi usare **Annulla** nel messaggio. Scorri il messaggio per chiuderlo oppure trascinalo fuori con il mouse. La modifica resta.

Per far svolgere l’attività in un altro modo, scrivilo nella sua **Chat**.

In **…**:

- **Passa…**: affidala a un collega, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: [tornerà a intervalli regolari](recurring.md).
- **Non serve**: l’attività viene rimossa. Puoi anche indicare il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara da questa scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominarla, oppure chiedilo nella chat, per esempio «Rinominala …». Il titolo scelto resta invariato.

**Riapri** ripristina un’attività chiusa. L’attività torna anche da sola quando succede qualcosa di nuovo, per esempio un nuovo messaggio da quella persona, ma non quando invii tu una risposta. Mostra la data in cui è tornata e viene ordinata come nuova. La chat riprende da dove si era interrotta, anche dopo settimane.

Una fattura che devi pagare di persona, da qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dati di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con addebito diretto o una carta registrata, non diventano attività. Quando un’email successiva conferma il pagamento, per esempio con un messaggio del mittente che conferma di averlo ricevuto, l’attività si chiude da sola. **Annulla** la ripristina per un giorno.

Un’attività che serve solo fino a un momento preciso, come una conferma prima di una riunione, si chiude da sola dopo quell’ora. Passa in **Fatte / scartate** con la dicitura «Non serve più». **Annulla** la ripristina per un giorno.

Prima che un messaggio o un passaggio a qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, incluse le chat di gruppo, e aspetta che Slack finisca di leggerle. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché è stata fatta una richiesta e la risposta è stata affermativa, l’attività si chiude da sola. **Annulla** la ripristina per un giorno.

Se un messaggio più recente cambia i piani, per esempio una festa si sposta in un’altra sede o una prenotazione viene annullata, The Machine aggiorna da sola le attività. Quelle ancora utili seguono i nuovi piani. Quelle che non richiedono più alcuna azione passano in **Fatte / scartate** con la dicitura «Non serve»; nella chat compare «Aggiornamento:» con il motivo e puoi usare **Annulla** per un giorno.

Nelle prime attività compare un breve suggerimento con le azioni principali: **Chiedi modifiche** e **Non serve**, e ti ricorda che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il relativo pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica a chi si riferisce, l’organizzazione se pertinente (non solo perché la persona ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se il Graph ha una foto o un logo, vengono mostrati; altrimenti compaiono le iniziali. Se un logo non è leggibile a queste dimensioni, per esempio perché è bianco su sfondo trasparente o è un marchio molto largo, viene mostrata anche l’iniziale.

A volte una riga discreta segnala ciò che non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessun aggiornamento da allora». Compare quando l’ultimo contatto con la persona è lontano o senza risposta e indica i canali non collegati, come WhatsApp. La tua Machine dichiara ciò che non sa invece di tirare a indovinare.

Quando viene indicato un canale non collegato, tocca **Connetti** accanto al suo nome per aprire la relativa connessione.

Il titolo indica cosa va fatto e cambia solo se cambia l’attività. Un’attività completata mantiene il proprio titolo, con sotto l’esito, per esempio «Fatta: Sam l’ha firmato martedì».

Una riga in grigio sopra la bozza indica il messaggio da cui proviene, insieme al logo del servizio. Toccalo per leggere il thread. La bozza mostra il logo della destinazione, così capisci subito se si tratta di una risposta Slack o di un’email.

Se la bozza tiene conto di un contributo dato altrove, per esempio il suggerimento di un collega su Slack, una riga lo indica, per esempio «Basata sul messaggio di Sam in #ops». Tocca la riga per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) viene mostrata come un’unica conversazione, dalla più vecchia alla più recente: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal, i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e si apre direttamente nella conversazione. **Mostra messaggi precedenti** aggiunge quelli più vecchi. In un’email, il resto del thread è raccolto sopra e sotto il messaggio.

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android, se hai l’app Gmail, la apre lì.

In **Dettagli** di un’email compaiono solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, Bcc o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, la sezione non compare.

Una risposta in un thread Slack mostra anche cosa è stato detto prima dell’inizio del thread. Anche il link dell’attività al messaggio originale apre la conversazione qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area (tocca uno di questi elementi per modificarlo), la tua ultima nota e il risultato di un agente di programmazione. Il titolo apre la chat. Le attività completate restano concise; il messaggio da cui provengono si trova in **Dettagli**.

Un’attività in attesa di qualcuno collega il tuo ultimo messaggio a quella persona, quello a cui stai aspettando risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non scegli **Lavoro** o **Personale**, l’attività viene assegnata all’area corretta in base alla persona e all’argomento. La tua Machine individua anche l’email a cui si riferisce, comprese quelle meno recenti.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore», anche nella tua lingua. L’icona del calendario mostra alcune opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività torna a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio pertinente, per esempio un’email, un messaggio Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, chi l’ha inviato e quando.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file sul modulo. Sul telefono, la fotocamera accanto alla graffetta scatta una foto. Puoi aggiungere fino a 5 file, come in chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuoverne uno.

I file restano associati all’attività e The Machine li legge mentre ci lavora. Puoi aggiungere anche solo i file: The Machine crea l’attività a partire da un PDF o da un file di testo. Le foto vengono mostrate come immagini piccole; toccane una per vederla a grandezza naturale.
