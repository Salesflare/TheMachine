---
title: ChatGPT
area: connections
summary: ChatGPTのプランでThe Machineを動かし、ChatGPTのスキルをインポートできます。
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## 目的

ChatGPTでサインインすると、ご自身のChatGPTプランを使ってThe Machineが読み取りや下書きを行います。The Machine自体にAIはありません。リクエストはお使いのアカウントとOpenAIの利用規約に基づいて、直接OpenAIに送信されます。

## サインイン

ホスト環境のThe Machineでは、セットアップページで**ChatGPTでサインイン**を押し、ChatGPTに表示されたコードを入力します。後でサインアウトした場合は、**ChatGPTに再接続**を押してください。

OpenAIでコードが拒否される場合は、[ChatGPTのセキュリティ設定](https://chatgpt.com/settings/security)を開いて一番下までスクロールし、「Codex、Excel、PowerPoint、Wordのデバイスコードサインインを有効にする」をオンにしてください。その後、もう一度コードを入力します。

このスイッチが表示されない場合、仕事用アカウント（Business、Enterprise、Edu）では、ChatGPTの管理者が[権限とロール](https://chatgpt.com/admin/permissions)の「CodexとWork Local」で有効にします。

ご自身のコンピューターでは、ターミナルで`openclaw models auth login`を実行します。

## 利用上限

ChatGPTのプランには、5時間単位と週単位の利用上限があります。**設定**の**モデル**で、それぞれの使用量とリセット時刻を確認できます。自分のチャットに使える余裕を残すため、バックグラウンドの処理は上限に達するかなり前に一時停止します。上限に達すると、ダッシュボードの上部にリセット時刻が表示されます。[モデル](model.md)をご覧ください。

## ChatGPTのスキルをインポートする

**設定**の**スキル**で**インポート**を押し、**ChatGPTから**を選んで**自分のスキルを検索**を押します。インポートされるのは指示のみです。[スキル](skills.md)をご覧ください。

## 連携を解除する

セットアップページで別のモデルを選びます（ご自身のコンピューターでは、同じ方法で別のプロバイダーにサインインします）。OpenAI側でアクセスを取り消すには、ChatGPTのセキュリティ設定でセッションからサインアウトしてください。
