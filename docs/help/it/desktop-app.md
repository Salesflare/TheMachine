---
title: L’app desktop
area: getting-started
summary: The Machine su Windows, Mac e Linux: la tua dashboard in una finestra dedicata e un robot in un angolo dello schermo.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
L’app desktop apre la tua dashboard in una finestra dedicata. In un angolo dello schermo c’è un piccolo robot: fai clic per aggiungere un’attività, chiedere informazioni sui tuoi messaggi o vedere cosa c’è per te. È un prototipo.

## Scaricala

Ogni link porta sempre alla versione più recente:

- Windows 10 o 11, 64 bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o versioni successive: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bit: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), il file [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) per Ubuntu e Debian oppure [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) per Arch e Omarchy

Li trovi anche nella tua dashboard. Su un computer, in **Impostazioni** > **App** trovi tutti e tre i download; sul tuo computer compare **Questo computer**. L’attività **Sfrutta al meglio The Machine** contiene **Scarica l’app desktop**: scarica la versione adatta al tuo computer oppure apre le istruzioni per Linux qui sotto. Scompare quando l’app ha effettuato l’accesso alla tua Machine. Nessuna delle due opzioni compare sul telefono o nell’app desktop.

## Windows

Apri il programma di installazione. L’app si installa solo per te, senza privilegi di amministratore, ed è firmata da Salesflare. Se sul computer non è mai stata usata WebView2, ci vorranno alcuni secondi in più per prepararla. Al termine, l’app si avvia subito. L’app si aggiorna automaticamente: nelle Impostazioni ti avvisa quando è pronta una nuova versione.

## Mac

Estrai il file zip, sposta The Machine in Applicazioni e aprila da lì. macOS ti chiede una volta se vuoi aprire un’app scaricata da internet: scegli Apri. L’app è firmata e autenticata da Apple e si aggiorna automaticamente.

## Linux

- Qualsiasi distribuzione: rendi eseguibile l’AppImage con `chmod +x` e avviala. Se compare un messaggio che segnala l’assenza di FUSE, installa `fuse3`.
- Ubuntu 22.04, Debian 12 o versioni successive: `sudo apt install ./the-machine-desktop-amd64.deb`. Include WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: metti il PKGBUILD in una cartella vuota ed esegui `makepkg -si` da lì. Scarica quella versione, la verifica con il checksum indicato nel file e la installa. Su Hyprland, come configurato da Omarchy, il robot resta sopra le altre finestre senza avere una finestra propria.

Su Linux l’app non si aggiorna automaticamente. Per installare una versione più recente, scarica di nuovo il file o il PKGBUILD aggiornato.

## Verifica un download

Ogni file include la provenienza della build di GitHub, che mostra che è stato creato dal workflow di The Machine a partire dal codice di The Machine. Con la [CLI di GitHub](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Accedi

Al primo avvio, la finestra dell’app ti chiede di accedere. Se usi una Machine ospitata o una Machine sulla The Machine Network, si apre il tuo account nel browser e poi torni all’app. Per una Machine self-hosted, inserisci il suo indirizzo da un computer sulla tua rete Tailscale.

Per usare la dashboard come app di Chrome o Edge, vedi [Installa l’app](phone-app.md).

## Il robot

Il robot scompare quando la finestra dell’app è in primo piano e ricompare quando è in primo piano un’altra finestra o quando riduci a icona o chiudi quella dell’app. Se hai più monitor, compare su quello in cui si trova la finestra dell’app, finché non lo trascini altrove. Su Hyprland, Sway e KDE compare sul monitor principale. Per disattivarlo o riattivarlo, apri **Impostazioni** (Ctrl+virgola o Comando-virgola su Mac) e seleziona **Mostra il robot**.
