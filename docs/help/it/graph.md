---
title: Il Graph
area: graph
summary: Le persone, le organizzazioni e i progetti nei tuoi messaggi, sempre aggiornati automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
La tua Machine crea una mappa delle persone con cui hai rapporti e di quello che succede, partendo dai tuoi messaggi, dalle riunioni e dalle decisioni. Non devi configurare nulla e tutto resta sulla tua Machine.

- [Persone](people.md): tutte le persone con cui sei in contatto, con un riepilogo e una cronologia per ciascuna.
- [Organizzazioni](organizations.md): le aziende in cui lavorano, con le relative persone e i progetti.
- [Progetti](projects.md): quello che succede, su bacheche con fasi, come le trattative in un CRM.

## Aggiornamenti di oggi

Una riga discreta in cima a ogni elenco indica cosa ha aggiornato oggi la tua Machine, per esempio **Aggiornate 4 persone oggi**. Toccala per vedere chi e cosa è cambiato. Toccando un nome si apre la sua pagina con **Modifiche recenti** aperto. Un piccolo punto contrassegna ogni riga e riquadro della bacheca modificati oggi. Conta solo le modifiche fatte dalla tua Machine, a partire da mezzanotte.

## Filtri e ordinamento

**Filtra**, accanto alle schede, restringe l’elenco. Ogni elenco ha i suoi filtri. Persone: grado di vicinanza, ultimo contatto, organizzazione, proprietario, tag e **Ha un progetto aperto**. Organizzazioni: settore, specializzazione, dimensione, paese, ultimo contatto, proprietario, tag e **Ha un progetto aperto**. Progetti: proprietario, bacheca, fase, tag, organizzazione, valore, data di chiusura prevista e **Senza risposta da oltre 10 giorni**.

I filtri selezionati compaiono sopra l’elenco, insieme a **Cancella**. Nei Progetti, elenco e bacheca condividono lo stesso filtro. Sul telefono, i filtri si aprono in un pannello.

Il menu di ordinamento cambia l’ordine dell’elenco. Persone e Organizzazioni si possono ordinare per grado di vicinanza, contatto più recente o meno recente e nome. Le Organizzazioni anche per dimensione. I Progetti si possono ordinare per ultima attività, nome, fase, **Valore** e **Data di chiusura**. **Scarica CSV**, sotto il menu di ordinamento, salva la scheda aperta come foglio di calcolo.

## Campi e tag

Nella sezione Campi di una persona, organizzazione o progetto, fai clic su un valore per modificarlo: **Salva** o Invio lo conferma, **Annulla** o Esc annulla la modifica, **Rimuovi** lo cancella.

**Gestisci campi** (**Aggiungi un campo** se non ce ne sono) aggiunge o rimuove campi da tutti i record di quel tipo. Nuovo campo ne aggiunge uno: testo, numero, data o una scelta da un elenco.

**+ Tag** aggiunge un tag, per esempio VIP o partner. **×** lo rimuove. I tag compaiono negli elenchi e **Filtra** permette di trovarli.

## Compleanno

Il compleanno di una persona compare in Contatti, insieme alla fonte: il suo contatto Google, un compleanno su Google Calendar (la routine Compleanni lo salva per i contatti con cui sei più in confidenza), un’importazione da Facebook, le tue note o tu. **Modifica** permette di inserirlo o correggerlo: mese e giorno, e anche l’anno se lo conosci. In quel caso viene mostrata anche l’età.

Fa fede quello che inserisci tu e resta salvato. **Rimuovi** lo cancella; il contatto o un’importazione non lo aggiungono di nuovo.

Se manca, **Aggiungi compleanno** nella sezione Campi permette di inserirlo. La routine Compleanni legge lo stesso compleanno mostrato nella pagina. Il compleanno è un dato personale: non viene mai condiviso con il team, nemmeno in un record condiviso.

## Importare un foglio di calcolo

**Importa CSV…**, sotto il menu di ordinamento di Persone, Organizzazioni o Progetti, aggiunge un foglio di calcolo salvato in formato CSV.

1. Controlla le colonne. La tua Machine prova a capire a cosa corrisponde ciascuna in base alle intestazioni e al loro contenuto. Puoi modificarle. Quando il tuo modello può essere eseguito, controlla anche le colonne e indica in breve i casi in cui non è sicuro. Vede solo le intestazioni, alcuni valori per colonna e le celle che le regole non sono riuscite a leggere.
2. Controlla le correzioni. **Rivedi** le mostra con il valore originale e quello corretto: spazi in eccesso, nomi scritti in maiuscolo, numeri di telefono in formato internazionale, errori negli indirizzi email (gmial.com), siti web convertiti nel loro dominio, date e valori in qualsiasi formato («€12k» diventa 12000), più tag nella stessa cella, una fase scritta in modo diverso e righe duplicate. Deseleziona un tipo di correzione o una riga per lasciarla invariata.
3. Controlla l’anteprima. Ogni riga è nuova, corrisponde a un record già presente nel tuo Graph oppure viene saltata, con una spiegazione. Una persona corrisponde in base all’email (altrimenti al nome e all’organizzazione), un’organizzazione in base al sito web o al nome, un progetto in base al nome.
4. **Importa** aggiunge i nuovi record e completa quelli corrispondenti. Le celle vuote non modificano nulla.

Puoi usare **Annulla** subito dopo l’importazione oppure **Annulla l’ultima importazione** sotto il menu di ordinamento per annullare l’ultima importazione, finché quei record non sono stati modificati. Se così facendo sovrascriveresti una correzione successiva, ti spiega il motivo. Il file resta sulla tua Machine.

## Proprietario

In una Fleet di lavoro, ogni persona, organizzazione e progetto ha un proprietario: **Proprietario** nella sezione Con te della pagina. Sei tu, a meno che non scelga qualcuno della tua Fleet di lavoro. **Proprietario** nei filtri mostra solo i tuoi record. Ogni modifica compare nella relativa cronologia.

## Team

**Team**, accanto a Miei, mostra quello che i tuoi colleghi condividono, con le stesse schede e lo stesso menu di ordinamento. **Filtra** permette di restringere i risultati in base a chi li ha condivisi, a un’organizzazione (Persone) o allo stato (Progetti). Quello che aggiungi lì è tuo.

Il lavoro con i clienti viene condiviso con le Machine dei tuoi colleghi, insieme al proprietario, ai campi e ai tag. Quello che condividono loro compare nella tua. Ogni conversazione indica **Team** o **Solo tu**. Scopri di più nel [Graph del team](team-graph.md).
