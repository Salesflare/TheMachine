---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via. Scopri cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 91b111b2d6f2a97b
---
La tua Machine legge tutte le novità e crea un’attività solo quando qualcosa richiede il tuo intervento. Un’attività per ogni questione, anche se riguarda molti messaggi.

## Dove si trovano le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in alto, l’ultimo passaggio che hai confermato, per esempio l’invio di un modulo o la risoluzione di un problema, è andato a buon fine mentre non c’eri. Rimane lì finché non tocchi **Ho capito**, per un giorno al massimo. Ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che è in attesa di te, prima le cose in scadenza entro domani. Ogni attività indica **Preparata** (una bozza o un risultato è pronto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima serve una tua decisione o risposta; se il lavoro non può proseguire o essere usato senza qualcosa che solo tu puoi fornire, come un prezzo, un dato o una scelta, una riga sotto il titolo lo spiega), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un brief, senza decisioni da prendere).
- **Più vecchie**: attività compattate, senza novità da una settimana (vedi sotto).
- **In attesa di altri**: attività compattate in cui il prossimo passo spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate, messaggi che [partono più tardi](send-later.md) e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: quelle che hai fatto e quelle che ti hanno fatto. Scopri di più in [Promesse](promises.md).
- **Fatte / scartate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatta 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviata. Spostata in Fatte.» o «Inviata. Spostata in Più tardi fino a lunedì». Se la risposta si limita a promettere di fare il lavoro, come «Te lo mando entro martedì», l’attività resta aperta: «Inviata. Lasciata aperta». **Apri** ti porta all’attività. La ricerca trova le attività per titolo o per destinatario, anche in Più tardi e Fatte.

In **Per te** vengono prima le attività scadute o in scadenza entro domani, poi le domande del tuo Fleet, quindi i promemoria di una bacheca e infine tutto il resto. All’interno di ogni gruppo, dalla più recente. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e anche quando è completata: cambia solo il contrassegno. Negli altri gruppi aperti vengono prima quelle scadute o in scadenza entro domani, poi le altre dalla più recente. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede l’attività come completata, per esempio «PR #3451 unito», ma non è ancora stata chiusa. **Riapri** la rimette nell’elenco e la tua Machine impara da questa scelta. Queste attività non risultano mai in ritardo. Se il messaggio lo indica, l’attività si chiude da sola dopo un giorno e puoi usare **Annulla**. Negli altri casi, aspetta che tu selezioni **Segna come fatto**.

Anche un’attività che hai già gestito da solo, per esempio rispondendo in Gmail o Slack, si chiude da sola. Una risposta che dice che un file è allegato quando non lo è non la chiude.

Se un messaggio arriva da un indirizzo che somiglia a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Questo non è Sam Lee». La persona viene mostrata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio di una revisione o di una risposta, indica il passaggio con **In attesa di:**. Rimane in **In attesa di altri**, compattata sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso vale dopo che hai risposto con una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è più tardi oggi, oppure la mattina successiva se la scadenza è passata. Indica anche chi deve ancora rispondere.

Quando un’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, **Dettagli** lo mostra sotto **Fatto quando**. Inviare la tua parte non chiude l’attività: rimane in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola. Se non arriva nulla entro il momento in cui è ora di sollecitare, l’attività torna con **Scrivi un breve sollecito** nella chat. Per cambiare cosa viene considerato completato, spiegalo nella chat.

Se per una settimana un’attività non riceve novità, passa da Per te a **Più vecchie**, così dopo qualche giorno di assenza trovi prima quelle nuove. Per novità si intende un nuovo messaggio o una tua azione, come un messaggio in chat, una modifica o un posticipo. Aprire un’attività non conta.

Le attività urgenti, quelle in scadenza a breve e quelle con un invio in corso restano in Per te. **Scarta tutto** contrassegna tutte le attività in Più vecchie come non necessarie dopo una sola conferma, proprio come fa **Non serve** una alla volta. Puoi annullare con **Annulla**. Una novità riporta l’attività in Per te.

Se nessuno tocca un’attività per una settimana, compare una sola volta la domanda **Serve ancora?**. **Non serve** la chiude, con la possibilità di annullare con **Annulla**. **Tieni** la mantiene e non te lo chiede più. Se non rispondi per un’altra settimana, l’attività viene compattata in Torna più tardi e non viene più conteggiata sul numero dell’icona dell’app né nel riepilogo mattutino. Aprirla, scrivere in chat, modificarla, posticiparla o ricevere un nuovo messaggio la riporta nell’elenco.

Una volta a settimana, un progetto inattivo e senza attività aperte può generare un’attività con un solo prossimo passo specifico, per un massimo di tre a settimana. Scopri di più in [Progetti](projects.md).

Quando niente richiede il tuo intervento, la tua Machine si riposa e l’elenco resta vuoto. Durante un controllo, si riattiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, una riga lo spiega e mostra **Controlla ora**.

Le opzioni **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer trovi la stessa selezione. Quando è attivo Lavoro o Personale, **Mostra tutto** torna alla vista completa. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo sotto Tutti.

La riga in cima all’elenco permette anche di passare direttamente all’altra vista: sotto **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima all’elenco indica il tuo ultimo riepilogo mattutino o serale e cosa contiene, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Toccala per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la **×**, il riepilogo rimane su tutti i tuoi dispositivi fino al successivo.

Se non hai un riepilogo recente, compare **Oggi finora**: cosa è stato fatto oggi e cosa è ancora aperto, per Lavoro e Personale o solo per la vista selezionata.

Un’attività di un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. **Progetto** sotto **Dettagli** permette di modificarlo o rimuoverlo. Scopri di più sulle [attività di un progetto](projects.md#a-project-s-to-dos).

**Area** sotto **Dettagli** sposta un’attività nell’altra area. Anche le fonti che può leggere e da cui può inviare si spostano con lei. **Annulla** nella nota la riporta dov’era.

Se per continuare un’attività serve l’altra area e tutti i messaggi da cui proviene sono lì, l’attività si sposta da sola e prosegue. Altrimenti compare **Sposta in Lavoro** e non viene spostato nulla finché non la tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola una volta individuata l’area giusta. Fino ad allora non appartiene a Lavoro né a Personale e rimane privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi nell’altra area, te lo chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai etichettato come Personale viene considerata Personale. Le email per un’altra delle tue aziende confluiscono nelle attività di quell’azienda. Un’attività sulla tua vita privata, per esempio un messaggio di famiglia al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp, un ordine nella tua casella personale o una [promessa](promises.md) di lavoro, è Lavoro fin dall’inizio.

Un’attività che hai spostato o assegnato tu rimane sempre dove l’hai messa. Lavoro o Personale stabilisce dove compare l’attività e con chi viene condivisa, mai da dove invia le risposte: una risposta parte sempre dalla conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un’altra modalità.

Anche se è Personale, l’attività risponde dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in un Fleet di lavoro né nel Graph del team.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, ciascuna con la bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta e Esc interrompe. L’intestazione indica quanto ci vuole al tuo ritmo, per esempio «circa 2 min».

Alla fine, il riepilogo indica cosa è stato inviato o chiuso e cosa è ancora in preparazione.

Un’attività che ti fa una domanda non viene inclusa in nessuno dei due casi: aspetta una tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa o quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si interrompono: i nuovi messaggi vengono comunque letti e salvati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo mattutino. In Controlli, sotto Connessioni, compare «Pausa notturna, recupero alle 06:30». Se di notte fai clic, digiti o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non ti allontani per un’ora. **Controlla ora** avvia sempre un controllo immediato.

**Controlla ora** legge subito tutte le fonti. Se non ci sono attività aperte, tocca la riga della tua Machine per vedere lo stato e **Dettagli**, che apre Controlli sotto Connessioni. Se ci sono attività aperte, l’opzione è in cima alla pagina sul computer. Una breve riga compare solo durante un controllo o se un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga che indica cosa ha trovato in tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · niente attività nuove» oppure «· 2 nuove attività». Si riferisce solo a quel controllo: le attività già presenti nell’elenco restano invariate. Se una nuova attività viene tenuta da parte per un momento più adatto, come il riepilogo mattutino, la riga indica fino a quando: «1 attività tenuta da parte fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole e la nuova attività o il motivo per cui non serviva farne una, per esempio «Solo in Cc, risponde un collega» o «Riunione già fissata per giovedì». Se il controllo ha dato un motivo generico, la conversazione non ne mostra uno specifico. Toccane una per leggerla, insieme al contesto.

Vengono mostrate le prime 10; tocca sotto per vedere le altre. Un numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono per un messaggio già nell’elenco compare una sola volta. La riga rimane visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email ricevute. Le tue risposte vengono lette per il contesto e per le promesse, ma non sono nuove email. Le email che la tua Machine ti invia, come il riepilogo mattutino o una notifica di correzione, non vengono mai lette né elencate. Le email relative alla fatturazione, alla prova o a un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passaggio, come **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Scopri di più su [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** ti chiede cosa vuoi cambiare: come svolgere l’attività oppure, una volta pronta la bozza, cosa modificarvi. Se lasci la richiesta a metà, la ritrovi al tuo ritorno; **Annulla** la elimina.

**Segna come fatto** indica che te ne sei occupato. Sul computer appare insieme agli altri pulsanti, quando c’è spazio su una riga. Sul telefono è visibile nelle attività pronte senza bozza o in quelle che ti fanno una domanda; negli altri casi si trova in cima al menu **…**. L’attività viene subito rimossa dall’elenco e nel messaggio compare **Annulla**. Scorri via il messaggio o trascinalo fuori con il mouse per chiuderla prima. La modifica viene mantenuta.

Per completare l’attività in un altro modo, scrivilo nella **Chat**. La risposta indica solo cosa è cambiato, per esempio il rinvio e fino a quando. Se non è stato possibile cambiare qualcosa, come una scadenza, te lo dice.

Nel menu **…**:

- **Passa…**: assegnala a un collega, a [Claude Code o Codex](hand-to-agent.md) oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: l’attività [si ripresenta a intervalli regolari](recurring.md).
- **Non serve**: l’attività viene rimossa. Se vuoi, indica il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine impara dalla scelta.

Tocca il titolo o **Nome** sotto **Dettagli** per rinominarla, oppure chiedilo nella chat, per esempio «Rinominala in…». Il titolo che scegli rimane.

**Riapri** riporta un’attività chiusa nell’elenco. L’attività si riapre anche da sola quando succede qualcosa di nuovo, per esempio se la persona ti scrive, ma non quando rispondi tu. A quel punto indica quando è stata riaperta e viene ordinata tra le nuove. La chat riprende da dove si era interrotta, anche dopo settimane.

Una fattura che devi pagare di persona, di qualsiasi paese, diventa un’attività con l’importo, la data di scadenza e i dati di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta salvata, non diventano attività. Se un’email successiva conferma il pagamento, per esempio con una conferma del mittente, l’attività si chiude da sola. Puoi riaprirla con **Annulla** entro un giorno.

Un’attività utile solo fino a un momento preciso, come una conferma da inviare prima di una riunione, si chiude da sola dopo quel momento. Viene spostata in **Fatte / scartate** con la dicitura «Non serve più». Puoi riaprirla con **Annulla** entro un giorno.

Prima che un messaggio o un passaggio per qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, comprese le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che l’attività è già stata completata, per esempio perché è stata fatta una richiesta e la risposta è stata positiva, l’attività si chiude da sola. Puoi riaprirla con **Annulla** entro un giorno.

Se qualcun altro scrive nella stessa conversazione dopo la preparazione della bozza, **Invia** la blocca: «Non inviata: nuovo messaggio nella conversazione». L’attività mostra il messaggio con **Leggila** e **Rifai per questo messaggio**. Premi di nuovo **Invia** per mandare la bozza così com’è.

Quando un messaggio più recente cambia i piani, per esempio una festa spostata in un’altra sede o una prenotazione annullata, The Machine aggiorna da sola le attività. Se l’attività serve ancora, segue il nuovo piano. Se non c’è più nulla da fare, viene spostata in **Fatte / scartate** con la dicitura «Non serve»; nella chat compare «Aggiornamento:» seguito dal motivo. Puoi riaprirla con **Annulla** entro un giorno.

Alla prima apertura delle attività, un breve suggerimento mostra le azioni principali: **Chiedi modifiche** e **Non serve**, e spiega che non parte nulla finché non premi **Invia**. Il suggerimento non compare più dopo che usi il relativo pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un messaggio di benvenuto che indica chi aspetta da più tempo una tua risposta. La risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica a chi si riferisce, l’organizzazione se pertinente (non solo perché qualcuno ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la relativa pagina nel Graph.

Se nel Graph sono disponibili, i nomi e le organizzazioni mostrano la foto o il logo; altrimenti mostrano le iniziali. Se un logo non si legge bene in piccolo, per esempio perché è bianco su sfondo trasparente o perché è un marchio largo, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessuna novità». Compare se l’ultimo scambio è vecchio o senza risposta e indica i canali non collegati, come WhatsApp. La tua Machine dice cosa non sa invece di tirare a indovinare.

Quando viene indicato un canale non collegato, **Connetti** accanto al nome apre la relativa connessione.

Il titolo indica cosa c’è da fare e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo, con sotto l’esito, per esempio «Fatta: Sam l’ha firmata martedì».

Sopra la bozza, una riga in grigio chiaro indica il messaggio da cui proviene, con il logo del servizio. Toccalo per leggere la conversazione. La bozza mostra il logo della destinazione, così vedi subito se si tratta di una risposta su Slack o di un’email.

Se la bozza tiene conto di un contributo ricevuto altrove, per esempio il suggerimento di un collega su Slack, una riga lo indica, per esempio «Basata su un messaggio di Sam in #ops». Tocca la riga per leggere il messaggio. Quando una modifica sostituisce la bozza, il contributo non viene più mostrato.

Una chat (Slack, WhatsApp, Telegram, Intercom…) viene mostrata come un’unica conversazione, dalla più vecchia: prima i messaggi precedenti a quello a cui si riferisce l’attività, poi le risposte successive. In WhatsApp, Telegram o Signal, i tuoi messaggi compaiono a destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e viene aperto nella conversazione. **Mostra messaggi precedenti** aggiunge i messaggi più vecchi. In un’email, il resto della conversazione è compattato sopra e sotto il messaggio.

Un messaggio si apre allo stesso modo dalla ricerca, dal Graph, dalle risposte di Ask o dall’ultimo controllo, contrassegnato con «Questo messaggio» oppure «Nuovi messaggi».

**Apri in Gmail** apre l’email nell’account Gmail a cui è arrivata. Su Android, se hai l’app Gmail, l’email si apre lì.

**Dettagli** di un’email mostra solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, i destinatari in Ccn o un indirizzo di risposta diverso. Se non ci sono altre informazioni, non compare nulla.

Una risposta in un thread Slack mostra anche i messaggi precedenti all’inizio del thread. Il link al messaggio originale dell’attività lo apre anche qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area (tocca un elemento per modificarlo), la tua ultima nota e il risultato di un agente di programmazione. Il titolo apre la chat. Un’attività completata rimane compatta; il messaggio da cui proviene si trova sotto **Dettagli**.

Un’attività «In attesa di» contiene un link al tuo ultimo messaggio alla persona e a quello che aspetti: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) crea un’attività per qualsiasi cosa. La creazione non invia nulla. Se non selezioni **Lavoro** o **Personale**, l’attività viene assegnata all’area giusta in base a chi riguarda e all’argomento. Trova anche l’email a cui si riferisce, comprese quelle più vecchie.

Se chiudi il modulo prima di aggiungere l’attività, il testo e le scelte rimangono disponibili la volta successiva; i file no. **Scarta** nel messaggio li elimina.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore». Puoi scriverli anche nella tua lingua. L’icona del calendario mostra alcune opzioni rapide e **Scegli una data**.
- **Si ripete**: l’attività si ripresenta a intervalli regolari. Scopri di più in [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, che sia un’email, un messaggio su Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, chi l’ha inviato e quando.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, usa la fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come in chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuoverne uno.

I file rimangono associati all’attività e la tua Machine li legge mentre ci lavora. Puoi creare un’attività anche solo con i file: la tua Machine la compila a partire da un PDF o da un file di testo. Una foto viene mostrata come immagine piccola; toccala per vederla a grandezza naturale.
