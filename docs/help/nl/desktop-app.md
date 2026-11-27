---
title: De desktopapp
area: getting-started
summary: The Machine op Windows, Mac en Linux: je dashboard in een eigen venster en een robot in een hoek van je scherm.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
De desktopapp opent je dashboard in een eigen venster. In een hoek van je scherm staat een kleine robot. Klik erop om een to-do toe te voegen, vragen te stellen over je berichten of te zien wat er voor jou is. Het is een prototype.

## Downloaden

Elke link bevat altijd de nieuwste versie:

- Windows 10 of 11, 64-bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac met macOS 13 of nieuwer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-bit: de [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), de [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) voor Ubuntu en Debian, of de [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) voor Arch en Omarchy

Je vindt de downloads ook op je dashboard. Op een computer staan ze alle drie bij **Instellingen** > **Apps**. Bij de app die je gebruikt, staat **Deze computer**. In de to-do **Haal meer uit The Machine** staat **Download de desktopapp**. Die downloadt de versie voor je computer of opent de Linux-instructies hieronder. De to-do verdwijnt zodra je in de app bent ingelogd op je Machine. Geen van beide is zichtbaar op je telefoon of in de desktopapp.

## Windows

Open het installatieprogramma. De app wordt alleen voor jou geïnstalleerd, zonder beheerdersrechten, en is ondertekend door Salesflare. Op een computer waarop WebView2 nog niet eerder is gebruikt, duurt het instellen daarvan een paar seconden langer. Daarna start de app meteen. De app wordt automatisch bijgewerkt. In **Instellingen** zie je wanneer er een nieuwe versie klaarstaat.

## Mac

Pak het zip-bestand uit, verplaats The Machine naar Applications en open de app daar. macOS vraagt eenmalig of je een app van internet wilt openen. Kies **Open**. De app is ondertekend en notarieel gewaarmerkt, en wordt automatisch bijgewerkt.

## Linux

- Elke distributie: maak de AppImage uitvoerbaar met `chmod +x` en start hem. Als je de melding krijgt dat FUSE ontbreekt, installeer je `fuse3`.
- Ubuntu 22.04, Debian 12 of nieuwer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK en gtk-layer-shell zijn inbegrepen.
- Arch en Omarchy: zet de PKGBUILD in een lege map en voer daar `makepkg -si` uit. Het bestand downloadt die versie, controleert die met de checksum in het bestand en installeert hem. Op Hyprland, zoals standaard ingesteld in Omarchy, blijft de robot boven andere vensters staan zonder eigen venster.

De AppImage wordt automatisch bijgewerkt als die in een map van jou staat, zoals ~/Applications. In **Instellingen** zie je wanneer er een nieuwe versie klaarstaat. De .deb en het Arch-pakket worden bijgewerkt via apt en pacman. In **Instellingen** zie je wanneer er een nieuwere versie beschikbaar is, met **Downloaden** voor de .deb of PKGBUILD. Een AppImage die je in een map hebt uitgepakt, wordt niet automatisch bijgewerkt. Gebruik de AppImage zoals die is.

## Een download controleren

Elk bestand heeft build-herkomstinformatie van GitHub. Daarmee kun je zien dat het is gebouwd met de code van The Machine, via de eigen workflow. Met de [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Inloggen

De eerste keer opent het venster om in te loggen. Voor een gehoste Machine of een Machine op The Machine Network opent je account in de browser en keer je daarna terug naar de app. Voor een zelfgehoste Machine heb je het eigen adres nodig, dat je op een computer in je Tailscale-netwerk kunt opzoeken.

Wil je je dashboard liever als app in Chrome of Edge gebruiken? Lees dan [De app installeren](phone-app.md).

## De robot

De robot verdwijnt zolang het venster van de app op de voorgrond staat. Hij verschijnt weer zodra een ander venster op de voorgrond staat, of wanneer je het venster minimaliseert of sluit. Als je meerdere monitors hebt, staat de robot op de monitor waarop het venster van de app staat, totdat je hem ergens anders naartoe sleept. Op Hyprland, Sway en KDE staat hij op de hoofdmonitor. Je kunt hem aan- of uitzetten via **Instellingen** (Ctrl+comma, of Command-comma op een Mac) > **De robot weergeven**.
