---
title: Graph del team
area: fleet
summary: Sperimentale. Condividi il lavoro con i clienti con la tua Fleet di lavoro, come in un CRM. Scopri cosa viene condiviso, cosa resta privato e come mantenere qualcosa riservato.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
In una Fleet di lavoro, la tua Machine può condividere il lavoro con i clienti con le Machine delle persone del team, come in un CRM condiviso. La funzionalità è **Sperimentale** ed è disattivata all’inizio.

## Attivarla

Un amministratore attiva **Condividi il Graph in questa Fleet** in **Cosa è condiviso** e conferma che l’azienda può condividere questa posta e ha informato le persone interessate. Tutti possono vedere se la condivisione è attiva.

Anche rendere obbligatori l’Email di lavoro o il Calendario di lavoro di tutti attiva la condivisione. Poi ogni persona sceglie cos’altro condividere in **Le tue connessioni**. La prima condivisione di una nuova persona del team aspetta un’ora, così può prima mantenere privato ciò che vuole.

## Le tue connessioni

In **Cosa è condiviso**, **Le tue connessioni** mostra ogni connessione con un interruttore. Le connessioni di lavoro con il dominio della Fleet sono attive all’inizio. Quelle con il dominio di un’altra azienda sono disattivate e riportano «Altra azienda, non condivisa». Le connessioni personali non vengono mai condivise. Se ne disattivi una, i contenuti che aveva condiviso vengono ritirati.

Il calendario di un’altra persona, che leggi accedendo con il tuo account, appare con il suo nome e come personale.

Anche all’interno di una connessione attiva, ogni conversazione viene classificata. Lo Slack della tua azienda include solo le conversazioni con i colleghi. Solo una chat di Slack Connect con un’altra azienda può riguardare il lavoro con i clienti. Le conversazioni personali, solo con i colleghi, sensibili o automatizzate restano escluse, a meno che non ne condividi una tu.

## Richiesto dalla Fleet

In **Richiesto dalla Fleet**, un amministratore può rendere obbligatori per tutti l’**Email di lavoro** e il **Calendario di lavoro** con il dominio della Fleet, dopo aver confermato che l’azienda ha informato le persone interessate. La posta di lavoro appartiene all’azienda, come in qualsiasi CRM. Le connessioni obbligatorie riportano «Richiesto dalla Fleet» e non possono essere disattivate. Le conversazioni che mantieni private restano private.

## Cosa viene condiviso con il team

- Conversazioni con i clienti: email di lavoro con persone esterne all’azienda, inclusi gli allegati.
- Persone, organizzazioni e progetti di lavoro, con una breve cronologia. Nella **Cronologia** di una pagina, **Team** mostra ogni evento una sola volta, nella lingua in cui l’ha scritto la Machine di una persona del team, e indica tutte le persone da cui proviene: «tramite Sam, Kim e Lee».
- Una piccola copia del logo di un’organizzazione e della foto di lavoro di una persona, ottenuta da una ricerca, Slack, LinkedIn, X, Salesflare o Microsoft. Mai immagini dai contatti Google, WhatsApp, Telegram o Facebook, né immagini che hai modificato o rimosso.
- In una bacheca Team, le riunioni di un progetto, le note di Zoom, le conversazioni di Intercom e le chat. Le conversazioni sensibili, come quelle sulle trattative, e quelle solo con i colleghi restano escluse.
- Il numero di elementi e le date del [brief del team](fleet.md#brief-requests) di una persona del team.
- Le risposte a chi chiede chi conosce una persona o vuole informazioni di contesto per una riunione. Vedi [Fleet](fleet.md#answered-by-itself-in-a-work-fleet).
- Gli [apprendimenti del team](fleet.md#team-learnings): come lavora il team, senza nomi né dettagli sui clienti.

## Cosa non viene condiviso automaticamente

- Conversazioni sensibili: acquisto o vendita di un’azienda, investimenti, trattative, risorse umane e selezione del personale, questioni legali, salute, denaro e sicurezza. Non viene condiviso nemmeno il fatto che esistano.
- Email automatiche: ricevute, fatture, avvisi, newsletter e fatture dei fornitori.
- Conversazioni solo con i colleghi, email personali e qualsiasi contenuto proveniente da un account personale. I contenuti personali non vengono mai condivisi, neanche se tocchi Team.
- Tutto ciò che hai contrassegnato con **Mantieni privato**, oltre alle bacheche e ai progetti impostati su Solo tu.
- Le persone che per te sono personali, come la tua famiglia o le tue amicizie, e le loro email. Un progetto a cui partecipano viene comunque condiviso con la sua bacheca, ma senza includerle.

Ogni conversazione viene classificata in base all’argomento, ma la classificazione può essere sbagliata. Controlla cosa verrebbe condiviso e usa Mantieni privato per correggerla. Se condividi una conversazione con il team o con persone specifiche, la condivisione prevale sull’etichetta di contenuto sensibile: controlla chi la riceverà.

## Condividere una bacheca con persone specifiche

Nel menu **⋯** di una bacheca, tocca **Condividi bacheca…** e scegli le persone del team. Solo loro riceveranno i progetti della bacheca con la cronologia completa: email, riunioni e note di Zoom, conversazioni di Intercom, chat, attività e spostamenti. Verranno condivisi anche i contenuti sensibili, come le trattative.

Le conversazioni personali e quelle solo con i colleghi restano escluse, così come la tua famiglia e le tue amicizie, le email automatiche e le connessioni che non hai selezionato.

- Anche un progetto aggiunto in seguito alla bacheca verrà condiviso. Se viene spostato fuori dalla bacheca, la condivisione viene ritirata.
- Se rimuovi una persona o non selezioni nessuno, la condivisione viene ritirata dalla sua Machine.
- Per condividere una singola conversazione con persone specifiche, tocca la sua etichetta e poi **Condividi con…**. Può includere email di lavoro sensibili o automatiche, ma mai conversazioni personali o solo con i colleghi.

## In caso di dubbio, aspetta

Se la tua Machine non è sicura, non condivide. Le conversazioni restano in **Condividere questi?**, raggruppate per tipo, per esempio «Scambi con partner e agenzie immobiliari», ciascuna con un suggerimento:

- **Condividi con il team**: tutte le persone della Fleet.
- **Condividi con…**: solo le persone del team che scegli, per esempio una persona della bacheca per le trattative con gli investitori.
- **Mantieni privato**: il contenuto resta solo tuo.

Puoi decidere per un intero gruppo con un solo tocco. Apri un gruppo per deselezionare le conversazioni che vuoi decidere una alla volta.

Le conversazioni sull’acquisto, la vendita o gli investimenti in un’azienda, così come le questioni del consiglio di amministrazione, sono sensibili e quindi non vengono mostrate qui. Il normale lavoro con un’azienda partner riguarda invece i clienti.

## Prima della prima condivisione

La prima condivisione avviene automaticamente un’ora dopo che la tua Machine te lo comunica. Durante quell’ora, apri **Fleet** e poi **Cosa è condiviso** per vedere, organizzate per azienda, le conversazioni con i clienti che verrebbero condivise. Tocca **Mantieni privato** su quelle che vuoi escludere oppure **Condividi ora** per inviarle subito. Gli amministratori possono vedere chi non ha ancora condiviso.

## Cosa è condiviso

In **Fleet** › **Cosa è condiviso** trovi tutto: il numero di elementi per tipo, ogni conversazione condivisa e il motivo per cui è stata inclusa, quelle in **Condividere questi?** e i contenuti che mantieni privati. Tocca un oggetto per leggerlo. Anche **Impostazioni** e l’etichetta di ogni conversazione rimandano qui.

Una nuova conversazione con un cliente aspetta un’ora prima di essere condivisa, così hai il tempo di cambiare idea.

## Annullare la condivisione

Tocca l’etichetta **Team** di una conversazione, poi **Annulla condivisione**. La Machine di ogni persona del team elimina la conversazione, i suoi allegati e le relative voci nella cronologia, oppure lo fa appena torna online. Qualcuno potrebbe averla già letta.

Se tocchi **Mantieni privato** su una persona, un’organizzazione o un progetto, ne annulli la condivisione per intero.

Se mantieni private due conversazioni con la stessa azienda, la tua Machine ti chiede una volta se vuoi mantenere sempre privata quell’azienda.

## Chi può vederlo

Solo le Machine delle persone del tuo team. I contenuti sono crittografati end-to-end. The Machine Network li trasmette, ma non può leggerli.

## Nuove persone e nuovi dispositivi

Un amministratore autorizza ogni persona una volta sola. La richiesta appare in **Attività** per tutti gli amministratori e vale la prima risposta. Da quel momento, non servono altre approvazioni per condividere.

Nel frattempo, il Graph e la Fleet della nuova persona indicano quali amministratori devono ancora approvare la richiesta. **Miei** e **Team** appaiono pochi secondi dopo l’approvazione, senza dover ricaricare la pagina.

Una nuova Machine di una persona già nel team riceve il Graph del team dopo 24 ore. Nel frattempo, gli amministratori possono toccare **Non suo** per escluderla.

## Quando una persona lascia il team

Da quel momento non riceve più nulla di nuovo. Quello che ha condiviso resta al team. Un amministratore può anche **Escludi** una persona e **Condividi di nuovo** in seguito.

## Disattivare la condivisione per tutti

Un amministratore disattiva **Condividi il Graph in questa Fleet** in **Cosa è condiviso**. Non verranno condivisi nuovi contenuti.

**Disattiva** mantiene ciò che le persone del team hanno già ricevuto. **Disattiva e rimuovi i dati condivisi** fa sì che ogni Machine li elimini. Quando la condivisione viene riattivata, ogni persona deve prima controllare di nuovo i contenuti.

## Smettere di condividere il proprio lavoro

Disattiva le connessioni in **Le tue connessioni**, a meno che la Fleet non le renda obbligatorie. I contenuti che avevano condiviso verranno ritirati.

Vedi anche [Fleet](fleet.md) e [Sicurezza e privacy](security-and-privacy.md).
