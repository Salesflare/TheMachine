---
title: Nessuna nuova attività
area: troubleshooting
summary: I controlli sono disattivati, in attesa o interrotti per il limite di utilizzo del modello. Scopri come capirlo e cosa fare.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: d265e540d9ecef0e
---
Le attività arrivano dai controlli: la tua Machine controlla cosa è arrivato negli ultimi 15 minuti circa.

## Ti sei appena registrato

Su una nuova Machine ospitata, i controlli si avviano da soli una volta collegate l’AI e la posta. Mentre la tua Machine legge la posta, Attività mostra «Lettura della posta in corso, le prime attività arriveranno tra qualche minuto». Una volta capito quanto c’è da leggere, indica all’incirca quanto ci vorrà: «Le prime attività arriveranno tra circa 10 min». Se manca un passaggio, **Serve il tuo intervento** lo indica, per esempio con **Collega la posta**, e include un link a quel passaggio.

Durante la lettura, Attività mostra i progressi («Letti 20 messaggi su 132. Lettura dei prossimi 40…»), alcune delle persone e organizzazioni che ha trovato e la tua prima attività non appena è pronta. Il numero indica quanti messaggi ha finito di leggere; la barra avanza mentre legge i successivi. I nomi provengono dalla tua posta e li vedi solo tu.

Se al primo controllo non trova nulla per te, indica cosa ha letto e suggerisce i passaggi successivi, per esempio collegare un servizio da cui ricevi spesso email o chiedere cosa è cambiato questa settimana.

## I controlli sono disattivati

In cima ad Attività compare «I controlli sono disattivati, quindi non arrivano ancora attività». Su una Machine ospitata, premi **Attiva i controlli**. Sul tuo computer, esegui `./install.sh --activate`.

## Il limite del tuo modello

Per lasciare spazio alle tue chat, i controlli si mettono in pausa quando raggiungono circa il 65% del limite di 5 ore del tuo piano AI e il 90% del limite settimanale. Se hai un modello di riserva con un altro piano, i controlli non aspettano. Vedi [Modello](model.md).

Mentre i controlli sono in attesa, in cima alla dashboard compare fino a quando, per esempio «I controlli sono in attesa fino alle 07:15 per salvaguardare la tua quota settimanale di ChatGPT». **Controlla ora** ne avvia comunque uno. In **Impostazioni**, **Modello** trovi i tuoi limiti.

Non perdi nulla: i contenuti arrivati vengono controllati appena possibile.

## Di notte

Dalle 00:00 alle 06:30, i controlli si mettono in pausa e i nuovi messaggi restano in attesa. Alle 06:30 vengono controllati tutti insieme, prima del riepilogo del mattino. **Controlli** mostra «In pausa per la notte, recupero alle 06:30». Usa l’app, scrivi in chat o tocca un’attività: i controlli ripartono e continuano finché non resti inattivo per un’ora. **Controlla ora** avvia subito un controllo.

## Un’esecuzione non è riuscita

In **Connessioni**, **Controlli**, la sezione **Esecuzioni recenti** mostra ogni esecuzione. Se una non riesce, viene riprovata automaticamente.

## Messi da parte

Quando un controllo rimanda un messaggio due volte, viene messo da parte. In **Connessioni**, **Controlli** trovi quanti sono, mentre **Messi da parte** li elenca. Un messaggio ricevuto da una persona che ti scrive, da qualcuno che conosci o da un cliente viene controllato un’ultima volta circa 3 giorni dopo il suo arrivo. Quel controllo crea un’attività o chiude il messaggio. Ciò che hai scartato o posticipato resta tale.
