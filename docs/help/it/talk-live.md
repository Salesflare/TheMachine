---
title: Conversazione dal vivo
area: cards
summary: Una conversazione a voce con The Machine su un’attività, con la voce di OpenAI. Funziona nella chat dell’attività e invia una bozza solo dopo che dai il tuo consenso.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: da63957f0556ff4f
---
## Avvia una conversazione

Nella chat di un’attività, tocca l’onda accanto al microfono e consenti l’accesso al microfono, se richiesto. Quando la barra indica **Dal vivo**, parla come durante una chiamata. The Machine risponde a voce. Parlale sopra per interromperla.

Conosce questa attività: i suoi messaggi, la bozza e la chat, e può cercare anche le altre tue attività. Di’ «segna come completata», «posticipala a domani alle 9» o «non serve» e lo farà. Di’ subito «no, non così» per annullare. Gli orari seguono il fuso orario delle tue [Orario di lavoro](work-hours.md).

Ascolta nella lingua dell’app e nelle lingue indicate dal browser. Colpi di tosse, rumori e altre lingue non ricevono risposta e non compaiono nella trascrizione.

La barra include **Silenzia** e **Termina**. Di’ «arrivederci» e la conversazione terminerà da sola. La conversazione dura al massimo 10 minuti, con un conto alla rovescia nell’ultimo minuto. Ricomincia per continuare.

## Parla con tutte le tue attività

Tocca **Parla** nella barra laterale, oppure nel menu su un telefono. The Machine ti dice quante attività sono in attesa e gestisce una alla volta quelle in **Per te**, nell’ordine in cui compaiono nell’elenco. Ti avvisa quando un’attività **In preparazione…** è pronta.

La modalità Parla ha una pagina dedicata: l’attività corrente è in alto, insieme alla sua bozza e a **Apri la chat**.

Chiedile di leggere una bozza, modificarla, posticiparla, segnarla come completata o passare alla successiva. Quello che dici su un’attività viene inserito nella sua chat. Ti segnala le nuove attività quando c’è una pausa. Di’ «aggiungi un’attività per…» per aggiungerne una senza perdere il segno.

Chiedi informazioni su una persona, un’organizzazione, un progetto, una riunione o una promessa: le cercherà e te le mostrerà. Può anche scartare, rinominare o riaprire le attività, comprese quelle in **Fatte / scartate**. Per qualsiasi altra richiesta, invia la domanda alla chat di una nuova attività e ti comunica la risposta.

Ricorda le conversazioni precedenti. Chiedi «che cosa avevo deciso per l’incontro fuori sede?» e ti dirà cosa hai deciso e quando. Solo la modalità Parla nella barra laterale può farlo.

Nel frattempo puoi visitare altre pagine: la barra resta in basso e **Parla** ti riporta alla conversazione. Questa conversazione dura al massimo 30 minuti. Continua in background su computer e Android. Su iPhone, si interrompe quando l’app esce dallo schermo.

## Fai una richiesta e invia dopo aver confermato

Chiedi qualcosa, per esempio «scrivi una risposta per dire che giovedì va bene», e The Machine invia la richiesta alla chat dell’attività come se l’avessi digitata. La chat segue le sue regole abituali.

La chat può anche cercare informazioni, per esempio gli orari di apertura di un negozio. Ti mostra che sta lavorando e puoi continuare a parlare. Quando la risposta è pronta, The Machine te lo dice e ti indica dove l’ha trovata.

Per inviare una bozza, chiedilo. The Machine la legge ad alta voce, indicando a chi è destinata, l’oggetto e il testo, poi ti chiede, per esempio: «Invio questa risposta via email a Sam?». Puoi tenere il telefono in tasca. Rispondi con un sì chiaro, per esempio «sì, inviala», e la bozza verrà inviata.

- Invia esattamente la bozza che ha letto. Se la bozza cambia, la legge e te lo chiede di nuovo. Se non rispondi entro 3 minuti, la richiesta scade.
- Se non dai un sì chiaro, non invia nulla.
- Se hai già visto o ascoltato una bozza, non la legge di nuovo. Ti chiede solo, per esempio: «La invio a Pat?».
- Di’ «invia tutte quelle pronte» e ti dirà i nomi di tutti in un’unica domanda. Un solo sì le invia tutte.
- Dopo il tuo sì, Parla mostra **Annulla** con un conto alla rovescia. Toccala oppure di’ «annulla» o «aspetta».
- Una volta inviata, Parla dice «Inviato.» e nell’attività compare **Inviato a** quella persona, con l’orario. Se l’invio non riesce, Parla ti spiega perché. Puoi chiedere «è stata inviata?» in qualsiasi momento: verifica, non tira a indovinare.

Puoi anche toccare **Approva**.

Di’ «fallo» per avviare The Machine sull’attività, come con **Fallo**. Di’ «segnala un bug» per inviare una segnalazione, come con **Segnala un bug** nella sezione Aiuto.

## Scegli una voce

In **Impostazioni**, **Generale**, alla voce **Input vocale**, scegli una **Voce** e tocca play per ascoltarla. **Cedar** è la voce predefinita. La voce Cove di ChatGPT non è disponibile.

## Una registrazione nella chat

Tutto quello che viene detto compare nella chat dell’attività, sotto la voce **Conversazione dal vivo**, così puoi rileggerlo in seguito.

## Requisiti

La conversazione dal vivo usa la voce di OpenAI, quindi la tua Machine deve avere una di queste opzioni:

- Accesso a ChatGPT: incluso nei piani che lo prevedono.
- Una chiave API OpenAI: OpenAI la addebita al minuto e la barra lo indica. Se sono disponibili entrambe le opzioni, la tua Machine usa la chiave.

In **Impostazioni**, **Generale**, **Input vocale** puoi vedere se la conversazione dal vivo è pronta. Senza OpenAI, l’icona dell’onda non compare. L’audio passa direttamente dal browser a OpenAI.

## Se non funziona

- **Il microfono è bloccato**: consenti l’accesso al microfono per questo sito nelle impostazioni del browser.
- **La conversazione dal vivo non si avvia**: controlla l’accesso a ChatGPT o la chiave OpenAI e riprova.
- **La conversazione dal vivo ha perso la connessione**: ricomincia. Quello che è stato detto resta nella chat.
- Se dice che non riesce a capire le tue parole, controlla il microfono oppure scrivi nella chat.
