---
title: La app de escritorio
area: getting-started
summary: The Machine en Windows, Mac y Linux: tu panel en una ventana propia y un robot en una esquina de la pantalla.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
La app de escritorio abre tu panel en una ventana propia. Un pequeño robot aparece en una esquina de la pantalla: haz clic en él para añadir una tarea, preguntar por tus mensajes o ver qué tienes para ti. Es un prototipo.

## Descárgala

Cada enlace siempre tiene la versión más reciente:

- Windows 10 u 11, 64 bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o posterior: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), el [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu y Debian, o el [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch y Omarchy

También los encontrarás en tu panel. En un ordenador, **Ajustes**, **Apps** muestra los tres, y en el tuyo aparece **Este equipo**. La tarea **Saca más partido a The Machine** incluye **Descarga la app de escritorio**, que descarga la versión para tu ordenador o abre los pasos para Linux que aparecen más abajo. Desaparece cuando inicias sesión en la app con tu Machine. Ninguno aparece en un móvil ni dentro de la app de escritorio.

## Windows

Abre el instalador. Se instala solo para ti, sin necesidad de permisos de administrador, y está firmado por Salesflare. En un ordenador donde antes no se haya usado WebView2, tardará unos segundos más en prepararlo, y después la app se iniciará enseguida. La app se actualiza sola: en Ajustes te avisa cuando hay una nueva versión disponible.

## Mac

Descomprime el archivo zip, mueve The Machine a Aplicaciones y ábrela desde allí. macOS te preguntará una vez si quieres abrir una app descargada de internet: elige Abrir. Está firmada y notarizada, y se actualiza sola.

## Linux

- Cualquier distribución: convierte la AppImage en ejecutable con `chmod +x` y ábrela. Si indica que falta FUSE, instala `fuse3`.
- Ubuntu 22.04, Debian 12 o posterior: `sudo apt install ./the-machine-desktop-amd64.deb`. Incluye WebKitGTK y gtk-layer-shell.
- Arch y Omarchy: pon el PKGBUILD en una carpeta vacía y ejecuta `makepkg -si` allí. Descarga esa versión, la comprueba con el checksum del archivo y la instala. En Hyprland, como viene configurado en Omarchy, el robot permanece por encima de las demás ventanas sin tener una ventana propia.

En Linux, la app no se actualiza sola. Para instalar una versión más reciente, vuelve a descargar el archivo o descarga el PKGBUILD más reciente.

## Comprueba una descarga

Cada archivo incluye la procedencia de compilación de GitHub, que demuestra que se creó a partir del código de The Machine mediante su propio flujo de trabajo. Con la [interfaz de línea de comandos de GitHub](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Inicia sesión

La primera vez, se abre la ventana para iniciar sesión. Si usas una Machine alojada o una de The Machine Network, se abre tu cuenta en el navegador y luego vuelve a la app. Para una Machine autoalojada, necesitas su dirección, desde un ordenador conectado a tu red de Tailscale.

Si prefieres tener el panel como una app de Chrome o Edge, consulta [Instalar la app](phone-app.md).

## El robot

El robot desaparece mientras la ventana de la app está en primer plano y vuelve cuando otra ventana pasa al frente, o cuando minimizas o cierras la app. Si tienes más de un monitor, aparece en el que tiene la ventana de la app, hasta que lo arrastras a otro (en Hyprland, Sway y KDE, aparece en el principal). Para activarlo o desactivarlo: **Ajustes** (Ctrl+coma o Command+coma en un Mac), **Mostrar el robot**.
