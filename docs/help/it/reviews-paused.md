---
title: Niente attività nuove
area: troubleshooting
summary: I controlli sono disattivati, in attesa o interrotti per il limite di utilizzo del tuo modello. Scopri come capirlo e cosa fare.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: 40617b8ac692660b
---
Le attività arrivano dai controlli: la tua Machine controlla ciò che è arrivato negli ultimi 15 minuti circa.

## Ti sei appena iscritto

Su una nuova Machine ospitata, i controlli si avviano da soli quando colleghi l’IA e la posta. Mentre la tua Machine legge la posta, Attività mostra «Lettura della posta in corso. Le prime attività arriveranno tra pochi minuti». Quando ha un’idea del volume, indica più o meno quanto ci vorrà: «Le prime attività arriveranno tra circa 10 min». Se manca un passaggio, **Serve il tuo intervento** indica quale, per esempio **Collega la posta**, con un link al passaggio.

Mentre legge, Attività mostra a che punto è («Lettura di 20 messaggi su 132. Lettura dei prossimi 40…»), alcune delle persone e organizzazioni che ha trovato e la prima attività non appena è pronta. Il numero indica i messaggi che ha finito di leggere; la barra continua ad avanzare mentre legge i successivi. I nomi provengono dalla tua posta e li vedi solo tu.

Se la prima analisi non trova nulla per te, indica cosa ha letto e suggerisce i passaggi successivi, per esempio collegare un servizio da cui ricevi spesso email o chiedere cosa è cambiato questa settimana.

## I controlli sono disattivati

In cima ad Attività compare «I controlli sono disattivati, quindi non arrivano ancora nuove attività». Su una Machine ospitata, premi **Attiva i controlli**. Sul tuo computer, esegui `./install.sh --activate`.

## Il limite del tuo modello

Per lasciare spazio alle tue chat, i controlli si mettono in pausa quando raggiungono circa il 65% del limite di 5 ore del tuo piano IA e il 90% del limite settimanale. Se hai un modello di riserva su un altro piano, i controlli non aspettano. Scopri di più in [Modello](model.md).

Mentre i controlli sono in attesa, in cima alla dashboard compare fino a quando, per esempio «I controlli aspettano fino alle 07:15 per non consumare la tua quota settimanale di ChatGPT». **Controlla ora** avvia comunque un controllo. In **Impostazioni**, **Modello** trovi i tuoi limiti.

Non perdi nulla: i messaggi arrivati vengono controllati appena possibile. Dopo una lunga attesa, vengono prima i messaggi recenti delle persone, mentre ogni controllo ne esamina anche alcuni tra i più vecchi.

Finché i controlli non hanno recuperato il ritardo, le nuove attività arrivano senza una bozza, così il tuo piano viene usato prima per controllare i messaggi. Le bozze arrivano in seguito; le attività urgenti non aspettano. Premi **Fallo** per averne una subito.

## Di notte

Dalle 00:00 alle 06:30, i controlli si mettono in pausa e i nuovi messaggi restano in attesa. Alle 06:30 vengono controllati tutti insieme, prima del riepilogo del mattino. **Controlli** mostra «In pausa per la notte. Recupero alle 06:30». Usa l’app, scrivi in chat o tocca un’attività: i controlli riprendono e continuano finché non resti inattivo per un’ora. **Controlla ora** avvia subito un controllo.

## Un’esecuzione non è riuscita

**Esecuzioni recenti**, in **Connessioni**, **Controlli**, mostra ogni esecuzione. Quelle non riuscite vengono riprovate automaticamente.

Un’esecuzione interrotta perché è stato raggiunto il limite di utilizzo del tuo piano IA mostra **È stato raggiunto il limite di utilizzo dell’IA.** e indica quando sarà di nuovo disponibile. È una pausa, non un errore: i messaggi restano in attesa e vengono controllati dopo il ripristino del limite. Non viene inviata nessuna [segnalazione di errore](error-reports.md).

## Messi da parte

Quando un controllo rimanda un messaggio per due volte, lo mette da parte. **Connessioni**, **Controlli** mostra quanti sono; **Messi da parte** li elenca. Un messaggio di una persona che ti scrive, di qualcuno che conosci o di un cliente viene controllato ancora una volta circa 3 giorni dopo il suo arrivo. Questo controllo crea un’attività o chiude il messaggio. Ciò che hai scartato o posticipato resta così.
