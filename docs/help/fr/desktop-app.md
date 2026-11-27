---
title: L’application de bureau
area: getting-started
summary: The Machine sur Windows, Mac et Linux : votre tableau de bord dans sa propre fenêtre, et un robot dans un coin de l’écran.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
L’application de bureau ouvre votre tableau de bord dans sa propre fenêtre. Un petit robot apparaît dans un coin de l’écran : cliquez dessus pour ajouter une tâche, poser une question sur vos messages ou voir ce qui vous concerne. C’est un prototype.

## Télécharger l’application

Chaque lien donne toujours accès à la dernière version :

- Windows 10 ou 11, 64 bits : [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac avec macOS 13 ou version ultérieure : [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits : [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), le [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) pour Ubuntu et Debian, ou le [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) pour Arch et Omarchy

Vous trouverez aussi ces liens dans votre tableau de bord. Sur un ordinateur, **Paramètres**, **Applis** répertorie les trois versions, avec **Cet ordinateur** à côté de celle qui correspond à votre ordinateur. La tâche **Tirez le meilleur de The Machine** contient **Télécharger l’app de bureau**. Elle télécharge la version adaptée à votre ordinateur ou ouvre les étapes Linux ci-dessous. Cette tâche disparaît dès que l’application est connectée à votre Machine. Ces liens ne s’affichent ni sur un téléphone ni dans l’application de bureau.

## Windows

Ouvrez le programme d’installation. Il s’installe uniquement pour vous, sans droits d’administrateur, et est signé par Salesflare. Sur un ordinateur qui n’a encore jamais utilisé WebView2, sa préparation prend quelques secondes de plus. L’application démarre juste après. Elle se met à jour automatiquement. Ses paramètres indiquent quand une nouvelle version est prête.

## Mac

Décompressez le fichier zip, déplacez The Machine dans Applications, puis ouvrez-la depuis ce dossier. macOS vous demande une fois si vous souhaitez ouvrir une application téléchargée sur Internet : choisissez « Ouvrir ». L’application est signée et notariée, et se met à jour automatiquement.

## Linux

- Toutes les distributions : rendez l’AppImage exécutable avec `chmod +x`, puis lancez-la. Si un message indique que FUSE est manquant, installez `fuse3`.
- Ubuntu 22.04, Debian 12 ou version ultérieure : `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK et gtk-layer-shell sont inclus.
- Arch et Omarchy : placez le PKGBUILD dans un dossier vide, puis exécutez `makepkg -si` depuis ce dossier. La commande télécharge cette version, la vérifie avec la somme de contrôle indiquée dans le fichier et l’installe. Sous Hyprland, comme dans Omarchy, le robot reste au-dessus des autres fenêtres sans avoir sa propre fenêtre.

L’AppImage se met à jour automatiquement si elle se trouve dans un dossier qui vous appartient, comme ~/Applications. Ses paramètres indiquent quand une nouvelle version est prête. Le .deb et le paquet Arch sont gérés par apt et pacman. Les paramètres indiquent quand une version plus récente est disponible, avec une option de téléchargement pour le .deb ou le PKGBUILD. Une AppImage décompressée dans un dossier ne se met pas à jour automatiquement. Utilisez l’AppImage telle quelle.

## Vérifier un téléchargement

Chaque fichier est accompagné des informations de provenance de compilation de GitHub, qui indiquent qu’il a été créé à partir du code de The Machine par son propre workflow. Avec [GitHub CLI](https://cli.github.com) : `gh attestation verify <file> -R Salesflare/TheMachine`.

## Se connecter

La première fois, la fenêtre de l’application s’ouvre sur l’écran de connexion. Pour une Machine hébergée ou une Machine sur The Machine Network, votre compte s’ouvre dans votre navigateur, puis l’application revient au premier plan. Pour une Machine auto-hébergée, saisissez son adresse depuis un ordinateur connecté à votre réseau Tailscale.

Pour utiliser le tableau de bord comme une application Chrome ou Edge, consultez [Installer l’application](phone-app.md).

## Le robot

Le robot disparaît lorsque la fenêtre de l’application est au premier plan. Il réapparaît lorsqu’une autre fenêtre passe au premier plan, ou lorsque vous réduisez ou fermez l’application. Si vous avez plusieurs écrans, il apparaît sur celui où se trouve la fenêtre de l’application, jusqu’à ce que vous le déplaciez ailleurs. Sous Hyprland, Sway et KDE, il apparaît sur l’écran principal. Pour l’activer ou le désactiver : **Paramètres** (Ctrl+virgule, ou Commande-virgule sur Mac), **Afficher le robot**.
