---
title: L’app desktop
area: getting-started
summary: The Machine su Windows, Mac e Linux: la tua dashboard in una finestra dedicata e un robot in un angolo dello schermo.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: af0a8a2994af969d
---
L’app desktop apre la tua dashboard in una finestra dedicata. In un angolo dello schermo c’è un piccolo robot: fai clic per aggiungere un’attività, chiedere informazioni sui tuoi messaggi o vedere cosa c’è per te. È un prototipo.

## Scarica l’app

Ogni link porta sempre alla versione più recente:

- Windows 10 o 11, 64 bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o versioni successive: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bit: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), il file [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) per Ubuntu e Debian oppure il [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) per Arch e Omarchy

Li trovi anche nella tua dashboard. Su un computer, **Impostazioni** > **App** mostra tutti e tre, e sul tuo compare **Questo computer**. Nell’attività **Sfrutta al meglio The Machine** trovi **Scarica l’app desktop**: scarica la versione per il tuo computer oppure apre i passaggi per Linux qui sotto. L’attività scompare quando accedi dall’app alla tua Machine. Queste opzioni non sono disponibili su un telefono o nell’app desktop.

## Windows

Apri il programma di installazione. Si installa solo per te, senza privilegi di amministratore, ed è firmato da Salesflare. Se sul computer non è mai stato usato WebView2, la sua configurazione richiede qualche secondo in più. Subito dopo, l’app si avvia. L’app si aggiorna automaticamente: nelle sue Impostazioni vedi quando è pronta una nuova versione.

## Mac

Estrai il file zip, sposta The Machine in Applicazioni e aprila da lì. macOS ti chiede una volta se vuoi aprire un’app scaricata da Internet: scegli Apri. L’app è firmata e autenticata da Apple e si aggiorna automaticamente.

## Linux

- Qualsiasi distribuzione: rendi eseguibile l’AppImage con `chmod +x` e avviala. Se compare un messaggio che segnala l’assenza di FUSE, installa `fuse3`.
- Ubuntu 22.04, Debian 12 o versioni successive: `sudo apt install ./the-machine-desktop-amd64.deb`. Include WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: metti il PKGBUILD in una cartella vuota ed esegui `makepkg -si` al suo interno. Scarica quella versione, la verifica con il checksum nel file e la installa. Su Hyprland, come configurato in Omarchy, il robot resta sopra le altre finestre senza avere una finestra propria.

L’AppImage si aggiorna automaticamente se si trova in una tua cartella, per esempio ~/Applications: nelle sue Impostazioni vedi quando è pronta una nuova versione. Il file .deb e il pacchetto Arch restano gestiti da apt e pacman: nelle Impostazioni vedi quando è disponibile una versione più recente, con Download per il file .deb o il PKGBUILD. Un’AppImage estratta in una cartella non si aggiorna automaticamente: usa l’AppImage così com’è.

## Verifica un download

Ogni file include le attestazioni di build di GitHub, che mostrano che è stato creato dal workflow di The Machine a partire dal suo codice. Con [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Accedi

Al primo avvio, si apre la finestra per accedere. Per una Machine ospitata o una sulla The Machine Network, si apre il tuo account nel browser e poi si torna all’app. Per una Machine ospitata da te, inserisci il suo indirizzo. Deve essere raggiungibile da un computer connesso alla tua rete Tailscale.

Una pagina della tua Machine può portare l’app in primo piano con un link apposito: `computer.themachine.desktop://open`. Il link apre solo l’app e non contiene altro.

Per usare la dashboard come app di Chrome o Edge, consulta [Installa l’app](phone-app.md).

## Il robot

Il robot scompare quando la finestra dell’app è in primo piano e ricompare quando lo è un’altra finestra, oppure quando riduci a icona o chiudi quella dell’app. Se hai più monitor, resta su quello in cui si trova la finestra dell’app, finché non lo trascini altrove. Su Hyprland, Sway e KDE resta sul monitor principale. Per attivarlo o disattivarlo: Impostazioni (Ctrl+virgola, o Command-virgola su Mac), Mostra il robot.
