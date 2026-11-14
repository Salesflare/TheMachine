---
title: Androidの通知
area: connections
summary: Androidスマートフォンの通知をOpenClawアプリ経由で読み取ります。読み取り専用です。
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 344d64dafc75a0a9
---
## 読み取る内容

Androidスマートフォンの通知をOpenClawアプリ経由で読み取ります。ワンタイムコードと、WhatsApp、Telegram、Signal、Discordの通知は対象外です。

## できること

スマートフォン上で何かを操作することはありません。通知を読み取るだけです。

## 接続する

ホスト型のMachineの場合：

1. スマートフォンにGoogle PlayからOpenClawをインストールします。
2. ダッシュボードで**接続**を開き、**その他**を選んで「Androidスマートフォン」を選択し、**セットアップコードを表示**を押します。
3. OpenClawアプリでGatewayを追加し、コードをスキャンします。ダッシュボードに戻り、**承認**を押します。
4. アプリの案内に従って通知へのアクセスを許可します。次に、アプリの設定で「通知イベントを転送」をオンにすると、10分ごとの確認時だけでなく、通知が届くたびに通知が送られます。

自分のコンピューターの場合は、OpenClawアプリでスマートフォンをペアリングしてから、`assistant connect android`を実行します。

## 接続を解除する

- ダッシュボードで**接続**を開き、Androidを選択して**詳細**を開き、**接続を解除**を押します。
- ホスト型のMachineでは、セットアップページで対象の横にある**削除**を押して解除することもできます。

## スマートフォンで接続を解除する

Androidの設定でOpenClawアプリの通知へのアクセスをオフにするか、OpenClawアプリでスマートフォンのペアリングを解除します。
