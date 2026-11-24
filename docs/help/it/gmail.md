---
title: Gmail
area: connections
summary: Legge le tue email e prepara bozze di risposta con il tuo stile. Invia un’email solo dopo la tua approvazione.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: f0565a7bf839f49f
---
## Cosa legge

Tutte le tue email: quelle degli ultimi 7 giorni quando colleghi Gmail, poi tutte le nuove, in entrata e in uscita. Conta anche la posta che invii, così impara come scrivi e cosa hai promesso.

Prima dà un’occhiata veloce alle email di Promozioni, Newsletter, Aggiornamenti e Forum: mittente, oggetto e poche parole, anche a molte email per volta. Se una è importante, la legge per intero e può trasformarla in un’attività. Nessuna email viene saltata senza essere esaminata.

## Cosa può inviare

Un’email da un’attività, e solo dopo la tua approvazione. **Fallo** prepara una bozza; **Rivedi e invia** la apre, pronta per essere modificata, e non viene inviata finché non premi **Invia ora**. **Accedi con Google** chiede a Google anche l’autorizzazione per inviare. Se usi la tua app sul tuo computer, l’accesso è di sola lettura finché non abiliti tu l’invio.

Durante la revisione, **Da** è un menu che compare solo se Gmail consente a questa casella di inviare come un tuo alias, cioè un indirizzo contrassegnato come **Miei** in **Impostazioni**, [I tuoi indirizzi](settings.md#your-addresses). Le risposte alle email ricevute tramite quell’alias partono da lì; le nuove email partono dall’indirizzo della tua casella. Subito prima dell’invio, Gmail verifica di nuovo l’indirizzo. Se non lo conferma, l’email non viene inviata.

La risposta viene inserita nella conversazione dell’email a cui risponde. Se parte da una tua casella diversa da quella che ha ricevuto l’email, l’attività te lo segnala prima dell’invio. La risposta arriva comunque nella conversazione originale.

Dopo l’invio di una risposta, la sua conversazione esce dalla Posta in arrivo e viene contrassegnata come Posticipata per alcuni giorni (3, a meno che l’attività non indichi diversamente). Poi torna nella Posta in arrivo, oppure prima se qualcuno risponde. Non resta mai fuori oltre la scadenza dell’attività: torna il giorno lavorativo precedente. Se la scadenza è oggi, resta nella Posta in arrivo. La schermata di revisione te lo segnala prima dell’invio. La casella è tua: se la risposta si limita a promettere di svolgere il lavoro, l’attività resta aperta.

## Collegala

Su una Machine ospitata:

1. Apri la pagina di configurazione su app.themachine.computer/setup.
2. In **Posta e calendario**, premi **Collega Google** e accedi. Nella schermata di Google, il nome indicato è Salesflare, che realizza The Machine.
3. Gmail e Google Calendar si collegano insieme.

Se ti sei registrato con Google e hai autorizzato Gmail e Calendar in quella schermata, si collegano automaticamente. L’invio avviene solo quando premi il pulsante per inviare.

Oppure, nella dashboard: **Connessioni**, **Email**, scegli Gmail e premi **Accedi con Google**. Al termine, torni alla dashboard.

Sul tuo computer, dopo averlo [associato al tuo account](friends.md#a-machine-on-your-own-computer):

1. Nella dashboard, apri **Connessioni**, poi **Email** e scegli Gmail.
2. Premi **Accedi con Google** e accedi nella scheda che si apre. Gmail e Google Calendar si collegano insieme.

Se non è associato, o se usi il tuo client OAuth di Google: apri **Usa la tua app** lì oppure esegui `assistant connect gmail`. Premi **Apri Google**, accedi e incolla l’indirizzo a cui ti reindirizza Google. Si collega anche Google Calendar associato allo stesso indirizzo.

Un amministratore di Google Workspace potrebbe dover prima autorizzare l’app dalla Console di amministrazione.

## Rimuovila

- Su una Machine ospitata: premi **Disconnetti** accanto all’indirizzo nella pagina di configurazione. Gmail e Calendar vengono rimossi per quell’indirizzo e la tua Machine dimentica l’accesso. Le altre tue Machine mantengono il proprio. Nella dashboard, **Disconnetti ↗** in Connessioni ti porta a quella pagina. **Riconnetti** ti permette di accedere di nuovo senza lasciare la dashboard.
- Sul tuo computer: apri **Connessioni**, scegli Gmail, poi **Dettagli** e **Disconnetti**. Smetterà di leggere la posta, ma manterrà ciò che ha già importato. La tua Machine dimentica l’accesso Google quando nessun’altra funzione lo usa. Le altre tue Machine mantengono il proprio.

## Rimuovila da Google

Nel tuo Account Google, apri Sicurezza, poi Le tue connessioni ad app e servizi di terze parti e rimuovi Salesflare (Accedi con Google o Machine ospitata) oppure la tua app.
