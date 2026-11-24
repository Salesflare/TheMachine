---
title: Promesse
area: cards
summary: Quello che hai promesso di fare e quello che gli altri hanno promesso a te. Il monitoraggio è automatico.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 0bc6594bbd8f4c0b
---
Tieni traccia di quello che hai promesso e di quello che gli altri hanno promesso a te. La tua Machine individua automaticamente le promesse nei tuoi messaggi.

## Dove trovarle

Nella pagina Attività, sotto **Promesse**:

- Quello che hai promesso di fare e per chi: **Hai promesso**.
- Quello che gli altri hanno detto che faranno: **Promesso a te**.

Ognuna ha un menu **⋯**:

- **Fallo** sulle tue promesse: diventa subito un'attività e la tua Machine la prepara. **Sollecita** su quelle degli altri: la tua Machine prepara una breve bozza di sollecito nella conversazione in cui l'hanno promesso, mentre tu resti nell'elenco. Una breve nota ti avvisa che è in preparazione, con **Apri attività**, e la promessa mostra «ora è un'attività». Non viene inviato nulla finché non lo invii tu. Se è già un'attività, si apre direttamente.
- **Segna come fatto**: la promessa è stata mantenuta.
- **Non succederà**: non si realizzerà, quindi la tua Machine smette di monitorarla e non crea un'attività.

Una promessa aperta diventa automaticamente un'attività nei pressi della data prevista: le tue la mattina prima, così hai un giorno per occupartene; quelle degli altri la mattina dopo, se sono ancora aperte. La promessa compare anche nel giorno corrispondente del [Calendario](calendar.md). Se è già un'attività, rimanda a quell'attività; **Segna come fatto** o **Non succederà** la chiude a sua volta. Quando la tua Machine rileva che è stata completata, chiude entrambe e aggiunge una nota.

Una risposta che si limita a promettere di svolgere il lavoro, come «Ti invierò i file entro martedì», non completa l'attività. L'attività resta aperta con quella data e la promessa rimanda a essa. La revisione dell'invio te lo segnala prima che tu invii il messaggio.

Se la promessa è già stata mantenuta, per esempio con una risposta che hai inviato o una riunione in cui te ne sei occupato, viene chiusa automaticamente e non crea un'attività.

Quando qualcuno risponde a una promessa fatta da lui, questa resta aperta finché la risposta non dimostra che è stata mantenuta. Un «Certo» o una risposta che ne mantiene solo una parte non basta. Se era in attesa di essere inviato un sollecito, questo viene annullato e l'attività resta aperta con la nota «Ha scritto di nuovo». Una risposta automatica di assenza non cambia nulla.

Se viene indicata una nuova data successiva, per esempio «meglio la settimana prossima», la stessa promessa viene spostata, insieme alla relativa attività, senza crearne un'altra. La pagina mostra la nuova data e il messaggio più recente.

Se non ha una data, le viene assegnato un giorno di **sollecito**: tre giorni dopo se l'hai fatta tu, una settimana dopo se l'ha fatta qualcun altro. Se è ancora aperta quel giorno, diventa un'attività.

Le promesse di Slack mostrano il nome della persona.

Vengono registrate anche le promesse ricevute via email da persone a cui non hai mai scritto, contrassegnate come **mittente non verificato**: si basano solo sulla loro parola. L'attività inizia con «Non verificato: non hai mai scritto a questa persona».

## Rimborsi

Quando un negozio, una compagnia aerea, un proprietario o un assicuratore ti promette un rimborso, per esempio per un ordine annullato o una richiesta di rimborso approvata, la tua Machine registra l'importo, chi deve pagarlo e la data prevista. La promessa compare sotto **Promesso a te**. Solo se il messaggio specifica tutti e tre i dettagli.

Se il denaro arriva prima, per esempio con un'email che dice «rimborso elaborato», una notifica del servizio di pagamento o una notifica dell'app della tua banca sul telefono, la promessa si chiude automaticamente e non crea un'attività.

Se il denaro non è arrivato entro quella data, viene creata una sola attività discreta: «Sollecita il rimborso di 42 € da …», con una breve email che cita il numero dell'ordine o della pratica. Non viene inviato nulla finché non lo invii tu. Se alla fine il denaro arriva, l'attività si chiude automaticamente. **Annulla** la riapre per un giorno.

Il [riepilogo settimanale](weekly-recap.md) conta le promesse mantenute e quelle ancora aperte. Sul tuo computer, `assistant promises` le elenca in un terminale.
