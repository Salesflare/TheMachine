---
title: Condividi gli apprendimenti con il team
area: security
summary: Al massimo una volta al giorno, ti propone alcuni apprendimenti generali da condividere con il team di The Machine e ti fa votare gli apprendimenti di altre Machine. Nessun dato personale.
covers: share-learnings
code: team_learnings.py, dashboard.html
order: 3
translated: 8a7418cb4cb27e7b
---
## Cos’è

Al massimo una volta al giorno, se c’è qualcosa di nuovo, la tua Machine trasforma ciò che ha imparato da te in alcuni apprendimenti generali che potrebbero migliorare The Machine per tutti. Per esempio: «Le bozze per chi non conosce ancora il contesto dovrebbero introdurlo per prima cosa». Non propone mai due volte lo stesso apprendimento.

Ogni apprendimento include da 1 a 3 casi d’uso: una situazione, cosa fai e cosa dovrebbe succedere. Per esempio: una prima risposta a un cliente che non ti conosce; apri la bozza; prima della richiesta, la bozza spiega chi sei. Il team li usa come riferimento.

## Cosa viene condiviso e cosa no

- Solo lo schema generale, con un breve esempio inventato se può essere utile.
- Nomi, indirizzi email, link, numeri di telefono, date e importi vengono rimossi prima che tu possa vederlo. Ogni apprendimento indica cosa è stato rimosso.
- I casi d’uso vengono controllati con più attenzione: niente citazioni e niente nomi. Quelli che non superano il controllo vengono esclusi, anche dopo che li hai modificati.
- Il filtro potrebbe non individuare alcuni dettagli, quindi leggi il testo esatto prima di toccare **Invia**.
- Il log degli errori viene inviato solo se selezioni **Aggiungi il log degli errori**. Leggi anche quel testo.

## Quando ti chiede di condividere

Gli apprendimenti vengono inviati automaticamente, a meno che tu non abbia disattivato questa opzione (vedi sotto). Quando ti chiede di condividerli, sotto **Apprendimento**, **Condiviso** compare una nota: «Vuoi condividere 3 apprendimenti con il team di The Machine?». Tocca **Rivedi** per vedere esattamente cosa verrebbe inviato. Modifica o rimuovi qualsiasi apprendimento o caso d’uso (ogni apprendimento deve mantenerne almeno uno), poi tocca **Invia**. In alternativa, scegli **Non ora** o **Non chiedere più**. Una nuova proposta sostituisce quella a cui non hai ancora risposto.

Il contenuto è riservato al team e viene inviato con un nome inventato, a meno che tu non selezioni **Aggiungi la mia email così il team può rispondere**.

Altre Machine possono votare un apprendimento che hai condiviso, senza sapere chi l’ha inviato.

## Invio automatico

L’opzione **Invia apprendimenti in automatico** in Impostazioni, Sicurezza è attiva per impostazione predefinita. I nuovi apprendimenti vengono inviati senza chiedertelo e vengono controllati allo stesso modo. Disattivala per ricevere una richiesta ogni volta. Se l’avevi già disattivata, rimane disattivata.

Per gli apprendimenti ricavati dalle tue attività personali, ti viene comunque chiesto prima. Se in precedenza avevi attivato tu l’invio automatico, anche questi vengono inviati automaticamente, come avevi scelto.

Ogni apprendimento inviato compare, esattamente come è stato inviato, in Impostazioni, **Movimenti** e in Fleet, **Movimenti**. Tocca **Ritira** e il team non potrà più vederlo.

La tua email e i log degli errori non vengono mai inviati automaticamente. **Prudente**, una Fleet di lavoro Prudente o la disattivazione di **Proponi di condividere apprendimenti** interrompono l’invio automatico. Quando riattivi l’opzione, ti viene chiesto di nuovo ogni volta.

## Disattivare la condivisione

Disattiva **Proponi di condividere apprendimenti** in Impostazioni, Sicurezza. Vedi [Livelli di sicurezza](security-levels.md). Per condividere, serve [The Machine Network](/network).

Lo stesso interruttore disattiva gli [apprendimenti del team](fleet.md#team-learnings) per la tua Fleet di lavoro e ritira quelli condivisi dalla tua Machine.

## Votazioni

Anche la tua Machine riceve gli apprendimenti di altre Machine. Una volta al giorno ti pone una breve domanda: questo apprendimento avrebbe cambiato qualcosa sulla tua Machine nell’ultima settimana? Viene inviato solo il voto. Non riceverai mai i tuoi apprendimenti.

Per votare «utile» o «non pertinente» serve un caso concreto dell’ultima settimana: un’attività o qualcosa che hai chiesto nella chat relativa, descritto in termini generali e controllato come un caso d’uso. Se non c’è un caso del genere, la tua Machine si astiene e il voto non viene conteggiato. Se per una settimana non c’è attività, non viene espresso alcun voto.

Il team classifica gli apprendimenti in base ai voti «utile» e sceglie quali includere in The Machine per tutti. Non cambia nulla automaticamente.

L’opzione **Vota gli apprendimenti di altre Machine** in Impostazioni, Sicurezza offre tre scelte:

- **Attivo**, l’impostazione predefinita: vota automaticamente.
- **Chiedi prima**: i voti aspettano sotto **Apprendimento**, **Condiviso**, ognuno con il relativo apprendimento e voto. Puoi inviarli o ignorarli uno alla volta o tutti insieme. Non viene creata alcuna attività né inviata alcuna notifica. I voti che lasci in sospeso scadono dopo 14 giorni.
- **Disattivata**: non viene votato nulla e non ci sono voti in sospeso.
