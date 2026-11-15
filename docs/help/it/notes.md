---
title: Note
area: graph
summary: Una pagina chiara per ogni argomento, come un viaggio o la tua casa, collegata alle persone e ai progetti che ne fanno parte.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a32102a88a8b3856
---
Una nota raccoglie le informazioni su un argomento: un viaggio, la tua casa, come gestire le fatture. Nel Graph, le note sono accanto a Persone, Organizzazioni e Progetti. Restano sulla tua Machine e non sono condivise con il tuo team.

## Crea una nota

Tocca **Nuova nota** in alto nella sezione Note. Inserisci un titolo e tocca **Inizia la nota** per aprire la pagina. Con **Aggiungi una riga** aggiungi ciò che vuoi conservare. Ogni riga di testo diventa una riga a sé.

## Collega persone, progetti e altre note

In una riga, digita @ e le prime lettere di un nome. Seleziona dall’elenco una persona, un’organizzazione, un progetto o una nota: il nome verrà inserito come link. Nella pagina dell’elemento collegato, la tua nota comparirà sotto **Collegato da**.

## Note sotto altre note

Una nota può essere contenuta in un’altra, per esempio Elettrodomestici sotto Casa. Nella sezione Note, le note sono organizzate ad albero: tocca la freccia accanto a una nota per vedere quelle contenute al suo interno. Per spostare una nota, tocca **Modifica** e scegli dove inserirla sotto **Sotto**. Dal menu ⋯, tocca **Nuova nota sotto questa** per crearne una al suo interno.

## Note che la tua Machine tiene aggiornate

La tua Machine crea e aggiorna anche le note usando i tuoi messaggi. Ogni riga indica da dove proviene, per esempio chi ha inviato l’email: toccala per aprire il messaggio. Le righe basate su **Ciò che ho imparato** riportano **Da ciò che ho imparato**.

Le tue modifiche restano sempre. Se rinomini una nota, la sposti, ne modifichi le date o cambi una riga, la tua Machine manterrà le modifiche quando aggiornerà la nota. Se elimini una riga o una nota, non verrà ripristinata. Le note future sullo stesso argomento verranno aggiunte dove hai inserito la prima.

**Ripristina l’originale** mostra di nuovo il testo scritto dalla tua Machine. Se modifichi una riga basata su ciò che la tua Machine ha imparato, la modifica si applica anche sotto **Ciò che ho imparato**, così ne resta una sola versione.

## Viaggi

Quando ricevi un’email con la prenotazione di un volo, hotel, treno, autobus, traghetto o auto a noleggio, la tua Machine la aggiunge a un viaggio sotto **Viaggi**. Le prenotazioni dello stesso itinerario vengono raccolte in un unico viaggio: l’andata, l’hotel e il ritorno. Per ogni riga, il viaggio mostra il codice di prenotazione, il posto e il biglietto, in ordine cronologico, oltre alle date. In [Calendario](calendar.md), il viaggio appare come una fascia che copre quei giorni e, se la tocchi, si apre.

La tua Machine legge i dettagli delle prenotazioni che compagnie aeree, hotel e siti di prenotazione inseriscono nelle email di conferma. Un’email senza questi dettagli non crea un viaggio. Se una prenotazione cambia, la relativa riga viene aggiornata; se viene annullata, viene rimossa. Quando tutte le prenotazioni di un viaggio sono annullate, anche il viaggio viene rimosso.

## Eventi

Quando ricevi via email i biglietti per un concerto, una partita, un festival o una conferenza, la tua Machine aggiunge l’evento sotto **Eventi**, con una nota per ogni evento. Una riga indica dove si svolge e riporta il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto alla stessa nota. Come un viaggio, l’evento mostra le date e appare come una fascia in [Calendario](calendar.md) che apre la nota.

- Ogni riga indica da chi provengono i biglietti, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email dei biglietti è stata creata un’attività, per esempio per pagarli, **Apri l’attività** la mostra.
- Un evento prenotato con la tua casella di lavoro è Lavoro, altrimenti è Personale.

La tua Machine legge, senza usare l’AI, i dettagli dei biglietti che i venditori inseriscono nelle email di conferma. Un’email senza questi dettagli non crea un evento. Una prenotazione annullata viene rimossa; quando tutti i biglietti per un evento sono annullati, anche l’evento viene rimosso.

## Casa

Sotto **Casa**, la tua Machine raccoglie ciò che sa sulla tua casa: **Bollette e abbonamenti**, **Elettrodomestici**, **Riparazioni e manutenzione** e **La casa**. Una sezione appare quando contiene almeno due righe.

- Una bolletta ricorrente, come quella dell’elettricità o dell’acqua, compare con la frequenza e la data dell’ultima bolletta. **Apri l’attività** mostra la bolletta; l’importo e i dettagli del pagamento restano lì.
- Un abbonamento che hai mantenuto compare con una riga che apre la relativa attività **Abbonamenti**. Gli abbonamenti che hai annullato non vengono elencati.
- Anche ciò che la tua Machine ha imparato sulla tua casa, per esempio la marca della lavastoviglie, compare in una riga. Se la modifichi, la modifica viene applicata anche sotto **Ciò che ho imparato**.
- Se tieni una tua nota in una sezione, per esempio una nota sulla lavastoviglie sotto **Elettrodomestici**, le informazioni su quell’elemento vengono aggiunte alla tua nota. La tua Machine non crea autonomamente note di questo tipo.

Vengono usate solo le bollette e gli abbonamenti Personali, e le note di Casa sono sempre Personali. Per ogni nuova bolletta, abbonamento o informazione appresa, la tua Machine chiede una volta alla sua AI di stabilire se riguarda la tua casa. Per una bolletta, invia il mittente, mai l’importo.

## Salute

Sotto **Salute**, la tua Machine raccoglie ciò che sa sulla tua salute: **Appuntamenti**, **Medici e assistenza**, **Farmaci**, **Allergie e patologie** e **Fatture e assicurazione**. Una sezione appare quando contiene almeno due righe.

- Un appuntamento nel tuo calendario a cui vai solo tu, per esempio dal dentista, compare con la prossima data o con l’ultima. **Dal tuo calendario** lo apre.
- Una fattura di un medico, dentista o farmacia compare con una riga che apre la relativa attività. L’importo resta lì.
- Anche ciò che la tua Machine ha imparato sulla tua salute, per esempio un’allergia, compare in una riga. Se la modifichi, la modifica viene applicata anche sotto **Ciò che ho imparato**.
- Se hai una tua nota in una sezione, per esempio una nota sul fisioterapista sotto **Appuntamenti**, le informazioni su quell’elemento vengono aggiunte alla nota.

Le note di Salute sono sempre Personali, anche se una fattura è arrivata al tuo indirizzo di lavoro. Per ogni nuovo appuntamento, fattura o informazione appresa, la tua Machine chiede una volta alla sua AI di stabilire se riguarda la tua salute. Invia il nome dell’appuntamento, mai le note né i nomi degli altri invitati.

## Figli

Sotto **Figli**, la tua Machine raccoglie ciò che sa sui tuoi figli: **Scuola**, **Attività**, **Medici e assistenza** e **Bollette e commissioni**. Una sezione appare quando contiene almeno due righe.

- Ciò che la tua Machine ha imparato su tuo figlio, per esempio il nome dell’insegnante o il giorno di nuoto, compare in una riga collegata alla sua pagina. La tua Machine considera qualcuno tuo figlio se sotto **Per te** è indicato come tale, per esempio figlia o figlio.
- Un evento nel tuo calendario a cui vai solo tu, per esempio una riunione con gli insegnanti, compare con la prossima data o con l’ultima. **Dal tuo calendario** lo apre.
- Una fattura della scuola, di un’attività o dell’assistenza all’infanzia compare con una riga che apre la relativa attività. L’importo resta lì.
- Se hai una tua nota per un figlio in una sezione, per esempio una nota per Isla sotto **Scuola**, le informazioni su quel figlio vengono aggiunte alla nota.

Le note di Figli sono sempre Personali, anche se la scuola scrive al tuo indirizzo di lavoro. Per ogni nuova informazione, la tua Machine chiede una volta alla sua AI di stabilire se riguarda i tuoi figli.

## Unisci, elimina e annulla

Dal menu ⋯, **Unisci in…** sposta le righe di una nota e le note contenute al suo interno in un’altra nota. Da quel momento, la tua Machine aggiunge i nuovi contenuti a quella nota. **Elimina** rimuove una nota. Dopo entrambe le azioni, e dopo aver rimosso una riga, per qualche istante è disponibile **Annulla**.

## Non sono note delle riunioni

Le note delle riunioni e quelle associate a una persona o a un’organizzazione restano dove sono. Le note qui sono pagine a sé.
