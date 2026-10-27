---
title: Stripe
area: connections
summary: Pagamenti falliti, contestazioni, cancellazioni e nuovi abbonamenti importanti. Legge soltanto.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
---
## Cosa legge

Gli eventi del tuo account Stripe che potrebbero richiedere te: pagamenti falliti, contestazioni, cancellazioni e nuovi abbonamenti importanti, con il cliente a cui appartengono. L'email di un cliente collega l'evento a quella persona e alla sua organizzazione nel [Graph](graph.md).

## Cosa può fare

Niente in Stripe. Non scrive mai, non rimborsa e non ritenta mai un pagamento. L'app Stripe di The Machine chiede a Stripe solo permessi di lettura, e Stripe te li mostra prima che tu la installi.

## Collegalo

Accedi con Stripe, il modo più semplice:

1. Su una Machine ospitata: apri la tua pagina di configurazione su app.themachine.computer/setup, vai su **Altre fonti** e apri Stripe. Sul tuo computer, abbinato al tuo account: **Connessioni**, **+ Aggiungi**, Stripe.
2. Premi **Accedi con Stripe**. Stripe chiede quale account, e mostra cosa può leggere The Machine.
3. Premi **Installa**. Torni alla tua pagina di configurazione, e Stripe è collegato.

Oppure incolla invece una chiave con restrizioni:

1. In Stripe, crea una chiave con restrizioni con Read su Events, Customers e Account, e None su tutto il resto.
2. Trova l'ID del tuo account (acct_...) in Settings, Business details.
3. Apri Stripe come sopra (o esegui `assistant connect stripe`), apri **Oppure incolla una chiave limitata**, incolla l'ID dell'account e la chiave, poi premi **Collegati**.

## Collegalo una volta per il tuo team

In una Fleet di lavoro, un proprietario o un admin collega Stripe una volta e lo condivide con il team:

1. Collega Stripe sulla tua Machine (sopra). Il riquadro **Connettori condivisi** della scheda Fleet ha anche **Collega Stripe**.
2. Nella scheda Fleet, apri **Condividi Stripe**. Sono tutti spuntati; togli la spunta a chi non deve riceverlo. Premi **Condividi**.

Anche le Machine dei colleghi lo leggono, in sola lettura. Sotto Connessioni dice chi l'ha condiviso, e solo gli admin della Fleet possono cambiarlo o fermarlo. La tua Machine rinnova il loro accesso ogni ora, quindi se resta spenta più a lungo, il loro Stripe si ferma finché non torna. Nessuno riceve mai il tuo accesso in sé. Dettagli: [Fleet](fleet.md).

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Stripe, **Dettagli**, poi **Disconnetti**. Ciò che ha già portato dentro resta.
- Su una Machine ospitata puoi anche premere **Rimuovi** accanto a Stripe nella tua pagina di configurazione.
- Condiviso con una Fleet: prima **Interrompi condivisione** nella scheda Fleet.

## Revocalo in Stripe

- Con accesso tramite Stripe: in Stripe, apri Settings, Installed apps, e rimuovi The Machine.
- Chiave con restrizioni: in Stripe, apri Developers, API keys, ed elimina o rigenera la chiave.
