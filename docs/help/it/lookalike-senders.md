---
title: Mittenti simili
area: security
summary: Le email da un indirizzo che imita qualcuno con cui hai rapporti vengono segnalate nell’attività associata e le bozze non vengono mai inviate a quell’indirizzo.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## Cosa rileva

Alcune truffe arrivano da un indirizzo che assomiglia a uno che conosci: `examp1e.com` al posto di `example.com`, `example-billing.com` o con una lettera diversa. The Machine confronta il dominio di ogni mittente con quelli con cui hai già rapporti. Se quello più recente assomiglia soltanto a uno noto, lo considera un mittente simile.

Lo stesso nome con un’altra estensione, come `example.nl` accanto a `example.com`, indica la stessa organizzazione, non un mittente simile. Gli indirizzi di posta gratuiti, come gmail.com, non vengono mai considerati.

## Nell’attività

L’attività relativa a un messaggio del genere lo dice chiaramente, per esempio: «Non è Alex. Il messaggio arriva da examp1e.com, non da example.com». Il mittente appare come semplice indirizzo, senza foto né link alla persona che imita.

## Cosa non farà The Machine

- Non assegna mai a un mittente simile un ruolo nel tuo Graph.
- Non lo unisce mai alla persona che imita e non lo suggerisce mai sotto **Stessa persona?**.
- Le risposte che prepara vengono inviate all’indirizzo registrato, non a quello simile.

La scelta spetta sempre a te: puoi comunque assegnargli un ruolo, unirlo alla persona che imita o scrivere a qualsiasi indirizzo.
