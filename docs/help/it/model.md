---
title: Modello
area: settings
summary: Quale modello IA risponde per te, quanto ragiona e quanto ha usato dei limiti del tuo piano.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: b76f4f927bfd7be1
---
**Impostazioni**, **Modello** mostra quale modello IA svolge il **Lavoro in background** e come hai effettuato l’accesso, ad esempio con ChatGPT.

Su una Machine ospitata con accesso a ChatGPT, il modello principale è GPT-6.2 Sol: risponde più velocemente di GPT-6.1 Sol allo stesso prezzo.

Su una Machine ospitata, l’accesso a Claude dura circa un anno. Con `claude auth login`, termina circa quattro settimane dopo aver effettuato l’accesso. Tre giorni prima, **Serve il tuo intervento** ti avvisa e ricevi un’email. Quando l’accesso termina, ricevi una notifica e, se non l’hai già ricevuta, anche l’email. **Accedi di nuovo** per risolvere il problema in un solo passaggio.

Un piano personale ChatGPT o Claude potrebbe usare le tue chat per l’addestramento per impostazione predefinita: **Disattiva l’addestramento con i tuoi dati** apre questa impostazione sul sito del provider e **Fatto** nasconde la riga.

## Modello e ragionamento per le chat

In **Chat**, scegli il modello e il livello di ragionamento per le chat delle tue attività e per l’Aiuto. Vedrai solo i modelli e i livelli disponibili con il tuo accesso.

Un ragionamento più approfondito aiuta a rispondere meglio alle domande difficili, ma richiede più tempo e usa più risorse del tuo piano. **Ragionamento ultra** coinvolge assistenti per le domande più difficili e usa più risorse di tutti. Una nuova Machine parte da **Ragionamento basso**: offre buoni risultati usando molte meno risorse del tuo piano. Le modifiche si applicano dal messaggio successivo.

Per cambiarlo solo per una chat, tocca il modello o il livello di ragionamento sotto la casella del messaggio. Scegli di nuovo l’opzione delle Impostazioni per seguire le Impostazioni.

I controlli, il tuo profilo e le bozze preparate in anticipo mantengono il proprio modello.

## Limiti

Se il tuo piano ha limiti di utilizzo, ad esempio i limiti di 5 ore e settimanali di un piano ChatGPT o Claude, vedrai quanto ne hai usato e quando si azzera ciascun limite. Consultare queste informazioni non consuma risorse del tuo piano.

## Spazio per le tue chat

Il lavoro in background lascia spazio alle tue chat. Si interrompe quando raggiungi circa il 65% del limite di 5 ore. I controlli dei nuovi messaggi continuano fino a circa il 90% del limite settimanale; il resto del lavoro usa ogni giorno circa un settimo delle risorse settimanali. Un accesso senza limiti, come una chiave API, non interrompe mai il lavoro.

Il lavoro in background non viene mai eseguito su GPT-6 Astra. Se hai effettuato l’accesso a ChatGPT e usi una versione di OpenClaw precedente a 2026.11.10, usa GPT-6.1 Sol anche quando il modello principale è GPT-6.2 Sol: in questo caso, la versione 6.2 non riutilizza le istruzioni memorizzate nella cache e consuma più risorse del tuo piano. Dalla versione OpenClaw 2026.11.10 in poi, il lavoro in background torna a usare il modello principale. Le tue chat continuano a usare il modello che hai scelto.

Prima di un controllo, un modello più piccolo (GPT-6 Luna con ChatGPT, Haiku con Claude) mette da parte newsletter, promozioni e avvisi delle app che chiaramente non richiedono interventi, così i controlli consumano meno risorse del tuo piano. Questi messaggi restano consultabili nelle ricerche. I messaggi scritti da una persona, una fattura, un avviso di sicurezza o un codice di accesso vengono sempre controllati.

## Prima di raggiungere un limite

Se il tuo piano ChatGPT ha azzeramenti disponibili, Attività mostra una breve notifica quando il lavoro in background rallenta: intorno al 65% del limite di 5 ore o al 90% del limite settimanale. La notifica indica quanto hai usato e quanti azzeramenti ti restano. **Usa un azzeramento** azzera i limiti, dopo la tua conferma. × nasconde la notifica fino al ripristino del limite. Se non hai azzeramenti disponibili, non compare nulla.

Su una Machine ospitata, la tua Machine vede e usa gli azzeramenti quando Codex sulla tua Machine ha effettuato l’accesso allo stesso account ChatGPT. Fino ad allora, Attività e Impostazioni mostrano **Attiva i ripristini**. Questa opzione apre il passaggio di Codex nella pagina di configurazione, dove effettui l’accesso con un codice, come per l’accesso a ChatGPT.

## Quando raggiungi un limite

Nella parte superiore della dashboard trovi il limite raggiunto e quando si azzera. Il lavoro resta in attesa, poi riprende da dove si era interrotto. Non perdi nulla. Se il tuo piano ChatGPT ha azzeramenti disponibili, **Usa un azzeramento** azzera i limiti. Su una Machine ospitata senza accesso a Codex, **Attiva i ripristini** apre invece la pagina di configurazione. Altrimenti, **Vedi gli azzeramenti in ChatGPT** apre la pagina di ChatGPT.

## Con un modello di riserva

Se la tua Machine ha un modello di riserva associato a un altro piano o provider, subentra quando raggiungi un limite e il lavoro non si interrompe. Nella parte superiore della dashboard compare «Limite ChatGPT raggiunto, uso del modello di riserva in corso». Se il modello di riserva smette di funzionare, il lavoro torna a interrompersi.

## Cambiare il modello principale

Il modello principale è quello usato dal resto di The Machine. Su una Machine ospitata, puoi cambiarlo nella pagina di configurazione, alla voce La tua IA. Sul tuo computer, consulta [ChatGPT](chatgpt.md), [Mistral](mistral.md) e la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
