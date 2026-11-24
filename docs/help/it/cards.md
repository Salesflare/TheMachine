---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo ok. Ecco cosa significano le sue parti.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: f77d6b07f6f94ce5
---
La tua Machine legge tutto ciò che arriva e crea un’attività solo quando qualcosa richiede il tuo intervento. Un’attività per ogni questione, anche se coinvolge più messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in cima trovi l’ultimo passaggio che hai confermato, come l’invio di un modulo o la gestione di un problema, completato mentre non c’eri. Resta qui finché non tocchi **Ho capito**, per un giorno al massimo. Ricevi una notifica anche sul telefono.
- **Per te**: tutto quello che aspetta una tua risposta, con prima le cose in scadenza entro domani. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e puoi completare l’azione con **Fallo** o **Invia**), **Serve il tuo intervento** (prima serve una tua decisione o risposta; se il lavoro non può proseguire o essere usato senza qualcosa che solo tu puoi fornire, come un prezzo, un dato o una scelta, una riga sotto il titolo spiega cosa manca), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un briefing, senza decisioni da prendere).
- **Più vecchie**: attività senza novità da una settimana, raccolte in un gruppo chiuso (vedi sotto).
- **In attesa di altri**: attività in cui il prossimo passo spetta a qualcun altro, raccolte in un gruppo chiuso (vedi sotto).
- **Torna più tardi**: attività posticipate, messaggi [programmati per un momento successivo](send-later.md) e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: quello che hai promesso e quello che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatto 5 minuti fa». Quelle che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviato. Spostata in Fatte.» oppure «Inviato. Spostata in Più tardi fino a lunedì.» Se la risposta promette soltanto di svolgere il lavoro, per esempio «Te lo mando entro martedì», l’attività resta aperta: «Inviato. Lasciata aperta.» **Apri** ti porta all’attività. La ricerca trova un’attività per titolo o per destinatario, anche in Più tardi e Fatte.

In **Per te** trovi prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, i promemoria di una bacheca e infine tutto il resto. All’interno di ogni gruppo, le più recenti compaiono per prime. Un’attività resta nello stesso posto mentre la tua Machine la prepara e quando viene completata: cambia solo il contrassegno. Negli altri gruppi aperti, le attività scadute o in scadenza entro domani vengono prima; le altre sono in ordine dalla più recente. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che l’attività è completata, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nel tuo elenco e aiuta la tua Machine a imparare. Queste attività non risultano mai in ritardo. Se il contrassegno compare su un messaggio, l’attività si chiude da sola dopo un giorno e puoi usare **Annulla**. Altrimenti resta in attesa di **Segna come fatto**.

Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola. Una risposta che dice che un file è allegato quando invece non lo è, non la chiude.

Se un messaggio arriva da un indirizzo che assomiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo segnala chiaramente: «Questo non è Sam Lee». Mostra la persona con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio di una revisione o di una risposta, indica **In attesa di:** seguito dal passaggio. Si trova in **In attesa di altri**, nel gruppo chiuso sopra Torna più tardi, finché un nuovo messaggio non la riporta in primo piano. Succede anche dopo che hai fatto una domanda: riappare la mattina prima della scadenza, alla scadenza se è più tardi in giornata, oppure la mattina successiva se la scadenza è passata. Indica anche chi deve ancora rispondere.

Se l’attività riguarda un risultato che deve fornire qualcun altro, per esempio un contratto firmato, **Dettagli** lo indica in **Fatto quando**. Inviare la tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non mostra il risultato, poi si chiude da sola. Se non arriva nulla entro il momento in cui dovresti sollecitare, riappare con **Scrivi un breve sollecito** nella chat. Per cambiare cosa conta come completamento, spiegalo nella chat.

Un’attività senza novità da una settimana passa da Per te a **Più vecchie**, così dopo qualche giorno di assenza trovi prima le attività nuove. Per novità si intende un nuovo messaggio o un’azione che hai fatto sull’attività, come un messaggio in chat, una modifica o un posticipo. Aprirla e basta non conta.

Le attività urgenti, quelle in scadenza a breve e quelle con un invio in corso restano in Per te. **Scarta tutto** contrassegna tutte le attività in Più vecchie come non necessarie dopo una sola conferma, proprio come fa **Non serve** per una alla volta, con la possibilità di usare **Annulla**. Se arriva una novità, l’attività torna in Per te.

Se nessuno interviene su un’attività per una settimana, compare una sola volta la domanda **Serve ancora?**. **Non serve** la chiude, con la possibilità di usare **Annulla**. **Tieni** la mantiene e la domanda non compare più. Se non rispondi per un’altra settimana, l’attività passa in Torna più tardi e non viene più conteggiata nel numero sull’icona dell’app né nel riepilogo del mattino. Aprirla, inviare un messaggio in chat, modificarla, posticiparla o ricevere un nuovo messaggio la riporta in primo piano.

Una volta alla settimana, un progetto che si è fermato e non ha attività aperte può generare un’attività con un prossimo passo specifico, fino a un massimo di tre a settimana. Vedi [Progetti](projects.md).

Quando niente richiede il tuo intervento, la tua Machine si riposa e l’elenco resta vuoto. Mentre controlla, si risveglia e te lo segnala. Se un controllo non è riuscito o è in ritardo, una riga lo indica e mostra **Controlla ora**.

**Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Il telefono e il computer mostrano la stessa selezione. Quando hai selezionato Lavoro o Personale, **Mostra tutto** torna a tutte le attività. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima all’elenco permette anche di passare direttamente all’altra vista: con **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco mostra il nome dell’ultimo riepilogo del mattino o della sera e quante attività ha conteggiato, per esempio **Riepilogo di ieri sera** · 12 completate, 3 aperte. Tocca la riga per rileggere il riepilogo, poi usa **Copia** per copiarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, il riepilogo resta su tutti i tuoi dispositivi fino al successivo.

Se non c’è un riepilogo recente, compare **Oggi finora**: quello che è stato completato oggi e quello che è ancora aperto, per Lavoro e Personale oppure solo per la vista selezionata.

Un’attività collegata a un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. In **Dettagli**, **Progetto** permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

In **Dettagli**, **Area** sposta un’attività nell’altra area. Si spostano anche i messaggi che può leggere e inviare. Usa **Annulla** sulla nota per riportarla dov’era.

Quando un’attività può proseguire solo nell’altra area e tutti i messaggi da cui proviene si trovano lì, si sposta da sola e continua. Altrimenti mostra **Sposta in Lavoro** e non si sposta finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola nell’area corretta quando trova a quale appartiene. Fino ad allora non è contrassegnata né come Lavoro né come Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi nell’altra area, lo chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai contrassegnato come Personale viene considerata Personale. Le email destinate a un’altra delle tue aziende finiscono nelle attività di quell’azienda. Un’attività sulla tua vita privata, come un messaggio di famiglia arrivato al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp, un ordine nella casella personale o una [promessa](promises.md) di lavoro, è Lavoro fin dall’inizio.

Un’attività che hai spostato o assegnato a un’area resta sempre dove l’hai messa. Lavoro o Personale determina dove compare l’attività e con chi viene condivisa, non dove invia le risposte: queste vanno sempre nella conversazione di origine, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Anche un’attività Personale di questo tipo risponde dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro o nel Graph del team.

Se hai almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta e Esc interrompe. L’intestazione indica quanto ci vorrà al tuo ritmo, per esempio «circa 2 min».

Alla fine, un riepilogo indica quante attività sono state inviate o chiuse e quante sono ancora in preparazione.

Le attività che ti fanno una domanda non vengono incluse: aspettano una tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa oppure quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, da 00:00 a 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, la sezione dei controlli mostra «In pausa per la notte, recupera alle 06:30». Se di notte fai clic, digiti o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre un controllo immediato.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per visualizzarla insieme a **Dettagli**, che apre la sezione dei controlli in Connessioni. Se hai attività aperte, la trovi in cima alla pagina sul computer. Una breve riga compare solo mentre è in corso un controllo o quando un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri ritmi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga con i risultati di tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · nessuna attività nuova» oppure «· 2 attività nuove». Si riferisce solo a quel controllo: le attività già presenti nell’elenco restano in attesa. Se una nuova attività viene messa da parte per un momento più adatto, per esempio il riepilogo del mattino, la riga indica fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività o il motivo per cui non serviva intervenire, per esempio «Solo in Cc, risponde un collega» o «Riunione già fissata per giovedì». Se il controllo ha fornito solo un motivo generico, la conversazione non ne mostra uno. Tocca una voce per leggerla insieme ai messaggi che la circondano.

Vengono mostrate le prime 10 voci; toccando sotto, vedi le altre. Un numero accanto a un nome, come (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica del telefono relativa a un messaggio già nell’elenco compare una sola volta. La riga resta visibile per 12 ore dopo il controllo.

Viene conteggiata solo la posta indirizzata a te. Le tue risposte vengono lette per capire il contesto e le promesse, ma non sono considerate nuova posta. Le email che la tua Machine ti invia, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né mostrate. Le email sulla fatturazione, sulla prova o su un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passaggio, come **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** ti permette di specificare cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. Se lasci la richiesta a metà, la ritrovi al tuo ritorno; **Annulla** la elimina.

**Segna come fatto** indica che l’attività è stata gestita: è visibile su un’attività pronta senza bozza o su una che ti fa una domanda; altrimenti si trova in cima a **…**. L’attività scompare subito dall’elenco e puoi usare **Annulla** nel messaggio per ripristinarla. Scorri il messaggio per eliminarlo oppure trascinalo fuori con il mouse per chiuderlo subito. La modifica viene mantenuta.

Per completare l’attività in un altro modo, spiegalo nella sua **Chat**. La risposta indica solo cosa è cambiato, per esempio il posticipo e fino a quando. Se non è stato possibile modificare qualcosa, come la data di scadenza, te lo dice.

In **…**:

- **Passa…**: affidala a un collega, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di revisionarla](ask-to-review.md).
- **Ripeti…**: l’attività [si ripresenta a intervalli regolari](recurring.md).
- **Non serve**: l’attività scompare. Se vuoi, puoi indicare il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine ne tiene conto per imparare.

Tocca il titolo o **Nome** in **Dettagli** per rinominarla, oppure chiedilo nella chat, per esempio «Rinominala in …». Il titolo scelto resta invariato.

**Riapri** riporta un’attività chiusa tra quelle aperte. Può riapparire anche da sola quando succede qualcosa di nuovo, per esempio quando arriva un nuovo messaggio da quella persona, ma non in seguito a una tua risposta. In tal caso mostra quando è riapparsa e viene ordinata come nuova. La chat riprende da dove si era interrotta, anche dopo settimane.

Una fattura che devi pagare tu, di qualsiasi paese, diventa un’attività con l’importo, la data di scadenza e i dati di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta registrata, non diventano attività. Se un’email successiva conferma il pagamento, per esempio perché il mittente ti comunica di averlo ricevuto, l’attività si chiude da sola. Puoi usare **Annulla** per ripristinarla entro un giorno.

Un’attività utile solo fino a un momento preciso, come una conferma da inviare prima di una riunione, si chiude da sola allo scadere del tempo. Passa in **Fatte / scartate** con la dicitura «Non serve più». Puoi usare **Annulla** per ripristinarla entro un giorno.

Prima di mostrare come pronte un’attività o un passaggio per qualcun altro, la tua Machine controlla le chat recenti con le persone coinvolte, comprese quelle di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché qualcuno ha ricevuto una richiesta e ha risposto di sì, l’attività si chiude da sola. Puoi usare **Annulla** per ripristinarla entro un giorno.

Se qualcun altro scrive nella stessa conversazione dopo che è stata creata la bozza, **Invia** la mette in attesa: «Non inviato: nuovo messaggio nella conversazione». L’attività mostra quel messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per inviare la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna da sola le attività. Quelle ancora utili seguono i nuovi piani. Quelle che non richiedono più alcuna azione passano in **Fatte / scartate** con la dicitura «Non serve»; nella chat compare «Aggiornamento:» seguito dal motivo. Puoi usare **Annulla** per ripristinarle entro un giorno.

Alla prima visita delle attività, un breve suggerimento mostra le azioni principali: **Chiedi modifiche** e **Non serve**, e spiega che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il relativo pulsante o premi ×.

Il tuo primo giorno, in cima ad Attività compare un messaggio di benvenuto che indica chi aspetta da più tempo una tua risposta. La risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica a chi si riferisce, l’organizzazione se pertinente, il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se il Graph ha una foto o un logo, li mostra accanto al nome o all’organizzazione; altrimenti mostra le iniziali. Se un logo non si legge bene a dimensioni ridotte, per esempio perché è bianco su sfondo trasparente o ha una scritta molto larga, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessun aggiornamento da allora». Compare quando l’ultimo contatto con la persona è vecchio o non ha ricevuto risposta e indica i canali non collegati, come WhatsApp. La tua Machine dice cosa non sa, invece di tirare a indovinare.

Se viene indicato un canale non collegato, tocca **Connetti** accanto al suo nome per collegarlo.

Il titolo indica cosa bisogna fare e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo, con il modo in cui si è conclusa sotto di esso, per esempio «Fatto: Sam l’ha firmato martedì».

Sopra la bozza, una riga in grigio indica il messaggio da cui proviene e mostra il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo della destinazione, così vedi subito se è una risposta su Slack o un’email.

Se la bozza si basa sul contributo di qualcuno in un’altra conversazione, per esempio un suggerimento di un collega su Slack, una riga lo indica, per esempio «Basata sul messaggio di Sam in #ops». Tocca la riga per leggere il messaggio. La bozza viene sostituita quando arriva un aggiornamento.

Le chat (Slack, WhatsApp, Telegram, Intercom…) mostrano un’unica conversazione, dalla più vecchia alla più recente: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal, i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e si apre in vista. **Mostra messaggi precedenti** aggiunge i messaggi più vecchi. In un’email, il resto della conversazione è raccolto in gruppi chiusi sopra e sotto il messaggio.

Puoi aprire un messaggio nello stesso modo dalla ricerca, dal Graph, dalle risposte di Ask o dall’ultimo controllo. È contrassegnato con «Questo messaggio» oppure «Nuovi messaggi».

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android si apre nell’app Gmail, se è installata.

**Dettagli** di un’email mostra solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, Bcc o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, non mostra nulla.

Una risposta in un thread Slack mostra anche cosa è stato detto prima che iniziasse il thread. Anche il link di un’attività al messaggio di origine lo apre qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area, che puoi toccare per modificarli, la tua ultima nota e il risultato di un agente di programmazione. Il titolo apre la chat. Un’attività completata resta compatta; il messaggio da cui proviene si trova in **Dettagli**.

Un’attività «In attesa di» collega il tuo ultimo messaggio alla persona da cui aspetti una risposta, per esempio «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono oppure `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, l’attività viene assegnata all’area corretta in base a chi e a cosa riguarda. Trova anche l’email a cui dà seguito, comprese quelle meno recenti.

Se chiudi il modulo prima di aggiungere l’attività, il testo e le scelte restano disponibili la volta successiva; i file no. **Scarta** nel messaggio elimina tutto.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore», anche nella tua lingua. L’icona del calendario offre alcune opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività si ripresenta a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, per esempio un’email, un messaggio su Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio accessibile alla tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, chi l’ha inviato e quando.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file sul modulo. Sul telefono, la fotocamera accanto alla graffetta permette di scattare una foto. Puoi aggiungere fino a 5 file, come in chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuoverne uno.

I file restano associati all’attività e la tua Machine li legge mentre ci lavora. Puoi aggiungere anche solo dei file: la tua Machine compila l’attività usando un PDF o un file di testo. Una foto compare come immagine piccola: toccala per vederla a grandezza naturale.
