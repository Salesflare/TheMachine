---
title: Note
area: graph
summary: Una pagina chiara per ogni argomento, come un viaggio o la tua casa, collegata alle persone e ai progetti che ne fanno parte.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, dashboard/graph-notes.js
order: 8
translated: 59dd4e1951e7cc7d
---
Una nota offre una panoramica su un argomento: un viaggio, la tua casa, il modo in cui vengono gestite le fatture. Le note si trovano nel Graph, insieme a Persone, Organizzazioni e Progetti. Restano sulla tua Machine e non vengono condivise con il tuo team.

## Crea una nota

Tocca **Nuova nota** in cima a Note. Assegna un titolo e tocca **Inizia la nota**: si aprirà la pagina. **Aggiungi una riga** aggiunge ciò che vuoi conservare. Ogni riga di testo diventa una riga a sé.

## Collega persone, progetti e altre note

Digita @ e alcune lettere di un nome in una riga. Scegli una persona, un’organizzazione, un progetto o una nota dall’elenco: il nome verrà inserito come link. Nella pagina dell’elemento che hai collegato, la tua nota comparirà sotto **Collegato da**.

## Note sotto altre note

Una nota può trovarsi sotto un’altra, per esempio Elettrodomestici sotto Casa. Note le mostra come un albero: tocca la freccia accanto a una nota per aprire quelle al suo interno. Per spostare una nota, tocca **Modifica** e scegli dove inserirla sotto **Sotto**. **Nuova nota sotto questa** nel menu ⋯ ne crea una proprio lì.

## Note che la tua Machine conserva

La tua Machine scrive anche note in autonomia, a partire dai tuoi messaggi, e le mantiene aggiornate. Ogni riga indica da dove proviene, per esempio chi ha inviato l’email: toccala per aprire il messaggio. Una riga tratta da **Ciò che ho imparato** riporta **Da ciò che ho imparato**.

Le tue modifiche restano sempre. Rinomina una nota, spostala, modifica le date o una riga: quando aggiorna la nota, la tua Machine mantiene le tue modifiche. Se elimini una riga o una nota, non verrà ripristinata. Le note successive sullo stesso argomento verranno inserite dove hai messo la prima.

**Ripristina l’originale** mostra di nuovo le parole usate dalla tua Machine. Se modifichi una riga tratta da ciò che la tua Machine ha imparato, la modifica si applica anche sotto **Ciò che ho imparato**, così ne esiste una sola versione.

## Viaggi

Quando arriva un’email di conferma per un volo, un hotel, un treno, un autobus, un traghetto o un’auto a noleggio, la tua Machine aggiunge la prenotazione a un viaggio sotto **Viaggi**. Le prenotazioni dello stesso viaggio vengono raccolte in un’unica voce: il viaggio di andata, l’hotel e il ritorno. Per ogni riga del viaggio sono indicati il codice di prenotazione, il posto e il biglietto, in ordine cronologico, oltre alle date del viaggio. In [Calendario](calendar.md) il viaggio appare come una fascia che copre quei giorni: toccala per aprire il viaggio.

La tua Machine legge i dettagli delle prenotazioni che compagnie aeree, hotel e siti di prenotazione inseriscono nelle email di conferma. Un’email senza questi dettagli non crea un viaggio. Se una prenotazione cambia, la relativa riga viene aggiornata; se viene annullata, la riga viene rimossa. Quando tutte le prenotazioni di un viaggio vengono annullate, viene rimosso anche il viaggio.

## Casa

Sotto **Casa**, la tua Machine conserva ciò che sa sulla tua casa: **Bollette e abbonamenti**, **Elettrodomestici**, **Riparazioni e manutenzione** e **La casa**. Una sezione compare quando contiene almeno due righe.

- Una bolletta ricorrente, per esempio quella dell’elettricità o dell’acqua, viene aggiunta con la frequenza e la data dell’ultima bolletta. **Apri l’attività** mostra la bolletta; l’importo e i dettagli del pagamento restano lì.
- Un abbonamento che hai mantenuto viene aggiunto e apre la relativa attività di **Abbonamenti**. Gli abbonamenti che hai annullato non vengono elencati.
- Anche ciò che la tua Machine ha imparato sulla tua casa, per esempio la marca della lavastoviglie, compare in una riga. Se la modifichi, la modifica si applica anche sotto **Ciò che ho imparato**.
- Se in una sezione hai una tua nota, per esempio una nota sulla lavastoviglie sotto **Elettrodomestici**, le informazioni su quell’elemento vengono aggiunte lì. La tua Machine non crea note di questo tipo in autonomia.

Vengono usate solo le bollette e gli abbonamenti Personali, e le note di Casa sono sempre Personali. Per ogni nuova bolletta, abbonamento o informazione appresa, la tua Machine chiede una volta alla sua AI di stabilire se riguarda la tua casa. Per una bolletta invia il mittente, mai l’importo.

## Salute

Sotto **Salute**, la tua Machine conserva ciò che sa sulla tua salute: **Appuntamenti**, **Medici e assistenza**, **Farmaci**, **Allergie e patologie** e **Fatture e assicurazione**. Una sezione compare quando contiene almeno due righe.

- Un appuntamento nel tuo calendario a cui vai solo tu, per esempio dal dentista, viene aggiunto con la prossima data o con l’ultima. **Dal tuo calendario** lo apre.
- Una fattura di un medico, un dentista o una farmacia viene aggiunta e apre la relativa attività. L’importo resta lì.
- Anche ciò che la tua Machine ha imparato sulla tua salute, per esempio un’allergia, compare in una riga. Se la modifichi, la modifica si applica anche sotto **Ciò che ho imparato**.
- Una tua nota in una sezione, per esempio una nota sul tuo fisioterapista sotto **Appuntamenti**, raccoglie le informazioni su quell’elemento.

Le note di Salute sono sempre Personali, anche quando una fattura arriva al tuo indirizzo di lavoro. Per ogni nuovo appuntamento, fattura o informazione appresa, la tua Machine chiede una volta alla sua AI di stabilire se riguarda la tua salute. Invia il nome dell’appuntamento, mai le note o i nomi delle altre persone invitate.

## Unisci, elimina e annulla

**Unisci in…** nel menu ⋯ sposta le righe di una nota e le note al suo interno in un’altra nota. Da quel momento, la tua Machine aggiunge le nuove informazioni a quella nota. **Elimina** rimuove una nota. Per entrambe le azioni, e anche quando rimuovi una riga, puoi toccare **Annulla** per qualche istante.

## Non sono note di riunione

Le note di riunione e quelle relative a una persona o a un’organizzazione restano dove si trovavano. Le note qui sono pagine a sé.
