---
title: Modello
area: settings
summary: Quale modello di IA ti risponde, quanto ragiona e quanto ha consumato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 249d2d7d6c368cfe
---
In **Impostazioni**, **Modello** mostra quale modello di IA svolge il **Lavoro in background** e come hai effettuato l’accesso, per esempio con ChatGPT.

Su una Machine ospitata con accesso a ChatGPT, il modello principale è GPT-6.2 Sol: risposte più rapide di GPT-6.1 Sol allo stesso prezzo.

Per impostazione predefinita, un piano personale di ChatGPT o Claude potrebbe usare le tue chat per l’addestramento. **Disattiva l’addestramento con i tuoi dati** apre questa impostazione sul sito del provider, mentre **Fatto** nasconde la riga.

## Modello e ragionamento nelle chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’Aiuto. Vedrai solo i modelli e i livelli disponibili con il tuo accesso.

Più ragionamento aiuta a rispondere meglio alle domande difficili, ma è più lento e consuma più risorse del tuo piano. **Ragionamento ultra** coinvolge assistenti per le domande più difficili e consuma più risorse di tutti. Una nuova Machine inizia con **Ragionamento basso**: buoni risultati consumando molte meno risorse del tuo piano. Le modifiche si applicano dal messaggio successivo.

Per modificarlo solo per una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Seleziona di nuovo l’opzione **Impostazioni** per usare le impostazioni generali.

I controlli, il tuo profilo e le bozze preparate in anticipo mantengono il proprio modello.

## Limiti

Se il tuo piano ha limiti di utilizzo, come i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, vedrai quanto ne hai usato e quando si azzera ciascun limite. Consultare questa pagina non consuma risorse del tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si mette in pausa quando raggiunge circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; le altre attività usano circa un settimo del limite settimanale al giorno. Un accesso senza limiti, come una chiave API, non si mette mai in pausa.

Il lavoro in background non usa mai GPT-6 Astra. Usa invece GPT-6.2 Sol, oppure GPT-6.1 Sol se 6.2 non è configurato.

## Quando si raggiunge un limite

In cima alla dashboard trovi il limite raggiunto e quando si azzera. Il lavoro resta in attesa, poi riprende da dove si era interrotto. Non si perde nulla. Se il tuo piano ChatGPT prevede azzeramenti, **Usa un azzeramento** azzera di nuovo i limiti. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva su un altro piano o provider, subentra quando si raggiunge un limite e il lavoro non resta in attesa. In cima alla dashboard trovi «Limite ChatGPT raggiunto, uso il modello di riserva». Se il modello di riserva smette di funzionare, tornano le pause.

## Cambiare il modello principale

Il modello principale è quello che usa il resto della Machine. Su una Machine ospitata, modificalo nella pagina di configurazione, alla voce «La tua IA». Sul tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
