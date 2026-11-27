---
title: De desktopapp
area: getting-started
summary: The Machine op Windows, Mac en Linux: je dashboard in een eigen venster, met een robot in een hoek van je scherm.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
De desktopapp opent je dashboard in een eigen venster. In een hoek van je scherm staat een kleine robot: klik erop om een to-do toe te voegen, vragen te stellen over je berichten of te zien wat er voor je klaarstaat. Het is een prototype.

## Downloaden

Elke link bevat altijd de nieuwste versie:

- Windows 10 of 11, 64-bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac met macOS 13 of nieuwer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-bits: de [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), het [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) voor Ubuntu en Debian, of de [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) voor Arch en Omarchy

Je vindt ze ook op je dashboard. Op een computer vind je onder **Instellingen** bij **Apps** alle drie de versies. Bij de versie voor je huidige computer staat **Deze computer**. De to-do **Haal meer uit The Machine** bevat **Download de desktopapp**. Daarmee download je de versie voor je computer, of open je de Linux-stappen hieronder. De to-do verdwijnt zodra de app is ingelogd op je Machine. Geen van beide wordt op een telefoon of in de desktopapp weergegeven.

## Windows

Open het installatieprogramma. De app wordt alleen voor jou geïnstalleerd, zonder beheerdersrechten, en is ondertekend door Salesflare. Op een computer waarop WebView2 nog niet eerder is gebruikt, duurt het een paar seconden langer om dat klaar te zetten. Daarna start de app meteen. De app werkt zichzelf bij: in de instellingen zie je wanneer een nieuwe versie klaarstaat.

## Mac

Pak het zip-bestand uit, verplaats The Machine naar Programma's en open de app daar. macOS vraagt één keer of je een app van het internet wilt openen: kies Open. De app is ondertekend en gelegaliseerd, en werkt zichzelf bij.

## Linux

- Elke distributie: maak de AppImage uitvoerbaar met `chmod +x` en start hem. Als je de melding krijgt dat FUSE ontbreekt, installeer je `fuse3`.
- Ubuntu 22.04, Debian 12 of nieuwer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK en gtk-layer-shell worden meegeleverd.
- Arch en Omarchy: zet de PKGBUILD in een lege map en voer daar `makepkg -si` uit. De juiste versie wordt gedownload, gecontroleerd aan de hand van de checksum in het bestand en geïnstalleerd. Op Hyprland, zoals Omarchy het instelt, blijft de robot boven andere vensters zonder een eigen venster.

Op Linux werkt de app zichzelf niet bij. Download voor een nieuwere versie het bestand opnieuw, of download de nieuwere PKGBUILD.

## Een download controleren

Elk bestand heeft GitHub-buildherkomstgegevens. Daarmee kun je zien dat het is gebouwd op basis van de code van The Machine, met de eigen workflow. Met de [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Inloggen

De eerste keer opent er een venster waarin je kunt inloggen. Bij een gehoste Machine of een Machine op The Machine Network opent je account in je browser. Daarna keer je terug naar de app. Bij een zelfgehoste Machine heb je het adres van die Machine nodig, vanaf een computer op je Tailscale-netwerk.

Wil je je dashboard liever als app in Chrome of Edge gebruiken? Bekijk dan [De app installeren](phone-app.md).

## De robot

De robot verdwijnt zodra het venster van de app op de voorgrond staat. Hij komt terug zodra een ander venster op de voorgrond staat, of wanneer je het venster minimaliseert of sluit. Met meerdere beeldschermen staat de robot op het scherm waarop het venster van de app staat, totdat je hem ergens anders naartoe sleept. Op Hyprland, Sway en KDE staat hij op het hoofdscherm. Uitzetten of weer inschakelen doe je via **Instellingen** (Ctrl+komma, of Command-komma op een Mac) en **Robot weergeven**.
