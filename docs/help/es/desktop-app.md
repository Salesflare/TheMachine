---
title: La app de escritorio
area: getting-started
summary: The Machine en Windows, Mac y Linux: tu panel en una ventana propia y un robot en una esquina de la pantalla.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
La app de escritorio abre tu panel en una ventana propia. Hay un pequeño robot en una esquina de la pantalla: haz clic en él para crear una tarea, preguntar por tus mensajes o ver qué hay para ti. Es un prototipo.

## Descargar

Cada enlace siempre tiene la versión más reciente:

- Windows 10 u 11, 64 bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o posterior: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), el [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu y Debian, o el [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch y Omarchy

## Windows

Abre el instalador. Se instala solo para ti, sin necesidad de permisos de administrador, y está firmado por Salesflare. En los ordenadores donde nunca se haya usado WebView2, la preparación tarda unos segundos más. Después, la app se inicia de inmediato. La app se actualiza automáticamente: en **Ajustes** se indica cuándo hay una nueva versión lista.

## Mac

Descomprime el archivo, mueve The Machine a Aplicaciones y ábrela desde allí. macOS te pregunta una vez si quieres abrir una app descargada de Internet: elige **Abrir**. Está firmada y notarizada, y se actualiza automáticamente.

## Linux

- Cualquier distribución: da permisos de ejecución al AppImage con `chmod +x` y ábrelo. Si indica que falta FUSE, instala `fuse3`.
- Ubuntu 22.04, Debian 12 o posterior: `sudo apt install ./the-machine-desktop-amd64.deb`. Incluye WebKitGTK y gtk-layer-shell.
- Arch y Omarchy: coloca el PKGBUILD en una carpeta vacía y ejecuta `makepkg -si` allí. Descarga esa versión, la comprueba con el checksum del archivo y la instala. En Hyprland, como en Omarchy, el robot se mantiene por encima de las demás ventanas sin tener una ventana propia.

En Linux, la app no se actualiza automáticamente. Para instalar una versión más reciente, vuelve a descargar el archivo o el PKGBUILD actualizado.

## Comprobar una descarga

Todos los archivos incluyen la procedencia de compilación de GitHub, que muestra que se compilaron a partir del código de The Machine mediante su propio flujo de trabajo. Con la [CLI de GitHub](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Iniciar sesión

La primera vez, se abre una ventana para iniciar sesión. Si usas una Machine alojada o una en The Machine Network, se abre tu cuenta en el navegador y, después, vuelves a la app. Una Machine autohospedada necesita su propia dirección, desde un ordenador de tu red de Tailscale.

Si prefieres tener el panel como una app de Chrome o Edge, consulta [Instalar la app](phone-app.md).
