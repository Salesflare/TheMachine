---
title: Modello
area: settings
summary: Quale modello di IA ti risponde, quanto ragiona e quanto ha usato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: a6db52984a6fddeb
---
**Impostazioni**, **Modello** mostra quale modello di IA svolge il tuo **Lavoro in background** e come hai effettuato l’accesso, ad esempio con ChatGPT.

Su una Machine ospitata con un accesso a ChatGPT, il modello principale è GPT-6.2 Sol: risponde più velocemente di GPT-6.1 Sol allo stesso prezzo.

Un piano personale di ChatGPT o Claude potrebbe usare le tue chat per addestrare i modelli per impostazione predefinita: **Disattiva l’addestramento con i tuoi dati** apre l’impostazione del provider, mentre **Fatto** nasconde la riga.

## Modello e ragionamento nelle chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per la sezione Aiuto. Vedrai solo i modelli e i livelli disponibili con il tuo accesso.

Più ragionamento aiuta a rispondere meglio alle domande difficili, ma è più lento e consuma una parte maggiore del tuo piano. **Ragionamento ultra** usa assistenti per le domande più difficili e consuma di più. Una nuova Machine parte da **Ragionamento basso**: offre buoni risultati consumando molto meno del tuo piano. La modifica si applica dal messaggio successivo.

Per modificarlo solo per una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Seleziona di nuovo **Impostazioni** per seguire le impostazioni.

I controlli, il tuo profilo e le bozze preparate in anticipo mantengono il proprio modello.

## Limiti

Se il tuo piano ha limiti di utilizzo, come i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, vedrai quanto ne hai usato e quando si azzera ciascun limite. Consultare questa schermata non consuma il tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si mette in pausa quando raggiunge circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; le altre attività usano circa un settimo del limite settimanale al giorno. Un accesso senza limiti, come una chiave API, non mette mai in pausa il lavoro.

Il lavoro in background non viene mai eseguito su GPT-6 Astra. Per ora, con un accesso a ChatGPT usa GPT-6.1 Sol anche quando il modello principale è GPT-6.2 Sol: con quell’accesso, 6.2 non riutilizza ancora le istruzioni memorizzate nella cache, quindi consuma di più del tuo piano. Le tue chat mantengono il modello che hai scelto.

## Quando si raggiunge un limite

Nella parte superiore della dashboard viene indicato quale limite è stato raggiunto e quando si azzera. Il lavoro resta in attesa, poi riprende da dove si era interrotto. Non perdi nulla. Se il tuo piano ChatGPT consente gli azzeramenti, **Usa un azzeramento** azzera i limiti. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva associato a un altro piano o provider, subentra quando si raggiunge un limite e il lavoro non resta in attesa. Nella parte superiore della dashboard viene indicato «Limite di ChatGPT raggiunto, uso il modello di riserva». Se il modello di riserva smette di funzionare, il lavoro torna a essere messo in pausa.

## Modificare il modello principale

Il modello principale è quello usato dal resto di The Machine. Su una Machine ospitata, puoi modificarlo nella pagina di configurazione, in La tua IA. Sul tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
