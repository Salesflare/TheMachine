---
title: L’app mobile
area: getting-started
summary: The Machine come app su iPhone e Android: notifiche per le tue attività e condivisione con The Machine da qualsiasi app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 3865fe910a5427fb
---
L’app mobile apre la tua dashboard personale, con lo stesso accesso che usi sul web. Scaricala dall’[App Store](https://apps.apple.com/app/id6829875215) per iPhone e iPad o da [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) per Android.

L’attività **Ottieni di più da The Machine**, in cima alla sezione Attività, ti consiglia di scaricarla. Nel browser del telefono, **Scarica** apre lo store. Se il telefono è impostato per mostrare i siti desktop, mostra i link a entrambi gli store. Su un computer mostra un codice QR da scansionare con il telefono e i link a entrambi gli store.

Da qualsiasi telefono, [themachine.computer/app](https://themachine.computer/app) apre lo store giusto. In **Impostazioni**, **App** trovi entrambi gli store in cima, oppure solo quello del telefono se stai usando un telefono. Su un computer, **Computer** installa la dashboard come app: scopri come fare in [Installa l’app](phone-app.md).

## Connettila

Su una Machine ospitata, l’app accede con il tuo account. Su una Machine autogestita, apri **Impostazioni**, **App** da un computer: sotto gli store, **Non sei nel Network?** mostra un codice. Installa l’app, poi scansionalo con la fotocamera del telefono oppure digita nell’app l’indirizzo che trovi sotto il codice. L’app ti chiede conferma prima di connettersi e resta valida la procedura di accesso della tua Machine.

## Notifiche

Quando si apre per la prima volta, l’app ti chiede se vuoi consentire le notifiche. Tocca una notifica per aprire il contenuto a cui si riferisce: un’attività apre la relativa chat, il messaggio del mattino apre la giornata nel **Calendario**, il briefing del team apre la sezione Attività e una domanda di Fleet apre la relativa attività. Il testo di un’attività non passa mai da Apple, Google o dal servizio di The Machine: questi trasmettono solo un messaggio predefinito, per esempio «Un’attività ha bisogno di te».

Poi l’app chiede alla tua Machine il titolo dell’attività e il prossimo passaggio, per esempio «Rispondi a Sam» con «Scrivi a Sam: martedì alle 10:00 va bene». Il messaggio del mattino include le cose in attesa e l’orario della prima riunione; il briefing del team include i primi elementi; un aggiornamento di Fleet riporta cosa è successo. Se non riesce a raggiungere la tua Machine, resta visibile il messaggio predefinito. Su Android indica quante attività sono in attesa, per esempio «2 attività hanno bisogno di te».

Una notifica include **Posticipa** (fino a domani) e **Segna come fatto**, oltre a **Fallo** per un’attività non ancora iniziata. Puoi usare queste opzioni dopo aver sbloccato il telefono, senza aprire l’app. Per inviare e completare i passaggi finali devi sempre aprire l’app. Ogni attività ha una sola notifica: «Preparazione» diventa «Pronta» e la notifica scompare quando l’attività è completata o posticipata, qui o altrove.

Quando viene completato un passaggio che hai confermato, la notifica mostra **Fatto** e descrive cosa è successo, finché non tocchi **Ho capito** nella sezione Attività. Su iPhone, puoi farlo la prossima volta che apri l’app.

Se disattivi **Testo nelle notifiche** in **Impostazioni**, **Sicurezza**, resta visibile il messaggio predefinito. Lo stesso vale se la schermata di blocco nasconde il contenuto delle notifiche. Quando non può mostrare altro, la notifica dice «Tocca per aprire». Se al suo arrivo il telefono non riesce a raggiungere la tua Machine, mostra i dettagli appena torna online.

Le notifiche seguono le stesse regole delle notifiche push sul web: le preferenze che hai scelto per ogni tipo in [Notifiche](notifications.md), il tuo [orario di lavoro](work-hours.md) e l’assenza di notifiche mentre usi una dashboard.

Ogni telefono con l’app compare in **Impostazioni**, **Notifiche** come **Telefono con l’app**. **Rimuovi** ne disattiva le notifiche. Per riceverle su una Machine autogestita serve The Machine Network; l’app funziona anche senza.

## Condividi con The Machine

In qualsiasi app, tocca Condividi e scegli The Machine. Si apre una **Nuova attività** con il testo, il link o i file che hai condiviso. Controlla i contenuti, aggiungi una data se vuoi e poi aggiungila. Non viene aggiunto nulla finché non lo fai.

Puoi condividere anche solo un file, come una fattura o una lettera. La tua Machine legge il testo di un PDF e compila l’attività: di cosa si tratta, il prossimo passaggio e la data. Il file viene inviato direttamente alla tua Machine e resta lì.

Anche la dashboard installata come app su Android può ricevere contenuti condivisi: selezionala nel menu di condivisione come faresti con qualsiasi altra app.

Nell’app non sono visibili i piani e la fatturazione. In **Impostazioni** trovi comunque **Apri l’account**, per eliminare il tuo account.
