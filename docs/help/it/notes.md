---
title: Note
area: graph
summary: Una pagina chiara per ogni argomento, come un viaggio o la tua casa, collegata alle persone e ai progetti che ne fanno parte.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 8e27b2c69f77196d
---
Una nota offre una panoramica su un argomento: un viaggio, la tua casa, come gestire le fatture. Le note si trovano nel Graph, insieme a persone, organizzazioni e progetti. Restano sulla tua Machine e non vengono condivise con il tuo team.

## Crea una nota

Tocca **Nuova nota** in cima a Note. Scegli un titolo e tocca **Inizia la nota** per aprire la pagina. Con **Aggiungi una riga** puoi aggiungere ciò che vuoi conservare. Ogni riga di testo diventa una riga a sé.

## Collega persone, progetti e altre note

In una riga, digita @ e le prime lettere di un nome. Scegli una persona, un’organizzazione, un progetto o una nota dall’elenco: il nome verrà inserito come link. Nella pagina dell’elemento collegato, sotto **Collegato da**, comparirà la tua nota.

## Note sotto altre note

Una nota può trovarsi sotto un’altra, per esempio Elettrodomestici sotto Casa. In Note le note sono organizzate ad albero: tocca la freccia accanto a una nota per aprire quelle che contiene. Per spostare una nota, tocca **Modifica** e scegli dove collocarla sotto **Sotto**. Dal menu ⋯, tocca **Nuova nota sotto questa** per crearne una lì.

In cima alla pagina di una nota trovi il percorso, per esempio **Note › Figli**: tocca una qualsiasi parte per aprirla. Sul telefono, le note intermedie sono raccolte nel menu ⋯.

## Note create dalla tua Machine

La tua Machine crea anche note dai tuoi messaggi e le mantiene aggiornate. Ogni riga indica da dove proviene, per esempio chi ha inviato l’email: toccala per aprire il messaggio. Una riga tratta da **Ciò che ho imparato** riporta **Da ciò che ho imparato**. Una riunione o un appuntamento nel calendario non compare mai come riga a sé: resta in [Calendario](calendar.md).

**Casa**, **Salute** e **Figli** compaiono solo quando la tua Machine ha almeno due informazioni concrete da mostrare, come una bolletta o qualcosa che ha imparato. Fino ad allora non appaiono nell’elenco. Se poi restano senza informazioni, scompaiono.

Le tue modifiche vengono sempre mantenute. Rinomina una nota, spostala, modifica le date o una riga: quando la nota viene aggiornata, la tua Machine conserva le modifiche. Se elimini una riga o una nota, non viene ripristinata. Le note successive sullo stesso argomento vengono aggiunte dove hai messo la prima.

**Ripristina l’originale** mostra di nuovo le parole usate dalla tua Machine. Se modifichi una riga tratta da ciò che la tua Machine ha imparato, la modifica viene applicata anche in **Ciò che ho imparato**, così ne esiste una sola versione.

## Viaggi

Quando ricevi un’email con una prenotazione di volo, hotel, treno, autobus, traghetto o auto a noleggio, la tua Machine la aggiunge a un viaggio sotto **Viaggi**. Le prenotazioni dello stesso itinerario vengono raccolte in un unico viaggio: andata, hotel e ritorno. Per ogni riga, il viaggio mostra il codice di prenotazione, il posto e il biglietto, in ordine cronologico, oltre alle date. In [Calendario](calendar.md) appare come una fascia che copre quei giorni. Tocca la fascia per aprire il viaggio.

La tua Machine legge i dettagli delle prenotazioni presenti nelle email di conferma inviate da compagnie aeree, hotel e siti di prenotazione. Un’email senza questi dettagli non crea un viaggio. Le email di prenotazione ricevute in precedenza, durante l’anno di [cronologia](history.md) conservato dalla tua Machine, vengono lette in background dopo che la cronologia è stata importata, iniziando dalle caselle di posta Personali.

Se una prenotazione viene modificata, la riga viene aggiornata; se viene annullata, viene rimossa. Quando vengono annullate tutte le prenotazioni di un viaggio, anche il viaggio viene rimosso.

## Eventi

Quando ricevi via email biglietti per un concerto, una partita, un festival o una conferenza, la tua Machine aggiunge l’evento sotto **Eventi**, creando una nota per ogni evento. Una riga indica il luogo e riporta il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto alla stessa nota. Come per un viaggio, l’evento mostra le date e appare come una fascia in [Calendario](calendar.md), da cui puoi aprire la nota.

- Ogni riga indica da chi provengono i biglietti, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email dei biglietti è stata creata un’attività, per esempio pagare i biglietti, **Apri l’attività** la mostra.
- Un evento prenotato dalla casella di posta di lavoro è di Lavoro; altrimenti è Personale.

La tua Machine legge i dettagli dei biglietti presenti nelle email di conferma inviate dai rivenditori, senza usare l’AI. Un’email senza questi dettagli non crea un evento. Se una prenotazione viene annullata, viene rimossa. Quando vengono annullati tutti i biglietti di un evento, anche l’evento viene rimosso.

## Casa

Sotto **Casa**, la tua Machine conserva ciò che sa sulla tua casa: **Bollette e abbonamenti**, **Elettrodomestici**, **Riparazioni e manutenzione** e **La casa**. Una sezione compare quando contiene almeno due righe.

- Una bolletta ricorrente, per esempio di luce o acqua, viene aggiunta con la frequenza con cui arriva e la data dell’ultima bolletta. **Apri l’attività** mostra la bolletta; l’importo e i dettagli di pagamento restano lì.
- Un abbonamento che hai mantenuto viene aggiunto con una riga che apre la relativa attività in **Abbonamenti**. Gli abbonamenti annullati non vengono elencati.
- Chi ti scrive regolarmente per questioni legate alla casa, per esempio il fornitore di energia, il provider Internet o il Comune, viene indicato con la frequenza con cui ti scrive. Tocca la riga per aprire la sua email più recente.
- Anche ciò che la tua Machine ha imparato sulla casa, per esempio la marca della lavastoviglie, viene aggiunto come riga. Se lo modifichi, la modifica viene applicata anche in **Ciò che ho imparato**.
- Se hai una tua nota in una sezione, per esempio una nota sulla lavastoviglie sotto **Elettrodomestici**, le informazioni su quell’elettrodomestico vengono aggiunte alla tua nota. La tua Machine non crea da sé note di questo tipo.

Vengono usate solo bollette, abbonamenti ed email Personali. Le note di Casa sono sempre Personali. Per ogni nuova bolletta, abbonamento o informazione appresa, la tua Machine chiede una volta alla sua AI di verificare se riguarda la tua casa. Per una bolletta invia il nome del mittente, mai l’importo.

Per **Casa**, **Salute** e **Figli**, la tua Machine chiede inoltre una volta alla sua AI di valutare ogni mittente delle tue email Personali. Invia il nome del mittente, il numero di email inviate e gli oggetti delle email più recenti, nascondendo i numeri. Non invia mai le email stesse.

La prima volta, esamina le email dell’ultimo anno nel giro di qualche ora, fuori dalle ore notturne e solo quando il tuo piano AI ha capacità disponibile. In seguito, controlla i nuovi mittenti ogni sei ore.

## Salute

Sotto **Salute**, la tua Machine conserva ciò che sa sulla tua salute: **Appuntamenti**, **Risultati dei test**, **Medici e assistenza**, **Farmaci**, **Allergie e patologie** e **Fatture e assicurazione**. Una sezione compare quando contiene almeno due righe.

- Una fattura di un medico, dentista o farmacia viene aggiunta con una riga che apre la relativa attività. L’importo resta lì.
- Ogni email del tuo ambulatorio, di un ospedale, di un laboratorio o della tua assicurazione sanitaria viene aggiunta come riga datata con il suo oggetto, così la tua cronologia si arricchisce nel tempo. Tocca la riga per aprire l’email.
- Anche ciò che la tua Machine ha imparato sulla tua salute, per esempio un’allergia, viene aggiunto come riga. Se lo modifichi, la modifica viene applicata anche in **Ciò che ho imparato**.
- Le informazioni sulla tua nota personale in una sezione, per esempio una nota sul tuo fisioterapista sotto **Appuntamenti**, vengono aggiunte a quella nota.

Le note di Salute sono sempre Personali, anche quando una fattura arriva al tuo indirizzo di lavoro. Per ogni nuova fattura o informazione appresa, la tua Machine chiede una volta alla sua AI di verificare se riguarda la tua salute.

## Figli

Sotto **Figli**, la tua Machine conserva ciò che sa sui tuoi figli: **Scuola**, **Attività**, **Assistenza all'infanzia**, **Medici e assistenza** e **Bollette e commissioni**. Babysitter e asilo nido vengono inseriti sotto Assistenza all’infanzia, mai sotto Medici e assistenza. Una sezione compare quando contiene almeno due righe.

- Ciò che la tua Machine ha imparato su tuo figlio, per esempio il nome dell’insegnante o il giorno di nuoto, viene aggiunto come riga collegata alla sua pagina. Considera una persona come tuo figlio quando nella sezione **Per te** è indicato quel rapporto, per esempio figlia o figlio.
- Una fattura della scuola, di un’associazione o del servizio di assistenza all’infanzia viene aggiunta con una riga che apre la relativa attività. L’importo resta lì.
- Ogni email della scuola, di un’associazione o del servizio di assistenza all’infanzia, per esempio la lettera settimanale o un avviso su una gita, viene aggiunta come riga datata con il suo oggetto, così trovi tutto quello che ti inviano in un unico posto. Tocca la riga per aprire l’email.
- Le informazioni sulla tua nota personale per un figlio in una sezione, per esempio una nota su Isla sotto **Scuola**, vengono aggiunte a quella nota.

Le note di Figli sono sempre Personali, anche quando la scuola scrive al tuo indirizzo di lavoro. Per ogni nuova informazione, la tua Machine chiede una volta alla sua AI di verificare se riguarda i tuoi figli.

## Unisci, elimina e annulla

Dal menu ⋯, **Unisci in…** sposta le righe di una nota e le note al suo interno in un’altra nota. Da quel momento, la tua Machine aggiunge le nuove informazioni a quella nota. **Elimina** rimuove una nota. Entrambe le azioni mostrano **Annulla** per qualche istante, così come la rimozione di una riga.

## Non sono note di riunione

Le note di riunione e quelle relative a una persona o a un’organizzazione restano dove si trovavano. Le note qui sono pagine indipendenti.
