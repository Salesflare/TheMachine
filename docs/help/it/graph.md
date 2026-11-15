---
title: Il Graph
area: graph
summary: Le persone, le organizzazioni e i progetti nei tuoi messaggi, sempre aggiornati automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: e437109f98725e65
---
La tua Machine crea una mappa delle persone con cui hai contatti e di quello che succede, a partire dai tuoi messaggi, riunioni e decisioni. Non devi configurare nulla e tutto resta sulla tua Machine.

- [Persone](people.md): tutte le persone con cui sei in contatto, con un riepilogo e una cronologia per ciascuna.
- [Organizzazioni](organizations.md): le aziende per cui lavorano, con le relative persone e i progetti.
- [Progetti](projects.md): quello che succede, organizzato in bacheche con fasi, come le trattative in un CRM.
- [Note](notes.md): una pagina leggibile per ogni argomento, come un viaggio o la tua Casa.

## Aggiornamenti di oggi

Una riga discreta in cima a ogni elenco indica cosa ha aggiornato oggi la tua Machine, ad esempio **Oggi ha aggiornato 4 persone**. Toccala per vedere chi e cosa è cambiato. Toccando un nome, si apre la sua pagina con **Modifiche recenti** aperto. Un piccolo punto segnala ogni riga e riquadro della bacheca modificati oggi. Vengono conteggiate solo le modifiche apportate dalla tua Machine, a partire da mezzanotte.

## Filtrare e ordinare

**Filtra**, accanto alle schede, restringe l’elenco. Ogni elenco ha filtri diversi. Persone: livello di vicinanza, ultimo contatto, organizzazione, proprietario, tag e **Ha un progetto aperto**. Organizzazioni: settore, specializzazione, dimensioni, paese, ultimo contatto, proprietario, tag e **Ha un progetto aperto**. Progetti: proprietario, bacheca, fase, tag, organizzazione, valore, data di chiusura prevista e **Senza risposta da oltre 10 giorni**.

I filtri selezionati appaiono sopra l’elenco, insieme a **Cancella**. In Progetti, l’elenco e la bacheca condividono lo stesso filtro. Sul telefono, i filtri si aprono in un pannello.

Il menu di ordinamento ordina l’elenco. Persone e Organizzazioni si possono ordinare per livello di vicinanza, contatto più recente o meno recente e nome. Organizzazioni si possono ordinare anche per dimensioni. Progetti si possono ordinare per ultima attività, nome, fase, **Valore** e **Data di chiusura**. **Scarica CSV**, sotto il menu di ordinamento, salva la scheda che stai visualizzando come foglio di calcolo.

## Campi e tag

Nella sezione Campi di una persona, organizzazione o progetto, fai clic su un valore per modificarlo: **Salva** o Invio conferma, **Annulla** o Esc annulla, **Rimuovi** svuota il campo.

**Gestisci campi** (**Aggiungi un campo** se non ce ne sono) aggiunge o rimuove campi per tutti i record di quel tipo. **Nuovo campo** ne aggiunge uno: testo, numero, data o una scelta da un elenco.

**+ Tag** aggiunge un tag, come VIP o partner; **×** lo rimuove. I tag appaiono negli elenchi e **Filtra** li trova.

## Compleanno

Il compleanno di una persona appare sotto Contatto, insieme alla fonte: il suo contatto Google, un compleanno su Google Calendar (la routine Compleanni lo salva per un contatto stretto), un’importazione da Facebook, le tue note oppure tu. **Modifica** permette di impostarlo o correggerlo: mese e giorno, e anche l’anno se lo conosci (in quel caso appare anche la sua età).

Il valore inserito da te ha la precedenza su tutte le fonti e rimane salvato. **Rimuovi** lo elimina; un contatto o un’importazione non lo aggiungono di nuovo.

Se non è impostato, **Aggiungi compleanno** sotto Campi permette di aggiungerlo. La routine Compleanni legge lo stesso compleanno mostrato nella pagina. Il compleanno è un dato personale: non viene mai condiviso con il tuo team, nemmeno in un record condiviso.

## Importare un foglio di calcolo

**Importa CSV…**, sotto il menu di ordinamento di Persone, Organizzazioni o Progetti, aggiunge un foglio di calcolo salvato in formato CSV.

1. Controlla le colonne. La tua Machine prova a capire a cosa corrisponde ogni colonna in base alle intestazioni e ai contenuti; puoi modificarle. Quando il tuo modello può essere eseguito, controlla anche le colonne e indica brevemente i casi in cui non è sicuro. Vede solo le intestazioni, alcuni valori per colonna e le celle che non riesce a interpretare secondo le regole.
2. Controlla le correzioni. **Rivedi** le mostra affiancate, prima e dopo: spazi in eccesso, nomi in maiuscolo, numeri di telefono nel formato internazionale, errori negli indirizzi email (gmial.com), siti web sostituiti dal relativo dominio, date e valori in qualsiasi formato ("€12k" corrisponde a 12000), più tag nella stessa cella, una fase scritta in modo diverso e la stessa riga ripetuta. Deseleziona un tipo di correzione o una riga per lasciarli invariati.
3. Controlla l’anteprima. Ogni riga è nuova, corrisponde a un elemento già presente nel tuo Graph oppure viene ignorata, con una spiegazione. Una persona viene riconosciuta dall’indirizzo email (altrimenti da nome e organizzazione), un’organizzazione dal sito web o dal nome, un progetto dal nome.
4. **Importa** aggiunge i nuovi elementi e aggiorna quelli corrispondenti. Una cella vuota non modifica nulla.

Usa **Annulla** subito dopo oppure **Annulla l’ultima importazione** sotto il menu di ordinamento per annullare l’ultima importazione, se i record non sono stati modificati nel frattempo. Se l’operazione sovrascriverebbe una correzione successiva, viene spiegato il motivo. Il file resta sulla tua Machine.

## Proprietario

In una Work Fleet, ogni persona, organizzazione e progetto ha un proprietario: **Proprietario** sotto **Con te** nella relativa pagina. Sei tu, a meno che tu non scelga qualcuno dalla tua Work Fleet. **Proprietario** in **Filtra** mostra solo gli elementi che ti appartengono. Ogni modifica appare nella cronologia.

## Team

**Team**, accanto a **I miei**, mostra ciò che condividono i tuoi colleghi, con le stesse schede e lo stesso menu di ordinamento. **Filtra** restringe l’elenco in base a chi ha condiviso l’elemento, all’organizzazione (Persone) o allo stato (Progetti). Quello che aggiungi qui è tuo.

Il lavoro con i clienti viene condiviso con le Machine dei tuoi colleghi, insieme al proprietario, ai campi e ai tag. Quello che condividono loro appare nella tua Machine. Ogni conversazione mostra **Team** o **Solo tu**. Scopri di più in [Graph del team](team-graph.md).
