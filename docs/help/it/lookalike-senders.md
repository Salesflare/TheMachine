---
title: Mittenti che imitano i tuoi contatti
area: security
summary: Le email da un indirizzo che imita qualcuno con cui hai rapporti vengono segnalate nell’attività, e le bozze non vengono mai indirizzate a quell’indirizzo.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## Cosa rileva

Alcune truffe arrivano da un indirizzo che assomiglia a uno che conosci: `examp1e.com` al posto di `example.com`, `example-billing.com` oppure con una lettera diversa. La Machine confronta il dominio di ogni mittente con quelli con cui hai già rapporti. Se il nuovo dominio somiglia soltanto a uno noto, lo considera un sosia.

Lo stesso nome con un’estensione diversa, come `example.nl` rispetto a `example.com`, appartiene alla stessa organizzazione e non è un sosia. Gli indirizzi di posta gratuiti, come gmail.com, non vengono mai considerati sosia.

## Nell’attività

Un’attività relativa a un messaggio del genere lo dice chiaramente, per esempio: «Questo non è Alex. Arriva da examp1e.com, non da example.com». Il mittente appare come semplice indirizzo, senza foto né link alla persona che imita.

## Cosa non farà The Machine

- Non assegna mai a un mittente sosia un ruolo nel tuo Graph.
- Non lo unisce mai alla persona che imita e non lo suggerisce mai sotto **Stessa persona?**.
- Le risposte che prepara vengono indirizzate all’indirizzo registrato, non a quello del sosia.

La scelta finale spetta sempre a te: puoi comunque assegnargli un ruolo, unirlo a un’altra persona o scrivere a qualsiasi indirizzo.
