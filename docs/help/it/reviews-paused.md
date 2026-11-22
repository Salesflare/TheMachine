---
title: Nessuna nuova attività
area: troubleshooting
summary: I controlli sono disattivati, in attesa o si sono fermati al limite di utilizzo del tuo modello. Ecco come capirlo e cosa fare.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: 07aca53acc41694d
---
Le attività arrivano dai controlli: la tua Machine esamina i nuovi messaggi ogni 15 minuti circa.

## Ti sei appena registrato

Su una nuova Machine ospitata, i controlli si avviano da soli quando colleghi l’IA e la posta. Mentre la tua Machine legge la posta, Attività mostra «Lettura della posta in corso. Le prime attività arriveranno tra pochi minuti». Una volta capito quanto c’è da leggere, indica più o meno quanto ci vorrà: «Le prime attività arriveranno tra circa 10 min». Se manca un passaggio, **Serve il tuo intervento** ti indica quale, ad esempio **Collega la posta**, con un link al passaggio.

Durante la lettura, Attività mostra a che punto è (ad esempio «Letti 20 di 132 messaggi. Lettura dei prossimi 40…»), alcune delle persone e organizzazioni trovate e la prima attività appena è pronta. Il numero indica i messaggi che ha finito di leggere; la barra continua ad avanzare mentre legge i successivi. I nomi provengono dalla tua posta e li vedi solo tu.

Se al primo controllo non trova nulla per te, indica cosa ha letto e suggerisce i passaggi successivi, come collegare un servizio da cui ricevi spesso email o chiedere cosa è cambiato questa settimana.

## I controlli sono disattivati

In cima ad Attività compare «I controlli sono disattivati, quindi non arriveranno ancora nuove attività». Su una Machine ospitata, premi **Attiva i controlli**. Sul tuo computer, esegui `./install.sh --activate`.

## Il limite del tuo modello

Per lasciare spazio alle tue chat, i controlli si fermano al raggiungimento di circa il 65% del limite di 5 ore del tuo piano IA e del 90% del limite settimanale. Se hai un modello di riserva con un altro piano, i controlli non aspettano. Vedi [Modello](model.md).

Mentre i controlli sono in attesa, in cima alla dashboard viene indicato fino a quando, ad esempio «I controlli attendono fino alle 07:15 per non consumare il limite settimanale di ChatGPT». **Controlla ora** ne avvia comunque uno. In **Impostazioni**, **Modello** trovi i tuoi limiti.

Non perdi nulla: i nuovi messaggi vengono controllati appena possibile.

## Di notte

Dalle 00:00 alle 06:30, i controlli si fermano e i nuovi messaggi restano in attesa. Alle 06:30 vengono controllati tutti insieme, prima del riepilogo del mattino. **Controlli** mostra «In pausa per la notte. Recupero alle 06:30». Usa l’app, scrivi in chat o tocca un’attività per riavviare i controlli; continueranno finché non resterai inattivo per un’ora. **Controlla ora** avvia subito un controllo.

## Un’esecuzione non è riuscita

**Esecuzioni recenti**, sotto **Connessioni**, **Controlli**, mostra ogni esecuzione. Se una non riesce, viene riprovata automaticamente.

Se un’esecuzione si è fermata al limite di utilizzo del tuo piano IA, compare **Il limite di utilizzo dell’IA è stato raggiunto.** e viene indicato quando sarà di nuovo disponibile. È una pausa, non un errore: i messaggi restano in attesa e vengono controllati dopo il ripristino del limite. Non viene inviata alcuna [segnalazione di errore](error-reports.md).

## Messi da parte

Quando un controllo mette da parte un messaggio per la seconda volta, il messaggio viene archiviato. **Connessioni**, **Controlli** mostra quanti ce ne sono, mentre **Messi da parte** li elenca. Un messaggio di una persona che ti scrive, di una persona che conosci o di un cliente viene controllato un’altra volta circa 3 giorni dopo il suo arrivo. Da quel controllo può nascere un’attività oppure il messaggio può essere chiuso. Ciò che hai scartato o posticipato resta così.
