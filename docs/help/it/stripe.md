---
title: Stripe
area: connections
summary: Pagamenti non riusciti, contestazioni, annullamenti e nuovi abbonamenti di importo elevato. Accesso in sola lettura.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 85e6e07cca1a8e8d
---
## Cosa legge

Gli eventi del tuo account Stripe che potrebbero richiedere il tuo intervento: pagamenti non riusciti, contestazioni, annullamenti e nuovi abbonamenti di importo elevato, con il cliente a cui si riferiscono. L’indirizzo email del cliente collega l’evento a quella persona e alla sua organizzazione nel [Graph](graph.md).

Un pagamento non riuscito indica a cosa si riferiva (un primo pagamento, un rinnovo) e quando Stripe riproverà. Non indica perché la carta è stata rifiutata: l’evento di Stripe non include questa informazione. Per scoprirlo, aprilo in Stripe.

## Cosa può fare

Niente su Stripe. Non emette mai rimborsi, non riprova i pagamenti e non modifica nulla. Richiede solo l’accesso in lettura, come mostra Stripe prima dell’installazione.

## Collegala

Accedi con Stripe, è il modo più semplice:

1. Nella dashboard: **Connessioni**, **Clienti**, Stripe. Oppure, nella pagina di configurazione di una Machine ospitata su app.themachine.computer/setup: **Altre fonti**, Stripe. Sul tuo computer, prima devi associarla al tuo account.
2. Premi **Accedi con Stripe**. Stripe ti chiede quale account usare e mostra cosa può leggere The Machine.
3. Premi **Installa**. Tornerai alla pagina da cui hai iniziato e Stripe sarà collegato.

Sul tuo computer, puoi anche incollare una chiave limitata:

1. In Stripe, crea una chiave limitata con accesso in lettura a Events, Customers e Account, e nessun accesso a tutto il resto.
2. Trova l’ID del tuo account (acct_...) in Settings, Business details.
3. Apri Stripe come indicato sopra (o esegui `assistant connect stripe`), apri **Oppure incolla una chiave limitata**, incolla l’ID dell’account e la chiave, poi premi **Collega**.

Sul tuo computer, se Accedi con Stripe non è ancora disponibile, Connessioni te lo segnala e apre subito questo modulo.

## Collegala una volta per il team

In una Fleet di lavoro, una persona proprietaria o amministratrice collega Stripe una volta e lo condivide con il team:

1. Collega Stripe sulla tua Machine (vedi sopra). Anche il riquadro **Connessioni condivise** nella scheda Fleet ha l’opzione **Collega Stripe**.
2. Nella scheda Fleet, apri **Condividi Stripe**. Tutte le persone sono selezionate; deseleziona chi non deve averla. Premi **Condividi**.

Anche le Machine delle altre persone del team potranno leggerlo. Connessioni mostra chi l’ha condiviso. Solo le persone con i diritti di amministrazione della Fleet possono modificarlo o interromperne la condivisione. La tua Machine rinnova il loro accesso ogni ora, quindi quando è spenta l’accesso a Stripe viene sospeso. Nessuno ottiene le tue credenziali di accesso. Scopri di più: [Fleet](fleet.md).

Se una persona del team collega lo stesso account Stripe anche per conto proprio, l’account viene letto una sola volta e la connessione condivisa resta inattiva.

Non è possibile condividere Stripe se è collegato tramite un servizio la cui chiave dà accesso anche ad altre app. In questo caso, collega Stripe direttamente per il team.

## Rimuovila

- Nella dashboard: **Connessioni**, apri Stripe, **Dettagli**, poi **Disconnetti**. I dati già importati restano.
- Su una Machine ospitata, Stripe, a cui hai effettuato l’accesso, mostra **Disconnetti ↗**, che apre la pagina di configurazione: premi **Rimuovi** accanto a Stripe.
- Se è condivisa con una Fleet: prima seleziona **Interrompi condivisione** nella scheda Fleet.

## Revoca l’accesso in Stripe

- Se hai effettuato l’accesso con Stripe: in Stripe, apri Settings, Installed apps e rimuovi The Machine.
- Se usi una chiave limitata: in Stripe, apri Developers, API keys ed elimina o ruota la chiave.
