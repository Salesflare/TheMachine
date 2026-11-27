---
title: Modello
area: settings
summary: Quale modello IA ti risponde, quanto ragiona e quanto ha consumato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 9a0777c555ab5637
---
**Impostazioni**, **Modello** mostra quale modello IA esegue il **Lavoro in background** e come hai effettuato l’accesso, per esempio con ChatGPT.

Su una Machine ospitata con accesso a ChatGPT, il modello principale è GPT-6.2 Sol: risponde più velocemente di GPT-6.1 Sol allo stesso prezzo.

L’accesso a Claude scade circa quattro settimane dopo aver effettuato l’accesso. **Serve il tuo intervento** ti avvisa tre giorni prima; una volta scaduto, ricevi una sola notifica. **Accedi di nuovo** risolve il problema in un passaggio.

Un piano personale ChatGPT o Claude potrebbe usare le tue chat per l’addestramento per impostazione predefinita: **Disattiva l’addestramento con i tuoi dati** apre l’impostazione sul sito del provider e **Fatto** nasconde la riga.

## Modello e ragionamento nelle chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’assistenza. Vedrai solo i modelli e i livelli disponibili con il tuo accesso.

Più ragionamento aiuta a rispondere meglio alle domande difficili, ma richiede più tempo e consuma più risorse del tuo piano. **Ragionamento ultra** usa assistenti aggiuntivi per le domande più difficili e consuma più risorse. Una nuova Machine parte da **Ragionamento basso**: buoni risultati consumando molte meno risorse del tuo piano. La modifica si applica dal messaggio successivo.

Per modificarlo solo per una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Seleziona di nuovo l’opzione Impostazioni per seguire le Impostazioni.

I controlli, il tuo profilo e le bozze preparate in anticipo usano un modello diverso.

## Limiti

Se il tuo piano ha limiti di utilizzo, come quelli di 5 ore e settimanali di un piano ChatGPT o Claude, qui puoi vedere quanto hai consumato e quando si azzera ciascun limite. Consultare queste informazioni non consuma risorse del tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si mette in pausa intorno al 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; le altre attività consumano circa un settimo del limite settimanale al giorno. Un accesso senza limiti, per esempio con una chiave API, non viene mai messo in pausa.

Il lavoro in background non viene mai eseguito con GPT-6 Astra. Con un accesso a ChatGPT e una versione di OpenClaw precedente alla 2026.11.10, usa GPT-6.1 Sol anche se il tuo modello principale è GPT-6.2 Sol: in questa versione 6.2 non riutilizza le istruzioni memorizzate nella cache, quindi consuma più risorse del tuo piano. Dalla versione 2026.11.10 di OpenClaw in poi, il lavoro in background torna a usare il modello principale. Le tue chat continuano a usare il modello che hai scelto.

Prima di un controllo, un modello leggero (GPT-6 Luna con ChatGPT, Haiku con Claude) filtra newsletter, promozioni e notifiche delle app che chiaramente non richiedono interventi, così i controlli consumano meno risorse del tuo piano. I messaggi restano ricercabili. I messaggi scritti da una persona, le fatture, gli avvisi di sicurezza e i codici di accesso vengono sempre controllati.

## Prima di raggiungere un limite

Se il tuo piano ChatGPT ha azzeramenti disponibili, in Attività compare una breve notifica quando il lavoro in background rallenta: intorno al 65% del limite di 5 ore o al 90% di quello settimanale. La notifica mostra quanto hai consumato e quanti azzeramenti restano. **Usa un azzeramento** azzera i limiti dopo la tua conferma. × nasconde la notifica fino al successivo azzeramento del limite. Se non hai azzeramenti disponibili, non compare nulla.

Su una Machine ospitata, la tua Machine vede e usa gli azzeramenti quando Codex sulla tua Machine ha effettuato l’accesso allo stesso account ChatGPT. Fino ad allora, Attività e Impostazioni mostrano **Attiva i ripristini**. Si apre la fase di Codex nella pagina di configurazione, dove accedi con un codice, come per l’accesso a ChatGPT.

## Quando si raggiunge un limite

In cima alla dashboard puoi vedere quale limite è stato raggiunto e quando si azzera. Il lavoro aspetta, poi riprende da dove si era interrotto. Non perdi nulla. Se il tuo piano ChatGPT ha azzeramenti disponibili, **Usa un azzeramento** azzera i limiti. Su una Machine ospitata senza accesso a Codex, **Attiva i ripristini** apre invece la pagina di configurazione. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva associato a un altro piano o provider, subentra quando viene raggiunto un limite e il lavoro non si ferma. In cima alla dashboard compare «Limite ChatGPT raggiunto, uso il modello di riserva». Se il modello di riserva smette di funzionare, le pause riprendono.

## Cambiare il modello principale

Il modello principale è quello usato dal resto di The Machine. Su una Machine ospitata, puoi cambiarlo nella pagina di configurazione, in La tua IA. Sul tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
