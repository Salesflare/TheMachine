---
title: Promesse
area: cards
summary: Quello che hai detto che avresti fatto e quello che gli altri ti hanno promesso. La tua Machine tiene traccia di tutto da sola.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 22b81ed3f7c4801f
---
Tieni traccia di quello che hai promesso e di quello che gli altri ti hanno promesso. La tua Machine individua automaticamente le promesse nei tuoi messaggi.

## Dove trovarle

Nella pagina Attività, sotto **Promesse**:

- Quello che hai detto che avresti fatto, e per chi: **Hai promesso**.
- Quello che gli altri hanno detto che avrebbero fatto: **Promesso a te**.

Ognuna ha un menu **⋯**:

- **Fallo** sulle tue: diventa subito un’attività e la tua Machine la prepara. **Sollecita** sulle loro: la tua Machine prepara una breve bozza di sollecito nel canale in cui te l’hanno promesso, mentre tu resti nell’elenco. Compare una breve nota che dice che è in arrivo, con **Apri attività**, e la promessa mostra «ora è un’attività». Non viene inviato nulla finché non lo invii tu. Se è già un’attività, si apre quell’attività.
- **Segna come fatto**: la promessa è stata mantenuta.
- **Non succederà**: non accadrà, quindi la tua Machine smette di tenerne traccia, senza creare un’attività.

Una promessa aperta diventa automaticamente un’attività quando si avvicina la data prevista: le tue la mattina prima, così hai un giorno per occupartene; quelle degli altri la mattina dopo, se sono ancora aperte. Compare anche nel giorno corrispondente del [Calendario](calendar.md). Se è già un’attività, si collega a essa. **Segna come fatto** o **Non succederà** chiude anche l’attività. Quando la tua Machine vede che la promessa è stata mantenuta, chiude entrambe e lo segnala con una nota.

Una promessa già mantenuta, per esempio con una risposta che hai inviato o una riunione che l’ha soddisfatta? Si chiude automaticamente, senza creare un’attività.

Se in seguito viene indicata una nuova data, per esempio «la settimana prossima invece», la stessa promessa viene spostata, insieme alla sua attività, senza crearne una seconda. La sua pagina mostra la nuova data e il messaggio più recente.

Una promessa senza data riceve un giorno di **ricontatto**: tre giorni dopo averla fatta tu, una settimana dopo che l’ha fatta l’altra persona. Se a quel punto è ancora aperta, diventa un’attività.

Le promesse da Slack mostrano il nome della persona.

Viene registrata anche una promessa via email di qualcuno a cui non hai mai scritto, contrassegnata come **mittente non verificato**: è solo una sua parola. L’attività inizia con «Non verificato: non hai mai scritto a …».

## Rimborsi

Quando un negozio, una compagnia aerea, un proprietario di casa o un assicuratore ti promette un rimborso, per esempio per un ordine annullato o una richiesta approvata, la tua Machine registra l’importo, chi deve pagarti e la data in cui dovresti riceverlo. La promessa compare sotto **Promesso a te**. Solo se il messaggio specifica tutti e tre i dettagli.

Se il denaro arriva prima, per esempio con un’email che dice «rimborso elaborato», una notifica del servizio di pagamento o una notifica dell’app della tua banca sul telefono, la promessa si chiude automaticamente, senza creare un’attività.

Se il denaro non arriva entro quella data, compare una sola attività discreta: «Sollecita il rimborso di €42 da …», con una breve email da inviare che indica il numero dell’ordine o della pratica. Non viene inviato nulla finché non lo invii tu. Se alla fine ricevi il denaro, l’attività si chiude automaticamente. **Annulla** la ripristina per un giorno.

Il [riepilogo settimanale](weekly-recap.md) conta le promesse mantenute e quelle ancora aperte. Sul tuo computer, `assistant promises` le elenca in un terminale.
