---
title: Attività
area: cards
summary: Un’attività per ogni cosa che richiede il tuo intervento, pronta per il tuo via libera. Ecco cosa significano le varie parti di un’attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
La tua Machine legge tutto ciò che arriva e crea un’attività solo quando c’è qualcosa che richiede il tuo intervento. Un’attività per ogni questione, anche se coinvolge più messaggi.

## Dove trovi le attività

La pagina **Attività** le raggruppa così:

- **Per te**: tutto ciò che aspetta una tua risposta, in ordine di urgenza. Ogni attività indica **Preparata** (il lavoro è pronto e **Fallo** o **Invia** lo porta a termine), **Serve il tuo intervento** (prima serve una tua decisione o risposta) oppure **In preparazione…** (la tua Machine ci sta lavorando).
- **Appena fatto**: un ultimo passaggio che hai confermato, come l’invio di un modulo o la creazione di una segnalazione, è andato a buon fine mentre non c’eri. Resta qui finché non tocchi **Ho capito**, per un massimo di un giorno. Ricevi una notifica anche sul telefono.
- **Torna più tardi**: le attività posticipate e quelle per cui non hai risposto a **Serve ancora?** (vedi sotto).
- **Promesse**: ciò che hai promesso e ciò che gli altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / ignorate**: tutte le attività completate, dalla più recente, con l’ora in cui sono state completate, come «Fatta 5 minuti fa». Le attività che sembrano già completate sono contrassegnate come **Sembra fatto**.

Dopo l’invio, una breve nota indica dove è finita l’attività, per esempio «Inviata. Spostata in Fatte.» o «Inviata. Spostata in Più tardi fino a lunedì». **Apri** ti porta all’attività. Puoi cercare un’attività per titolo o per destinatario, anche in Più tardi e Fatte.

In **Per te** vengono prima le attività scadute o in scadenza entro domani, poi le domande della tua Fleet e infine le altre. All’interno di ogni gruppo, le più recenti vengono prima. Un’attività mantiene la sua posizione mentre la tua Machine la prepara e quando è completata: cambia solo il contrassegno. Negli altri gruppi aperti vengono prima quelle scadute o in scadenza entro domani, poi le altre in ordine di arrivo. Anche la barra laterale mantiene lo stesso ordine.

**Sembra fatto** significa che la tua Machine vede che l’attività è completata, per esempio «PR #3451 è stata unita», ma non è ancora chiusa. **Riapri** la rimette nell’elenco e la tua Machine ne fa tesoro. Queste attività non vengono mai indicate come in ritardo. Dopo un giorno si chiudono da sole, con **Annulla**. Anche un’attività che hai già gestito tu, per esempio rispondendo in Gmail o Slack, si chiude da sola.

Quando un messaggio arriva da un indirizzo che somiglia soltanto a quello di una persona che conosci, per esempio sam@acme-corp.example invece di sam@acmecorp.example, l’attività lo dice chiaramente: «Non è Sam Lee». La persona viene mostrata con il suo indirizzo reale, mai con il nome usato nel messaggio. La tua Machine verifica il messaggio con la persona all’indirizzo che hai già, mai con chi l’ha scritto.

Se un’attività è ancora in attesa di qualcun altro, per esempio per una revisione o una risposta, indica il passaggio con **In attesa di:**. Resta in **In attesa di altri**, compattata sopra Torna più tardi, finché un nuovo messaggio non la riporta nell’elenco. Succede lo stesso dopo che hai fatto una domanda: l’attività torna la mattina prima della scadenza, alla scadenza se è più tardi oggi, oppure la mattina successiva se la scadenza è già passata. Indica anche chi deve ancora rispondere.

Se l’attività riguarda un risultato che deve fornire qualcun altro, come un contratto firmato, in **Dettagli** lo trovi indicato sotto **Fatto quando**. L’invio della tua parte non chiude l’attività: resta in **In attesa di altri** finché un messaggio non conferma il risultato, poi si chiude da sola, con **Annulla**. Se non arriva nulla entro il momento in cui è ora di sollecitare, l’attività torna con l’opzione **Scrivi un breve sollecito** nella sua chat. Per modificare cosa conta come completamento, scrivilo nella chat.

Se nessuno tocca un’attività per una settimana, viene chiesto una volta: **Serve ancora?** **Non serve** la chiude, con **Annulla**. **Tieni** la mantiene e non verrà più chiesto. Se non rispondi per un’altra settimana, l’attività viene spostata in Torna più tardi e non viene più conteggiata nel numero sull’icona dell’app né nel riepilogo del mattino. Se la apri, invii un messaggio nella chat, la modifichi, la posticipi o arriva un nuovo messaggio, torna nell’elenco.

Una volta alla settimana, un progetto rimasto inattivo e senza attività aperte può ricevere un’attività con un unico passo successivo specifico, per un massimo di tre a settimana. Vedi [Progetti](projects.md).

Quando non c’è nulla che richiede il tuo intervento, la tua Machine fa un pisolino e l’elenco resta vuoto. Durante un controllo si riattiva e te lo segnala. Se un controllo non è riuscito o è in ritardo, lo indica nella sua riga, con **Controlla ora** sotto.

Le opzioni **Tutti**, **Lavoro** e **Personale** in cima alla barra laterale mostrano tutte le attività o solo quelle di un tipo. La scelta è la stessa sul telefono e sul computer. Quando è selezionato Lavoro o Personale, **Mostra tutto** riporta alla visualizzazione completa. Un avviso sulla tua Machine, come un componente che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

Anche la riga in cima all’elenco permette di passare direttamente all’altra visualizzazione: **Solo Personale · Lavoro · Mostra tutto**.

La riga in cima all’elenco indica il tuo ultimo riepilogo del mattino o della sera e cosa include, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Tocca la riga per rileggere il riepilogo, con **Copia** per incollarlo dove vuoi. Una volta aperto o dopo aver toccato la **×**, resta su tutti i tuoi dispositivi fino al riepilogo successivo.

Se non c’è un riepilogo recente, viene mostrato **Oggi finora**: cosa è stato completato oggi e cosa è ancora aperto, per Lavoro e Personale oppure solo per il tipo selezionato.

Un’attività legata a un progetto mostra il nome del progetto sotto il titolo. Toccalo per aprire il progetto. Puoi modificare o rimuovere **Progetto** in **Dettagli**. Vedi [Le attività di un progetto](projects.md#a-projects-to-dos).

**Area** in **Dettagli** sposta un’attività nell’altra area. Si sposta anche l’accesso ai messaggi che può leggere e da cui può inviare. **Annulla** nella nota la riporta indietro.

Se un’attività ha bisogno dell’altra area per procedere e tutti i messaggi da cui proviene si trovano lì, si sposta da sola e procede. Altrimenti mostra **Sposta in Lavoro** e non si sposta finché non lo tocchi. Un’attività che hai aggiunto senza scegliere Lavoro o Personale si sposta da sola quando trova la sua area. Nel frattempo non è indicata come Lavoro né Personale e resta privata.

Un’attività può sempre leggere i messaggi da cui proviene. Se ha bisogno di altri messaggi dell’altra area, te lo chiede con **Usa questa email per questa attività**. Una casella di lavoro che hai etichettato Personale viene considerata Personale. Le email per un’altra delle tue aziende vanno alle attività di quell’azienda. Un’attività che riguarda la tua vita privata, come un messaggio di famiglia arrivato al tuo indirizzo di lavoro, è Personale fin dall’inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall’inizio. Un’attività che hai spostato o assegnato tu resta sempre dove l’hai messa. Lavoro o Personale determina dove compare l’attività e con chi è condivisa, mai dove risponde: la risposta va sempre nella conversazione da cui proviene, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

Un’attività Personale di questo tipo risponde comunque dall’indirizzo di lavoro a cui è arrivata l’email e non compare mai in una Fleet di Lavoro o nel Graph del team.

Se hai almeno due attività in attesa, **Scorri** nell’intestazione di Per te le mostra una alla volta, nell’ordine dell’elenco, con ogni bozza completa e le opzioni **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Sul computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc interrompe. Sotto il titolo, l’intestazione indica anche quanto tempo richiedono, al ritmo che preferisci, per esempio «circa 2 min».

Un’attività che ti fa una domanda non viene inclusa: aspetta una tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte. Controlla i nuovi messaggi quando ce ne sono 40 in attesa oppure quando il messaggio più vecchio di una persona è in attesa da 15 minuti. Newsletter, notifiche e ricevute vengono incluse nel controllo successivo, entro un’ora.

Di notte, da 00:00 a 06:30, i controlli si fermano: i nuovi messaggi vengono comunque letti e conservati, poi controllati tutti insieme alle 06:30, così le attività sono pronte prima del riepilogo del mattino. In Connessioni, sotto Controlli, viene indicato «In pausa per la notte, recupera alle 06:30». Se di notte apri l’app, scrivi nella chat o tocchi un’attività, i controlli riprendono normalmente finché non resti inattivo per un’ora. **Controlla ora** avvia sempre subito un controllo.

**Controlla ora** legge subito tutte le fonti. Se non hai attività aperte, tocca la riga della tua Machine per vederla, con **Dettagli**, che apre Controlli in Connessioni. Se hai attività aperte, sul computer trovi l’opzione in cima. Una breve riga compare solo durante un controllo o se uno non è riuscito o è in ritardo. Puoi anche chiedere nella chat.

LinkedIn, X e Salesflare seguono i propri ritmi.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, sopra le attività compare una riga con ciò che ha trovato in ogni fonte letta, per esempio «Controllati 13 messaggi alle 16:11 · nulla richiede il tuo intervento» oppure «· 2 nuove attività». Se una nuova attività aspetta un momento più adatto, come il riepilogo del mattino, viene indicato fino a quando: «1 attività in sospeso fino a domani alle 08:30».

Tocca la riga per vedere ogni conversazione email, chat e notifica, con l’icona della fonte: chi ha scritto, l’oggetto o le prime parole, e la nuova attività o il motivo per cui non serviva intervenire, come «In copia, risponde un collega» o «Riunione già fissata per giovedì». Se il controllo ha trovato solo un motivo generico, la conversazione non ne mostra uno. Tocca una conversazione per leggerla.

Vengono mostrate le prime 10. Tocca sotto per vedere le altre. Il numero accanto a un nome, come (3), indica quanti nuovi messaggi ci sono in quella chat. Una notifica sul telefono relativa a un messaggio già elencato compare una sola volta. La riga resta visibile per 12 ore dopo il controllo.

Vengono conteggiate solo le email indirizzate a te. Le tue risposte vengono lette per avere il contesto e tenere traccia delle promesse, ma non sono nuove email. Le email della tua Machine, come il riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email relative alla fatturazione, al periodo di prova o a un invito vengono lette normalmente.

## I pulsanti

Un’attività mostra il passo successivo, come **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** indica cosa cambiare: come svolgere l’attività oppure, quando la bozza è pronta, cosa modificare al suo interno. **Segna come fatto** indica che l’attività è stata gestita: è visibile su un’attività pronta senza bozza, altrimenti si trova in cima a **…**, anche se richiede una tua decisione. L’attività esce subito dall’elenco e nel messaggio compare **Annulla**. Per chiuderla più rapidamente, fai scorrere il messaggio oppure trascinalo fuori con il mouse. La modifica resta.

Per farla in un altro modo, scrivilo nella sua **Chat**.

In **…**:

- **Passa…**: assegnala a un collega, a [Claude Code o Codex](hand-to-agent.md), oppure [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: [torna secondo una cadenza](recurring.md).
- **Non serve**: l’attività viene rimossa. Puoi scegliere un motivo: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine ne fa tesoro.

Tocca il titolo o **Nome** in **Dettagli** per rinominarla. Il titolo che scegli resta.

**Riapri** riporta nell’elenco un’attività chiusa. L’attività può tornare anche da sola quando succede qualcosa di nuovo, per esempio quando arriva un nuovo messaggio da quella persona, ma non quando rispondi tu.

Una bolletta che devi pagare tu, da qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dati di pagamento indicati nella bolletta. Non succede con le bollette pagate automaticamente, come quelle con addebito diretto o carta salvata. Quando un’email successiva conferma il pagamento, per esempio quando il mittente conferma di averlo ricevuto, l’attività si chiude da sola. **Annulla** la riporta indietro per un giorno.

Un’attività che serviva solo fino a un momento preciso, come una conferma prima di una riunione, si chiude da sola dopo quell’ora. Viene spostata in **Fatte / ignorate** con la dicitura «Non serve più». **Annulla** la riporta indietro per un giorno.

Prima che un messaggio o un passaggio per qualcuno risulti pronto, la tua Machine controlla le chat recenti con le persone coinvolte, comprese le chat di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che è già stato fatto, per esempio perché è stato chiesto e qualcuno ha risposto di sì, l’attività si chiude da sola. **Annulla** la riporta indietro per un giorno.

Quando un messaggio più recente cambia i piani, per esempio perché una festa è stata spostata in un altro locale o una prenotazione è stata annullata, The Machine aggiorna da sola le attività. Quelle ancora utili seguono i nuovi piani. Quelle per cui non resta nulla da fare vengono spostate in **Fatte / ignorate** con la dicitura «Non serve». Nella chat compare «Aggiornamento:» con il motivo e **Annulla** riporta l’attività indietro per un giorno.

Nelle tue prime attività compare un breve suggerimento con le azioni principali: **Chiedi modifiche** e **Non serve**. Ti ricorda anche che nulla viene inviato finché non premi **Invia**. Il suggerimento scompare definitivamente quando usi il pulsante o premi ×.

Il primo giorno, in cima ad Attività ti diamo il benvenuto e ti diciamo chi aspetta da più tempo una tua risposta. La risposta viene preparata per prima, così è pronta quando arrivi.

Ogni attività inizia con il titolo. La riga sotto indica a chi riguarda, l’organizzazione se pertinente (non solo perché qualcuno ci lavora), il progetto, Lavoro o Personale e quando è arrivata. Tocca un nome per aprire la pagina della persona nel Graph.

I nomi e le organizzazioni mostrano la foto o il logo se il Graph ne ha uno, altrimenti le iniziali. Se un logo non si leggerebbe bene in piccolo, per esempio perché è bianco su sfondo trasparente o è un logotipo largo, viene mostrata anche l’iniziale.

A volte una riga discreta indica cosa non si sa, per esempio «Ultimo contatto 12 giorni fa via email; nessun aggiornamento». Compare quando l’ultimo contatto risale a tempo fa o non ha ricevuto risposta, e indica i canali non collegati, come WhatsApp. La tua Machine dichiara cosa non sa invece di tirare a indovinare.

Se viene indicato un canale non collegato, **Connetti** accanto al nome apre quella connessione.

Il titolo indica cosa c’è da fare e cambia solo quando cambia l’attività. Un’attività completata mantiene il suo titolo, con sotto l’esito, per esempio «Fatta: Sam l’ha firmata martedì».

Sopra la bozza, una riga in caratteri chiari indica il messaggio da cui proviene e mostra il logo del servizio. Tocca la riga per leggere la conversazione. La bozza mostra il logo della destinazione, così capisci subito se si tratta di una risposta Slack o di un’email.

Se la bozza si basa su un contributo di qualcuno in un altro posto, come il suggerimento di un collega su Slack, una riga lo indica, per esempio «Basata sul messaggio di Sam in #ops». Tocca la riga per leggere il messaggio.

Una chat (Slack, WhatsApp, Telegram, Intercom…) mostra una conversazione unica, dal messaggio più vecchio al più recente: i messaggi precedenti a quello dell’attività e le risposte successive. In WhatsApp, Telegram o Signal i tuoi messaggi sono a destra, come nell’app. Il messaggio dell’attività è contrassegnato da «Questa attività» e la conversazione si apre su quel messaggio. **Mostra messaggi precedenti** aggiunge quelli più vecchi. In un’email, il resto della conversazione è compattato sopra e sotto il messaggio.

I **Dettagli** di un’email mostrano solo le informazioni che non sono già nella sua intestazione, come gli indirizzi Cc completi, Bcc o un indirizzo diverso per le risposte. Se non c’è altro da aggiungere, non vengono mostrati.

Una risposta in un thread Slack mostra anche cosa è stato detto prima dell’inizio del thread. Il link di un’attività al suo messaggio apre anche qui la conversazione, con **Apri in Slack** in fondo.

**Dettagli** mostra il nome, il progetto e l’area, che puoi modificare toccandoli, l’ultima nota e il risultato di un agente di coding. **Chat ›** apre la chat. Un’attività completata resta sintetica; il messaggio da cui proviene si trova in **Dettagli**.

Un’attività «In attesa di» rimanda al tuo ultimo messaggio a quella persona, quello a cui stai aspettando risposta: «Email a Pat · mar».

## Crea un’attività

**Nuova attività** (sotto **Cerca** sul computer) crea un’attività per qualsiasi cosa. Crearla non invia nulla. Se non hai selezionato Lavoro o Personale, viene assegnata all’area giusta in base a chi riguarda e al contenuto. Trova anche l’email a cui fa seguito, comprese quelle più vecchie.

- **Scadenza**: inserisci un giorno o un orario, per esempio «domani», «ven prossimo», «3 nov», «14:00» o «tra 2 ore», anche nella tua lingua. L’icona del calendario offre scelte rapide e **Scegli una data**.
- **Messaggio**: allega il messaggio a cui si riferisce, per esempio un’email o un messaggio da Slack, Teams, WhatsApp, Telegram o qualsiasi altro servizio disponibile su The Machine. Cerca per testo o mittente. Ogni risultato indica la provenienza, il mittente e la data.
- **File**: tocca la graffetta, incolla uno screenshot o trascina i file nel modulo. Sul telefono, tocca la fotocamera accanto per scattare una foto. Puoi aggiungere fino a 5 file, come nella chat (vedi [Aggiungere file](card-chat.md#add-files)). Tocca × per rimuovere un file.

I file restano allegati all’attività e The Machine li legge mentre ci lavora. Puoi allegare solo i file: l’attività viene compilata a partire da un PDF o da un file di testo. Una foto viene mostrata come immagine piccola: toccala per vederla a grandezza intera.
