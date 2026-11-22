---
title: Androidの通知
area: connections
summary: OpenClawアプリを通じて、Androidスマートフォンの通知を読み取ります。読み取りのみです。
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## 読み取る情報

OpenClawアプリを通じて、Androidスマートフォンの通知を読み取ります。ワンタイムコードと、WhatsApp、Telegram、Signal、Discordの通知は読み取りません。

## できること

スマートフォン上で操作は行いません。通知を読み取るだけです。

## 接続する

ホスティング版のMachineの場合：

1. スマートフォンのGoogle PlayからOpenClawをインストールします。
2. ダッシュボードで**接続**を開き、**その他**からAndroidの通知を選んで、**設定コードを表示**を押します。
3. OpenClawアプリでGatewayを追加し、コードをスキャンします。ダッシュボードに戻り、**承認**を押します。
4. アプリの案内に従って通知へのアクセスを許可します。次に、アプリの設定でForward Notification Eventsをオンにします。通知が10分ごとの確認時だけでなく、届くたびに受信できるようになります。

自分のコンピューターの場合は、OpenClawアプリでスマートフォンをペアリングしてから、`assistant connect android`を実行します。

## 接続を解除する

- ダッシュボードで**接続**を開き、Androidの**詳細**から**接続を解除**を選びます。
- ホスティング版のMachineでは、セットアップページで対象の横にある**削除**を押す方法もあります。

## スマートフォンから削除する

Androidの設定でOpenClawアプリの通知へのアクセスをオフにするか、OpenClawアプリでスマートフォンのペアリングを解除します。
