---
title: Invia più tardi
area: cards
summary: Premi **Invia più tardi** accanto a **Invia ora** per programmare l’invio di un’email o di un messaggio. Lo approvi subito e scegli quando inviarlo. Se l’altra persona scrive per prima, resta in attesa di una tua conferma.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, schedule an email, send at a time, delay, tomorrow morning, unsend, take back
translated: 6fa6af155c337981
---
## Programma un messaggio

Nella finestra in cui controlli un messaggio, premi **Invia più tardi** accanto a **Invia ora**. Scegli **Tra 2 ore**, **Domani**, **Lunedì** o **Scegli una data**, poi **Salva l’orario**. Il messaggio viene inviato esattamente come l’hai visto, all’ora scelta nel tuo fuso orario.

La funzione è disponibile per email, Slack, WhatsApp, Telegram, Signal, Teams e Intercom. Non è disponibile per LinkedIn e X, perché la tua Machine non può controllare se è arrivato un nuovo messaggio subito prima dell’invio, né per le risposte in un documento.

La trovi anche in **Nuova email**. Se controlli più messaggi insieme, verranno inviati tutti all’ora scelta.

## Mentre è in attesa

L’attività resta in **Torna più tardi** e nel [Calendario](calendar.md), nel giorno previsto, insieme al messaggio e all’orario di invio: «Invio gio 26 nov, 09:30». **Invia ora** lo invia subito, **Cambia orario** permette di scegliere un altro orario e **Annulla** lo trasforma di nuovo in una bozza. Lo stesso vale nella chat.

Se modifichi la bozza, completi o scarti l’attività, oppure la riporti indietro, il messaggio non viene inviato: serve di nuovo la tua conferma.

## Se l’altra persona scrive per prima

Se l’altra persona scrive prima dell’invio, la tua Machine non invia il messaggio. L’attività torna con il suo messaggio, ad esempio «Non inviato: Sam Lee ha scritto per primo», e ricevi la notifica che ricevi quando posticipi un’attività. Per un’email, vale qualsiasi indirizzo che la tua Machine conosce per quella persona, in qualsiasi casella collegata. Vale anche se risponde un’altra persona nella conversazione.

Una risposta automatica, ad esempio un messaggio di assenza, non impedisce l’invio. Lo stesso vale per un tuo messaggio.

Subito prima dell’invio, la tua Machine controlla di nuovo la conversazione. Se non ci riesce, l’attività mostra «Non è ancora stato possibile controllare se è arrivato un nuovo messaggio» e la Machine riprova per un’ora. Poi chiede a te invece di inviare il messaggio.

Su WhatsApp, controlla i messaggi ricevuti fino a quel momento dal tuo WhatsApp collegato.

## Se la Machine è spenta

Se in quel momento la tua Machine è spenta, in sospensione o disconnessa, il messaggio viene inviato quando torna disponibile, con un ritardo massimo di un’ora. Se il ritardo supera un’ora, l’attività torna con il messaggio «Non inviato: il ritardo ha superato un’ora» e decidi tu cosa fare.

Quando passi a un altro computer, i messaggi programmati chiedono di nuovo la tua conferma. Scopri di più in [Passare a un altro computer](moving.md).

## Chi può programmare un messaggio

Puoi farlo solo tu, dalla dashboard o dall’app. La tua Machine, la sua chat, un’IA che hai collegato e le altre Machine non possono programmare un messaggio. [Movimenti](activity.md) mostra quando un messaggio è stato programmato, modificato, annullato, inviato o non inviato.
