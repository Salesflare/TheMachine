---
title: Promesse
area: cards
summary: Quello che hai detto che avresti fatto e quello che gli altri hanno promesso a te. Tutto viene monitorato automaticamente.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: dbac0241c54b0ec6
---
Tieni traccia di quello che hai promesso e di quello che gli altri hanno promesso a te. La tua Machine individua automaticamente le promesse nei tuoi messaggi.

## Dove trovarle

Nella sezione **Promesse** della pagina Attività:

- Quello che hai detto che avresti fatto e per chi: **Hai promesso**.
- Quello che gli altri hanno detto che avrebbero fatto: **Promesso a te**.

Ognuna ha un menu **⋯**:

- **Fallo** sulle tue promesse: diventano subito un’attività e la tua Machine la prepara. **Sollecita** sulle promesse degli altri: la tua Machine prepara una breve richiesta di aggiornamento nel luogo in cui è stata fatta la promessa, mentre tu resti nell’elenco. Compare una breve nota che ti avvisa che sta per arrivare, con **Apri attività**, e la promessa mostra «un’attività adesso». Non viene inviato nulla finché non lo invii tu. Se è già un’attività, si apre quell’attività.
- **Segna come fatto**: la promessa è stata mantenuta.
- **Non succederà**: non accadrà, quindi la tua Machine smette di monitorarla e non crea un’attività.

Una promessa aperta diventa automaticamente un’attività quando arriva la scadenza (le tue la mattina prima, così hai un giorno per occupartene) e compare nel giorno corrispondente del [Calendario](calendar.md). Se è già un’attività, rimanda a quell’attività; **Segna come fatto** o **Non succederà** chiude anche l’attività. Quando la tua Machine vede che è stata completata, chiude entrambe e te lo segnala con una riga.

È già stata mantenuta, per esempio con una risposta che hai inviato o una riunione in cui se ne è parlato? Si chiude automaticamente, senza creare un’attività.

Viene indicata una nuova data in seguito, per esempio «la prossima settimana invece»? La data della stessa promessa cambia, insieme a quella della sua attività, senza crearne una seconda. La sua pagina mostra la nuova data e il messaggio più recente.

Alle promesse senza data viene assegnato un giorno per il **sollecito**: tre giorni dopo che hai fatto la promessa, una settimana dopo che l’ha fatta l’altra persona. Se a quel punto è ancora aperta, diventa un’attività.

Le promesse di Slack mostrano il nome della persona.

Viene monitorata anche una promessa ricevuta via email da qualcuno a cui non hai mai scritto, contrassegnata come **mittente non verificato**: è solo la sua parola. L’attività inizia con «Non verificato: non gli hai mai scritto prima».

Il [riepilogo settimanale](weekly-recap.md) conta le promesse mantenute e quelle ancora aperte. Sul tuo computer, `assistant promises` le elenca in un terminale.
