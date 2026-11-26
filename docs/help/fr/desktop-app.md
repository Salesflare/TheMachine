---
title: L’application de bureau
area: getting-started
summary: The Machine sur Windows, Mac et Linux : votre tableau de bord dans sa propre fenêtre, avec un robot dans un coin de l’écran.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
L’application de bureau ouvre votre tableau de bord dans sa propre fenêtre. Un petit robot apparaît dans un coin de l’écran : cliquez dessus pour ajouter une tâche, poser une question sur vos messages ou voir ce qui vous concerne. C’est un prototype.

## Télécharger l’application

Chaque lien mène toujours à la dernière version :

- Windows 10 ou 11, 64 bits : [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac avec macOS 13 ou une version ultérieure : [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits : [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) pour Ubuntu et Debian, ou [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) pour Arch et Omarchy

## Windows

Ouvrez le programme d’installation. Il s’installe uniquement pour vous, sans droits d’administrateur, et est signé par Salesflare. Sur un ordinateur qui n’a encore jamais utilisé WebView2, sa configuration prend quelques secondes de plus. L’application démarre juste après. Elle se met à jour automatiquement. Ses **Paramètres** vous indiquent quand une nouvelle version est prête.

## Mac

Décompressez l’archive, déplacez The Machine dans Applications et ouvrez-la depuis ce dossier. macOS vous demande une seule fois si vous voulez ouvrir une application téléchargée sur Internet : choisissez **Ouvrir**. Elle est signée et notariée, et se met à jour automatiquement.

## Linux

- Toutes les distributions : rendez l’AppImage exécutable avec `chmod +x`, puis lancez-la. Si un message indique que FUSE est absent, installez `fuse2` sur Arch ou `libfuse2t64` sur Ubuntu 24.04.
- Ubuntu 22.04, Debian 12 ou version ultérieure : `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK et gtk-layer-shell sont inclus.
- Arch et Omarchy : placez le PKGBUILD dans un dossier vide et exécutez-y `makepkg -si`. Le fichier télécharge cette version, la vérifie à l’aide de la somme de contrôle indiquée dans le fichier, puis l’installe. Sous Hyprland, comme sur Omarchy, le robot reste au-dessus des autres fenêtres sans avoir sa propre fenêtre.

Sous Linux, l’application ne se met pas à jour automatiquement. Pour installer une version plus récente, téléchargez à nouveau le fichier ou le PKGBUILD le plus récent.

## Se connecter

Au premier lancement, la fenêtre vous invite à vous connecter. Pour une Machine hébergée ou une Machine sur The Machine Network, votre compte s’ouvre dans le navigateur, puis l’application s’ouvre à nouveau. Une Machine auto-hébergée nécessite sa propre adresse, accessible depuis un ordinateur connecté à votre réseau Tailscale.

Pour utiliser le tableau de bord comme une application Chrome ou Edge, consultez [Installer l’application](phone-app.md).
