---
title: Promesse
area: cards
summary: Quello che hai detto che avresti fatto e ciò che gli altri ti hanno promesso. Il monitoraggio è automatico.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Tieni traccia di ciò che hai promesso e di ciò che gli altri ti hanno promesso. La tua Machine individua automaticamente le promesse nei tuoi messaggi.

## Dove trovarle

Nella sezione **Promesse** della pagina delle attività:

- Quello che hai detto che avresti fatto e per chi: **Hai promesso**.
- Quello che gli altri hanno detto che avrebbero fatto: **Promesso a te**.

Ognuna ha un menu **⋯**:

- **Fallo**, per le tue promesse: diventano subito un'attività e la tua Machine la prepara. **Sollecita**, per quelle degli altri: la tua Machine prepara una breve risposta nella conversazione in cui hanno fatto la promessa, mentre tu resti nell'elenco. Una breve nota ti avvisa che è in preparazione, con **Apri attività**, e la promessa mostra «un'attività ora». Non viene inviato nulla finché non lo invii tu. Se è già un'attività, si apre quell'attività.
- **Segna come fatto**: la promessa è stata mantenuta.
- **Non succederà**: non accadrà, quindi la tua Machine smette di monitorarla senza creare un'attività.

Una promessa aperta diventa automaticamente un'attività più o meno alla data prevista: le tue la mattina prima, così hai un giorno per mantenerle; quelle degli altri la mattina dopo, se sono ancora aperte. Appare anche nel giorno corrispondente del [Calendario](calendar.md). Se è diventata un'attività, rimanda a quell'attività e **Segna come fatto** o **Non succederà** chiude anche l'attività. Quando la tua Machine rileva che è stata mantenuta, chiude entrambe e lo indica con una nota.

Una risposta che si limita a promettere di fare il lavoro, come «Ti invierò i file entro martedì», non completa l'attività. L'attività resta aperta con quella data e la promessa rimanda ad essa. La schermata di revisione dell'invio te lo segnala prima che tu invii il messaggio.

La promessa è già stata mantenuta, per esempio con una risposta che hai inviato o una riunione in cui hai risolto la questione? Si chiude automaticamente, senza creare un'attività.

La promessa ha una nuova data, per esempio «piuttosto la settimana prossima»? La stessa promessa viene spostata, insieme alla sua attività, senza crearne una seconda. La sua pagina mostra la nuova data e il messaggio più recente.

Una promessa senza data riceve un giorno di **promemoria**: tre giorni dopo che l'hai fatta, una settimana dopo che l'ha fatta l'altra persona. Se è ancora aperta, diventa un'attività.

Le promesse di Slack mostrano il nome della persona.

Viene registrata anche una promessa via email da qualcuno a cui non hai mai scritto, contrassegnata come **mittente non verificato**: è solo una sua parola. L'attività inizia con «Non verificato: non hai mai scritto a questa persona».

## Rimborsi

Quando un negozio, una compagnia aerea, un proprietario di casa o una compagnia assicurativa ti promette un rimborso, per esempio per un ordine annullato o una richiesta di risarcimento approvata, la tua Machine registra l'importo, chi deve pagarlo e la data prevista. Lo trovi in **Promesso a te**. Succede solo quando il messaggio specifica chiaramente tutti e tre i dati.

Quando il rimborso arriva prima, per esempio con un'email che dice «rimborso elaborato», una notifica del servizio di pagamento o una notifica dell'app della banca sul telefono, la promessa si chiude automaticamente, senza creare un'attività.

Non è arrivato entro quella data? Viene creata una sola attività discreta: «Sollecita il rimborso di 42 € da …», con una breve email che cita il numero dell'ordine o della pratica. Non viene inviato nulla finché non lo invii tu. Se il rimborso arriva comunque, l'attività si chiude automaticamente. **Annulla** la riapre per un giorno.

Il [riepilogo settimanale](weekly-recap.md) conta le promesse mantenute e quelle ancora aperte. Sul tuo computer, `assistant promises` le elenca in un terminale.
