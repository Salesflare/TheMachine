---
title: Note
area: graph
summary: Una pagina chiara per ogni argomento, come un viaggio o la tua casa, collegata alle persone e ai progetti che ne fanno parte.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 336e0f0dad44f19a
---
Una nota è una panoramica su un argomento: un viaggio, la tua casa, come si gestiscono le fatture. Le note si trovano nel Graph, accanto a Persone, Organizzazioni e Progetti. Restano sulla tua Machine e non vengono condivise con il tuo team.

## Crea una nota

Tocca **Nuova nota** in alto in Note. Assegna un titolo e tocca **Inizia la nota** per aprire la pagina. Con **Aggiungi una riga** aggiungi ciò che vuoi conservare. Ogni riga di testo diventa una riga a sé.

## Collega persone, progetti e altre note

In una riga, digita @ e alcune lettere di un nome. Scegli una persona, un’organizzazione, un progetto o una nota dall’elenco: il nome verrà inserito come link. Nella pagina dell’elemento collegato, sotto **Collegato da**, vedrai la tua nota.

## Note sotto altre note

Una nota può trovarsi sotto un’altra, per esempio Elettrodomestici sotto Casa. In Note, le note sono disposte ad albero: tocca la freccia accanto a una nota per aprire quelle sotto di essa. Per spostare una nota, tocca **Modifica** e scegli dove collocarla in **Sotto**. Nel menu ⋯, **Nuova nota sotto questa** crea una nota proprio lì.

In cima alla pagina di una nota è indicato dove si trova, per esempio **Note › Figli**: tocca una qualsiasi parte per aprirla. Sul telefono, le note intermedie sono raccolte nel menu ⋯.

## Note create dalla tua Machine

La tua Machine scrive anche note in autonomia, a partire dai tuoi messaggi, e le mantiene aggiornate. Ogni riga indica da dove proviene, per esempio chi ha inviato l’email: toccala per aprire il messaggio. Una riga tratta da **Ciò che ho imparato** riporta **Da ciò che ho imparato**. Una riunione o un appuntamento in calendario non diventa mai una riga a sé: resta in [Calendario](calendar.md).

**Casa**, **Salute** e **Figli** compaiono solo quando la tua Machine ha almeno due informazioni concrete da aggiungere, come una bolletta o qualcosa che ha imparato. Fino ad allora non appaiono nell’elenco. Se poi restano vuote, vengono rimosse.

Le tue modifiche vengono sempre mantenute. Rinomina una nota, spostala, cambia le date o una riga: quando la aggiorna, la tua Machine la lascia così. Se elimini una riga o una nota, non viene ripristinata. Le note aggiunte in seguito sullo stesso argomento finiscono dove hai collocato la prima.

**Ripristina l’originale** mostra di nuovo il testo originale della tua Machine. Se modifichi una riga che deriva da ciò che ha imparato, la modifica viene applicata anche in **Ciò che ho imparato**, così ne esiste una sola versione.

## Viaggi

Quando riceve un’email con la prenotazione di un volo, un hotel, un treno, un autobus, un traghetto o un’auto a noleggio, la tua Machine la aggiunge a un viaggio in **Viaggi**. Le prenotazioni dello stesso viaggio finiscono tutte nello stesso viaggio: l’andata, l’hotel e il ritorno. Il viaggio riporta il codice di prenotazione, il posto e il biglietto di ogni riga, in ordine cronologico, oltre alle date. In [Calendario](calendar.md) è mostrato come una fascia che copre quei giorni e, toccandola, si apre il viaggio.

La tua Machine legge i dettagli delle prenotazioni inseriti da compagnie aeree, hotel e siti di prenotazione nelle email di conferma. Un’email senza questi dettagli non crea un viaggio. Le email di prenotazione ricevute in passato, durante l’anno di [cronologia](history.md) conservato dalla tua Machine, vengono lette in background dopo che la cronologia è stata caricata, a partire dalle caselle email personali. Una conferma più vecchia letta in seguito viene aggiunta al viaggio già esistente.

Se una prenotazione cambia, la relativa riga viene aggiornata. Se viene annullata, la riga viene rimossa. Quando tutte le prenotazioni di un viaggio sono annullate, viene rimosso anche il viaggio.

## Eventi

Quando riceve un’email con i biglietti per un concerto, una partita, un festival o una conferenza, la tua Machine aggiunge l’evento in **Eventi**, con una nota per ciascun evento. Una riga indica dove si svolge l’evento e riporta il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto alla stessa nota. Come per un viaggio, l’evento riporta le date e appare come una fascia in [Calendario](calendar.md), che apre la nota.

- Ogni riga indica chi ha inviato i biglietti, per esempio **Da Example Tickets**, e apre l’email.
- Se dall’email dei biglietti è stata creata un’attività, per esempio pagare i biglietti, **Apri l’attività** la mostra.
- Un evento prenotato nella casella email di lavoro è classificato come Lavoro, altrimenti come Personale.

La tua Machine legge i dettagli dei biglietti inseriti dai venditori nelle email di conferma, senza usare l’AI. Un’email senza questi dettagli non crea un evento. Se una prenotazione viene annullata, viene rimossa. Quando tutti i biglietti per un evento sono annullati, viene rimosso anche l’evento.

## Casa

In **Casa**, la tua Machine conserva ciò che sa sulla tua casa: **Bollette e abbonamenti**, **Elettrodomestici**, **Riparazioni e manutenzione** e **La casa**. Una sezione compare quando contiene almeno due righe.

- Una bolletta ricorrente, per esempio di luce o acqua, ha una riga che indica ogni quanto arriva e la data dell’ultima. **Apri l’attività** mostra la bolletta; l’importo e i dettagli del pagamento restano lì.
- Un abbonamento che hai mantenuto ha una riga che apre la relativa attività in **Abbonamenti**. Gli abbonamenti annullati non vengono mostrati.
- Chi ti scrive regolarmente per la casa, per esempio il fornitore di energia, il gestore Internet o il comune, ha una riga che indica ogni quanto scrive. Toccala per aprire l’email più recente.
- Anche ciò che la tua Machine ha imparato sulla tua casa, per esempio la marca della lavastoviglie, ha una riga. Se la modifichi, cambia anche in **Ciò che ho imparato**.
- Se in una sezione hai una tua nota, per esempio una nota sulla lavastoviglie in **Elettrodomestici**, le informazioni su quell’elemento vengono inserite nella tua nota. La tua Machine non crea autonomamente note di questo tipo.

Vengono usate solo bollette, abbonamenti ed email personali, e le note di Casa sono sempre personali. Per ogni nuova bolletta, abbonamento o informazione appresa, la tua Machine chiede una volta alla sua AI se riguarda la tua casa. Per una bolletta invia il mittente, mai l’importo.

Per **Casa**, **Salute** e **Figli** insieme, la tua Machine chiede inoltre una volta alla sua AI informazioni su ogni mittente delle tue email personali. Invia il nome del mittente, il numero di email che ha inviato e gli oggetti delle più recenti, con i numeri nascosti. Non invia mai il contenuto delle email. Se un’email è arrivata due volte o in due delle tue caselle, viene conteggiata una volta sola. Lo stesso vale per una risposta con lo stesso oggetto nella conversazione.

Le email di massa non vengono mai aggiunte a queste note e non vengono mai inviate all’AI: spam, promozioni, newsletter e altri messaggi di mailing list, oltre alle notifiche automatiche. Le email in una conversazione a cui hai risposto vengono comunque conteggiate, così come le email di prenotazione per **Viaggi** ed **Eventi**.

La prima volta, la tua Machine esamina le email dell’ultimo anno in poche ore, non di notte e solo quando il tuo piano AI ha spazio disponibile. In seguito controlla i nuovi mittenti ogni sei ore.

## Salute

In **Salute**, la tua Machine conserva ciò che sa sulla tua salute: **Appuntamenti**, **Risultati dei test**, **Medici e assistenza**, **Farmaci**, **Allergie e patologie** e **Fatture e assicurazione**. Una sezione compare quando contiene almeno due righe.

- Una fattura di un medico, dentista o farmacista ha una riga che apre la relativa attività. L’importo resta lì.
- Ogni email del tuo ambulatorio, di un ospedale, di un laboratorio o della tua assicurazione sanitaria diventa una riga con la data e l’oggetto, così la tua cronologia si arricchisce nel tempo. Toccala per aprire l’email.
- Anche ciò che la tua Machine ha imparato sulla tua salute, per esempio un’allergia, ha una riga. Se la modifichi, cambia anche in **Ciò che ho imparato**.
- Se hai una tua nota in una sezione, per esempio una nota sul tuo fisioterapista in **Appuntamenti**, le informazioni su quell’elemento vengono inserite lì.

Le note di Salute sono sempre personali, anche quando una fattura è arrivata al tuo indirizzo di lavoro. Per ogni nuova fattura o informazione appresa, la tua Machine chiede una volta alla sua AI se riguarda la tua salute.

## Figli

In **Figli**, la tua Machine conserva ciò che sa sui tuoi figli: **Scuola**, **Attività**, **Assistenza all'infanzia**, **Medici e assistenza** e **Bollette e commissioni**. Una babysitter o un asilo nido rientrano in Assistenza all'infanzia, mai in Medici e assistenza. Una sezione compare quando contiene almeno due righe.

- Ciò che la tua Machine ha imparato su un figlio, per esempio il nome del suo insegnante o il giorno di nuoto, ha una riga collegata alla sua pagina. La tua Machine considera qualcuno tuo figlio quando in **Per te** è indicato come tale, per esempio figlia o figlio.
- Una fattura della scuola, di un club o dell’assistenza all’infanzia ha una riga che apre la relativa attività. L’importo resta lì.
- Ogni email della scuola, di un club o dell’assistenza all’infanzia, per esempio una comunicazione su una gita o un cambio di programma, diventa una riga con la data e l’oggetto, così trovi tutti i messaggi in un unico posto. Toccala per aprire l’email.
- Se hai una tua nota per un figlio in una sezione, per esempio una nota per Isla in **Scuola**, le informazioni su quel figlio vengono inserite lì.

Le note di Figli sono sempre personali, anche quando la scuola scrive al tuo indirizzo di lavoro. Per ogni nuova informazione, la tua Machine chiede una volta alla sua AI se riguarda i tuoi figli.

## Unisci, elimina e annulla

Nel menu ⋯, **Unisci in…** sposta le righe di una nota e le note contenute al suo interno in un’altra nota. Da quel momento, la tua Machine aggiunge le nuove informazioni a quella nota. **Elimina** rimuove una nota. Per entrambe le azioni, e anche quando rimuovi una riga, puoi toccare **Annulla** per qualche istante.

## Non sono note delle riunioni

Le note delle riunioni e quelle su una persona o un’organizzazione restano dove sono. Le note qui sono pagine a sé.
