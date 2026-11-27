---
title: De desktopapp
area: getting-started
summary: The Machine op Windows, Mac en Linux: je dashboard in een eigen venster, met een robot in een hoek van je scherm.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
De desktopapp opent je dashboard in een eigen venster. In een hoek van je scherm staat een kleine robot: klik erop om een to-do toe te voegen, iets over je berichten te vragen of te bekijken wat er voor je klaarstaat. Het is een prototype.

## Downloaden

Elke link verwijst altijd naar de nieuwste versie:

- Windows 10 of 11, 64-bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac met macOS 13 of nieuwer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-bit: de [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), de [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) voor Ubuntu en Debian, of de [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) voor Arch en Omarchy

## Windows

Open het installatieprogramma. Het installeert de app alleen voor jou, zonder beheerdersrechten, en is ondertekend door Salesflare. Op een computer waarop WebView2 nog niet eerder is gebruikt, duurt het instellen daarvan een paar seconden langer. Daarna start de app meteen. De app werkt zichzelf bij: in **Instellingen** staat wanneer een nieuwe versie klaarstaat.

## Mac

Pak het zipbestand uit, verplaats The Machine naar Applications en open de app daar. macOS vraagt één keer of je een app van het internet wilt openen: kies **Open**. De app is ondertekend en genotariseerd, en werkt zichzelf bij.

## Linux

- Elke distributie: maak de AppImage uitvoerbaar met `chmod +x` en start hem. Als FUSE ontbreekt, installeer je `fuse3`.
- Ubuntu 22.04, Debian 12 of nieuwer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK en gtk-layer-shell worden meegeleverd.
- Arch en Omarchy: zet de PKGBUILD in een lege map en voer daar `makepkg -si` uit. Het script downloadt die versie, controleert die aan de hand van de checksum in het bestand en installeert hem. Op Hyprland, zoals Omarchy dat gebruikt, blijft de robot boven andere vensters staan zonder een eigen venster.

Op Linux werkt de app zichzelf niet bij. Download voor een nieuwere versie het bestand opnieuw, of download de nieuwere PKGBUILD.

## Een download controleren

Elk bestand heeft buildherkomstgegevens van GitHub. Die laten zien dat het bestand is gebouwd vanuit de code van The Machine, met de eigen workflow van The Machine. Met de [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Inloggen

De eerste keer opent het venster met de optie om in te loggen. Voor een gehoste Machine of een Machine op The Machine Network opent je account in de browser en keert de app daarna terug. Voor een zelfgehoste Machine heb je het adres ervan nodig, vanaf een computer op je Tailscale-netwerk.

Wil je het dashboard liever als app in Chrome of Edge gebruiken? Bekijk dan [De app installeren](phone-app.md).
