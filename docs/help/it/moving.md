---
title: Passa a un altro computer
area: getting-started
summary: Esporta tutto ciò che la tua Machine sa in un unico file cifrato e importalo su un’altra Machine, ospitata o tua.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
---
Tutto ciò che la tua IA impara è tuo: messaggi, conversazioni, attività con la loro cronologia, bozze, il Graph, ricordi, skill e lavori degli agenti. Puoi portare tutto con te, anche se smetti di usare The Machine.

## Esportare

Sul tuo computer:

1. In **Impostazioni** › **Generale** › **Esporta**, premi **Esporta** accanto a Tutto.
2. Se vuoi, scegli una passphrase. Senza, ricevi un codice di esportazione: annotalo, l’importazione ne ha bisogno.
3. Se vuoi, attiva **Includi chiavi e token** (serve una passphrase), così non devi ricollegare le tue fonti.
4. Premi **Avvia esportazione** e poi **Scarica**. Il file viene eliminato dopo 24 ore, o subito con **Elimina**.

Su una Machine ospitata, **Esporta** accanto a Tutto apre la pagina del tuo account. Premi **Esporta tutto** e poi **Scarica**. La tua Machine elimina il file dopo 24 ore, o subito con **Eliminalo ora**.

Il file è sempre cifrato. Dopo un’esportazione, Impostazioni mostra cosa contiene, con i numeri, e cosa non contiene e perché. Gli accessi a Google e Microsoft tramite il servizio ospitato richiedono sempre un nuovo accesso dall’altra parte.

## Importare

1. In **Impostazioni** › **Generale** › **Esporta**, premi **Scegli file** accanto a Importa e scegli l’esportazione.
2. Digita la sua passphrase o il codice di esportazione e premi **Apri**. The Machine controlla prima tutto il file.
3. Ospitata: premi **Importa ora**. The Machine si riavvia con essa tra pochi minuti. Sul tuo computer: premi **Sostituisci con questa esportazione**, poi **Sostituisci**. The Machine si riavvia con essa tra un paio di minuti e le Impostazioni mostrano **Importata**.

L’importazione sostituisce ciò che quella Machine ha ora e prima ne conserva una copia. Niente di ciò che era in attesa parte da solo: gli invii in coda aspettano che tu li rinvii.

Avanzato: su un computer dove The Machine gira senza gestore dei servizi, le Impostazioni mostrano i comandi. Puoi anche eseguirli tu: `assistant service stop`, `assistant import --staged --force`, `assistant service start`.

Su un nuovo computer, [installa prima The Machine](self-hosted-setup.md). Poi annulla il piano ospitato se non ti serve più: vedi [Annullare o eliminare](cancel-and-delete.md).
