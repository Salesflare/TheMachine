---
title: L’app mobile
area: getting-started
summary: Usa The Machine su iPhone e Android: ricevi notifiche per le tue attività e condividi contenuti con The Machine da qualsiasi app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 927fa395fe97f565
---
L’app mobile apre la tua dashboard personale, con lo stesso accesso che usi sul web. Scaricala dall’[App Store](https://apps.apple.com/app/id6829875215) per iPhone e iPad o da [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) per Android.

L’attività **Sfrutta al meglio The Machine** in cima alla sezione Attività ti suggerisce di scaricarla. Nel browser del telefono, **Scarica** apre lo store. Se il telefono è impostato per mostrare i siti desktop, vengono mostrati i link a entrambi gli store. Su un computer compare un codice QR da scansionare con il telefono e i link a entrambi gli store.

Da qualsiasi telefono, [themachine.computer/app](https://themachine.computer/app) apre lo store giusto. In **Impostazioni**, **App** trovi entrambi gli store in cima, oppure solo quello del telefono se usi un telefono. Su un computer, **Computer** installa la dashboard come app: vedi [Installa l’app](phone-app.md).

## Collegala

Su una Machine ospitata, l’app accede con il tuo account. Su una Machine ospitata autonomamente, apri **Impostazioni**, **App** da un computer: sotto gli store, **Non sei nel Network?** mostra un codice. Installa l’app e poi scansiona il codice con la fotocamera del telefono, oppure inserisci nell’app l’indirizzo mostrato sotto il codice. L’app ti chiede conferma prima di collegarsi. Continua a essere necessario accedere alla tua Machine.

Selezionando **Accedi con** un servizio in **Connessioni** (Shortcut, Notion, Slack, Zoom e gli altri), si apre la schermata di accesso del telefono. Quando hai finito, torni all’app e la nuova connessione compare automaticamente in **Connessioni**.

Quando l’app non riesce a raggiungere la tua Machine, te lo dice e riprova automaticamente. Su Mac, l’app ricarica anche la pagina quando la finestra torna vuota dopo la sospensione, e riappare anche il messaggio che stavi scrivendo in chat. Su Mac o iPad con tastiera, premi Cmd+R per ricaricare la pagina.

## Notifiche

Al primo avvio, l’app ti chiede se vuoi consentire le notifiche. Tocca una notifica per aprire il contenuto: un’attività appare nell’elenco evidenziata, la notifica del mattino apre la giornata in **Calendario**, il riepilogo del team apre Attività e una domanda di Fleet apre la relativa attività. Il testo di un’attività non passa mai da Apple, Google o dal servizio di The Machine: trasmettono solo una frase fissa, come «C’è un’attività che richiede il tuo intervento».

L’app chiede poi alla tua Machine il titolo e il prossimo passaggio dell’attività, ad esempio «Rispondi a Sam» con «Scrivi a Sam: martedì alle 10:00 va bene». La notifica del mattino mostra gli impegni in attesa e l’orario della prima riunione, il riepilogo del team i primi elementi e un aggiornamento di Fleet cosa è successo. Se non riesce a raggiungere la tua Machine, resta la frase fissa. Su Android indica quante attività sono in attesa, ad esempio «2 attività richiedono il tuo intervento».

Una notifica include **Posticipa** (fino a domani) e **Segna come fatto**, oltre a **Fallo** per un’attività non ancora iniziata. Puoi usarli dopo aver sbloccato il telefono, senza aprire l’app. L’invio e i passaggi finali aprono sempre l’app. C’è una notifica per ogni attività: «In preparazione» diventa «Pronta» e scompare quando l’attività viene completata o posticipata, nell’app o altrove.

Quando viene completato un passaggio che hai confermato, la notifica mostra **Fatto** e cosa è successo, finché non tocchi **Ho capito** nella sezione Attività. Su iPhone puoi farlo anche la prossima volta che apri l’app.

Se disattivi **Testo nelle notifiche** in **Impostazioni**, **Sicurezza**, la notifica mostra la frase fissa. Succede lo stesso se la schermata di blocco nasconde il contenuto delle notifiche. Se non può mostrare altro, dice «Tocca per aprire». Se il telefono non riesce a raggiungere la tua Machine quando arriva una notifica, i dettagli vengono mostrati quando torna online.

Le notifiche seguono le stesse regole delle notifiche push sul web: le preferenze che hai scelto per ogni tipo in [Notifiche](notifications.md), il tuo [orario di lavoro](work-hours.md) e l’assenza di notifiche mentre usi una dashboard.

Ogni telefono con l’app compare in **Impostazioni**, **Notifiche** come **Telefono con l’app**. **Rimuovi** ne interrompe le notifiche. Per riceverle su una Machine ospitata autonomamente serve The Machine Network. L’app funziona anche senza.

## Condividi con The Machine

In qualsiasi app, tocca Condividi e scegli The Machine. Si apre una **Nuova attività** con il testo, il link o i file che hai condiviso. Controlla il contenuto, aggiungi una data se vuoi e aggiungi l’attività. Non viene aggiunto nulla finché non lo fai.

Puoi condividere anche solo un file, ad esempio una fattura o una lettera. La tua Machine legge il testo di un PDF e completa l’attività: indica di cosa si tratta, il prossimo passaggio e la data. Il file viene inviato direttamente alla tua Machine e resta lì.

Anche la dashboard installata come app su Android può ricevere contenuti condivisi: selezionala nel menu di condivisione.

Piani e fatturazione non sono disponibili nell’app. In **Impostazioni** resta **Apri l’account**, per eliminare il tuo account.
