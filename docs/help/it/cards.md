---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via libera. Ecco cosa significano le sue varie parti.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 12be97d431968927
---
La tua Machine legge tutto ciò che arriva e crea un’attività solo quando serve il tuo intervento. Un’attività per ogni questione, indipendentemente dal numero di messaggi coinvolti.

## Dove si trovano le attività

La pagina **Attività** le raggruppa:

- **Appena fatto**: in cima trovi un ultimo passaggio che hai confermato, come l’invio di un modulo o la chiusura di una segnalazione, completato mentre non c’eri. Resta qui finché non tocchi **Ho capito**, al massimo per un giorno. Ricevi una notifica anche sul telefono.
- **Per te**: tutto ciò che aspetta il tuo intervento, a partire dalle cose più urgenti. Ogni attività mostra **Preparata** (il lavoro è pronto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima serve una tua decisione o una risposta), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un breve aggiornamento, senza decisioni da prendere).
- **In attesa di altri**: attività raccolte in un gruppo chiuso, in cui il prossimo passo spetta a qualcun altro (vedi sotto).
- **Torna più tardi**: attività posticipate e quelle senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: ciò che hai promesso e ciò che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / ignorate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, per esempio «Fatto 5 minuti fa». Le attività che sembrano già completate sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviato. Spostata in Fatte.» oppure «Inviato. Spostata in Più tardi fino a lunedì». **Apri** ti porta all’attività. Cerca un’attività per titolo o per destinatario, anche tra quelle in Più tardi e Fatte.

In **Per te** compaiono prima le attività scadute o in scadenza entro domani, poi le domande della tua Fleet, quindi i promemoria di una bacheca e infine tutto il resto. All’interno di ogni gruppo, le più recenti vengono prima. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e quando è completata: cambia solo il suo contrassegno. Negli altri gruppi aperti, le attività scadute o in scadenza entro domani vengono prima, poi le altre dalla più recente. La barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che l’attività è completata, per esempio «PR #3451 unita», ma non è ancora stata chiusa. **Riapri** la rimette nel tuo elenco e la tua Machine ne tiene conto. Queste attività non risultano mai in ritardo. Dopo un giorno si chiude da sola e puoi usare **Annulla**. Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola.

Se un messaggio arriva da un indirizzo che assomiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Questo non è Sam Lee». La persona viene mostrata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività ancora in attesa di qualcun altro, per esempio una revisione o una risposta, indica il passaggio con **In attesa di:**. Rimane in **In attesa di altri**, raccolta in un gruppo chiuso sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Lo stesso succede dopo che hai fatto una domanda: l’attività ricompare la mattina prima della scadenza, alla scadenza se è più tardi oggi oppure la mattina successiva se la scadenza è già passata. Indica anche chi deve ancora rispondere.

Se un’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, **Dettagli** lo mostra alla voce **Fatto quando**. Inviare la tua parte non la chiude: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola e puoi usare **Annulla**. Se non arriva nulla entro il momento in cui devi sollecitare, l’attività ricompare con **Scrivi un breve sollecito** nella chat. Per cambiare cosa significa completarla, scrivilo nella chat.

Se nessuno tocca un’attività per una settimana, compare una sola volta la domanda **Serve ancora?**. **Non serve** la chiude e puoi usare **Annulla**. **Tieni** la mantiene e non te lo chiede più. Se non rispondi per un’altra settimana, viene raccolta nel gruppo Torna più tardi e non viene più conteggiata sul numero dell’icona dell’app né nel riepilogo del mattino. Se la apri, scrivi un messaggio in chat, la modifichi, la posticipi o arriva un nuovo messaggio, torna nell’elenco.

Una volta alla settimana, un progetto rimasto inattivo e senza attività aperte può generare un’attività con un solo passo successivo specifico, al massimo tre a settimana. Vedi [Progetti](projects.md).

Quando non c’è nulla che richiede il tuo intervento, la tua Machine riposa e l’elenco è vuoto. Mentre controlla, si risveglia e te lo fa sapere. Se un controllo non è riuscito o è in ritardo, lo indica e mostra **Controlla ora** sotto.

Le opzioni **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer trovi la stessa selezione. Quando è attivo Lavoro o Personale, **Mostra tutto** torna a tutte le attività. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima all’elenco permette anche di passare direttamente a un’altra opzione: **Solo personale · Lavoro · Mostra tutto**.

La riga in cima all’elenco mostra il nome dell’ultimo riepilogo del mattino o della sera e quante attività include, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Tocca la riga per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, resta visibile su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non c’è un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per l’opzione selezionata.

Un’attività legata a un progetto mostra il nome del progetto sotto il titolo. Toccala per aprire il progetto. **Progetto** in **Dettagli** ti permette di cambiarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

**Area** in **Dettagli** sposta un’attività nell’altra area. Si spostano con lei anche le fonti che può leggere e da cui può inviare messaggi. **Annulla** nella nota la riporta indietro.

Se un’attività ha bisogno dell’altra area per proseguire e i messaggi da cui proviene si trovano tutti lì, si sposta e prosegue da sola. Altrimenti mostra **Sposta in Lavoro** e non viene spostata finché non la tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola nell’area giusta quando la trova. Fino ad allora non è né Lavoro né Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, te lo chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai etichettato come Personale viene considerata Personale. Le email di un’altra delle tue aziende finiscono nelle attività di quell’azienda. Un’attività sulla tua vita privata, per esempio un familiare che scrive al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, per esempio un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. Lavoro o Personale determina dove compare un’attività e con chi viene condivisa, ma non dove risponde: la risposta va sempre nella conversazione di origine, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in una Fleet di Lavoro né nel Team Graph.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con la bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. Sotto il titolo, l’intestazione indica anche quanto tempo ci vuole al tuo ritmo, per esempio «circa 2 min».

Un’attività che ti fa una domanda non viene inclusa in nessuna delle due opzioni: serve la tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i messaggi arrivati quando ce ne sono 40 in attesa o quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, da 00:00 a 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, la voce Controlli mostra «In pausa per la notte, recupero alle 06:30». Se di notte apri l’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non ci sono attività aperte, tocca la riga della tua Machine per visualizzarla insieme a **Dettagli**, che apre Controlli in Connessioni. Se ci sono attività aperte, sul computer si trova in cima. Qui viene mostrata una breve riga solo mentre è in corso un controllo, oppure se un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i propri tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga con ciò che ha trovato in tutte le fonti lette, per esempio «Controllati 13 messaggi alle 16:11 · niente richiede il tuo intervento» oppure «· 2 nuove attività». Se una nuova attività viene messa da parte per un momento più opportuno, per esempio il riepilogo del mattino, la riga indica fino a quando: «1 attività messa da parte fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica, con l’icona del servizio di origine: chi ha scritto, l’oggetto o le prime parole, e la nuova attività oppure il motivo per cui non serviva fare nulla, per esempio «Solo in Cc, risponde un collega» o «Riunione già fissata per giovedì». Se il controllo ha trovato solo un motivo generico, per una conversazione non viene mostrato alcun motivo. Tocca una voce per leggerla.

Vengono mostrate le prime 10 voci. Tocca sotto per vedere le altre. Un numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già presente nell’elenco viene mostrata una sola volta. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email che hai ricevuto. Le tue risposte vengono lette per avere contesto e tenere traccia delle promesse, ma non sono nuove email. Le email della tua Machine, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email sulla fatturazione, sulla prova o su un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il passo successivo, come **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare. **Segna come fatto** indica che è stata gestita: compare in vista su un’attività pronta senza bozza, altrimenti in cima a **…**, anche su un’attività che richiede una tua decisione. L’attività lascia subito l’elenco e nel messaggio compare **Annulla**. Per chiuderla subito, fai scorrere via il messaggio oppure trascinalo fuori con il mouse. La modifica resta.

Per farla svolgere in un altro modo, dillo nella **Chat**.

In **…**:

- **Passa…**: assegnala a un collega, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: [torna a intervalli regolari](recurring.md).
- **Non serve**: l’attività scompare. Se vuoi, puoi indicare il motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine ne tiene conto.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività. Il titolo che scegli resta invariato.

**Riapri** rimette nell’elenco un’attività chiusa. Ricompare anche da sola quando succede qualcosa di nuovo, per esempio se arriva un nuovo messaggio da quella persona, ma non se sei tu a rispondere.

Una fattura che devi pagare tu, di qualsiasi paese, diventa un’attività con l’importo, la data di scadenza e i dati di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta registrata, non diventano attività. Quando un’email successiva conferma il pagamento, per esempio dal mittente, l’attività si chiude da sola. Puoi usare **Annulla** per ripristinarla entro un giorno.

Un’attività che serve solo fino a un momento preciso, per esempio una conferma prima di una riunione, si chiude da sola dopo quel momento. Viene spostata in **Fatte / ignorate** con la dicitura «Non serve più». Puoi usare **Annulla** per ripristinarla entro un giorno.

Prima di preparare un messaggio o un passaggio di consegne per qualcuno, la tua Machine controlla le chat recenti con le persone coinvolte, comprese quelle di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che è già tutto a posto, per esempio perché hai chiesto qualcosa e la persona ha detto di sì, l’attività si chiude da sola. Puoi usare **Annulla** per ripristinarla entro un giorno.

Se un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna le attività da sola. Un’attività ancora utile segue i nuovi piani. Se non resta più nulla da fare, viene spostata in **Fatte / ignorate** con la dicitura «Non serve». Nella chat compare «Aggiornamento:» con il motivo. Puoi usare **Annulla** per ripristinarla entro un giorno.

Quando usi le attività per la prima volta, compare un breve suggerimento sulle azioni principali: **Chiedi modifiche** e **Non serve**, e sul fatto che nulla viene inviato finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il relativo pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un saluto e il nome della persona che aspetta da più tempo una tua risposta. La sua risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica di chi si tratta, l’organizzazione se è pertinente (non solo perché una persona ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la sua pagina nel Graph.

I nomi e le organizzazioni mostrano la foto o il logo, se disponibile nel Graph, altrimenti le iniziali. Se un logo è difficile da leggere in piccolo, per esempio perché è bianco su sfondo trasparente o è un marchio scritto molto largo, viene mostrata anche l’iniziale.

A volte compare una riga discreta che indica cosa non si sa, per esempio «Ultimo contatto via email 12 giorni fa; da allora nulla». Compare se l’ultimo scambio con quella persona è vecchio o senza risposta e indica i canali non collegati, come WhatsApp. La tua Machine dice ciò che non sa invece di tirare a indovinare.

Se viene indicato un canale non collegato, tocca Connetti accanto al suo nome per aprire quella connessione.

Il titolo indica cosa c’è da fare e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo, con sotto l’esito, per esempio «Fatto: Sam l’ha firmato martedì».

Sopra la bozza, una riga in grigio chiaro indica il messaggio da cui proviene, con il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo del servizio a cui verrà inviata, così vedi subito se si tratta di una risposta su Slack o di un’email.

Se la bozza si basa su un suggerimento dato altrove, per esempio da un collega su Slack, una riga lo indica, per esempio «Basato sul messaggio di Sam in #ops». Tocca la riga per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra un’unica conversazione, dalla più vecchia alla più recente: i messaggi precedenti a quello a cui si riferisce l’attività e le risposte successive. In WhatsApp, Telegram o Signal i tuoi messaggi sono sulla destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e si apre in primo piano. **Mostra messaggi precedenti** aggiunge quelli più vecchi. Un’email mostra il resto della conversazione raccolto in un gruppo chiuso sopra e sotto il messaggio.

**Dettagli** di un’email mostra solo le informazioni non presenti nell’intestazione, come gli indirizzi completi in Cc, quelli in Ccn o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, non viene mostrato.

Una risposta in un thread Slack mostra anche ciò che è stato detto prima dell’inizio del thread. Anche il link di un’attività al proprio messaggio lo apre qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area, che puoi toccare per modificarli, l’ultima nota e il risultato di un agente di programmazione. **Chat ›** apre la chat. Un’attività completata resta breve; il messaggio da cui proviene si trova in **Dettagli**.

Un’attività «In attesa di» include il link al tuo ultimo messaggio alla persona, quello a cui stai aspettando risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) aggiunge un’attività per qualsiasi cosa. Crearla non invia nulla. Se non scegli **Lavoro** o **Personale**, l’attività finisce nell’area giusta in base a chi riguarda e all’argomento. Trova anche l’email a cui fa seguito, comprese quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14:00» o «tra 2 ore», anche nella tua lingua. L’icona del calendario mostra le date rapide e **Scegli una data**.
- **Si ripete**: l’attività torna a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, per esempio un’email, un messaggio su Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile in The Machine. Cerca per testo o mittente. Ogni risultato mostra la fonte, chi l’ha inviato e quando.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file sul modulo. Sul telefono, usa la fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungi file](card-chat.md#add-files)). Con × rimuovi un file.

I file restano associati all’attività e The Machine li legge mentre ci lavora. Puoi aggiungere anche solo dei file: The Machine ricava i dettagli dell’attività da un PDF o da un file di testo. Una foto viene mostrata come immagine piccola. Tocca per vederla a grandezza naturale.
