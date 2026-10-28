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

Mentre ascolta, la casella mostra un timer. Tocca la croce per fermarti senza tenere niente. Una registrazione dura al massimo 2 minuti; a 2 minuti si ferma da sola e scrive quello che hai detto.

Quello che hai detto finisce nella casella, dove c’era il cursore. Non viene inviato niente: leggilo, cambia quello che vuoi e invialo tu.

## La prima volta

La prima volta che tocchi il microfono, la tua Machine prepara la voce. Scarica il modello vocale una volta sola, circa 600 MB, e mostra "Preparazione della voce…" con l’avanzamento. Ci vuole qualche minuto. La tua registrazione aspetta e viene trascritta appena tutto è pronto.

## Dove va la tua voce

Di base la tua registrazione viene trascritta sulla tua Machine stessa. Non la lascia mai e viene cancellata appena il testo è pronto. Il riconoscimento vocale del browser non viene usato, perché alcuni browser mandano la tua voce al loro produttore.

In **Impostazioni**, **Generale**, sotto **Input vocale**, puoi scegliere:

- **Trascritto**: **Su questa Machine**, oppure **Con OpenAI**. OpenAI è più veloce su un server piccolo, ma la tua registrazione va a OpenAI, con la tua chiave. Serve una chiave API di OpenAI in OpenClaw. Un accesso con ChatGPT non la include.
- **Precisione**: **Più preciso** funziona meglio per la maggior parte delle lingue e, su un server piccolo, ci mette più o meno quanto hai parlato. **Più veloce** è più rapido, ma sbaglia più parole.
- **Lingua**: **Rileva** funziona per tutte le lingue dell’app. Scegliere la tua è un po’ più veloce.

## Se non funziona

- **Il microfono è bloccato**: consenti il microfono per questo sito nelle impostazioni del browser. Nell’app sul telefono, è nei permessi dell’app.
- **Nessun microfono trovato**: collegane uno e riprova.
- **Impossibile raggiungere la tua Machine**: la registrazione resta. Tocca **Riprova** quando la tua Machine è di nuovo raggiungibile.
- **Non ho capito niente**: parla un po’ più vicino al microfono, o più a lungo.
