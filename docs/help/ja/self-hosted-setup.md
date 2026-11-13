---
title: 自分のコンピューターで実行する
area: getting-started
summary: オープンソースアプリをLinux、macOS、Windowsにインストールできます。無料で、自分のモデルとデータを使えます。
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
The Machineは無料で自分のコンピューターで実行できます。オープンソース（AGPL）で、データは手元に残ります。インストールにはターミナルが必要ですが、アカウントの接続には必要ありません。

## 必要なもの

- OpenClaw 2026.11.2以降。The Machineが動作するオープンソースのエージェントです。インストーラーからインストールできます。
- Python 3.12以降と、Node.js 24（24.22.1以降）または26.12.1以降。25は使えません。
- スマートフォンからダッシュボードにアクセスするためのTailscale。
- rootではなく、通常のユーザーアカウント。

## インストール

LinuxまたはmacOSの場合（macOSはベータ版です）：

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Windowsの場合（ベータ版）、WSL2内で動作します。PowerShellで`irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`を実行してください。WSL2とUbuntu、アプリに必要なものをセットアップした後、`./install.sh`を実行します。

インストーラーがアカウントを見つけて1つずつ接続し、すべてを有効にする前に先週の内容をプレビューできます。

## インストール後

- メールを接続するには、**ToDo**の上部にある**Gmail**（または**Outlook**）を押し、続けて**このMachineをペアリング**を押してアカウントとペアリングします。アカウントがない場合は、そのすぐ下に**自分のアプリを使う**があります。
- 次に、**Googleでサインイン**（Outlookの場合は**Microsoftでサインイン**）を押します。メールとカレンダーが一緒に接続されます。
- その他のソースは、**接続**からソースの種類を選びます。独自のGoogleクライアントまたはEntraアプリを使う場合は、ターミナルで`assistant connect`を実行します。
- `assistant doctor`で問題がないか確認できます。問題ごとに修正方法が表示されます。
- 最新の署名済みリリースがインストールされ、アップデートも署名済みリリースとして提供されます。
- アカウントとペアリングすると、サインイン後にスマートフォンアプリから開けます。ペアリングを解除すると、その連携が削除されます。

詳しいガイドはリポジトリにあります：[はじめに](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md)。
