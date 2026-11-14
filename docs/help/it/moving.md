---
title: Passa a un altro computer
area: getting-started
summary: Esporta tutto ciò che la tua Machine sa in un unico file crittografato e importalo su un’altra Machine, ospitata o tua.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
translated: a08d8cd091c7d47b
---
Tutto ciò che la tua Machine impara è tuo: messaggi, attività, bozze, Graph, ricordi e skill. Trasferisci tutto su un’altra Machine o conserva una copia.

## Esportazione

Sul tuo computer:

1. Vai in **Impostazioni** › **Generale** › **Esporta** e premi **Esporta** accanto a Tutto.
2. Se vuoi, scegli una passphrase. Se non ne imposti una, ricevi un codice di esportazione: annotalo, ti servirà per l’importazione.
3. Se vuoi, attiva **Includi chiavi e token** (richiede una passphrase), così non dovrai collegare di nuovo le tue fonti.
4. Premi **Avvia esportazione**, poi **Scarica**. Il file viene eliminato dopo 24 ore oppure subito se premi **Elimina**.

Su una Machine ospitata, **Esporta** accanto a Tutto apre la pagina del tuo account. Premi **Esporta tutto**, poi **Scarica**. La tua Machine elimina il file dopo 24 ore oppure subito se premi **Elimina ora**.

Il file è sempre crittografato. In Impostazioni puoi vedere cosa contiene e cosa no. Per gli account Google e Microsoft collegati tramite il nostro accesso ospitato, dovrai accedere di nuovo sull’altra Machine.

## Importazione

1. Vai in **Impostazioni** › **Generale** › **Esporta**, premi **Scegli file** accanto a Importa e seleziona l’esportazione.
2. Inserisci la passphrase o il codice di esportazione e premi **Apri**. La Machine controlla prima tutto il file.
3. Su una Machine ospitata, premi **Importa ora**. Sul tuo computer, premi **Sostituisci con questa esportazione**, poi **Sostituisci**. La Machine si riavvia con i dati importati entro pochi minuti e in Impostazioni compare **Importata**.

L’importazione sostituisce i dati presenti sulla Machine, dopo averne conservato una copia. Non viene inviato nulla automaticamente: gli invii in coda aspettano una tua conferma.

Se Impostazioni non riesce a riavviare The Machine sul tuo computer, ti mostra i comandi da eseguire.

Su un nuovo computer, [installa The Machine](self-hosted-setup.md) prima. Poi annulla il tuo piano ospitato se non ti serve più: consulta [Annulla o elimina](cancel-and-delete.md).
