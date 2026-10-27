---
title: Modello
area: settings
summary: Quale modello di IA risponde per te, quanto ragiona e quanto ha usato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
---
In **Impostazioni**, **Modello** mostra il modello usato dal lavoro in background (indicato con **Lavoro in background**) e come hai effettuato l’accesso, per esempio con ChatGPT.

## Modello e ragionamento per le chat

In **Chat**, scegli il modello e il livello di ragionamento che usano le chat delle tue attività e l’Aiuto. L’elenco ha solo i modelli offerti dal tuo accesso, come quelli di ChatGPT se hai effettuato l’accesso con ChatGPT, e ogni modello solo i livelli che ha.

Più ragionamento risponde meglio alle domande difficili, ma è più lento e usa di più il tuo piano. **Ragionamento ultra** chiama degli aiutanti per le domande più difficili: è il più lento e quello che usa di più. Una modifica vale dal messaggio successivo.

Una chat può usare qualcos’altro: sotto la sua casella del messaggio, tocca il modello o il livello di ragionamento. Quella scelta vale solo per quella chat. Scegli di nuovo lo stesso delle Impostazioni per seguire le Impostazioni.

Le revisioni, il tuo profilo e le bozze preparate in anticipo mantengono il loro modello.

## Limiti

Se il tuo piano ha limiti di utilizzo, mostra quanto hai usato di ciascuno e quando si azzera, per esempio il limite di 5 ore e quello settimanale di un piano ChatGPT o Claude. Leggere questi dati non consuma mai il tuo piano.

## Spazio per le tue chat

Il lavoro in background (revisioni, il tuo profilo, bozze preparate in anticipo) lascia spazio alle tue chat. Si mette in pausa a circa il 65% del limite di 5 ore. Le revisioni di quello che è arrivato continuano fino a circa il 90% del limite settimanale; il resto lo distribuisce a circa un settimo al giorno. Un accesso senza limiti di utilizzo, come una chiave API, non va mai in pausa.

Il lavoro in background non gira mai su GPT-6 Astra. Usa invece GPT-6.1 Sol.

## Quando raggiungi un limite

In cima alla dashboard vedi quale limite è stato raggiunto e quando si azzera. Il lavoro aspetta, poi riprende da dove si era fermato. Non si perde nulla. Alcuni piani ChatGPT includono degli azzeramenti: **Usa un azzeramento** fa ripartire i limiti, dopo una conferma. Altrimenti **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Cambia il modello principale

Il modello principale è quello che usa il resto di The Machine. Su una Machine in hosting, scegline un altro nella tua pagina di configurazione, sotto Il tuo modello. Sul tuo computer, cambialo in OpenClaw. Vedi [ChatGPT](chatgpt.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
