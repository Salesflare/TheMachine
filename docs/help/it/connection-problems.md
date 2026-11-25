---
title: Una connessione richiede il tuo aiuto
area: troubleshooting
summary: Una fonte mostra «Serve il tuo aiuto» oppure smette di importare dati. Ecco cosa fare.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: cc4b227abd053022
---
## Controlla lo stato

Apri **Connessioni**. Ogni fonte indica il proprio stato:

- **Riconnessione automatica**: un breve intoppo. La fonte riprova da sola.
- **In attesa della prima sincronizzazione**: la connessione è stata appena stabilita. Attendi qualche minuto.
- **Prossima lettura alle** 07:00: X e LinkedIn acquisiscono dati solo di giorno. Non devi fare nulla.
- **Configurazione non ancora completata**: nessuno ha ancora effettuato l’accesso a questa fonte. Premi **Collega**. Si avvierà entro un minuto.
- **Serve il tuo aiuto**: apri **Dettagli**. Qui trovi cosa è andato storto e cosa fare.
- **Telefono disconnesso**: il tuo telefono Android non riesce a raggiungere la tua Machine. Apri l’app OpenClaw sul telefono.

Se una fonte non importa nulla per più tempo del solito, mostra **In attesa di una nuova sincronizzazione**. Il messaggio scompare da solo non appena una sincronizzazione va a buon fine.

Il numero accanto a **Connessioni** conta solo le fonti che richiedono il tuo aiuto.

## Soluzioni comuni

- «Accedi di nuovo a Google» (o Microsoft): basta premere **Riconnetti** una volta per riattivare tutte le fonti di quell’account, come Gmail e Calendario.
- «devi effettuare di nuovo l’accesso»: premi **Riconnetti** e accedi.
- «serve un programma che non è su questo computer»: esegui in un terminale su quel computer il comando indicato nella scheda. Ti dice cosa installare oppure trova un programma che è stato spostato.
- Microsoft sta ancora configurando l’accesso: riprova da sola.
- Slack: premi **Riconnetti**. Hai effettuato la connessione con una chiave Maton? Controlla la chiave e la connessione Slack in Maton.
- Android: apri l’app OpenClaw sul telefono e consentile di accedere alle notifiche.

Sul tuo computer, `assistant doctor` controlla tutte le fonti e indica come risolvere ogni problema.

Hai ancora problemi? Consulta [Contatta l’assistenza](get-support.md).
