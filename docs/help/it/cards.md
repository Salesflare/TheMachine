---
title: Attività
area: cards
summary: Un'attività per ogni cosa che ha bisogno di te, pronta per il tuo sì. Cosa significano le parti di un'attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
La tua Machine legge tutto ciò che è nuovo e crea un'attività solo quando qualcosa ha bisogno di te. Un'attività per questione, per quanti messaggi comprenda.

## Dove stanno le attività

La pagina **Attività** le raggruppa:

- **Per te**: tutto ciò che aspetta te, prima il più urgente. Ogni attività dice **Preparata** (il lavoro è fatto, e **Fallo** o **Invia** lo porta a termine) **Serve il tuo intervento** (prima serve una tua decisione o una risposta) o **In preparazione…** (la tua Machine ci sta lavorando).
- **Appena fatto**: un ultimo passo che hai confermato, come inviare un modulo o creare una issue, è andato a buon fine mentre eri via. Mostra cosa è successo finché non tocchi **Ho capito**, al massimo per un giorno, e lo sa anche il tuo telefono. Poi resta solo in Fatto.
- **Torna più tardi**: posticipate, e le attività senza risposta a **Serve ancora?** (sotto).
- **Promesse**: quello che hai promesso e quello che altri hanno promesso a te. Vedi [Promesse](promises.md).
- **Fatte / ignorate**: tutte le attività concluse, in base a quando sono state concluse, dalla più recente, 30 alla volta mentre scorri. Un’attività appena inviata è in cima, e ognuna dice quando, come «Fatto 5 minuti fa». Quelle che sembrano già concluse stanno tra le altre in base a quando hanno cominciato a sembrarlo, con l’etichetta **Sembra fatto**.

Dopo l’invio, una breve nota dice dove si trova l’attività, come «Inviato. Spostato in Fatto.» o, se aspetta una risposta, «Inviato. Spostato in Più tardi fino a lun.» **Apri** ti ci porta. Il thread che esce dalla posta in arrivo per qualche giorno riguarda solo la tua casella. La ricerca trova un’attività per titolo o destinatario, anche in Più tardi e Fatto.

**Per te** mette prima ciò che è scaduto o in scadenza entro domani, poi le domande della tua Fleet, poi il resto. In ogni parte, prima la più recente. Un'attività resta al suo posto mentre la tua Machine la prepara e quando ha finito: cambia solo il suo segno. Gli altri gruppi aperti mettono prima ciò che è scaduto o in scadenza entro domani, il resto dalla più recente. La barra laterale ha lo stesso ordine.

Un’attività con **Sembra fatto** appare come una fatta, con ciò che mostra che è fatta, come "PR #3451 unita". Non è ancora chiusa: **Riapri** la rimette nella tua lista, e la tua Machine ne tiene conto. Non risultano mai in ritardo e non contano come in attesa di te. Dopo un giorno si chiude da sola, con **Annulla**. Anche un’attività che hai già sbrigato tu, per esempio con una risposta in Gmail o Slack, si chiude da sola.

Un’attività il cui ultimo passo è ancora aperto da parte di qualcun altro, come una revisione, un merge o una risposta, mostra **In attesa di:** quel passo e resta aperta. Aspetta in **In attesa di altri**, chiusa sopra Torna più tardi, e non conta come pronta per te. Un nuovo messaggio su di essa la riporta indietro. Lo stesso se hai risposto con una domanda: torna la mattina prima della scadenza, alla scadenza se è più tardi oggi, o la mattina dopo se è passata, e dice chi sta ancora aspettando.

Quando un’attività punta a un risultato che deve dare qualcun altro, come un contratto firmato o un pagamento, i suoi **Dettagli** mostrano quel risultato come **Fatto quando**. Inviare la tua parte non la chiude: aspetta in **In attesa di altri** finché un messaggio non mostra il risultato, poi si chiude da sola, con **Annulla**. Se non arriva niente quando è ora di sollecitare, torna con **Scrivi un breve sollecito** nella sua chat. Per cambiare cosa conta come fatto, dillo nella chat.

Un’attività che nessuno tocca da una settimana chiede una volta: **Serve ancora?** **Non serve** la chiude, con **Annulla**. **Tieni** la tiene, e non lo chiede più. Aprirla, un messaggio in chat, una modifica, posticiparla o un nuovo messaggio su di lei contano come un tocco. Senza risposta per un’altra settimana, finisce in Torna più tardi, sotto Serve ancora?, invece di sparire. Allora il numero sull’icona dell’app e il riepilogo del mattino smettono di contarla. Un tocco la riporta indietro.

Una volta a settimana, un progetto rimasto fermo senza nulla di aperto può ricevere un’attività con un prossimo passo preciso, al massimo tre a settimana. Vedi [Progetti](projects.md).

Quando niente ha bisogno di te, la tua Machine fa un pisolino sull’elenco vuoto. Mentre controlla, si sveglia e lo dice. Se un controllo non è riuscito o è in ritardo, la sua riga lo dice, con **Controlla ora** sotto.

**Tutti**, **Lavoro** e **Personale** sopra l'elenco nella barra laterale mostrano tutte le attività o solo un tipo. La tua Machine ricorda la scelta, così telefono e computer mostrano lo stesso elenco. Quando è attivo Lavoro o Personale, la parte alta dell'elenco lo indica, con **Mostra tutto** per tornare indietro. Un avviso sulla tua Machine stessa, come una parte che continua a riavviarsi, non è né Lavoro né Personale e compare solo in Tutti.

La riga in cima all'elenco passa anche direttamente all'altra: **Solo personale · Lavoro · Mostra tutto**.

La riga in cima all’elenco indica il tuo ultimo riepilogo del mattino o della sera e cosa ha contato, per esempio **Riepilogo di ieri sera** · 12 fatte, 3 aperte. Toccala per rileggerlo, con **Copia** per incollarlo ovunque. Appena la apri o tocchi la sua **×**, sparisce su tutti i tuoi dispositivi fino al prossimo riepilogo.

Senza un riepilogo recente mostra **Oggi finora**: cosa è stato fatto oggi e cosa è ancora aperto, per Lavoro e Personale, o solo quello che filtri.

Un'attività su un progetto mostra il nome del progetto nella riga sotto il titolo; apre il progetto. **Progetto** in **Dettagli** lo cambia o lo toglie. Vedi [le attività di un progetto](projects.md#a-projects-to-dos).

**Area** in **Dettagli** sposta l'attività nella tua altra area. Cosa può leggere e da dove può inviare segue lo spostamento; i messaggi da cui è nata restano dove sono. **Annulla** nell'avviso che segue la riporta indietro.

Quando un'attività ha bisogno di un'altra area per andare avanti e i messaggi da cui nasce sono tutti lì, si sposta da sola e continua. Altrimenti lo chiede con un pulsante **Sposta in Lavoro**. Niente si sposta finché non lo tocchi; poi continua da sola. Un'attività aggiunta senza scegliere Lavoro o Personale si sposta da sola appena sa dove va. Fino ad allora non indica né Lavoro né Personale e resta privata.

Quando avvii un'attività, può sempre leggere i messaggi da cui è nata, anche nella casella di un'altra azienda. Se le servono altri messaggi da un'altra area, lo chiede con **Usa questa email per questa attività**; un tocco li aggiunge e continua. La posta per un'altra delle tue aziende va subito tra le attività di quell'azienda. Un'attività della tua vita privata, come la famiglia che scrive al tuo indirizzo di lavoro, è Personale fin dall'inizio.

Il lavoro che ti arriva su un account personale, come un cliente su WhatsApp o un ordine nella tua casella personale, è Lavoro fin dall'inizio. Un'attività che hai spostato o messo tu resta sempre dove l'hai messa. Lavoro o Personale decide dove compare un'attività e con chi è condivisa, mai da dove risponde: una risposta va sempre dove si trova la conversazione, anche dopo uno spostamento, a meno che tu non scelga un altro modo.

La risposta parte comunque dall'indirizzo di lavoro dove è arrivata, e non compare mai in una Work Fleet né nel Graph del team.

Con due o più in attesa, **Scorri** nell’intestazione di Per te le passa una alla volta, nell’ordine della lista, ogni bozza per intero, con **Invia** o **Fallo**, **Chiedi modifiche**, **Posticipa** e **Salta**. Al computer, Invio invia ciò che è sullo schermo, `S` posticipa, `→` salta ed Esc si ferma. Sotto il titolo, l’intestazione dice anche quanto ci vuole al tuo ritmo, come "circa 2 min".

Un'attività che ti chiede qualcosa resta fuori da entrambi: le serve la tua risposta, non un tocco.

## Controlla ora

La tua Machine legge ogni fonte ogni pochi minuti, giorno e notte, e controlla cosa è arrivato in cerca di attività appena 40 messaggi sono in attesa o il messaggio più vecchio di una persona aspetta da 15 minuti. Newsletter, notifiche e ricevute entrano nel controllo successivo, entro un’ora.

Di notte, dalle 00:00 alle 06:30, i controlli vanno in pausa: i nuovi messaggi vengono comunque letti e salvati, e controllati insieme alle 06:30, così le tue attività sono pronte prima del riepilogo del mattino. Controlli, in Connessioni, dice allora “In pausa per la notte, recupera alle 06:30”. Se di notte apri l’app, scrivi in chat o tocchi un’attività, i controlli tornano normali finché non resti inattivo per un’ora. **Controlla ora** controlla sempre subito.

**Controlla ora** legge subito ogni fonte. Se non c’è niente di aperto, tocca la riga della tua Machine per vederlo, con **Dettagli**, che apre Controlli in Connessioni. Con attività aperte, è in alto su un computer. Lì compare una breve riga solo mentre un controllo è in corso, o quando uno non è riuscito o è in ritardo. Puoi anche chiederlo in chat.

LinkedIn, X e Salesflare mantengono il loro ritmo.

## Ultimo controllo

Dopo un controllo che ha letto nuovi messaggi, una riga sopra le tue attività dice cosa ha trovato in tutte le fonti, come “13 messaggi controllati alle 16:11 · nulla ha bisogno di te” o “· 2 nuove attività”. Quando una nuova attività aspetta un momento migliore, come il tuo riepilogo del mattino, dice fino a quando: “1 attività in attesa fino a domani 08:30”.

Tocca la riga per vedere ogni conversazione, chat e notifica, con l’icona della sua fonte: chi ha scritto, l’oggetto o le prime parole, e la sua nuova attività o perché non serviva nulla, come “Solo in copia, risponde un collega” o “Riunione già fissata per giovedì”. Una conversazione non mostra un motivo quando il controllo ne ha dato solo uno vago. Toccane una per leggerla.

Si vedono le prime 10, e un tocco sotto mostra le altre. Un numero dopo un nome, come (3), è quanti messaggi nuovi ha quella chat. Una notifica del telefono su un messaggio già in elenco compare una volta sola. La riga resta per 12 ore dopo il controllo.

Conta solo le email indirizzate a te. Le tue risposte vengono lette per il contesto e le promesse, ma non sono email nuove. Le email che la tua Machine ti manda, come il tuo riepilogo del mattino o un avviso di correzione, non vengono mai lette né elencate. Le email su pagamenti, la tua prova o un invito vengono lette come sempre.

## I pulsanti

Un'attività mostra il passo successivo, come **Fallo** o **Rivedi e invia**, con **Posticipa** accanto. Vedi [Fallo](do-it.md) e [Posticipa](snooze.md).

**Chiedi modifiche** dice cosa cambiare: come farla, o, con una bozza pronta, cosa cambiarci. Se sul telefono la riga è piena, **Posticipa** passa in **…**. C'è anche **Segna come fatto** (è sistemata): in vista su una pronta senza bozza, altrimenti in cima a **…**, anche su una che aspetta la tua decisione. Esce subito dall’elenco, con **Annulla** nel messaggio. Scorri via il messaggio, o trascinalo via con il mouse, per chiuderlo prima. La modifica resta.

Per farla in un altro modo, dillo nella sua **Chat**.

In **…** (sul telefono si apre dal fondo dello schermo):

- **Passa…**: passala a un collega, a [Claude Code o Codex](hand-to-agent.md) (quelli che hai configurato) o [chiedi a qualcuno di rivederla](ask-to-review.md).
- **Ripeti…**: [torna con un ritmo](recurring.md).
- **Non serve**: sparisce. Scegli il motivo, se vuoi: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine ne impara.

Tocca il titolo, o **Nome** in **Dettagli**, per rinominarla. Il tuo titolo resta, anche quando l'attività cambia.

Un'attività chiusa può tornare con **Riapri**. Torna anche da sola quando succede qualcosa di nuovo, come un nuovo messaggio dall'altra persona. La tua risposta non la fa tornare.

Una fattura che devi ancora pagare tu, da qualsiasi paese, diventa un’attività con l’importo, la scadenza e i dati di pagamento della fattura. Quelle pagate in automatico, come un addebito diretto o una carta salvata, no. Se un’email successiva mostra che è pagata, ad esempio il mittente conferma di aver ricevuto il pagamento, l’attività si chiude da sola. **Annulla** la riporta indietro per un giorno.

Un'attività che contava solo fino a un certo momento, come una conferma prima di una riunione, si chiude da sola quando quel momento è passato. Passa tra quelle fatte con "Non serve più" e quando era. **Annulla** la riporta indietro per un giorno.

Prima che un messaggio o un passaggio per qualcuno appaia pronto, la tua Machine controlla le tue chat recenti con le persone coinvolte, anche di gruppo, e aspetta che Slack le legga. Se un messaggio successivo mostra che è già fatto, ad esempio la persona è stata già chiesta e ha detto sì, l’attività si chiude da sola. **Annulla** la riporta indietro per un giorno.

Quando un messaggio più recente cambia il piano, come una festa spostata altrove o una prenotazione annullata, The Machine aggiorna da sola le sue attività. Una che conta ancora segue il nuovo piano. Una in cui non resta niente da fare passa tra quelle fatte come "Non serve", la sua chat dice "Aggiornato:" e perché, e **Annulla** la riporta indietro per un giorno.

Sulle tue prime attività, una riga breve sotto i pulsanti mostra l'essenziale: **Chiedi modifiche** e **Non serve** quando un'attività non è proprio giusta, e sulla tua prima bozza pronta, che non parte nulla finché non premi **Invia**. Un suggerimento sparisce per sempre appena usi il suo pulsante o premi ×, su tutti i tuoi dispositivi.

Il primo giorno, la parte alta delle Attività ti saluta per nome e mostra chi aspetta la tua risposta da più tempo. The Machine prepara prima quella risposta, così è pronta quando arrivi. Non parte nulla finché non la invii. La riga sparisce dopo il primo giorno o la prima attività decisa.

Ogni attività inizia con il suo titolo. La riga sotto dice chi riguarda, l'organizzazione quando riguarda una (mai solo perché qualcuno ci lavora), il progetto, Lavoro o Personale (sotto **Tutti**) e quando è arrivata, più a che punto è quando il suo gruppo non lo dice già. Tocca un nome per aprirne la pagina nel Graph.

Un nome e un'organizzazione mostrano la loro foto o il loro logo quando il Graph ne ha uno. Altrimenti mostrano le iniziali. Un logo che così piccolo non si leggerebbe, come bianco su sfondo trasparente o una scritta molto larga, mostra anche lui l'iniziale.

A volte una riga discreta sotto il testo dice cosa non si sa, come «Ultimo contatto 12 giorni fa via email; niente da allora.» Compare solo quando l'ultimo contatto è vecchio o ancora senza risposta, e nomina i canali non collegati dove potrebbero aver risposto, come WhatsApp. La tua Machine prepara con gli stessi fatti, quindi dice cosa non sa invece di tirare a indovinare.

Quando nomina un canale non collegato, Collega accanto apre quel collegamento.

Un titolo dice cosa c'è da fare. Cambia solo quando cambia quello, come per una nuova richiesta. Un'attività fatta mantiene il suo titolo, con sotto come è finita, come cosa è stato inviato o "Fatto: Sam ha firmato martedì".

Sopra la bozza, una riga discreta indica il messaggio da cui viene, con il logo del servizio (Gmail, Slack, WhatsApp…). Toccala per leggere la conversazione. La bozza inizia con il logo di dove va, così vedi se è una risposta su Slack o un'email prima di leggere. Un passo senza bozza, come un passaggio, mostra il logo sul suo pulsante.

Quando la bozza segue l'indicazione di qualcun altro in un altro messaggio, come il suggerimento di un collega su Slack, una riga sotto l'attività lo dice, come "Secondo Sam in #ops". Toccala per leggere quel messaggio qui, con Apri in Slack o Gmail all'interno. Se quel messaggio è la fonte dell'attività stessa, la riga della fonte lo mostra già e non c'è una seconda riga.

Una chat (Slack, WhatsApp, Telegram, Intercom…) si legge come un'unica conversazione, dal più vecchio, ogni messaggio una volta; il messaggio di cui parla l'attività è sotto "Questa attività". In WhatsApp, Telegram o Signal i tuoi messaggi stanno a destra, come nell'app.

In un'email, **Dettagli** mostra solo ciò che l'intestazione non dice, come gli indirizzi Cc completi, Ccn o un altro indirizzo di risposta; se non c'è nulla da aggiungere, non compare.

Una risposta in un thread di Slack mostra anche cosa è stato detto prima del thread. Un link dell'attività al suo messaggio lo apre anche qui, con **Apri in Slack** in fondo.

**Dettagli** mostra nome, progetto e area (toccane uno per cambiarlo), la tua ultima nota e il risultato di un agente di codice. **Chat ›** alla fine di quella riga apre la chat. Un'attività fatta resta breve: il titolo, una riga e cosa è partito; il messaggio da cui viene è nei suoi **Dettagli**.

Un'attività "In attesa di" (qualcuno ti ha promesso qualcosa) ha il link al tuo ultimo messaggio a quella persona, quello a cui aspetti risposta: "Email a Pat · mar".

## Creane una tu

**Nuova attività** (sotto **Cerca** su un computer) aggiunge un'attività per qualsiasi cosa. Crearla non invia niente. Senza Lavoro o Personale, va dove deve: in base a chi e a cosa riguarda, a un'azienda o casella che nomina, o all'email a cui dà seguito. Se niente lo indica, parte dove sono la maggior parte delle tue attività. The Machine cerca quell'email nella tua casella, anche quelle più vecchie non ancora importate.

- **Scadenza**: scrivi un giorno o un'ora, come "domani", "ven prossimo", "3 nov", "15:00", "2pm", "tra 2 ore" o "domani 9". Capisce anche altre lingue ("over 2 uur", "morgen 9u"). L'icona del calendario ha scelte rapide, come quando posticipi, e **Scegli una data**.
- **Messaggio**: allega il messaggio a cui si riferisce: un'email, Slack, Teams, WhatsApp, Telegram o qualsiasi altro messaggio che The Machine ha. Cerca per testo o mittente. Ogni risultato mostra da dove arriva, chi l'ha inviato e quando.
- **File**: tocca la graffetta nel riquadro, incolla uno screenshot o trascina i file sul modulo. Su un telefono, la fotocamera accanto scatta una foto. Fino a 5 file, degli stessi tipi e dimensioni della chat (vedi [Aggiungi file](card-chat.md#add-files)). × ne toglie uno.

I file restano con l'attività: compaiono sull'attività e nella sua chat, e The Machine li legge quando ci lavora. Bastano i file: The Machine legge il testo di un PDF o di un file di testo e compila l’attività da lì. Una foto appare come una piccola immagine: toccala per vederla a schermo intero.
