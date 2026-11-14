---
title: Gmail
area: connections
summary: Legge le tue email e prepara bozze di risposta con il tuo stile. Invia un’email solo dopo la tua approvazione.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: e06946aaa6ad0e1a
---
## Cosa legge

Tutte le tue email: quelle degli ultimi 7 giorni quando colleghi Gmail, poi tutte le nuove, in entrata e in uscita. Conta anche la posta che invii, così impara come scrivi e cosa hai promesso.

Prima dà un’occhiata veloce alle email di Promozioni, newsletter, Aggiornamenti e Forum: mittente, oggetto e qualche parola, a molte email per volta. Quando una è importante, la legge per intero e può trasformarla in un’attività. Non ne salta nessuna senza averla vista.

## Cosa può inviare

Un’email da un’attività, e solo dopo la tua approvazione. **Fallo** prepara una bozza; **Rivedi e invia** la apre, pronta da modificare, e non invia nulla finché non premi **Invia ora**. **Accedi con Google** chiede a Google anche il permesso di inviare. Se usi la tua app sul tuo computer, l’accesso consente solo la lettura finché non aggiungi tu la funzione di invio.

**Da** nella schermata di revisione è un piccolo menu di selezione, disponibile quando Gmail consente a questa casella di inviare come un tuo alias, uno contrassegnato come **Miei** in **Impostazioni**, [I tuoi indirizzi](settings.md#your-addresses). Le risposte alle email ricevute a quell’indirizzo partono da lì; le nuove email partono dall’indirizzo della tua casella. Subito prima dell’invio, Gmail verifica di nuovo l’indirizzo: se non lo conferma, non viene inviato nulla.

Una risposta viene inserita nella conversazione dell’email a cui risponde. Se parte da una tua casella diversa da quella che ha ricevuto l’email, l’attività te lo segnala prima dell’invio. La risposta finisce comunque nella loro conversazione.

## Collegala

Su una Machine ospitata:

1. Apri la pagina di configurazione all’indirizzo app.themachine.computer/setup.
2. In **Posta e calendario**, premi **Collega Google** e accedi. Nella schermata di Google compare Salesflare, l’azienda che ha creato The Machine.
3. Gmail e Google Calendar si collegano insieme.

Se ti sei registrato con Google e hai autorizzato Gmail e Calendar in quella schermata, si collegano automaticamente. Le email vengono inviate solo quando premi **Invia**.

In alternativa, dalla dashboard: **Connessioni**, **Email**, scegli Gmail e premi **Accedi con Google**. Al termine, torni alla dashboard.

Sul tuo computer, dopo averlo [associato al tuo account](friends.md#a-machine-on-your-own-computer):

1. Nella dashboard, apri **Connessioni**, poi **Email** e scegli Gmail.
2. Premi **Accedi con Google** e accedi nella scheda che si apre. Gmail e Google Calendar si collegano insieme.

Se non hai associato la Machine, oppure usi il tuo client OAuth di Google: apri **Usa la tua app** da lì, oppure esegui `assistant connect gmail`. Premi **Apri Google**, accedi e incolla l’indirizzo della pagina a cui ti reindirizza Google. Si collega anche Google Calendar associato allo stesso indirizzo.

Un amministratore di Google Workspace potrebbe dover prima autorizzare l’app dalla Console di amministrazione.

## Rimuovila

- Su una Machine ospitata: premi **Disconnetti** accanto all’indirizzo nella pagina di configurazione. Così rimuovi Gmail e Calendar per quell’indirizzo e la tua Machine dimentica l’accesso. Le altre tue Machine mantengono il proprio accesso. Nella dashboard, **Disconnetti ↗** in Connessioni ti porta a quella pagina. Da lì, **Riconnetti** ti fa accedere di nuovo senza uscire dalla dashboard.
- Sul tuo computer: apri **Connessioni**, seleziona Gmail, poi **Dettagli** e **Disconnetti**. Gmail smette di leggere le email. Quelle già importate restano. Quando nessun’altra cosa su quella Machine usa quell’accesso Google, la Machine lo dimentica. Le altre tue Machine mantengono il proprio accesso.

## Disinstallala da Google

Nel tuo Account Google, apri Sicurezza, poi Le tue connessioni ad app e servizi di terze parti, e rimuovi Salesflare (Accedi con Google o versione ospitata) oppure la tua app.
