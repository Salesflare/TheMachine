---
title: Input vocale
area: cards
summary: Parla invece di scrivere. Quello che dici appare nel campo del messaggio, così puoi controllarlo. Non viene inviato nulla.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
translated: f311b21bb4996eb4
---
## Parla invece di scrivere

Tocca il microfono nel campo di un messaggio: nella chat di un’attività, in **Nuova attività**, in **Aiuto** o nel campo in cui modifichi una bozza. Parla, poi tocca il segno di spunta. Oppure tieni premuto il microfono mentre parli e rilascialo quando hai finito.

Mentre ascolta, il campo mostra un timer e quello che ha capito finora. Tocca la X per interrompere senza conservare nulla. La registrazione si interrompe automaticamente dopo 2 minuti.

Il testo appare nel campo, nel punto in cui si trova il cursore. Non viene inviato nulla: leggilo, modificalo come vuoi e invialo tu.

## Dove viene elaborata la tua voce

Scegli l’opzione in **Impostazioni**, **Generale**, sotto **Input vocale**. Una breve frase indica quale opzione è in uso.

- **Automatico** (impostazione predefinita): OpenAI trascrive la registrazione quando la tua Machine usa OpenAI (una chiave OpenAI o un piano ChatGPT che consente l’uso dell’audio). Altrimenti, la tua Machine la trascrive e la registrazione non lascia mai la Machine.
- **Su questa Machine**: la registrazione viene sempre trascritta sulla tua Machine, anche quando OpenAI è configurato.
- **Con OpenAI**: la registrazione viene sempre trascritta da OpenAI.

La registrazione viene eliminata non appena il testo è pronto.

## Preparazione

Per trascrivere il parlato direttamente, la tua Machine prima scarica in background un modello vocale (da 150 a 500 MB), quando è poco utilizzata. Nel frattempo, in Impostazioni appare **Preparazione in corso (in background)**. Il download non è necessario quando è in uso OpenAI.

Fino ad allora, **Automatico** usa il riconoscimento vocale integrato nel browser, se disponibile, e lo indica sotto il campo. Alcuni browser inviano la registrazione al produttore. Se selezioni **Su questa Machine**, la registrazione resta in attesa e nel campo appare «Preparazione della voce…» con il tempo rimanente.

## Impostazioni

- **Trascritto**: **Automatico**, **Su questa Machine** o **Con OpenAI**.
- **Precisione** (solo sulla tua Machine): **Più preciso** funziona meglio per la maggior parte delle lingue. **Più veloce** è più rapido, ma fa più errori ed è l’impostazione predefinita su una Machine standard.
- **Lingua**: **Rileva** funziona con tutte le lingue dell’app. Selezionare la tua lingua è un po’ più veloce.

Per parlare a voce alta con The Machine, consulta [Parlare dal vivo](talk-live.md).

## Se non funziona

- **Il microfono è bloccato**: consenti l’accesso al microfono per questo sito nelle impostazioni del browser. Nell’app per telefono, lo trovi tra le autorizzazioni dell’app.
- **Nessun microfono trovato**: collegane uno e riprova.
- **Impossibile raggiungere la tua Machine**: la registrazione viene conservata e trascritta quando la tua Machine torna disponibile. Per riprovare prima, tocca **Prova ora**.
- **Non ho capito nulla**: avvicinati al microfono o parla un po’ più a lungo.
