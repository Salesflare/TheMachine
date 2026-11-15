---
title: Shortcut
area: connections
summary: 状態が変わったストーリーと、その担当者や期限を読み取ります。読み取り専用です。
covers: connector:shortcut
code: connectors/shortcut.py
site: Connect, More sources, Remove
translated: 2298e2fcb1af74b3
---
## 読み取る情報

Shortcutのワークスペースで状態が変わったストーリーと、その担当者や期限を読み取ります。

## できること

何もできません。Shortcutのトークンではさらに多くの操作ができますが、読み取り専用です。

## 接続する

1. ホスト版のMachineの場合：app.themachine.computer/setupでセットアップページを開き、**その他のソース**からShortcutを開きます。自分のコンピューターの場合：**接続**、**プロジェクトとコード**、Shortcutの順に開くか、`assistant connect shortcut`を実行します。
2. **トークンを取得**を押します。新しいタブでShortcutのAPIトークンページが開きます。トークンを作成してコピーします。
3. トークンを貼り付けて**接続**を押します。トークンがすぐに確認され、接続したユーザーとワークスペースが表示されます。

Shortcutのワークスペースが複数ありますか？トークンは1つのワークスペースに紐づくため、先にShortcutで該当のワークスペースに切り替えてください。

## 接続を解除する

- ダッシュボードで：**接続**を開き、Shortcut、**詳細**、**接続を解除**の順に選びます。すでに取り込まれた情報は残ります。
- ホスト版のMachineでは、セットアップページでShortcutの横にある**削除**を押すこともできます。

## Shortcutでトークンを取り消す

同じAPIトークンページでトークンを削除します。
