---
title: Il Graph
area: graph
summary: Le persone, le organizzazioni e i progetti nei tuoi messaggi, aggiornati da soli.
covers: tab:people
code: graph.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, enrichment.py, dashboard.html
order: 1
---
La tua Machine costruisce una mappa delle persone con cui hai a che fare e di cosa sta succedendo, a partire da messaggi, riunioni e decisioni. Non c'è niente da configurare, e resta sulla tua Machine.

## Persone

Tutte le persone con cui sei in contatto, le più vicine per prime. La pagina di una persona inizia con foto, nome, ruolo, organizzazione e luogo, e una riga su come siete in contatto ("Vi sentite ogni giorno · ultimo ven 23 ott · prossima riunione mar 27 ott"). Sotto:

- **Contatto**: i suoi telefoni ed email. Toccane uno per chiamare o scrivere, oppure **Copia**.
- **Con te**: cosa rappresenta per te, contatto di Lavoro o Personale, e la tua Famiglia o la tua Fleet, con **Vedi in Fleet**.
- **Anche su**: gli altri posti dove vi scrivete. **Slack** apre la persona in Slack, o il tuo thread Slack più recente con lei.
- Le **Persone** e i **Progetti** di cui fa parte, **In sospeso tra voi** (promesse in entrambe le direzioni, con **Fatto** e **Lascia perdere**) e la sua **Cronologia**.

Gli indirizzi e le chat di una persona si uniscono da soli quando è chiaro che si tratta della stessa persona, come un'email di lavoro con il suo indirizzo personale in CC.

Le schede **Lavoro** e **Personale** mostrano solo quei contatti. **Scarica CSV**, nel menu di ordinamento, salva la scheda in cui sei come foglio di calcolo, anche per Organizzazioni e Progetti.

### Cronologia

Ogni pagina di persona e organizzazione ne ha una, dalla più recente: email, riunioni e i loro riepiloghi Zoom, conversazioni Intercom (aperte o chiuse, con **Apri in Intercom**), chat WhatsApp, Telegram, Slack, LinkedIn e X, attività, promesse e spostamenti di progetto. I chip in alto mostrano una fonte alla volta. **Mostra altro** carica quelle più vecchie.

Le riunioni ancora da fare stanno a parte in alto sotto **In arrivo**, le più vicine per prime; **Mostra tutti i prossimi** mostra le altre. Una riunione presente in più di uno dei tuoi calendari compare una volta sola.

La cronologia di un'organizzazione contiene i messaggi delle sue persone e le conversazioni Intercom dal suo dominio. Le tue cronologie sono tue: il Graph del team mostra solo quello che le tue regole di condivisione consentono.

Se una pagina dice **Impossibile caricare questa pagina.**, tocca **Riprova**. Se continua a dirlo, usa **Qualcosa non va?** in fondo alla pagina.

## Filtra e ordina

**Filtra**, accanto alle schede in Persone, Organizzazioni e Progetti, restringe l'elenco per proprietario, tag, bacheca, fase, organizzazione, valore, data di chiusura prevista e **Senza risposta da oltre 10 giorni**. Persone e organizzazioni corrispondono tramite i loro progetti aperti. In Progetti, l'elenco e la bacheca condividono un solo filtro.

I filtri che hai scelto compaiono sopra l'elenco, con **Cancella**. Il menu di ordinamento ordina anche per **Valore** e **Data di chiusura**. Il filtro lo fa la tua Machine, così anche gli elenchi lunghi restano veloci. Sul telefono i filtri si aprono in un pannello.

## Team

**Team**, accanto a Miei, mostra cosa condividono i tuoi colleghi. Ha le stesse schede, lo stesso menu di ordinamento e **Nuova persona** o **Nuova organizzazione** come Miei; quello che aggiungi è tuo. **Filtra** lo restringe per chi l'ha condiviso, un'organizzazione (Persone) o uno stato (Progetti). In Progetti, **Miei**, **Tocca a me** e **Tutti** scelgono gli stessi progetti di una bacheca condivisa.

## Proprietario

In una Fleet di lavoro, ogni persona, organizzazione e progetto ha un proprietario: **Proprietario** sotto Con te nella sua pagina. Sei tu, a meno che tu non scelga qualcuno della tua Fleet di lavoro. **Proprietario** in Filtra mostra solo i tuoi, nell'elenco e sulla bacheca. Una scheda sulla bacheca mostra il nome del proprietario. Ogni cambio compare nella sua cronologia. Un record condiviso con il tuo team porta con sé il suo proprietario, con le stesse regole di condivisione del resto.

## Campi e tag

Sotto Campi in una persona, organizzazione o progetto, fai clic su un valore per cambiarlo: **Salva** o Invio lo conserva, **Annulla** o Esc lo lascia com'era, **Rimuovi** lo svuota. **Gestisci campi** aggiunge o rimuove campi: **Nuovo campo** ne aggiunge uno per tutti quelli dello stesso tipo: testo, numero, data o una scelta da un elenco. **Rimuovi** toglie un campo a tutti.

**+ Tag** aggiunge un tag, come VIP o partner; **×** lo toglie. I tag compaiono negli elenchi e **Filtra** li trova. Un record condiviso con il tuo team porta con sé i suoi campi e tag.

## Importa un foglio di calcolo

**Importa CSV…**, nel menu di ordinamento di Persone, Organizzazioni o Progetti, aggiunge un foglio di calcolo salvato come CSV. La tua Machine indovina quale colonna è quale dalle intestazioni e da cosa contengono; puoi cambiarle tutte.

Quando il tuo modello può girare, controlla anche le colonne, in qualsiasi lingua e comunque siano scritte le intestazioni, con un breve motivo dove non è sicuro. Vede solo le intestazioni, alcuni valori per colonna e le celle che le regole non sono riuscite a leggere, sulla tua Machine come una revisione. Senza modello, resta l'ipotesi fatta dalle intestazioni.

**Rivedi**, accanto alle correzioni suggerite, elenca le correzioni semplici come prima e dopo: spazi in più, nomi in maiuscolo, numeri di telefono in formato internazionale, refusi nelle email (gmial.com), siti web ridotti al dominio, date e valori in qualsiasi formato ("€12k" è 12000), più tag in una cella, una fase scritta in modo diverso da quella della bacheca e la stessa riga due volte.

Togli la spunta a un tipo o a una singola riga per lasciarla com'è. Non viene corretto nulla che non sia spuntato.

L'anteprima mostra ogni riga come nuova, corrispondente a una già presente nel tuo Graph, oppure saltata, con il motivo. Una corrispondenza è la stessa email per una persona (altrimenti lo stesso nome nella stessa organizzazione), lo stesso sito web o nome per un'organizzazione, e lo stesso nome per un progetto.

**Importa** aggiunge quelle nuove e completa le corrispondenze; una cella vuota non cambia nulla. **Annulla** subito dopo, o **Annulla l’ultima importazione** nel menu di ordinamento, annulla l'ultima importazione finché quei record non sono stati modificati. Le correzioni successive restano: se Annulla dovesse sovrascriverne una, spiega invece il perché. Il file resta sulla tua Machine.

## Un'organizzazione, più siti web

**⋯**, **Stessa organizzazione di…** nella pagina di un'organizzazione la fa diventare parte di un'altra, con le sue persone, i progetti e le note. **Aggiungi un sito web…** aggiunge un altro dei suoi siti, come il .io accanto al .com: le persone con un indirizzo lì si uniscono a essa, e i suoi dettagli vengono cercati per ogni sito.

Sono elencati sotto **Siti web**, ciascuno con **Separa** per annullare. Le modifiche successive all'organizzazione unita restano. Le organizzazioni che sembrano doppie compaiono sotto **Stessa organizzazione?**: **Unisci** o **Non è la stessa**.

## Aggiungi una persona o un'organizzazione

**Nuova persona** in cima a Persone, **Nuova organizzazione** in cima a Organizzazioni, oppure, sul telefono, **+** nella barra in alto. Inserisci un nome, e per una persona un'email e un'organizzazione se le hai; per un'organizzazione, il suo sito web. Quando nel tuo Graph c'è già qualcuno di simile, il modulo te lo mostra prima, così puoi aprire quello. **Aggiungi** apre la nuova pagina.

Una persona che aggiungi resta, anche senza messaggi. Il suo primo messaggio si collega a lei. Un'organizzazione che hai aggiunto si può eliminare dal suo menu **⋯** finché non c'è nessuno dentro.

## Su di te

I tuoi indirizzi e numeri, alias compresi, sono sempre tu, mai qualcuno nel tuo Graph. Se cerchi te stesso, o aggiungi una persona con uno dei tuoi indirizzi, si apre **Su di te**, e un'importazione salta la tua riga.

Su di te elenca i tuoi indirizzi con la loro provenienza; cambiali in **Impostazioni**, sotto Account. Una persona creata in passato dal tuo indirizzo passa da sola in Su di te, con un backup conservato sulla tua Machine.

Per inviare il tuo biglietto da visita a un collega o a un amico, scegli **Condividi il mio contatto**. Vedi [Condividi un contatto](share-contact.md).

## Immagine

Fai clic sull'immagine nella pagina di una persona o di un'organizzazione per cambiarla: **Carica un’immagine**, scegline una trovata per loro, oppure **Rimuovi foto**. Resta sulla tua Machine.

## Note

**Modifica** nella pagina di una persona o di un'organizzazione ha un campo **Note**, per qualsiasi cosa tu voglia ricordare. Le note compaiono nella pagina e restano anche dopo un'unione.

## Modifica una persona

**Modifica**, in cima alla sua pagina, cambia nome, ruolo, organizzazione, luogo, LinkedIn, telefoni ed email, cosa rappresenta per te, e Lavoro o Personale. **Salva** conserva le modifiche, **Annulla** lascia tutto com'era.

Le tue modifiche restano, anche quando i suoi dettagli vengono cercati di nuovo o una revisione legge qualcos'altro, e anche dopo **Unisci** e **Annulla**. Svuota un campo per usare di nuovo il valore trovato. Un nome vuoto riporta quello dei suoi messaggi.

## Stessa persona?

Quando due persone potrebbero essere una sola, la loro pagina chiede se sono la stessa persona, e Persone le elenca sotto **Stessa persona?**. **Unisci** le unisce, con tutti i loro messaggi, note, ruoli e progetti. **Non è la stessa** le tiene separate per sempre.

**Unisci tutti** unisce in una volta ogni coppia dell'elenco, tranne quelle che hai segnato come **Non è la stessa**. **Annulla** subito dopo le separa di nuovo tutte.

La pagina di una persona unita elenca il motivo sotto **Unita da**. **Annulla** la separa di nuovo.

Per unire tu stesso due persone, aprine una, poi **⋯**, **Stessa persona di…** e scegli l'altra.

## Ruolo e foto

Le persone con un indirizzo aziendale ricevono ruolo, foto, LinkedIn e città, cercati come i [dettagli delle organizzazioni](organization-data.md). Su una Machine in hosting vengono inviati solo il nome e il dominio aziendale. Disattivalo in **Impostazioni**, sotto Sicurezza: **Cerca i contatti di lavoro**.

Le tue connessioni completano altri dati mentre girano, con quello che leggono già e senza chiedere nulla in più: ruolo, telefono e fuso orario da Slack, bio, luogo e sito web da X, headline e foto da LinkedIn, e ruoli dai contatti Google e da Salesflare. Quello che una persona dice di sé viene prima. Passa con il mouse sulla riga sotto il nome per vedere da dove viene. Resta tutto sulla tua Machine.

Le immagini di WhatsApp arrivano tramite la sincronizzazione WhatsApp sempre attiva, quando lo consente: fino a 50 al giorno, solo per persone già nel tuo Graph. Non viene inviato nulla a loro.

## Elimina una persona definitivamente

Nella sua pagina, apri il menu ⋯ e scegli **Elimina definitivamente…**, poi **Elimina**. Rimuove la persona e quello che la tua Machine sa di lei: la sua scheda, gli indirizzi, i dettagli trovati, i messaggi solo tra voi due e le note su di lei. Le attività che la riguardano restano, senza il suo nome. Non verrà aggiunta di nuovo. Non si può annullare.

## Chi è chi

Ruoli che la tua Machine ha letto nei tuoi messaggi, in attesa della tua conferma. **✓ Giusto** ne conferma uno; **Modifica** apre la pagina della persona in modifica. Impara dalle tue modifiche. Compare solo quando ci sono ruoli in attesa.

## In una Fleet di lavoro

Il lavoro con i clienti viene condiviso con le Machine dei tuoi colleghi, e il loro compare nella tua. Ogni thread mostra **Team** o **Solo tu**. Vedi [Graph del team](team-graph.md).

## Organizzazioni

Aziende, dagli indirizzi e dai nomi nei tuoi messaggi. Vedi [Dettagli delle organizzazioni](organization-data.md).

La pagina di un'organizzazione è fatta come quella di una persona: logo, nome e cosa fa, una riga su come siete in contatto, poi **Contatto** (sito web e LinkedIn), **Con te** (cosa rappresenta per te), le persone che ci lavorano e la sua **Cronologia**.

I suoi **Progetti** elencano prima quelli aperti, ciascuno con la sua fase. I loro spostamenti compaiono nella sua cronologia. **Modifica** in alto cambia i suoi dettagli e cosa rappresenta per te. **Chiedi alla Fleet chi la conosce** trova un modo per arrivarci tramite la tua Fleet.

La posta degli strumenti di riscaldamento email viene tenuta fuori, sotto "Nascosta come riscaldamento", con **Annulla** per ogni dominio.

## Progetti

Li nomina la tua Machine in base a ciò di cui parlano i tuoi messaggi. I segnali che sembrano farne parte compaiono come "probabilmente ne fa parte". Se rinomini un progetto con il nome di un altro progetto, i due si uniscono.

Oppure gestiscili a mano, come le trattative in un CRM:

- **Nuovo progetto**: in cima a una bacheca, **+ Aggiungi** sotto una fase, **Nuovo progetto** in cima all'elenco, **+** nella barra in alto sul telefono, oppure dalla pagina di una persona o di un'organizzazione. Inserisci un nome, una bacheca e una fase, un'organizzazione (cercala nel tuo Graph, o **Aggiungi** una nuova), un valore, una data di chiusura prevista, persone e note. I progetti già nel tuo Graph con un nome simile compaiono per primi.
- **Modifica** nella pagina di un progetto, oppure **Modifica** nel **⋯** di una scheda sulla bacheca (o premi E su una scheda). Cambia tutto quanto sopra.
- **Vinto** o **Perso**, con il motivo. Vinto lo sposta nell'ultima fase della bacheca, Perso in Fermi o rifiutati. **Riapri** lo annulla.
- **Archivia** lo toglie dalla bacheca e dagli elenchi; un nuovo messaggio su di esso lo riporta indietro. **Elimina** lo rimuove per sempre; i suoi messaggi e le sue persone restano.
- Sposta una scheda trascinandola, oppure con **⋯**, **Sposta in** sul telefono. Il tuo spostamento resta finché un messaggio più recente non la sposta.
- **Fasi**, in cima a una bacheca, mostra solo le fasi che scegli, per ogni bacheca. **Cancella** le mostra di nuovo tutte.
- "4 senza risposta da oltre 10 giorni" sotto una fase: toccalo per vedere solo quelli, sulla bacheca e nell'elenco. Toccalo di nuovo per vederli tutti.

### Le attività di un progetto

Un'attività può appartenere a un progetto. La tua Machine lo sceglie quando il suo thread o le persone che riguarda sono su un unico progetto aperto, e l'attività ne mostra il nome sotto il titolo. **Cambia progetto** in **Altro** dell'attività, o **Metti su un progetto** nel menu dei comandi (Ctrl K), lo cambia o lo toglie. La tua scelta resta.

La pagina di un progetto elenca le sue attività sotto **Attività**, prima quelle aperte, e la sua scheda sulla bacheca dice quante sono aperte. Collegare un'attività a un progetto condiviso non condivide nulla in più: il tuo team vede comunque solo quello che viene da messaggi condivisi.

### L'organizzazione di un progetto

Ogni progetto può essere collegato a un'organizzazione. La sua pagina, la sua riga e la sua scheda sulla bacheca la mostrano, con un link.

Quando nessuno l'ha scelta, la tua Machine la imposta in base alle persone del progetto e ai suoi messaggi, escludendo i tuoi colleghi. Lo fa solo quando un'organizzazione è chiaramente l'altra parte: l'email personale come Gmail non conta mai, e un progetto con più aziende resta senza. Il modulo del progetto indica allora "Dalle sue persone".

La tua scelta in **Modifica** resta sempre, anche quando la togli. **Stessa organizzazione di…** sposta con sé i progetti di un'organizzazione, e **Separa** li riporta indietro.

### Bacheche

Progetti di un tipo organizzati in fasi, come una pipeline di valutazione. **⋯** su una bacheca: **Modifica bacheca** (nome, fasi, quali progetti ne fanno parte), **Apri su questa bacheca** e **Nuova bacheca**. Le revisioni continuano ad aggiungere i progetti adatti e li mettono in una fase. Quando non sono sicure, la bacheca mostra "2 progetti potrebbero stare qui": **Aggiungi** o **Escludi**.

Spuntane alcuni, o **Seleziona tutto**, per gestirli in una volta, e **Annulla** subito dopo se cambi idea. Un progetto che raggruppa più controparti diventa un progetto per controparte quando lo aggiungi.

**Pipeline**, in cima a una bacheca, somma il valore dei progetti aperti per fase, e quanto dovrebbe chiudersi ogni mese in base alle date di chiusura. I progetti vinti, persi e fermi non sono aperti; quello che hai vinto questo mese compare a parte. I valori sono in euro, a meno che la tua Machine non usi un'altra valuta. Con **Proprietario** in Filtra, conta solo i tuoi.

Una nuova bacheca, o una bacheca suggerita che salvi, guarda una volta in tutta la tua cronologia. Trova progetti e organizzazioni adatti, crea un progetto per organizzazione e mette ciascuno in una fase. L'intestazione dice "Sto guardando nella tua cronologia…" mentre lavora, poi quanti ne ha aggiunti e quanti aspettano la tua revisione. Una bacheca Solo tu tiene per te quello che trova.

### La bacheca di un collega

In **Team**, le bacheche condivise dai colleghi compaiono accanto alle tue, prima quelle con più tuoi progetti. Ogni scheda dice l'ultima cosa successa, con la data, come sulla bacheca del suo proprietario: la riga più recente condivisa con il team, altrimenti il suo ultimo spostamento. Il nome del proprietario compare solo quando una fase ha schede di più colleghi; se è tutta di una persona, lo dice l'intestazione.

**Miei**, **Tocca a me** e **Tutti** scelgono cosa mostra una bacheca condivisa, e anche l'elenco dei progetti del team. Miei è ciò di cui fai parte: un suo thread, un progetto di cui sei proprietario o che hai tu, o una tua attività che lo riguarda. Tocca a me è ciò che aspetta te: un'attività aperta che lo riguarda, o un thread in cui il messaggio più recente è stato scritto a te.

Il resto di una fase si raccoglie in **Mostra altri N**. I progetti che si somigliano, come una serie di prove "… valutazione CRM", si raccolgono in una riga con un conteggio; toccala per aprirli. Niente di tutto questo cambia ciò che viene condiviso.

## Un'attività su qualcuno

**Nuova attività** nel menu **⋯** di una persona, un'organizzazione o un progetto avvia un'attività che li riguarda.

## Cosa sa di qualcuno

Sotto Cosa si sa, ogni fatto ha un menu:

- **Dimentica** lo elimina ovunque.
- Non riguarda questa persona lo toglie solo da quella pagina.
