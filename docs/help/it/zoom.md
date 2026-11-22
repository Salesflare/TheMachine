---
title: Zoom
area: connections
summary: Riepiloghi e trascrizioni delle riunioni che ospiti, generati da AI Companion. Legge soltanto.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
translated: 9533caa1429fb3fc
---
## Cosa legge

Il riepilogo di AI Companion per ogni riunione Zoom che ospiti e la relativa trascrizione, se disponibile su Zoom: gli ultimi 7 giorni al momento della connessione, poi le nuove man mano che arrivano. Legge anche il tuo nome e il tuo indirizzo email su Zoom, per sapere a chi appartengono le riunioni.

I riepiloghi richiedono un piano Zoom a pagamento, AI Companion attivo durante la riunione e la crittografia end-to-end disattivata.

## Cosa ne fa

Abbina ogni riepilogo alla riunione corrispondente nel tuo calendario. Lo mostra nelle **Note** della riunione e la trascrizione nella **Trascrizione**, contrassegnata come **Da Zoom**, accanto a tutto ciò che hai aggiunto. La tua Machine crea attività a partire dai prossimi passi che spettano a te. Non viene inviato nulla finché non lo invii tu.

## Cosa può fare

Legge soltanto le tue riunioni. Non crea, modifica né elimina mai nulla su Zoom. La sessione di accesso a Zoom resta sulla tua Machine.

## Connettilo

Su una Machine ospitata:

1. Apri la pagina di configurazione su app.themachine.computer/setup e vai a **Altre fonti**.
2. Apri Zoom, scegli lavoro o personale e premi **Connetti a Zoom**.
3. Accedi a Zoom e autorizza The Machine (di Salesflare).

Oppure, nella dashboard: apri **Connessioni**, poi **Riunioni**, scegli Zoom e premi **Accedi con Zoom**. Al termine, tornerai alla dashboard.

Sul tuo computer, una volta [associata al tuo account](friends.md#a-machine-on-your-own-computer): apri **Connessioni**, poi **Riunioni**, scegli Zoom e premi **Accedi con Zoom**.

## Rimuovilo

- Nella dashboard: apri **Connessioni**, poi Zoom e **Dettagli**, quindi **Disconnetti**. Smetterà di leggere. I contenuti già importati restano.
- Su una Machine ospitata puoi anche premere **Rimuovi** accanto a Zoom nella pagina di configurazione.

## Disinstallalo su Zoom

Accedi su marketplace.zoom.us, apri Manage, poi Added Apps e rimuovi The Machine. Non potrà più leggere nulla. I contenuti già importati resteranno sulla tua Machine finché non li elimini: consulta [Annullare e eliminare](cancel-and-delete.md).
