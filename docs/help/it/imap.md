---
title: Altra email (IMAP)
area: connections
summary: La posta di qualsiasi provider con IMAP, come iCloud, Yahoo, Fastmail, Telenet o il tuo dominio.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
---
## Cosa legge

La tua posta in arrivo e la cartella Inviata: gli ultimi 7 giorni quando colleghi, poi tutto ciò che è nuovo. Conta anche la posta che invii: così impara come scrivi e cosa hai promesso. Le altre cartelle non vengono lette.

Nella tua casella non cambia nulla, tranne una copia di ciò che The Machine invia, nella cartella Inviata. La posta non viene segnata come letta.

## Cosa può fare

Invia un’email solo quando premi Invia, tramite il server di posta del tuo provider (SMTP) con la stessa password. Una copia va nella cartella Inviata. Le risposte restano nella loro conversazione, e la tua firma è quella delle Impostazioni, altrimenti quella con cui finisce la tua posta inviata.

## Collegala

1. Nella dashboard, apri **Connessioni**, poi **Email**, e scegli **Altra email**.
2. Inserisci il tuo indirizzo email e la password.
3. Premi **Collegati**.

Molti provider chiedono una password per le app di posta, non la tua password normale. Creane una nelle impostazioni dell’account del tuo provider:

- iCloud: una password specifica per app su account.apple.com.
- Yahoo: Sicurezza dell’account, Genera password per app.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: la tua normale password della posta Telenet.
- Zoho Mail con l’autenticazione a due fattori: una password specifica per l’applicazione nel tuo account Zoho, in Sicurezza.
- Proton Mail: avvia Proton Mail Bridge sullo stesso computer e usa la password che mostra Bridge. Funziona solo con The Machine su quello stesso computer. The Machine mostra l’impronta del certificato di Bridge e si fida solo di quello.

Le impostazioni del server vengono compilate per la maggior parte dei provider. Il tuo non è stato trovato? Apri **Impostazioni del server** e inserisci quello che il tuo provider indica per le app di posta: server IMAP e SMTP, le loro porte e la sicurezza (SSL/TLS o STARTTLS). The Machine non si collega mai senza TLS.

Gmail o posta Microsoft, anche sul tuo dominio? Scegli invece **Gmail** o **Outlook**. Accedono senza password. Se scrivi i loro server in Impostazioni del server, ti porta lì lo stesso: Microsoft non accetta più password dalle app di posta.

## Se si ferma

- **Il server di posta ha rifiutato la password**: l’hai cambiata, o la password per app è stata rimossa. Collegala di nuovo con quella nuova.
- **Il server di posta ha rifiutato la password per l’invio**: non è stato inviato nulla. Ricollegala; se continua a rifiutarla, controlla il server SMTP in Impostazioni del server. Fino ad allora legge soltanto.
- **Il server di posta non è raggiungibile**: riprova da sola. Se continua a non riuscire, controlla il nome del server in Impostazioni del server.
- **Il certificato del server di posta è per un altro nome**: con l’hosting condiviso risponde spesso il server del provider. Scrivi il nome mostrato in Impostazioni del server. The Machine non salta mai il controllo del certificato.

## Rimuovila

**Connessioni**, apri l’account, **Dettagli**, poi **Disconnetti**. Smette di leggere e ciò che ha già portato resta. Rimuovi anche la password per app presso il tuo provider.
