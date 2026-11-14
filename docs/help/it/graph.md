---
title: Graph
area: graph
summary: Le persone, le organizzazioni e i progetti nei tuoi messaggi, sempre aggiornati automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
La tua Machine crea una mappa delle persone con cui hai rapporti e di quello che succede, usando i tuoi messaggi, le riunioni e le decisioni. Non devi configurare nulla e tutto resta sulla tua Machine.

- [Persone](people.md): tutte le persone con cui sei in contatto, con un riepilogo e una cronologia per ciascuna.
- [Organizzazioni](organizations.md): le aziende in cui lavorano, con le relative persone e i progetti.
- [Progetti](projects.md): quello che succede, organizzato in bacheche con fasi, come le trattative in un CRM.

## Aggiornato oggi

Una riga discreta in cima a ogni elenco mostra gli aggiornamenti di oggi della tua Machine, per esempio **Aggiornate 4 persone oggi**. Toccala per vedere chi e cosa è cambiato. Tocca un nome per aprire la sua pagina con **Modifiche recenti** già aperto. Un puntino indica ogni riga e riquadro della bacheca modificato oggi. Vengono conteggiate solo le modifiche apportate dalla tua Machine, a partire dalla mezzanotte.

## Filtrare e ordinare

**Filtra**, accanto alle schede, restringe l’elenco. Ogni elenco ha i suoi filtri. Persone: vicinanza, ultimo contatto, organizzazione, proprietario, tag e **Ha un progetto aperto**. Organizzazioni: settore, specialità, dimensione, paese, ultimo contatto, proprietario, tag e **Ha un progetto aperto**. Progetti: proprietario, bacheca, fase, tag, organizzazione, valore, data di chiusura prevista e **Senza risposta da oltre 10 giorni**.

I filtri selezionati appaiono sopra l’elenco, insieme a **Cancella**. In Progetti, elenco e bacheca condividono lo stesso filtro. Sul telefono, i filtri si aprono in un pannello.

Il menu di ordinamento permette di riordinare l’elenco. Persone e Organizzazioni si possono ordinare per vicinanza, contatto più recente o meno recente e nome. Le Organizzazioni si possono ordinare anche per dimensione. I Progetti si possono ordinare per ultima attività, nome, fase, **Valore** e **Data di chiusura**. **Scarica CSV**, sotto il menu di ordinamento, salva la scheda aperta come foglio di calcolo.

## Campi e tag

Nella sezione Campi di una persona, organizzazione o progetto, fai clic su un valore per modificarlo: **Salva** o Invio conferma, **Annulla** o Esc annulla, **Rimuovi** lo cancella.

**Gestisci campi** (oppure **Aggiungi un campo** se non ce ne sono) aggiunge o rimuove campi per tutti i record di quel tipo. **Nuovo campo** ne aggiunge uno: testo, numero, data o una scelta da un elenco.

**+ Tag** aggiunge un tag, per esempio VIP o partner; **×** lo rimuove. I tag appaiono negli elenchi e puoi trovarli con **Filtra**.

## Compleanno

Il compleanno di una persona appare in Contatti, insieme alla fonte: il suo contatto Google, un compleanno su Google Calendar (la routine Compleanni lo salva per i contatti stretti), un’importazione da Facebook, le tue note o tu. **Modifica** permette di inserirlo o correggerlo: mese e giorno, e anche l’anno se lo conosci. In quel caso, viene mostrata anche l’età.

Fa fede la data inserita da te, che rimane salvata indipendentemente dalla fonte. **Rimuovi** la cancella. Non verrà ripristinata da un contatto o da un’importazione.

Se non è ancora stato inserito, **Aggiungi compleanno** lo aggiunge sotto Campi. La routine Compleanni legge la stessa data mostrata nella pagina. Il compleanno è un dato personale: non viene mai condiviso con il tuo team, nemmeno nei record condivisi.

## Importare un foglio di calcolo

**Importa CSV…**, sotto il menu di ordinamento di Persone, Organizzazioni o Progetti, aggiunge un foglio di calcolo salvato in formato CSV.

1. Controlla le colonne. La tua Machine prova a capire a cosa corrisponde ciascuna colonna, basandosi sulle intestazioni e sul contenuto. Puoi modificarle. Quando il tuo modello è disponibile, controlla anche le colonne e indica brevemente i casi in cui non è sicuro. Può vedere solo le intestazioni, alcuni valori per colonna e le celle che non è riuscito a leggere con le regole.
2. Controlla le correzioni. **Rivedi** le mostra una per una, con il valore originale e quello corretto: spazi in eccesso, nomi in maiuscolo, numeri di telefono in formato internazionale, errori negli indirizzi email (gmial.com), siti web convertiti nel loro dominio, date e valori in qualsiasi formato ("€12k" corrisponde a 12000), più tag nella stessa cella, una fase scritta in modo diverso e righe duplicate. Deseleziona un tipo di correzione o una riga per lasciarla com’è.
3. Controlla l’anteprima. Ogni riga è nuova, corrisponde a una già presente nel tuo Graph oppure viene ignorata. Per ogni riga trovi il motivo. Una persona viene abbinata tramite l’email oppure, se manca, tramite nome e organizzazione. Un’organizzazione viene abbinata tramite il sito web o il nome. Un progetto viene abbinato tramite il nome.
4. **Importa** aggiunge i nuovi record e aggiorna quelli corrispondenti. Le celle vuote non modificano nulla.

Puoi usare **Annulla** subito dopo l’importazione oppure **Annulla l’ultima importazione** nel menu di ordinamento, purché i record non siano stati modificati nel frattempo. Se l’annullamento sovrascrivesse una correzione successiva, la tua Machine ti spiega perché non è possibile. Il file resta sulla tua Machine.

## Proprietario

In una Fleet di lavoro, ogni persona, organizzazione e progetto ha un proprietario: **Proprietario**, nella sezione Con te della relativa pagina. Sei tu, a meno che tu non scelga qualcuno della tua Fleet di lavoro. **Proprietario** in Filtra mostra solo i record che ti appartengono. Ogni modifica appare nella cronologia.

## Team

**Team**, accanto a I miei, mostra i contenuti condivisi dai tuoi colleghi, con le stesse schede e lo stesso menu di ordinamento. **Filtra** restringe i risultati in base a chi li ha condivisi, a un’organizzazione (Persone) o allo stato (Progetti). Quello che aggiungi qui è tuo.

Il lavoro con i clienti viene condiviso con le Machine dei tuoi colleghi, insieme al proprietario, ai campi e ai tag. I contenuti condivisi dai colleghi appaiono anche nella tua Machine. Ogni conversazione indica **Team** o **Solo tu**. Scopri di più in [Graph del team](team-graph.md).
