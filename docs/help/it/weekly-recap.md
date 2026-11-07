---
title: Riepilogo settimanale
area: weekly
summary: Una volta a settimana, com'è andata la tua Machine: attività, promesse, persone e progetti, e cosa ha notato. Attivo di default.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
---
## Cosa contiene

- La tua settimana con The Machine, e quante attività ne sono valse la pena, rispetto alla settimana prima.
- Attività: nuove, fatte, scartate e posticipate, e quanto in fretta hai risposto.
- Promesse: le tue mantenute e aperte, quelle degli altri arrivate o ancora in attesa.
- Apprendimenti da condividere con il team di The Machine, se ce ne sono in attesa. Vedi [Condividi gli apprendimenti con il team](share-learnings.md).
- Persone e progetti, per esempio chi non si fa più sentire.
- Cosa ho notato: bozze inviate così com'erano o modificate, attività scartate in pochi minuti, attività posticipate più di una volta.
- Dietro le quinte: quanti segnali ha controllato questa settimana e quanti sono ancora in attesa.
- Scelte, ognuna in un suo messaggio dopo il riepilogo: una fonte molto attiva senza risultati (**Smetti di controllare** o **Continua a controllare**) e un'attività posticipata più di una volta (**Lascia perdere**, **Fallo ora** o **Tieni**). Non cambia nulla finché non tocchi.

## Quando e dove

Una volta a settimana, di default il venerdì dopo le 16:00 nel tuo fuso orario. Arriva su [Telegram](telegram.md), oppure come notifica dal titolo "La tua settimana" dall'[app per telefono](phone-app.md) e dall'app della dashboard. Arriva anche via email quando l'email è attiva per **Riepilogo del mattino** in Impostazioni › Notifiche. Con [Prudente](security-levels.md) non arriva via email.

## Disattivalo

È attivo di default. Disattivalo in Impostazioni › Notifiche con l'interruttore **Riepilogo settimanale**. Se l'hai disattivato, resta disattivato. Sul tuo computer puoi anche impostare `weekly_recap` nel config.json: `enabled` false con `chosen` true, e se vuoi `weekday` (da 1 a 7, il venerdì è 5) e `at` ("16:00"). Vedi la [guida alla configurazione](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
