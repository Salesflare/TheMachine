---
title: LinkedIn
area: connections
summary: I tuoi messaggi LinkedIn, letti nel browser della tua Machine, connesso al tuo account. Le risposte partono solo dopo la tua approvazione.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: bc67fbc21c77a97a
---
## Cosa legge

I tuoi messaggi LinkedIn. Li legge di tanto in tanto, durante le ore di veglia, nel browser della tua Machine, connesso al tuo account. Non segna nulla come letto. Legge anche le conversazioni archiviate e le richieste di messaggi; lo spam è escluso.

## Ruoli e aziende

Aggiorna anche i ruoli e le aziende dei tuoi collegamenti LinkedIn già presenti nel tuo Graph, partendo dall’elenco **Connessioni**. Non apre i loro profili né aggiunge nuove persone. Quando cambia il ruolo o l’azienda di una persona, la sua cronologia lo segnala, per esempio: «Ora Head of Sales presso Acme, prima Sales Lead presso Acme».

Il ruolo viene ricavato dal titolo del profilo, per esempio «Head of Sales presso Acme» o «VP Sales and Strategy», mai da uno slogan. La persona viene identificata tramite il link al profilo oppure il nome e l’azienda. Se non c’è un’azienda con cui fare il confronto, basta che il suo nome completo appartenga a una sola persona nel tuo Graph. Nella sua pagina puoi anche vedere da quando siete collegati.

La lettura è molto lenta: una pagina alla volta, a distanza di alcuni minuti, per qualche decina di pagine al giorno e solo di giorno. Per circa 3.000 collegamenti servono all’incirca quattro giorni. Se LinkedIn oppone resistenza, la lettura si interrompe fino al giorno successivo.

## Cosa può inviare

Può rispondere a un messaggio o inviare un nuovo messaggio a un profilo che indichi, ma solo dopo che approvi il messaggio nell’elenco delle attività. Fino ad allora prepara solo una bozza.

LinkedIn non offre un modo ufficiale per farlo. Leggere i messaggi e inviarne ogni tanto uno che hai approvato difficilmente causerà problemi; gli invii di massa o automatici possono far bloccare un account.

## Collegalo

1. Nella dashboard, apri **Connessioni**, poi **Chat**, e scegli LinkedIn.
2. Scegli **Lavoro** (con la relativa azienda) oppure **Personale**, poi premi **Collega**.
3. Premi **Accedi a LinkedIn** e accedi dal browser della tua Machine. La connessione si attiva automaticamente quando hai effettuato l’accesso.

Se usi una Machine ospitata, puoi anche andare alla pagina di configurazione su app.themachine.computer/setup: apri **Altre fonti**, seleziona LinkedIn, accedi quando richiesto, poi premi **Collega**. Sul tuo computer, `assistant connect linkedin` fa la stessa cosa da terminale.

Se colleghi un secondo account LinkedIn, avrà un browser dedicato. Se LinkedIn disconnette la tua Machine, consulta [Disconnessione da un sito](signed-out.md).

## Se LinkedIn chiede un codice

La prima volta che la tua Machine accede, LinkedIn spesso invia un codice via email. Inseriscilo nella finestra di accesso, sotto **Codice**, poi premi **Accedi**. La pagina resta aperta mentre digiti.

Se LinkedIn torna alla pagina iniziale o non succede nulla per due minuti, aspetta un minuto e premi **Riprova**. Se LinkedIn mostra una verifica anti-robot, completala nel browser della tua Machine.

## Rimuovilo

- Nella dashboard: apri **Connessioni**, seleziona LinkedIn, poi **Dettagli** e **Disconnetti**. La lettura si interrompe. I contenuti già importati restano.
- Se usi una Machine ospitata, puoi anche premere **Rimuovi** accanto a LinkedIn nella pagina di configurazione.

## Disconnettila da LinkedIn

In LinkedIn, apri **Impostazioni** > **Accesso e sicurezza** > **Dove hai effettuato l’accesso**, poi disconnetti la sessione del browser della tua Machine.
