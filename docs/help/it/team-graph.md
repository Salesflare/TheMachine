---
title: Graph del team
area: fleet
summary: Sperimentale. Condividi il lavoro con i clienti con la tua Fleet di lavoro, come in un CRM. Scopri cosa viene condiviso, cosa resta sempre privato e come mantenere qualcosa riservato.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
In una Fleet di lavoro, la tua Machine può condividere il lavoro con i clienti con le Machines dei tuoi compagni di team, come in un CRM condiviso. È **Sperimentale** ed è disattivata per impostazione predefinita.

## Attivarla

Un admin attiva **Condividi il Graph in questa Fleet** in **Cosa è condiviso** e conferma che l'azienda può condividere queste email e che lo ha comunicato ai suoi dipendenti. Tutti possono vedere se è attiva.

Anche rendere obbligatori l'email o il calendario di lavoro di tutti attiva la condivisione. A quel punto, ognuno sceglie cos'altro condividere in **Le tue connessioni**. La prima condivisione di un nuovo compagno di team attende un'ora, così può decidere prima cosa mantenere privato.

## Le tue connessioni

**Le tue connessioni** in **Cosa è condiviso** elenca ogni connessione con un interruttore. Quelle di lavoro con il dominio della tua Fleet sono attive per impostazione predefinita. Quelle con il dominio di un'altra azienda sono disattivate e indicate come «Altra azienda, non condivisa». Le connessioni personali non vengono mai condivise. Se ne disattivi una, i dati che ha condiviso vengono ritirati.

Il calendario di un'altra persona, che consulti accedendo con il tuo account, compare con il suo nome ed è indicato come personale.

Anche all'interno di una connessione attiva, ogni conversazione viene classificata. Lo Slack della tua azienda conta solo come conversazione tra colleghi; solo una chat Slack Connect con un'altra azienda può essere lavoro con i clienti. Le conversazioni personali, solo tra colleghi, sensibili e automatiche restano escluse, a meno che tu non ne condivida una manualmente.

## Richiesto dalla Fleet

Un admin può rendere obbligatori per tutti **Email di lavoro** e **Calendario di lavoro** con il dominio della Fleet, in **Richiesto dalla Fleet**, dopo aver confermato che l'azienda lo ha comunicato ai suoi dipendenti. Le email di lavoro appartengono all'azienda, come in qualsiasi CRM. Le connessioni obbligatorie sono indicate come «Richiesto dalla Fleet» e non possono essere disattivate. Le conversazioni che mantieni private restano private.

## Cosa viene condiviso con il team

- Conversazioni con i clienti: email di lavoro con persone esterne all'azienda, inclusi gli allegati.
- Persone, organizzazioni e progetti di lavoro, con una breve cronologia. Nella **Cronologia** di una pagina, **Team** mostra ogni evento una sola volta, nella lingua in cui la Machine di un compagno di team l'ha scritto, insieme a tutte le persone coinvolte: «tramite Sam, Kim e Lee».
- Una piccola copia del logo di un'organizzazione e della foto di lavoro di una persona, presa da una ricerca, Slack, LinkedIn, X, Salesflare o Microsoft. Mai una foto dai contatti Google, WhatsApp, Telegram o Facebook, né una foto che hai modificato o rimosso.
- Su una bacheca del Team, le riunioni di un progetto, le note di Zoom, le conversazioni di Intercom e le chat. Quelle sensibili, come le trattative, e le chat solo tra colleghi restano escluse.
- Il numero e le date delle attività per il [brief del team](fleet.md#brief-requests) di un compagno di team.
- Le risposte a chi chiede chi conosce una persona o vuole informazioni sulle riunioni. Vedi [Fleet](fleet.md#answered-by-itself-in-a-work-fleet).
- [Apprendimenti del team](fleet.md#team-learnings): come lavora il team, senza nomi né dettagli dei clienti.

## Cosa non viene condiviso automaticamente

- Conversazioni sensibili: acquisto o vendita di un'azienda, investimenti, trattative, risorse umane e assunzioni, questioni legali, salute, denaro e sicurezza. Non viene condiviso nemmeno il fatto che esistano.
- Email automatiche: ricevute, fatture, avvisi, newsletter e fatture dei fornitori.
- Conversazioni solo tra colleghi, email personali e qualsiasi contenuto proveniente da un account personale. I contenuti personali non vengono mai condivisi, nemmeno quando tocchi Team.
- Qualsiasi elemento che hai contrassegnato con **Mantieni privato**, e le bacheche e i progetti impostati su Only you.
- Una persona che per te è personale, come un familiare o un amico, e le sue email. Un progetto a cui partecipa viene comunque condiviso con la sua bacheca, ma senza includerla.

Ogni conversazione viene classificata in base al contenuto, ma la classificazione può essere sbagliata. Controlla cosa verrebbe condiviso e usa Mantieni privato per correggere eventuali errori. Se condividi una conversazione con il team o con persone specifiche, la condivisione prevale sull'etichetta di contenuto sensibile: controlla quindi chi può vederla.

## Condividere una bacheca con persone specifiche

Nel menu **⋯** di una bacheca, tocca **Condividi bacheca…** e scegli i compagni di team. Solo loro riceveranno i progetti della bacheca con le cronologie complete: email, riunioni e note di Zoom, conversazioni di Intercom, chat, attività e spostamenti. Verranno condivisi anche gli elementi sensibili, come le trattative.

Le conversazioni personali e quelle solo tra colleghi restano escluse, così come i tuoi familiari e amici, le email automatiche e le connessioni che non hai selezionato.

- Anche un progetto aggiunto in seguito alla bacheca verrà condiviso. Se viene spostato fuori dalla bacheca, la condivisione viene ritirata.
- Se rimuovi una persona o non selezioni nessuno, il contenuto viene ritirato dalla sua Machine.
- Per condividere una singola conversazione con persone specifiche, tocca la sua etichetta e poi **Condividi con…**. Può trattarsi di email di lavoro sensibili o automatiche, ma mai di conversazioni personali o solo tra colleghi.

## Se hai dubbi, aspetta

Se la tua Machine non è sicura, non condivide. Le conversazioni in attesa compaiono in **Condividere questi?**, raggruppate per tipo, ad esempio «Scambi con partner e annunci», ognuna con un suggerimento:

- **Condividi con il team**: tutti nella Fleet.
- **Condividi con…**: solo i compagni di team che scegli, ad esempio un membro della bacheca per le trattative con gli investitori.
- **Mantieni privato**: il contenuto resta visibile solo a te.

Basta un tocco per decidere per un intero gruppo. Apri un gruppo per deselezionare le conversazioni che vuoi decidere una alla volta.

Le conversazioni sull'acquisto, la vendita o l'investimento in un'azienda e le questioni del consiglio di amministrazione sono sensibili, quindi non compaiono qui in attesa. Il lavoro quotidiano con un'azienda partner è lavoro con i clienti.

## Prima della prima condivisione

La prima condivisione avviene automaticamente un'ora dopo che la tua Machine te lo comunica. In quell'ora, apri **Fleet** e poi **Cosa è condiviso** per vedere, organizzate per azienda, le conversazioni con i clienti che verrebbero condivise. Tocca **Mantieni privato** su quelle che vuoi escludere oppure **Condividi ora** per inviarle subito. Gli admin possono vedere chi non ha ancora condiviso.

## Cosa è condiviso

**Fleet** › **Cosa è condiviso** mostra tutto: il numero di elementi per tipo, ogni conversazione condivisa e il motivo della condivisione, quelle in **Condividere questi?** e ciò che mantieni privato. Tocca un oggetto per leggere la conversazione. Anche **Impostazioni** e l'etichetta di ogni conversazione rimandano qui.

Una nuova conversazione con un cliente resta in attesa per un'ora prima di essere condivisa, così hai il tempo di cambiare idea.

## Annullare la condivisione

Tocca l'etichetta **Team** su una conversazione e poi **Annulla condivisione**. La Machine di ogni compagno di team elimina la conversazione, i suoi allegati e le relative voci della cronologia. Se è offline, lo farà quando tornerà online. Qualcuno potrebbe averla già letta.

Usa **Mantieni privato** su una persona, un'organizzazione o un progetto per annullarne tutta la condivisione.

Se mantieni private due conversazioni con la stessa azienda, la tua Machine ti chiederà una volta se vuoi mantenere sempre privata quell'azienda.

## Chi può vedere i contenuti

Solo le Machines dei tuoi compagni di team. I contenuti sono crittografati end-to-end. The Machine Network li trasmette, ma non può leggerli.

## Accesso e nuovi dispositivi

Un admin autorizza ogni persona una sola volta. La richiesta compare in **Attività** per tutti gli admin e vale la prima risposta. Dopodiché, non servono altre conferme per condividere.

Fino ad allora, il Graph e la Fleet della nuova persona indicano quali admin devono ancora rispondere. **Miei** e **Team** compaiono pochi secondi dopo l'autorizzazione, senza dover ricaricare la pagina.

Una nuova Machine di una persona già presente riceve il Graph del team dopo 24 ore. Nel frattempo, gli admin possono toccare **Non suo** per escluderla.

## Quando qualcuno se ne va

Da quel momento non riceve più nulla di nuovo. Quello che ha condiviso resta al team. Un admin può anche **Escludi** una persona e **Condividi di nuovo** in seguito.

## Disattivare la condivisione per tutti

Un admin disattiva **Condividi il Graph in questa Fleet** in **Cosa è condiviso**. Non verranno condivisi nuovi contenuti.

**Disattiva** conserva ciò che i compagni di team hanno già ricevuto. **Disattiva e rimuovi i dati condivisi** chiede a ogni Machine di eliminarlo. Quando la condivisione viene riattivata, ognuno deve prima ricontrollare i contenuti.

## Smettere di condividere il proprio lavoro

Disattiva le tue connessioni in **Le tue connessioni**, a meno che non siano obbligatorie per la Fleet. I contenuti che hanno condiviso verranno ritirati.

Vedi anche [Fleet](fleet.md) e [Sicurezza e privacy](security-and-privacy.md).
