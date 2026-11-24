---
title: Amici e Network
area: fleet
summary: Aggiungi amici con il loro nome utente esatto, trova persone che conosci e che hanno una Machine e abbina una Machine sul tuo computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 70a39b4999d112b7
---
## Amici

Aggiungi una persona usando il suo nome utente esatto, nella scheda **Fleet**, sotto Amici. Gli amici possono chiedere chi conosce qualcuno, ricevere contesto sugli incontri e presentazioni tramite conoscenze comuni, e vedere quando hai impegni (solo gli orari impegnati, mai i dettagli). I giorni che il calendario non mostra risultano sconosciuti, mai liberi. Puoi rimuovere o bloccare una persona amica in qualsiasi momento.

## Trova persone che conosci

In **Fleet**, sotto **Network**:

- «Controlla quali dei miei contatti hanno una Machine» suggerisce persone che conosci.
- «Consenti alle persone che hanno la mia email di trovarmi» permette loro di trovarti.

Entrambe le opzioni sono attive per impostazione predefinita e disattivate al livello di sicurezza Prudente. Puoi disattivare una delle due in qualsiasi momento; la tua scelta viene mantenuta. Le persone possono trovarti tramite l'email di accesso (sempre attiva) e gli indirizzi collegati, ognuno con il proprio interruttore in **Trovabile da**, tranne quelli condivisi, come info@, che restano disattivati finché non li attivi.

Quando attivi questa opzione, le persone che conosci ti vengono proposte subito come attività e anche quando si iscrivono in seguito. Per ognuna trovi **Amico** e **Famiglia** (**Collega** per un collega), **Non ora** e **Non suggerire mai** nel menu ⋯. Una volta che siete amici, non ti verrà più suggerita. **Lascia il Network** ti rimuove dal Network.

Le persone che trova compaiono nell'elenco Persone con l'etichetta **Ha una Machine**. La ricerca controlla gli indirizzi nei tuoi messaggi e quelli che hai aggiunto a una persona con **Modifica**. Se qualcuno si è registrato con un altro indirizzo, aggiungilo al suo profilo. Nella pagina di una persona trovata, **Aggiungi come amico** invia la stessa richiesta di Collega (**Aggiungi come famiglia** si trova nel menu ⋯).

Per chi non ha una Machine compare **Invita su The Machine**: si apre l'email che riceverà, in **Inviare questa email?**, la stessa usata per qualsiasi attività, che puoi modificare. Non viene inviata finché non selezioni **Invia ora**. Se chiudi la finestra, l'invito resta tra le attività. Se non hai una casella di posta da cui inviare: **Copia** o **Apri nella tua email**.

Puoi usare anche i numeri di telefono: quelli delle chat WhatsApp con le persone a cui hai scritto o che hai incontrato, e quelli che hai aggiunto con **Modifica**. Il numero WhatsApp collegato e i numeri indicati in Informazioni su di te ti rendono trovabile, ciascuno con il proprio interruttore in **Trovabile da**. Un numero permette di trovare qualcuno solo se quella persona ha cercato anche te o se siete amici, così nessuno può provare numeri a caso per vedere chi ha una Machine.

## Pianifica con altre Machine

Quando una persona con una Machine scrive «vediamoci la settimana prossima», la tua Machine chiede alla sua quali orari sono liberi e trova quello che va bene a entrambi, entro il tuo orario di lavoro. Riceverete entrambi un'attività, per esempio «Incontra Alex Example», con l'orario sotto. Tocca **Prenota**, **Altro orario** o **Non serve**. L'invito viene inviato solo dopo che entrambi avete toccato Prenota.

Viene condiviso solo se sei libero o impegnato, con crittografia end-to-end, per un massimo di 14 giorni e con intervalli arrotondati a 15 minuti. Gli eventi privati risultano come impegni. Una Machine può fare una richiesta solo se vi siete scambiati email in entrambe le direzioni. Imposta questa opzione in **Cosa possono chiedere altre Machine alla mia**: **Libero/occupato per pianificare** o **Disattivata**, insieme alla durata delle riunioni, al margine tra una e l'altra e agli orari preferiti. Ogni richiesta compare in Attività, sotto Calendario.

Un orario è considerato libero solo se il calendario lo indica. La tua Machine non propone orari se non hai collegato un calendario, se non è stato possibile leggerlo per un giorno o se la data è a più di 30 giorni. Gli eventi di un'intera giornata contano come impegni se sono contrassegnati come Occupato, mentre quelli contrassegnati come Libero non contano mai. Un evento di un'intera giornata aggiunto da un'attività risulta Libero, a meno che tu non sia assente o abbia già preso quei giorni: in tal caso, prima che tu lo aggiunga viene indicato come «occupato».

Se l'altra persona non ha una Machine o non risponde, nella bozza dell'email compare un link che le permette di scegliere uno dei tuoi orari liberi. La sua scelta diventa un'attività con **Prenota**; non viene prenotato nulla finché non lo tocchi.

Il link mostra solo gli orari liberi, secondo le stesse regole, e non rivela altro su di te. Scade quando la riunione viene prenotata o dopo 14 giorni. Nell'email appare come «Scegli un orario». In fondo alla pagina compare «La Machine di Alex ha trovato questi orari. Procuratene una.», con il tuo nome. Disattiva questa opzione con **Piè di pagina nei link di prenotazione**. Ogni link e ogni scelta compaiono in Attività.

## Una Machine sul tuo computer

Per unirti al Network da una Machine che gestisci tu:

1. Nella dashboard della tua Machine, apri **Impostazioni** e seleziona **Unisciti al Network**.
2. Nella pagina che si apre, accedi (o crea il tuo account) e conferma. La tua Machine lo rileva automaticamente, senza riavviarsi.

Puoi continuare a usare anche il metodo con codice: nella pagina del tuo account su app.themachine.computer, seleziona **Abbina una Machine self-hosted**, poi esegui `assistant fleet-pair` con il codice sul tuo computer e riavvia. Il codice può essere usato una sola volta ed è valido per 15 minuti.

Puoi avere fino a 5 Machine per account. Puoi disconnetterle da lì.
