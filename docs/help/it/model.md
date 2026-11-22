---
title: Modello
area: settings
summary: Quale modello IA ti risponde, quanto ragiona e quanto ha consumato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: ee95ad4fa5323e3a
---
In **Impostazioni**, **Modello** mostra quale modello IA svolge il **Lavoro in background** e come hai effettuato l’accesso, per esempio con ChatGPT.

Su una Machine ospitata con accesso a ChatGPT, il modello principale è GPT-6.2 Sol: risponde più velocemente di GPT-6.1 Sol allo stesso prezzo.

Per impostazione predefinita, un piano personale ChatGPT o Claude potrebbe usare le tue chat per addestrare i modelli. **Disattiva l’addestramento con i tuoi dati** apre l’impostazione sul sito del provider, mentre **Fatto** nasconde la riga.

## Modello e ragionamento per le chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’assistenza. Vedrai solo i modelli e i livelli disponibili con il tuo accesso.

Più ragionamento aiuta a rispondere meglio alle domande difficili, ma è più lento e consuma una parte maggiore del tuo piano. **Ragionamento ultra** coinvolge assistenti per le domande più difficili e consuma più risorse. Una nuova Machine parte da **Ragionamento basso**: offre buoni risultati consumando molto meno del tuo piano. Le modifiche si applicano dal messaggio successivo.

Per cambiarlo solo in una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Seleziona di nuovo l’opzione **Impostazioni** per usare le impostazioni generali.

I controlli, il tuo profilo e le bozze preparate in anticipo mantengono il proprio modello.

## Limiti

Se il tuo piano ha limiti di utilizzo, per esempio i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, vedrai quanto hai consumato e quando si azzera ciascun limite. Consultare questa schermata non consuma il tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si mette in pausa quando raggiunge circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; le altre attività usano circa un settimo del limite settimanale al giorno. Un accesso senza limiti, come una chiave API, non viene mai messo in pausa.

Il lavoro in background non viene mai eseguito su GPT-6 Astra. Per ora, con un accesso a ChatGPT usa GPT-6.1 Sol, anche se il modello principale è GPT-6.2 Sol: con quell’accesso, 6.2 non riutilizza ancora le istruzioni memorizzate nella cache, quindi consuma di più del tuo piano. Le tue chat continuano a usare il modello che hai scelto.

Prima di un controllo, un modello più piccolo (GPT-6 Luna con ChatGPT, Haiku con Claude) mette da parte newsletter, promozioni e notifiche delle app che chiaramente non richiedono attenzione, così i controlli consumano meno del tuo piano. Potrai comunque cercarle. I messaggi scritti da una persona, le fatture, gli avvisi di sicurezza e i codici di accesso vengono sempre controllati.

## Prima di raggiungere un limite

Se il tuo piano ChatGPT ha ancora degli azzeramenti, in Attività compare una breve notifica quando il lavoro in background rallenta: a circa il 65% del limite di 5 ore o al 90% di quello settimanale. Indica quanto hai consumato e quanti azzeramenti restano. **Usa un azzeramento** azzera i limiti dopo la tua conferma. × nasconde la notifica fino al ripristino del limite. Se non hai azzeramenti, non compare nulla.

Su una Machine ospitata, la tua Machine vede e usa gli azzeramenti quando Codex sulla tua Machine ha effettuato l’accesso allo stesso account ChatGPT. Fino ad allora, in Attività e in Impostazioni compare **Attiva i ripristini**. Apre il passaggio di Codex nella pagina di configurazione, dove accedi con un codice, come per l’accesso a ChatGPT.

## Quando raggiungi un limite

In cima alla dashboard viene indicato quale limite hai raggiunto e quando si azzera. Il lavoro resta in attesa e poi riprende da dove si era interrotto. Non perdi nulla. Se il tuo piano ChatGPT include azzeramenti, **Usa un azzeramento** azzera i limiti. Su una Machine ospitata senza accesso a Codex, **Attiva i ripristini** apre invece la pagina di configurazione. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva incluso in un altro piano o fornito da un altro provider, subentra quando raggiungi un limite e il lavoro non resta in attesa. In cima alla dashboard compare «Limite ChatGPT raggiunto, uso il modello di riserva». Se il modello di riserva smette di funzionare, riprendono le pause.

## Cambiare il modello principale

Il modello principale è quello che usa il resto di The Machine. Su una Machine ospitata, puoi cambiarlo nella pagina di configurazione, in Your AI. Sul tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
