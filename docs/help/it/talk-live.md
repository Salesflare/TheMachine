---
title: Parla dal vivo
area: cards
summary: Una conversazione vocale con The Machine su un’attività, con la voce di OpenAI. Funziona nella chat dell’attività e invia una bozza solo dopo che hai detto sì.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: 60168384f08de74e
---
## Avvia una conversazione

Nella chat di un’attività, tocca l’onda accanto al microfono e consenti l’accesso al microfono, se richiesto. Quando la barra mostra **Dal vivo**, parla come durante una chiamata. La Machine ti risponde a voce. Parlale sopra per interromperla.

Conosce questa attività: i suoi messaggi, la bozza e la chat. Può anche cercare informazioni sulle altre tue attività. Di’ «segnala come fatta», «posticipala a domani alle 9» o «non serve» e lo farà. Per annullare, di’ «no, non così» subito dopo. Gli orari seguono il fuso orario del tuo [Orario di lavoro](work-hours.md).

Ascolta nella lingua dell’app e nelle lingue indicate dal browser. Tosse, rumori e altre lingue non ricevono risposta e non compaiono nella trascrizione.

La barra include **Silenzia** e **Fine**. Se saluti, la conversazione termina da sola. Dura fino a 10 minuti, con un conto alla rovescia nell’ultimo minuto. Riavviala per continuare.

## Parla di tutte le tue attività

Tocca **Parla** nella barra laterale, oppure nel menu su telefono. La Machine ti dice quante attività sono in attesa e prende una alla volta quelle in **Per te**, partendo dalla più urgente. Ti avvisa quando un’attività contrassegnata **In preparazione…** è pronta.

Parla ha una pagina dedicata: l’attività su cui sta lavorando è in alto, con la sua bozza e **Apri la chat**.

Chiedile di leggere una bozza, modificarla, posticiparla, segnarla come fatta o passare alla successiva. Quello che dici su un’attività viene aggiunto alla sua chat. Ti segnala le nuove attività quando c’è una pausa. Di’ «aggiungi un’attività per...» per aggiungerne una senza perdere il segno.

Chiedile informazioni su una persona, un’organizzazione, un progetto, una riunione o una promessa: le cercherà e te le mostrerà. Può anche scartare, rinominare o riaprire attività, comprese quelle in **Fatte / scartate**. Per qualsiasi altra cosa, invia la domanda alla chat di una nuova attività e poi ti dà la risposta.

Ricorda le conversazioni precedenti. Chiedile «cosa avevo deciso per il ritiro aziendale?» e ti risponderà, dicendoti anche quando ne avevi parlato. Solo Parla nella barra laterale può farlo.

Nel frattempo puoi usare le altre pagine: la barra resta in basso e **Parla** ti riporta alla conversazione. Questa conversazione dura fino a 30 minuti. Continua in background su computer e Android. Su iPhone si interrompe quando l’app esce dallo schermo.

## Chiedi quello che ti serve e invia con un sì

Chiedi qualcosa, per esempio «scrivi una risposta per dire che giovedì va bene», e The Machine lo invierà alla chat dell’attività come se l’avessi scritto tu. La chat segue le sue solite regole.

La chat può anche cercare informazioni, come gli orari di apertura di un negozio. Mostra **Ci sto lavorando…** e puoi continuare a parlare. Quando la risposta è pronta, The Machine te la comunica e ti dice dove l’ha trovata.

Per inviare una bozza, chiediglielo. The Machine la legge ad alta voce, indicando a chi è indirizzata, l’oggetto e il testo, poi ti chiede, per esempio: «Invio questa risposta via email a Sam?». Puoi farlo anche con il telefono in tasca. Di’ chiaramente di sì, per esempio «sì, inviala», e la bozza verrà inviata.

- Invia esattamente la bozza che ha letto. Se la bozza cambia, la legge e te lo chiede di nuovo. Se non rispondi entro 3 minuti, la richiesta scade.
- Se non dai un sì chiaro, non viene inviato nulla.
- Una bozza che hai già visto o sentito non viene riletta. Ti chiede solo, per esempio: «La invio a Pat?».
- Di’ «invia tutte quelle pronte» e indicherà tutti i destinatari in un’unica domanda. Basta un sì per inviarle tutte.
- Dopo che hai detto sì, Parla mostra **Annulla** con un conto alla rovescia. Toccalo oppure di’ «annulla» o «aspetta».
- Una volta inviata la bozza, Parla dice «Inviata» e l’attività mostra **Inviato a** quella persona, con l’ora. Se l’invio non riesce, Parla ti dice perché. Puoi chiedere «è stata inviata?» in qualsiasi momento: controlla, non tira a indovinare.

Puoi anche toccare **Approva**.

Di’ «fallo» per avviare The Machine sull’attività, come con **Fallo**. Di’ «segnala un bug» per inviare una segnalazione, come con **Segnala un bug** nella sezione Aiuto.

## Scegli una voce

In **Impostazioni**, **Generale**, alla voce **Input vocale**, scegli una **Voce** e tocca Riproduci per ascoltarla. **Cedar** è la voce predefinita. La voce Cove di ChatGPT non è disponibile.

## Una registrazione nella chat

Tutto quello che viene detto viene aggiunto alla chat dell’attività, sotto la voce **Conversazione dal vivo**, così puoi rileggerlo in seguito.

## Cosa serve

Parla dal vivo usa la voce di OpenAI, quindi la tua Machine deve avere una di queste opzioni:

- Accesso a ChatGPT: incluso nei piani che lo prevedono.
- Una chiave API OpenAI: OpenAI la addebita al minuto e la barra te lo segnala. Se hai entrambe le opzioni, la tua Machine usa la chiave.

In **Impostazioni**, **Generale**, **Input vocale** puoi vedere se Parla dal vivo è pronto. Senza OpenAI, l’onda non viene mostrata. L’audio passa direttamente dal browser a OpenAI.

## Se non funziona

- **Il microfono è bloccato**: consenti l’accesso al microfono per questo sito nelle impostazioni del browser.
- **Parla dal vivo non si è avviato**: controlla l’accesso a ChatGPT o la chiave OpenAI, poi riprova.
- **Parla dal vivo ha perso la connessione**: riavvialo. Quello che è stato detto resta nella chat.
- Dice che non riesce a capire le tue parole: controlla il microfono oppure scrivi nella chat.
