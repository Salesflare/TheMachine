---
title: Promesse
area: cards
summary: Tieni traccia di ciò che hai promesso e di ciò che gli altri hanno promesso a te. La tua Machine se ne occupa da sola.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: ba0e2190e1b8b791
---
Tieni traccia di ciò che hai promesso e di ciò che gli altri hanno promesso a te. La tua Machine individua da sola le promesse nei tuoi messaggi.

## Dove trovarle

Nella pagina Attività, sotto **Promesse**:

- Ciò che hai detto che avresti fatto e per chi: **Hai promesso**.
- Ciò che gli altri hanno detto che avrebbero fatto: **Promesso a te**.

Ognuna ha un menu **⋯**:

- **Fallo** sulle tue: diventano subito un’attività e la tua Machine la prepara. **Sollecita** su quelle degli altri: la tua Machine prepara una bozza di breve sollecito nel luogo in cui hanno fatto la promessa, mentre tu resti nell’elenco. Una breve nota dice che sta per partire, con **Apri attività**, e la promessa mostra «un’attività ora». Non viene inviato nulla finché non lo invii tu. Se è già un’attività, si apre quell’attività.
- **Segna come fatto**: la promessa è stata mantenuta.
- **Non succederà**: non accadrà, quindi la tua Machine smette di tenerne traccia e non crea un’attività.

Una promessa aperta diventa anche un’attività da sola, in prossimità della sua data (le tue la mattina prima, così hai un giorno per farlo; quelle degli altri la mattina dopo, se sono ancora aperte) e compare nel giorno corrispondente del [Calendario](calendar.md). Se è già un’attività, rimanda a quell’attività, e **Segna come fatto** o **Non succederà** chiude anche l’attività. Quando la tua Machine rileva che è stata completata, chiude entrambe e lo segnala con una nota.

Una risposta che si limita a promettere il lavoro, come «Ti invierò i file entro martedì», non completa l’attività. L’attività resta aperta con quella data e la promessa rimanda a essa. Prima dell’invio, la schermata di revisione lo segnala.

Se la promessa è già stata mantenuta, per esempio con una risposta che hai inviato o durante una riunione, si chiude da sola, senza creare un’attività.

Quando qualcuno risponde a una promessa che ha fatto, questa resta aperta finché la risposta non dimostra che è stata mantenuta. Un «Certo», una risposta automatica o una risposta che mantiene solo una parte della promessa non bastano. Se era in attesa di invio un sollecito, questo viene annullato e l’attività resta aperta con la nota «Ti hanno riscritto».

Se la promessa riceve una nuova data successiva, per esempio «meglio la prossima settimana», la stessa promessa viene spostata, insieme alla sua attività, senza crearne una seconda. La sua pagina mostra la nuova data e il messaggio più recente.

Se non ha una data, le viene assegnato un giorno per il sollecito: tre giorni dopo che l’hai fatta tu, una settimana dopo che l’ha fatta qualcun altro. Se è ancora aperta quel giorno, diventa un’attività.

Le promesse da Slack mostrano il nome della persona.

Anche una promessa ricevuta via email da una persona a cui non hai mai scritto viene registrata, contrassegnata come **mittente non verificato**: è solo la sua parola. Il nome dell’attività inizia con «Non verificato: non hai mai scritto a questa persona».

## Rimborsi

Quando un negozio, una compagnia aerea, un locatore o un assicuratore ti promette un rimborso, per esempio per un ordine annullato o una richiesta approvata, la tua Machine registra l’importo, chi deve pagare e la data prevista per l’accredito. Lo trovi sotto **Promesso a te**. Succede solo se il messaggio specifica chiaramente tutti e tre i dettagli.

Se il rimborso arriva prima, per esempio con un’email «rimborso elaborato», una notifica del servizio di pagamento o una notifica dell’app della banca sul telefono, la promessa si chiude da sola, senza creare un’attività.

Se non è arrivato entro quella data, viene creata una sola attività discreta: «Sollecita il rimborso di 42 € da …», con un breve messaggio da inviare via email che indica il numero dell’ordine o della pratica. Non viene inviato nulla finché non lo invii tu. Se poi il denaro arriva, l’attività si chiude da sola. **Annulla** la riapre per un giorno.

Il [riepilogo settimanale](weekly-recap.md) conta le promesse mantenute e quelle ancora aperte. Sul tuo computer, `assistant promises` le elenca in un terminale.
