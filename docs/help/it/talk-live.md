---
title: Parla dal vivo
area: cards
summary: Una conversazione vocale con The Machine su un’attività, con la voce di OpenAI. Funziona nella chat dell’attività e invia una bozza solo dopo la tua conferma.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: f5555cb693a23682
---
## Avvia una conversazione

Nella chat di un’attività, tocca l’onda accanto al microfono e consenti l’accesso al microfono, se richiesto. Quando la barra mostra **Dal vivo**, parla come durante una chiamata. The Machine risponde a voce. Parlale sopra per interromperla.

Conosce questa attività: i messaggi, la bozza e la chat. Può anche cercare informazioni sulle altre tue attività. Di’ «segna come fatto», «posticipa a domani alle 9» o «non serve» e lo farà. Per annullare, di’ «no, non così» subito dopo. Gli orari seguono il fuso orario del tuo [Orario di lavoro](work-hours.md).

Ascolta nella lingua dell’app e nelle lingue indicate dal browser. Tosse, rumori e altre lingue non ricevono risposta e non vengono inclusi nella trascrizione.

Nella barra trovi **Silenzia** e **Termina**. Se la saluti, la conversazione termina da sola. Può durare fino a 10 minuti; nell’ultimo minuto compare un conto alla rovescia. Riavviala per continuare.

## Parla di tutte le tue attività

Tocca **Parla** nella barra laterale, oppure nel menu sul telefono. The Machine ti dice quante attività sono in attesa e passa una alla volta a quelle in **Per te**, nell’ordine in cui compaiono nell’elenco. Ti avvisa quando un’attività contrassegnata come **In preparazione…** è pronta.

Parla ha una pagina dedicata: l’attività su cui stai lavorando compare in alto, con la bozza e **Apri la chat**.

Chiedile di leggere una bozza, modificarla, posticiparla, segnarla come fatta o passare alla successiva. Quello che dici su un’attività viene aggiunto alla sua chat. Ti segnala le nuove attività durante una pausa. Di’ «aggiungi un’attività per...» per aggiungerne una senza perdere il punto in cui eri arrivato.

Chiedile di cercare una persona, un’organizzazione, un progetto, una riunione o una promessa: la cercherà e te la mostrerà. Può anche scartare, rinominare o riaprire attività, comprese quelle in **Fatte / scartate**. Per qualsiasi altra cosa, passa la domanda alla chat di una nuova attività e ti comunica la risposta.

Ricorda le conversazioni precedenti. Chiedile «cosa avevo deciso per il ritiro?» e ti dirà cosa hai deciso e quando. Questa funzione è disponibile solo da **Parla** nella barra laterale.

Nel frattempo puoi aprire altre pagine: la barra resta in fondo e **Parla** ti riporta alla conversazione. Questa può durare fino a 30 minuti. Sui computer e su Android continua in background. Su iPhone si interrompe quando l’app non è più sullo schermo.

## Chiedi qualcosa e invia dopo aver confermato

Chiedile di fare qualcosa, per esempio «scrivi una risposta per dire che giovedì va bene», e The Machine inoltrerà la richiesta alla chat dell’attività come se l’avessi digitata. La chat seguirà le sue solite regole.

La chat può anche cercare informazioni, per esempio gli orari di apertura di un negozio. Mostra **Ci sto lavorando…** e puoi continuare a parlare. Quando la risposta è pronta, The Machine te la comunica e ti dice dove l’ha trovata.

Per inviare una bozza, dillo a voce. The Machine la legge ad alta voce, indicando il destinatario, l’oggetto e il testo, poi chiede, per esempio: «Invio questa risposta a Sam via email?». Puoi farlo anche con il telefono in tasca. Rispondi con un sì chiaro, come «sì, inviala», e la bozza verrà inviata.

- Invia esattamente la bozza che ha letto. Se la bozza cambia, la legge e chiede di nuovo. Se non rispondi entro 3 minuti, la richiesta scade.
- Se non dai una conferma chiara, non viene inviato nulla.
- Se hai già visto o ascoltato una bozza, non viene letta di nuovo. Ti viene solo chiesto, per esempio: «La invio a Pat?».
- Di’ «invia tutte quelle pronte» e ti dirà tutti i destinatari in un’unica domanda. Un solo sì le invia tutte.
- Dopo la conferma, Parla mostra **Annulla** con un conto alla rovescia. Toccalo oppure di’ «annulla» o «aspetta».
- Una volta inviata la bozza, Parla dice «Inviata» e nell’attività compare **Inviato a** quella persona, con l’ora. Se l’invio non riesce, Parla ti spiega perché. Puoi chiedere «è stata inviata?» in qualsiasi momento: verifica, non tira a indovinare.

Puoi anche toccare **Approva**.

Di’ «fallo» per avviare The Machine sull’attività, come con **Fallo**. Di’ «segnala un bug» per inviare una segnalazione, come con **Segnala un bug** nella sezione Aiuto.

## Scegli una voce

In **Impostazioni**, **Generale**, alla voce **Input vocale**, scegli una **Voce** e tocca Riproduci per ascoltarla. **Cedar** è la voce predefinita. La voce Cove di ChatGPT non è disponibile.

## Una registrazione nella chat

Tutto quello che dici viene aggiunto alla chat dell’attività, sotto la voce **Conversazione dal vivo**, così puoi rileggerlo in seguito.

## Requisiti

Parla dal vivo usa la voce di OpenAI, quindi la tua Machine ha bisogno di una di queste opzioni:

- Un accesso a ChatGPT: incluso nei piani che lo prevedono.
- Una chiave API di OpenAI: OpenAI la addebita al minuto e la barra te lo segnala. Se hai entrambe le opzioni, la tua Machine usa la chiave.

In **Impostazioni**, **Generale**, **Input vocale** puoi vedere se Parla dal vivo è pronto. Senza OpenAI, l’icona a forma d’onda non compare. L’audio passa direttamente dal browser a OpenAI.

## Se non funziona

- **Il microfono è bloccato**: consenti l’accesso al microfono per questo sito nelle impostazioni del browser.
- **Parla dal vivo non si è avviato**: controlla l’accesso a ChatGPT o la chiave OpenAI e riprova.
- **Parla dal vivo ha perso la connessione**: riavvialo. Quello che hai detto resta nella chat.
- Se dice che non riesce a capire le tue parole, controlla il microfono oppure scrivi nella chat.
