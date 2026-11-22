---
title: Salesflare CRM
area: connections
summary: Account, contatti e trattative, così sa chi conta. Legge i dati usando la tua chiave API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 3d6041d568843d96
---
## Cosa legge

I tuoi account, contatti e trattative in Salesflare, e il feed di ogni account: email dei colleghi a cui non eri in copia e riunioni con note.

## Cosa può modificare

Niente. (Sul tuo computer, l’impostazione `join_pipelines` può aggiungerti agli account nelle pipeline che scegli. Per impostazione predefinita è disattivata.)

## Collegalo

1. In Salesflare, apri [Impostazioni, chiavi API](https://app.salesflare.com/#/settings/apikeys) e crea una chiave.
2. Su una Machine ospitata: apri la pagina di configurazione su app.themachine.computer/setup, vai a **Altre fonti**, apri Salesflare CRM, incolla la chiave e premi **Collega**.
3. Nella dashboard: **Connessioni**, **Clienti**, Salesflare CRM, incolla la chiave e premi **Collega**. La scheda mostrerà a che punto è.

## Dettagli della sincronizzazione

In **Connessioni**, **Clienti**, Salesflare mostra l’avanzamento: gli account letti in questo ciclo e quelli eventualmente saltati perché Salesflare era troppo lenta. Se un ciclo dura ore, viene indicato che potrebbe essersi bloccato.

I riquadri indicano quanti account è riuscita ad aprire e quante email e riunioni ha importato. Se la tua chiave API non consente a Salesflare di aprire nessun account, la scheda mostra **Serve il tuo aiuto**: usa la chiave di un utente che può visualizzarli. Se Salesflare va spesso in timeout, ma riesce a completare ogni nuovo tentativo, indica che è **a volte lenta**.

Se Salesflare non ha attivato per il tuo team l’accesso al feed tramite chiavi API, la scheda te lo segnala: non riceverai email o riunioni finché il supporto Salesflare non lo attiva. La verifica viene ripetuta ogni 10 minuti il primo giorno, poi circa ogni ora. Quando l’accesso funziona, la sincronizzazione riprende automaticamente.

- **Ferma**: non riceverai nuovi dati finché non premi **Avvia**. La sincronizzazione riprende da dove si era fermata.
- **Riavvia sincronizzazione**: ricomincia da capo e legge di nuovo i dati dell’ultima settimana. I dati già importati non vengono persi.
- **Chiavi API**: apre la pagina delle chiavi API di Salesflare, dove puoi crearne una nuova.

## Rimuovila

- Nella dashboard: **Connessioni**, apri Salesflare, **Dettagli**, poi **Disconnetti**. I dati già importati restano.
- Su una Machine ospitata puoi anche premere **Rimuovi** accanto a Salesflare nella pagina di configurazione.

## Revoca l’accesso in Salesflare

Elimina la chiave API in Salesflare, in Impostazioni, chiavi API.
