---
title: L’app per dispositivi mobili
area: getting-started
summary: Usa The Machine come app su iPhone e Android: ricevi notifiche per le tue attività e condividi contenuti con The Machine da qualsiasi app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: aaf34f864dadf180
---
L’app per dispositivi mobili apre la tua dashboard personale, con lo stesso accesso che usi sul web. Scaricala dall’[App Store](https://apps.apple.com/app/id6829875215) per iPhone e iPad o da [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) per Android.

L’attività **Sfrutta al meglio The Machine**, in cima alla sezione Attività, te la consiglia. Nel browser del telefono, **Scarica** apre lo store. Se il telefono è configurato per mostrare i siti desktop, vedrai i link a entrambi gli store. Sul computer, invece, vedrai un codice QR da scansionare con il telefono e i link a entrambi gli store.

Da qualsiasi telefono, [themachine.computer/app](https://themachine.computer/app) apre lo store giusto. In **Impostazioni**, **App** trovi entrambi gli store in cima alla pagina, oppure solo quello del tuo telefono se usi un telefono. Sul computer trovi anche l’app desktop per Windows, Mac e Linux: consulta [L’app desktop](desktop-app.md).

## Collegala

Su una Machine ospitata, l’app accede con il tuo account. Su una Machine self-hosted, apri **Impostazioni**, **App** da un computer: sotto gli store, **Non sei nel Network?** mostra un codice. Installa l’app, poi scansiona il codice con la fotocamera del telefono oppure inserisci nell’app l’indirizzo che trovi sotto il codice. L’app ti chiede conferma prima di connettersi e resta attivo l’accesso della tua Machine.

Toccando **Accedi con** un servizio in **Connessioni** (Shortcut, Notion, Slack, Zoom e altri), si apre la schermata di accesso del telefono. Una volta effettuato l’accesso, torni all’app e la nuova connessione compare automaticamente in **Connessioni**.

Se l’app non riesce a raggiungere la tua Machine, te lo comunica e riprova automaticamente. Su Mac, se la finestra dell’app torna vuota dopo la sospensione, l’app ricarica automaticamente la pagina. Anche il messaggio che stavi scrivendo in una chat ricompare. Su Mac o iPad con tastiera, premi Cmd+R per ricaricare la pagina.

## Notifiche

Al primo avvio, l’app ti chiede se vuoi consentire le notifiche. Toccane una per aprire ciò a cui si riferisce: un’attività appare nell’elenco, evidenziata; il briefing del mattino apre la giornata di oggi in **Calendario**; il riepilogo del team apre Attività; una domanda di Fleet apre l’attività corrispondente. Il testo delle attività non passa da Apple, Google o dal servizio di The Machine: questi trasmettono solo una frase fissa, come «Un’attività ha bisogno di te».

Poi l’app chiede alla tua Machine il titolo e il prossimo passaggio dell’attività, per esempio «Rispondi a Sam» con «Invia a Sam: martedì alle 10:00 va bene». Il briefing del mattino indica cosa ti aspetta e l’orario della prima riunione; il riepilogo del team mostra i primi elementi; un aggiornamento di Fleet indica cosa è successo. Se non riesce a raggiungere la tua Machine, resta visibile la frase fissa. Su Android indica quante attività ti aspettano, per esempio «2 attività hanno bisogno di te».

Una notifica offre **Posticipa** (fino a domani) e **Segna come fatto**, oltre a **Fallo** per un’attività non ancora iniziata. Puoi usarle dopo aver sbloccato il telefono, senza aprire l’app. L’invio e i passaggi finali aprono sempre l’app. C’è una notifica per ogni attività: «In preparazione» diventa «Pronta» e la notifica scompare quando l’attività viene completata o posticipata, dall’app o da qualsiasi altro luogo.

Quando viene completato un passaggio che hai confermato, la notifica mostra **Fatto** e indica cosa è successo, finché non tocchi **Ho capito** in Attività. Su iPhone puoi farlo anche la prossima volta che apri l’app.

Se disattivi **Testo nelle notifiche** in **Impostazioni**, **Sicurezza**, resta visibile la frase fissa. Lo stesso vale se la schermata di blocco nasconde il contenuto delle notifiche. Se non può mostrare altro, la notifica dice «Tocca per aprire». Se quando arriva una notifica il telefono non riesce a raggiungere la tua Machine, i dettagli appariranno quando tornerà online.

Seguono le stesse regole delle notifiche push sul web: le preferenze che hai scelto per ogni tipo in [Notifiche](notifications.md), il tuo [orario di lavoro](work-hours.md) e l’assenza di notifiche mentre usi una dashboard.

Ogni telefono con l’app compare in **Impostazioni**, **Notifiche** come **Telefono con l’app**. **Rimuovi** ne interrompe le notifiche. Per riceverle su una Machine self-hosted serve The Machine Network; l’app funziona anche senza.

## Condividi con The Machine

In qualsiasi app, tocca Condividi e scegli The Machine. Si apre una **Nuova attività** con il testo, il link o i file che hai condiviso. Controllala, aggiungi una data se vuoi e poi aggiungila. Non viene aggiunto nulla finché non lo fai.

Puoi condividere anche solo un file, per esempio una fattura o una lettera. La tua Machine legge il testo di un PDF e compila l’attività: indica di cosa si tratta, il prossimo passaggio e la data. Il file viene inviato direttamente alla tua Machine e resta lì.

Anche la dashboard installata come app su Android può ricevere contenuti condivisi: selezionala nella schermata di condivisione come faresti con qualsiasi altra app.

Piani e fatturazione non sono disponibili nell’app. In **Impostazioni** trovi comunque **Apri l’account** per eliminare il tuo account.
