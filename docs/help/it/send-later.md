---
title: Invia più tardi
area: cards
summary: Approva un messaggio ora e scegli quando inviarlo. Se ti scrivono prima, torna in attesa di una tua conferma.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, send at a time, delay, tomorrow morning, unsend, take back
translated: 29860e4848acce2e
---
## Programma un messaggio

Nella finestra in cui controlli un messaggio, premi **Invia più tardi** accanto a **Invia ora**. Scegli **Tra 2 ore**, **Domani**, **Lunedì** o **Scegli una data**, poi premi **Salva l’orario**. Il messaggio verrà inviato esattamente come l’hai visto, all’ora scelta nel tuo fuso orario.

Puoi farlo per email, Slack, WhatsApp, Telegram, Signal, Teams e Intercom. Non per LinkedIn e X, perché la tua Machine non può controllare se è arrivato un nuovo messaggio subito prima dell’invio, né per le risposte in un documento.

Puoi farlo anche da **Nuova email**. Se controlli più messaggi insieme, verranno inviati tutti all’ora che scegli.

## Mentre è in attesa

L’attività compare sotto **Torna più tardi** e nel giorno corrispondente del [Calendario](calendar.md), insieme al messaggio e all’orario di invio: «Invio gio 26 nov, 09:30». **Invia ora** lo invia subito, **Cambia orario** ti permette di scegliere un altro momento e **Annulla** lo trasforma di nuovo in una bozza. Lo stesso vale nella chat.

Se modifichi la bozza, completi l’attività, la scarti o la ripristini, il messaggio non parte: serve di nuovo la tua conferma.

## Se ti scrivono prima

Se l’altra persona ti scrive prima dell’invio, la tua Machine non invia il messaggio. L’attività ricompare insieme al suo messaggio, con una nota come «Non inviata: Sam Lee ha scritto prima», e ricevi la notifica che riceveresti per un’attività posticipata. Per le email, vengono considerati i messaggi inviati da qualsiasi indirizzo associato a quella persona che la tua Machine conosce, in qualsiasi casella collegata. Viene considerata anche la risposta di un’altra persona nella conversazione.

Le risposte automatiche, come quelle di assenza dall’ufficio, non bloccano l’invio. Non lo bloccano nemmeno i tuoi messaggi.

Subito prima dell’invio, la tua Machine controlla di nuovo la conversazione. Se non può farlo, l’attività mostra «Non è ancora stato possibile controllare se ci sono nuovi messaggi» e riprova per un’ora. Poi ti chiede cosa fare invece di inviare il messaggio.

Su WhatsApp controlla i messaggi ricevuti fino a quel momento dal tuo account WhatsApp collegato.

## Se la Machine è spenta

Se in quel momento la tua Machine è spenta, in sospensione o disconnessa, il messaggio verrà inviato quando sarà di nuovo disponibile, con un ritardo massimo di un’ora. Se passa più tempo, l’attività ricompare con la nota «Non inviata: il ritardo è stato di più di un’ora» e decidi tu cosa fare.

Quando passi a un altro computer, i messaggi programmati richiedono di nuovo la tua conferma. Scopri di più in [Spostamento](moving.md).

## Chi può programmare un messaggio

Solo tu, dalla dashboard o dall’app. La tua Machine, la sua chat, un’IA collegata e le altre Machine non possono programmare un messaggio. [Movimenti](activity.md) mostra quando un messaggio è stato programmato, modificato, annullato, inviato o non inviato.
