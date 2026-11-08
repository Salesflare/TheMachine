---
title: Routine
area: cards
summary: Lavoro che la tua Machine fa da sola, con un ritmo, come un riepilogo del lunedì dei tuoi deal aperti. Legge soltanto.
covers: tab:routines
code: routines.py, routines_app.py, routine_imports.py, routine_patterns.py, dashboard/routines-page.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report, suggested, digest, newsletter
---
## Crearne una

Apri **Routine** nella barra laterale e di’ in una riga cosa deve fare e quando: "ogni lunedì alle 9, riassumi i miei deal aperti" o "ogni giorno feriale al mattino, elenca le email a cui devo ancora rispondere". Poi **Aggiungi**.

Senza un orario, gira alle 8:00. L’orario è quello dell’orologio della tua Machine.

## Cosa fa una routine

All’orario stabilito, la tua Machine legge ciò che le serve, come i tuoi messaggi, le riunioni e il Graph, e mette il risultato nella pagina Routine. Ogni risultato dice **Pronta**, **Niente di nuovo** (con il perché) o **Non è andato** (con il perché). Un’esecuzione che finisce senza risultato conta come non riuscita, mai come fatta.

Le routine leggono soltanto. Non inviano, rispondono, pubblicano né cambiano nulla.

Ogni esecuzione conosce l’ultimo risultato, così può dire cosa è cambiato da allora.

## Giorni persi

Se la tua Machine era spenta o occupata, le esecuzioni perse non si accumulano: gira solo la più recente, una volta. Ogni data gira una volta, anche dopo un riavvio.

Le routine girano una alla volta e aspettano quando l’uso del tuo piano IA è basso, come tutto il lavoro in background. **Esegui ora** la esegue subito.

## Cambiarla o fermarla

È nel menu ⋯ della routine. **Cambia quando** prende un nuovo ritmo con parole tue, come "ogni giorno feriale alle 8". **Metti in pausa** ferma le esecuzioni fino a **Riprendi**; ciò che è stato perso durante la pausa non gira dopo. **Ferma** chiude una routine per sempre.

## Passaggi di script

Una routine può eseguire i tuoi comandi sulla tua Machine. In **Modifica**, apri **Passaggi di script**. **Recupera dati** esegue prima un comando, come `python3 ~/scripts/deals.py`, nella sua cartella (vuota: la tua cartella home) e al massimo per i suoi secondi. Ciò che stampa va all’esecuzione per lavorarci. Senza parole, ciò che stampa è il risultato.

**Verifica** riceve il risultato come input dopo l’esecuzione. Se termina con un errore, l’esecuzione mostra **Non è andato** con ciò che ha detto la verifica. Un comando di Recupera dati che fallisce si mostra allo stesso modo.

Un comando è una riga e gira senza shell: niente pipe né variabili. I passaggi di script sono tuoi, si impostano solo sulla tua dashboard. Un’esecuzione di prova e **Provalo** eseguono anche Recupera dati e lo dicono; comunque non inviano e non tengono nulla. Una routine non invia mai, quindi un passaggio di script dovrebbe solo leggere.

## Dai tuoi job di OpenClaw

Se prima avevi creato job pianificati in OpenClaw, la tua Machine li legge (non li cambia mai) e propone quelli adatti come routine in **Suggerito**. Ognuno è stato eseguito una volta, così vedi un risultato vero.

Tiene le tue correzioni al job e lascia fuori ciò che inviava o pubblicava. Un job che eseguiva uno script, o leggeva ciò che raccoglieva un job di script, lo porta come Recupera dati. **Aggiungi** ne fa una routine, **No, grazie** non chiede mai più di quel job. Un job che ti ricordava di fare qualcosa arriva invece come offerta di attività ricorrente in Attività.

Aspettano al massimo tre suggerimenti alla volta. Dopo una settimana di buone esecuzioni, la routine chiede **Disattivare il vecchio job di OpenClaw?** Si disattiva solo quando tocchi **Disattiva**, e puoi riattivarlo in OpenClaw.

## Da quello che fai

La tua Machine nota anche il lavoro che fai con un ritmo e lo propone come routine in **Suggerito**, anche senza OpenClaw. Cerca:

- la stessa richiesta, tre volte o più di fila, come "riassumi i ticket di supporto aperti" ogni lunedì;
- un’email che invii con un ritmo, come un report settimanale al tuo team;
- newsletter ed email di aggiornamento che arrivano ogni settimana;
- un canale Slack molto attivo dove altri scrivono ogni settimana.

Ogni suggerimento dice cosa ha visto, come "Chiesto 4 volte di fila", ed è stato eseguito una volta perché tu veda un risultato vero. Pensa a un riepilogo del team, un brief prima di una call settimanale, un riepilogo del supporto o dello sviluppo, il polso dei tuoi numeri o un riassunto delle newsletter che ricevi.

Propone solo ciò che è tuo e chiaramente utile: un riassunto di notizie solo sulle tue newsletter, mai uno generico. Quando niente va bene, non c’è nessun suggerimento. Guarda al massimo una volta al giorno, e tutto resta sulla tua Machine. Un’attività che chiudi con un ritmo arriva invece come offerta di attività ricorrente.

## Routine e attività ricorrenti

Un’attività ricorrente (recurring.md) ti ricorda di fare qualcosa. Una routine è lavoro che la tua Machine fa da sola e ti mostra. Usa un’attività ricorrente per "pagare l’affitto il primo del mese", e una routine per "ogni venerdì, dimmi quali deal si sono fermati".
