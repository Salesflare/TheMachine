---
title: Problemi sul tuo computer
area: troubleshooting
summary: La tua Machine legge i log del computer e ti segnala i problemi reali, spiegandone la causa e come risolverli. Una soluzione viene applicata solo quando tocchi Fallo.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: b18e5f4989d6baff
---
## Cosa legge

Su Linux con systemd, la tua Machine legge il log della tua sessione utente: i tuoi servizi e i rapporti di arresto anomalo dei tuoi programmi. Su Omarchy controlla anche Hyprland e la barra. Non legge mai il log dell’intero sistema e non chiede mai autorizzazioni aggiuntive.

Legge quale servizio si è fermato, come è terminato e quale programma si è arrestato in modo anomalo. Non legge mai il contenuto delle righe di log, quindi il testo dei log non viene conservato né lascia il tuo computer.

## Cosa viene considerato un problema

Un servizio che continua a riavviarsi, uno che ha avuto diversi errori in un giorno o resta inattivo, uno che ha esaurito la memoria e un programma che si è arrestato in modo anomalo. Su Omarchy, anche un arresto anomalo di Hyprland o della barra e gli errori nelle impostazioni di Hyprland.

Un singolo riavvio o un singolo errore di esecuzione sono normali e non generano notifiche. Lo stesso vale per un servizio che ha avuto qualche errore, ma poi è tornato a funzionare correttamente, e per un servizio inattivo che non deve essere avviato: non è abilitato e nessun altro servizio o timer lo avvia.

I browser controllati da test e agenti (headless, Playwright, Puppeteer, CI) non generano notifiche. Lo stesso vale per un programma che si chiude mentre il suo servizio viene arrestato o riavviato. Non generano notifiche nemmeno le esecuzioni di sviluppo: ciò che esegue un agente di programmazione, i test e i programmi avviati da una cartella temporanea o di cache. Se un programma si arresta in modo anomalo più volte, viene creata un’attività che indica quante volte è successo e quando.

Uno script viene indicato con il suo nome, per esempio backup.py, non con python3 o node.

## Cosa ricevi

Un’attività che spiega in parole semplici cosa è successo, perché è importante e cosa puoi fare. I comandi che mostrano il motivo si trovano sotto **Mostra altro**. Chiedi nella sua chat e The Machine indagherà. Ogni modifica che apporta resta in sospeso finché non dai il tuo OK, come quando tocchi **Fallo**.

Quando c’è una soluzione sicura, l’attività include **Fallo**. Se un tuo servizio resta inattivo, lo riavvia; su Omarchy, riavvia anche la barra. **Fallo** esegue solo quel comando e il risultato appare nella chat dell’attività. Non interviene mai sui servizi di The Machine stessa né sull’OpenClaw Gateway.

Per lo stesso problema viene creata al massimo un’attività ogni due settimane, e mai se la relativa attività è ancora aperta. Al massimo due nuove attività al giorno. Un’attività relativa a un servizio inattivo si chiude da sola quando il servizio riparte o il problema viene risolto.

## In un terminale

`assistant doctor` elenca gli stessi problemi dell’ultimo giorno.

## Altri computer

Su macOS, Windows e sui computer senza systemd, non legge nulla e lo segnala in `assistant doctor`.

Su una Machine ospitata, ci occupiamo noi di tenere in funzione il server: i problemi vengono segnalati al team di The Machine, non a te sotto forma di attività.

## Disattivarlo

Imposta `"computer_logs": false` in config.json e riavvia il servizio.
