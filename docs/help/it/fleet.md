---
title: Fleet
area: fleet
summary: Una Fleet di lavoro per il tuo team, una Fleet di famiglia per casa. Machine che si aiutano seguendo le tue regole di condivisione.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 974bbbb54608efc3
---
Una Fleet permette alla tua Machine di collaborare con le Machine del tuo team, della tua famiglia o dei tuoi amici tramite The Machine Network. Quello che si comunicano è crittografato end-to-end e la tua Machine risponde solo in base alle tue regole.

## Tipi di Fleet

- **Fleet di lavoro**: il tuo team. Passa il lavoro, chiedi **chi conosce qualcuno**, ricevi presentazioni e un brief del team.
- **Fleet di famiglia**: fino a 6 persone. Se tutti sono liberi, potete condividere attività e programmi. È gratuita; le Machine ospitate al suo interno hanno un prezzo riservato alle famiglie. Vedi [Famiglia](family.md).
- **Amici**: chiunque usi The Machine, una persona alla volta. È gratis. Vedi [Amici](friends.md).

## La scheda Fleet

La scheda appare quando entri in una Fleet. Mostra un pannello per ogni Fleet, poi Amici, Network, Condivisione e Movimenti. I proprietari e gli amministratori vedono anche **Gestisci**; una Fleet di lavoro che condivide il proprio Graph mostra anche **Cosa è condiviso**.

## Costi, uscita e creazione di una Fleet

Sotto il nome di ogni Fleet, **Quanto costa** mostra i posti, chi paga la tua Machine e, per il proprietario, la carta e le fatture della Fleet. **Lascia questa Fleet** ti fa uscire dalla Fleet; il proprietario deve prima passare il ruolo a qualcun altro. **Crea un’altra Fleet** ne avvia una nuova.

Ogni opzione apre la sezione corrispondente del tuo account. Se il prezzo cambia, prima ti viene mostrato l’importo da confermare. Su una Machine self-hosted, si apre il tuo account in una nuova scheda, dove puoi accedere.

## Fai una domanda alla tua Fleet

Fai una domanda come «chi conosce qualcuno in Acme?» dalla scheda Fleet, oppure seleziona **Chiedi alla Fleet** su un’organizzazione nel [Graph](graph.md). La Machine di ogni compagno di team risponde in base alle proprie regole di condivisione e, se previsto dalla regola, prima chiede a quella persona.

Per tutto il resto, usa **Chiedi qualsiasi cosa** nel pannello della tua Fleet di lavoro. Ogni compagno di team riceve una bozza di risposta basata sui propri account di lavoro, ma non ricevi nulla finché non la invia.

## Risposte automatiche in una Fleet di lavoro

In una Fleet di lavoro Standard, la tua Machine risponde automaticamente a tre tipi di domande dei compagni di team: **chi conosce qualcuno**, **contesto delle riunioni** («chi è questa persona invitata?») e **chi gestisce le email condivise**. Usa solo le informazioni già condivise con il team nel [Graph del team](team-graph.md), mai conversazioni private, personali o sensibili. Ogni risposta compare nella scheda Fleet, sotto **Movimenti**.

Per disattivare una risposta, seleziona **Mai** sotto **Condivisione**. Una regola impostata su **Chiedimi prima** funziona come **Sempre**. Se la condivisione del Graph del team è disattivata, per le domande su chi conosce qualcuno e sul contesto delle riunioni la Machine ti chiede prima.

Le Fleet di lavoro con impostazioni prudenti, Amici e Fleet di famiglia continuano a chiederti prima. Le presentazioni tramite conoscenti, i passaggi di lavoro e le domande libere seguono le rispettive regole.

## Apprendimenti del team

La tua Machine annota come lavora il team, basandosi sulle conversazioni con i clienti già condivise nel Graph del team, al massimo una volta al giorno. Per esempio: «Le richieste di rimborso ricevono risposta dalla casella dell’assistenza usando il modello per i rimborsi». Gli apprendimenti compaiono nel pannello della tua Fleet di lavoro, sotto **Apprendimenti del team**, e sono visibili a tutti nella Fleet. Ognuno viene registrato sotto **Movimenti**. Non viene chiesto prima a nessuno.

- Solo conversazioni a cui ha partecipato qualcuno del tuo team. Mai conversazioni private, personali o sensibili.
- Solo informazioni valide per più clienti: un processo, uno strumento, uno stile di scrittura o chi si occupa di cosa. Mai informazioni su un singolo cliente, feedback sul tuo prodotto o nomi, indirizzi, numeri o citazioni.
- Gli apprendimenti su cui non è sicura vengono scartati.

La tua Machine usa gli apprendimenti pertinenti quando prepara un’attività di lavoro per questa azienda. Le tue informazioni, regole e skill hanno la precedenza; le attività personali non li usano mai. Se un’attività usa un apprendimento, te lo indica, per esempio: «Usato un apprendimento del team: i rimborsi vengono gestiti dalla casella dell’assistenza». Tocca **Rimuovi** per eliminarlo per tutta la Fleet.

Chiunque nella Fleet può rimuovere un apprendimento con **Rimuovi**: viene eliminato per tutti e non viene ricreato. Per impedirlo, disattiva **Proponi di condividere apprendimenti** in Impostazioni, Sicurezza. Le Fleet di lavoro con impostazioni prudenti non ricevono apprendimenti.

## Brief del team

Nella scheda Fleet, sotto **Condivisione**, scegli **Giornaliero** o **Settimanale** per il **Brief del team**. La tua Machine chiede quindi alle Machine dei tuoi compagni di team conteggi e date. Le cose che richiedono il tuo intervento appaiono in Attività, sotto Lavoro: un cliente in attesa di un compagno di team, un’azienda senza attività da almeno due settimane, due persone del team che scrivono agli stessi contatti o una riunione condivisa.

- Un’attività indica chi deve occuparsene, da quando è in attesa, cosa ha chiesto e cosa c’è in gioco, per esempio un progetto in corso. Se non c’è nulla di specifico da segnalare, resta una voce nel brief e non diventa un’attività.
- L’azienda e i compagni di team rimandano alle rispettive pagine. **Dettagli** mostra cosa hanno scritto (toccalo per leggerlo), cosa c’è in gioco, chi del team è in contatto e le conversazioni più recenti. Vengono mostrati solo i contenuti condivisi dal [Graph del team](team-graph.md).
- Se quello che hanno scritto si trova solo nelle email di un compagno di team, l’attività indica a chi chiedere.
- **Chiedi al team** invia loro una domanda precompilata al riguardo. Le risposte compaiono nell’attività.
- **Non serve** chiude l’attività e il brief ne tiene conto. Ricompare solo se ci sono novità.
- Quando qualcuno risponde o se ne occupa, l’attività si chiude automaticamente. Se riguarda un’azienda per cui hai già un’attività, viene aggiunta a quella.

## Richieste di brief

Ogni mattina, un compagno di team che ha attivato il brief del team chiede alla tua Machine conteggi e date. In una Fleet di lavoro, la tua Machine risponde automaticamente usando solo le informazioni già condivise dal [Graph del team](team-graph.md). Non risponde se la condivisione del Graph del team è disattivata. Ogni risposta compare nella scheda Fleet, sotto **Movimenti**, mai come attività o notifica.

Per interrompere la condivisione, disattiva **Condividi i miei fatti del brief con il team** nella scheda Fleet, sotto **Condivisione**. Nel brief di quella persona risulterai senza risposta.

In una Fleet con impostazioni prudenti, le richieste restano in attesa nella scheda Fleet, sotto **Richieste di brief**. Puoi scegliere **Condividi una volta**, **Condividi sempre**, **Rifiuta** o **Mai**. Non viene condiviso nulla finché non scegli e le richieste senza risposta scadono.

## Graph del team

In una Fleet di lavoro, il lavoro con i clienti viene condiviso con il team dopo che l’hai controllato. Vedi [Graph del team](team-graph.md).

## Connessioni condivise

Un proprietario o un amministratore può collegare Stripe o Intercom una sola volta e condividerli con il team da **Connessioni condivise** nella scheda Fleet. I compagni di team possono consultarli, ma non modificarli, e possono vedere chi li ha condivisi. Solo gli amministratori possono modificarli o interromperne la condivisione. Vedi [Stripe](stripe.md) e [Intercom](intercom.md).

## A cosa risponde la tua Machine

Imposta le regole per ogni Fleet nel pannello Condivisione. Vedi [Regole di condivisione](sharing-rules.md). In **Impostazioni** trovi una scorciatoia: **Regole Fleet**.

## Accesso aziendale

Permetti ai compagni di team di unirsi con il proprio account aziendale. In una Fleet di lavoro ospitata, il proprietario o un amministratore che ha effettuato l’accesso con Google Workspace o Microsoft 365 può attivare **Accesso aziendale** nella pagina Account.

I compagni di team che accedono con il dominio aziendale vedono **Chiedi di partecipare**. Un proprietario o un amministratore deve approvare ogni richiesta con **Approva**. Gli account Gmail personali e Outlook.com non vengono mai considerati.

Se rimuovi una persona dalla Fleet, questa viene disconnessa ovunque.

Per entrare in una Fleet, crearne una o associare una Machine sul tuo computer, vedi [Piani e fatturazione](plans-and-billing.md) e [Amici e Network](friends.md).

## Per proprietari e amministratori

**Gestisci** nella scheda Fleet elenca tutte le Fleet che gestisci, con le persone, i ruoli e gli inviti. Su una Machine ospitata puoi invitare persone, cambiare i ruoli, rimuovere persone e rispondere alle richieste di accesso direttamente da qui. Se una modifica influisce sul prezzo, si apre il tuo account per permetterti di confermarla. Su una Machine self-hosted, puoi vedere chi fa parte della Fleet e trovi un link alle relative impostazioni nel tuo account, dove gestire persone e inviti.

**Impostazioni della Fleet**, sotto il nome di ogni Fleet nel relativo pannello e in Gestisci, apre le impostazioni della Fleet nel tuo account: connessioni condivise, sicurezza, accesso aziendale, quale Machine risponde e queste due opzioni:

- **Rimossi di recente**: ogni persona rimossa o che ha lasciato la Fleet. «Rimosso, confermato» significa che la Machine della persona ha eliminato i dati di lavoro e che la persona è disconnessa ovunque. Fino ad allora, compare **In attesa** con il motivo.
- **Movimenti**: chi ha fatto cosa e quando: inviti, ingressi, rimozioni, ruoli, Machine ospitate, fatturazione, connessioni condivise e approvazioni. Include anche ogni volta che il nostro team di assistenza legge il rapporto della Machine di un membro o i relativi log. Non include mai il contenuto dei messaggi. **Scarica CSV** esporta i dati. Vengono conservati per 12 mesi.

**Chiedimi prima di avviare la Machine di un membro**, per il proprietario: se attiva, la Machine di ogni nuovo membro aspetta la tua approvazione, anche in una Fleet gratuita. Se disattivata, in una Fleet gratuita la Machine si avvia subito e ricevi una notifica. Una Machine a pagamento aspetta sempre che tu confermi l’importo.

Dopo aver selezionato **Interrompi condivisione**, una connessione condivisa mostra «Rimosso, confermato» quando tutte le Machine ne hanno perso l’accesso.
