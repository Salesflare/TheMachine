---
title: Graph del team
area: fleet
summary: Sperimentale. Condividi il lavoro con i clienti con la tua Fleet di lavoro, come un CRM. Cosa viene condiviso, cosa mai, e come tenere qualcosa privato.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
---
In una Fleet di lavoro, la tua Machine può condividere il lavoro con i clienti con le Machine dei tuoi colleghi, come un CRM condiviso. È **Sperimentale**: è nuovo e cambia ancora, quindi parte disattivato.

## Attivalo

Un admin attiva **Condividi il Graph in questo Fleet** in **Cosa è condiviso** e conferma che l'azienda può condividere questa posta e lo ha detto alle sue persone. Tutti vedono se è attivo. Una Fleet che condivideva già prima resta attivo. Poi ogni persona controlla cosa verrebbe condiviso e tocca **Inizia ora**. Prima di allora non parte niente.

## Le tue connessioni

**Le tue connessioni** in **Cosa è condiviso** elenca ognuna con un interruttore. Quelle di lavoro sul dominio della tua Fleet partono attive. Una sul dominio di un'altra azienda parte disattivata, anche se è un account di lavoro: dice "Altra azienda, non condivisa". Puoi attivarla. Quelle personali non vengono mai condivise. Se ne disattivi una, ciò che ha condiviso viene ritirato.

Il calendario di un'altra persona che leggi con il tuo accesso compare con il suo nome, come connessione personale.

Dentro una connessione attiva, ogni conversazione viene comunque classificata. Le conversazioni personali e quelle solo tra colleghi restano fuori. La posta sensibile e quella automatica restano fuori dalla condivisione automatica; le tue scelte esplicite di condivisione possono prevalere su queste classificazioni.

## Richiesto dalla Fleet

Un admin può rendere obbligatorie per tutti l'**Email di lavoro** e il **Calendario di lavoro** sul dominio della Fleet, in **Richiesto dalla Fleet**, dopo aver confermato che l'azienda lo ha detto alle sue persone. La posta di lavoro appartiene all'azienda, come in qualsiasi CRM. Queste connessioni mostrano poi "Richiesto da" la tua Fleet e non si possono disattivare. Le conversazioni che tieni private restano private.

## Cosa va al team

- Conversazioni con i clienti: email di lavoro con persone esterne alla tua azienda, con i loro allegati.
- Persone, organizzazioni e progetti di lavoro, con una breve cronologia.
- Su una bacheca del team, anche le riunioni di un progetto, le note di Zoom, le conversazioni di Intercom e le chat, perché sono sulla bacheca. Quelle sensibili, come le trattative, restano fuori.

## Fuori dalla condivisione automatica

- Conversazioni sensibili: acquisto o vendita di un'azienda, investimenti, valutazioni, trattative, HR, assunzioni e recruiter, questioni legali, salute, denaro, sicurezza. Nemmeno il fatto che esistano.
- Posta automatica: ricevute, fatture, avvisi, newsletter e le fatture della tua azienda con i suoi fornitori.
- Conversazioni interne (solo tra colleghi), posta personale e tutto ciò che arriva da un account personale. Ciò che è personale non viene mai condiviso, nemmeno se tocchi Team.
- Tutto ciò che hai segnato con **Mantieni privato**, e le bacheche e i progetti impostati su Solo tu.

Ogni conversazione viene valutata da sola, in base al suo argomento. La classificazione può sbagliare; controlla cosa verrebbe condiviso e usa Mantieni privato per correggerla. La tua scelta esplicita di Team o una condivisione con colleghi specifici può prevalere su una classificazione sensibile; controlla i destinatari prima di condividere.

## Condividi una bacheca con persone scelte

Nel menu **⋯** di una bacheca, tocca **Condividi bacheca…** e scegli i colleghi. Solo loro ricevono i suoi progetti con la cronologia completa: conversazioni email, riunioni e le loro note di Zoom, conversazioni di Intercom, chat, attività e spostamenti. Vengono condivisi anche quelli sensibili, come le trattative.

Le conversazioni personali e quelle solo tra colleghi restano fuori, e così le persone in Famiglia o Amici e la posta automatica quando è condivisa solo la bacheca. Restano fuori anche le connessioni che non hai selezionato.

- Un progetto aggiunto alla bacheca in seguito viene condiviso anche lui. Uno tolto dalla bacheca viene ritirato.
- Togli qualcuno, o non scegliere nessuno, e la bacheca viene ritirata dalla sua Machine.
- Anche una singola conversazione può andare a persone scelte: tocca la sua etichetta, poi **Condividi con…**. Questa scelta esplicita può includere posta di lavoro sensibile o automatica. Le conversazioni personali e quelle solo tra colleghi non si possono condividere.

## Non è sicura? Aspetta

Quando la tua Machine non è sicura, non condivide. Quelle conversazioni aspettano in **Condividerle?** finché non scegli **Condividi con il team** o **Mantieni privato**.

## Prima della prima condivisione

Apri **Fleet**, poi **Cosa è condiviso**. Elenca le conversazioni con i clienti che verrebbero condivise, per organizzazione. Tocca **Mantieni privato** su quelle che vuoi, poi **Inizia ora**.

Finché non inizi, la tua Machine te lo ricorda ogni pochi giorni, durante il tuo orario di lavoro. Gli admin vedono chi non ha ancora iniziato.

## Cosa è condiviso

**Fleet** › **Cosa è condiviso** mostra tutto in un posto: i conteggi per tipo, ogni conversazione condivisa con il motivo, quelle in attesa in **Condividerle?** e ciò che tieni privato. In **Impostazioni** c'è una scorciatoia, e anche l'etichetta su ogni conversazione ci porta. Tocca l’oggetto di una conversazione per leggerla.

Una nuova conversazione con un cliente aspetta un'ora prima di partire, così hai tempo per cambiare idea.

## Annulla la condivisione

Tocca l'etichetta **Team** su una conversazione, poi **Non condividere più**. La tua Machine lo dice alla Machine di ogni collega, e ognuna elimina la conversazione, i suoi allegati e le sue righe nella cronologia. Una Machine spenta lo fa quando torna attiva. Qualcuno potrebbe averla già letta.

**Mantieni privato** su una persona, un'organizzazione o un progetto annulla la condivisione di tutto allo stesso modo.

Se tieni private due conversazioni con la stessa azienda, la tua Machine ti chiede una volta: tenere sempre private le conversazioni di quell'azienda?

## Chi lo vede

Solo le Machine dei tuoi colleghi. Tutto è crittografato end-to-end, sigillato per la Machine di ogni collega. The Machine Network lo inoltra soltanto e non può leggerlo.

## Ingresso e nuovi dispositivi

Un admin fa entrare ogni persona nella Fleet una volta. Dopo, condividere con lei non richiede altre conferme. La richiesta compare in **Suggerimenti** per ogni admin, e la prima risposta vale per tutto il team. I membri non la ricevono mai.

Una nuova Machine di qualcuno che è già dentro riceve il Graph del team dopo 24 ore. Nel frattempo gli admin la vedono e possono toccare **Non è sua** per tenerla fuori.

## Quando qualcuno se ne va

Da quel momento non riceve più niente di nuovo. Ciò che ha condiviso resta al team. Un admin può anche **Escludere** qualcuno, e **Condividi di nuovo** più tardi.

## Disattivalo per tutti

Un admin può disattivare **Condividi il Graph in questo Fleet** in **Cosa è condiviso**. Tutti vedono se è attivo. Quando è disattivato, non parte niente di nuovo.

**Disattiva** lascia ciò che è già sulle Machine dei colleghi. **Disattiva e rimuovi i dati condivisi** fa eliminare a ogni Machine ciò che ha ricevuto. Quando la condivisione torna attiva, ogni persona la ricontrolla prima.

## Smetti di condividere il tuo lavoro

Disattiva le tue connessioni in **Le tue connessioni**, a meno che il Fleet non le richieda. Ciò che hanno condiviso viene ritirato.

Vedi anche [Fleet](fleet.md) e [Sicurezza e privacy](security-and-privacy.md).
