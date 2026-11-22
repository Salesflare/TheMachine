---
title: Contatta l’assistenza
area: troubleshooting
summary: Segnala un bug dalla dashboard, scrivici o lascia che il nostro team controlli la tua Machine per un giorno.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
translated: 419a75e887b25e20
---
## Scrivici

Scrivi a support@themachine.computer. Ti risponderà una persona.

Se la Machine è ospitata, nel piè di pagina della dashboard trovi «C’è qualcosa che non va?», che apre il modulo **Segnala un problema** del tuo account.

## Segnala un bug

Apri **Aiuto**, poi **Segnala un bug**. Anche un messaggio di errore include il pulsante **Segnala un bug**.

1. Descrivi il problema.
2. Se può essere utile, aggiungi uno screenshot: fai **Fai uno screenshot** della dashboard oppure **Allega un’immagine**.
3. Se puoi, lascia attiva l’opzione **Includi un report per il supporto**. Aggiunge versioni, controlli ed errori recenti, senza messaggi, chiavi o indirizzi, e permette al nostro team di leggere i log e le impostazioni della tua Machine per 24 ore. Scopri di più in [Accesso all’assistenza](get-support.md#support-access). Se non la selezioni, invierai solo quello che hai scritto e lo screenshot.
4. Tocca **Invia**. Il modulo si chiude subito e il report per il supporto viene inviato automaticamente.

Poi ce ne occupiamo noi. Una Machine installata in proprio può inviare il report quando è sulla Network; altrimenti, scrivici.

Puoi anche dire alla tua Machine in chat che c’è un problema. Aprirà **Segnala un bug** per te, con le tue parole e un breve riepilogo già inseriti. Non viene inviato nulla finché non tocchi **Invia**.

Quando correggiamo un bug che hai segnalato e la tua Machine applica la correzione, ti avvisiamo una sola volta: con un breve messaggio sulla dashboard e una breve email. Una Machine installata in proprio riceve la notifica quando è sulla Network.

Il messaggio ti chiede se ora funziona davvero. Tocca **Ora funziona** oppure **Non ancora a posto** per indicarci cosa non va ancora, aggiungendo un’immagine se può essere utile. La risposta ci arriva come una nuova segnalazione, collegata alla prima. **×** chiude il messaggio senza inviare una risposta.

Se la Machine è offline o invii molte segnalazioni di seguito, la tua segnalazione non va persa. La tua Machine la conserva e la invia più tardi, in automatico. Fino ad allora, la trovi in **In attesa di invio**.

## Accesso all’assistenza

Il nostro team può controllare la tua Machine, ma solo se lo autorizzi. Se segnali un bug con **Includi un report per il supporto** attivo, l’accesso si attiva quando premi **Invia**. Se usi il tuo computer, la tua Machine deve essere [associata al tuo account](friends.md).

- Solo lettura: log, impostazioni, versioni, modalità di sincronizzazione di ogni connessione ed errori recenti, ripuliti come nel report per il supporto. Mai i tuoi messaggi, chiavi, password o i nomi dei tuoi contatti.
- L’accesso termina automaticamente dopo 24 ore. Mentre è attivo, lo trovi in **Impostazioni**, **Sicurezza**: tocca **Disattiva** per terminarlo subito.
- Ogni consultazione è elencata in **Impostazioni**, **Movimenti**, con l’orario. Scopri di più in [Movimenti](activity.md).

## Dal tuo computer

Esegui `assistant support-bundle`. Il comando salva un file con le versioni, i controlli di `assistant doctor`, i log recenti e le tue impostazioni, senza chiavi, token, password o indirizzi. Esaminalo, poi invialo a chi ti sta aiutando.

Per segnalare un bug nell’app open source, apri una segnalazione su [GitHub](https://github.com/Salesflare/TheMachine/issues), usando solo dati inventati.
