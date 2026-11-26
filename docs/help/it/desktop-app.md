---
title: L'app desktop
area: getting-started
summary: The Machine su Windows, Mac e Linux: la tua dashboard in una finestra tutta sua e un robot in un angolo dello schermo.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
L'app desktop apre la tua dashboard in una finestra tutta sua. Un piccolo robot compare in un angolo dello schermo: cliccaci per aggiungere un'attività, chiedere informazioni sui tuoi messaggi o vedere cosa c'è per te. È un prototipo.

## Scarica l'app

Ogni link porta sempre alla versione più recente:

- Windows 10 o 11, 64 bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o versioni successive: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bit: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), il file [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) per Ubuntu e Debian oppure [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) per Arch e Omarchy

## Windows

Apri il programma di installazione. Si installa solo per te, senza bisogno di un amministratore, ed è firmato da Salesflare. Se sul computer non è mai stato usato WebView2, la configurazione richiede qualche secondo in più. Subito dopo, l'app si avvia. L'app si aggiorna da sola: nelle **Impostazioni** puoi vedere quando è pronta una nuova versione.

## Mac

Estrai il file zip, sposta The Machine in Applicazioni e aprila da lì. macOS ti chiede una volta se vuoi aprire un'app scaricata da Internet: scegli Apri. L'app è firmata e autenticata da Apple e si aggiorna da sola.

## Linux

- Qualsiasi distribuzione: rendi eseguibile l'AppImage con `chmod +x` e avviala. Se compare un messaggio che indica che manca FUSE, installa `fuse2` su Arch o `libfuse2t64` su Ubuntu 24.04.
- Ubuntu 22.04, Debian 12 o versioni successive: `sudo apt install ./the-machine-desktop-amd64.deb`. Include WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: metti il PKGBUILD in una cartella vuota e avvia `makepkg -si` da lì. Scarica quella versione, la verifica usando il checksum nel file e la installa. Su Hyprland, come configurato in Omarchy, il robot rimane sopra le altre finestre senza avere una finestra propria.

Su Linux l'app non si aggiorna da sola. Per installare una versione più recente, scarica di nuovo il file o il PKGBUILD aggiornato.

## Accedi

La prima volta, si apre la finestra di accesso. Se usi una Machine ospitata o una sulla The Machine Network, si apre il tuo account nel browser e poi si torna all'app. Per una Machine ospitata autonomamente, serve il suo indirizzo, che trovi su un computer nella tua rete Tailscale.

Per usare la dashboard come app di Chrome o Edge, consulta [Installa l'app](phone-app.md).
