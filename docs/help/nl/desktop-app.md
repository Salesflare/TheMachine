---
title: De desktopapp
area: getting-started
summary: The Machine op Windows, Mac en Linux: je dashboard in een eigen venster en een robot in een hoek van je scherm.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: af0a8a2994af969d
---
De desktopapp opent je dashboard in een eigen venster. In een hoek van je scherm staat een kleine robot. Klik erop om een to-do toe te voegen, iets over je berichten te vragen of te zien wat er voor je is. Dit is een prototype.

## Downloaden

Elke link verwijst altijd naar de nieuwste versie:

- Windows 10 of 11, 64-bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac met macOS 13 of nieuwer: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-bit: de [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), de [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) voor Ubuntu en Debian, of de [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) voor Arch en Omarchy

Je dashboard bevat deze downloads ook. Ga op een computer naar **Instellingen** en **Apps** om alle drie te zien. Op je eigen computer staat **Deze computer** erbij. In de to-do **Haal meer uit The Machine** staat **Download de desktopapp**. Daarmee download je de versie voor jouw computer of open je de Linux-stappen hieronder. De to-do verdwijnt zodra je in de app bent ingelogd op je Machine. Deze opties zijn niet te zien op een telefoon of in de desktopapp.

## Windows

Open het installatiebestand. De app wordt alleen voor jou geïnstalleerd, zonder beheerdersrechten, en is ondertekend door Salesflare. Op een computer waarop WebView2 nog niet eerder is gebruikt, duurt het een paar seconden langer om dat klaar te maken. Daarna start de app meteen. De app werkt zichzelf bij. In de Instellingen zie je wanneer een nieuwe versie klaarstaat.

## Mac

Pak het zipbestand uit, verplaats The Machine naar Applications en open de app daar. macOS vraagt één keer of je een app van het internet wilt openen. Kies Open. De app is ondertekend en genotariseerd, en werkt zichzelf bij.

## Linux

- Elke distributie: maak de AppImage uitvoerbaar met `chmod +x` en start hem. Als je de melding krijgt dat FUSE ontbreekt, installeer dan `fuse3`.
- Ubuntu 22.04, Debian 12 of nieuwer: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK en gtk-layer-shell worden meegeleverd.
- Arch en Omarchy: zet de PKGBUILD in een lege map en voer daar `makepkg -si` uit. Die downloadt de versie, controleert deze aan de hand van de checksum in het bestand en installeert hem. Op Hyprland, zoals bij Omarchy, blijft de robot boven andere vensters staan zonder een eigen venster.

De AppImage werkt zichzelf bij als die in een map van jou staat, zoals ~/Applications. In de Instellingen zie je wanneer een nieuwe versie klaarstaat. De .deb en het Arch-pakket blijven bij apt en pacman. In de Instellingen zie je wanneer er een nieuwere versie is, met Download voor de .deb of PKGBUILD. Een AppImage die naar een map is uitgepakt, werkt zichzelf niet bij. Gebruik de AppImage zoals die is.

## Een download controleren

Elk bestand bevat de buildprovenance van GitHub. Die laat zien dat het is gebouwd met de code van The Machine, via zijn eigen workflow. Met de [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Inloggen

De eerste keer opent het venster met de optie om in te loggen. Bij een gehoste Machine of een Machine op The Machine Network opent je account in je browser en keer je daarna terug naar de app. Voor een zelfgehoste Machine heb je het eigen adres nodig, vanaf een computer op je Tailscale-netwerk.

Een pagina van je Machine kan de app naar voren halen met een eigen link, `computer.themachine.desktop://open`. De link opent alleen de app en bevat verder niets.

Wil je je dashboard liever als Chrome- of Edge-app gebruiken? Bekijk dan [De app installeren](phone-app.md).

## De robot

De robot verdwijnt wanneer het venster van de app op de voorgrond staat en verschijnt weer wanneer een ander venster op de voorgrond staat, of wanneer je de app minimaliseert of sluit. Als je meerdere beeldschermen hebt, staat hij op het scherm waarop het appvenster staat, totdat je hem ergens anders naartoe sleept. Op Hyprland, Sway en KDE staat hij op het hoofdscherm. Zet hem aan of uit via **Instellingen** (Ctrl+comma, of Command-comma op een Mac) en **De robot tonen**.
