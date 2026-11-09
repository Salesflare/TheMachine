---
title: Problemi sul tuo computer
area: troubleshooting
summary: La tua Machine legge i log del suo computer e ti segnala i problemi veri, con la causa e una soluzione. Una soluzione parte solo quando tocchi Do it.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
---
## Cosa legge

Su Linux con systemd, la tua Machine legge il log della tua sessione utente: i tuoi servizi e i rapporti di crash dei tuoi programmi. Su Omarchy controlla anche Hyprland e la barra. Non legge mai il log di tutto il sistema e non chiede mai più accesso.

Legge quale servizio si è fermato, come è finito e quale programma si è bloccato. Mai cosa dice una riga del log, quindi nessun testo del log viene tenuto o esce dal tuo computer.

## Cosa conta come problema

Un servizio che continua a riavviarsi, uno che è fallito più volte in un giorno o resta fermo, uno che ha esaurito la memoria e un programma che si è bloccato. Su Omarchy anche un crash di Hyprland o della barra, ed errori nelle impostazioni di Hyprland.

Un solo riavvio o una sola esecuzione fallita è normale e non dà avvisi.

I browser guidati da test e agenti (headless, Playwright, Puppeteer, CI) restano in silenzio, e così un programma che si ferma mentre il suo servizio viene fermato o riavviato. Un programma che si blocca più e più volte dà una sola attività, che dice quante volte e quando.

## Cosa ricevi

Un’attività che dice in parole semplici cosa è successo, perché conta e cosa puoi fare. I comandi che mostrano il perché sono sotto Mostra altro. Chiedi nella sua chat e The Machine ci guarda. Tutto ciò che lei cambia aspetta il tuo OK, come con Do it.

Quando c’è una correzione sicura, l’attività ha Do it. Riavvia un tuo servizio rimasto fermo e, su Omarchy, riporta la barra. Do it esegue solo quel comando, e il risultato compare nella chat dell’attività. Non tocca mai i servizi di The Machine né l’OpenClaw Gateway.

Lo stesso problema porta al massimo un’attività ogni due settimane, e mai mentre la sua attività è ancora aperta. Al massimo due nuove al giorno.

## In un terminale

`assistant doctor` elenca gli stessi problemi dell’ultimo giorno.

## Altri computer

Su macOS, Windows e computer senza systemd non legge nulla e lo dice in `assistant doctor`.

## Disattivarla

Imposta `"computer_logs": false` in config.json e riavvia il servizio.
