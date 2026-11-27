---
title: L’app desktop
area: getting-started
summary: The Machine su Windows, Mac e Linux: la tua dashboard in una finestra tutta sua e un robottino in un angolo dello schermo.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
L’app desktop apre la tua dashboard in una finestra tutta sua. Un robottino si trova in un angolo dello schermo: fai clic per aggiungere un’attività, chiedere informazioni sui messaggi o vedere cosa c’è per te. È un prototipo.

## Scarica l’app

Ogni link porta sempre all’ultima versione:

- Windows 10 o 11, 64 bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o versioni successive: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bit: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), il file [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) per Ubuntu e Debian oppure il [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) per Arch e Omarchy

## Windows

Apri il programma di installazione. Installa l’app solo per te, senza bisogno dei privilegi di amministratore, ed è firmato da Salesflare. Su un computer che non ha mai usato WebView2, la configurazione richiede qualche secondo in più. Poi l’app si avvia subito. L’app si aggiorna automaticamente: nelle **Impostazioni** puoi vedere quando è pronta una nuova versione.

## Mac

Estrai il file zip, sposta The Machine in Applicazioni e aprila da lì. macOS chiede una volta se vuoi aprire un’app scaricata da internet: scegli **Apri**. È firmata e autenticata da Apple e si aggiorna automaticamente.

## Linux

- Qualsiasi distribuzione: rendi eseguibile l’AppImage con `chmod +x` e avviala. Se compare un messaggio che indica che manca FUSE, installa `fuse3`.
- Ubuntu 22.04, Debian 12 o versioni successive: `sudo apt install ./the-machine-desktop-amd64.deb`. Include WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: metti il PKGBUILD in una cartella vuota ed esegui `makepkg -si` da lì. Scarica quella versione, la verifica con il checksum indicato nel file e la installa. Su Hyprland, come configurato in Omarchy, il robottino rimane sopra le altre finestre senza avere una finestra propria.

Su Linux l’app non si aggiorna automaticamente. Per installare una versione più recente, scarica di nuovo il file oppure il PKGBUILD più recente.

## Verifica un download

Ogni file include l’attestazione di provenienza della build di GitHub, che dimostra che è stato compilato dal workflow di The Machine usando il codice di The Machine. Con la [CLI di GitHub](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Accedi

Al primo avvio, la finestra si apre sulla schermata di accesso. Per una Machine ospitata o una sulla The Machine Network, puoi accedere al tuo account nel browser e poi tornare all’app. Per una Machine che ospiti tu, serve il suo indirizzo, accessibile da un computer sulla tua rete Tailscale.

Per usare la dashboard come app di Chrome o Edge, consulta [Installa l’app](phone-app.md).
