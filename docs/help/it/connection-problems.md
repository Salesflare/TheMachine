---
title: Una connessione richiede assistenza
area: troubleshooting
summary: Una fonte mostra **Serve il tuo aiuto** o smette di importare dati. Ecco cosa puoi provare.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: c07a7f214b1e4deb
---
## Controlla lo stato

Apri **Connessioni**. Ogni fonte indica il proprio stato:

- **Riconnessione automatica**: un’interruzione momentanea. La fonte riprova da sola.
- **In attesa della prima sincronizzazione**: è appena stata collegata. Aspetta qualche minuto.
- **Legge di nuovo alle** 07:00: X e LinkedIn leggono solo durante il giorno. Non devi fare nulla.
- **Serve il tuo aiuto**: apri **Dettagli**. Qui trovi cosa è andato storto e cosa fare.
- **Telefono disconnesso**: il tuo telefono Android non riesce a raggiungere la tua Machine. Apri l’app OpenClaw sul telefono.

Se una fonte non importa nulla per più tempo del solito, mostra **In attesa di una nuova sincronizzazione**. Lo stato si aggiorna da solo quando una sincronizzazione va a buon fine.

Il numero su **Connessioni** conta solo le fonti che richiedono il tuo aiuto.

## Soluzioni comuni

- "Accedi di nuovo a Google" (o Microsoft): basta un clic su **Riconnetti** per ripristinare tutte le fonti di quell’account, come Gmail e Calendar.
- "devi accedere di nuovo": premi **Riconnetti** e accedi.
- Microsoft sta ancora configurando l’accesso: riprova da sola.
- Slack: premi **Riconnetti**. Hai effettuato la connessione con una chiave Maton? Controlla la chiave e la connessione Slack in Maton.
- Android: apri l’app OpenClaw sul telefono e consenti l’accesso alle notifiche.

Sul tuo computer, `assistant doctor` controlla ogni fonte e indica come risolvere ciascun problema.

Hai ancora problemi? Consulta [Ricevere assistenza](get-support.md).
