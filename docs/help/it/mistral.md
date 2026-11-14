---
title: Mistral
area: connections
summary: Fai funzionare la tua Machine con i modelli di Mistral, con una chiave API di Mistral. Le Chat Pro include crediti API.
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key, Keys, Remove
translated: 5d782f28fb69efef
---
## A cosa serve

Mistral è un fornitore europeo di AI. Con una chiave API di Mistral, la tua Machine legge e prepara le bozze con i modelli di Mistral. The Machine non ha un’AI propria: le richieste vanno direttamente a Mistral, con il tuo account e alle sue condizioni.

## Prendi una chiave

Mistral non ha un accesso per le altre app, quindi funziona con una chiave API. Nella [console di Mistral](https://console.mistral.ai/), apri API keys e creane una. Le Chat Pro include crediti API ogni mese; dopo, Mistral fa pagare in base all’uso.

## Collegalo

Su una Machine in hosting, apri la tua pagina di configurazione, vai a La tua IA e apri **Altri servizi di IA**. Scegli Mistral come provider, incolla la chiave e premi **Salva chiave**. La tua Machine prova prima la chiave con una richiesta minima. Una chiave sbagliata si vede subito, e non viene salvato nulla.

Mistral Large diventa il modello principale. C’è anche Mistral Small, una scelta più economica per le chat o come riserva.

Sul tuo computer, vedi la [guida ai modelli](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).

## Uso

**Impostazioni**, **Modello** dice "Usa la tua chiave API di Mistral". Una chiave API non ha limiti di utilizzo, quindi il lavoro in background non si ferma mai per lei. Vedi [Modello](model.md).

## Rimuovilo

Nella tua pagina di configurazione, in La tua IA, premi **Rimuovi** accanto a Mistral in **Chiavi**. La chiave viene eliminata dalla tua Machine e, se Mistral era il tuo modello principale, subentra un altro modello collegato. Per annullare la chiave stessa, eliminala nella console di Mistral.
