---
title: デスクトップアプリ
area: getting-started
summary: Windows、Mac、Linuxで使えるThe Machine。専用ウィンドウにダッシュボードを表示し、画面の隅にはロボットがいます。
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
デスクトップアプリを開くと、専用ウィンドウにダッシュボードが表示されます。画面の隅には小さなロボットがいます。クリックすると、ToDoを追加したり、メッセージについて質問したり、自分向けの情報を確認したりできます。これはプロトタイプです。

## ダウンロード

リンク先には常に最新バージョンがあります。

- Windows 10または11、64ビット：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13以降のMac：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux、64ビット：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、UbuntuとDebian用の[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)、ArchとOmarchy用の[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

## Windows

インストーラーを開きます。管理者権限は不要で、自分だけにインストールされます。Salesflareによって署名されています。WebView2を使ったことがないコンピューターでは、準備に数秒余計にかかります。その後、アプリがすぐに起動します。アプリは自動で更新されます。新しいバージョンの準備が完了すると、**設定**に表示されます。

## Mac

zipを展開し、The Machineを「アプリケーション」に移動して開きます。macOSでは、インターネットからダウンロードしたアプリを開くときに一度だけ確認が表示されます。**開く**を選択してください。アプリは署名と公証を受けており、自動で更新されます。

## Linux

- どのディストリビューションでも使えます。`chmod +x`でAppImageに実行権限を付けて起動します。FUSEが見つからないと表示された場合は、`fuse3`をインストールしてください。
- Ubuntu 22.04、Debian 12以降：`sudo apt install ./the-machine-desktop-amd64.deb`。WebKitGTKとgtk-layer-shellも一緒にインストールされます。
- ArchとOmarchy：PKGBUILDを空のフォルダーに置き、そこで`makepkg -si`を実行します。対象バージョンをダウンロードし、ファイル内のチェックサムと照合してからインストールします。OmarchyのようにHyprlandを使っている場合、ロボットは独立したウィンドウを持たず、ほかのウィンドウより前面に表示されます。

Linuxではアプリは自動更新されません。新しいバージョンを使うには、ファイルまたは新しいPKGBUILDをもう一度ダウンロードしてください。

## ダウンロードを確認する

すべてのファイルにはGitHubのビルド来歴があり、The Machineのコードから専用のワークフローでビルドされたことを確認できます。[GitHub CLI](https://cli.github.com)を使います：`gh attestation verify <file> -R Salesflare/TheMachine`。

## ログイン

初回は、ログイン画面がウィンドウに表示されます。ホスティング版MachineまたはThe Machine Network上のMachineの場合、ブラウザーでアカウントを開き、アプリに戻ります。セルフホスト版Machineでは、Tailscaleネットワーク上のコンピューターからアクセスできるアドレスが必要です。

ChromeまたはEdgeのアプリとしてダッシュボードを使うには、[アプリをインストールする](phone-app.md)をご覧ください。
