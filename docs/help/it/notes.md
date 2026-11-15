---
title: Note
area: graph
summary: Una pagina chiara per ogni argomento, come un viaggio o la tua casa, collegata alle persone e ai progetti di cui parla.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a71c5e46042cddd0
---
Una nota offre una panoramica su un argomento: un viaggio, la tua casa, come vengono gestite le fatture. Le note si trovano nel Graph, accanto a Persone, Organizzazioni e Progetti. Restano sulla tua Machine e non vengono condivise con il tuo team.

## Crea una nota

Tocca **Nuova nota** in cima a Note. Scegli un titolo e tocca **Inizia la nota**: si apre la pagina. Tocca **Aggiungi una riga** per aggiungere ciò che vuoi conservare. Ogni riga di testo diventa una riga a sé.

## Collega persone, progetti e altre note

Digita @ seguito da alcune lettere di un nome in una riga. Scegli una persona, un'organizzazione, un progetto o una nota dall'elenco: il nome verrà inserito come link. Nella pagina dell'elemento collegato, sotto **Collegato da**, trovi la tua nota.

## Note secondarie

Una nota può trovarsi sotto un'altra, per esempio Elettrodomestici sotto Casa. Note le mostra come un albero: tocca la freccia accanto a una nota per vedere quelle al suo interno. Per spostare una nota, tocca **Modifica** e scegli dove inserirla sotto **Sotto**. Tocca **Nuova nota sotto questa** nel menu ⋯ per crearne una subito.

In cima alla pagina di una nota trovi la sua posizione, per esempio **Note › Figli**: tocca una parte qualsiasi per aprirla. Sul telefono, le note intermedie sono raccolte nel menu ⋯.

## Note create dalla tua Machine

La tua Machine crea anche note in automatico a partire dai tuoi messaggi e le tiene aggiornate. Ogni riga indica da dove proviene, per esempio chi ha inviato l'email: toccala per aprire il messaggio. Una riga tratta da **Ciò che ho imparato** riporta **Da ciò che ho imparato**.

Le riunioni e gli appuntamenti del calendario non diventano mai una riga a sé: restano in [Calendario](calendar.md). Anche le relative email restano lì: l'invito, le risposte, gli aggiornamenti e le cancellazioni.

**Casa**, **Salute** e **Figli** compaiono solo quando la tua Machine ha almeno due informazioni concrete da mostrare, per esempio una fattura o qualcosa che ha imparato. Fino ad allora non appaiono nell'elenco. Se poi restano di nuovo vuote, scompaiono.

Le tue modifiche vengono sempre mantenute. Rinomina una nota, spostala, cambia le sue date o una riga: quando la tua Machine aggiorna la nota, la lascia così. Se elimini una riga o una nota, non viene ripristinata. Le note successive sullo stesso argomento vengono aggiunte alla nota che hai scelto la prima volta.

**Ripristina l’originale** mostra di nuovo le parole usate dalla tua Machine. Se modifichi una riga tratta da ciò che la tua Machine ha imparato, la modifica si riflette anche in **Ciò che ho imparato**, così c'è una sola versione.

## Pagine generate

Quando una nota contiene almeno due righe tratte dai tuoi messaggi o da ciò che la tua Machine ha imparato, la tua Machine scrive una pagina in cima alla nota. Legge le conversazioni, non solo i loro oggetti:

- Un breve riepilogo: di cosa si parla e a che punto è la situazione.
- **Fatti principali**, **Decisioni**, **Questioni aperte** e una **Cronologia**, solo se ci sono informazioni concrete da riportare.
- Seguono le righe della nota, numerate, sotto **Fonti**. Ogni frase termina con i numeri delle righe da cui proviene: toccane uno per aprire la riga corrispondente.

La pagina viene riscritta solo quando cambiano le righe della nota, al massimo circa una volta al giorno. Se le fonti non contengono informazioni concrete, la pagina non viene creata e restano solo le righe. Se elimini una riga, dalla pagina scompaiono anche le informazioni che provenivano solo da quella riga. Nell'elenco Note, sotto il nome di ogni nota, appare l'inizio del riepilogo della pagina.

Nel Graph, i progetti e le organizzazioni hanno già una pagina dedicata, con una descrizione in cima. Le conversazioni che li riguardano finiscono lì, non in una nota.

## Note dalle tue conversazioni

La tua Machine legge le conversazioni complete e le inserisce nella nota a cui si riferiscono: thread email da una qualsiasi delle tue caselle di posta, chat in WhatsApp, Slack, Telegram, LinkedIn o un'altra app collegata, e note delle riunioni. I messaggi di chat vengono considerati un'unica conversazione finché la chat non resta inattiva per due giorni.

- Le conversazioni su un progetto o un'organizzazione nel Graph vengono aggiunte alla relativa pagina, non a una nuova nota.
- Una conversazione può finire in una sezione di **Casa**, **Salute** o **Figli**, in una tua nota oppure in una nota creata dalla tua Machine sotto **Lavoro**, **Auto**, **Tasse** o un'altra cartella.
- La tua Machine crea una nuova nota solo quando un argomento compare in almeno due conversazioni o in una conversazione a cui hai risposto e che è chiaramente ancora in corso.
- Ogni riga corrisponde a una conversazione, dalla più recente alla meno recente. Toccala per aprire la conversazione.

All'AI viene inviata una breve parte di ogni conversazione, senza risposte citate o firme. Ogni conversazione viene analizzata una sola volta; i nuovi messaggi vengono aggiunti alla stessa conversazione.

Le email e le chat di massa non vengono mai inserite in una nota né inviate all'AI: spam, promozioni, newsletter e altre email di liste, notifiche da indirizzi no-reply, bot e canali di trasmissione. Le conversazioni a cui hai risposto vengono incluse, così come le email di prenotazione per **Viaggi** ed **Eventi**.

La prima volta, la tua Machine esamina gli ultimi tre mesi di conversazioni nel giro di qualche ora, fuori dall'orario notturno e solo se il tuo piano AI ha spazio disponibile. In seguito, organizza le nuove conversazioni quando ce ne sono dieci in attesa oppure quando una è in attesa da mezza giornata.

## Viaggi

Quando ricevi un'email di prenotazione per un volo, un hotel, un treno, un autobus, un traghetto o un'auto a noleggio, la tua Machine la aggiunge a un viaggio sotto **Viaggi**. Le prenotazioni dello stesso viaggio vengono riunite in un'unica nota: andata, hotel e ritorno. Per ogni riga, la nota riporta il codice di prenotazione, il posto e il biglietto, in ordine cronologico, oltre alle date del viaggio. In [Calendario](calendar.md) il viaggio appare come una fascia che copre quei giorni. Toccala per aprire il viaggio.

La tua Machine legge i dettagli della prenotazione che compagnie aeree, hotel e siti di prenotazione includono nelle email di conferma. Un'email senza questi dettagli non crea un viaggio. Le email di prenotazione precedenti, comprese nell'anno di [cronologia](history.md) conservato dalla tua Machine, vengono lette in background una volta importata la cronologia, a partire dalle caselle di posta Personali. Una conferma più vecchia letta in seguito viene aggiunta al viaggio già esistente.

Se una prenotazione cambia, la relativa riga viene aggiornata. Se viene cancellata, la riga scompare. Quando tutte le prenotazioni di un viaggio vengono cancellate, scompare anche il viaggio.

## Eventi

Quando ricevi via email i biglietti per un concerto, una partita, un festival o una conferenza, la tua Machine aggiunge l'evento sotto **Eventi**, con una nota per ogni evento. Una riga indica dove si svolge e riporta il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto alla stessa nota. Come per i viaggi, la nota riporta le date dell'evento e appare come una fascia in [Calendario](calendar.md). Toccala per aprire la nota.

- Ogni riga indica chi ha inviato i biglietti, per esempio **Da Example Tickets**, e apre la relativa email.
- Se dall'email dei biglietti è stata creata un'attività, per esempio per pagare i biglietti, tocca **Apri l’attività** per visualizzarla.
- Un evento prenotato dalla tua casella di posta di lavoro è Lavoro; altrimenti è Personale.

La tua Machine legge i dettagli dei biglietti inclusi nelle email di conferma dei venditori, senza usare l'AI. Un'email senza questi dettagli non crea un evento. Se una prenotazione viene cancellata, scompare la relativa riga. Quando vengono cancellati tutti i biglietti di un evento, scompare anche l'evento.

## Casa

Sotto **Casa**, la tua Machine conserva ciò che sa sulla tua casa: **Bollette e abbonamenti**, **Elettrodomestici**, **Riparazioni e manutenzione** e **La casa**. Una sezione compare quando contiene almeno due righe.

- Una bolletta ricorrente, come quella dell'energia o dell'acqua, ha una riga che indica la frequenza e la data dell'ultima bolletta. Tocca **Apri l’attività** per visualizzare la bolletta: l'importo e i dettagli di pagamento restano lì.
- Un abbonamento che hai mantenuto ha una riga che apre la relativa attività in **Abbonamenti**. Gli abbonamenti cancellati non vengono elencati.
- Chi ti scrive regolarmente per questioni legate alla casa, come il fornitore di energia, il provider internet o il Comune, ha una riga che indica la frequenza delle email. Toccala per aprire l'email più recente.
- Anche ciò che la tua Machine ha imparato sulla tua casa, per esempio la marca della lavastoviglie, appare in una riga. Se la modifichi, cambia anche sotto **Ciò che ho imparato**.
- Se hai una tua nota in una sezione, per esempio una nota sulla lavastoviglie sotto **Elettrodomestici**, le informazioni su quell'elemento vengono aggiunte alla tua nota. La tua Machine non crea note di questo tipo in automatico.

Vengono usate solo bollette, abbonamenti ed email Personali, e le note di Casa sono sempre Personali. Per ogni nuova bolletta, abbonamento o informazione appresa, la tua Machine chiede una volta all'AI se riguarda la tua casa. Per una bolletta, invia chi l'ha emessa, mai l'importo.

Anche le tue conversazioni vengono aggiunte a queste note, come descritto sopra in **Note dalle tue conversazioni**.

## Salute

Sotto **Salute**, la tua Machine conserva ciò che sa sulla tua salute: **Appuntamenti**, **Risultati dei test**, **Medici e assistenza**, **Farmaci**, **Allergie e patologie** e **Fatture e assicurazione**. Una sezione compare quando contiene almeno due righe.

- Una fattura di un medico, dentista o farmacista ha una riga che apre la relativa attività. L'importo resta lì.
- Ogni email del tuo ambulatorio, di un ospedale, di un laboratorio o della tua assicurazione sanitaria diventa una riga con la data e l'oggetto, così la tua cronologia si arricchisce nel tempo. Toccala per aprire l'email.
- Anche ciò che la tua Machine ha imparato sulla tua salute, per esempio un'allergia, appare in una riga. Se la modifichi, cambia anche sotto **Ciò che ho imparato**.
- Se hai una tua nota in una sezione, per esempio una nota sul tuo fisioterapista sotto **Appuntamenti**, le informazioni su quell'elemento vengono aggiunte alla tua nota.

Le note di Salute sono sempre Personali, anche quando una fattura arriva al tuo indirizzo di lavoro. Per ogni nuova fattura o informazione appresa, la tua Machine chiede una volta all'AI se riguarda la tua salute.

## Figli

Sotto **Figli**, la tua Machine conserva ciò che sa sui tuoi figli: **Scuola**, **Attività**, **Assistenza all'infanzia**, **Medici e assistenza** e **Bollette e commissioni**. Le informazioni su una babysitter o un asilo nido finiscono sotto Assistenza all'infanzia, mai sotto Medici e assistenza. Una sezione compare quando contiene almeno due righe.

- Ciò che la tua Machine ha imparato su tuo figlio, per esempio il nome dell'insegnante o il giorno di nuoto, appare in una riga collegata alla sua pagina. Una persona viene considerata tuo figlio se sotto **Per te** è indicato il suo rapporto con te, per esempio figlia o figlio.
- Una fattura della scuola, di un club o per l'assistenza all'infanzia ha una riga che apre la relativa attività. L'importo resta lì.
- Ogni email della scuola, di un club o di chi si occupa dell'assistenza all'infanzia, per esempio un avviso su una gita o un cambio di programma, diventa una riga con la data e l'oggetto, così trovi tutto quello che ti inviano in un unico posto. Toccala per aprire l'email.
- Se hai una tua nota per un figlio in una sezione, per esempio una nota su Isla sotto **Scuola**, le informazioni su quel figlio vengono aggiunte alla tua nota.

Le note di Figli sono sempre Personali, anche quando la scuola scrive al tuo indirizzo di lavoro. Per ogni nuova informazione, la tua Machine chiede una volta all'AI se riguarda i tuoi figli.

## Unisci, elimina e annulla

Tocca **Unisci in…** nel menu ⋯ per spostare le righe di una nota e le note al suo interno in un'altra nota. Da quel momento, la tua Machine aggiunge le nuove informazioni a quella nota. Tocca **Elimina** per eliminare una nota. Dopo entrambe le operazioni, e dopo la rimozione di una riga, per un breve periodo è disponibile **Annulla**.

## Diverse dalle note delle riunioni

Le note delle riunioni e quelle relative a una persona o un'organizzazione restano dove sono. Le note qui sono pagine indipendenti.
