---
title: Nessuna nuova attività
area: troubleshooting
summary: I controlli sono disattivati, in attesa o fermi sul limite di utilizzo del tuo modello. Come capirlo e cosa fare.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: 39b4aa749445dfba
---
Le attività nascono dai controlli: la tua Machine legge quello che è arrivato, a piccoli gruppi, entro circa 15 minuti.

## Appena registrato

Su una nuova Machine ospitata, i controlli partono da soli appena la tua IA e la tua posta sono collegate. Mentre la tua Machine legge la tua posta, Attività dice "Leggo la tua posta, le prime attività arrivano tra pochi minuti". Appena sa quanto c’è da leggere, dice più o meno quanto ci vuole: "Prime attività tra circa 10 min." Se manca un passaggio, **Serve il tuo intervento** lo indica, come **Collega la posta**, con un link a quel passaggio.

Mentre legge, Attività mostra a che punto è, alcune delle persone e organizzazioni che ha incontrato e la tua prima attività appena arriva. I nomi vengono dalla tua posta e li vedi solo tu.

Se al primo sguardo non trova niente per te, dice cosa ha letto e propone i passi successivi, come collegare un servizio che ti scrive spesso o chiedere cosa è cambiato questa settimana.

## I controlli sono disattivati

In cima ad Attività compare "I controlli sono disattivati, quindi per ora non arrivano attività." Su una Machine in hosting, premi **Attiva i controlli**. Sul tuo computer, esegui `./install.sh --activate`.

## Il limite del tuo modello

I controlli di quello che è arrivato si mettono in pausa a circa il 65% del limite di 5 ore del tuo piano e al 90% del limite settimanale, per lasciare spazio alle tue chat. Una bacheca che scorre la tua cronologia va più piano, a circa un settimo della settimana al giorno. Con un modello di riserva funzionante, su un altro piano o fornitore, i controlli non aspettano. Vedi [Modello](model.md).

Mentre i controlli aspettano, in cima alla dashboard compare fino a quando, per esempio "I controlli aspettano fino alle 07:15 per risparmiare la tua settimana di ChatGPT." **Controlla ora** ne avvia uno subito. Quando raggiungi un limite, in cima alla dashboard compare quale e quando si azzera. **Connessioni**, poi **Controlli**, lo mostra accanto all’esecuzione. **Impostazioni**, **Modello** mostra i tuoi limiti. Vedi [Modello](model.md).

Mentre aspetta non si perde nulla: quello che è arrivato viene controllato appena possibile.

## Un’esecuzione non è riuscita

**Esecuzioni recenti** sotto **Controlli** mostra ogni esecuzione. Un gruppo non riuscito viene ritentato da solo.

## Messi da parte

Quando un controllo rimanda un messaggio due volte, viene messo da parte. **Connessioni**, **Controlli** mostra quanti, e **Messi da parte** li elenca. Uno da una persona che ti scrive direttamente, da qualcuno che conosci o da un cliente riceve un ultimo controllo circa 3 giorni dopo l’arrivo. Quel controllo crea un’attività o lo chiude. Ciò che hai scartato o posticipato resta così.
