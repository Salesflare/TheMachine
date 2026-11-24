---
title: Sicurezza e privacy
area: security
summary: La tua Machine privata, email archiviate in modo cifrato e nulla viene inviato senza il tuo OK. In breve, con i link per saperne di più.
covers:
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: 27c910c92b215ad3
---
## In breve

- La tua Machine: se è ospitata, funziona nel cloud nell’UE, solo per te e mai condivisa. Oppure puoi usarla sul tuo computer.
- Non leggiamo le tue email: i messaggi sono archiviati in modo cifrato e i nostri strumenti di assistenza non possono aprirli.
- Nulla viene inviato senza il tuo OK: la tua Machine legge e prepara bozze, ma decidi tu cosa inviare. Vedi [Fallo](do-it.md).
- I tuoi dati non vengono usati per addestrare l’IA: non abbiamo una nostra IA. Il tuo provider opera con il tuo account e secondo i suoi termini.
- Apprendimenti per il team, a meno che tu non li disattivi: ogni tanto vengono condivisi alcuni suggerimenti generali, mai personali, dopo una verifica. Vedi [Condividi gli apprendimenti](share-learnings.md).
- Segnalazioni di errore, a meno che tu non le disattivi: quando qualcosa non funziona, includono il tipo di errore e il punto del codice in cui si è verificato. Mai i tuoi messaggi, nomi o indirizzi. Vedi [Segnalazioni di errore](error-reports.md).
- Conteggi di utilizzo su una Machine ospitata: conteggi giornalieri delle tue attività, come le attività aperte o le email inviate, mai il loro contenuto. Rileviamo anche quanto impiega la dashboard ad aprirsi, solo i tempi di caricamento, da telefono o computer, app o browser.
- Puoi portare i tuoi dati con te o eliminarli: esporta tutto da **Impostazioni** › **Generale** oppure elimina la tua Machine e i relativi backup con un solo pulsante. Vedi [Disdici o elimina](cancel-and-delete.md).
- I nostri accessi vengono registrati: ogni volta che il team legge il report o i log della tua Machine ospitata. I proprietari e gli amministratori di Fleet li vedono in **Movimenti**. Vedi [Fleet](fleet.md).

## Backup

Una Machine ospitata esegue ogni notte il backup dei tuoi dati. Il backup viene cifrato sulla tua Machine prima di essere trasferito e poi archiviato in Microsoft Azure nei Paesi Bassi (UE). Conserviamo gli ultimi 7 backup giornalieri, 4 settimanali e 3 mensili, per circa 3 mesi. Vengono eliminati quando elimini la tua Machine.

Possiamo aprirli? Sì, per ripristinare una Machine non funzionante: la chiave è in nostro possesso, ma viene conservata separatamente dai backup. I messaggi nel backup vengono cifrati una seconda volta con un’altra chiave, anch’essa in nostro possesso, custodita separatamente e mai inclusa nel backup.

I backup sono una rete di sicurezza. Conserva una copia di ciò che non puoi perdere: **Tutto**, in **Impostazioni** › **Generale** › **Esporta**. Vedi [Passa a un altro computer](moving.md).

Sul tuo computer non viene eseguito alcun backup automatico e noi non abbiamo una copia. È sufficiente un backup cifrato ogni notte della cartella principale: vedi [Per iniziare](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md#later).

## Livelli di sicurezza

**Standard** mantiene le impostazioni predefinite di oggi. **Prudente** non mostra testo nelle notifiche, non salva gli accessi e conserva meno dati. L’amministratore di una Fleet di lavoro può impostare la Fleet come Prudente. Vedi [Livelli di sicurezza](security-levels.md).

## Accesso

Per accedere alla dashboard di una Machine ospitata serve una passkey oppure l’accesso con Google o Microsoft insieme a un codice di autenticazione.

## Connessioni

L’articolo di ogni connessione spiega cosa legge e cosa può inviare. Puoi disconnetterle in qualsiasi momento: vedi [Connessioni](connections.md).

## Aiuto

L’Aiuto funziona sulla tua Machine e non può vedere i tuoi dati. Al team di The Machine viene inviato solo l’argomento di ogni domanda, mai le tue parole. Vedi [Chiedi aiuto](help-chat.md#what-the-team-sees).

## Altro

- [Sicurezza](/security): come è stata realizzata, cosa il nostro team può e non può vedere e come cerchiamo eventuali problemi.
- [Informativa sulla privacy](/privacy) e [termini sul trattamento dei dati](/dpa).
- Hai trovato un problema di sicurezza? Consulta la [politica di sicurezza](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md).
