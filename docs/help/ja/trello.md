---
title: Trello
area: connections
summary: 1つのTrelloボードのカードの変更、コメント、アクティビティを読み取ります。読み取り専用です。
covers: connector:trello
code: connectors/trello.py
site: Sign in with Trello, Connect, More sources, Remove
---
## 読み取る内容

接続ごとに1つのTrelloボードのカードの変更、コメント、アクティビティを読み取ります。ボードを閲覧済みにすることはありません。

## できること

Trelloでは何も実行しません。読み取り専用です。

## 接続する

1. ダッシュボードで、**接続**、**プロジェクトとコード**、Trelloの順に選びます。または、ホスト型Machineのセットアップページ app.themachine.computer/setup で、**その他のソース**、Trelloの順に選びます。自分のコンピューターで使う場合は、先にアカウントとペアリングします。
2. **Trelloでサインイン**を押して、読み取りアクセスを許可します。Trelloでは、このアプリの作成者としてSalesflareが表示されます。
3. 連携するボードを選び、**接続**を押します。別のボードを連携するには、Trelloをもう一度追加します。

## 接続を解除する

- ダッシュボードで、**接続**を選び、ボードを開いて、**詳細**、**接続を解除**の順に選びます。すでに取り込まれた内容は残ります。
- ホスト型Machineでは、セットアップページでその横にある**削除**を押して解除することもできます。

## Trelloでアクセスを取り消す

Trelloのアカウント設定の「アプリケーション」から、The Machineのアクセスを取り消します。
