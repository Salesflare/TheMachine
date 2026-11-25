---
title: Niente attività nuove
area: troubleshooting
summary: I controlli sono disattivati, in attesa o sospesi per il limite di utilizzo del tuo modello. Scopri come capirlo e cosa fare.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: f0e9e4dc6c850b25
---
Le attività arrivano dai controlli: la tua Machine esamina ciò che è arrivato negli ultimi 15 minuti circa.

## Ti sei appena registrato

Su una nuova Machine ospitata, i controlli si avviano automaticamente quando colleghi l’IA e la posta. Mentre la tua Machine legge la posta, Attività mostra «Sto leggendo la posta. Le prime attività arriveranno tra pochi minuti». Quando sa quanto c’è da leggere, indica più o meno quanto ci vorrà: «Le prime attività arriveranno tra circa 10 min». Se manca un passaggio, **Serve il tuo intervento** indica quale, per esempio **Collega la posta**, con un link per completarlo.

Mentre legge, Attività mostra a che punto è («Ho letto 20 messaggi su 132. Sto leggendo i prossimi 40…»), alcune persone e organizzazioni che ha trovato e la prima attività appena è pronta. Il numero indica quanti messaggi ha finito di leggere; la barra continua ad avanzare mentre legge i successivi. I nomi vengono dalla tua posta e li vedi solo tu.

Se dalla prima verifica non emerge nulla, viene indicato cosa è stato letto e vengono proposti i passaggi successivi, per esempio collegare un servizio da cui ricevi spesso email o chiedere cosa è cambiato questa settimana.

## I controlli sono disattivati

In cima ad Attività compare «I controlli sono disattivati, quindi non arrivano ancora nuove attività». Su una Machine ospitata, premi **Attiva i controlli**. Sul tuo computer, esegui `./install.sh --activate`.

## Il limite del tuo modello

Per lasciare spazio alle tue chat, i controlli si mettono in pausa quando raggiungono circa il 65% del limite di 5 ore del tuo piano IA e il 90% del limite settimanale. Se hai un modello di riserva con un altro piano, i controlli non aspettano. Scopri di più in [Modello](model.md).

Mentre i controlli sono in attesa, in cima alla dashboard viene indicato fino a quando, per esempio: «I controlli aspettano fino alle 07:15 per non consumare la tua quota settimanale di ChatGPT». **Controlla ora** avvia comunque un controllo. In **Impostazioni**, **Modello** trovi i tuoi limiti.

Non perdi nulla: i messaggi arrivati vengono controllati appena possibile. Dopo una lunga attesa, vengono prima i messaggi recenti delle persone; ogni controllo esamina anche alcuni dei messaggi più vecchi.

## Di notte

Dalle 00:00 alle 06:30, i controlli si mettono in pausa e i nuovi messaggi restano in attesa. Alle 06:30 vengono controllati tutti insieme, prima del riepilogo del mattino. In **Controlli** compare «In pausa per la notte. Recupero alle 06:30». Usa l’app, scrivi in chat o tocca un’attività per far ripartire i controlli; continueranno finché non rimarrai inattivo per un’ora. **Controlla ora** avvia subito un controllo.

## Un’esecuzione non è riuscita

**Esecuzioni recenti**, in **Connessioni**, **Controlli**, mostra ogni esecuzione. Se un’esecuzione non riesce, viene riprovata automaticamente.

Se un’esecuzione si è fermata perché hai raggiunto il limite di utilizzo del tuo piano IA, compare il messaggio **È stato raggiunto il limite di utilizzo dell’IA.** e viene indicato quando sarà nuovamente disponibile. È una pausa, non un errore: i messaggi restano in attesa e vengono controllati dopo il ripristino del limite. Non viene inviata alcuna [segnalazione di errore](error-reports.md).

## Messi da parte

Quando un controllo mette da parte un messaggio per due volte, il messaggio viene messo da parte. In **Connessioni**, **Controlli** trovi il numero dei messaggi; **Messi da parte** li mostra. I messaggi di una persona che ti scrive, di una persona che conosci o di un cliente vengono controllati ancora una volta dopo circa 3 giorni dal loro arrivo. La verifica crea un’attività oppure chiude il messaggio. Ciò che hai scartato o posticipato resta così.
