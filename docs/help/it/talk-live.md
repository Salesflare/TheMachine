---
title: Parla dal vivo
area: cards
summary: Una conversazione a voce con The Machine su un’attività, con la voce di OpenAI. Lavora nella chat dell’attività e invia una bozza solo dopo il tuo sì.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Inizia una conversazione

Nella chat di un’attività, tocca l’onda accanto al microfono. Consenti il microfono se il browser lo chiede. Quando la barra dice **Dal vivo**, parla come in una chiamata. The Machine risponde ad alta voce, e puoi parlarle sopra per interromperla.

Conosce l’attività in cui sei: i suoi messaggi, la sua bozza e la sua chat. Può anche consultare le tue altre attività. Di' "segnala come fatta", "rimandala" o "non serve" e lo fa da sola. Di' "no, non quello" subito dopo per tornare indietro.

Ascolta nelle tue lingue: quella dell’app e quelle indicate dal browser. Un rumore, un colpo di tosse o un suono in un’altra lingua non riceve risposta e resta fuori dalla trascrizione.

La barra ha **Silenzia** e **Fine**. Saluta, o di' che hai finito, e si chiude da sola. Una conversazione dura al massimo 10 minuti. Un minuto prima della fine, il timer mostra quanto manca. Riavviala per continuare.

## Ripassa tutte le attività a voce

Tocca **Parla** nella barra laterale (nel menu sul telefono) per ripassare a voce tutto ciò che ti aspetta. The Machine dice quante sono e le prende una alla volta: prima **Pronta**, poi **Da decidere**. Vede anche le altre attività, come quelle ancora **In preparazione**, e ti avvisa quando una è pronta.

Parla ha una pagina sua: una conversazione dall'inizio alla fine, con in alto l'attività di cui si parla, la sua bozza e **Apri la chat**. Non ti sposta da una chat all'altra.

Chiedile di leggere una bozza, cambiarla, rimandarla, segnarla come fatta o passare alla prossima. L'invio funziona come nella chat di un'attività: una bozza per domanda, dopo un sì chiaro. Quello che dici su un'attività finisce nella chat di quell'attività. Quando arriva una nuova attività, te lo dice in una pausa. Di' "aggiungi un'attività per..." e ne crea una nuova, senza lasciare quella su cui sei.

Arriva anche al resto di The Machine. Chiedi di una persona, un'organizzazione, un progetto, una riunione o una promessa, e la cerca e te la mostra. Può rimandare un'attività, segnarla come fatta, ignorarla, rinominarla o riaprirla, anche una in **Fatte / ignorate**. Per tutto il resto crea un'attività, lascia che se ne occupi la sua chat e ti dice la risposta.

Intanto puoi andare su un'altra pagina: la barra resta in basso, e **Parla** nella barra laterale ti riporta indietro. Questa conversazione dura al massimo 30 minuti. Continua in background su computer e Android. Su iPhone si ferma quando l'app lascia lo schermo.

## Chiedi le cose, e invia con un sì

Quando chiedi qualcosa, come "scrivi una risposta dicendo che giovedì va bene" o "posticipa questa a lunedì", The Machine la passa alla chat dell’attività, come se l’avessi scritta tu. La chat segue le solite regole: può cambiare la bozza o posticipare l’attività.

La chat può anche cercare informazioni, come gli orari di un negozio sul web. Nel frattempo mostra **Ci sto lavorando…**, e puoi continuare a parlare. Quando la risposta è pronta, The Machine te la dice, e dove l’ha trovata. Se nel frattempo chiedi altro, aspetta il suo turno.

Per inviare una bozza, dillo. The Machine chiede prima, dicendo a chi e come, per esempio "Invio questa risposta a Lotte per email?". Prima legge ad alta voce tutta la bozza: a chi va, l'oggetto e il testo. Così funziona anche con il telefono in tasca. Rispondi con un sì chiaro, come "sì, invia", e quella bozza parte.

- Invia esattamente la bozza che ha letto. Se cambia dopo la domanda, la rilegge e chiede di nuovo. Una domanda senza risposta entro 3 minuti scade.
- Se la risposta non è un sì chiaro, non parte niente e chiede di nuovo. "No" non invia niente.
- Una bozza che hai già visto sullo schermo, o sentito in questa conversazione, non viene riletta: chiede solo, per esempio "La invio a Nick?".
- Di' "invia entrambe" o "invia tutte quelle pronte" e nomina tutti in una domanda. Un sì le invia tutte.
- Parla dice quanti secondi hai e mostra **Annulla** con lo stesso conto alla rovescia. Toccalo, o di' "annulla" o "aspetta".
- Quando la Machine l’ha inviato, Parla dice "Inviato." e la barra e il to-do mostrano **Inviato a** quella persona con l’orario. Se non è partito, Parla dice perché. Chiedi "è partito?" quando vuoi: controlla, non tira mai a indovinare.

Puoi sempre toccare **Approva** invece.

"Fallo" fa partire The Machine sull’attività, come **Fallo**, anche nel browser. "Segnala come fatta" la chiude. Di' "segnala un bug" e invia una segnalazione, come **Segnala un bug** nell’Aiuto, chiedendo prima se può aggiungere altro.

## Scegli una voce

In **Impostazioni**, **Generale**, sotto **Input vocale**, scegli in **Voce** come suona The Machine. Tocca riproduci per sentire un esempio. **Cedar** è la voce predefinita. La voce Cove di ChatGPT non è disponibile per parlare dal vivo.

## Una traccia nella chat

Quello che dite tutti e due viene scritto nella chat dell’attività, sotto una riga **Conversazione dal vivo**. Puoi rileggerlo più tardi.

## Cosa ti serve

Parla dal vivo usa la voce in tempo reale di OpenAI, quindi OpenAI deve essere configurato in OpenClaw:

- Un accesso ChatGPT: incluso nel tuo piano, se il tuo piano ha accesso.
- Una chiave API OpenAI: OpenAI addebita alla tua chiave ogni minuto di conversazione, e la barra lo dice. Se sono configurati tutti e due, OpenClaw usa la chiave.

**Impostazioni**, **Generale**, **Input vocale** mostra se Parla dal vivo è pronto. Senza OpenAI, l’onda non compare. Il tuo audio va dal browser direttamente a OpenAI. La tua chiave non arriva mai al browser.

## Se non funziona

- **Il microfono è bloccato**: consenti il microfono per questo sito nelle impostazioni del browser.
- **Parla dal vivo non è partito**: controlla OpenAI in OpenClaw, poi riprova.
- **Parla dal vivo ha perso la connessione**: riavvialo. Quello che è stato detto finora resta nella chat.
- Se dice che non capisce le tue parole, quello che hai detto non è arrivato due volte di fila. Controlla il microfono, o scrivi nella chat. Lo dice una volta, poi aspetta di sentirti.
