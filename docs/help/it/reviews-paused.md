---
title: Nessuna nuova attività
area: troubleshooting
summary: Le revisioni sono disattivate, in attesa o ferme sul limite di utilizzo del tuo modello. Come capirlo e cosa fare.
covers: 
code: dashboard.html, assistant.py
order: 3
---
Le attività nascono dalle revisioni: la tua Machine legge quello che è arrivato, a piccoli gruppi, entro circa 15 minuti.

## Appena registrato

Su una nuova Machine ospitata, le revisioni partono da sole appena la tua IA e la tua posta sono collegate. Mentre la tua Machine legge la tua posta, Attività dice "Leggo la tua posta, le prime attività arrivano tra pochi minuti". Se manca un passaggio, **Serve il tuo intervento** lo indica, come **Collega la posta**, con un link a quel passaggio.

## Le revisioni sono disattivate

In cima ad Attività compare "Le revisioni sono disattivate, quindi per ora non arrivano attività." Su una Machine in hosting, premi **Attiva le revisioni**. Sul tuo computer, esegui `./install.sh --activate`.

## Il limite del tuo modello

Le revisioni di quello che è arrivato si mettono in pausa a circa il 65% del limite di 5 ore del tuo piano e al 90% del limite settimanale, per lasciare spazio alle tue chat. Una bacheca che scorre la tua cronologia va più piano, a circa un settimo della settimana al giorno. Con un modello di riserva funzionante, su un altro piano o fornitore, le revisioni non aspettano. Vedi [Modello](model.md).

Mentre le revisioni aspettano, in cima alla dashboard compare fino a quando, per esempio "Le revisioni aspettano fino alle 07:15 per risparmiare la tua settimana di ChatGPT." **Rivedi ora** ne avvia una subito. Quando raggiungi un limite, in cima alla dashboard compare quale e quando si azzera. **Connessioni**, poi **Revisioni**, lo mostra accanto all’esecuzione. **Impostazioni**, **Modello** mostra i tuoi limiti. Vedi [Modello](model.md).

Mentre aspetta non si perde nulla: quello che è arrivato viene revisionato appena possibile.

## Un’esecuzione non è riuscita

**Esecuzioni recenti** sotto **Revisioni** mostra ogni esecuzione. Un gruppo non riuscito viene ritentato da solo.
