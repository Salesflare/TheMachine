---
title: デスクトップアプリ
area: getting-started
summary: Windows、Mac、Linuxで使えるThe Machine。独立したウィンドウでダッシュボードを開き、画面の隅にロボットを表示します。
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
デスクトップアプリでは、独立したウィンドウでダッシュボードを開けます。画面の隅に小さなロボットが表示され、クリックするとToDoを追加したり、メッセージについて質問したり、自分向けの情報を確認したりできます。これはプロトタイプです。

## ダウンロード

各リンクから、いつでも最新版をダウンロードできます。

- Windows 10または11、64-bit：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13以降のMac：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux、64-bit：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、UbuntuとDebian用の[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)、またはArchとOmarchy用の[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

ダッシュボードからもダウンロードできます。コンピューターで**設定**の**アプリ**を開くと、3種類すべてが表示されます。現在使っているコンピューターには**このコンピューター**と表示されます。**The Machineをもっと活用する**ToDoには**デスクトップアプリをダウンロード**があり、コンピューターに合ったアプリをダウンロードできます。Linuxの場合は、下記の手順が開きます。Machineにログインすると、このToDoは表示されなくなります。スマートフォンやデスクトップアプリ内では表示されません。

## Windows

インストーラーを開きます。管理者権限は不要で、自分だけにインストールされます。Salesflareによって署名されています。WebView2を使ったことのないコンピューターでは、準備に数秒余分にかかります。準備が終わると、アプリがすぐに起動します。アプリは自動で更新されます。新しいバージョンが利用可能になると、**設定**に表示されます。

## Mac

zipを解凍し、The MachineをApplicationsに移動して、そこから開きます。macOSでは、インターネットからダウンロードしたアプリを開くときに一度だけ確認が表示されます。**開く**を選択してください。署名と公証を受けており、自動で更新されます。

## Linux

- どのディストリビューションでも：`chmod +x`でAppImageに実行権限を付けて、起動します。FUSEが見つからないというメッセージが表示された場合は、`fuse3`をインストールしてください。
- Ubuntu 22.04、Debian 12以降：`sudo apt install ./the-machine-desktop-amd64.deb`。WebKitGTKとgtk-layer-shellも一緒にインストールされます。
- ArchとOmarchy：PKGBUILDを空のフォルダーに置き、そこで`makepkg -si`を実行します。該当するバージョンをダウンロードし、ファイル内のチェックサムと照合してからインストールします。OmarchyのようなHyprland環境では、ロボットは独立したウィンドウを持たず、ほかのウィンドウより前面に表示されます。

AppImageを~/Applicationsなどの自分のフォルダーに置くと、自動で更新されます。新しいバージョンが利用可能になると、**設定**に表示されます。.debとArchパッケージはaptとpacmanで管理されます。新しいバージョンが公開されると、**設定**に表示され、.debまたはPKGBUILDの**ダウンロード**リンクが表示されます。フォルダーに展開したAppImageは自動更新されません。AppImageは展開せず、そのまま使ってください。

## ダウンロードを確認する

すべてのファイルにはGitHubのビルド来歴情報が付いています。The Machineのコードから、The Machine独自のワークフローでビルドされたことを確認できます。[GitHub CLI](https://cli.github.com)を使う場合：`gh attestation verify <file> -R Salesflare/TheMachine`。

## ログイン

初回は、ログイン画面がウィンドウに表示されます。ホスティング版MachineまたはThe Machine Network上のMachineでは、ブラウザーでアカウントが開き、ログイン後にアプリに戻ります。セルフホスト版Machineでは、Tailscaleネットワーク上のコンピューターからMachineのアドレスを入力します。

代わりにChromeまたはEdgeのアプリとしてダッシュボードを使う場合は、[アプリをインストールする](phone-app.md)をご覧ください。

## ロボット

アプリのウィンドウが前面にある間、ロボットは表示されません。別のウィンドウが前面になるか、アプリを最小化または閉じると、再び表示されます。モニターが複数ある場合、ロボットはアプリのウィンドウがあるモニターに表示されます。別の場所にドラッグすることもできます（Hyprland、Sway、KDEではメインモニターに表示されます）。表示のオン・オフは、「**設定**」（Ctrl+comma、MacではCommand-comma）から**ロボットを表示**を選びます。
