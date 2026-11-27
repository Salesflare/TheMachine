---
title: L’application de bureau
area: getting-started
summary: The Machine sur Windows, Mac et Linux : votre tableau de bord dans une fenêtre dédiée et un robot dans un coin de l’écran.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
L’application de bureau ouvre votre tableau de bord dans une fenêtre dédiée. Un petit robot apparaît dans un coin de l’écran : cliquez dessus pour ajouter une tâche, poser une question sur vos messages ou voir ce qui est prévu pour vous. C’est un prototype.

## Télécharger l’application

Chaque lien mène toujours à la dernière version :

- Windows 10 ou 11, 64 bits : [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac avec macOS 13 ou une version ultérieure : [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits : l’[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), le fichier [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) pour Ubuntu et Debian, ou le [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) pour Arch et Omarchy

Vous trouverez aussi ces liens dans votre tableau de bord. Sur un ordinateur, **Paramètres**, **Applis** les répertorie tous les trois, avec la mention **Cet ordinateur** sur celui que vous utilisez. La tâche **Tirez le meilleur de The Machine** contient **Télécharger l’app de bureau**. Elle télécharge la version adaptée à votre ordinateur ou ouvre les étapes Linux ci-dessous. Elle disparaît une fois l’application connectée à votre Machine. Ces liens ne s’affichent ni sur un téléphone ni dans l’application de bureau.

## Windows

Ouvrez le programme d’installation. Il s’installe uniquement pour vous, sans droits d’administrateur, et est signé par Salesflare. Sur un ordinateur où aucune application n’a encore utilisé WebView2, quelques secondes de plus sont nécessaires pour le préparer. L’application démarre juste après. Elle se met à jour automatiquement : ses paramètres vous indiquent quand une nouvelle version est prête.

## Mac

Décompressez le fichier zip, déplacez The Machine dans Applications, puis ouvrez-le depuis ce dossier. macOS vous demande une fois si vous souhaitez ouvrir une application téléchargée sur Internet : choisissez Ouvrir. L’application est signée et notariée, et se met à jour automatiquement.

## Linux

- Toutes les distributions : rendez l’AppImage exécutable avec `chmod +x`, puis lancez-la. Si un message indique que FUSE est manquant, installez `fuse3`.
- Ubuntu 22.04, Debian 12 ou version ultérieure : `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK et gtk-layer-shell sont inclus.
- Arch et Omarchy : placez le PKGBUILD dans un dossier vide, puis exécutez `makepkg -si` dans ce dossier. Le fichier télécharge cette version, la vérifie avec la somme de contrôle indiquée dans le fichier, puis l’installe. Sous Hyprland, comme dans Omarchy, le robot reste au-dessus des autres fenêtres sans avoir sa propre fenêtre.

Sous Linux, l’application ne se met pas à jour automatiquement. Pour installer une version plus récente, téléchargez à nouveau le fichier ou récupérez le nouveau PKGBUILD.

## Vérifier un téléchargement

Chaque fichier dispose de la provenance de build GitHub, qui indique qu’il a été créé à partir du code de The Machine par son propre workflow. Avec la [CLI GitHub](https://cli.github.com) : `gh attestation verify <file> -R Salesflare/TheMachine`.

## Se connecter

Lors de la première utilisation, une fenêtre s’ouvre pour vous permettre de vous connecter. Pour une Machine hébergée ou une Machine sur The Machine Network, votre compte s’ouvre dans le navigateur, puis l’application s’ouvre à nouveau. Pour une Machine auto-hébergée, vous devez saisir son adresse. Vous pouvez la trouver depuis un ordinateur connecté à votre réseau Tailscale.

Pour utiliser le tableau de bord comme une application dans Chrome ou Edge, consultez [Installer l’application](phone-app.md).

## Le robot

Le robot disparaît lorsque la fenêtre de l’application est au premier plan. Il réapparaît lorsqu’une autre fenêtre passe au premier plan, ou lorsque vous réduisez ou fermez la fenêtre de l’application. Si vous avez plusieurs écrans, il apparaît sur celui où se trouve la fenêtre de l’application, jusqu’à ce que vous le déplaciez ailleurs. Sous Hyprland, Sway et KDE, il apparaît sur l’écran principal. Pour l’activer ou le désactiver : Paramètres (Ctrl+virgule, ou Commande+virgule sur Mac), **Afficher le robot**.
