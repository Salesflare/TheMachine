---
title: Modello
area: settings
summary: Quale modello di IA risponde, quanto ragiona e quanto ha consumato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: f34db396a7290252
---
In **Impostazioni**, **Modello** mostra quale modello di IA svolge il **Lavoro in background** e come hai effettuato l’accesso, per esempio con ChatGPT.

Su una Machine ospitata con accesso a ChatGPT, il modello principale è GPT-6.2 Sol: risponde più velocemente di GPT-6.1 Sol allo stesso prezzo.

Un piano personale ChatGPT o Claude potrebbe usare le tue chat per l’addestramento, per impostazione predefinita. **Disattiva l’addestramento con i tuoi dati** apre l’impostazione del provider, mentre **Fatto** nasconde la riga.

## Modello e ragionamento per le chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’assistenza. Vedrai solo i modelli e i livelli disponibili con il tuo accesso.

Più ragionamento aiuta a rispondere meglio alle domande difficili, ma è più lento e consuma più risorse del tuo piano. **Ragionamento ultra** coinvolge assistenti per le domande più difficili e consuma più risorse. Una nuova Machine parte da **Ragionamento basso**: buoni risultati consumando molte meno risorse del tuo piano. Le modifiche si applicano dal messaggio successivo.

Per cambiare queste impostazioni solo per una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Scegli di nuovo l’opzione Impostazioni per seguire le impostazioni generali.

I controlli, il tuo profilo e le bozze preparate in anticipo usano ciascuno il proprio modello.

## Limiti

Se il tuo piano ha limiti di utilizzo, come i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, qui vedrai quanto è stato usato e quando si azzera ogni limite. Consultare questa schermata non consuma risorse del tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si mette in pausa quando raggiunge circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; le altre attività usano circa un settimo del limite settimanale al giorno. Un accesso senza limiti, come una chiave API, non viene mai messo in pausa.

Il lavoro in background non usa mai GPT-6 Astra. Con un accesso a ChatGPT e una versione di OpenClaw precedente a 2026.11.10, usa GPT-6.1 Sol, anche se il modello principale è GPT-6.2 Sol: in questo caso, 6.2 non riutilizza le istruzioni memorizzate nella cache e consuma più risorse del tuo piano. Dalla versione 2026.11.10 di OpenClaw in poi, il lavoro in background torna a usare il modello principale. Le tue chat continuano a usare il modello che hai scelto.

Prima di un controllo, un modello leggero (GPT-6 Luna con ChatGPT, Haiku con Claude) esclude newsletter, promozioni e notifiche delle app che chiaramente non richiedono alcuna azione, così i controlli consumano meno risorse del tuo piano. Questi messaggi restano consultabili nelle ricerche. I messaggi scritti da una persona, le bollette, gli avvisi di sicurezza e i codici di accesso vengono sempre controllati.

## Prima di raggiungere un limite

Se il tuo piano ChatGPT ha azzeramenti disponibili, Attività mostra una breve riga quando il lavoro in background rallenta: circa al 65% del limite di 5 ore o al 90% del limite settimanale. La riga indica quanto è stato usato e quanti azzeramenti restano. **Usa un azzeramento** riavvia i limiti dopo la tua conferma. × nasconde la riga fino all’azzeramento di quel limite. Se non hai azzeramenti disponibili, non compare nulla.

Su una Machine ospitata, la tua Machine vede e usa gli azzeramenti quando Codex sulla tua Machine ha effettuato l’accesso allo stesso account ChatGPT. Fino ad allora, Attività e Impostazioni mostrano **Attiva i ripristini**. Si apre il passaggio di Codex nella pagina di configurazione, dove puoi accedere con un codice, come per ChatGPT.

## Quando raggiungi un limite

In cima alla dashboard viene indicato quale limite è stato raggiunto e quando si azzera. Il lavoro resta in attesa e poi riprende da dove si era interrotto. Non perdi nulla. Se il tuo piano ChatGPT ha azzeramenti disponibili, **Usa un azzeramento** riavvia i limiti. Su una Machine ospitata senza accesso a Codex, **Attiva i ripristini** apre invece la pagina di configurazione. Negli altri casi, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva associato a un altro piano o provider, passa a usarlo quando raggiungi un limite e il lavoro non resta in attesa. In cima alla dashboard appare «Limite di ChatGPT raggiunto, uso il modello di riserva». Se il modello di riserva smette di funzionare, il lavoro torna a essere messo in pausa.

## Cambiare il modello principale

Il modello principale è quello che usa il resto di The Machine. Su una Machine ospitata, puoi cambiarlo dalla pagina di configurazione, in La tua IA. Sul tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
