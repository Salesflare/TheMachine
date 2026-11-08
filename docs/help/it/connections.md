---
title: Connessioni
area: connections
summary: Le tue fonti in un solo posto: come stanno andando, aggiungine una nuova o disconnettine una.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## Come stanno andando

La scheda **Connessioni** raggruppa le tue fonti in **Email e calendario**, **Chat** e **Altre fonti**. Ognuna dice come sta andando: Connesso, In attesa della prima sincronizzazione, Riconnessione automatica o Serve il tuo aiuto. Apri **Dettagli** per vedere **Sincronizzazioni recenti**, dove la sincronizzazione è spiegata in parole semplici (come "In pari" o "Prima lettura"), e cosa fare.

I suoi numeri mostrano cosa ha portato, cosa è arrivato nelle ultime 24 ore e cosa non è ancora stato controllato. Un calendario conta eventi: tutti, quelli dei prossimi 7 giorni e delle ultime 24 ore.

Sotto lo stato, ogni fonte dice in una riga cosa porta e, quando può agire, che lo fa solo dopo che premi **Invia** o dai l’OK.

## Aggiungine una

Apri **+ Aggiungi** e scegli una fonte. Chiede quello che le serve, una domanda alla volta. **Annulla** interrompe l'aggiunta. Una volta collegata, la tua Machine si riavvia per iniziare a leggerla, poi apre la nuova scheda, che mostra come va la prima sincronizzazione. Su una Machine in hosting, Google, Microsoft, Microsoft OneDrive, Zoom, Stripe e Intercom accedono da qui: scegli **Lavoro** o **Personale**, accedi e torni a questo modulo, che mostra come va il collegamento. GitHub, WhatsApp, Codex, Chat di Telegram e il tuo telefono Android mostrano il loro codice direttamente in questo modulo.

L’elenco è diviso in gruppi (**Email e calendario**, **Chat**, **Riunioni**, **Documenti e file**, **Clienti**, **Progetti e codice**, **Altro**), dalla A alla Z in ciascuno.

**Suggerito per te** compare in alto quando la tua Machine vede un motivo per una fonte, con quel motivo in una riga: email da Stripe, riunioni Zoom nel tuo calendario, messaggi che rimandano a Google Docs, o una configurazione non finita. Li conta sulla tua Machine; non esce nulla. Nessun motivo, nessuna sezione. Una fonte già collegata non viene mai suggerita.

**Riconnetti** su una fonte e in **Serve il tuo intervento** apre lo stesso modulo. Sul tuo computer, `assistant connect` fa lo stesso in un terminale.

## Lavoro o personale

Ogni fonte conta come lavoro (per un’azienda che indichi tu) o personale. Cambialo sotto **Dettagli**. Dice **Ipotizzato** solo quando l'ha scelto la tua Machine in base all'indirizzo; quando scegli tu, la scelta è tua. Le attività di lavoro aspettano i tuoi giorni lavorativi.

## Capacità

Una fonte può portare segnali (ciò che arriva diventa to-do), fare cose per i tuoi to-do (leggere un documento quando ne serve uno, o inviare, rispondere o cambiare qualcosa dopo il tuo OK), o entrambe. Con entrambe, **Dettagli** ha un interruttore per ciascuna: **Porta segnali** e **Può fare cose**. Una resta attiva. Per fermarle entrambe, disconnettila. Le risposte di una chat rispondono a ciò che porta, quindi una chat ha solo **Può fare cose**.

Con **Porta segnali** spento, non si sincronizza e la sua scheda non mostra numeri. Con **Può fare cose** spento, la tua Machine non legge mai nulla su richiesta, non scrive bozze e non cambia nulla con essa. Le fonti di prima le hanno entrambe attive.

## Rimuovine una

Apri la fonte, **Dettagli**, poi **Disconnetti**. Smette di leggere. Quello che ha già portato dentro resta. Su una Machine in hosting, Google, Microsoft, Microsoft OneDrive, Zoom e Stripe mostrano **Disconnetti ↗**, che apre la tua pagina di configurazione.

**Disconnesso di recente** elenca gli accessi Google, Microsoft e Zoom che hai rimosso. **Rimosso, confermato** significa che Google ha confermato la disconnessione, oppure, per Microsoft e Zoom, che non ne resta alcuna copia. **In sospeso** spiega il perché, e la tua Machine continua a riprovare.

## Accessi salvati

I siti usati dal browser della tua Machine, come LinkedIn o X, possono salvare un accesso: spunta **Salva per la prossima volta** quando accedi. Poi **Accessi** li elenca. Quando un sito disconnette la tua Machine, lei rientra con un tocco. Le password restano cifrate sulla tua Machine. **Dimentica** ne rimuove uno.

## Controlli

**Controlli** mostra come la tua Machine sta leggendo quello che arriva: le esecuzioni recenti e cosa ha trovato ciascuna. Vedi [Nessuna nuova attività](reviews-paused.md).

Ogni connessione ha un suo articolo in questa sezione, con cosa legge e cosa può inviare.
