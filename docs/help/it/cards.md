---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via libera. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: baa6b797e040a271
---
La tua Machine legge tutto quello che arriva e crea un’attività solo quando serve il tuo intervento. Una sola attività per ogni questione, anche se riguarda più messaggi.

## Dove trovi le attività

La pagina **Attività** le raccoglie così:

- **Appena fatto**: in cima, mostra un ultimo passaggio che hai confermato, come l’invio di un modulo o la risoluzione di un problema, completato mentre non c’eri. Resta lì finché non tocchi **Ho capito**, per un massimo di un giorno. Ricevi una notifica anche sul telefono.
- **Per te**: tutto quello che aspetta una tua risposta, in ordine di urgenza. Ogni attività ha uno stato: **Preparata** (il lavoro è fatto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima devi decidere o rispondere), **In preparazione…** (la tua Machine ci sta lavorando) oppure **Da leggere** (un riepilogo o un resoconto, senza decisioni da prendere).
- **In attesa di altri**: attività raccolte che aspettano il prossimo passo di un’altra persona (vedi sotto).
- **Torna più tardi**: attività posticipate e attività senza risposta a **Serve ancora?** (vedi sotto).
- **Promesse**: quelle che hai fatto e quelle che gli altri hanno fatto a te. Vedi [Promesse](promises.md).
- **Fatte / ignorate**: tutte le attività concluse, dalla più recente, con l’indicazione di quando sono state completate, per esempio «Completata 5 minuti fa». Quelle che sembrano già concluse sono contrassegnate con **Sembra fatto**.

Dopo l’invio, una breve nota ti dice dove è finita l’attività, per esempio «Inviata. Spostata in Fatte» oppure «Inviata. Spostata in Più tardi fino a lunedì». **Apri** ti porta all’attività. La ricerca trova le attività per titolo o per destinatario, anche in Più tardi e Fatte.

In **Per te** vengono prima le attività scadute o in scadenza entro domani, poi le domande dalla tua Fleet, i promemoria di una bacheca e infine le altre. In ogni gruppo, le più recenti vengono prima. Un’attività resta nella stessa posizione mentre la tua Machine la prepara e quando è conclusa: cambia solo il suo stato. Negli altri gruppi aperti, prima vengono quelle scadute o in scadenza entro domani, poi le altre dalla più recente. Anche la barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che è stato completato, per esempio «PR #3451 integrata», ma non è ancora chiuso. **Riapri** lo rimette nella tua lista e aiuta la tua Machine a imparare. Queste attività non risultano mai in ritardo. Dopo un giorno si chiudono da sole e puoi usare **Annulla**. Si chiude da sola anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack.

Se un messaggio arriva da un indirizzo che somiglia a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività te lo segnala chiaramente: «Non è Sam Lee». La persona viene mostrata con il suo indirizzo, mai con il nome che ha usato. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Un’attività che aspetta ancora qualcun altro, per esempio una revisione o una risposta, indica il passaggio con **In attesa di:**. Resta in **In attesa di altri**, raccolta sopra Torna più tardi, finché un nuovo messaggio non la riporta nella lista. Lo stesso vale dopo che hai risposto a una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è più tardi oggi, oppure la mattina successiva se la scadenza è già passata. Indica anche chi deve ancora rispondere.

Se un’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, **Dettagli** lo indica alla voce **Fatto quando**. Inviare la tua parte non la chiude: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola e puoi usare **Annulla**. Se non arriva nulla entro il momento in cui è ora di sollecitare, l’attività torna con **Scrivi un breve sollecito** nella chat. Per cambiare cosa conta come completamento, scrivilo nella chat.

Se nessuno tocca un’attività per una settimana, compare una domanda: **Serve ancora?** Con **Non serve** l’attività si chiude e puoi usare **Annulla**. **Tieni** la lascia aperta e non te lo chiede più. Se non rispondi per un’altra settimana, viene raccolta in Torna più tardi e non viene più conteggiata sul numero dell’icona dell’app né nel riepilogo del mattino. Aprirla, scrivere un messaggio in chat, modificarla, posticiparla o ricevere un nuovo messaggio la riporta nella lista.

Una volta alla settimana, un progetto rimasto inattivo e senza attività aperte può generare un’attività con un unico prossimo passo specifico, fino a tre a settimana. Vedi [Progetti](projects.md).

Quando niente richiede il tuo intervento, la tua Machine si riposa e la lista resta vuota. Durante un controllo, si riattiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, la riga lo indica e mostra **Controlla ora**.

Le opzioni **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. Sul telefono e sul computer trovi la stessa selezione. Se hai scelto Lavoro o Personale, **Mostra tutto** torna alla lista completa. Un avviso sulla tua Machine, per esempio un componente che continua a riavviarsi, non è né Lavoro né Personale e appare solo in Tutti.

La riga in cima alla lista ti permette anche di passare direttamente all’altra vista: se è attivo **Solo personale**, tocca **Lavoro** o **Mostra tutto**.

La riga in cima alla lista mostra il nome dell’ultimo riepilogo del mattino o della sera e il numero di elementi inclusi, per esempio **Riepilogo di ieri sera** · 12 completate, 3 aperte. Tocca la riga per rileggere il riepilogo. Con **Copia** puoi incollarlo dove vuoi. Dopo averlo aperto o aver toccato la sua **×**, resta su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non c’è un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per la vista selezionata.

Un’attività di un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. **Progetto** in **Dettagli** permette di modificarlo o rimuoverlo. Vedi [Le attività di un progetto](projects.md#a-project-s-to-dos).

**Area** in **Dettagli** sposta un’attività nell’altra area. Anche le fonti che può leggere e i messaggi che può inviare cambiano di conseguenza. **Annulla** nella nota la riporta dov’era.

Se un’attività ha bisogno dell’altra area per procedere e tutti i messaggi da cui proviene si trovano lì, si sposta e procede da sola. Altrimenti mostra **Sposta in Lavoro** e non si sposta finché non lo tocchi. Un’attività che hai creato senza scegliere Lavoro o Personale si sposta da sola quando trova l’area giusta. Fino ad allora non è assegnata a nessuna delle due e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi nell’altra area, te lo chiede con **Usa questa email per questa attività**. Un account di lavoro che hai contrassegnato come Personale viene considerato Personale. La posta delle altre tue aziende va alle attività di quella specifica azienda. Un’attività sulla tua vita privata, come un messaggio di famiglia arrivato al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. Lavoro o Personale determina dove appare un’attività e con chi viene condivisa, mai dove risponde: la risposta va sempre alla conversazione originale, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non appare mai in una Fleet di Lavoro o nel Graph del team.

Se ci sono almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine della lista, con la bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia quello che vedi sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. Sotto il titolo, l’intestazione indica anche quanto tempo serve al tuo ritmo, per esempio «circa 2 min».

Un’attività che ti fa una domanda non viene inclusa: richiede una tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ne sono in attesa 40 o quando un messaggio di una persona aspetta da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli si fermano. I nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, alla voce Controlli, compare «In pausa per la notte, riprende alle 06:30». Se di notte fai clic, scrivi o scorri nell’app, scrivi in chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per vedere lo stato e **Dettagli**, che apre Controlli in Connessioni. Se hai attività aperte, l’opzione si trova in cima alla lista sul computer. Una breve riga compare solo durante un controllo o se un controllo non è riuscito o è in ritardo. Puoi anche chiedere in chat.

LinkedIn, X e Salesflare seguono i loro tempi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, una riga sopra le attività indica cosa ha trovato in ogni fonte letta, per esempio «Controllati 13 messaggi alle 16:11 · niente richiede il tuo intervento» oppure «· 2 nuove attività». Se una nuova attività aspetta un momento più adatto, per esempio il riepilogo del mattino, la riga indica fino a quando: «1 attività in attesa fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica con l’icona della relativa fonte: chi ha scritto, l’oggetto o le prime parole, e la nuova attività o il motivo per cui non era necessario crearne una, per esempio «Sei solo in Cc, risponde un collega» oppure «Riunione già fissata per giovedì». Se il controllo ha dato solo un motivo vago, la conversazione non ne mostra uno. Tocca una voce per leggerla.

Vengono mostrate le prime 10 voci. Tocca sotto per vedere le altre. Il numero dopo un nome, per esempio (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già in elenco viene mostrata una sola volta. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email indirizzate a te. Le tue risposte vengono lette per avere contesto e tenere traccia delle promesse, ma non sono considerate nuova posta. Le email che la tua Machine ti invia, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email sulla fatturazione, sul periodo di prova o su un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il prossimo passo, per esempio **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** ti permette di indicare cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. **Segna come fatto** indica che è tutto a posto: appare su un’attività pronta senza bozza oppure, negli altri casi, in cima a **…**, anche per un’attività che richiede una tua decisione. L’attività esce subito dalla lista e nel messaggio compare **Annulla**. Scorri il messaggio per chiuderlo oppure trascinalo fuori con il mouse. La modifica resta.

Per farla in un altro modo, scrivilo nella sua **Chat**.

In **…** trovi:

- **Passa…**: assegna l’attività a un collega, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi una revisione](ask-to-review.md).
- **Ripeti…**: l’attività [torna a intervalli regolari](recurring.md).
- **Non serve**: l’attività scompare. Puoi scegliere anche un motivo: **Non pertinente**, **Fatti sbagliati** oppure **Già gestito**. La tua Machine impara dalla tua scelta.

Tocca il titolo o **Nome** in **Dettagli** per rinominare l’attività. Il titolo che scegli resta invariato.

**Riapri** ripristina un’attività chiusa. L’attività torna anche da sola quando succede qualcosa di nuovo, per esempio se ricevi un nuovo messaggio da quella persona, ma non quando rispondi tu.

Una fattura che devi pagare di persona, di qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dettagli di pagamento indicati nella fattura. Le fatture pagate automaticamente, per esempio con un addebito diretto o una carta registrata, non diventano attività. Quando un’email successiva conferma il pagamento, per esempio da parte del mittente, l’attività si chiude da sola. Puoi usare **Annulla** per ripristinarla entro un giorno.

Un’attività utile solo fino a un certo momento, per esempio una conferma da inviare prima di una riunione, si chiude da sola dopo quell’ora. Viene spostata in **Fatte / ignorate** con la dicitura «Non serve più». Puoi usare **Annulla** per ripristinarla entro un giorno.

Prima che un messaggio o un passaggio per qualcun altro risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, incluse le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che è già tutto fatto, per esempio perché hai chiesto qualcosa e ti hanno risposto di sì, l’attività si chiude da sola. Puoi usare **Annulla** per ripristinarla entro un giorno.

Se un messaggio più recente cambia i piani, per esempio una festa si sposta in un altro locale o una prenotazione viene annullata, The Machine aggiorna le attività da sola. Se un’attività serve ancora, segue i nuovi piani. Se non resta nulla da fare, viene spostata in **Fatte / ignorate** con la dicitura «Non serve». Nella chat compare «Aggiornamento:» con il motivo. Puoi usare **Annulla** per ripristinarla entro un giorno.

Quando crei le prime attività, compare un breve suggerimento che mostra le azioni principali: **Chiedi modifiche** e **Non serve**. Ti ricorda anche che non viene inviato nulla finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il relativo pulsante o premi ×.

Il primo giorno, in cima ad Attività trovi un messaggio di benvenuto che indica chi aspetta da più tempo una tua risposta. La bozza di quella risposta viene preparata per prima, così è pronta al tuo arrivo.

Ogni attività inizia con il titolo. La riga sotto indica chi riguarda, l’organizzazione se pertinente (non solo perché una persona ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la sua pagina nel Graph.

Se nel Graph è disponibile, accanto al nome o all’organizzazione compare la foto o il logo; altrimenti vengono mostrate le iniziali. Anche per un logo poco leggibile in piccolo, per esempio bianco su sfondo trasparente o composto da una scritta larga, viene mostrata l’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto via email 12 giorni fa; nessun aggiornamento da allora». Compare quando l’ultimo contatto è vecchio o senza risposta e segnala i canali non collegati, per esempio WhatsApp. La tua Machine indica ciò che non sa invece di fare supposizioni.

Se viene indicato un canale non collegato, tocca **Connetti** accanto al nome per aprire la relativa connessione.

Il titolo descrive cosa c’è da fare e cambia solo se cambia l’attività. Un’attività completata mantiene il titolo e mostra sotto come è finita, per esempio «Fatto: Sam ha firmato martedì».

Sopra la bozza, una riga in grigio indica il messaggio da cui proviene, con il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo della destinazione, così vedi subito se si tratta di una risposta su Slack o di un’email.

Se la bozza tiene conto di un suggerimento ricevuto altrove, per esempio da un collega su Slack, una riga lo indica, per esempio «In base al messaggio di Sam in #ops». Tocca la riga per leggere quel messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra un’unica conversazione, dalla più vecchia alla più recente: i messaggi precedenti a quello dell’attività e le risposte successive. In WhatsApp, Telegram o Signal i tuoi messaggi sono sulla destra, come nell’app. Il messaggio dell’attività è contrassegnato con «Questa attività» e viene aperto nella conversazione. **Mostra messaggi precedenti** aggiunge quelli più vecchi. In un’email, il resto della conversazione è raccolto sopra e sotto il messaggio.

**Apri in Gmail** apre l’email nell’account Gmail che l’ha ricevuta. Su Android, se hai installato l’app Gmail, l’email si apre lì.

**Dettagli** di un’email mostra solo le informazioni non visibili nell’intestazione, come gli indirizzi Cc completi, il Bcc o un indirizzo di risposta diverso. Se non c’è altro da aggiungere, non compare nulla.

Una risposta in un thread Slack mostra anche i messaggi precedenti all’inizio della conversazione. Il link dell’attività al messaggio originale lo apre qui, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area (tocca uno di questi elementi per modificarlo), la tua ultima nota e il risultato di un agente di programmazione. Tocca il titolo per aprire la chat. Un’attività completata resta in formato compatto: il messaggio da cui proviene è in **Dettagli**.

Un’attività «In attesa di» collega il tuo ultimo messaggio alla persona a cui hai scritto, quello a cui aspetti risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer, **+** sul telefono o `N`) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non selezioni **Lavoro** o **Personale**, viene assegnata all’area giusta in base alla persona e all’argomento. Trova anche l’email a cui si riferisce, comprese quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14» o «tra 2 ore». Puoi scriverlo anche nella tua lingua. L’icona del calendario mostra le scelte rapide e **Scegli una data**.
- **Si ripete**: l’attività torna a intervalli regolari. Vedi [Attività ricorrenti](recurring.md).
- **Persona**: collega le persone o le aziende a cui si riferisce, fino a un massimo di 5.
- Icona del messaggio: allega il messaggio a cui si riferisce, per esempio un’email, un messaggio su Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio disponibile nella tua Machine. Cerca per testo o mittente. Ogni risultato indica la fonte, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, tocca la fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungi file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano allegati all’attività e la tua Machine li legge mentre ci lavora. Puoi usare anche solo i file: ricava l’attività da un PDF o da un file di testo. Le foto vengono mostrate in miniatura: toccale per vederle a grandezza naturale.
