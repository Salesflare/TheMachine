---
title: Amici e Network
area: fleet
summary: Aggiungi amici usando il loro nome utente esatto, trova persone che conosci e che hanno una Machine e abbina una Machine sul tuo computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 637784bf811800bb
---
## Amici

Aggiungi qualcuno usando il suo nome utente esatto, nella scheda **Fleet**, sotto Amici. Gli amici possono chiedere chi conosce una persona, ricevere informazioni sugli incontri e presentazioni tramite conoscenze comuni, e vedere quando hai impegni (solo gli orari, mai il motivo). Puoi rimuovere o bloccare un amico quando vuoi.

## Trova le persone che conosci

In **Fleet**, sotto **Network**:

- **Controlla quali dei miei contatti hanno una Machine** suggerisce persone che conosci.
- **Lascia che mi trovi chi ha la mia email** consente agli altri di trovarti.

Entrambe le opzioni sono attive per impostazione predefinita e disattivate al livello di sicurezza Prudente. Puoi disattivarle quando vuoi; la tua scelta viene salvata. Le persone possono trovarti usando l’email con cui accedi (sempre attiva) e gli indirizzi che hai collegato, ognuno con il proprio interruttore sotto **Trovabile da**, tranne quelli condivisi, come info@, che restano disattivati finché non li attivi.

Quando attivi questa opzione, le persone che conosci compaiono subito come attività, e così anche quelle che si iscrivono in seguito. Per ognuna puoi scegliere **Amico** e **Famiglia** (**Collegati** per un collega), **Non ora** e **Non suggerire mai** nel menu ⋯. Una volta diventati amici, non ti verranno più suggeriti. **Lascia il Network** ti rimuove dal Network.

Le persone che trova vengono indicate con **Ha una Machine** nell’elenco Persone. La ricerca controlla gli indirizzi nei tuoi messaggi e quelli che hai aggiunto alla scheda di una persona con **Modifica**: se qualcuno si è iscritto con un altro indirizzo, aggiungilo alla sua scheda. Nella pagina di una persona trovata, **Aggiungi come amico** invia la stessa richiesta di Collegati (**Aggiungi come famiglia** si trova nel menu ⋯).

Per chi non ha una Machine, trovi **Invita su The Machine**: si apre l’email che riceverà, in **Inviare questa email?**, come per qualsiasi attività. Se vuoi, puoi modificarla. L’email non parte finché non selezioni **Invia ora**. Se chiudi la finestra, l’invito resta come attività. Se non hai una casella email da cui inviare: **Copia** o **Apri nella tua email**.

Puoi trovare anche persone tramite il numero di telefono: vengono controllati i numeri delle chat WhatsApp con persone a cui hai scritto o che hai incontrato, e quelli che hai aggiunto con **Modifica**. Il tuo numero WhatsApp collegato e i numeri in Su di te ti rendono trovabile, ognuno con il proprio interruttore sotto **Trovabile da**. Un numero permette di trovare qualcuno solo se anche quella persona ti ha cercato o se siete amici, così nessuno può provare numeri a caso per vedere chi ha una Machine.

## Pianificare con altre Machine

Quando qualcuno con una Machine scrive «vediamoci la prossima settimana», la tua Machine chiede alla sua quali orari liberi ha e ne trova uno che vada bene a entrambi, durante il tuo orario di lavoro. Riceverete entrambi un’attività, per esempio «Incontra Alex Example», con l’orario indicato sotto. Seleziona **Prenota**, **Altro orario** o **Non serve**. L’invito parte solo dopo che entrambi avete selezionato Prenota.

Vengono condivisi solo gli orari libero/occupato, protetti con crittografia end-to-end, per un massimo di 14 giorni e arrotondati a intervalli di 15 minuti. Gli eventi privati risultano come occupati. Una Machine può fare una richiesta solo se vi siete scambiati email in entrambe le direzioni. Imposta questa opzione in **Cosa possono chiedere altre Machine alla mia**: **Libero/occupato per pianificare** o **Disattivata**, insieme alla durata degli incontri, all’intervallo tra uno e l’altro e agli orari preferiti. Ogni richiesta compare in **Movimenti**, sotto **Calendario**.

Se l’altra persona non ha una Machine o non risponde, la bozza dell’email include un link che le permette di scegliere uno dei tuoi orari liberi. La sua scelta diventa un’attività con **Prenota**; la prenotazione non viene effettuata finché non la selezioni.

Il link mostra solo gli orari liberi, secondo le stesse regole, e nessun’altra informazione su di te. Scade quando l’incontro viene prenotato o dopo 14 giorni. Nell’email compare come «Scegli un orario». In fondo alla pagina compare «La Machine di Alex ha trovato questi orari. Ottieni la tua.», con il tuo nome. Puoi disattivare questa opzione con **Piè di pagina nei link di prenotazione**. Ogni link e ogni scelta compaiono in **Movimenti**.

## Una Machine sul tuo computer

Per unirti al Network con una Machine che gestisci tu:

1. Nella dashboard della tua Machine, apri **Impostazioni** e seleziona **Unisciti al Network**.
2. Nella pagina che si apre, accedi (o crea un account) e conferma. La tua Machine si collega da sola, senza riavviarsi.

Puoi continuare a usare il metodo con il codice: seleziona **Abbina una Machine self-hosted** nella pagina del tuo account su app.themachine.computer, poi esegui `assistant fleet-pair` con il codice sul tuo computer e riavvia. Il codice è valido una sola volta, per 15 minuti.

Puoi avere fino a 5 Machine per account. Da quella pagina puoi scollegare ognuna.
