---
title: Niente attività nuove
area: troubleshooting
summary: I controlli sono disattivati, in attesa o bloccati dal limite di utilizzo del tuo modello. Ecco come capirlo e cosa fare.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: d8a15909ab8164e8
---
Le attività arrivano dai controlli: la tua Machine controlla cosa è arrivato negli ultimi 15 minuti circa.

## Ti sei appena registrato

Su una nuova Machine ospitata, i controlli si avviano da soli quando colleghi l’IA e la posta. Mentre la tua Machine legge la posta, Attività mostra «Lettura della posta in corso. Le prime attività arriveranno tra qualche minuto». Quando capisce quanta posta c’è, indica più o meno quanto ci vorrà: «Le prime attività arriveranno tra circa 10 min». Se manca un passaggio, **Serve il tuo intervento** lo indica, per esempio con **Collega la posta**, insieme a un link per completarlo.

Mentre legge, Attività mostra a che punto è («Lettura di 20 messaggi su 132. Lettura dei prossimi 40…»), alcune persone e organizzazioni che ha trovato e la prima attività appena è pronta. Il numero indica i messaggi che ha finito di leggere; la barra continua ad avanzare mentre legge i successivi. I nomi vengono dalla tua posta e li vedi solo tu.

Se al primo controllo non trova niente per te, indica cosa ha letto e suggerisce i prossimi passi, per esempio collegare un servizio da cui ricevi spesso email o chiedere cosa è cambiato questa settimana.

## I controlli sono disattivati

In cima ad Attività compare «I controlli sono disattivati, quindi non arriveranno nuove attività». Su una Machine ospitata, premi **Attiva i controlli**. Sul tuo computer, esegui `./install.sh --activate`.

## Il limite del tuo modello

Per lasciare spazio alle tue chat, i controlli si mettono in pausa quando raggiungono circa il 65% del limite di 5 ore del tuo piano IA e il 90% del limite settimanale. Se hai un modello di riserva con un altro piano, i controlli non aspettano. Scopri di più in [Modello](model.md).

Mentre i controlli sono in attesa, in cima alla dashboard trovi fino a quando, per esempio «I controlli sono in attesa fino alle 07:15 per risparmiare il limite settimanale di ChatGPT». **Controlla ora** avvia comunque un controllo. In **Impostazioni**, **Modello** trovi i tuoi limiti.

Non perdi niente: i messaggi ricevuti vengono controllati appena possibile. Dopo una lunga attesa, vengono prima i messaggi recenti delle persone, mentre ogni controllo ne esamina anche una parte dei più vecchi.

Finché non si sono messi in pari, arrivano nuove attività senza una bozza, così il tuo piano viene usato prima per controllare i messaggi. Le bozze arrivano in seguito, ma quelle urgenti non aspettano. Premi **Fallo** per riceverne una subito.

## Di notte

Da 00:00 a 06:30 i controlli si mettono in pausa e i nuovi messaggi restano in attesa. Alle 06:30 vengono controllati tutti insieme, prima del riepilogo del mattino. **Controlli** mostra «In pausa per la notte. Recupero alle 06:30». Usa l’app, scrivi in chat o tocca un’attività per riavviare i controlli. Continueranno finché non passa un’ora senza che usi l’app. **Controlla ora** avvia subito un controllo.

## Un’esecuzione non è riuscita

**Esecuzioni recenti**, in **Connessioni**, **Controlli**, mostra ogni esecuzione. Se una non riesce, viene riprovata automaticamente. Se la tua IA smette di rispondere, per esempio perché la sessione è scaduta, accedi di nuovo da **Impostazioni**, **Modello**: i controlli ripartono subito.

Se un’esecuzione si è fermata al raggiungimento del limite di utilizzo del tuo piano IA, viene mostrato **È stato raggiunto il limite di utilizzo dell’IA.** e quando verrà reimpostato. È una pausa, non un errore: i messaggi restano in attesa e vengono controllati dopo la reimpostazione. Non viene inviata nessuna [segnalazione di errore](error-reports.md).

## Messi da parte

Quando un controllo rimanda un messaggio per due volte, il messaggio viene messo da parte. **Connessioni**, **Controlli** mostra quanti sono, mentre **Messi da parte** li elenca.

Anche un messaggio che fa fallire ogni controllo mentre la tua IA funziona viene messo da parte, così il resto può essere controllato.

Un messaggio di una persona che ti scrive, di qualcuno che conosci o di un cliente viene controllato ancora una volta circa 3 giorni dopo il suo arrivo. Quel controllo crea un’attività o la chiude. Ciò che hai scartato o posticipato resta così.
