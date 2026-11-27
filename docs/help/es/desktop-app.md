---
title: La app de escritorio
area: getting-started
summary: The Machine en Windows, Mac y Linux: tu panel en una ventana propia y un robot en una esquina de la pantalla.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
La app de escritorio abre tu panel en una ventana propia. En una esquina de la pantalla aparece un pequeño robot: haz clic en él para añadir una tarea, preguntar por tus mensajes o ver qué tienes para ti. Es un prototipo.

## Descargarla

Cada enlace tiene siempre la versión más reciente:

- Windows 10 u 11, 64 bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac con macOS 13 o posterior: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), el [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu y Debian, o el [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch y Omarchy

También puedes encontrarlos en tu panel. En un ordenador, **Ajustes**, **Apps** muestra las tres opciones; en el tuyo aparece **Este equipo**. La tarea **Saca más partido a The Machine** incluye **Descarga la app de escritorio**, que descarga la versión para tu ordenador o abre los pasos de Linux de abajo. Desaparece cuando la app tiene la sesión iniciada en tu Machine. Ninguna de las dos aparece en el móvil ni dentro de la app de escritorio.

## Windows

Abre el instalador. Se instala solo para ti, sin permisos de administrador, y está firmado por Salesflare. Si nunca se ha usado WebView2 en el ordenador, tardará unos segundos más en prepararlo. Después, la app se inicia enseguida. La app se actualiza sola: en Ajustes se indica cuándo hay una nueva versión.

## Mac

Descomprime el archivo zip, mueve The Machine a Aplicaciones y ábrela desde allí. macOS te preguntará una vez si quieres abrir una app descargada de internet: selecciona Abrir. Está firmada y notarizada, y se actualiza sola.

## Linux

- Cualquier distribución: dale permisos de ejecución al AppImage con `chmod +x` y ejecútalo. Si indica que falta FUSE, instala `fuse3`.
- Ubuntu 22.04, Debian 12 o posterior: `sudo apt install ./the-machine-desktop-amd64.deb`. Incluye WebKitGTK y gtk-layer-shell.
- Arch y Omarchy: coloca el PKGBUILD en una carpeta vacía y ejecuta `makepkg -si` allí. Descarga esa versión, la comprueba con el checksum del archivo y la instala. En Hyprland, como en Omarchy, el robot se mantiene por encima de las demás ventanas sin tener una ventana propia.

El AppImage se actualiza solo si está en una carpeta tuya, como ~/Applications: en Ajustes se indica cuándo hay una nueva versión. El paquete .deb y el de Arch se actualizan con apt y pacman: en Ajustes se indica cuándo hay una versión más reciente, con la opción Descargar para el .deb o el PKGBUILD. Un AppImage descomprimido en una carpeta no se actualiza solo; usa el AppImage tal cual.

## Comprobar una descarga

Cada archivo incluye la procedencia de compilación de GitHub, que demuestra que se compiló a partir del código de The Machine mediante su propio flujo de trabajo. Con [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Iniciar sesión

La primera vez, se abre la ventana para iniciar sesión. Si usas una Machine alojada o una de The Machine Network, se abre tu cuenta en el navegador y luego vuelves a la app. Para una Machine alojada por ti, necesitas su dirección, desde un ordenador de tu red de Tailscale.

Si prefieres tener el panel como una app de Chrome o Edge, consulta [Instalar la app](phone-app.md).

## El robot

El robot desaparece mientras la ventana de la app está en primer plano y vuelve cuando otra ventana pasa a estarlo, o cuando minimizas o cierras la app. Si tienes más de un monitor, aparece en el monitor donde está la ventana de la app hasta que lo arrastres a otro sitio (en Hyprland, Sway y KDE, aparece en el monitor principal). Para activarlo o desactivarlo: Ajustes (Ctrl+coma o Command+coma en Mac), **Mostrar el robot**.
