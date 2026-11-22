---
title: Gmail
area: connections
summary: Legge le tue email e prepara risposte con il tuo stile. Invia un’email solo dopo la tua approvazione.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Cosa legge

Tutte le tue email: quelle degli ultimi 7 giorni quando ti connetti, poi tutte le nuove, in entrata e in uscita. Conta anche le email che invii, così impara come scrivi e quali promesse hai fatto.

Prima dà un’occhiata veloce alle email di Promozioni, Newsletter, Aggiornamenti e Forum: mittente, oggetto e qualche parola, a molte email alla volta. Quando una è importante, la legge per intero e può trasformarla in un’attività. Nessuna viene ignorata senza prima essere vista.

## Cosa può inviare

Un’email da un’attività, e solo dopo la tua approvazione. **Fallo** prepara una bozza; **Rivedi e invia** la apre, pronta per essere modificata. Non parte nulla finché non premi **Invia ora**. **Accedi con Google** chiede a Google anche l’autorizzazione per inviare. Se usi la tua app sul tuo computer, l’accesso è di sola lettura finché non aggiungi tu l’invio.

In fase di revisione, **Da** è un selettore che compare quando Gmail consente a questa casella di inviare come un tuo alias, contrassegnato con **Miei** in Impostazioni, [I tuoi indirizzi](settings.md#your-addresses). Se rispondi a un’email ricevuta a quell’alias, la risposta parte da lì; le nuove email partono dall’indirizzo della tua casella. Subito prima dell’invio, Gmail verifica di nuovo l’indirizzo: se non lo conferma, l’email non viene inviata.

La risposta viene inserita nella conversazione dell’email a cui risponde. Se viene inviata da una tua casella diversa da quella che ha ricevuto l’email, l’attività te lo segnala prima dell’invio. La risposta finisce comunque nella loro conversazione.

Dopo l’invio di una risposta, la relativa conversazione scompare dalla posta in arrivo e rimane con l’etichetta Posticipati per alcuni giorni (3, salvo diversa indicazione nell’attività), poi ricompare oppure torna prima se qualcuno risponde. La schermata di revisione te lo segnala prima dell’invio. La casella è tua: se una risposta si limita a promettere di svolgere il lavoro, l’attività resta aperta.

## Connetti Gmail

Su una Machine ospitata:

1. Apri la pagina di configurazione all’indirizzo app.themachine.computer/setup.
2. In **Posta e calendario**, premi **Collega Google** e accedi. Nella schermata di Google compare Salesflare, l’azienda che ha creato The Machine.
3. Gmail e Google Calendar si connettono insieme.

Se ti sei registrato con Google e hai autorizzato Gmail e Calendar in quella schermata, si connettono automaticamente. L’invio avviene solo quando premi Invia.

Oppure, nella dashboard, apri **Connessioni**, **Email**, seleziona Gmail e premi **Accedi con Google**. Al termine, torni alla dashboard.

Sul tuo computer, dopo averlo [associato al tuo account](friends.md#a-machine-on-your-own-computer):

1. Nella dashboard, apri **Connessioni**, poi **Email**, e seleziona Gmail.
2. Premi **Accedi con Google** e accedi nella scheda che si apre. Gmail e Google Calendar si connettono insieme.

Se non hai associato la Machine o usi un tuo client OAuth Google, apri **Usa la tua app** oppure esegui `assistant connect gmail`. Premi **Apri Google**, accedi e incolla l’indirizzo a cui Google ti reindirizza. Si connette anche Google Calendar per lo stesso indirizzo.

Un amministratore di Google Workspace potrebbe dover autorizzare prima l’app dalla Console di amministrazione.

## Rimuovi Gmail

- Su una Machine ospitata: nella pagina di configurazione, premi **Disconnetti** accanto all’indirizzo. Gmail e Calendar vengono rimossi per quell’indirizzo e la tua Machine dimentica l’accesso. Le altre tue Machine mantengono il proprio accesso. Nella dashboard, **Disconnetti ↗** in Connessioni ti porta alla pagina di configurazione. Da lì, **Riconnetti** ti permette di accedere di nuovo senza uscire dalla dashboard.
- Sul tuo computer: apri **Connessioni**, seleziona Gmail, poi **Dettagli** e **Disconnetti**. Gmail smette di leggere le email. I dati già importati restano. Se nessun’altra app usa quell’accesso Google, la tua Machine lo dimentica. Le altre tue Machine mantengono il proprio accesso.

## Disinstalla da Google

Nel tuo Account Google, apri Sicurezza, poi Le tue connessioni ad app e servizi di terze parti, e rimuovi Salesflare (Accedi con Google o ospitato) oppure la tua app.
