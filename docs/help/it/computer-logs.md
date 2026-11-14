---
title: Problemi sul tuo computer
area: troubleshooting
summary: La tua Machine legge i log del computer e ti segnala i problemi reali, spiegandone la causa e come risolverli. La soluzione viene applicata solo quando tocchi **Fallo**.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: 1a191d8433bfba2a
---
## Cosa legge

Su Linux con systemd, la tua Machine legge i log della tua sessione utente: i tuoi servizi e i rapporti sui crash dei tuoi programmi. Su Omarchy controlla anche Hyprland e la barra. Non legge mai i log dell'intero sistema e non chiede mai autorizzazioni aggiuntive.

Legge quale servizio si è arrestato, come si è concluso e quale programma è andato in crash. Non legge mai il contenuto delle righe di log, quindi il testo dei log non viene conservato né lascia il tuo computer.

## Cosa conta come problema

Un servizio che continua a riavviarsi, che ha avuto diversi errori in un giorno o che resta inattivo, uno che ha esaurito la memoria e un programma andato in crash. Su Omarchy, anche un crash di Hyprland o della barra e gli errori nelle impostazioni di Hyprland.

Un singolo riavvio o una singola esecuzione non riuscita sono normali e non generano avvisi. Lo stesso vale per un servizio che ha avuto qualche errore, ma poi ha ripreso a funzionare normalmente.

I browser controllati da test e agenti (headless, Playwright, Puppeteer, CI) non generano avvisi. Lo stesso vale per un programma che si arresta mentre il suo servizio viene arrestato o riavviato. Non generano avvisi nemmeno le esecuzioni di sviluppo: quelle avviate da un agente di programmazione, i test e i programmi eseguiti da una cartella temporanea o di cache. Se un programma va in crash ripetutamente, viene creata una sola attività che indica quante volte è successo e quando.

Uno script viene indicato con il suo nome, come backup.py, non con python3 o node.

## Cosa ricevi

Un'attività che spiega in parole semplici cosa è successo, perché è importante e cosa puoi fare. I comandi che mostrano la causa sono sotto **Mostra altro**. Scrivi nella chat dell'attività e The Machine indagherà. Ogni modifica che apporta aspetta la tua conferma, proprio come con **Fallo**.

Quando c'è una soluzione sicura, l'attività include **Fallo**. Se un tuo servizio resta inattivo, lo riavvia e, su Omarchy, ripristina la barra. **Fallo** esegue solo quel comando e il risultato compare nella chat dell'attività. Non interviene mai sui servizi di The Machine né su OpenClaw Gateway.

Lo stesso problema genera al massimo un'attività ogni due settimane e mai mentre la relativa attività è ancora aperta. Vengono create al massimo due nuove attività al giorno. Un'attività relativa a un servizio inattivo si chiude automaticamente quando il servizio riprende a funzionare o il problema viene risolto.

## Nel terminale

`assistant doctor` elenca gli stessi problemi dell'ultimo giorno.

## Altri computer

Su macOS, Windows e sui computer senza systemd non legge nulla e lo comunica con `assistant doctor`.

Su una Machine ospitata, il server è gestito da noi: i suoi problemi vengono segnalati al team di The Machine, non a te sotto forma di attività.

## Disattivarlo

Imposta `"computer_logs": false` in config.json e riavvia il servizio.
