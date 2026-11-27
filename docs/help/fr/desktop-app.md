---
title: L’application de bureau
area: getting-started
summary: The Machine sur Windows, Mac et Linux : votre tableau de bord dans une fenêtre dédiée et un robot dans un coin de l’écran.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: af0a8a2994af969d
---
L’application de bureau ouvre votre tableau de bord dans une fenêtre dédiée. Un petit robot apparaît dans un coin de l’écran : cliquez dessus pour ajouter une tâche, poser une question sur vos messages ou voir ce qui est prévu pour vous. C’est un prototype.

## Télécharger l’application

Chaque lien pointe toujours vers la dernière version :

- Windows 10 ou 11, 64 bits : [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac avec macOS 13 ou version ultérieure : [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits : l’[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), le fichier [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) pour Ubuntu et Debian, ou le [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) pour Arch et Omarchy

Vous trouverez aussi ces liens dans votre tableau de bord. Sur un ordinateur, **Paramètres**, **Applis** liste les trois versions et indique **Cet ordinateur** pour celle qui correspond à votre appareil. La tâche **Tirez le meilleur de The Machine** contient **Télécharger l’app de bureau**. Elle télécharge la version adaptée à votre ordinateur ou ouvre les instructions Linux ci-dessous. La tâche disparaît une fois l’application connectée à votre Machine. Ces liens n’apparaissent ni sur un téléphone ni dans l’application de bureau.

## Windows

Ouvrez le programme d’installation. Il s’installe uniquement pour vous, sans droits d’administrateur, et est signé par Salesflare. Sur un ordinateur où aucune application n’a encore utilisé WebView2, quelques secondes supplémentaires sont nécessaires pour le préparer. L’application démarre juste après. Elle se met à jour automatiquement : ses Paramètres indiquent quand une nouvelle version est prête.

## Mac

Décompressez le fichier zip, déplacez The Machine dans Applications, puis ouvrez-la depuis ce dossier. macOS vous demande une fois si vous voulez ouvrir une application téléchargée sur Internet : choisissez Ouvrir. Elle est signée et notariée, et se met à jour automatiquement.

## Linux

- Toute distribution : rendez l’AppImage exécutable avec `chmod +x`, puis lancez-la. Si un message indique que FUSE est manquant, installez `fuse3`.
- Ubuntu 22.04, Debian 12 ou version ultérieure : `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK et gtk-layer-shell sont inclus.
- Arch et Omarchy : placez le PKGBUILD dans un dossier vide, puis exécutez `makepkg -si` dans ce dossier. Il télécharge la version correspondante, la vérifie avec la somme de contrôle indiquée dans le fichier, puis l’installe. Sous Hyprland, comme dans Omarchy, le robot reste au-dessus des autres fenêtres sans avoir sa propre fenêtre.

L’AppImage se met à jour automatiquement si elle se trouve dans un dossier qui vous appartient, comme ~/Applications : ses Paramètres indiquent quand une nouvelle version est prête. Le fichier .deb et le paquet Arch sont gérés par apt et pacman. Les Paramètres indiquent quand une version plus récente est disponible, avec Télécharger pour le fichier .deb ou le PKGBUILD. Une AppImage décompressée dans un dossier ne se met pas à jour automatiquement : utilisez l’AppImage telle quelle.

## Vérifier un téléchargement

Chaque fichier inclut la preuve de provenance de GitHub, qui indique qu’il a été créé à partir du code de The Machine par son propre workflow. Avec la [CLI GitHub](https://cli.github.com) : `gh attestation verify <file> -R Salesflare/TheMachine`.

## Se connecter

La première fois, la fenêtre de l’application vous invite à vous connecter. Pour une Machine hébergée ou une Machine sur The Machine Network, votre compte s’ouvre dans votre navigateur, puis l’application s’affiche de nouveau. Pour une Machine auto-hébergée, vous devez saisir son adresse, depuis un ordinateur connecté à votre réseau Tailscale.

Une page de votre Machine peut afficher l’application au premier plan grâce à son propre lien, `computer.themachine.desktop://open`. Ce lien ouvre uniquement l’application et ne transmet aucune information.

Pour utiliser le tableau de bord comme une application Chrome ou Edge, consultez [Installer l’application](phone-app.md).

## Le robot

Le robot disparaît lorsque la fenêtre de l’application est au premier plan et réapparaît lorsqu’une autre fenêtre l’est, ou lorsque vous réduisez ou fermez l’application. Si vous avez plusieurs écrans, il apparaît sur celui où se trouve la fenêtre de l’application, jusqu’à ce que vous le déplaciez ailleurs. Sous Hyprland, Sway et KDE, il apparaît sur l’écran principal. Pour l’activer ou le désactiver : Paramètres (Ctrl+virgule, ou Commande-virgule sur Mac), Afficher le robot.
