---
title: デスクトップアプリ
area: getting-started
summary: Windows、Mac、Linuxで使えるThe Machine。専用ウィンドウでダッシュボードを開き、画面の隅にロボットを表示します。
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
デスクトップアプリでは、ダッシュボードが専用ウィンドウで開きます。画面の隅には小さなロボットが表示されます。クリックすると、ToDoを追加したり、メッセージについて質問したり、自分向けの情報を確認したりできます。これはプロトタイプです。

## ダウンロードする

各リンクから常に最新バージョンをダウンロードできます。

- Windows 10または11、64ビット：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13以降のMac：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux、64ビット：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、UbuntuとDebian向けの[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)、またはArchとOmarchy向けの[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

ダッシュボードにもダウンロードリンクがあります。コンピューターでは、**設定**の**アプリ**に3つすべてが表示され、自分のコンピューターには**このコンピューター**と表示されます。**The Machineをもっと活用する**ToDoには**デスクトップアプリをダウンロード**があり、コンピューターに合ったアプリをダウンロードするか、下記のLinuxの手順を開けます。Machineにログインすると、この項目は表示されなくなります。どちらもスマートフォンやデスクトップアプリ内には表示されません。

## Windows

インストーラーを開きます。管理者権限なしで自分専用にインストールされ、Salesflareの署名が付いています。WebView2を使うアプリがまだないコンピューターでは、準備に数秒余分にかかりますが、その後すぐにアプリが起動します。アプリは自動更新され、新しいバージョンが準備できると**設定**に表示されます。

## Mac

zipを展開し、The Machineを「アプリケーション」に移動して、そこから開きます。macOSでインターネットからダウンロードしたアプリを開くときに一度確認が表示されるので、「開く」を選びます。署名と公証が済んでおり、自動更新されます。

## Linux

- どのディストリビューションでも使えます。`chmod +x`でAppImageに実行権限を付けて起動します。FUSEがないというメッセージが表示された場合は、`fuse3`をインストールします。
- Ubuntu 22.04、Debian 12以降：`sudo apt install ./the-machine-desktop-amd64.deb`。WebKitGTKとgtk-layer-shellも一緒にインストールされます。
- ArchとOmarchy：PKGBUILDを空のフォルダーに置き、そこで`makepkg -si`を実行します。該当バージョンをダウンロードし、ファイル内のチェックサムと照合してからインストールします。OmarchyのようなHyprlandでは、ロボットは専用ウィンドウを使わず、ほかのウィンドウより前面に表示されます。

Linuxではアプリは自動更新されません。新しいバージョンを使うには、ファイルまたは新しいPKGBUILDをもう一度ダウンロードしてください。

## ダウンロードを確認する

すべてのファイルにはGitHubのビルド来歴情報があり、The Machineのコードから専用のワークフローでビルドされたことを確認できます。[GitHub CLI](https://cli.github.com)では、`gh attestation verify <file> -R Salesflare/TheMachine`を実行します。

## ログイン

初回起動時は、ログイン画面が開きます。ホスティング版MachineまたはThe Machine Network上のMachineでは、ブラウザーでアカウントが開き、ログイン後にアプリに戻ります。セルフホスト版Machineでは、Tailscaleネットワーク上のコンピューターからMachineのアドレスを入力します。

ChromeまたはEdgeでダッシュボードをアプリとして使うには、[アプリをインストールする](phone-app.md)をご覧ください。

## ロボット

アプリのウィンドウが前面にある間、ロボットは表示されません。別のウィンドウが前面に来るか、アプリを最小化または閉じると、再び表示されます。モニターが複数ある場合、ロボットはアプリのウィンドウがあるモニターに表示されます。別の場所にドラッグすることもできます（Hyprland、Sway、KDEではメインモニターに表示されます）。オフまたはオンにするには、**設定**（Ctrl+comma、MacではCommand-comma）を開き、**ロボットを表示**を選びます。
