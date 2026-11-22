---
title: Promesse
area: cards
summary: Ciò che hai promesso di fare e ciò che gli altri hanno promesso a te. Tutto viene monitorato automaticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Tieni traccia di ciò che hai promesso e di ciò che gli altri hanno promesso a te. La tua Machine individua automaticamente le promesse nei tuoi messaggi.

## Dove si trovano

Nella pagina Attività, sotto **Promesse**:

- Ciò che hai promesso di fare e a chi: **Hai promesso**.
- Ciò che gli altri hanno promesso di fare: **Promesso a te**.

Ogni promessa ha un menu **⋯**:

- Sulle tue, **Fallo**: diventano subito un’attività e la tua Machine la prepara. Sulle promesse degli altri, **Sollecita**: la tua Machine prepara una breve bozza di sollecito nel punto in cui hanno fatto la promessa, mentre tu resti nell’elenco. Una breve nota dice che è in arrivo, con **Apri attività**, e la promessa mostra «ora è un’attività». Non viene inviato nulla finché non lo invii. Se è già un’attività, si apre direttamente.
- **Segna come mantenuta**: la promessa è stata mantenuta.
- **Non succederà**: non si realizzerà, quindi la tua Machine smette di monitorarla senza creare un’attività.

Una promessa aperta diventa automaticamente anche un’attività intorno alla sua data (le tue la mattina prima, così hai un giorno per svolgerla; quelle degli altri la mattina dopo, se sono ancora aperte) e compare nel giorno corrispondente nel [Calendario](calendar.md). Se è già un’attività, rimanda a essa; **Segna come mantenuta** o **Non succederà** chiude anche quell’attività. Quando la tua Machine rileva che è stata completata, entrambe vengono chiuse e compare una nota che lo segnala.

Una risposta che si limita a promettere il lavoro, come «Invierò i file entro martedì», non completa l’attività. L’attività resta aperta con quella data e la promessa rimanda a essa. La schermata di revisione dell’invio lo segnala prima che tu invii il messaggio.

Una promessa già mantenuta, per esempio con una risposta che hai inviato o durante una riunione? Si chiude automaticamente, senza creare un’attività.

Viene indicata una nuova data successiva, per esempio «la settimana prossima invece»? La promessa viene aggiornata, così come la sua attività, senza crearne una seconda. La sua pagina mostra la nuova data e il messaggio più recente.

Una promessa senza data riceve un giorno di **sollecito**: tre giorni dopo che l’hai fatta tu, una settimana dopo che l’ha fatta l’altra persona. Se è ancora aperta a quel punto, diventa un’attività.

Le promesse di Slack mostrano il nome della persona.

Viene registrata anche una promessa via email di una persona a cui non hai mai scritto, contrassegnata come **mittente non verificato**: è solo una sua parola. L’attività inizia con «Non verificato: non hai mai scritto a questa persona».

## Rimborsi

Quando un negozio, una compagnia aerea, un proprietario di casa o un’assicurazione ti promette un rimborso, per esempio per un ordine annullato o una richiesta di risarcimento approvata, la tua Machine registra l’importo, chi paga e il giorno in cui dovrebbe arrivare. La promessa compare sotto **Promesso a te**. Solo se il messaggio indica chiaramente tutti e tre i dati.

Se il denaro arriva prima, per esempio con un’email che conferma l’elaborazione del rimborso, una notifica del servizio di pagamento o una notifica dell’app della banca sul telefono, la promessa si chiude automaticamente, senza creare un’attività.

Non è arrivato entro quel giorno? Compare una sola attività discreta: «Sollecita il rimborso di 42 € da …», con una breve email che indica il numero dell’ordine o della pratica. Non viene inviato nulla finché non lo invii. Se poi il denaro arriva, l’attività si chiude automaticamente. **Annulla** la riapre per un giorno.

Il [Riepilogo settimanale](weekly-recap.md) conta le promesse mantenute e quelle ancora aperte. Sul tuo computer, `assistant promises` le elenca in un terminale.
