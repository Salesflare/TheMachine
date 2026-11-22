---
title: Riepilogo settimanale
area: weekly
summary: Una volta a settimana, scopri come se l’è cavata la tua Machine: attività, promesse, persone e progetti, e cosa ha notato. Attivo per impostazione predefinita.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 223b143a6efd5692
---
## Cosa include

- Serve il tuo intervento: promesse scadute fatte a te e promesse che hai fatto tu, scadute o in scadenza nelle prossime due settimane.
- La prossima settimana: le tue riunioni (con un link quando la preparazione è pronta), le attività in scadenza e le promesse fatte da altri per quel periodo.
- Cosa è cambiato: quante attività sono state utili rispetto alla settimana precedente, quante volte **Fallo** ha funzionato al primo tentativo, cosa ha modificato nel modo in cui scrivi e nei suoi filtri, e quante bozze sono state inviate così come erano.
- Per il team di The Machine: apprendimenti da condividere, se ce ne sono in attesa. Vedi [Condividere gli apprendimenti con il team](share-learnings.md).
- Persone e progetti: i progetti che stanno prendendo slancio o rallentando, chi è nuovo e chi non si fa più sentire.
- Dietro le quinte: quanti segnali ha controllato questa settimana e quanti sono ancora in attesa.
- Su [Telegram](telegram.md), seguono delle scelte, ognuna nel suo messaggio: una fonte molto attiva senza risultati (**Smetti di controllare** o **Continua a controllare**) e un’attività posticipata più di una volta (**Non serve**, **Fallo** o **Tieni**). Non cambia nulla finché non tocchi una scelta.

## Quando e dove

Una volta a settimana, il venerdì dopo le 16:00 nel tuo fuso orario, per impostazione predefinita. Arriva su [Telegram](telegram.md) oppure come notifica intitolata "La tua settimana" dall’[app per telefono](phone-app.md) e dall’app dashboard. Arriva anche via email quando l’email è attiva per **Riepilogo del mattino** in Impostazioni › Notifiche. Con [Prudente](security-levels.md), o se **Testo nelle notifiche** è disattivato, non arriva via email.

## Disattivarlo

È attivo per impostazione predefinita. Per disattivarlo, vai in Impostazioni › Notifiche e disattiva **Riepilogo settimanale**. Se lo hai disattivato, resta disattivato. Sul tuo computer puoi anche impostare `weekly_recap` in config.json: `enabled` false con `chosen` true, e, se vuoi, `weekday` (da 1 a 7, venerdì è 5) e `at` ("16:00"). Consulta la [guida alla configurazione](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
