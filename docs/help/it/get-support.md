---
title: Ricevi assistenza
area: troubleshooting
summary: Segnala un bug dalla dashboard, scrivici o lascia che il nostro team guardi la tua Machine per un giorno.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
---
## Scrivici

Scrivi a support@themachine.computer. Ti risponde una persona.

Su una Machine in hosting, il piè di pagina della dashboard ha "Qualcosa non va?", che apre il modulo **Segnala un problema** del tuo account.

## Segnala un bug

Apri **Aiuto**, poi **Segnala un bug**. Anche un messaggio di errore ha un pulsante **Segnala un bug**.

1. Spiega cosa è andato storto.
2. Aggiungi uno screenshot se aiuta: **Fai uno screenshot** della dashboard, oppure **Allega un’immagine**.
3. Lascia attivo **Includi un report per il supporto**, a meno che tu non preferisca di no. Aggiunge versioni, controlli ed errori recenti, senza messaggi, chiavi o indirizzi, e permette al nostro team di leggere log e impostazioni della tua Machine per 24 ore. Vedi [Accesso per l’assistenza](get-support.md#support-access). Senza spunta partono solo il tuo testo e il tuo screenshot.
4. Tocca **Invia**. Il modulo si chiude subito. La tua Machine aggiunge da sola il report per il supporto; un controllo lento non blocca mai la tua segnalazione.

Da lì ci pensiamo noi. Una Machine self-hosted può inviarne una quando è nel Network; altrimenti scrivici.

Quando correggiamo un bug che hai segnalato e la tua Machine ha la correzione, te lo diciamo una volta: una breve riga nella tua dashboard (**Ho capito** la chiude) e una breve email. Una Machine self-hosted lo sa quando è nel Network.

Se una segnalazione non può partire subito (sei offline, o ne hai inviate molte in poco tempo), non va persa. La tua Machine la conserva, ti dice quando parte e la invia da sola. Le segnalazioni ancora in attesa compaiono sotto **In attesa di invio**.

## Accesso per l’assistenza

Il nostro team può dare un’occhiata alla tua Machine per te, ma solo dopo che l’hai permesso. Quando segnali un bug con **Includi un report per il supporto** attivo, si attiva quando premi **Invia**. Sul tuo computer, la tua Machine deve essere [associata al tuo account](friends.md).

- Sola lettura: log, impostazioni, versioni, come si sincronizza ogni connessione ed errori recenti, ripuliti come il report per il supporto. Mai i tuoi messaggi, chiavi, password o chi sono i tuoi contatti.
- Termina da solo dopo 24 ore. Finché è attivo, **Impostazioni**, **Sicurezza** lo mostra: **Disattiva** lo termina subito.
- Ogni accesso è elencato in Impostazioni, **Movimenti**, con data e ora. Vedi [Movimenti](activity.md).

## Dal tuo computer

Esegui `assistant support-bundle`. Salva un file con versioni, i controlli di `assistant doctor`, i log recenti e le tue impostazioni, senza chiavi, token, password o indirizzi. Controllalo, poi mandalo a chi ti aiuta.

Per un bug nell’app open source, apri una issue su [GitHub](https://github.com/Salesflare/TheMachine/issues), solo con dati inventati.
