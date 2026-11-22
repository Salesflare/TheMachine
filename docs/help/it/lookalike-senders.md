---
title: Mittenti che si spacciano per altri
area: security
summary: Le email da un indirizzo che imita quello di una persona con cui hai a che fare vengono segnalate nelle relative attività e le bozze non vengono mai inviate a quell’indirizzo.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 15a6a5dafcfa807b
---
## Cosa intercetta

Alcune truffe arrivano da un indirizzo che sembra quello di una persona che conosci: `examp1e.com` invece di `example.com`, `example-billing.com`, una lettera diversa o due lettere invertite. The Machine confronta il dominio di ogni mittente con quelli delle persone con cui hai già a che fare.

Se due indirizzi si somigliano, quello a cui hai scritto, che hai incontrato o che hai configurato tu è quello vero, anche se l’altro ti ha scritto per primo. Se nessuno dei due ha queste caratteristiche, quello più recente viene considerato il mittente che imita l’altro.

Lo stesso nome con un finale diverso, come `example.nl` rispetto a `example.com`, indica la stessa organizzazione, non un mittente che imita un altro. Gli indirizzi email gratuiti, come gmail.com, non vengono mai considerati.

## Nelle attività

Un’attività relativa a un messaggio di questo tipo lo dice chiaramente, per esempio: «Questo non è Alex. Il messaggio arriva da examp1e.com, non da example.com». Il mittente viene mostrato solo con il suo indirizzo, senza foto né link alla persona che imita.

## Cosa non farà The Machine

- Non assegna mai un ruolo nel tuo Graph a un mittente che imita qualcun altro e non imposta mai il suo dominio come organizzazione di un progetto.
- Non lo unisce mai alla persona che imita, neanche se scrive nella stessa conversazione con lo stesso nome, e non lo suggerisce mai in **Stessa persona?**.
- Le risposte che prepara vengono inviate all’indirizzo registrato, non a quello del mittente che imita qualcun altro.

La tua scelta ha sempre la precedenza: puoi comunque assegnargli un ruolo, unirlo a un’altra persona o scrivere a qualsiasi indirizzo.
