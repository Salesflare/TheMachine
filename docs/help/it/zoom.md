---
title: Zoom
area: connections
summary: I riepiloghi e le trascrizioni di AI Companion delle riunioni che organizzi. Legge soltanto.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
---
## Cosa legge

Il riepilogo di AI Companion di ogni riunione Zoom che organizzi, e la trascrizione quando Zoom ne ha una: gli ultimi 7 giorni quando lo colleghi, poi quelle nuove man mano che arrivano. Legge anche il tuo nome e la tua email su Zoom, per sapere di chi sono le riunioni.

I riepiloghi richiedono un piano Zoom a pagamento, AI Companion attivo durante la riunione e nessuna crittografia end-to-end.

## Cosa ne fa

Ogni riepilogo viene abbinato alla riunione nel tuo calendario. Il riepilogo compare nelle **Note** di quella riunione e la trascrizione nella sua **Trascrizione**, segnati **Da Zoom**, accanto a ciò che hai aggiunto lì, senza mai sostituirlo. Le tue revisioni lo usano poi per i follow-up di quella riunione, e la suddivisione dei follow-up per la Fleet arriva già compilata con chi fa cosa. Prima la controlli e la modifichi; non parte nulla finché non la invii tu.

## Cosa può fare

Legge soltanto. Non crea, non cambia e non elimina mai nulla in Zoom, e vede solo le tue riunioni. Il tuo accesso a Zoom resta sulla tua Machine.

## Collegalo

Su una Machine ospitata:

1. Apri la tua pagina di configurazione su app.themachine.computer/setup e vai su **Altre fonti**.
2. Apri Zoom, scegli lavoro o personale e premi **Collega Zoom**.
3. Accedi a Zoom e autorizza The Machine. È fatta da Salesflare.

Oppure nella dashboard: **Connessioni**, **+ Aggiungi**, scegli Zoom e premi **Accedi con Zoom**. Quando hai finito, torni alla dashboard.

Sul tuo computer, quando è [abbinato al tuo account](friends.md#a-machine-on-your-own-computer): apri **Connessioni**, poi **+ Aggiungi**, scegli Zoom e premi **Accedi con Zoom**.

## Rimuovilo

- Nella dashboard: **Connessioni**, apri Zoom, **Dettagli**, poi **Disconnetti**. Smette di leggere. Ciò che ha già portato dentro resta.
- Su una Machine ospitata puoi anche premere **Rimuovi** accanto a Zoom nella tua pagina di configurazione.

## Disinstallalo su Zoom

Accedi su marketplace.zoom.us, apri Manage, poi Added Apps, e rimuovi The Machine. Non può più leggere nulla. Ciò che ha già portato dentro resta sulla tua Machine finché non lo elimini: vedi [Annulla ed elimina](cancel-and-delete.md).
