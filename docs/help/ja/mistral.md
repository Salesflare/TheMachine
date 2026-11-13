---
title: Mistral
area: connections
summary: Mistralのモデルを使ってThe Machineを動かせます。MistralのAPIキーが必要です。Le Chat ProにはAPIクレジットが含まれています。
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key, Keys, Remove
---
## 用途

MistralはヨーロッパのAIプロバイダーです。MistralのAPIキーを使うと、The MachineがMistralのモデルで情報を読み取り、下書きを作成します。The Machine独自のAIはありません。リクエストは、お使いのアカウントとMistralの利用規約に基づいて、Mistralに直接送られます。

## APIキーを取得する

Mistralには他のアプリ用のサインイン機能がないため、APIキーを使います。[Mistralコンソール](https://console.mistral.ai/)を開き、APIキーのページでキーを作成してください。Le Chat Proには毎月のAPIクレジットが含まれています。クレジットを使い切ると、Mistralから利用分が請求されます。

## 接続する

ホスト版のMachineでは、セットアップページを開き、Your AIに移動して**その他のAIサービス**を開きます。プロバイダーにMistralを選び、キーを貼り付けて**キーを保存**を押します。まず、キーを使ってごく小さなリクエストを1件試します。キーが間違っている場合はその場で表示され、何も保存されません。

メインモデルはMistral Largeになります。チャット用やフォールバック用に、より低価格なMistral Smallも利用できます。

自分のコンピューターで使う場合は、[モデルガイド](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md)をご覧ください。

## 使用状況

**設定**の**モデル**には「MistralのAPIキーを使用します」と表示されます。APIキーには利用制限がないため、バックグラウンド処理が利用制限で一時停止することはありません。[モデル](model.md)をご覧ください。

## 接続を解除する

セットアップページのYour AIで、**キー**にあるMistralの横の**削除**を押します。キーがThe Machineから削除されます。Mistralがメインモデルだった場合は、接続済みの別のモデルに切り替わります。APIキー自体を無効にするには、Mistralコンソールで削除してください。
