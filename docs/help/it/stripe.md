---
title: Stripe
area: connections
summary: Pagamenti non riusciti, contestazioni, cancellazioni e nuovi abbonamenti importanti. Accesso in sola lettura.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 6e7ca235dc502297
---
## Cosa legge

Gli eventi del tuo account Stripe che potrebbero richiedere il tuo intervento: pagamenti non riusciti, contestazioni, cancellazioni e nuovi abbonamenti importanti, insieme al cliente a cui si riferiscono. L’indirizzo email del cliente collega l’evento alla persona e alla sua organizzazione nel [Graph](graph.md).

## Cosa può fare

Non può fare nulla su Stripe. Non emette mai rimborsi, non riprova i pagamenti e non modifica nulla. Richiede solo l’accesso in lettura, come mostra Stripe prima dell’installazione.

## Collegalo

Accedi con Stripe, è il modo più semplice:

1. Nella dashboard: **Connessioni**, **Clienti**, Stripe. Oppure, nella pagina di configurazione di una Machine ospitata su app.themachine.computer/setup: **Altre fonti**, Stripe. Sul tuo computer, prima devi associarla al tuo account.
2. Premi **Accedi con Stripe**. Stripe ti chiede quale account usare e mostra cosa può leggere The Machine.
3. Premi **Installa**. Torni alla pagina di partenza e Stripe è collegato.

Sul tuo computer, puoi anche incollare una chiave limitata:

1. In Stripe, crea una chiave limitata con accesso in lettura a Events, Customers e Account e nessun accesso a tutto il resto.
2. Trova l’ID del tuo account (acct_...) in Impostazioni, Dettagli aziendali.
3. Apri Stripe come descritto sopra (oppure esegui `assistant connect stripe`), apri **Oppure incolla una chiave limitata**, incolla l’ID dell’account e la chiave, poi premi **Collega**.

Sul tuo computer, se l’opzione Accedi con Stripe non è ancora disponibile, Connessioni te lo segnala e apre direttamente questo modulo.

## Collegalo una volta per il tuo team

In una Fleet di lavoro, il proprietario o un amministratore collega Stripe una volta e lo condivide con il team:

1. Collega Stripe alla tua Machine (vedi sopra). Anche il riquadro **Connessioni condivise** nella scheda Fleet include l’opzione **Collega Stripe**.
2. Nella scheda Fleet, apri **Condividi Stripe**. Tutti sono selezionati; deseleziona chi non deve avervi accesso. Premi **Condividi**.

Anche le Machine dei tuoi colleghi potranno leggerlo. In Connessioni puoi vedere chi l’ha condiviso; solo gli amministratori della Fleet possono modificarlo o interrompere la condivisione. La tua Machine rinnova l’accesso ogni ora, quindi quando è spenta l’accesso a Stripe dei colleghi viene sospeso. Nessuno riceve le tue credenziali di accesso. Per i dettagli, consulta [Fleet](fleet.md).

Se un collega collega anche direttamente lo stesso account Stripe, viene usato solo il suo collegamento e quello condiviso resta inattivo.

Non è possibile condividere un collegamento a Stripe creato tramite un servizio la cui chiave permette di accedere anche ad altre app. Collega Stripe direttamente per il team.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Stripe, **Dettagli**, poi **Disconnetti**. I dati già importati restano.
- Su una Machine ospitata, per Stripe a cui hai effettuato l’accesso vedrai **Disconnetti ↗**, che apre la pagina di configurazione: premi **Rimuovi** accanto a Stripe.
- Se è condiviso con una Fleet, prima seleziona **Interrompi condivisione** nella scheda Fleet.

## Revoca l’accesso da Stripe

- Se hai effettuato l’accesso con Stripe: in Stripe, apri Impostazioni, App installate e rimuovi The Machine.
- Se hai usato una chiave limitata: in Stripe, apri Developers, API keys ed elimina o ruota la chiave.
