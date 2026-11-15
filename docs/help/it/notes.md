---
title: Note
area: graph
summary: Una pagina chiara per ogni argomento, come un viaggio o la tua casa, collegata alle persone e ai progetti che ne fanno parte.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, folder_overview.py, memory_seed.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 1087ac0970878932
---
Una nota è una panoramica su un argomento: un viaggio, la tua casa, il modo in cui vengono gestite le fatture. Le note si trovano nel Graph, accanto a persone, organizzazioni e progetti. Restano sulla tua Machine e non vengono condivise con il tuo team.

## Crea una nota

In cima a Note, seleziona **Nuova nota**. Inserisci un titolo e seleziona **Inizia la nota** per aprire la pagina. Con **Aggiungi una riga** aggiungi ciò che vuoi conservare. Ogni riga di testo diventa una riga a sé.

## Collega persone, progetti e altre note

In una riga, digita @ e le prime lettere di un nome. Scegli una persona, un’organizzazione, un progetto o una nota dall’elenco: il nome verrà aggiunto come link. Nella pagina dell’elemento collegato compare **Collegato da** con la tua nota.

## Note sotto altre note

Una nota può trovarsi sotto un’altra, come Elettrodomestici sotto Casa. In Note le note sono organizzate ad albero: seleziona la freccia accanto a una nota per aprire quelle al suo interno. Per spostare una nota, seleziona **Modifica** e scegli dove collocarla sotto **Sotto**. Dal menu ⋯, seleziona **Nuova nota sotto questa** per crearne una lì.

In cima alla pagina di una nota trovi la sua posizione, ad esempio **Note › Figli**: tocca una parte qualsiasi per aprirla. Sul telefono, le note intermedie sono raccolte nel menu ⋯.

## Note create dalla tua Machine

La tua Machine crea anche note in autonomia a partire dai tuoi messaggi e le mantiene aggiornate. Ogni riga indica da dove proviene, ad esempio chi ha inviato l’email: toccala per aprire il messaggio. Una riga tratta da **Ciò che ho imparato** riporta **Da ciò che ho imparato**.

Una riunione o un appuntamento nel calendario non diventa mai una riga a sé: resta in [Calendario](calendar.md). Anche le relative email restano lì: l’invito, le risposte, gli aggiornamenti e le cancellazioni.

**Casa**, **Salute** e **Figli** compaiono solo quando la tua Machine ha almeno due informazioni concrete da mostrare, come una fattura o qualcosa che ha imparato. Fino ad allora non compaiono nell’elenco. Se in seguito non hanno più contenuti, scompaiono.

Le tue modifiche vengono sempre mantenute. Rinomina una nota, spostala, modifica le sue date o una riga: la tua Machine manterrà queste modifiche quando aggiornerà la nota. Se elimini una riga o una nota, non verrà ripristinata. Le note create in seguito sullo stesso argomento verranno inserite dove hai collocato la prima.

**Ripristina l’originale** mostra di nuovo le parole scelte dalla tua Machine. Se modifichi una riga basata su ciò che la tua Machine ha imparato, la modifica viene applicata anche a **Ciò che ho imparato**, così ne esiste una sola versione.

## Pagine scritte

Quando una nota contiene almeno due righe tratte dai tuoi messaggi o da ciò che la tua Machine ha imparato, la tua Machine scrive una pagina in cima alla nota. Legge le conversazioni, non solo i loro oggetti:

- Un breve riepilogo: di cosa si parla e a che punto è la situazione.
- **Fatti principali**, **Decisioni**, **Questioni aperte** e una **Cronologia**, ma solo quando ci sono informazioni concrete da riportare.
- Sotto **Fonti** trovi le righe della nota, numerate. Ogni frase termina con i numeri delle righe da cui proviene: tocca un numero per andare alla riga corrispondente.

La pagina viene riscritta solo quando cambiano le righe della nota, al massimo circa una volta al giorno. Se le fonti non contengono informazioni concrete, la pagina non viene creata e restano solo le righe. Quando rimuovi una riga, dalla pagina scompare anche ciò che proveniva solo da quella riga. Nell’elenco Note, sotto il nome della nota, trovi l’inizio del riepilogo della pagina.

Un progetto o un’organizzazione ha già una propria pagina nel Graph, con una descrizione in cima. Le conversazioni al riguardo vengono aggiunte a quella pagina, non a una nota.

## Panoramiche

Una nota che contiene altre note, come **Lavoro** o **Casa**, mostra una breve panoramica in cima quando almeno due delle note al suo interno hanno novità: una o due frasi su cosa sta succedendo e alcuni elementi che sono cambiati da poco o che verranno dopo. Alla fine di ogni elemento trovi i nomi delle note da cui proviene: toccane uno per aprire la nota.

La panoramica si basa sulle pagine e sulle righe più recenti delle note al suo interno. Viene aggiornata al massimo una volta al giorno, e solo quando ci sono cambiamenti. Se non ci sono novità, la panoramica non viene mostrata. Nell’elenco Note, sotto il nome della cartella, trovi l’inizio della panoramica.

## Note dalle tue conversazioni

La tua Machine legge le conversazioni complete e assegna ognuna alla nota pertinente: una conversazione email da una qualsiasi delle tue caselle, una chat in WhatsApp, Slack, Telegram, LinkedIn o un’altra app collegata, oppure gli appunti di una riunione. I messaggi di una chat contano come un’unica conversazione finché la chat non resta inattiva per due giorni.

- Una conversazione su un progetto o un’organizzazione nel tuo Graph viene aggiunta alla relativa pagina, non a una nuova nota.
- Una conversazione può essere aggiunta a una sezione di **Casa**, **Salute** o **Figli**, a una nota che hai creato tu oppure a una nota che la tua Machine crea sotto **Lavoro**, **Auto**, **Tasse** o un’altra cartella.
- La tua Machine crea una nuova nota solo per un argomento con almeno due conversazioni, oppure per un argomento su cui hai scritto e che è chiaramente ancora in corso.
- Ogni riga corrisponde a una conversazione, dalla più recente alla meno recente. Toccala per aprire la conversazione.

All’AI viene inviata una breve parte di ogni conversazione, senza le risposte citate né le firme. Ogni conversazione viene esaminata una volta; i nuovi messaggi che ne fanno parte vengono aggiunti in seguito.

Le email e le chat di massa non vengono mai aggiunte a una nota né inviate all’AI: spam, promozioni, newsletter e altre email di mailing list, notifiche automatiche, bot e canali di trasmissione. Una conversazione a cui hai partecipato conta comunque, così come le email di prenotazione per **Viaggi** ed **Eventi**.

La prima volta, la tua Machine esamina i tre mesi precedenti nell’arco di qualche ora, fuori dall’orario notturno e solo se il tuo piano AI ha spazio disponibile. In seguito, organizza le nuove conversazioni quando ce ne sono dieci in attesa, oppure quando una è in attesa da mezza giornata.

## Note dalla memoria di OpenClaw

Se hai già usato OpenClaw, la tua Machine legge una volta le pagine degli argomenti nella sua cartella della memoria, ad esempio una pagina su un viaggio o sulla tua salute. Le informazioni utili vengono aggiunte alla nota sull’argomento oppure a una nuova nota. Ogni riga indica la pagina di origine, ad esempio **Dalle tue pagine della memoria · Lisbona**, insieme alla sua data. Passaci sopra il cursore per vedere dove si trova quella pagina.

La tua Machine non modifica mai queste pagine e ignora i registri giornalieri, le pagine sull’assistente stesso e le cartelle contrassegnate come sensibili o private. Legge al massimo 80 pagine, poche alla volta, e non le legge più di una volta.

## Viaggi

Quando ricevi un’email di prenotazione per un volo, un hotel, un treno, un autobus, un traghetto o un’auto a noleggio, la tua Machine aggiunge il viaggio a una nota sotto **Viaggi**. Le prenotazioni dello stesso viaggio vengono raccolte in un’unica nota: l’andata, l’hotel e il ritorno. Per ogni riga del viaggio sono indicati il codice di prenotazione, il posto e il biglietto, in ordine cronologico; sono indicate anche le date del viaggio. In [Calendario](calendar.md), il viaggio compare come una fascia che copre quei giorni. Tocca la fascia per aprire il viaggio.

La tua Machine legge i dettagli di prenotazione che compagnie aeree, hotel e siti di prenotazione inseriscono nelle email di conferma. Un’email che non li contiene non crea un viaggio. Le email di prenotazione precedenti, comprese nell’anno della [cronologia](history.md) conservata dalla tua Machine, vengono esaminate in background una volta importata la cronologia, a partire dalle caselle email Personali. Se in seguito viene esaminata una conferma più vecchia, viene aggiunta al viaggio già esistente.

Se una prenotazione cambia, la relativa riga viene aggiornata. Se viene cancellata, la riga viene rimossa. Quando tutte le prenotazioni di un viaggio sono cancellate, anche il viaggio viene rimosso.

## Eventi

Quando ricevi via email i biglietti per un concerto, una partita, un festival o una conferenza, la tua Machine aggiunge l’evento sotto **Eventi**, con una nota per ogni evento. Una riga indica il luogo, il codice di prenotazione, il posto e il numero di biglietti. Un secondo ordine per lo stesso evento viene aggiunto alla stessa nota. Come per un viaggio, le date dell’evento sono indicate nella nota e l’evento compare come una fascia in [Calendario](calendar.md) che apre la nota.

- Ogni riga indica chi ha inviato i biglietti, ad esempio **Da Example Tickets**, e apre l’email.
- Se dall’email dei biglietti è stata creata un’attività, ad esempio pagare i biglietti, seleziona **Apri l’attività** per visualizzarla.
- Un evento prenotato nella casella di lavoro è di tipo Lavoro; negli altri casi è Personale.

La tua Machine legge i dettagli dei biglietti inseriti dai rivenditori nelle email di conferma, senza usare l’AI. Un’email che non contiene quei dettagli non crea un evento. Se una prenotazione viene cancellata, viene rimossa; quando tutti i biglietti di un evento sono cancellati, anche l’evento viene rimosso.

## Casa

Sotto **Casa**, la tua Machine conserva ciò che sa della tua abitazione: **Bollette e abbonamenti**, **Elettrodomestici**, **Riparazioni e manutenzione** e **La casa**. Una sezione compare quando contiene almeno due righe.

- Una bolletta ricorrente, come quella dell’energia o dell’acqua, viene aggiunta con la sua frequenza e la data dell’ultima bolletta. Seleziona **Apri l’attività** per visualizzare la bolletta; l’importo e i dettagli del pagamento restano lì.
- Un abbonamento che hai mantenuto viene aggiunto con una riga che apre la relativa attività **Abbonamenti**. Gli abbonamenti che hai cancellato non vengono elencati.
- Chi ti scrive regolarmente per la tua casa, ad esempio il fornitore di energia, il provider Internet o il comune, viene aggiunto con una riga che indica la frequenza dei messaggi. Toccala per aprire l’email più recente.
- Anche ciò che la tua Machine ha imparato sulla tua casa, ad esempio la marca della lavastoviglie, viene aggiunto come riga. Se lo modifichi, la modifica viene applicata anche a **Ciò che ho imparato**.
- Se hai una tua nota in una sezione, ad esempio una nota sulla lavastoviglie sotto **Elettrodomestici**, le informazioni su quell’elemento vengono aggiunte alla tua nota. La tua Machine non crea note di questo tipo in autonomia.

Vengono usate solo bollette, abbonamenti ed email Personali, e le note di Casa sono sempre Personali. Per ogni nuova bolletta, abbonamento o informazione appresa, la tua Machine chiede una volta all’AI di verificare se riguarda la tua casa. Per una bolletta, invia il mittente, mai l’importo.

Anche le tue conversazioni vengono aggiunte a queste note, come descritto sopra in **Note dalle tue conversazioni**.

## Salute

Sotto **Salute**, la tua Machine conserva ciò che sa sulla tua salute: **Appuntamenti**, **Risultati dei test**, **Medici e assistenza**, **Farmaci**, **Allergie e patologie** e **Fatture e assicurazione**. Una sezione compare quando contiene almeno due righe.

- Una fattura di un medico, dentista o farmacista viene aggiunta con una riga che apre la relativa attività. L’importo resta lì.
- Ogni email del tuo ambulatorio, di un ospedale, di un laboratorio o della tua assicurazione sanitaria viene aggiunta come riga datata con il suo oggetto, così la tua cronologia si arricchisce nel tempo. Toccala per aprire l’email.
- Anche ciò che la tua Machine ha imparato sulla tua salute, ad esempio un’allergia, viene aggiunto come riga. Se lo modifichi, la modifica viene applicata anche a **Ciò che ho imparato**.
- Una tua nota in una sezione, ad esempio una nota sul fisioterapista sotto **Appuntamenti**, raccoglie le informazioni su quell’elemento.

Le note di Salute sono sempre Personali, anche se una fattura è arrivata al tuo indirizzo di lavoro. Per ogni nuova fattura o informazione appresa, la tua Machine chiede una volta all’AI di verificare se riguarda la tua salute.

## Figli

Sotto **Figli**, la tua Machine conserva ciò che sa sui tuoi figli: **Scuola**, **Attività**, **Assistenza all'infanzia**, **Medici e assistenza** e **Bollette e commissioni**. Una babysitter o un asilo nido vengono inseriti in Assistenza all'infanzia, mai in Medici e assistenza. Una sezione compare quando contiene almeno due righe.

- Ciò che la tua Machine ha imparato su tuo figlio, ad esempio il nome del suo insegnante o il giorno in cui va a nuoto, viene aggiunto come riga collegata alla sua pagina. Una persona viene considerata tuo figlio se in **Per te** risulta essere tua figlia o tuo figlio.
- Una fattura della scuola, di un club o dell’assistenza all’infanzia viene aggiunta con una riga che apre la relativa attività. L’importo resta lì.
- Ogni email della scuola, di un club o dell’assistenza all’infanzia, ad esempio una comunicazione su una gita o un cambio di programma, viene aggiunta come riga datata con il suo oggetto, così trovi tutte le comunicazioni in un unico posto. Toccala per aprire l’email.
- Una tua nota per un figlio in una sezione, ad esempio una nota per Isla sotto **Scuola**, raccoglie le informazioni su quel figlio.

Le note di Figli sono sempre Personali, anche se la scuola scrive al tuo indirizzo di lavoro. Per ogni nuova informazione, la tua Machine chiede una volta all’AI di verificare se riguarda i tuoi figli.

## Unisci, elimina e annulla

Dal menu ⋯, seleziona **Unisci in…** per spostare le righe di una nota e le note al suo interno in un’altra nota. Da quel momento la tua Machine aggiungerà le nuove informazioni a quell’altra nota. Seleziona **Elimina** per rimuovere una nota. Dopo entrambe le azioni compare per qualche istante l’opzione **Annulla**, che compare anche quando rimuovi una riga.

## Non sono appunti delle riunioni

Gli appunti delle riunioni e le note su una persona o un’organizzazione restano al loro posto. Le note qui sono pagine a sé.
