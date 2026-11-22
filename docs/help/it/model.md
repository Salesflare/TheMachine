---
title: Modello
area: settings
summary: Quale modello di IA ti risponde, quanto ragiona e quanto ha consumato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: d63ec55d8d0339e6
---
In **Impostazioni**, **Modello** mostra quale modello di IA svolge il **Lavoro in background** e con quale account hai effettuato l’accesso, per esempio ChatGPT.

Su una Machine ospitata con un accesso a ChatGPT, il modello principale è GPT-6.2 Sol: risponde più velocemente di GPT-6.1 Sol allo stesso prezzo.

Per impostazione predefinita, un piano personale di ChatGPT o Claude potrebbe usare le tue chat per l’addestramento. **Disattiva l’addestramento con i tuoi dati** apre questa impostazione presso il provider, mentre **Fatto** nasconde la riga.

## Modello e ragionamento nelle chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’Aiuto. Vedi solo i modelli e i livelli disponibili con il tuo account.

Un ragionamento più approfondito migliora le risposte alle domande difficili, ma è più lento e usa più risorse del tuo piano. **Ragionamento ultra** usa assistenti per le domande più difficili e consuma più risorse. Una nuova Machine parte da **Ragionamento basso**: dà buoni risultati consumando molte meno risorse del tuo piano. Le modifiche si applicano dal messaggio successivo.

Per cambiarlo solo per una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Seleziona di nuovo l’opzione delle Impostazioni per seguire le Impostazioni.

I controlli, il tuo profilo e le bozze preparate in anticipo mantengono il proprio modello.

## Limiti

Se il tuo piano prevede limiti di utilizzo, come i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, qui vedi quanto ne hai usato e quando si azzera ciascun limite. Consultare questa sezione non consuma le risorse del tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si mette in pausa quando raggiungi circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; gli altri lavori consumano ogni giorno circa un settimo del limite settimanale. Un accesso senza limiti, come una chiave API, non mette mai in pausa il lavoro.

Il lavoro in background non viene mai svolto con GPT-6 Astra. Per ora, con un accesso a ChatGPT usa GPT-6.1 Sol, anche se il tuo modello principale è GPT-6.2 Sol: con questo accesso, 6.2 non riutilizza ancora le istruzioni memorizzate nella cache, quindi consuma più risorse del tuo piano. Le tue chat continuano a usare il modello che hai scelto.

## Prima di raggiungere un limite

Se il tuo piano ChatGPT ha degli azzeramenti disponibili, in Attività compare una breve riga quando il lavoro in background rallenta: intorno al 65% del limite di 5 ore o al 90% del limite settimanale. La riga indica quanto hai usato e quanti azzeramenti restano. **Usa un azzeramento** azzera i limiti dopo la tua conferma. × nasconde la riga fino al successivo azzeramento del limite. Se non hai azzeramenti disponibili, non compare nulla.

## Quando raggiungi un limite

In cima alla dashboard trovi il limite raggiunto e quando si azzera. Il lavoro si ferma, poi riprende da dove si era interrotto. Non perdi nulla. Se il tuo piano ChatGPT include degli azzeramenti, **Usa un azzeramento** azzera i limiti. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva associato a un altro piano o provider, subentra quando raggiungi un limite e il lavoro non si ferma. In cima alla dashboard compare «Limite ChatGPT raggiunto, uso il modello di riserva». Se il modello di riserva smette di funzionare, il lavoro torna a essere messo in pausa.

## Cambiare il modello principale

Il modello principale è quello usato dal resto di The Machine. Su una Machine ospitata, puoi cambiarlo nella pagina di configurazione, sotto La tua IA. Sul tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
