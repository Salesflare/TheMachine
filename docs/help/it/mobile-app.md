---
title: L’app mobile
area: getting-started
summary: The Machine come app su iPhone e Android: notifiche per le tue attività e condivisione con The Machine da qualsiasi app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 672364a90f92ef8f
---
L’app mobile apre la tua dashboard personale, con l’accesso effettuato come sul web. **Scarica** l’app dall’[App Store](https://apps.apple.com/app/id6829875215) per iPhone e iPad o da [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) per Android.

L’attività **Sfrutta al meglio The Machine** in cima alla sezione Attività te la suggerisce. Nel browser del telefono, **Scarica** apre lo store. Se il telefono è impostato per mostrare i siti desktop, compaiono i link a entrambi gli store. Su un computer compare un codice QR da scansionare con il telefono e i link a entrambi gli store.

Su qualsiasi telefono, [themachine.computer/app](https://themachine.computer/app) apre lo store giusto. In **Impostazioni**, **App** trovi entrambi gli store in cima, oppure solo quello del tuo telefono se stai usando un telefono. Su un computer, **Computer** installa la dashboard come app: vedi [Installare l’app](phone-app.md).

## Collega l’app

Su una Machine ospitata, l’app accede con il tuo account. Su una Machine self-hosted, apri **Impostazioni**, **App** su un computer: sotto gli store, **Non sei nel Network?** mostra un codice. Installa l’app, poi scansiona il codice con la fotocamera del telefono oppure inserisci nell’app l’indirizzo mostrato sotto. L’app ti chiede di confermare la connessione e resta valida la modalità di accesso della tua Machine.

**Accedi con** un servizio in **Connessioni** (Shortcut, Notion, Slack, Zoom e gli altri) apre la schermata di accesso del telefono. Quando hai finito, torni all’app e la nuova connessione compare automaticamente in **Connessioni**.

Quando l’app non riesce a raggiungere la tua Machine, te lo dice e riprova automaticamente. Su un Mac o un iPad con tastiera, Cmd+R ricarica la pagina.

## Notifiche

La prima volta che si apre, l’app ti chiede di consentire le notifiche. Tocca una notifica per aprire ciò a cui si riferisce: un’attività appare nell’elenco, evidenziata; il promemoria del mattino apre la giornata di oggi nel **Calendario**; il riepilogo del team apre Attività; una domanda di Fleet apre la relativa attività. Il testo di un’attività non passa mai dai servizi di Apple, Google o The Machine: trasmettono solo una frase fissa, come «C’è un’attività che ti aspetta».

Poi l’app chiede alla tua Machine il titolo dell’attività e il passaggio successivo, per esempio «Rispondi a Sam» con «Scrivi a Sam: martedì alle 10:00 va bene». Il promemoria del mattino mostra cosa ti aspetta e l’ora della prima riunione; il riepilogo del team, i primi elementi; un aggiornamento di Fleet, cosa è successo. Se non riesce a raggiungere la tua Machine, resta visibile la frase fissa. Su Android indica quante attività ti aspettano, per esempio «Hai 2 attività».

Una notifica include **Posticipa** (fino a domani) e **Segna come fatto**, oltre a **Fallo** per un’attività non ancora iniziata. Le azioni sono disponibili dopo aver sbloccato il telefono, senza aprire l’app. L’invio e i passaggi finali aprono sempre l’app. C’è una notifica per ogni attività: «In preparazione» diventa «Pronta» e la notifica scompare quando l’attività è completata o posticipata, qui o altrove.

Quando un passaggio che hai confermato va a buon fine, la notifica mostra **Fatto** e cosa è successo, finché non tocchi **Ho capito** in Attività. Su iPhone la notifica può aggiornarsi solo la prossima volta che apri l’app.

Se disattivi **Testo nelle notifiche** in **Impostazioni**, **Sicurezza**, resta visibile la frase fissa. Lo stesso succede se la schermata di blocco nasconde il contenuto delle notifiche. Quando non può mostrare altro, la notifica dice «Tocca per aprire». Se il telefono non riesce a raggiungere la tua Machine quando arriva una notifica, ne mostra i dettagli appena torna online.

Le notifiche seguono le stesse regole delle notifiche push sul web: le preferenze per tipo che hai scelto in [Notifiche](notifications.md), il tuo [orario di lavoro](work-hours.md) e nessuna notifica mentre usi una dashboard.

Ogni telefono con l’app compare in **Impostazioni**, **Notifiche** come **Telefono con l’app**. **Rimuovi** ne interrompe le notifiche. Per riceverle, una Machine self-hosted ha bisogno di The Machine Network; l’app funziona anche senza.

## Condividi con The Machine

In qualsiasi app, tocca Condividi e scegli The Machine. Si apre una **Nuova attività** con il testo, il link o i file che hai condiviso. Controllala, aggiungi una data se vuoi e aggiungila. Non viene aggiunto nulla finché non lo fai.

Puoi condividere anche solo un file, come una fattura o una lettera. La tua Machine legge il testo di un PDF e compila l’attività: di cosa si tratta, il passaggio successivo e la data. Il file va direttamente alla tua Machine e resta lì.

Anche la dashboard installata come app su Android può ricevere contenuti condivisi: sceglila nel menu di condivisione come faresti con qualsiasi altra app.

Piani e pagamenti non sono visibili nell’app. In **Impostazioni** trovi **Apri l’account**, da cui puoi eliminare il tuo account.
