---
title: Parla dal vivo
area: cards
summary: Una conversazione a voce con The Machine su un’attività, con la voce di OpenAI. Può cercare informazioni e dare suggerimenti, ma non invia mai niente.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Inizia una conversazione

Nella chat di un’attività, tocca l’onda accanto al microfono. Consenti il microfono se il browser lo chiede. Quando la barra dice **Dal vivo**, parla come in una chiamata. The Machine risponde ad alta voce.

Conosce l’attività in cui sei: i suoi messaggi e la sua bozza. Può anche consultare le tue altre attività.

La barra ha **Silenzia** e **Fine**. Una conversazione dura al massimo 10 minuti. Un minuto prima della fine, il timer mostra quanto manca. Riavviala per continuare.

## Da una conversazione non parte niente

The Machine non può inviare, cambiare o approvare niente mentre parli. Quando chiedi qualcosa, come "scrivi una risposta dicendo che giovedì va bene", mostra la richiesta sopra la barra. Tocca **Invia alla chat** per passarla alla chat. Quello che la chat scrive poi aspetta il tuo **Approva**, come sempre.

Dire "sì" o "invialo" non fa niente. Contano solo i tuoi tocchi.

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
