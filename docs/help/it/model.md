---
title: Modello
area: settings
summary: Quale modello di IA ti risponde, quanto ragiona e quanto ha consumato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: c7a96914e4deb3d4
---
In **Impostazioni**, **Modello** mostra quale modello di IA svolge il **Lavoro in background** e come hai effettuato l’accesso, per esempio con ChatGPT.

Un piano personale di ChatGPT o Claude potrebbe usare le tue chat per l’addestramento per impostazione predefinita: **Disattiva l’addestramento con i tuoi dati** apre questa impostazione sul sito del provider e **Fatto** nasconde la riga.

## Modello e ragionamento per le chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’assistenza. Vedrai solo i modelli e i livelli disponibili con il tuo accesso.

Un ragionamento più approfondito migliora le risposte alle domande difficili, ma è più lento e consuma più risorse del tuo piano. **Ragionamento ultra** coinvolge assistenti per le domande più difficili e consuma più risorse. Una nuova Machine inizia con **Ragionamento basso**: buoni risultati consumando molte meno risorse del tuo piano. Le modifiche si applicano dal messaggio successivo.

Per modificarlo solo per una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Seleziona di nuovo l’opzione Impostazioni per seguire le impostazioni.

I controlli, il tuo profilo e le bozze preparate in anticipo usano un modello diverso.

## Limiti

Se il tuo piano ha limiti di utilizzo, come i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, vedrai quanto hai usato e quando si azzera ciascun limite. Consultare questa schermata non consuma le risorse del tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si mette in pausa quando raggiunge circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi proseguono fino a circa il 90% del limite settimanale; il resto del lavoro usa circa un settimo del limite settimanale al giorno. Un accesso senza limiti, come una chiave API, non comporta mai pause.

Il lavoro in background non viene mai eseguito su GPT-6 Astra. Usa invece GPT-6.2 Sol, oppure GPT-6.1 Sol se 6.2 non è configurato.

## Quando si raggiunge un limite

Nella parte superiore della dashboard viene indicato quale limite è stato raggiunto e quando si azzera. Il lavoro resta in attesa, poi riprende da dove si era interrotto. Non perdi nulla. Se il tuo piano ChatGPT consente azzeramenti, **Usa un azzeramento** riavvia i limiti. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva su un altro piano o provider, subentra quando si raggiunge un limite e il lavoro non resta in attesa. Nella parte superiore della dashboard viene mostrato «Limite di ChatGPT raggiunto, in uso il modello di riserva». Se il modello di riserva smette di funzionare, riprendono le pause.

## Cambiare il modello principale

Il modello principale è quello usato dal resto di The Machine. Se hai una Machine ospitata, puoi cambiarlo nella pagina di configurazione, alla voce La tua IA. Se usi il tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
