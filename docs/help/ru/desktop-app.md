---
title: Настольное приложение
area: getting-started
summary: The Machine в Windows, Mac и Linux: ваша панель управления в отдельном окне и робот в углу экрана.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
Настольное приложение открывает вашу панель управления в отдельном окне. В углу экрана стоит маленький робот: нажмите на него, чтобы добавить задачу, спросить о сообщениях или посмотреть, что для вас. Это прототип.

## Скачать

По каждой ссылке всегда доступна последняя версия:

- Windows 10 или 11, 64-разрядная версия: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac с macOS 13 или новее: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-разрядная версия: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), файл [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) для Ubuntu и Debian или [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) для Arch и Omarchy

## Windows

Откройте установщик. Он установит приложение только для вашей учётной записи, без прав администратора. Установщик подписан Salesflare. Если на компьютере раньше не использовался WebView2, его установка займёт несколько секунд, после чего приложение сразу запустится. Приложение обновляется автоматически: в разделе **Настройки** появится сообщение, когда будет доступна новая версия.

## Mac

Распакуйте архив, переместите The Machine в папку «Программы» и откройте приложение оттуда. macOS один раз спросит, хотите ли вы открыть приложение из интернета: нажмите «Открыть». Приложение подписано, прошло нотариальную проверку и обновляется автоматически.

## Linux

- Любой дистрибутив: сделайте AppImage исполняемым с помощью `chmod +x` и запустите его. Если появится сообщение об отсутствии FUSE, установите `fuse2` на Arch или `libfuse2t64` на Ubuntu 24.04.
- Ubuntu 22.04, Debian 12 или новее: `sudo apt install ./the-machine-desktop-amd64.deb`. В этот пакет уже входят WebKitGTK и gtk-layer-shell.
- Arch и Omarchy: поместите PKGBUILD в пустую папку и выполните там `makepkg -si`. Команда скачает нужную версию, проверит её по контрольной сумме в файле и установит. В Hyprland, как в Omarchy, робот остаётся поверх других окон и не занимает отдельное окно.

В Linux приложение не обновляется автоматически. Чтобы установить новую версию, скачайте файл заново или загрузите более новый PKGBUILD.

## Войти

При первом запуске откроется окно входа. Для облачной Machine или Machine в The Machine Network приложение откроет вашу учётную запись в браузере и вернётся обратно. Для размещённой у себя Machine укажите её адрес, доступный с компьютера в вашей сети Tailscale.

Чтобы вместо этого установить панель управления как приложение Chrome или Edge, см. статью [Установить приложение](phone-app.md).
