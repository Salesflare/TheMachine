---
title: Amici e Network
area: fleet
summary: Aggiungi amici tramite nome utente, trova persone che conosci e che hanno una Machine e abbina una Machine sul tuo computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 3565b3898b234575
---
## Amici

Aggiungi qualcuno inserendo il suo nome utente esatto, nella scheda **Fleet**, sotto Amici. Gli amici possono chiedere chi conosce una persona, avere informazioni utili per le riunioni e presentazioni tramite conoscenze comuni, e vedere quando sei impegnato (solo gli orari, mai i dettagli). Puoi rimuovere o bloccare un amico in qualsiasi momento.

## Trova le persone che conosci

In **Fleet**, sotto **Network**:

- «Controlla quali dei miei contatti hanno una Machine» ti suggerisce persone che conosci.
- «Permetti a chi ha la mia email di trovarmi» permette agli altri di trovarti.

Entrambe le opzioni sono attive per impostazione predefinita e disattivate al livello di sicurezza Careful. Puoi disattivare una delle due in qualsiasi momento; la scelta resta salvata. Le persone possono trovarti tramite l’email che usi per accedere (sempre attiva) e gli indirizzi collegati, ognuno con il proprio interruttore sotto **Trovabile da**. Gli indirizzi condivisi, come info@, restano disattivati finché non li attivi.

Le persone che conosci compaiono subito quando attivi l’opzione, e anche quando si iscrivono in seguito. Per ognuna puoi scegliere Connetti, Non ora o **Non suggerire mai**. Una volta diventati amici, non riceverai più suggerimenti. Con **Lascia il Network** esci dal Network.

Nella tua lista Persone, quelle trovate mostrano **Ha una Machine**. Il sistema controlla gli indirizzi presenti nei tuoi messaggi e quelli che hai aggiunto a una persona con **Modifica**. Se qualcuno si è iscritto con un altro indirizzo, aggiungilo alla persona. Nella pagina di una persona trovata, **Aggiungi come amico** invia la stessa richiesta di Connetti (**Aggiungi come famiglia** si trova nel menu ⋯).

Per chi non ha una Machine, compare **Invita su The Machine**. Si apre l’email che riceverà, nella schermata **Inviare questa email?**. È la stessa email usata per qualsiasi attività e puoi modificarla. Non viene inviata finché non premi **Invia ora**. Se chiudi la schermata, l’invito resta tra le attività. Se non hai una casella da cui inviare: **Copia** o **Apri nella tua email**.

Contano anche i numeri di telefono: quelli nelle chat di WhatsApp con persone a cui hai scritto o che hai incontrato, e quelli che hai aggiunto con **Modifica**. Il tuo numero WhatsApp collegato e i numeri inseriti nella sezione Informazioni su di te ti rendono trovabile, ciascuno con il proprio interruttore sotto **Trovabile da**. Un numero permette di trovare qualcuno solo se anche quella persona ti ha cercato o se siete amici. Così nessuno può provare numeri a caso per vedere chi ha una Machine.

## Pianifica con altre Machine

Quando una persona con una Machine scrive «vediamoci la settimana prossima», la tua Machine chiede alla sua quali orari hai liberi e ne trova uno che vada bene a entrambi, all’interno del tuo orario di lavoro. Ognuno riceve un’attività, ad esempio «Incontra Alex Example», con l’orario indicato sotto. Tocca **Prenota**, **Altro orario** o **Non serve**. L’invito viene inviato solo dopo che entrambi avete toccato Prenota.

Vengono condivise solo le fasce libere o occupate, con crittografia end-to-end, per un massimo di 14 giorni e arrotondate a intervalli di 15 minuti. Gli eventi privati risultano occupati. Una Machine può fare una richiesta solo se vi siete scambiati email in entrambe le direzioni. Configura l’opzione in **Cosa possono chiedere altre Machine alla mia**: **Libero/occupato per pianificare** o **Disattivata**, insieme alla durata delle riunioni, al tempo di margine e agli orari preferiti. Ogni richiesta compare in Attività, sotto Calendario.

Se l’altra persona non ha una Machine o non risponde, la bozza dell’email include un link per scegliere uno dei tuoi orari liberi. La sua scelta diventa un’attività con **Prenota**. Non viene prenotato nulla finché non la tocchi.

Il link mostra solo gli orari liberi, secondo le stesse regole, e nessun’altra informazione su di te. Scade quando la riunione viene prenotata o dopo 14 giorni. Nell’email appare come «Scegli un orario». In fondo alla pagina compare «La tua Machine ha trovato questi orari. Ottieni la tua.» seguito dal tuo nome. Puoi disattivarlo con **Piè di pagina nei link di prenotazione**. Ogni link e ogni scelta compaiono in Attività.

## Una Machine sul tuo computer

Per unirti al Network da una Machine che gestisci tu:

1. Nella dashboard della tua Machine, apri **Impostazioni** e premi **Unisciti al Network**.
2. Nella pagina che si apre, accedi (o crea un account) e conferma. La tua Machine la rileva automaticamente, senza riavviarsi.

Puoi ancora usare il metodo con il codice: premi **Abbina una Machine self-hosted** nella pagina del tuo account su app.themachine.computer, poi esegui `assistant fleet-pair` con il codice sul tuo computer e riavvia. Il codice può essere usato una sola volta e scade dopo 15 minuti.

Puoi avere fino a 5 Machine per account. Puoi disconnetterle dalla stessa pagina.
