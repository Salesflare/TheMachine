---
title: Note
area: graph
summary: Una pagina chiara per ogni argomento, come un viaggio o la tua casa, collegata alle persone e ai progetti coinvolti.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: b88647412222409d
---
Una nota offre una panoramica su un argomento: un viaggio, la tua casa, come gestire le fatture. Le note si trovano nel Graph, accanto a Persone, Organizzazioni e Progetti. Restano sulla tua Machine e non vengono condivise con il tuo team.

## Inizia una nota

Tocca **Nuova nota** in alto nella sezione Note. Assegna un titolo e tocca **Inizia la nota** per aprire la pagina. Con **Aggiungi una riga** puoi aggiungere quello che vuoi conservare. Ogni riga di testo diventa una riga a sé.

## Collega persone, progetti e altre note

In una riga, digita @ e le prime lettere di un nome. Scegli una persona, un’organizzazione, un progetto o una nota dall’elenco: il nome verrà inserito come link. Nella pagina dell’elemento collegato, la tua nota comparirà sotto **Collegato da**.

## Note sotto altre note

Una nota può trovarsi sotto un’altra, per esempio Elettrodomestici sotto Casa. Le note sono organizzate in una struttura ad albero: tocca la freccia accanto a una nota per aprire quelle che contiene. Per spostare una nota, tocca **Modifica** e scegli dove collocarla sotto **Sotto**. Per creare una nota al suo interno, tocca **Nuova nota sotto questa** nel menu ⋯.

## Note che la tua Machine tiene

La tua Machine scrive anche note da sola, a partire dai tuoi messaggi, e le aggiorna. Ogni riga indica da dove proviene, per esempio chi ha inviato l’email: toccala per aprire il messaggio. Una riga tratta da **Ciò che ho imparato** riporta **Da ciò che ho imparato**.

Le tue modifiche restano sempre. Rinomina o sposta una nota, cambia le date o una riga: quando la aggiorna, la tua Machine manterrà le tue modifiche. Se elimini una riga o una nota, non verrà ripristinata. Le note successive sullo stesso argomento verranno aggiunte a quella che hai scelto.

Con **Ripristina l’originale** puoi rivedere le parole originali della tua Machine. Se modifichi una riga che proviene da ciò che la tua Machine ha imparato, la modifica si applica anche in **Ciò che ho imparato**, così ne esiste una sola versione.

## Viaggi

Quando ricevi un’email di conferma per un volo, un hotel, un treno, un autobus, un traghetto o un’auto a noleggio, la tua Machine la aggiunge a un viaggio sotto **Viaggi**. Le prenotazioni dello stesso viaggio vengono raggruppate: l’andata, l’hotel e il ritorno. Il viaggio include il codice di prenotazione, il posto e il biglietto per ogni riga, in ordine cronologico, e mostra le date. In [Calendario](calendar.md) appare come una singola fascia che copre quei giorni; toccandola, si apre il viaggio.

La tua Machine legge i dettagli di prenotazione inseriti da compagnie aeree, hotel e siti di prenotazione nelle email di conferma. Un’email che non li contiene non crea un viaggio. Le email di prenotazione precedenti, comprese nell’anno di [cronologia](history.md) conservato dalla tua Machine, vengono lette in background dopo che la cronologia è stata importata. Se una prenotazione cambia, la relativa riga viene aggiornata; se viene annullata, viene rimossa. Quando tutte le prenotazioni di un viaggio sono annullate, viene rimosso anche il viaggio.

## Eventi

Quando ricevi via email i biglietti per un concerto, una partita, un festival o una conferenza, la tua Machine aggiunge l’evento sotto **Eventi**, con una nota per ogni evento. Una riga indica dove si svolge e include il codice di prenotazione, il posto e il numero di biglietti. Se fai un secondo ordine per lo stesso evento, viene aggiunto alla stessa nota. Come per un viaggio, l’evento mostra le date e appare come una fascia in [Calendario](calendar.md) che apre la nota.

- Ogni riga indica da chi provengono i biglietti, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email dei biglietti è stata creata un’attività, per esempio per pagarli, tocca **Apri l’attività** per visualizzarla.
- Un evento prenotato con la tua casella email di lavoro è classificato come Lavoro, altrimenti come Personale.

La tua Machine legge i dettagli dei biglietti inseriti dai rivenditori nelle email di conferma, senza usare l’AI. Un’email che non li contiene non crea un evento. Se una prenotazione viene annullata, viene rimossa; quando tutti i biglietti di un evento sono annullati, viene rimosso anche l’evento.

## Casa

Sotto **Casa**, la tua Machine conserva ciò che sa sulla tua casa: **Bollette e abbonamenti**, **Elettrodomestici**, **Riparazioni e manutenzione** e **La casa**. Una sezione appare quando contiene almeno due righe.

- Una bolletta ricorrente, per esempio quella dell’energia o dell’acqua, ha una riga che indica ogni quanto arriva e la data dell’ultima. Tocca **Apri l’attività** per visualizzare la bolletta: l’importo e i dettagli del pagamento sono lì.
- Un abbonamento che hai mantenuto ha una riga che apre la relativa attività in **Abbonamenti**. Quelli che hai annullato non vengono elencati.
- Anche ciò che la tua Machine ha imparato sulla tua casa, come la marca della lavastoviglie, compare in una riga. Se la modifichi, la modifica viene applicata anche in **Ciò che ho imparato**.
- Se tieni una tua nota in una sezione, per esempio una nota sulla lavastoviglie in **Elettrodomestici**, le informazioni su quell’elemento vengono aggiunte alla tua nota. La tua Machine non crea note di questo tipo da sola.

Vengono considerate solo le bollette e gli abbonamenti Personali, e le note di Casa sono sempre Personali. Per ogni nuova bolletta, abbonamento o elemento appreso, la tua Machine chiede una volta alla sua AI di stabilire se riguarda la tua casa. Per una bolletta, invia il nome del mittente, mai l’importo.

## Salute

Sotto **Salute**, la tua Machine conserva ciò che sa sulla tua salute: **Appuntamenti**, **Medici e assistenza**, **Farmaci**, **Allergie e patologie** e **Fatture e assicurazione**. Una sezione appare quando contiene almeno due righe.

- Un appuntamento sul tuo calendario a cui partecipi solo tu, per esempio dal dentista, ha una riga con la prossima data o, se non ce ne sono, con l’ultima. Tocca **Dal tuo calendario** per aprirlo.
- Una fattura di un medico, dentista o farmacista ha una riga che apre la relativa attività. L’importo è indicato lì.
- Anche ciò che la tua Machine ha imparato sulla tua salute, per esempio un’allergia, compare in una riga. Se la modifichi, la modifica viene applicata anche in **Ciò che ho imparato**.
- Se hai una tua nota in una sezione, per esempio una nota sul tuo fisioterapista in **Appuntamenti**, le informazioni su quell’elemento vengono aggiunte alla nota.

Le note di Salute sono sempre Personali, anche se una fattura è arrivata al tuo indirizzo email di lavoro. Per ogni nuovo appuntamento, fattura o elemento appreso, la tua Machine chiede una volta alla sua AI di stabilire se riguarda la tua salute. Per un appuntamento invia il nome, mai le note o i nomi degli altri invitati.

## Figli

Sotto **Figli**, la tua Machine conserva ciò che sa sui tuoi figli: **Scuola**, **Attività**, **Medici e assistenza** e **Bollette e commissioni**. Una sezione appare quando contiene almeno due righe.

- Ciò che la tua Machine ha imparato su tuo figlio, per esempio il nome dell’insegnante o il giorno di nuoto, compare in una riga che rimanda alla sua pagina. Considera qualcuno tuo figlio se sotto **Per te** è indicato un rapporto di parentela, per esempio figlia o figlio.
- Un evento sul tuo calendario a cui partecipi solo tu, per esempio un colloquio con gli insegnanti, ha una riga con la prossima data o, se non ce ne sono, con l’ultima. Tocca **Dal tuo calendario** per aprirlo.
- Una fattura per la scuola, un club o l’assistenza all’infanzia ha una riga che apre la relativa attività. L’importo è indicato lì.
- Se hai una tua nota per un figlio in una sezione, per esempio una nota per Isla in **Scuola**, le informazioni su quel figlio vengono aggiunte alla nota.

Le note di Figli sono sempre Personali, anche se la scuola scrive al tuo indirizzo email di lavoro. Per ogni nuovo elemento, la tua Machine chiede una volta alla sua AI di stabilire se riguarda i tuoi figli.

## Unisci, elimina e annulla

**Unisci in…** nel menu ⋯ sposta le righe di una nota e le note contenute al suo interno in un’altra nota. Da quel momento, la tua Machine aggiungerà i nuovi contenuti a quella nota. **Elimina** rimuove una nota. Dopo entrambe le operazioni, e dopo aver rimosso una riga, per qualche istante puoi toccare **Annulla**.

## Diverse dalle note delle riunioni

Le note delle riunioni e quelle associate a una persona o un’organizzazione restano dove sono. Le note qui sono pagine a sé.
