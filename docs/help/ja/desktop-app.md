---
title: デスクトップアプリ
area: getting-started
summary: Windows、Mac、Linuxで使えるThe Machine。専用ウィンドウにダッシュボードが開き、画面の隅にはロボットが表示されます。
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
デスクトップアプリを開くと、専用ウィンドウにダッシュボードが表示されます。画面の隅には小さなロボットが表示されます。クリックすると、ToDoを追加したり、メッセージについて質問したり、自分向けの情報を確認したりできます。これはプロトタイプです。

## ダウンロード

各リンクから、いつでも最新バージョンをダウンロードできます。

- Windows 10または11、64ビット：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13以降のMac：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux、64ビット：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、UbuntuとDebian用の[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)、またはArchとOmarchy用の[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

## Windows

インストーラーを開きます。管理者権限は不要で、自分だけにインストールされます。Salesflareによる署名済みです。WebView2を使ったことのないコンピューターでは、準備に数秒ほど余分にかかります。準備ができると、アプリがすぐに起動します。アプリは自動で更新されます。新しいバージョンが準備できると、設定に表示されます。

## Mac

zipファイルを解凍し、The Machineをアプリケーションフォルダーに移動して、そこから開きます。インターネットからダウンロードしたアプリを開くとき、macOSが一度だけ確認します。「開く」を選択してください。署名と公証を受けており、自動で更新されます。

## Linux

- すべてのディストリビューション：`chmod +x`を実行してAppImageに実行権限を付与し、起動します。FUSEが見つからないと表示された場合は、Archでは`fuse2`、Ubuntu 24.04では`libfuse2t64`をインストールしてください。
- Ubuntu 22.04、Debian 12以降：`sudo apt install ./the-machine-desktop-amd64.deb`。WebKitGTKとgtk-layer-shellもインストールされます。
- ArchとOmarchy：PKGBUILDを空のフォルダーに置き、そのフォルダーで`makepkg -si`を実行します。該当バージョンをダウンロードし、ファイル内のチェックサムと照合してからインストールします。OmarchyのようにHyprlandを使っている場合、ロボットは専用ウィンドウを使わず、ほかのウィンドウより前面に表示されます。

Linuxではアプリは自動更新されません。新しいバージョンを使うには、ファイルまたは新しいPKGBUILDを再度ダウンロードしてください。

## ログイン

初回は、ログイン画面がウィンドウに表示されます。ホスティング版MachineまたはThe Machine Network上のMachineの場合、ブラウザーでアカウントが開き、アプリに戻ります。セルフホスト版Machineの場合は、Tailscaleネットワーク上のコンピューターからアクセスできるアドレスを入力します。

ChromeまたはEdgeのアプリとしてダッシュボードを使う場合は、[アプリをインストールする](phone-app.md)をご覧ください。
