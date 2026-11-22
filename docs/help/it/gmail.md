---
title: Gmail
area: connections
summary: Legge la tua posta e prepara risposte con il tuo stile. Invia un’email solo dopo la tua approvazione.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Cosa legge

Tutta la tua posta: gli ultimi 7 giorni al momento della connessione, poi tutti i nuovi messaggi, in entrata e in uscita. Conta anche la posta che invii, così impara come scrivi e quali promesse hai fatto.

I messaggi di Promozioni, newsletter, Aggiornamenti e Forum vengono esaminati rapidamente: mittente, oggetto e qualche parola, molti alla volta. Se uno è importante, viene letto per intero e può diventare un’attività. Nessun messaggio viene ignorato senza essere visto.

## Cosa può inviare

Un’email da un’attività, e solo dopo la tua approvazione. **Fallo** prepara una bozza; **Rivedi e invia** la apre, pronta per essere modificata, e non parte nulla finché non premi **Invia ora**. **Accedi con Google** chiede a Google anche l’autorizzazione per inviare. Se usi la tua app sul tuo computer, l’accesso è di sola lettura finché non aggiungi tu la possibilità di inviare.

Nella schermata di revisione, **Da** è un selettore che compare se Gmail permette a questa casella di inviare usando un tuo alias, contrassegnato come **Miei** nelle **Impostazioni**, [I tuoi indirizzi](settings.md#your-addresses). Una risposta a un’email ricevuta su quell’alias partirà da lì; una nuova email partirà dall’indirizzo della tua casella. Subito prima dell’invio, Gmail verifica di nuovo l’indirizzo: se non lo conferma, l’email non viene inviata.

Una risposta viene aggiunta alla conversazione dell’email a cui risponde. Se viene inviata da una tua casella diversa da quella che ha ricevuto l’email, l’attività te lo segnala prima dell’invio. La risposta verrà comunque aggiunta alla conversazione originale.

Dopo l’invio di una risposta, la conversazione scompare dalla posta in arrivo e viene contrassegnata come posticipata per alcuni giorni (3, salvo diversa indicazione nell’attività), poi ricompare oppure torna prima se qualcuno risponde. La schermata di revisione te lo segnala prima dell’invio. La casella è tua: se la risposta si limita a promettere di svolgere il lavoro, l’attività resta aperta.

## Collegalo

Su una Machine ospitata:

1. Apri la pagina di configurazione su app.themachine.computer/setup.
2. In **Posta e calendario**, premi **Collega Google** e accedi. Nella schermata di Google compare il nome Salesflare, l’azienda che ha creato The Machine.
3. Gmail e Google Calendar si collegano insieme.

Se ti sei registrato con Google e hai autorizzato Gmail e Calendar in quella schermata, si collegano automaticamente. L’invio avviene solo quando premi Invia.

Oppure, nella dashboard: **Connessioni**, **Email**, seleziona Gmail e premi **Accedi con Google**. Al termine, tornerai alla dashboard.

Sul tuo computer, dopo averlo [associato al tuo account](friends.md#a-machine-on-your-own-computer):

1. Nella dashboard, apri **Connessioni**, poi **Email** e seleziona Gmail.
2. Premi **Accedi con Google** e accedi nella scheda che si apre. Gmail e Google Calendar si collegano insieme.

Se il computer non è associato o usi un tuo client OAuth di Google, apri **Usa la tua app** lì oppure esegui `assistant connect gmail`. Premi **Apri Google**, accedi, poi incolla l’indirizzo a cui ti reindirizza Google. Si collegherà anche Google Calendar per lo stesso indirizzo.

Un amministratore di Google Workspace potrebbe dover autorizzare prima l’app nella Console di amministrazione.

## Rimuovilo

- Su una Machine ospitata: premi **Disconnetti** accanto all’indirizzo nella pagina di configurazione. Questo scollega Gmail e Calendar per quell’indirizzo e la tua Machine dimentica l’accesso. Le altre tue Machine mantengono il proprio accesso. Nella dashboard, **Disconnetti ↗** in **Connessioni** ti porta a quella pagina. Da lì, **Riconnetti** ti permette di accedere di nuovo senza uscire dalla dashboard.
- Sul tuo computer: apri **Connessioni**, seleziona Gmail, poi **Dettagli** e **Disconnetti**. La lettura si interrompe, ma i dati già importati restano. Se nessun altro elemento usa quell’accesso Google, la Machine lo dimentica. Le altre tue Machine mantengono il proprio accesso.

## Rimuovilo da Google

Nel tuo Account Google, apri Sicurezza, poi Le tue connessioni ad app e servizi di terze parti e rimuovi Salesflare (Accedi con Google o versione ospitata) oppure la tua app.
