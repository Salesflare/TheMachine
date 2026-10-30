---
title: Gmail
area: connections
summary: Legge la tua posta e scrive bozze di risposta con il tuo stile. Invia un'email solo dopo la tua approvazione.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
---
## Cosa legge

Tutta la tua posta: gli ultimi 7 giorni quando la colleghi, poi tutto ciò che è nuovo, in entrata e in uscita. Conta anche la posta che invii, così impara come scrivi e cosa hai promesso.

La posta di Promozioni, newsletter, Aggiornamenti e Forum riceve prima un'occhiata veloce: mittente, oggetto e qualche parola, molte alla volta. Quando una conta, viene letta per intero e può diventare un'attività. Niente viene saltato senza essere visto.

## Cosa può inviare

Un'email da un'attività, e solo dopo la tua approvazione. **Fallo** prepara una bozza; **Rivedi e invia** la apre pronta da modificare, e non parte niente finché non premi **Invia ora**. **Accedi con Google** chiede a Google anche il permesso di inviare. Con la tua app sul tuo computer, l'accesso è di sola lettura finché non aggiungi tu l'invio.

Una risposta finisce nella conversazione dell’email a cui risponde. Se parte da una casella diversa da quella in cui è arrivata l’email, l’attività lo dice prima dell’invio: per loro finisce comunque nella stessa conversazione.

## Collegalo

Su una Machine in hosting:

1. Apri la tua pagina di configurazione su app.themachine.computer/setup.
2. In **Email e calendario**, premi **Collega Google** e accedi. La schermata di Google indica Salesflare, che produce The Machine.
3. Gmail e Google Calendar si collegano insieme.

Oppure nella dashboard: **Connessioni**, **+ Aggiungi**, scegli Gmail e premi **Accedi con Google**. Quando hai finito, torni alla dashboard.

Sul tuo computer, una volta [associato al tuo account](fleet.md):

1. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli Gmail.
2. Premi **Accedi con Google** e accedi nella scheda che si apre. Gmail e Google Calendar si collegano insieme.

Se non è associato, o con il tuo client OAuth di Google: apri lì **Usa la tua app**, oppure esegui `assistant connect gmail`. Usa gog. Apri l'indirizzo che mostra e accedi.

Un admin di Google Workspace potrebbe dover prima consentire l'app, nella Console di amministrazione.

## Rimuovilo

- Su una Machine in hosting: premi **Disconnetti** accanto all'indirizzo nella tua pagina di configurazione. Così rimuovi Gmail e Calendar per quell'indirizzo e revochi l'accesso su Google. Nella dashboard, **Disconnetti ↗** in Connessioni ti porta lì. **Riconnetti** lì ti fa accedere di nuovo senza lasciare la dashboard.
- Sul tuo computer: **Connessioni**, apri Gmail, **Dettagli**, poi **Disconnetti**. Smette di leggere. Ciò che ha già importato resta. Quando nient'altro usa quell'accesso Google, viene revocato su Google.

## Disinstallalo su Google

Nel tuo Account Google, apri Sicurezza, poi Le tue connessioni ad app e servizi di terze parti, e rimuovi Salesflare (Accedi con Google, o in hosting) oppure la tua app.
