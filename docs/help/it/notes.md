---
title: Note
area: graph
summary: Una pagina chiara per ogni argomento, come un viaggio o la tua casa, collegata alle persone e ai progetti che ne fanno parte.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 88cfd4099bf27f38
---
Una nota offre una panoramica su un argomento: un viaggio, la tua casa, come gestire le fatture. Le note si trovano nel Graph, accanto a Persone, Organizzazioni e Progetti. Restano sulla tua Machine e non vengono condivise con il tuo team.

## Crea una nota

Tocca **Nuova nota** in alto nella sezione Note. Assegna un titolo e tocca **Inizia la nota** per aprire la pagina. Tocca **Aggiungi una riga** per aggiungere ciò che vuoi conservare. Ogni riga di testo diventa una riga a sé.

## Collega persone, progetti e altre note

Digita @ e le prime lettere di un nome in una riga. Scegli una persona, un’organizzazione, un progetto o una nota dall’elenco: il nome verrà inserito come link. Nella pagina dell’elemento collegato, sotto **Collegato da**, comparirà la tua nota.

## Note nidificate

Una nota può trovarsi sotto un’altra, come Elettrodomestici sotto Casa. La sezione Note le mostra come un albero: tocca la freccia accanto a una nota per vedere quelle che contiene. Per spostare una nota, tocca **Modifica** e scegli dove metterla sotto **Sotto**. Tocca **Nuova nota sotto questa** nel menu ⋯ per crearne una al suo interno.

In cima alla pagina di una nota trovi il percorso, per esempio **Note › Figli**: tocca una parte qualsiasi per aprirla. Sul telefono, le note intermedie sono raccolte nel menu ⋯.

## Note create dalla tua Machine

La tua Machine crea anche note dai tuoi messaggi e le mantiene aggiornate. Ogni riga indica da dove proviene, per esempio chi ha inviato l’email: toccala per aprire il messaggio. Una riga tratta da **Ciò che ho imparato** riporta **Da ciò che ho imparato**. Una riunione o un appuntamento sul calendario non compare mai come riga a sé: resta in [Calendario](calendar.md).

**Casa**, **Salute** e **Figli** compaiono solo quando la tua Machine ha almeno due informazioni concrete da aggiungere, come una bolletta o qualcosa che ha imparato. Fino ad allora non appaiono nell’elenco. Se poi non hanno più contenuti, scompaiono.

Le tue modifiche vengono sempre mantenute. Rinomina una nota, spostala, modifica le date o una riga: quando aggiorna la nota, la tua Machine conserva le tue modifiche. Se elimini una riga o una nota, non verrà ripristinata. Le note successive sullo stesso argomento finiranno nel posto in cui hai messo la prima.

Tocca **Ripristina l’originale** per rivedere le parole originali della tua Machine. Se modifichi una riga che deriva da qualcosa che la tua Machine ha imparato, la modifica si riflette anche in **Ciò che ho imparato**, così ne esiste una sola versione.

## Pagine scritte automaticamente

Quando una nota contiene almeno due righe tratte dai tuoi messaggi o da ciò che la tua Machine ha imparato, la tua Machine scrive una pagina in cima alla nota. Legge le conversazioni, non solo gli argomenti:

- Un breve riepilogo: di cosa si tratta e a che punto è.
- **Fatti principali**, **Decisioni**, **Questioni aperte** e una **Cronologia**, solo se ci sono informazioni concrete da riportare.
- Seguono le righe della nota, numerate sotto **Fonti**. Ogni frase termina con i numeri delle righe da cui proviene: tocca un numero per aprire la riga.

La pagina viene riscritta solo quando cambiano le righe della nota, al massimo circa una volta al giorno. Se le fonti non contengono informazioni concrete, la pagina non viene creata e restano solo le righe. Se elimini una riga, anche ciò che nella pagina derivava solo da quella riga viene rimosso. Nell’elenco delle note, sotto il nome di ciascuna nota, compare l’inizio del riepilogo.

Progetti e organizzazioni hanno già una propria pagina nel Graph, con una descrizione in cima. Le conversazioni su un progetto o un’organizzazione vengono aggiunte alla relativa pagina, non a una nota.

## Note dalle tue conversazioni

La tua Machine legge le conversazioni complete e le assegna alla nota pertinente: una conversazione email da una qualsiasi delle tue caselle, una chat su WhatsApp, Slack, Telegram, LinkedIn o un’altra app collegata, oppure gli appunti di una riunione. I messaggi di una chat contano come un’unica conversazione finché la chat non resta inattiva per due giorni.

- Una conversazione su un progetto o un’organizzazione nel Graph viene aggiunta alla relativa pagina, non a una nuova nota.
- Una conversazione può finire in una sezione di **Casa**, **Salute** o **Figli**, in una tua nota oppure in una nota creata dalla tua Machine sotto **Lavoro**, **Auto**, **Tasse** o un’altra cartella.
- La tua Machine crea una nuova nota solo se un argomento ha almeno due conversazioni oppure se hai scritto tu e la conversazione è chiaramente ancora in corso.
- Ogni riga corrisponde a una conversazione, dalla più recente alla meno recente. Tocca una riga per aprire la conversazione.

All’IA invia solo una breve parte di ogni conversazione, senza risposte citate né firme. Ogni conversazione viene elaborata una volta sola e i nuovi messaggi vengono aggiunti alla conversazione esistente.

Le email in blocco e le chat non vengono mai aggiunte a una nota né inviate all’IA: spam, promozioni, newsletter e altri messaggi di mailing list, notifiche automatiche, bot e canali broadcast. Le conversazioni a cui hai partecipato contano comunque, così come le email di prenotazione per **Viaggi** ed **Eventi**.

La prima volta, la tua Machine esamina i tre mesi precedenti nell’arco di qualche ora, fuori dalle ore notturne e solo se il tuo piano IA ha spazio disponibile. In seguito, organizza le nuove conversazioni quando ce ne sono dieci in attesa o quando una è in attesa da mezza giornata.

## Viaggi

Quando ricevi un’email di prenotazione per un volo, un hotel, un treno, un autobus, un traghetto o un’auto a noleggio, la tua Machine la aggiunge a un viaggio sotto **Viaggi**. Le prenotazioni dello stesso itinerario finiscono nello stesso viaggio: l’andata, l’hotel e il ritorno. Per ogni riga, il viaggio mostra il codice di prenotazione, il posto e il biglietto, in ordine cronologico, oltre alle date. In [Calendario](calendar.md) compare come una fascia che copre quei giorni e che apre il viaggio.

La tua Machine legge i dettagli che compagnie aeree, hotel e siti di prenotazione inseriscono nelle email di conferma. Un’email senza questi dettagli non crea un viaggio. Le email di prenotazione precedenti, comprese nell’anno di [cronologia](history.md) conservato dalla tua Machine, vengono lette in background dopo che la cronologia è stata importata, a partire dalle tue caselle Personali. Se in seguito viene letta una conferma più vecchia, viene aggiunta al viaggio già esistente.

Se una prenotazione cambia, la relativa riga viene aggiornata. Se viene annullata, la riga viene rimossa. Quando tutte le prenotazioni di un viaggio sono annullate, il viaggio viene rimosso.

## Eventi

Quando ricevi i biglietti per un concerto, una partita, un festival o una conferenza, la tua Machine aggiunge l’evento sotto **Eventi**, creando una nota per ogni evento. Una riga indica dove si svolge l’evento, con il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto alla stessa nota. Come un viaggio, l’evento mostra le date e compare in [Calendario](calendar.md) come una fascia che apre la nota.

- Ogni riga indica da chi provengono i biglietti, per esempio **Da Example Tickets**, e apre l’email corrispondente.
- Se dall’email dei biglietti è stata creata un’attività, per esempio pagare i biglietti, **Apri l’attività** la mostra.
- Un evento prenotato con la casella di lavoro è Lavoro, altrimenti è Personale.

La tua Machine legge i dettagli dei biglietti dalle email di conferma inviate dai venditori, senza usare l’IA. Un’email senza questi dettagli non crea un evento. Una prenotazione annullata viene rimossa. Quando tutti i biglietti di un evento sono annullati, anche l’evento viene rimosso.

## Casa

Sotto **Casa**, la tua Machine raccoglie ciò che sa sulla tua casa: **Bollette e abbonamenti**, **Elettrodomestici**, **Riparazioni e manutenzione** e **La casa**. Una sezione compare quando contiene almeno due righe.

- Una bolletta ricorrente, per esempio quella dell’energia o dell’acqua, ha una riga che indica ogni quanto arriva e la data dell’ultima. Tocca **Apri l’attività** per vedere la bolletta: l’importo e i dettagli del pagamento restano lì.
- Un abbonamento che hai mantenuto ha una riga che apre l’attività **Abbonamenti**. Gli abbonamenti annullati non vengono elencati.
- Chi ti scrive regolarmente a proposito della casa, per esempio il fornitore di energia, il provider internet o il comune, ha una riga che indica ogni quanto ti scrive. Tocca la riga per aprire l’email più recente.
- Anche ciò che la tua Machine ha imparato sulla casa, come la marca della lavastoviglie, compare in una riga. Se la modifichi, cambierà anche sotto **Ciò che ho imparato**.
- Se tieni una tua nota in una sezione, per esempio una nota sulla lavastoviglie sotto **Elettrodomestici**, le informazioni su quell’argomento finiscono nella tua nota. La tua Machine non crea note di questo tipo.

Vengono usate solo bollette, abbonamenti ed email personali, e le note di Casa sono sempre Personali. Per ogni nuova bolletta, abbonamento o informazione appresa, la tua Machine chiede una volta alla sua IA di verificare se riguarda la tua casa. Per una bolletta, invia il mittente, mai l’importo.

Anche le tue conversazioni vengono aggiunte a queste note, come descritto sopra in **Note dalle tue conversazioni**.

## Salute

Sotto **Salute**, la tua Machine raccoglie ciò che sa sulla tua salute: **Appuntamenti**, **Risultati dei test**, **Medici e assistenza**, **Farmaci**, **Allergie e patologie** e **Fatture e assicurazione**. Una sezione compare quando contiene almeno due righe.

- Una fattura di un medico, dentista o farmacia ha una riga che apre la relativa attività. L’importo resta lì.
- Ogni email del tuo ambulatorio, di un ospedale, di un laboratorio o della tua assicurazione sanitaria compare come una riga con la data e l’oggetto, così la cronologia si arricchisce nel tempo. Tocca la riga per aprire l’email.
- Anche ciò che la tua Machine ha imparato sulla tua salute, come un’allergia, compare in una riga. Se la modifichi, cambierà anche sotto **Ciò che ho imparato**.
- Se hai una tua nota in una sezione, per esempio una nota sul fisioterapista sotto **Appuntamenti**, le informazioni su quell’argomento finiscono nella tua nota.

Le note di Salute sono sempre Personali, anche se una fattura è arrivata al tuo indirizzo di lavoro. Per ogni nuova fattura o informazione appresa, la tua Machine chiede una volta alla sua IA di verificare se riguarda la tua salute.

## Figli

Sotto **Figli**, la tua Machine raccoglie ciò che sa sui tuoi figli: **Scuola**, **Attività**, **Assistenza all'infanzia**, **Medici e assistenza** e **Bollette e commissioni**. Una babysitter o un asilo nido rientra in Assistenza all'infanzia, mai in Medici e assistenza. Una sezione compare quando contiene almeno due righe.

- Ciò che la tua Machine ha imparato sui tuoi figli, come il nome dell’insegnante o il giorno di nuoto, compare in una riga collegata alla loro pagina. Considera una persona come tuo figlio o tua figlia quando sotto **Per te** è indicato il rapporto, per esempio figlia o figlio.
- Una fattura della scuola, di un’associazione o per l’assistenza all’infanzia ha una riga che apre la relativa attività. L’importo resta lì.
- Ogni email della scuola, di un’associazione o di un servizio di assistenza all’infanzia, per esempio una comunicazione su una gita o un cambio di programma, compare come una riga con la data e l’oggetto, così trovi tutto quello che ti inviano in un unico posto. Tocca la riga per aprire l’email.
- Se hai una tua nota per un figlio o una figlia in una sezione, per esempio una nota per Isla sotto **Scuola**, le informazioni su quel figlio o quella figlia finiscono nella tua nota.

Le note di Figli sono sempre Personali, anche se la scuola scrive al tuo indirizzo di lavoro. Per ogni nuova informazione, la tua Machine chiede una volta alla sua IA di verificare se riguarda i tuoi figli.

## Unisci, elimina e annulla

Tocca **Unisci in…** nel menu ⋯ per spostare le righe di una nota e le note contenute al suo interno in un’altra nota. Da quel momento, la tua Machine aggiungerà le nuove informazioni a quella nota. Tocca **Elimina** per rimuovere una nota. Dopo entrambe le operazioni, e anche dopo aver rimosso una riga, puoi toccare **Annulla** per qualche istante.

## Diversi dagli appunti delle riunioni

Gli appunti delle riunioni e le note su una persona o un’organizzazione restano dove si trovavano. Le note di questa sezione sono pagine a sé.
