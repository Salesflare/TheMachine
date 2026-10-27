---
title: Stripe
area: connections
summary: Pagamenti falliti, contestazioni, cancellazioni e nuovi abbonamenti importanti. Legge soltanto.
covers: connector:stripe
code: connectors/stripe.py
site: Connect, More sources, Remove
---
## Cosa legge

Gli eventi del tuo account Stripe che potrebbero richiedere te: pagamenti falliti, contestazioni, cancellazioni e nuovi abbonamenti importanti, con il cliente a cui appartengono.

## Cosa può fare

Niente in Stripe. Non scrive mai, non rimborsa e non ritenta mai un pagamento.

## Collegalo

1. In Stripe, crea una chiave con restrizioni con Read su Events, Customers e Account, e None su tutto il resto.
2. Trova l'ID del tuo account (acct_...) in Settings, Business details.
3. Su una Machine ospitata: apri la tua pagina di configurazione su app.themachine.computer/setup, vai su **Altre fonti** e apri Stripe. Sul tuo computer: **Connessioni**, **+ Aggiungi**, Stripe, oppure `assistant connect stripe`.
4. Incolla l'ID dell'account e la chiave, poi premi **Collegati**.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Stripe, **Dettagli**, poi **Disconnetti**. Ciò che ha già portato dentro resta.
- Su una Machine ospitata puoi anche premere **Rimuovi** accanto a Stripe nella tua pagina di configurazione.

## Revocalo in Stripe

In Stripe, apri Developers, API keys, ed elimina o rigenera la chiave con restrizioni.
