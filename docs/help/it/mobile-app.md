---
title: L’app mobile
area: getting-started
summary: The Machine come app per iPhone e Android: notifiche per le tue attività e condivisione con The Machine da qualsiasi app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 0d4d41134db91fcc
---
L’app mobile apre la tua dashboard personale, con lo stesso accesso che usi sul web. Scaricala dall’[App Store](https://apps.apple.com/app/id6829875215) per iPhone e iPad o da [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) per Android.

L’attività **Ottieni di più da The Machine**, in cima alla sezione Attività, ti suggerisce di scaricarla. Nel browser di un telefono, **Scarica** apre lo store. Se il telefono è impostato per mostrare i siti desktop, vedrai i link a entrambi gli store. Su un computer, vedrai un codice QR da scansionare con il telefono e i link a entrambi gli store.

Da qualsiasi telefono, [themachine.computer/app](https://themachine.computer/app) apre lo store giusto. In **Impostazioni**, **App** trovi i link a entrambi gli store in cima, oppure solo quello del tuo telefono se lo usi da un telefono. Su un computer, **Computer** installa la dashboard come app: scopri come fare in [Installare l’app](phone-app.md).

## Collega l’app

Su una Machine ospitata, l’app accede con il tuo account. Se la Machine è ospitata da te, apri **Impostazioni**, **App** su un computer: sotto gli store, **Non sei nel Network?** mostra un codice. Installa l’app, poi scansiona il codice con la fotocamera del telefono oppure inserisci nell’app l’indirizzo che trovi sotto il codice. L’app ti chiede conferma prima di connettersi e continua a valere l’accesso richiesto dalla tua Machine.

## Notifiche

La prima volta che si apre, l’app chiede il permesso di inviare notifiche. Tocca una notifica per aprire il contenuto: un’attività appare nell’elenco, evidenziata; la notifica del mattino apre il giorno di oggi in **Calendario**; il riepilogo del team apre la sezione Attività; una domanda di Fleet apre la relativa attività. Il testo di un’attività non passa mai da Apple, Google o dal servizio di The Machine: questi trasmettono solo un messaggio fisso, come «C’è un’attività che ti aspetta».

Poi l’app chiede alla tua Machine il titolo dell’attività e il passaggio successivo, per esempio «Rispondi a Sam» con «Scrivi a Sam: martedì alle 10:00 va bene». La notifica del mattino mostra le attività in attesa e l’ora della prima riunione; il riepilogo del team mostra le prime attività; un aggiornamento di Fleet mostra cos’è successo. Se non riesce a raggiungere la tua Machine, resta il messaggio fisso. Su Android indica quante attività sono in attesa, per esempio «Hai 2 attività che ti aspettano».

Una notifica include **Posticipa** (fino a domani) e **Segna come fatto**, oltre a **Fallo** per un’attività non ancora iniziata. Le opzioni funzionano dopo aver sbloccato il telefono, senza aprire l’app. Per inviare o completare i passaggi finali devi sempre aprire l’app. C’è una notifica per ogni attività: «In preparazione» diventa «Pronta» e scompare quando l’attività viene completata o posticipata, qui o altrove.

Quando un passaggio che hai confermato va a buon fine, la notifica indica **Fatto** e spiega cos’è successo. Rimane finché non tocchi **Ho capito** nella sezione Attività. Su iPhone puoi farlo anche la prossima volta che apri l’app.

Se disattivi **Testo nelle notifiche** in **Impostazioni**, **Sicurezza**, rimane il messaggio fisso. Lo stesso vale se la schermata di blocco nasconde il contenuto delle notifiche. Se non può mostrare altro, l’app dice «Tocca per aprire». Se quando arriva una notifica il telefono non riesce a raggiungere la tua Machine, ne mostra i dettagli appena torna online.

Seguono le stesse regole delle notifiche push sul web: le scelte che hai fatto per ogni tipo in [Notifiche](notifications.md), il tuo [orario di lavoro](work-hours.md) e nessuna notifica mentre usi una dashboard.

Ogni telefono con l’app appare in **Impostazioni**, **Notifiche** come **Telefono con l’app**. **Rimuovi** interrompe le notifiche su quel telefono. Per ricevere notifiche su una Machine ospitata da te serve The Machine Network, ma l’app funziona anche senza.

## Condividi con The Machine

In qualsiasi app, tocca Condividi e scegli The Machine. Si apre una **Nuova attività** con il testo, il link o i file che hai condiviso. Controllala, aggiungi una data se vuoi e aggiungila. Non viene aggiunto nulla finché non lo fai.

Puoi condividere anche solo un file, per esempio una fattura o una lettera. La tua Machine legge il testo di un PDF e compila l’attività: di cosa si tratta, qual è il passaggio successivo e la data. Il file va direttamente alla tua Machine e rimane lì.

Anche la dashboard installata come app su Android può ricevere contenuti condivisi: scegli la dashboard dal menu di condivisione, come faresti con qualsiasi altra app.

Nell’app non trovi i piani e la fatturazione. In **Impostazioni** trovi comunque **Apri l’account** per eliminare il tuo account.
