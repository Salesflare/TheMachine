---
title: Il Graph
area: graph
summary: Le persone, le organizzazioni e i progetti nei tuoi messaggi, sempre aggiornati automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 4dbe1a4e1702b1c1
---
La tua Machine crea una mappa delle persone con cui hai a che fare e di quello che succede, a partire dai tuoi messaggi, dalle riunioni e dalle decisioni. Non devi configurare nulla e tutto resta sulla tua Machine.

- [Persone](people.md): tutte le persone con cui sei in contatto, con un riepilogo e una cronologia per ciascuna.
- [Organizzazioni](organizations.md): le aziende in cui lavorano, con le relative persone e i progetti.
- [Progetti](projects.md): quello che succede, organizzato in bacheche con fasi, come le trattative in un CRM.

## Aggiornamenti di oggi

Una riga discreta in cima a ogni elenco indica cosa ha aggiornato oggi la tua Machine, ad esempio **Aggiornati 4 contatti oggi**. Toccala per vedere chi e cosa è cambiato. Tocca un nome per aprire la relativa pagina con **Modifiche recenti** già aperto. Un piccolo punto contrassegna ogni riga e riquadro della bacheca modificati oggi. Vengono conteggiate solo le modifiche apportate dalla tua Machine, a partire dalla mezzanotte.

## Filtri e ordinamento

**Filtra**, accanto alle schede, restringe l’elenco. Ogni elenco ha i suoi filtri. Persone: grado di vicinanza, ultimo contatto, organizzazione, proprietario, tag e **Ha un progetto aperto**. Organizzazioni: settore, specializzazione, dimensioni, paese, ultimo contatto, proprietario, tag e **Ha un progetto aperto**. Progetti: proprietario, bacheca, fase, tag, organizzazione, valore, data di chiusura prevista e **Senza risposta da oltre 10 giorni**.

I filtri selezionati compaiono sopra l’elenco, insieme a **Cancella**. In Progetti, elenco e bacheca condividono lo stesso filtro. Sul telefono, i filtri si aprono in un pannello.

Il menu di ordinamento permette di ordinare l’elenco. Persone e Organizzazioni si possono ordinare per grado di vicinanza, contatto più recente o meno recente e nome. Organizzazioni anche per dimensioni. Progetti anche per **Valore** e **Data di chiusura**. **Scarica CSV**, sotto il menu di ordinamento, salva la scheda aperta come foglio di calcolo.

## Campi e tag

Nella sezione Campi di una persona, organizzazione o progetto, fai clic su un valore per modificarlo: **Salva** o Invio conferma la modifica, **Annulla** o Esc la annulla, **Rimuovi** svuota il campo.

**Gestisci campi** aggiunge o rimuove campi da tutti i record di quel tipo. **Nuovo campo** ne aggiunge uno: testo, numero, data o una scelta da un elenco.

**+ Tag** aggiunge un tag, ad esempio VIP o partner; **×** lo rimuove. I tag compaiono negli elenchi e puoi trovarli con **Filtra**.

## Compleanno

Il compleanno di una persona compare in Contatto, insieme all’origine: il suo contatto Google, un compleanno su Google Calendar (la routine Compleanni lo salva per i contatti con cui hai più confidenza), un’importazione da Facebook oppure tu. **Modifica** permette di inserirlo o correggerlo: mese e giorno, e anche l’anno se lo conosci (in tal caso compare anche l’età). Il dato inserito da te prevale su tutte le altre fonti e rimane salvato. **Rimuovi** lo elimina; il contatto o un’importazione non lo aggiungeranno di nuovo.

Se non c’è, **Aggiungi compleanno** nella sezione Campi permette di inserirlo. La routine Compleanni legge lo stesso compleanno mostrato nella pagina. Il compleanno è un dato personale: non viene mai condiviso con il tuo team, nemmeno in un record condiviso.

## Importa un foglio di calcolo

**Importa CSV…**, sotto il menu di ordinamento in Persone, Organizzazioni o Progetti, aggiunge un foglio di calcolo salvato in formato CSV.

1. Controlla le colonne. La tua Machine prova a capire a cosa corrisponde ciascuna, in base alle intestazioni e ai contenuti; puoi modificarle. Quando il tuo modello può essere eseguito, controlla anche le colonne e indica brevemente i casi in cui non è sicuro. Vede solo le intestazioni, alcuni valori per colonna e le celle che non è riuscita a leggere seguendo le regole.
2. Controlla le correzioni. **Rivedi** le mostra con il prima e il dopo: spazi in eccesso, nomi in maiuscolo, numeri di telefono nel formato internazionale, errori di battitura negli indirizzi email (gmial.com), siti web convertiti nel relativo dominio, date e valori in qualsiasi formato ("€12k" corrisponde a 12000), più tag nella stessa cella, una fase scritta in modo diverso e la stessa riga duplicata. Deseleziona un tipo di correzione o una riga per lasciarla invariata.
3. Controlla l’anteprima. Ogni riga è nuova, corrisponde a un record già presente nel tuo Graph oppure viene ignorata, con una spiegazione. Una persona corrisponde in base all’indirizzo email (altrimenti al nome e all’organizzazione), un’organizzazione in base al sito web o al nome, un progetto in base al nome.
4. **Importa** aggiunge i nuovi record e completa quelli corrispondenti. Le celle vuote non modificano nulla.

**Annulla** subito dopo l’importazione, oppure **Annulla l’ultima importazione** dal menu di ordinamento, annulla l’ultima importazione se quei record non sono stati modificati nel frattempo. Se l’annullamento sovrascriverebbe una correzione successiva, la tua Machine spiega il motivo. Il file rimane sulla tua Machine.

## Proprietario

In una Fleet di lavoro, ogni persona, organizzazione e progetto ha un proprietario: **Proprietario** sotto Con te nella relativa pagina. Sei tu, a meno che tu non scelga qualcuno della tua Fleet di lavoro. **Proprietario** in Filtra mostra solo i record di cui sei proprietario. Ogni modifica compare nella cronologia.

## Team

**Team**, accanto a Miei, mostra ciò che i tuoi colleghi condividono, con le stesse schede e lo stesso menu di ordinamento. **Filtra** restringe l’elenco in base a chi ha condiviso il record, a un’organizzazione (Persone) o allo stato (Progetti). Quello che aggiungi qui è tuo.

Il lavoro con i clienti viene condiviso con le Machine dei tuoi colleghi, insieme al proprietario, ai campi e ai tag; quello che condividono loro compare nella tua. Ogni conversazione indica **Team** o **Solo tu**. Scopri di più in [Graph del team](team-graph.md).
