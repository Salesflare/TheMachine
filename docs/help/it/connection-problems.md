---
title: Una connessione ha bisogno di aiuto
area: troubleshooting
summary: Una fonte dice Serve il tuo aiuto, o non porta più nulla. Cosa provare.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
---
## Controlla lo stato

Apri **Connessioni**. Ogni fonte dice come sta andando:

- **Riconnessione automatica**: un breve intoppo. Riprova da sola.
- **In attesa della prima sincronizzazione**: appena collegata. Aspetta qualche minuto.
- **Legge di nuovo alle** 07:00: X e LinkedIn leggono solo di giorno. Non serve fare nulla.
- **Serve il tuo aiuto**: apri **Dettagli**. Spiega cosa è andato storto e cosa fare.
- **Telefono disconnesso**: il telefono non raggiunge OpenClaw. Apri l’app OpenClaw sul telefono.

Una fonte che continua a fallire e non porta nulla di nuovo per ore, più a lungo della sua solita pausa, non risulta collegata. Si risolve da sola appena arriva qualcosa di nuovo.

Il numero su **Connessioni** conta solo le fonti a cui serve il tuo aiuto.

## Soluzioni comuni

- "Accedi di nuovo a Google" (o Microsoft): una riga per account. Un solo **Riconnetti** ripristina tutte le sue fonti, come Gmail e Calendar.
- "deve accedere di nuovo": premi **Riconnetti** e accedi. Su una Machine in hosting, accedi direttamente lì e torni alla dashboard.
- Microsoft sta ancora configurando l'accesso: riprova da sola.
- Slack: controlla la tua chiave API di Maton e la connessione Slack in Maton.
- Android: apri l'app OpenClaw sul telefono e dalle l'accesso alle notifiche.

Sul tuo computer, `assistant doctor` controlla ogni fonte e mostra la soluzione per ogni problema.

Ancora bloccato? Vedi [Ricevi assistenza](get-support.md).
