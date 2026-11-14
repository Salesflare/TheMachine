---
title: LinkedIn
area: connections
summary: I tuoi messaggi LinkedIn, letti nel browser della tua Machine, connesso al tuo account. Le risposte partono solo dopo la tua approvazione.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: 850b91f79b9e23fc
---
## Cosa legge

I tuoi messaggi LinkedIn. Li legge di tanto in tanto, durante le ore di veglia, nel browser della tua Machine, connesso al tuo account. Non segna nulla come letto. Legge anche le conversazioni archiviate e le richieste di messaggi, ma non lo spam.

## Ruoli e aziende

Inoltre, aggiorna i ruoli e le aziende delle tue connessioni LinkedIn già presenti nel tuo Graph, usando l’elenco Connessioni. Non apre i loro profili né aggiunge nuove persone. Quando cambia il ruolo o l’azienda di qualcuno, lo trovi nella sua cronologia, per esempio «Ora Head of Sales presso Acme, prima Sales Lead presso Acme».

Il ruolo viene ricavato dal titolo del profilo, per esempio «Head of Sales presso Acme» o «VP Sales and Strategy», mai da uno slogan. Trova le persone tramite il link al loro profilo oppure tramite nome e azienda. Se non c’è un’azienda da confrontare, basta il nome completo, purché appartenga a una sola persona nel tuo Graph. Nella pagina trovi anche da quando siete collegati.

Legge molto lentamente: una pagina alla volta, a distanza di alcuni minuti, poche decine di pagine al giorno e solo durante il giorno. Per circa 3.000 connessioni ci vogliono più o meno quattro giorni. Se LinkedIn blocca l’accesso, si ferma fino al giorno successivo.

## Cosa può inviare

Può rispondere a un messaggio o inviare un nuovo messaggio a un profilo che indichi, ma solo dopo che l’hai approvato nell’attività. Fino ad allora prepara solo una bozza.

LinkedIn non offre un modo ufficiale per farlo. È molto improbabile che la lettura e l’invio occasionale di un messaggio da te approvato causino problemi. L’invio in massa o automatizzato può portare al blocco dell’account.

## Collegala

Su una Machine ospitata:

1. Apri la pagina di configurazione all’indirizzo app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri LinkedIn, accedi a LinkedIn dal browser della tua Machine quando richiesto, poi premi **Collegati**.

Sul tuo computer:

1. Nella dashboard, apri **Connessioni**, poi **Chat** e seleziona LinkedIn.
2. Seleziona **Lavoro** (con la relativa azienda) o **Personale**, poi premi **Collegati**.
3. Premi **Accedi a LinkedIn** e accedi dal browser della tua Machine. Una volta effettuato l’accesso, la connessione si attiva automaticamente.

Oppure esegui `assistant connect linkedin`.

Un secondo account LinkedIn avrà un browser dedicato. Se LinkedIn disconnette la tua Machine, consulta [Disconnessione da un sito](signed-out.md).

## Se LinkedIn ti chiede un codice

La prima volta che la tua Machine accede, LinkedIn spesso ti invia un codice via email. Inseriscilo nella finestra di accesso, sotto **Codice**, poi premi **Accedi**. La pagina resta aperta mentre inserisci il codice.

Se LinkedIn torna all’inizio o non succede nulla per due minuti, aspetta un minuto e premi **Riprova**. Se LinkedIn mostra un controllo anti-robot, completalo nel browser della tua Machine.

## Rimuovila

- Nella dashboard: apri **Connessioni**, seleziona LinkedIn, poi **Dettagli** e **Disconnetti**. Smetterà di leggere i messaggi. Quelli già importati restano.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a LinkedIn nella pagina di configurazione.

## Disconnettila da LinkedIn

In LinkedIn, apri Impostazioni, Accedi e sicurezza, Dove hai effettuato l’accesso, poi disconnetti la sessione del browser della tua Machine.
