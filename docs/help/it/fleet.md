---
title: Fleet
area: fleet
summary: Una Fleet di Lavoro per il tuo team, una Fleet di Famiglia per casa. Machine che si aiutano a vicenda, secondo le tue regole di condivisione.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV
order: 1
---
The Machine Network collega le Machine. Ciò che si dicono è cifrato end-to-end, e ogni Machine risponde solo secondo le tue regole.

## Tipi di Fleet

- **Fleet di Lavoro**: il tuo team. Passa il lavoro, chiedi chi conosce qualcuno, ottieni presentazioni e un brief del team.
- **Fleet di Famiglia**: fino a 6 persone. Quando sono tutti liberi, attività e piani condivisi. Gratis. Vedi [Famiglia](family.md).
- **Amici**: chiunque usi The Machine, uno per uno. Gratis. Vedi [Amici](friends.md).

## La scheda Fleet

Compare quando sei in una Fleet, con un pannello per ogni Fleet, Famiglia, Amici, Network, Condivisione e Registro attività.

## Chiedi alla tua Fleet

Chiedi "chi conosce qualcuno in Acme?" dalla scheda Fleet, oppure **Chiedi alla Fleet** su un'organizzazione nel [Graph](graph.md). La Machine di ogni collega risponde secondo le sue regole di condivisione, e prima chiede al collega quando la regola lo prevede.

## Risposte da sola in una Fleet di lavoro

In una Fleet di lavoro Standard, la tua Machine risponde da sola su **chi conosce qualcuno**, **contesto delle riunioni** ("chi è questo ospite?") e **chi gestisce le email condivise**. Usa solo ciò che il [Graph del team](team-graph.md) già condivide con il team. Mai thread privati, personali o sensibili, e solo nomi che il Graph del team già condivide. Ogni risposta compare nella scheda Fleet, sotto **Movimenti**.

Per fermarne una, impostala su **Mai** sotto **Condivisione**. Una regola salvata come **Chiedimi prima** ora funziona come **Sempre**. Finché la condivisione del Graph del team della tua Fleet è disattivata, chi conosce qualcuno e contesto delle riunioni continuano a chiedere prima a te.

Le Fleet di lavoro Prudenti, Amici e Famiglia chiedono ancora prima a te. Presentazioni, passaggi di lavoro, follow-up condivisi e domande libere mantengono le loro regole.

## Apprendimenti del team

Al massimo una volta al giorno, la tua Machine legge alcuni thread con i clienti che il Graph del team già condivide, e annota come lavorate. Per esempio: "Ai rimborsi si risponde dalla casella del supporto con il modello per i rimborsi." Compaiono nel riquadro della Fleet di lavoro sotto **Apprendimenti del team**, per tutta la Fleet, e ognuno è registrato sotto **Movimenti**. Non si chiede prima a nessuno.

- Solo thread in cui ha scritto qualcuno del tuo team. Mai quelli privati, personali o sensibili.
- Solo ciò che vale per più clienti: un processo, uno strumento, uno stile di scrittura, o chi gestisce cosa. Mai qualcosa su un solo cliente, mai feedback sul tuo prodotto, e mai nomi, indirizzi, numeri o citazioni.
- Ognuno ha un'etichetta: di che tipo è, che viene da conversazioni del team, e che è per questa Fleet. Quelli di cui non è sicura vengono scartati.

Chiunque nella Fleet può premere **Rimuovi** su un apprendimento. Sparisce per tutti e non viene creato di nuovo. Per fermarli, disattiva **Proponi di condividere apprendimenti** in Impostazioni, Sicurezza. Le Fleet di lavoro Prudenti non ne ricevono.

## Richieste di brief

Un collega con il brief del team attivo chiede ogni mattina numeri e date alla tua Machine. In una Fleet di lavoro la tua Machine risponde da sola, solo con ciò che il [Graph del team](team-graph.md) già condivide. Mai thread privati o personali, e non parte niente se la condivisione del Graph del team è disattivata. Ogni risposta compare sotto **Movimenti**. Non diventa mai un’attività né una notifica.

Per fermarlo, disattiva **Condividi i miei dati del brief con il team** nella scheda Fleet, sotto **Condivisione**. Il loro brief ti indica allora come senza risposta.

In una Fleet Prudente, le richieste ti aspettano nella scheda Fleet sotto **Richieste di brief**: **Condividi una volta**, **Condividi sempre**, **Rifiuta** o **Mai**. Aspetta solo l’ultima richiesta di ogni collega, e quelle senza risposta scadono. Non viene condiviso nulla finché non scegli.

## Graph del team

In una Fleet di Lavoro, il lavoro con i clienti viene condiviso con il tuo team, dopo che l'hai controllato. Vedi [Graph del team](team-graph.md).

## Connessioni condivise

Un proprietario o un admin può collegare Stripe o Intercom una volta e condividerlo con il team, dal riquadro **Connessioni condivise** della scheda Fleet. Le Machine dei colleghi lo leggono, in sola lettura, e vedono chi l'ha condiviso. Solo gli admin lo cambiano o lo fermano. Vedi [Stripe](stripe.md) e [Intercom](intercom.md).

## Cosa risponde la tua Machine

Impostalo per ogni Fleet, nel pannello Condivisione. Vedi [Regole di condivisione](sharing-rules.md). **Impostazioni** ha una scorciatoia: **Regole Fleet**.

## Accesso aziendale

Per una Fleet di Lavoro ospitata. Un proprietario o un admin che ha fatto l'accesso con un account aziendale Google Workspace o Microsoft 365 può attivare **Accesso aziendale** nella pagina Account. Usa il dominio di quell'account.

I colleghi che accedono con un account di quel dominio vedono allora **Chiedi di entrare**. Un proprietario o un admin deve approvare ogni richiesta con **Approva**. Gli account Gmail personali e Outlook.com non contano mai.

Togliere qualcuno dalla Fleet lo disconnette ovunque.

Per entrare in una Fleet, crearne una o abbinare una Machine sul tuo computer, vedi [Piani e fatturazione](plans-and-billing.md) e [Amici e il Network](friends.md).

## Per proprietari e admin

La parte Fleet della pagina del tuo account mostra altre due cose:

- **Rimossi di recente**: ogni persona rimossa o che è uscita. Dice **Rimosso, confermato** quando la sua Machine ha rimosso i dati di lavoro, Google ha confermato la disconnessione e ogni token condiviso che aveva è stato sostituito. Fino ad allora dice **In sospeso** e perché.
- **Registro attività**: chi ha fatto cosa e quando. Inviti, ingressi, rimozioni, ruoli, Machine ospitate e fatturazione, connettori condivisi e approvazioni. Elenca anche ogni volta che il nostro team ha aperto la Machine di un membro o i suoi log. Mai il contenuto dei messaggi. **Scarica CSV** lo esporta. Conservato 12 mesi.

Dopo **Interrompi condivisione**, un connettore condiviso mostra **Rimosso, confermato** quando ogni Machine ha eliminato il token.
