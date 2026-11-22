---
title: Gmail
area: connections
summary: Legge le tue email e prepara risposte con il tuo stile. Invia un’email solo dopo la tua approvazione.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: c1f2362cd496840e
---
## Cosa legge

Tutte le tue email: quelle degli ultimi 7 giorni quando colleghi Gmail, poi tutte le nuove, in entrata e in uscita. Conta anche le email che invii, così impara come scrivi e quali promesse hai fatto.

Prima dà un’occhiata alle email di Promozioni, newsletter, Aggiornamenti e Forum: mittente, oggetto e qualche parola, a molte email alla volta. Se una è importante, la legge per intero e può trasformarla in un’attività. Non ne salta nessuna senza averla vista.

## Cosa può inviare

Un’email associata a un’attività, e solo dopo la tua approvazione. **Fallo** prepara una bozza; **Rivedi e invia** la apre, pronta per essere modificata, e non invia nulla finché non premi **Invia ora**. **Accedi con Google** chiede a Google anche l’autorizzazione per inviare. Se usi la tua app sul tuo computer, l’accesso è di sola lettura finché non aggiungi tu la possibilità di inviare.

Nel passaggio di revisione, **Da** è un selettore che compare se Gmail consente a questa casella di inviare email usando un tuo alias, contrassegnato come **Miei** in Impostazioni, [I tuoi indirizzi](settings.md#your-addresses). Se rispondi a un’email arrivata a quell’alias, la risposta parte da lì; le nuove email partono dall’indirizzo della tua casella. Subito prima dell’invio, Gmail viene interrogato di nuovo: se non conferma l’indirizzo, l’email non viene inviata.

La risposta viene aggiunta alla conversazione dell’email a cui risponde. Se parte da una tua casella diversa da quella che ha ricevuto l’email, l’attività te lo segnala prima dell’invio. La risposta finirà comunque nella loro conversazione.

Dopo l’invio di una risposta, la conversazione viene spostata fuori dalla Posta in arrivo sotto l’etichetta Posticipata per alcuni giorni (3, salvo diversa indicazione nell’attività), poi vi ritorna oppure torna prima se qualcuno risponde. Te lo segnala durante la revisione, prima dell’invio.

## Collegalo

Su una Machine ospitata:

1. Apri la pagina di configurazione su app.themachine.computer/setup.
2. In **Posta e calendario**, premi **Collega Google** e accedi. Nella schermata di Google compare Salesflare, l’azienda che crea The Machine.
3. Gmail e Google Calendar si collegano insieme.

Se hai creato l’account con Google e in quella schermata hai autorizzato Gmail e Calendar, si collegano automaticamente. Le email vengono inviate solo quando premi Invia.

Oppure, nella dashboard: **Connessioni**, **Email**, scegli Gmail e premi **Accedi con Google**. Al termine tornerai alla dashboard.

Sul tuo computer, dopo averlo [associato al tuo account](friends.md#a-machine-on-your-own-computer):

1. Nella dashboard, apri **Connessioni**, poi **Email** e scegli Gmail.
2. Premi **Accedi con Google** e accedi nella scheda che si apre. Gmail e Google Calendar si collegano insieme.

Se non hai associato il computer o usi un tuo client OAuth Google, apri **Usa la tua app** lì oppure esegui `assistant connect gmail`. Premi **Apri Google**, accedi e incolla l’indirizzo a cui ti reindirizza Google. Si collega anche Google Calendar per lo stesso indirizzo.

Un amministratore di Google Workspace potrebbe dover autorizzare prima l’app nella Console di amministrazione.

## Rimuovilo

- Su una Machine ospitata: premi **Disconnetti** accanto all’indirizzo nella pagina di configurazione. Gmail e Calendar verranno scollegati per quell’indirizzo e la tua Machine dimenticherà l’accesso. Le altre Machine manterranno il proprio. Nella dashboard, **Disconnetti ↗** in Connessioni ti porta alla pagina. Da lì, **Riconnetti** ti permette di accedere di nuovo senza uscire dalla dashboard.
- Sul tuo computer: apri **Connessioni**, scegli Gmail, poi **Dettagli** e **Disconnetti**. Smetterà di leggere le email. Quelle già importate resteranno. Se nessun altro servizio usa quell’accesso Google, lo dimenticherà. Le altre Machine manterranno il proprio.

## Disinstallalo da Google

Nel tuo Account Google, apri Sicurezza, poi Le tue connessioni ad app e servizi di terze parti, e rimuovi Salesflare (Accedi con Google o Machine ospitata) oppure la tua app.
