---
title: Graph del team
area: fleet
summary: Sperimentale. Condividi il lavoro con i clienti con la tua Fleet di lavoro, come in un CRM. Scopri cosa viene condiviso, cosa resta sempre privato e come mantenere qualcosa riservato.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: 9788be6d2d5e3fa6
---
In una Fleet di lavoro, la tua Machine può condividere il lavoro con i clienti con le Machine dei tuoi colleghi, come in un CRM condiviso. È **Sperimentale** ed è disattivata all’inizio.

## Attivarla

Un amministratore attiva **Condividi il Graph in questa Fleet** in **Cosa è condiviso** e conferma che l’azienda può condividere queste email e ha informato il personale. Tutti possono vedere se la condivisione è attiva.

Se si rende obbligatorio l’uso dell’email o del calendario di lavoro di tutti, la condivisione si attiva. Poi ognuno sceglie cos’altro condividere in **Le tue connessioni**. La prima condivisione di un nuovo collega resta in sospeso per un’ora, così può prima mantenere privato ciò che preferisce.

## Le tue connessioni

In **Cosa è condiviso**, **Le tue connessioni** mostra ogni connessione con un interruttore. Le connessioni di lavoro con il dominio della Fleet sono attive all’inizio. Quelle con il dominio di un’altra azienda sono disattivate e indicate come «Altra azienda, non condivisa». Le connessioni personali non vengono mai condivise. Se ne disattivi una, i dati che aveva condiviso vengono rimossi.

Il calendario di un’altra persona, che leggi accedendo con il tuo account, appare con il suo nome e come personale.

Anche all’interno di una connessione attiva, ogni conversazione viene classificata separatamente. Lo Slack della tua azienda include solo le conversazioni con i colleghi. Solo una chat Slack Connect con un’altra azienda può essere considerata lavoro con i clienti. Le conversazioni personali, solo con colleghi, sensibili e automatiche restano escluse, a meno che non ne condivida una tu.

## Richiesto dalla Fleet

Un amministratore può rendere obbligatorie per tutti **Email di lavoro** e **Calendario di lavoro** con il dominio della Fleet, in **Richiesto dalla Fleet**, dopo aver confermato che l’azienda ha informato il personale. Le email di lavoro appartengono all’azienda, come in qualsiasi CRM. Le connessioni obbligatorie indicano «Richiesto dalla Fleet» e non si possono disattivare. Le conversazioni che mantieni private restano private.

## Cosa viene condiviso con il team

- Conversazioni con i clienti: email di lavoro con persone esterne all’azienda, inclusi gli allegati.
- Persone, organizzazioni e progetti di lavoro, con una breve cronologia. Nella **Cronologia** di una pagina, **Team** mostra ogni evento una sola volta, nella lingua in cui la Machine di un collega l’ha scritto, con tutte le persone da cui proviene: «tramite Sam, Kim e Lee».
- Una piccola copia del logo di un’organizzazione e della foto di lavoro di una persona, ricavata da una ricerca, Slack, LinkedIn, X, Salesflare o Microsoft. Mai immagini dai contatti Google, da WhatsApp, Telegram o Facebook, né immagini che hai modificato o rimosso.
- In una bacheca Team, riunioni e note Zoom di un progetto, conversazioni Intercom e chat. Le conversazioni sensibili, come quelle sulle trattative, e quelle solo con colleghi restano escluse.
- Conteggi e date del [brief del team](fleet.md#brief-requests) di un collega.
- Risposte alle domande di un collega su chi conosce una persona o sul contesto di una riunione. Vedi [Fleet](fleet.md#answered-by-itself-in-a-work-fleet).
- [Apprendimenti del team](fleet.md#team-learnings): come lavora il team, senza nomi né dettagli dei clienti.

## Cosa resta escluso dalla condivisione automatica

- Conversazioni sensibili: acquisto o vendita di un’azienda, investimenti, trattative, risorse umane e selezione del personale, questioni legali, salute, denaro e sicurezza. Non viene condiviso nemmeno il fatto che esistano.
- Email automatiche: ricevute, fatture, avvisi, newsletter e fatture dei fornitori.
- Conversazioni solo con colleghi, email personali e qualsiasi contenuto proveniente da un account personale. I contenuti personali non vengono mai condivisi, nemmeno quando tocchi Team.
- Tutto ciò che hai contrassegnato con **Mantieni privato**, oltre alle bacheche e ai progetti impostati su Solo tu.
- Una persona che per te è personale, come un familiare o un amico, e le sue email. Un progetto a cui partecipa viene comunque condiviso insieme alla sua bacheca, ma senza includere quella persona.

Ogni conversazione viene valutata in base all’argomento, ma la valutazione può essere sbagliata. Controlla cosa verrà condiviso e usa Mantieni privato per correggere eventuali errori. Se condividi una conversazione con il team o con persone specifiche, la scelta prevale sull’etichetta di contenuto sensibile. Controlla quindi con chi la condividi.

## Condividere una bacheca con alcune persone

Nel menu **⋯** di una bacheca, tocca **Condividi bacheca…** e scegli i colleghi. Solo loro riceveranno i progetti con la cronologia completa: email, riunioni e note Zoom, conversazioni Intercom, chat, attività e spostamenti. Verranno condivisi anche i contenuti sensibili, come le trattative.

Le conversazioni personali e quelle solo con colleghi restano escluse, così come quelle con familiari e amici, le email automatiche e le connessioni che non hai selezionato.

- Anche i progetti aggiunti in seguito alla bacheca verranno condivisi. Se un progetto viene spostato fuori dalla bacheca, la condivisione viene annullata.
- Se rimuovi una persona, o non selezioni nessuno, i contenuti vengono rimossi dalla sua Machine.
- Per condividere una singola conversazione con alcune persone, tocca la sua etichetta e poi **Condividi con…**. Puoi includere email di lavoro sensibili o automatiche, ma mai conversazioni personali o solo con colleghi.

## Se hai dubbi, aspetta

Se la tua Machine non è sicura, non condivide. Le conversazioni restano in sospeso in **Condividere questi?**, suddivise per categoria, ad esempio «Scambi con partner e annunci», e ciascuna ha un suggerimento:

- **Condividi con il team**: tutte le persone della Fleet.
- **Condividi con…**: solo i colleghi che scegli, ad esempio un membro della bacheca per le trattative con gli investitori.
- **Mantieni privato**: resta solo a te.

Basta un tocco per decidere cosa fare di un intero gruppo. Apri un gruppo per deselezionare le conversazioni che vuoi decidere singolarmente.

Le conversazioni su acquisto, vendita o investimenti in un’azienda e le questioni relative ai consigli di amministrazione sono sensibili, quindi non vengono messe in sospeso qui. Il normale lavoro con un’azienda partner è lavoro con i clienti.

## Prima della prima condivisione

La prima condivisione viene inviata automaticamente un’ora dopo che la tua Machine ti avvisa. Durante quell’ora, apri **Fleet** e poi **Cosa è condiviso** per vedere, suddivise per organizzazione, le conversazioni con i clienti che verrebbero condivise. Tocca **Mantieni privato** su quelle che vuoi escludere oppure **Condividi ora** per inviarle subito. Gli amministratori possono vedere chi non ha ancora condiviso.

## Cosa è condiviso

In **Fleet** › **Cosa è condiviso** trovi tutto: i conteggi per categoria, ogni conversazione condivisa e il motivo della condivisione, quelle in **Condividere questi?** e ciò che mantieni privato. Tocca un oggetto per leggere la conversazione. Anche **Impostazioni** e l’etichetta di ogni conversazione rimandano qui.

Una nuova conversazione con un cliente resta in sospeso per un’ora prima di essere condivisa, così hai il tempo di cambiare idea. Trascorsa quell’ora, viene condivisa entro mezz’ora. L’annullamento della condivisione e **Mantieni privato** vengono applicati al team entro 5 minuti.

## Annullare la condivisione

Tocca l’etichetta **Team** su una conversazione, poi **Annulla condivisione**. La Machine di ogni collega elimina la conversazione, gli allegati e le relative righe della cronologia, oppure lo fa appena torna online. Qualcuno potrebbe averla già letta.

Se tocchi **Mantieni privato** su una persona, un’organizzazione o un progetto, ne annulli la condivisione completa.

Se mantieni private due conversazioni con la stessa azienda, la tua Machine ti chiede una volta se vuoi mantenere sempre privata quell’azienda.

## Chi può vedere i contenuti

Solo le Machine dei tuoi colleghi. I contenuti sono cifrati end-to-end. The Machine Network li inoltra, ma non può leggerli.

## Ingresso e nuovi dispositivi

Un amministratore autorizza ogni persona una volta sola. La richiesta appare in **Attività** a tutti gli amministratori e vale la prima risposta. Dopo di che, non servono altre autorizzazioni per condividere.

Nel frattempo, il Graph e la Fleet della nuova persona indicano quali amministratori devono ancora autorizzarla. **Miei** e **Team** appaiono pochi secondi dopo l’autorizzazione, senza ricaricare la pagina.

La nuova Machine di una persona già nella Fleet riceve il Graph del team dopo 24 ore. Nel frattempo, gli amministratori possono toccare **Non suo** per escluderla.

## Quando una persona lascia il team

Da quel momento non riceve più nulla di nuovo. I contenuti che ha condiviso restano al team. Un amministratore può anche **Escludi** una persona e **Condividi di nuovo** in seguito.

## Disattivare la condivisione per tutti

Un amministratore disattiva **Condividi il Graph in questa Fleet** in **Cosa è condiviso**. Non verrà condiviso più nulla di nuovo.

**Disattiva** mantiene ciò che i colleghi hanno già ricevuto. **Disattiva e rimuovi i dati condivisi** fa sì che ogni Machine li elimini. Quando la condivisione viene riattivata, ogni persona ricontrolla i contenuti prima di condividerli.

## Smettere di condividere il tuo lavoro

Disattiva le connessioni in **Le tue connessioni**, a meno che la Fleet non le renda obbligatorie. I contenuti condivisi tramite quelle connessioni vengono rimossi.

Vedi anche [Fleet](fleet.md) e [Sicurezza e privacy](security-and-privacy.md).
