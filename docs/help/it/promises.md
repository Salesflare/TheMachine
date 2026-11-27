---
title: Promesse
area: cards
summary: Quello che hai promesso e quello che gli altri hanno promesso a te. Vengono tenute sotto controllo automaticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: b624394de7ff77b1
---
Tieni traccia di quello che hai promesso e di quello che gli altri hanno promesso a te. La tua Machine rileva automaticamente le promesse nei tuoi messaggi.

## Dove trovarle

Nella sezione **Promesse** della pagina Attività:

- Quello che hai detto che avresti fatto e per chi: **Hai promesso**.
- Quello che gli altri hanno detto che avrebbero fatto: **Promesso a te**.

Ognuna ha un menu **⋯**:

- **Fallo** sulle tue: diventano subito un’attività e la tua Machine la prepara. **Sollecita** sulle loro: la tua Machine prepara una breve email di sollecito nel luogo in cui è stata fatta la promessa, mentre tu resti nell’elenco. Una breve nota ti dice che sta per essere inviata e mostra **Apri attività**; la promessa indica «ora è un’attività». Non viene inviata finché non la invii tu. Se la promessa è già un’attività, si apre quell’attività.
- **Segna come completata**: la promessa è stata mantenuta.
- **Non succederà**: non accadrà, quindi la tua Machine smette di tenerne traccia senza creare un’attività.

Una promessa aperta diventa automaticamente un’attività intorno alla data prevista: le tue la mattina prima, così hai un giorno per completarla; quelle degli altri la mattina dopo, se sono ancora aperte. Compare anche nel giorno corrispondente nel [Calendario](calendar.md). Se è già un’attività, rimanda a quell’attività; **Segna come completata** o **Non succederà** chiude anche l’attività. Quando la tua Machine rileva che è stata completata, chiude entrambe e lo segnala con una nota.

Una risposta che si limita a promettere di fare il lavoro, come «Ti invierò i file entro martedì», non completa l’attività. L’attività resta aperta con quella data e la promessa rimanda a essa. La schermata di revisione dell’invio te lo segnala prima che tu invii il messaggio. Se prima modifichi il testo, la vecchia promessa e la data scompaiono: l’attività resta aperta finché la tua Machine non rileva che il lavoro è stato completato, e un’eventuale promessa nel messaggio che invii viene collegata all’attività.

La promessa è già stata mantenuta, per esempio con una risposta che hai inviato o una riunione in cui ne avete parlato? Si chiude automaticamente, senza creare un’attività.

Quando qualcuno risponde a una promessa che ha fatto, questa resta aperta finché la risposta non mostra che è stata mantenuta. Un «Certo» o una risposta che ne mantiene solo una parte non basta. Se era in attesa l’invio di un sollecito, questo viene annullato e l’attività resta aperta con la nota «Ha scritto di nuovo». Una risposta automatica di assenza non cambia nulla.

La promessa ha una nuova data successiva, come «la prossima settimana invece»? La stessa promessa e la relativa attività vengono spostate, senza crearne una seconda. La sua pagina mostra la nuova data e il messaggio più recente.

Una promessa senza data riceve un giorno per il **sollecito**: tre giorni dopo che l’hai fatta, una settimana dopo che l’ha fatta l’altra persona. Se a quel punto è ancora aperta, diventa un’attività.

Le promesse di Slack mostrano il nome della persona.

La tua Machine registra anche le promesse ricevute via email da persone a cui non hai mai scritto, contrassegnandole come **mittente non verificato**: sono basate solo sulla parola di chi le ha fatte. L’attività inizia con «Non verificato: non hai mai scritto a questa persona».

## Rimborsi

Quando un negozio, una compagnia aerea, un proprietario di casa o una compagnia assicurativa ti promette un rimborso, per esempio per un ordine annullato o una richiesta approvata, la tua Machine registra l’importo, chi deve pagarlo e la data prevista. La promessa compare in **Promesso a te**. Solo se il messaggio specifica tutti e tre i dettagli.

Se il rimborso arriva prima, per esempio con un’email che dice «rimborso elaborato», una notifica del servizio di pagamento o una notifica dell’app della banca sul tuo telefono, la promessa si chiude automaticamente, senza creare un’attività.

Il rimborso non è arrivato entro quella data? Compare un’attività discreta: «Sollecita il rimborso di 42 € da …», con una breve email da inviare che include il numero dell’ordine o della pratica. Non viene inviata finché non la invii tu. Se poi il denaro arriva, l’attività si chiude automaticamente. **Annulla** la riapre per un giorno.

Il [riepilogo settimanale](weekly-recap.md) conta le promesse mantenute e quelle ancora aperte. Sul tuo computer, `assistant promises` le elenca in un terminale.
