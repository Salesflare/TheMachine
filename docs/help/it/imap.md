---
title: Altra email (IMAP)
area: connections
summary: Email di qualsiasi provider con IMAP, come iCloud, Yahoo, Fastmail, Telenet o il tuo dominio.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
translated: a21e9d52d723f351
---
## Cosa legge

La posta in arrivo e la cartella Inviati: gli ultimi 7 giorni quando colleghi l’account, poi tutti i nuovi messaggi. Conta anche la posta che invii, così impara come scrivi e cosa hai promesso. Le altre cartelle non vengono lette.

La tua casella di posta non viene modificata, a parte una copia dei messaggi inviati da The Machine, nella cartella Inviati. I messaggi non vengono contrassegnati come letti.

## Cosa può fare

Invia email solo dopo che premi **Invia**, attraverso il server di posta del tuo provider (SMTP) e con la stessa password. Una copia viene salvata nella cartella Inviati. Le risposte restano nella stessa conversazione e la firma è quella delle **Impostazioni**, oppure quella che compare in fondo ai messaggi che invii.

## Collegala

1. Nella dashboard, apri **Connessioni**, poi **Email** e scegli **Altra email**.
2. Inserisci il tuo indirizzo email e la password.
3. Premi **Collega**.

Molti provider richiedono una password per app di posta, non la password normale. Creane una nelle impostazioni del tuo account:

- iCloud: una password specifica per app su account.apple.com.
- Yahoo: Sicurezza dell’account, Genera password per app.
- Fastmail: Impostazioni, Privacy e sicurezza, Password per app.
- Telenet: la tua normale password di posta Telenet.
- Zoho Mail con autenticazione a due fattori: una password specifica per app nel tuo account Zoho, alla voce Sicurezza.
- Proton Mail: avvia Proton Mail Bridge sullo stesso computer e usa la password indicata da Bridge. Funziona solo con The Machine su quel computer. The Machine mostra l’impronta digitale del certificato di Bridge e si fida solo di quel certificato.

Le impostazioni del server sono già compilate per la maggior parte dei provider. Non trovi il tuo? Apri **Impostazioni del server** e inserisci i dati forniti dal tuo provider per le app di posta: i server IMAP e SMTP, le porte e il tipo di sicurezza (SSL/TLS o STARTTLS). The Machine non si connette mai senza TLS.

Usi Gmail o la posta Microsoft, anche con il tuo dominio? Scegli **Gmail** o **Outlook**. Puoi accedere senza password. Anche i server inseriti in Impostazioni del server vanno configurati lì: Microsoft non accetta più le password delle app di posta.

Hai inserito un indirizzo Microsoft 365? Il modulo lo rileva e mostra **Accedi con Microsoft** al posto del campo password. Si apre la schermata di accesso di Outlook. Se l’indirizzo non viene rilevato entro pochi secondi, il modulo della password resta disponibile.

## Quando smette di funzionare

- **Il server di posta ha rifiutato la password**: l’hai cambiata oppure la password per app è stata rimossa. Collega di nuovo l’account con quella nuova.
- **Il server di posta ha rifiutato la password per l’invio**: non è stato inviato nulla. Collega di nuovo l’account; se il server continua a rifiutarla, controlla il server SMTP in Impostazioni del server. Nel frattempo, l’account può solo leggere la posta.
- **Il server di posta non è raggiungibile**: riprova automaticamente. Se continua a non funzionare, controlla il nome del server in Impostazioni del server.
- **Il certificato del server di posta è valido per** un altro nome: con l’hosting condiviso, spesso il server risponde con il proprio nome. Inserisci il nome indicato in Impostazioni del server. The Machine non ignora mai il controllo del certificato.

## Rimuovila

**Connessioni**, apri l’account, **Dettagli**, poi **Disconnetti**. L’account smette di leggere la posta e i messaggi già importati restano. Rimuovi anche la password per app dal tuo provider.
