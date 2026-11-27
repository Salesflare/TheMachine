---
title: L’app desktop
area: getting-started
summary: The Machine su Windows, Mac e Linux: la tua dashboard in una finestra dedicata e un robot in un angolo dello schermo.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
L’app desktop apre la tua dashboard in una finestra dedicata. Un piccolo robot compare in un angolo dello schermo: cliccaci per aggiungere un’attività, chiedere informazioni sui tuoi messaggi o vedere cosa c’è per te. È un prototipo.

## Scarica l’app

Ogni link porta sempre alla versione più recente:

- Windows 10 o 11, 64 bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o versioni successive: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bit: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), il file [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) per Ubuntu e Debian oppure il [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) per Arch e Omarchy

Li trovi anche nella tua dashboard. Su un computer, **Impostazioni** > **App** mostra tutti e tre, con l’etichetta **Questo computer** accanto a quello in uso. L’attività **Sfrutta al meglio The Machine** include **Scarica l’app desktop**: scarica la versione per il tuo computer oppure apre i passaggi per Linux qui sotto. L’attività scompare quando l’app ha effettuato l’accesso alla tua Machine. Queste opzioni non compaiono sul telefono né nell’app desktop.

## Windows

Apri il programma di installazione. L’app si installa solo per te, senza privilegi di amministratore, ed è firmata da Salesflare. Se sul computer non è mai stato usato WebView2, la prima installazione richiede qualche secondo in più. Una volta pronto, l’app si avvia subito. Si aggiorna automaticamente e nelle Impostazioni ti avvisa quando è pronta una nuova versione.

## Mac

Estrai il file zip, sposta The Machine in Applicazioni e aprila da lì. macOS chiede una sola volta se vuoi aprire un’app scaricata da internet: scegli Apri. L’app è firmata e autenticata da Apple e si aggiorna automaticamente.

## Linux

- Qualsiasi distribuzione: rendi eseguibile l’AppImage con `chmod +x` e avviala. Se segnala che manca FUSE, installa `fuse3`.
- Ubuntu 22.04, Debian 12 o versioni successive: `sudo apt install ./the-machine-desktop-amd64.deb`. Include WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: metti il PKGBUILD in una cartella vuota ed esegui `makepkg -si` al suo interno. Scarica quella versione, la verifica con il checksum nel file e la installa. Su Hyprland, come in Omarchy, il robot resta sopra le altre finestre senza avere una finestra propria.

L’AppImage si aggiorna automaticamente se si trova in una tua cartella, ad esempio ~/Applications. Nelle Impostazioni ti avvisa quando è pronta una nuova versione. Il file .deb e il pacchetto Arch si aggiornano con apt e pacman: nelle Impostazioni trovi l’avviso quando è disponibile una versione più recente, con il pulsante Download per il file .deb o il PKGBUILD. Un’AppImage estratta in una cartella non si aggiorna automaticamente: usa l’AppImage così com’è.

## Verifica un download

Ogni file include le attestazioni di provenienza della build di GitHub, che mostrano che è stato creato a partire dal codice di The Machine dal workflow del progetto. Con la [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Accedi

Al primo avvio, si apre la finestra per accedere. Per una Machine ospitata oppure una sulla The Machine Network, si apre il tuo account nel browser e poi si torna all’app. Per una Machine ospitata autonomamente, inserisci il suo indirizzo da un computer collegato alla tua rete Tailscale.

Per usare la dashboard come app di Chrome o Edge, consulta [Installa l’app](phone-app.md).

## Il robot

Il robot scompare quando la finestra dell’app è in primo piano e ricompare quando è in primo piano un’altra finestra oppure quando riduci a icona o chiudi quella dell’app. Se hai più monitor, si posiziona su quello in cui si trova la finestra dell’app, finché non lo trascini altrove. Su Hyprland, Sway e KDE si posiziona sul monitor principale. Per attivarlo o disattivarlo, vai in **Impostazioni** (Ctrl+virgola, oppure Command+virgola su Mac) e seleziona **Mostra il robot**.
