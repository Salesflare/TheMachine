---
title: Riepilogo settimanale
area: weekly
summary: Una volta a settimana, com'è andata la tua Machine: attività, promesse, persone e progetti, e cosa ha notato. Disattivato di default.
covers: weekly-recap
code: assistant.py, config.example.json
order: 1
---
## Cosa contiene

- La tua settimana con The Machine, e quante attività ne sono valse la pena, rispetto alla settimana prima.
- Attività: nuove, fatte, scartate e posticipate, e quanto in fretta hai risposto.
- Promesse: le tue mantenute e aperte, quelle degli altri arrivate o ancora in attesa.
- Apprendimenti da condividere con il team di The Machine, se ce ne sono in attesa. Vedi [Condividi gli apprendimenti con il team](share-learnings.md).
- Persone e progetti, per esempio chi non si fa più sentire.
- Cosa ho notato: bozze inviate così com'erano o modificate, attività scartate in pochi minuti, attività posticipate più di una volta.
- Dietro le quinte: cosa ha esaminato e quanto è costato.

## Quando e dove

Una volta a settimana, di default il venerdì dopo le 16:00 nel tuo fuso orario. Arriva su [Telegram](telegram.md), oppure come notifica dal titolo "La tua settimana" dall'[app per telefono](phone-app.md).

## Attivalo

È disattivato di default, e la dashboard non ha ancora un interruttore, quindi oggi una Machine ospitata non può attivarlo. Sul tuo computer, imposta `weekly_recap` nel config.json della tua Machine: `enabled` true, e se vuoi `weekday` (da 1 a 7, il venerdì è 5) e `at` ("16:00"). Vedi la [guida alla configurazione](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
