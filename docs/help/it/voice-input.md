---
title: Input vocale
area: cards
summary: Parla invece di scrivere. Quello che dici finisce nella casella del messaggio, così puoi controllarlo. Non viene inviato niente.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
---
## Parla invece di scrivere

Tocca il microfono in una casella di messaggio: la chat di un’attività, **Nuova attività**, **Aiuto**, o la casella per modificare una bozza. Parla, poi tocca il segno di spunta. Oppure tieni premuto il microfono mentre parli e rilascia quando hai finito.

Mentre ascolta, la casella mostra un timer. Tocca la croce per fermarti senza tenere niente. Una registrazione dura al massimo 2 minuti; a 2 minuti si ferma da sola e scrive quello che hai detto. Quello che ha già sentito appare nella barra mentre parli, così il testo è pronto poco dopo che ti fermi.

Quello che hai detto finisce nella casella, dove c’era il cursore. Non viene inviato niente: leggilo, cambia quello che vuoi e invialo tu.

## Dove va la tua voce

In **Impostazioni**, **Generale**, sotto **Input vocale**, una riga breve dice quale è in uso.

- **Automatico** (predefinito): quando OpenAI è configurato in OpenClaw, la registrazione viene trascritta da OpenAI. Cioè una chiave API, o un accesso ChatGPT se il tuo piano consente l’audio. Senza OpenAI, viene trascritta sulla tua Machine stessa e non la lascia mai.
- **Su questa Machine**: sempre sulla tua Machine, anche quando OpenAI è configurato.
- **Con OpenAI**: sempre OpenAI.

Una registrazione viene eliminata appena torna il testo.

## Preparazione

Per trascrivere la voce da sola, la tua Machine ha bisogno di un modello vocale da 150 a 500 MB. Lo scarica in background, a bassa priorità, quando è configurata, la sua prima revisione è finita ed è tranquilla da un po’. Nel frattempo le impostazioni mostrano **In preparazione (in background)**. Non lo fa mai quando si usa OpenAI.

Finché non è pronta, **Automatico** usa il riconoscimento vocale del browser, se ne ha uno, e lo dice sotto la casella. Alcuni browser lo inviano al loro produttore. Con **Su questa Machine** scelto, la registrazione aspetta e la casella mostra "Preparazione della voce…" con il tempo rimanente.

## Impostazioni

- **Trascritto**: **Automatico**, **Su questa Machine** o **Con OpenAI**.
- **Precisione** (solo sulla tua Machine): **Più preciso** funziona meglio per la maggior parte delle lingue. **Più veloce** è più rapido ma sbaglia più parole. Su un server Standard, che ha meno memoria, **Più veloce** è il predefinito.
- **Lingua**: **Rileva** funziona per tutte le lingue dell’app. Scegliere la tua è un po’ più veloce.

Per parlare invece ad alta voce con The Machine, vedi [Parla dal vivo](talk-live.md).

## Se non funziona

- **Il microfono è bloccato**: consenti il microfono per questo sito nelle impostazioni del browser. Nell’app sul telefono, è nei permessi dell’app.
- **Nessun microfono trovato**: collegane uno e riprova.
- **Impossibile raggiungere la tua Machine**: la registrazione resta e viene trascritta quando la tua Machine torna raggiungibile. Per provare prima, tocca **Prova ora**.
- **Non ho capito niente**: parla un po’ più vicino al microfono, o più a lungo.
