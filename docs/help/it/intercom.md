---
title: Intercom
area: connections
summary: Conversazioni con i clienti nel tuo workspace Intercom. Risponde solo dopo che invii il messaggio, a tuo nome.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 2cbee87e6d24c0a9
---
## Cosa legge

Le conversazioni con i clienti nel tuo workspace Intercom: quelle degli ultimi 7 giorni quando lo colleghi, poi le nuove man mano che arrivano. Legge anche a quale workspace e teammate è associato l’accesso.

## Cosa può fare

Con il tuo **Accedi con Intercom**, può rispondere a una conversazione a tuo nome, ma solo dopo che premi **Invia** su quel testo esatto. Non assegna mai conversazioni, non le chiude, non aggiunge tag e non scrive note. Un Intercom condiviso con te tramite la tua Fleet può solo leggere.

## Attività da Intercom

Un’attività da Intercom mostra il cliente e **Leggi il messaggio** apre la conversazione, con un link per visualizzarla in Intercom. La risposta viene inviata in quella conversazione, a meno che tu non chieda di inviarla via email.

Solo le conversazioni assegnate a te, o ancora non assegnate, diventano attività. Quando un teammate se ne occupa in Intercom, la relativa attività si chiude automaticamente e puoi usare **Annulla**. Su un Intercom condiviso con te, le tue conversazioni sono quelle assegnate al teammate con cui scrivi.

Un’attività di Intercom si chiude automaticamente anche quando qualcuno del team chiude la conversazione in Intercom, oppure le risponde e il cliente non scrive più, se l’attività richiedeva solo una risposta. Vale anche se hai risposto appena prima che arrivasse l’attività, prima che The Machine leggesse la tua risposta. Una nota, un posticipo o la risposta di un bot non contano.

Quando la tua Machine non può rispondere in Intercom (è condiviso con te in sola lettura, le risposte non sono abilitate o non è collegato), la risposta viene preparata per l’invio via email. L’attività spiega perché e chiede **Inviare via email invece?** Per rispondere in Intercom, tocca **Collega il tuo Intercom** nell’attività e accedi. L’attività viene quindi riscritta come risposta in Intercom. Non viene inviato nulla prima che tu lo invii.

Il tuo Intercom personale e un Intercom condiviso con te per lo stesso workspace non leggono entrambi: quello condiviso resta inattivo e le sue conversazioni passano al tuo, una sola volta ciascuna.

## Collegarlo

1. Nella dashboard: **Connessioni**, **Clienti**, Intercom. Oppure, nella pagina di configurazione di una Machine ospitata, su app.themachine.computer/setup: **Altre fonti**, Intercom. Sul tuo computer, prima abbinala al tuo account.
2. Premi **Accedi con Intercom**.
3. Autorizza The Machine (creata da Salesflare) in Intercom. Tornerai al punto di partenza.

Accedendo a un altro workspace, aggiungi un secondo account Intercom.

Intercom viene sempre considerato lavoro, per l’azienda indicata nel nome del workspace.

## Rimuoverlo

- Nella dashboard: **Connessioni**, apri Intercom, **Dettagli**, poi **Disconnetti**. Smetterà di leggere. Quello che ha già importato resta.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a Intercom nella pagina di configurazione.

## Disinstallarlo da Intercom

In Intercom, apri Impostazioni, App, App installate e rimuovi The Machine.
