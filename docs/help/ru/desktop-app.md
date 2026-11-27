---
title: Приложение для компьютера
area: getting-started
summary: The Machine на Windows, Mac и Linux: ваша панель управления в отдельном окне и робот в углу экрана.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
Приложение открывает панель управления в отдельном окне. В углу экрана находится небольшой робот: нажмите на него, чтобы добавить задачу, спросить о сообщениях или узнать, что для вас. Это прототип.

## Скачать приложение

По каждой ссылке всегда доступна последняя версия:

- Windows 10 или 11, 64-разрядная версия: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac с macOS 13 или новее: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-разрядная версия: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), файл [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) для Ubuntu и Debian или [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) для Arch и Omarchy

## Windows

Откройте установщик. Приложение установится только для вашей учётной записи, права администратора не нужны. Установщик подписан Salesflare. На компьютере, где раньше не использовался WebView2, его подготовка займёт на несколько секунд больше, зато после этого приложение запустится сразу. Приложение обновляется автоматически. В разделе **Настройки** появится сообщение, когда будет доступна новая версия.

## Mac

Распакуйте архив, переместите The Machine в папку «Программы» и откройте приложение оттуда. macOS один раз спросит, хотите ли вы открыть приложение из интернета. Выберите **Открыть**. Приложение подписано и нотариально заверено, а обновления устанавливаются автоматически.

## Linux

- Любой дистрибутив: сделайте AppImage исполняемым с помощью `chmod +x` и запустите его. Если появится сообщение, что не хватает FUSE, установите `fuse3`.
- Ubuntu 22.04, Debian 12 или новее: `sudo apt install ./the-machine-desktop-amd64.deb`. В пакет уже входят WebKitGTK и gtk-layer-shell.
- Arch и Omarchy: поместите PKGBUILD в пустую папку и выполните там `makepkg -si`. Команда скачает нужную версию, проверит её по контрольной сумме в файле и установит. В Hyprland, как в Omarchy, робот остаётся поверх других окон и не занимает отдельное окно.

В Linux приложение не обновляется автоматически. Чтобы установить новую версию, скачайте файл заново или скачайте более новый PKGBUILD.

## Проверить загрузку

У каждого файла есть аттестация сборки GitHub, подтверждающая, что он собран из кода The Machine с помощью собственного workflow. С помощью [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Войти

При первом запуске откроется окно для входа. Если вы используете размещённую в облаке Machine или Machine в The Machine Network, приложение откроет вашу учётную запись в браузере, а затем вернётся в приложение. Для самостоятельно размещённой Machine укажите её адрес с компьютера в вашей сети Tailscale.

Если вместо этого вы хотите использовать панель управления как приложение Chrome или Edge, см. статью [Установить приложение](phone-app.md).
