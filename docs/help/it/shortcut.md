---
title: Shortcut
area: connections
summary: Storie che cambiano stato, con assegnatari e scadenze. Può solo leggerle.
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
translated: 68419e11fabc157c
---
## Cosa legge

Le storie nel tuo workspace di Shortcut che cambiano stato, con i relativi assegnatari e le scadenze.

## Cosa può fare

Non può fare nulla in Shortcut. Può solo leggere.

## Collega Shortcut

1. Nella dashboard: **Connessioni**, **Progetti e codice**, Shortcut. Oppure, nella pagina di configurazione di una Machine ospitata, vai su app.themachine.computer/setup e scegli **Altre fonti**, Shortcut. Sul tuo computer, prima devi associarlo al tuo account.
2. Premi **Accedi con Shortcut** e consenti l’accesso in lettura. A Shortcut chiede solo l’accesso in lettura.
3. Quando torni in The Machine, la tua Machine verifica subito l’accesso e mostra l’account usato e il workspace a cui si è collegata.

Hai più di un workspace Shortcut? Passa prima a quello giusto in Shortcut. Per un altro workspace, aggiungi di nuovo Shortcut.

## In alternativa, incolla un token

In **Oppure incolla un token API**, premi **Recupera il tuo token**. Shortcut apre la pagina API Tokens in una nuova scheda: crea un token, copialo e incollalo, poi premi **Collega**. Sul tuo computer, `assistant connect shortcut` te lo chiede a sua volta. Un token dà accesso completo al tuo account, ma The Machine lo usa solo per leggere.

## Rimuovi la connessione

- Nella dashboard: **Connessioni**, apri Shortcut, **Dettagli**, poi **Disconnetti**. I dati già importati restano.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a Shortcut nella pagina di configurazione.

## Revoca l’accesso in Shortcut

Se hai incollato un token, eliminalo dalla pagina API Tokens. Se hai effettuato l’accesso, disconnetterlo qui interrompe ogni lettura.
