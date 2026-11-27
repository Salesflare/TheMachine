---
title: L’application pour ordinateur
area: getting-started
summary: The Machine sur Windows, Mac et Linux : votre tableau de bord dans sa propre fenêtre, et un petit robot dans un coin de l’écran.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
L’application pour ordinateur ouvre votre tableau de bord dans sa propre fenêtre. Un petit robot apparaît dans un coin de l’écran : cliquez dessus pour ajouter une tâche, poser une question sur vos messages ou voir ce qui vous attend. C’est un prototype.

## Télécharger

Chaque lien donne toujours accès à la dernière version :

- Windows 10 ou 11, 64 bits : [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac avec macOS 13 ou une version ultérieure : [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits : [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), le fichier [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) pour Ubuntu et Debian, ou le [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) pour Arch et Omarchy

## Windows

Ouvrez le programme d’installation. Il s’installe uniquement pour vous, sans droits d’administrateur, et est signé par Salesflare. Sur un ordinateur qui n’a encore jamais utilisé WebView2, sa préparation prend quelques secondes de plus. L’application démarre juste après. Elle se met à jour automatiquement : ses **Paramètres** vous indiquent quand une nouvelle version est prête.

## Mac

Décompressez le fichier zip, déplacez The Machine dans Applications, puis ouvrez-la depuis ce dossier. macOS vous demande une fois si vous souhaitez ouvrir une application téléchargée sur Internet : choisissez Ouvrir. L’application est signée et notariée, et se met à jour automatiquement.

## Linux

- Toutes les distributions : rendez l’AppImage exécutable avec `chmod +x`, puis lancez-la. Si un message indique que FUSE est absent, installez `fuse3`.
- Ubuntu 22.04, Debian 12 ou version ultérieure : `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK et gtk-layer-shell sont inclus.
- Arch et Omarchy : placez le PKGBUILD dans un dossier vide et exécutez `makepkg -si` depuis ce dossier. Le fichier correspondant à cette version est téléchargé, puis vérifié à l’aide de la somme de contrôle indiquée dans le fichier avant l’installation. Sous Hyprland, comme dans Omarchy, le robot reste au-dessus des autres fenêtres sans avoir sa propre fenêtre.

Sous Linux, l’application ne se met pas à jour automatiquement. Pour installer une version plus récente, téléchargez à nouveau le fichier ou le PKGBUILD le plus récent.

## Vérifier un téléchargement

Chaque fichier dispose des attestations de provenance de build de GitHub, qui confirment qu’il a été créé à partir du code de The Machine par son propre workflow. Avec [GitHub CLI](https://cli.github.com) : `gh attestation verify <file> -R Salesflare/TheMachine`.

## Se connecter

Lors de la première ouverture, une fenêtre vous invite à vous connecter. Pour une Machine hébergée ou une Machine sur The Machine Network, elle ouvre votre compte dans votre navigateur, puis revient à l’application. Pour une Machine auto-hébergée, indiquez son adresse, accessible depuis un ordinateur connecté à votre réseau Tailscale.

Pour utiliser le tableau de bord dans Chrome ou Edge comme une application, consultez [Installer l’application](phone-app.md).
