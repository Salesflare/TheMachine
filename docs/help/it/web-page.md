---
title: Pagine web osservate
area: connections
summary: Una pagina web che osservi. Un'attività solo quando cambia qualcosa che conta.
covers: connector:web_page
code: connectors/web_page.py
---
## Cosa legge

Il testo di una pagina web pubblica per connessione, ogni poche ore e al massimo una volta all'ora. Lascia fuori menu, piè di pagina, avvisi sui cookie e pubblicità. Quando il testo è cambiato, The Machine guarda cosa è cambiato e crea un'attività solo se conta, come un nuovo prezzo o una policy cambiata. Date, contatori e piccole riformulazioni non creano mai un'attività. Una pagina invariata non costa nulla.

Prima chiede il robots.txt del sito e lascia stare la pagina se il sito dice di no. Le pagine dietro un accesso o costruite solo con JavaScript non si possono osservare.

## Cosa può fare

Niente. Legge solo la pagina.

## Collegalo

1. Nella dashboard, apri **Connessioni**, poi **Altro**, e scegli Pagina web. Oppure esegui `assistant connect web_page`.
2. Incolla l'indirizzo della pagina.

Oppure chiedilo nella tua chat: "Osserva questa pagina per i cambi di prezzo" con il suo indirizzo. Chiedi quali pagine osservi, o di smettere di osservarne una.

## Rimuovilo

Nella dashboard: **Connessioni**, apri la pagina, **Dettagli**, poi **Disconnetti**. Oppure chiedi alla tua chat di smettere di osservarla.
