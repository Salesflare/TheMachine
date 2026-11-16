---
title: L’app mobile
area: getting-started
summary: The Machine come app per iPhone e Android: notifiche per le tue attività e condivisione con The Machine da qualsiasi app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: f622bdc266f69965
---
L’app mobile apre la tua dashboard personale, con lo stesso accesso che usi sul web. Scaricala dall’[App Store](https://apps.apple.com/app/id6829875215) per iPhone e iPad o da [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) per Android.

L’attività **Ottieni di più da The Machine**, in cima alla sezione Attività, te la consiglia. Nel browser del telefono, **Scarica** apre lo store. Se il telefono è impostato per mostrare i siti desktop, mostra i link a entrambi gli store. Sul computer mostra un codice QR da scansionare con il telefono e i link a entrambi gli store.

Da qualsiasi telefono, [themachine.computer/app](https://themachine.computer/app) apre lo store giusto. In **Impostazioni**, **App** trovi in alto entrambi gli store, oppure solo quello del tuo telefono se lo stai usando. Sul computer, **Computer** installa la dashboard come app: scopri come fare in [Installare l’app](phone-app.md).

## Collegarla

Su una Machine ospitata, l’app accede con il tuo account. Per una Machine ospitata autonomamente, apri **Impostazioni**, **App** su un computer: sotto gli store, **Non sei nel Network?** mostra un codice. Installa l’app e scansionalo con la fotocamera del telefono, oppure inserisci nell’app l’indirizzo mostrato sotto il codice. L’app ti chiede conferma prima di collegarsi e resta necessario accedere alla tua Machine.

Toccando **Accedi con** un servizio in **Connessioni** (Shortcut, Notion, Slack, Zoom e gli altri), si apre la schermata di accesso sul telefono. Quando hai finito, torni all’app e la nuova connessione appare automaticamente in **Connessioni**.

## Notifiche

Al primo avvio, l’app ti chiede il permesso di inviare notifiche. Tocca una notifica per aprire ciò a cui si riferisce: un’attività appare nell’elenco, evidenziata; la notifica del mattino apre il giorno di oggi in **Calendario**; il riepilogo del team apre la sezione Attività; una domanda di Fleet apre la relativa attività. Il testo di un’attività non passa mai da Apple, Google o dal servizio di The Machine: tramite questi servizi viene inviata solo una frase predefinita, come «C’è un’attività che ti aspetta».

L’app chiede poi alla tua Machine il titolo dell’attività e il passo successivo, per esempio «Rispondi a Sam» con «Scrivi a Sam: martedì alle 10:00 va bene». La notifica del mattino indica cosa ti aspetta e l’ora della prima riunione; il riepilogo del team mostra le prime attività; un aggiornamento di Fleet spiega cos’è successo. Se non riesce a raggiungere la tua Machine, resta visibile la frase predefinita. Su Android indica quante attività ti aspettano, per esempio «Hai 2 attività».

Una notifica include **Posticipa** (fino a domani) e **Segna come fatto**, oltre a **Fallo** per un’attività non ancora iniziata. Queste azioni funzionano dopo aver sbloccato il telefono, senza aprire l’app. L’invio e i passaggi finali aprono sempre l’app. C’è una notifica per ogni attività: «In preparazione» diventa «Pronta» e la notifica scompare quando l’attività è completata o posticipata, qui o altrove.

Quando viene completato un passaggio che hai confermato, la notifica mostra **Fatto** e indica cos’è successo, finché non tocchi **Ho capito** nella sezione Attività. Su iPhone puoi farlo anche la prossima volta che apri l’app.

Se disattivi **Testo nelle notifiche** in **Impostazioni**, **Sicurezza**, resta visibile la frase predefinita. Lo stesso vale se la schermata di blocco nasconde il contenuto delle notifiche. Quando non può mostrare altro, la notifica dice «Tocca per aprire». Se al suo arrivo il telefono non riesce a raggiungere la tua Machine, i dettagli appariranno quando tornerà online.

Seguono le stesse regole delle notifiche push sul web: le impostazioni che hai scelto per ogni tipo in [Notifiche](notifications.md), il tuo [orario di lavoro](work-hours.md) e nessuna notifica mentre stai usando una dashboard.

Ogni telefono con l’app appare in **Impostazioni**, **Notifiche** come **Telefono con l’app**. **Rimuovi** interrompe le notifiche su quel telefono. Per riceverle, una Machine ospitata autonomamente ha bisogno di The Machine Network; l’app funziona anche senza.

## Condividere con The Machine

In qualsiasi app, tocca Condividi e scegli The Machine. Si apre una **Nuova attività** con il testo, il link o i file che hai condiviso. Controllala, aggiungi una data se vuoi e poi aggiungila. Non viene aggiunto nulla finché non confermi.

Puoi condividere anche un file da solo, per esempio una fattura o una lettera. La tua Machine legge il testo di un PDF e compila l’attività: di cosa si tratta, il passo successivo e la data. Il file viene inviato direttamente alla tua Machine e resta lì.

Anche la dashboard installata come app su Android può ricevere contenuti condivisi: scegli l’app nel menu di condivisione come faresti con le altre.

I piani e la fatturazione non sono visibili nell’app. In **Impostazioni** trovi comunque **Apri l’account**, da cui puoi eliminare il tuo account.
