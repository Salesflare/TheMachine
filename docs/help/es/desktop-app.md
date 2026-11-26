---
title: La app de escritorio
area: getting-started
summary: The Machine en Windows, Mac y Linux: tu panel en una ventana propia y un robot en una esquina de la pantalla.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
La app de escritorio abre tu panel en una ventana propia. Un pequeño robot aparece en una esquina de la pantalla: haz clic en él para añadir una tarea, preguntar por tus mensajes o ver qué tienes para ti. Es un prototipo.

## Descárgala

Cada enlace siempre tiene la versión más reciente:

- Windows 10 u 11, 64 bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o posterior: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), el archivo [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu y Debian, o el [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch y Omarchy

## Windows

Abre el instalador. Se instala solo para ti, sin necesidad de permisos de administrador, y está firmado por Salesflare. En un ordenador que no haya usado WebView2 antes, tardará unos segundos más en prepararlo, así que la app se abrirá justo después. La app se actualiza sola: en **Ajustes** te avisará cuando haya una versión nueva.

## Mac

Descomprime el archivo, mueve The Machine a Aplicaciones y ábrela desde allí. macOS te preguntará una vez si quieres abrir una app descargada de Internet: elige Abrir. Está firmada y notarizada, y se actualiza sola.

## Linux

- Cualquier distribución: da permisos de ejecución al AppImage con `chmod +x` e inícialo. Si indica que falta FUSE, instala `fuse2` en Arch o `libfuse2t64` en Ubuntu 24.04.
- Ubuntu 22.04, Debian 12 o posterior: `sudo apt install ./the-machine-desktop-amd64.deb`. Incluye WebKitGTK y gtk-layer-shell.
- Arch y Omarchy: coloca el PKGBUILD en una carpeta vacía y ejecuta `makepkg -si` allí. Descarga esa versión, la comprueba con la suma de verificación del archivo y la instala. En Hyprland, como viene configurado en Omarchy, el robot permanece por encima de las demás ventanas sin tener una ventana propia.

En Linux, la app no se actualiza sola. Para instalar una versión más reciente, vuelve a descargar el archivo o descarga el PKGBUILD más reciente.

## Iniciar sesión

La primera vez, se abrirá la ventana para iniciar sesión. Si usas una Machine alojada o una de The Machine Network, se abrirá tu cuenta en el navegador y luego volverá a la app. Una Machine autoalojada necesita su propia dirección, desde un ordenador de tu red de Tailscale.

Si prefieres usar el panel como una app de Chrome o Edge, consulta [Instalar la app](phone-app.md).
