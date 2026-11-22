---
title: Condividere gli apprendimenti con il team
area: security
summary: Al massimo una volta al giorno, propone alcuni apprendimenti generali al team di The Machine e vota quelli di altre Machine. Nessun dato personale.
covers: share-learnings
code: team_learnings.py, dashboard.html
order: 3
translated: 8a7418cb4cb27e7b
---
## Cos’è

Al massimo una volta al giorno, se c’è qualcosa di nuovo, la tua Machine trasforma ciò che ha imparato da te in alcuni apprendimenti generali che potrebbero migliorare The Machine per tutti. Per esempio: «Le bozze per chi non conosce ancora il contesto dovrebbero spiegarlo prima». Non propone mai due volte lo stesso apprendimento.

Ogni apprendimento include da 1 a 3 casi d’uso: una situazione, cosa fai e cosa dovrebbe succedere. Per esempio: la prima risposta a un cliente che non ti conosce; apri la bozza; prima della richiesta, spiega chi sei. Il team li usa come base per il proprio lavoro.

## Cosa viene condiviso e cosa no

- Solo lo schema generale, con un breve esempio inventato, se può essere utile.
- Nomi, indirizzi email, link, numeri di telefono, date e importi vengono rimossi prima che tu possa vederli. Ogni apprendimento indica cosa è stato rimosso.
- I casi d’uso vengono controllati con più attenzione: niente citazioni né nomi. Quelli che non superano il controllo vengono esclusi, anche dopo che li hai modificati.
- I filtri potrebbero non rilevare alcuni dettagli, quindi leggi il testo esatto prima di toccare **Invia**.
- Il log degli errori viene inviato solo se selezioni **Aggiungi il log degli errori**. Leggi anche quell’estratto.

## Quando ti chiede

Gli apprendimenti vengono inviati automaticamente, a meno che tu non abbia disattivato l’opzione (vedi sotto). Quando ti chiede di condividerli, sotto **Apprendimento**, **Condiviso** compare una nota: «Vuoi condividere 3 apprendimenti con il team di The Machine?». Tocca **Rivedi** per vedere esattamente cosa verrebbe inviato. Puoi modificare o rimuovere qualsiasi apprendimento o caso d’uso (ogni apprendimento deve conservarne almeno uno), poi tocca **Invia**. In alternativa, scegli **Non ora** o **Non chiedere più**. Una nuova proposta sostituisce quella a cui non hai ancora risposto.

Il contenuto viene inviato al team in modo riservato e con un nome inventato, a meno che tu non selezioni **Aggiungi la mia email così il team può rispondere**.

Altre Machine possono votare un apprendimento che hai condiviso, senza sapere chi l’ha inviato.

## Invio automatico

L’opzione **Invia apprendimenti in automatico** in Impostazioni, Sicurezza è attiva per impostazione predefinita. I nuovi apprendimenti vengono inviati senza chiedertelo, dopo gli stessi controlli. Disattivala per ricevere una richiesta ogni volta. Se l’avevi già disattivata, resterà disattivata.

Per gli apprendimenti tratti dalle tue attività personali, la Machine ti chiede comunque prima di inviarli. Se in precedenza avevi attivato personalmente l’invio automatico, verranno inviati automaticamente anche questi, come hai scelto.

Ogni apprendimento inviato compare, esattamente com’è stato condiviso, in Impostazioni, **Movimenti**, e in Fleet, **Movimenti**. Tocca **Ritira** e il team non potrà più vederlo.

La tua email e i log degli errori non vengono mai inviati automaticamente. **Prudente**, una Fleet di lavoro impostata su Prudente o la disattivazione di **Proponi di condividere apprendimenti** impediscono l’invio automatico. Se riattivi l’opzione, la Machine ti chiederà di nuovo ogni volta.

## Disattivare la condivisione

Disattiva **Proponi di condividere apprendimenti** in Impostazioni, Sicurezza. Vedi [Livelli di sicurezza](security-levels.md). Per condividere, serve [The Machine Network](/network).

Lo stesso interruttore disattiva anche gli [apprendimenti del team](fleet.md#team-learnings) per la tua Fleet di lavoro e ritira quelli che la tua Machine ha condiviso.

## Votare

Anche la tua Machine riceve apprendimenti da altre Machine. Una volta al giorno, ti viene chiesto brevemente: avrebbe cambiato qualcosa sulla tua Machine nell’ultima settimana? Viene inviato solo il voto. Non riceverai mai i tuoi apprendimenti.

Per votare che un apprendimento è utile o non pertinente, serve un caso concreto della settimana passata: un’attività o qualcosa che hai chiesto nella chat dell’apprendimento, descritto in termini generali e verificato come un caso d’uso. Se non c’è un caso, la tua Machine si astiene e il voto non viene conteggiato. Se non c’è stata alcuna attività per una settimana, non vengono espressi voti.

Il team ordina gli apprendimenti in base ai voti «Utile» e sceglie quali includere in The Machine per tutti. Non cambia nulla automaticamente.

In Impostazioni, Sicurezza, **Vota gli apprendimenti di altre Machine** ha tre opzioni:

- **Attivo**, l’opzione predefinita: la Machine vota automaticamente.
- **Chiedi prima**: i voti restano in attesa sotto **Apprendimento**, **Condiviso**, insieme all’apprendimento e al voto. Puoi inviarli o saltarli uno alla volta o tutti insieme. Nessuna attività né notifica. I voti che lasci in sospeso scadono dopo 14 giorni.
- **Disattivata**: non vengono espressi voti e non viene inviato nulla di ciò che è in attesa.
