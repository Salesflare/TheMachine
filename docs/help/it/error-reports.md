---
title: Segnalazioni di errore
area: security
summary: Quando qualcosa si rompe, la tua Machine dice al team di The Machine cosa non ha funzionato e in che punto del codice. Mai i tuoi messaggi, nomi o indirizzi.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html
order: 4
---
## Cos'è

Quando qualcosa in The Machine si rompe, la tua Machine manda al team una breve firma dell'errore, così possiamo correggerlo prima che qualcuno debba segnalarlo. È attivo di default e serve [The Machine Network](/network).

## Cosa viene inviato

Solo questo, per ogni tipo di errore:

- il tipo di errore, come `KeyError` o `TypeError`;
- il suo messaggio, senza niente di specifico: numeri, id, testo tra virgolette, indirizzi email, link, percorsi di file e tutto ciò che sembra una chiave. Viene tolta anche ogni altra parola che potrebbe essere un nome;
- dove è successo nel codice di The Machine: file, funzione e riga, mai una cartella sul tuo computer;
- la versione dell'app, quante volte è successo, e quando la prima e l'ultima volta.

Un esempio vero: `IndexError`, `list index out of range`, in `assistant.py:fault_event:7899`, versione `05b17ee6ac79`, 1 volta.

## Cosa non viene mai inviato

Cosa dicono i tuoi messaggi, le attività, le bozze o le chat. Nomi, indirizzi email, numeri di telefono, link, token o password. Di quale account o persona si trattava.

## Da dove vengono gli errori

- il servizio e i suoi job: revisioni, preparazione delle attività, chat, connessioni e sincronizzazioni;
- la dashboard nel tuo browser;
- i job di Claude Code e Codex che falliscono: solo lo strumento e il tipo di errore.

Lo stesso errore conta una volta, con un conteggio. Al massimo un invio ogni 10 minuti. Il team li conserva 30 giorni.

## Ritmo

Il lavoro in background aspetta quando i limiti del tuo piano AI si esauriscono, per lasciare spazio alle tue chat (vedi [Il tuo modello AI](model.md)). Con le segnalazioni di errore attive, la tua Machine dice al team, una volta al giorno, quante volte è successo: per ogni volta, l'ora in cui è iniziato, quale limite, quanti minuti è durato e quanti lavori hanno aspettato. Solo conteggi e minuti, niente sui lavori.

## Disattivalo

In Impostazioni, Sicurezza, disattiva **Invia segnalazioni di errore**. Non viene più registrato né inviato niente, compresi i conteggi sul ritmo, e ciò che era in attesa viene eliminato. Gli errori restano visibili sulla tua Machine, che può proporre una correzione.

Vedi [Sicurezza e privacy](security-and-privacy.md).
