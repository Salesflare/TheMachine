---
title: Il Graph
area: graph
summary: Le persone, le organizzazioni e i progetti nei tuoi messaggi, sempre aggiornati automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 9052c679e45207f7
---
La tua Machine crea una mappa delle persone con cui hai a che fare e di quello che succede, a partire dai tuoi messaggi, dalle riunioni e dalle decisioni. Non devi configurare nulla e la mappa resta sulla tua Machine.

- [Persone](people.md): tutte le persone con cui sei in contatto, con un riepilogo e una cronologia per ciascuna.
- [Organizzazioni](organizations.md): le aziende per cui lavorano, con le relative persone e i progetti.
- [Progetti](projects.md): quello che succede, organizzato in bacheche con fasi, come le trattative in un CRM.

## Aggiornamenti di oggi

Una riga discreta in cima a ogni elenco indica cosa ha aggiornato oggi la tua Machine, per esempio **Oggi sono state aggiornate 4 persone**. Toccala per vedere chi e cosa è cambiato. Toccando un nome si apre la sua pagina con **Modifiche recenti** aperte. Un puntino indica ogni riga e riquadro della bacheca modificati oggi. Vengono conteggiate solo le modifiche apportate dalla tua Machine, a partire da mezzanotte.

## Filtri e ordinamento

**Filtra**, accanto alle schede, restringe l’elenco. Ogni elenco ha i suoi filtri. Persone: vicinanza, ultimo contatto, organizzazione, proprietario, tag e **Ha un progetto aperto**. Organizzazioni: settore, specializzazione, dimensioni, paese, ultimo contatto, proprietario, tag e **Ha un progetto aperto**. Progetti: proprietario, bacheca, fase, tag, organizzazione, valore, data di chiusura prevista e **Senza risposta da oltre 10 giorni**.

I filtri selezionati compaiono sopra l’elenco, con **Cancella**. Nei Progetti, elenco e bacheca condividono lo stesso filtro. Sul telefono, i filtri si aprono in un pannello.

Il menu di ordinamento consente di ordinare l’elenco. Persone e Organizzazioni si possono ordinare per vicinanza, contatto più recente o meno recente e nome. Le Organizzazioni anche per dimensioni. Progetti si possono ordinare per ultima attività, nome, fase, **Valore** e **Data di chiusura**. **Scarica CSV**, sotto il menu di ordinamento, salva la scheda aperta in formato foglio di calcolo.

## Campi e tag

Nella sezione Campi di una persona, organizzazione o progetto, fai clic su un valore per modificarlo: **Salva** o Invio lo conferma, **Annulla** o Esc lo annulla, **Rimuovi** lo svuota.

**Gestisci campi** (**Aggiungi un campo** quando non ce ne sono) aggiunge o rimuove campi per tutti i record di quel tipo. **Nuovo campo** ne aggiunge uno: testo, numero, data o una scelta da un elenco.

**+ Tag** aggiunge un tag, per esempio VIP o partner. **×** lo rimuove. I tag compaiono negli elenchi (sul telefono, quelli di una persona sono visibili nella sua pagina) e **Filtra** permette di trovarli.

## Compleanno

Il compleanno di una persona compare in Contatti, insieme alla fonte: il suo contatto Google, un compleanno su Google Calendar (la routine Compleanni lo salva per le persone con cui sei più in confidenza), un’importazione da Facebook, le tue note o tu. **Modifica** permette di impostarlo o correggerlo: mese e giorno, e anche l’anno se lo conosci. In quel caso, viene mostrata anche l’età.

Il dato inserito da te ha la precedenza su tutte le fonti e resta salvato. **Rimuovi** lo elimina. Un contatto o un’importazione non lo aggiungerà di nuovo.

Se non è impostato, puoi aggiungerlo da **Aggiungi compleanno** nella sezione Campi. La routine Compleanni legge lo stesso compleanno mostrato nella pagina. Il compleanno è un dato personale: non viene mai condiviso con il tuo team, neanche in un record condiviso.

## Importare un foglio di calcolo

**Importa CSV…**, sotto il menu di ordinamento in Persone, Organizzazioni o Progetti, aggiunge un foglio di calcolo salvato in formato CSV.

1. Controlla le colonne. La tua Machine prova a capire a cosa corrisponde ciascuna in base alle intestazioni e ai contenuti. Puoi modificare qualsiasi scelta. Quando il tuo modello è disponibile, controlla anche le colonne e spiega brevemente i casi in cui non è sicuro. Vede solo le intestazioni, alcuni valori per colonna e le celle che non è riuscito a leggere con le regole.
2. Controlla le correzioni. **Rivedi** le mostra prima e dopo: spazi in eccesso, nomi in maiuscolo, numeri di telefono in formato internazionale, errori negli indirizzi email (gmial.com), siti web convertiti nel dominio, date e valori in qualsiasi formato ("€12k" corrisponde a 12000), più tag nella stessa cella, una fase scritta in modo diverso e la stessa riga duplicata. Deseleziona un tipo o una riga per lasciarli invariati.
3. Controlla l’anteprima. Ogni riga è nuova, corrisponde a una già presente nel tuo Graph oppure viene ignorata, con una spiegazione. Una persona viene abbinata tramite email (altrimenti tramite nome e organizzazione), un’organizzazione tramite sito web o nome e un progetto tramite nome.
4. **Importa** aggiunge i nuovi record e completa quelli corrispondenti. Le celle vuote non modificano nulla.

Puoi usare **Annulla** subito dopo l’importazione, oppure **Annulla l’ultima importazione** sotto il menu di ordinamento, per annullare l’ultima importazione se i record non sono stati modificati nel frattempo. Se l’annullamento sovrascrivesse una correzione successiva, ti verrà spiegato il motivo. Il file resta sulla tua Machine.

## Proprietario

In una Fleet di lavoro, ogni persona, organizzazione e progetto ha un proprietario: **Proprietario** nella sezione Insieme a te della pagina. Sei tu, a meno che tu non scelga qualcuno dalla tua Fleet di lavoro. Con **Proprietario** nei filtri puoi visualizzare solo i tuoi record. Ogni modifica compare nella relativa cronologia.

## Team

**Team**, accanto a Miei, mostra ciò che condividono i tuoi colleghi, con le stesse schede e lo stesso menu di ordinamento. **Filtra** restringe l’elenco in base a chi ha condiviso l’elemento, a un’organizzazione (Persone) o allo stato (Progetti). Quello che aggiungi qui è tuo.

Il lavoro con i clienti viene condiviso con le Machine dei tuoi colleghi, insieme al proprietario, ai campi e ai tag. Quello che condividono loro compare nella tua Machine. Ogni conversazione mostra **Team** o **Solo tu**. Scopri di più in [Graph del team](team-graph.md).
