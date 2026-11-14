---
title: Promesse
area: cards
summary: Quello che hai promesso di fare e quello che gli altri hanno promesso a te. La tua Machine tiene traccia di tutto automaticamente.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 8e5ce7b371ab7fd0
---
Tieni traccia di quello che hai promesso e di quello che gli altri hanno promesso a te. La tua Machine individua automaticamente le promesse nei tuoi messaggi.

## Dove trovarle

Nella pagina Attività, sotto **Promesse**:

- Quello che hai detto che avresti fatto, e per chi: **Hai promesso**.
- Quello che gli altri hanno detto che avrebbero fatto: **Promesso a te**.

Ognuna ha un menu **⋯**:

- **Fallo** sulle tue: diventano subito un'attività e la tua Machine la prepara. **Sollecita** su quelle degli altri: la tua Machine prepara una breve bozza di sollecito nel punto in cui hanno fatto la promessa, mentre tu resti nell'elenco. Una breve nota ti dice che è in arrivo, con **Apri attività**, e la promessa mostra «un'attività adesso». Non viene inviato nulla finché non lo invii tu. Se è già un'attività, si apre quell'attività.
- **Segna come fatto**: la promessa è stata mantenuta.
- **Non succederà**: non si avvererà, quindi la tua Machine smette di tenerne traccia, senza creare un'attività.

Una promessa aperta diventa anche automaticamente un'attività intorno alla sua data (le tue la mattina prima, così hai un giorno per farlo; quelle degli altri la mattina dopo, se sono ancora aperte) e appare nel giorno corrispondente nel [Calendario](calendar.md). Se è già un'attività, la promessa rimanda a quell'attività e **Segna come fatto** o **Non succederà** la chiude a sua volta. Quando la tua Machine vede che è stata completata, chiude entrambe e lo indica con una nota.

La promessa è già stata mantenuta, per esempio con una risposta che hai inviato o una riunione in cui ne avete parlato? Si chiude automaticamente, senza creare un'attività.

La promessa riceve una nuova data successiva, per esempio «la settimana prossima invece»? La stessa promessa viene spostata, insieme alla sua attività, senza crearne una seconda. La sua pagina mostra la nuova data e il messaggio più recente.

Una promessa senza data riceve un **giorno di promemoria**: tre giorni dopo che l'hai fatta tu, una settimana dopo che l'ha fatta l'altra persona. È ancora aperta a quel punto? Diventa un'attività.

Le promesse da Slack mostrano il nome della persona.

Viene registrata anche una promessa via email di una persona a cui non hai mai scritto, contrassegnata come **mittente non verificato**: è basata solo sulla sua parola. L'attività inizia con «Non verificato: non hai mai scritto a questa persona».

Il [riepilogo settimanale](weekly-recap.md) conta quelle mantenute e quelle ancora aperte. Sul tuo computer, `assistant promises` le elenca in un terminale.
