---
title: Modello
area: settings
summary: Quale modello IA ti risponde, quanto ragiona e quanto ha usato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: eee77413a4bdbf0b
---
In **Impostazioni**, **Modello** mostra quale modello IA svolge il **Lavoro in background** e come hai effettuato l’accesso, per esempio con ChatGPT.

## Modello e ragionamento per le chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’assistenza. Vedrai solo i modelli e i livelli disponibili con il tuo metodo di accesso.

Più ragionamento aiuta a rispondere meglio alle domande difficili, ma è più lento e consuma più risorse del tuo piano. **Ragionamento ultra** usa assistenti per le domande più difficili e consuma più risorse di tutte le altre opzioni. Una Machine nuova parte da **Ragionamento basso**: ottieni buoni risultati consumando molte meno risorse del tuo piano. La modifica si applica dal messaggio successivo.

Per cambiarlo solo per una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Seleziona di nuovo l’opzione Impostazioni per seguire le Impostazioni.

I controlli, il tuo profilo e le bozze preparate in anticipo usano un modello dedicato.

## Limiti

Se il tuo piano ha limiti di utilizzo, come i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, vedrai quanto ne hai usato e quando si azzera ciascun limite. Consultare queste informazioni non consuma il tuo piano.

## Spazio per le tue chat

Il Lavoro in background lascia spazio alle tue chat. Si mette in pausa quando raggiunge circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; le altre attività usano circa un settimo del limite settimanale al giorno. Un accesso senza limiti, per esempio con una chiave API, non si mette mai in pausa.

Il Lavoro in background non usa mai GPT-6 Astra. Usa invece GPT-6.1 Sol.

## Quando raggiungi un limite

In cima alla dashboard viene indicato quale limite hai raggiunto e quando si azzera. Le attività restano in attesa, poi riprendono da dove si erano interrotte. Non perdi nulla. Se il tuo piano ChatGPT permette di azzerare i limiti, **Usa un azzeramento** li azzera. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la relativa pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva associato a un altro piano o provider, subentra quando raggiungi un limite e le attività non restano in attesa. In cima alla dashboard viene indicato: «Limite ChatGPT raggiunto, uso il modello di riserva». Se il modello di riserva smette di funzionare, le pause riprendono.

## Cambiare il modello principale

Il modello principale è quello che usa il resto di The Machine. Se usi una Machine ospitata, puoi cambiarlo nella pagina di configurazione, in La tua IA. Se usi il tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
