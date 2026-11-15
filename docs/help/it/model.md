---
title: Modello
area: settings
summary: Quale modello di IA ti risponde, quanto ragiona e quanto ha consumato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 744a27a77ab747ac
---
In **Impostazioni**, **Modello** mostra quale modello di IA svolge il **Lavoro in background** e come hai effettuato l’accesso, per esempio con ChatGPT.

Per impostazione predefinita, un piano personale ChatGPT o Claude potrebbe usare le tue chat per addestrare i modelli. **Disattiva l’addestramento con i tuoi dati** apre questa impostazione presso il provider, mentre **Fatto** nasconde la riga.

## Modello e ragionamento per le chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’assistenza. Vedrai solo i modelli e i livelli disponibili con il tuo accesso.

Più ragionamento permette di rispondere meglio alle domande difficili, ma è più lento e consuma di più il tuo piano. **Ragionamento ultra** usa assistenti per le domande più difficili e consuma di più. Una nuova Machine inizia con **Ragionamento basso**: buoni risultati consumando molto meno del tuo piano. Le modifiche si applicano dal messaggio successivo.

Per cambiare il modello o il livello di ragionamento solo per una chat, tocca quello mostrato sotto la casella del messaggio. Scegli di nuovo l’opzione di **Impostazioni** per usare le impostazioni generali.

I controlli, il tuo profilo e le bozze preparate in anticipo mantengono il proprio modello.

## Limiti

Se il tuo piano ha limiti di utilizzo, come i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, qui vedrai quanto ne hai usato e quando si azzera ciascun limite. Consultare questa schermata non consuma il tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si mette in pausa quando hai usato circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; le altre attività usano circa un settimo del limite settimanale al giorno. Un accesso senza limiti, come una chiave API, non si mette mai in pausa.

Il lavoro in background non viene mai eseguito su GPT-6 Astra. Al suo posto usa GPT-6.1 Sol.

## Quando raggiungi un limite

Nella parte superiore del dashboard trovi il limite raggiunto e quando si azzera. Il lavoro resta in attesa, poi riprende da dove si era interrotto. Non perdi nulla. Se il tuo piano ChatGPT consente di azzerare i limiti, **Usa un azzeramento** li azzera. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva associato a un altro piano o provider, subentra quando raggiungi un limite e il lavoro non resta in attesa. Nella parte superiore del dashboard trovi il messaggio «Limite ChatGPT raggiunto, uso del modello di riserva in corso». Se il modello di riserva smette di funzionare, le pause riprendono.

## Cambiare il modello principale

Il modello principale è quello usato dal resto di The Machine. Se hai una Machine ospitata, puoi cambiarlo nella pagina di configurazione, sotto La tua IA. Se usi il tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
