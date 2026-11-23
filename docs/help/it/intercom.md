---
title: Intercom
area: connections
summary: Conversazioni con i clienti nel tuo spazio di lavoro Intercom. Risponde solo dopo che invii il messaggio, a tuo nome.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 5a6938dd6c220a43
---
## Cosa legge

Le conversazioni con i clienti nel tuo spazio di lavoro Intercom: quelle degli ultimi 7 giorni quando lo colleghi, poi le nuove man mano che arrivano. Legge anche a quale spazio di lavoro e a quale membro del team è associato l’accesso.

## Cosa può fare

Se colleghi il tuo account con **Accedi con Intercom**, può rispondere a una conversazione a tuo nome, ma solo dopo che premi **Invia** su quel testo. Non assegna mai conversazioni, non le chiude, non aggiunge tag e non scrive note. Un Intercom condiviso con te tramite la tua Fleet serve solo per leggere.

## Attività da Intercom

Un’attività da Intercom mostra il cliente e **Leggi il messaggio** apre la conversazione con un link per visualizzarla su Intercom. Ogni messaggio è associato a chi l’ha scritto: il cliente da una parte, il tuo team e il suo bot dall’altra, anche quando a iniziare la conversazione è stato un membro del team o una campagna. La risposta viene inviata in quella conversazione, a meno che tu non chieda di inviarla via email.

Solo le conversazioni assegnate a te o non ancora assegnate diventano attività. Quando un membro del team ne prende una su Intercom, la relativa attività si chiude da sola e puoi usare **Annulla**. Su un Intercom condiviso con te, le tue conversazioni sono quelle assegnate al membro del team a nome del quale scrivi.

Un’attività di Intercom si chiude da sola anche quando qualcuno del team chiude la conversazione su Intercom oppure risponde e il cliente non scrive più, se l’attività richiedeva solo una risposta. Vale anche se hai risposto poco prima che arrivasse l’attività, prima che The Machine leggesse la tua risposta. Una nota, un posticipo o una risposta del bot non contano.

Quando la tua Machine non può rispondere su Intercom (perché l’account è condiviso con te in sola lettura, le risposte sono disattivate o non è collegato), la bozza viene inviata via email. L’attività spiega il motivo e chiede **Inviare via email invece?** Per rispondere su Intercom, tocca **Collega il tuo Intercom** nell’attività e accedi. L’attività viene quindi ricreata come risposta su Intercom. Non viene inviato nulla prima che tu lo invii.

Il tuo account Intercom e quello condiviso con te per lo stesso spazio di lavoro non leggono entrambi le conversazioni: quello condiviso resta inattivo e le conversazioni passano al tuo, una sola volta ciascuna.

## Collega Intercom

1. Nella dashboard: **Connessioni**, **Clienti**, Intercom. Oppure, nella pagina di configurazione di una Machine ospitata, su app.themachine.computer/setup: **Altre fonti**, Intercom. Sul tuo computer, prima associa la Machine al tuo account.
2. Premi **Accedi con Intercom**.
3. Autorizza The Machine (creata da Salesflare) su Intercom. Tornerai al punto di partenza.

Se accedi a un altro spazio di lavoro, viene aggiunto un secondo account Intercom.

Intercom viene sempre considerato lavoro, per l’azienda indicata dal nome del suo spazio di lavoro.

## Rimuovi Intercom

- Nella dashboard: **Connessioni**, apri Intercom, seleziona **Dettagli**, poi **Disconnetti**. Intercom smette di leggere le conversazioni. Quelle già importate restano.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a Intercom nella pagina di configurazione.

## Disinstalla Intercom

Su Intercom, apri Impostazioni, App, App installate e rimuovi The Machine.
