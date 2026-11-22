---
title: Il Graph
area: graph
summary: Le persone, le organizzazioni e i progetti nei tuoi messaggi, sempre aggiornati automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 181ff5fa2a9d8f47
---
La tua Machine crea una mappa delle persone con cui hai contatti e di quello che succede, a partire da messaggi, riunioni e decisioni. Non devi configurare nulla e tutto resta sulla tua Machine.

- [Persone](people.md): tutte le persone con cui hai contatti, con un riepilogo e una cronologia per ciascuna.
- [Organizzazioni](organizations.md): le aziende in cui lavorano, con le persone e i progetti associati.
- [Progetti](projects.md): quello che succede, organizzato in bacheche con fasi, come le trattative in un CRM.

Le modifiche che fai compaiono subito. Le nuove persone, i nuovi messaggi nelle loro cronologie e i dettagli trovati vengono mostrati entro 30 minuti.

## Aggiornamenti di oggi

Una riga discreta in cima a ogni elenco indica cosa ha aggiornato oggi la tua Machine, ad esempio **Oggi sono state aggiornate 4 persone**. Tocca la riga per vedere chi e cosa è cambiato. Toccando un nome si apre la sua pagina con **Modifiche recenti** già aperte. Un puntino indica ogni riga e riquadro della bacheca modificati oggi. Vengono conteggiate solo le modifiche fatte dalla tua Machine, a partire da mezzanotte.

## Filtra e ordina

**Filtra**, accanto alle schede, restringe l’elenco. Ogni elenco ha i propri filtri. Persone: grado di vicinanza, ultimo contatto, organizzazione, proprietario, tag e **Ha un progetto aperto**. Organizzazioni: settore, specializzazione, dimensioni, paese, ultimo contatto, proprietario, tag e **Ha un progetto aperto**. Progetti: proprietario, bacheca, fase, tag, organizzazione, valore, data di chiusura prevista e **Senza risposta da oltre 10 giorni**.

I filtri selezionati compaiono sopra l’elenco, insieme a **Cancella**. Nei Progetti, l’elenco e la bacheca condividono un unico filtro. Sul telefono, i filtri si aprono in un pannello.

Il menu di ordinamento permette di ordinare l’elenco. Persone e Organizzazioni si possono ordinare per grado di vicinanza, contatto più recente o meno recente e nome. Le Organizzazioni si possono ordinare anche per dimensioni. I Progetti si possono ordinare per ultima attività, nome, fase, **Valore** e **Data di chiusura**. **Scarica CSV**, sotto il menu di ordinamento, salva la scheda aperta come foglio di calcolo.

## Campi e tag

Nella sezione Campi di una persona, organizzazione o progetto, fai clic su un valore per modificarlo: **Salva** o Invio conferma la modifica, **Annulla** o Esc la annulla, **Rimuovi** svuota il campo.

**Gestisci campi** (**Aggiungi un campo** quando non ce ne sono) aggiunge o rimuove campi da tutti i record di quel tipo. **Nuovo campo** ne aggiunge uno: testo, numero, data o una scelta da un elenco.

**+ Tag** aggiunge un tag, ad esempio VIP o partner; **×** lo rimuove. I tag compaiono negli elenchi (sul telefono, quelli di una persona compaiono sulla sua pagina) e puoi trovarli con **Filtra**.

## Compleanno

Il compleanno di una persona compare in Contatti, insieme alla fonte: il suo contatto Google, un compleanno su Google Calendar (la routine Compleanni lo salva per i contatti con cui hai più confidenza), un’importazione da Facebook, le tue note o tu. **Modifica** permette di impostarlo o correggerlo: mese e giorno, e anche l’anno se lo conosci (in quel caso viene mostrata anche l’età).

Il compleanno che inserisci tu ha la precedenza su tutte le altre fonti e resta salvato. **Rimuovi** lo elimina; non viene ripristinato da un contatto o da un’importazione.

Se non è impostato, puoi aggiungerlo da **Aggiungi compleanno** nella sezione Campi. La routine Compleanni legge lo stesso compleanno mostrato nella pagina. Il compleanno è un dato personale: non viene mai condiviso con il team, nemmeno in un record condiviso.

## Importa un foglio di calcolo

**Importa CSV…**, sotto il menu di ordinamento in Persone, Organizzazioni o Progetti, aggiunge un foglio di calcolo salvato in formato CSV.

1. Controlla le colonne. La tua Machine prova ad abbinarle in base alle intestazioni e ai contenuti, ma puoi modificare gli abbinamenti. Quando il tuo modello è disponibile, controlla anche le colonne e spiega brevemente i casi in cui non è sicuro. Vede solo le intestazioni, alcuni valori per colonna e le celle che le regole non sono riuscite a leggere.
2. Controlla le correzioni. **Rivedi** le mostra prima e dopo: spazi in eccesso, nomi in maiuscolo, numeri di telefono in formato internazionale, errori negli indirizzi email (gmial.com), siti web convertiti nel loro dominio, date e valori in qualsiasi formato ("€12k" diventa 12000), più tag in una cella, una fase scritta in modo diverso e la stessa riga duplicata. Deseleziona un tipo di correzione o una riga per lasciarla invariata.
3. Controlla l’anteprima. Ogni riga è nuova, corrisponde a un record già presente nel tuo Graph oppure viene ignorata, con una spiegazione. Una persona viene abbinata tramite email (altrimenti tramite nome e organizzazione), un’organizzazione tramite sito web o nome e un progetto tramite nome.
4. **Importa** aggiunge i nuovi record e completa quelli corrispondenti. Le celle vuote non modificano nulla.

**Annulla** subito dopo l’importazione, oppure **Annulla l’ultima importazione** nel menu di ordinamento, annulla l’ultima importazione se quei record non sono stati modificati nel frattempo. Se l’importazione sovrascriverebbe una correzione successiva, viene spiegato il motivo. Il file resta sulla tua Machine.

## Proprietario

In una Fleet di lavoro, ogni persona, organizzazione e progetto ha un proprietario: **Proprietario** nella sezione Con te della relativa pagina. Sei tu, a meno che non scelga una persona della tua Fleet di lavoro. **Proprietario** in Filtra mostra solo i tuoi record. Ogni modifica compare nella relativa cronologia.

## Team

**Team**, accanto a I miei, mostra ciò che i tuoi colleghi condividono, con le stesse schede e lo stesso menu di ordinamento. **Filtra** permette di restringere i risultati in base a chi li ha condivisi, a un’organizzazione (Persone) o allo stato (Progetti). Quello che aggiungi qui è tuo.

Il lavoro con i clienti viene condiviso con le Machine dei tuoi colleghi, insieme al proprietario, ai campi e ai tag. Quello che condividono loro compare nella tua. Ogni conversazione indica **Team** o **Solo tu**. Consulta [Graph del team](team-graph.md).
