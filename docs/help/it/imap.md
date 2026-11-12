---
title: Altra email (IMAP)
area: connections
summary: La posta di qualsiasi provider con IMAP, come iCloud, Yahoo, Fastmail, Telenet o il tuo dominio. Per ora legge soltanto.
covers: connector:imap
code: imap_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
---
## Cosa legge

La tua posta in arrivo e la cartella Inviata: gli ultimi 7 giorni quando colleghi, poi tutto ciò che è nuovo. Conta anche la posta che invii: così impara come scrivi e cosa hai promesso. Le altre cartelle non vengono lette.

Nella tua casella non cambia nulla. La posta non viene segnata come letta.

## Cosa può fare

Per ora legge soltanto: non può ancora inviare da questa casella. Una risposta preparata per te la copi tu nel tuo programma di posta.

## Collegala

1. Nella dashboard, apri **Connessioni**, poi **+ Aggiungi**, e scegli **Altra email**.
2. Inserisci il tuo indirizzo email e la password.
3. Premi **Collegati**.

Molti provider chiedono una password per le app di posta, non la tua password normale. Creane una nelle impostazioni dell’account del tuo provider:

- iCloud: una password specifica per app su account.apple.com.
- Yahoo: Sicurezza dell’account, Genera password per app.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: la tua normale password della posta Telenet.
- Proton Mail: avvia Proton Mail Bridge sullo stesso computer e usa la password che mostra Bridge.

Le impostazioni del server vengono compilate per la maggior parte dei provider. Il tuo non è stato trovato? Apri **Impostazioni del server** e inserisci quello che il tuo provider indica per le app di posta: server IMAP, porta e sicurezza (SSL/TLS o STARTTLS). The Machine non si collega mai senza TLS.

Gmail o posta Microsoft, anche sul tuo dominio? Scegli invece **Gmail** o **Outlook**. Accedono senza password.

## Se si ferma

- **Il server di posta ha rifiutato la password**: l’hai cambiata, o la password per app è stata rimossa. Collegala di nuovo con quella nuova.
- **Il server di posta non è raggiungibile**: riprova da sola. Se continua a non riuscire, controlla il nome del server in Impostazioni del server.

## Rimuovila

**Connessioni**, apri l’account, **Dettagli**, poi **Disconnetti**. Smette di leggere e ciò che ha già portato resta. Rimuovi anche la password per app presso il tuo provider.
