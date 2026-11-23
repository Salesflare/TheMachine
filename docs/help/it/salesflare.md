---
title: Salesflare CRM
area: connections
summary: Account, contatti e trattative, così sa chi conta. Legge i dati usando la tua chiave API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 8051c61777603a7e
---
## Cosa legge

I tuoi account, contatti e trattative in Salesflare, e il feed di ogni account: le email dei colleghi a cui non eri in copia e le riunioni con le relative note.

## Cosa può modificare

Niente. (Sul tuo computer, l’impostazione `join_pipelines` può aggiungerti agli account nelle pipeline che scegli. È disattivata per impostazione predefinita.)

## Collegarla

1. In Salesflare, apri [Impostazioni, chiavi API](https://app.salesflare.com/#/settings/apikeys) e crea una chiave.
2. Su una Machine ospitata: apri la pagina di configurazione su app.themachine.computer/setup, vai a **Altre fonti**, apri Salesflare CRM, incolla la chiave e premi **Collega**.
3. Nella dashboard: **Connessioni**, **Clienti**, Salesflare CRM, incolla la chiave e premi **Collega**. La scheda mostrerà a che punto è.

## Dettagli della sincronizzazione

In **Connessioni**, **Clienti**, Salesflare mostra a che punto è: gli account controllati in questo ciclo, quelli eventualmente saltati perché Salesflare era troppo lento e quelli che la tua chiave API non può aprire (**senza accesso**). Se un ciclo dura ore, viene indicato che potrebbe essersi bloccato.

Le schede mostrano quanti account ha letto questa settimana e quante email e riunioni ha importato.

Non c’è nulla da fare se alcuni account non sono accessibili: il resto viene importato normalmente. Se la tua chiave API non può aprire nessun account, la scheda mostra **Serve il tuo aiuto**: usa la chiave di un utente che può vederli. Una nuova chiave riparte da zero e legge di nuovo l’ultima settimana. Se Salesflare continua a interrompere la connessione, ma ogni nuovo tentativo riesce, viene indicato che Salesflare è **a volte lento**.

Se Salesflare non ha attivato l’accesso al feed tramite chiavi API per il tuo team, la scheda te lo segnala: non verranno importate email o riunioni finché il supporto di Salesflare non lo attiva. Il controllo viene ripetuto ogni 10 minuti il primo giorno, poi circa ogni ora. Quando funziona, la sincronizzazione riprende automaticamente.

- **Ferma**: non verrà importato nulla di nuovo finché non premi **Inizia**. La sincronizzazione riprende da dove si era interrotta.
- **Riavvia sincronizzazione**: ricomincia da zero e legge di nuovo l’ultima settimana. Non perderai nulla di ciò che è già stato importato.
- **Chiavi API**: apre la pagina delle chiavi API di Salesflare per crearne una nuova.

## Rimuoverla

- Nella dashboard: **Connessioni**, apri Salesflare, **Dettagli**, poi **Disconnetti**. I dati già importati restano.
- Su una Machine ospitata, puoi anche premere **Rimuovi** accanto a Salesflare nella pagina di configurazione.

## Revocare l’accesso in Salesflare

Elimina la chiave API in Salesflare, in Impostazioni, Chiavi API.
