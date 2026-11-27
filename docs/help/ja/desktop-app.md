---
title: デスクトップアプリ
area: getting-started
summary: Windows、Mac、Linuxで使えるThe Machine。専用ウィンドウでダッシュボードを開き、画面の隅にロボットを表示します。
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: af0a8a2994af969d
---
デスクトップアプリでは、専用ウィンドウでダッシュボードを開けます。画面の隅に小さなロボットが表示されます。クリックすると、ToDoを追加したり、メッセージについて質問したり、自分向けの情報を確認したりできます。これはプロトタイプです。

## ダウンロード

各リンクから常に最新バージョンをダウンロードできます。

- Windows 10または11、64-bit：[the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13以降のMac：[the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux、64-bit：[AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage)、UbuntuとDebian用の[.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb)、またはArchとOmarchy用の[PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

ダッシュボードからもダウンロードできます。コンピューターで**設定**の**アプリ**を開くと、3つすべてが表示されます。使用中のコンピューターには**このコンピューター**と表示されます。**The Machineをもっと活用する**ToDoには**デスクトップアプリをダウンロード**があります。使用中のコンピューター用のアプリをダウンロードするか、Linuxの場合は下記の手順が開きます。アプリでMachineにログインすると、このToDoは消えます。スマートフォンやデスクトップアプリ内には、どちらも表示されません。

## Windows

インストーラーを開きます。管理者権限は不要で、自分だけにインストールされます。Salesflareによる署名付きです。WebView2を使ったことのないコンピューターでは、準備に数秒余分にかかりますが、その後すぐにアプリが起動します。アプリは自動更新され、新しいバージョンが準備できると設定に表示されます。

## Mac

zipを展開し、The Machineを「アプリケーション」に移動して、そこから開きます。macOSでインターネットからダウンロードしたアプリを開くときは、一度だけ確認が表示されます。「開く」を選んでください。署名と公証が済んでおり、自動更新されます。

## Linux

- すべてのディストリビューション：`chmod +x`でAppImageに実行権限を付けて起動します。FUSEがないと表示された場合は、`fuse3`をインストールします。
- Ubuntu 22.04、Debian 12以降：`sudo apt install ./the-machine-desktop-amd64.deb`を実行します。WebKitGTKとgtk-layer-shellも一緒にインストールされます。
- ArchとOmarchy：空のフォルダーにPKGBUILDを置き、そこで`makepkg -si`を実行します。そのバージョンをダウンロードし、ファイル内のチェックサムと照合してからインストールします。OmarchyのようなHyprland環境では、ロボットは専用ウィンドウを使わず、ほかのウィンドウより前面に表示されます。

AppImageを~/Applicationsなどの自分のフォルダーに置くと、自動更新されます。新しいバージョンが準備できると設定に表示されます。.debとArchパッケージはaptとpacmanで管理されます。設定には新しいバージョンが出たことが表示され、.debまたはPKGBUILD用の「ダウンロード」が表示されます。フォルダーに展開したAppImageは自動更新されません。AppImageは展開せず、そのまま使ってください。

## ダウンロードの確認

すべてのファイルにはGitHubのビルド来歴があり、The Machineのコードから専用のワークフローでビルドされたことを確認できます。[GitHub CLI](https://cli.github.com)を使う場合：`gh attestation verify <file> -R Salesflare/TheMachine`。

## ログイン

初回はログイン画面が開きます。ホスティング版MachineまたはThe Machine Network上のMachineでは、ブラウザーでアカウントを開いてからアプリに戻ります。セルフホスト版Machineでは、Tailscaleネットワーク内のコンピューターからMachineのアドレスを入力します。

Machineのページから、専用リンク`computer.themachine.desktop://open`でアプリを前面に表示できます。このリンクはアプリを開くだけで、情報は含まれていません。

ChromeまたはEdgeでダッシュボードをアプリとして使うには、[アプリをインストールする](phone-app.md)をご覧ください。

## ロボット

アプリのウィンドウが前面にある間、ロボットは非表示になります。別のウィンドウが前面になるか、アプリを最小化または閉じると再び表示されます。モニターが複数ある場合、ロボットはアプリのウィンドウがあるモニターに表示されます。別の場所にドラッグして移動することもできます。Hyprland、Sway、KDEではメインモニターに表示されます。ロボットの表示を切り替えるには、「設定」（Ctrl+カンマ、MacではCommand+カンマ）を開き、**ロボットを表示**を選びます。
