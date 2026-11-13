---
title: Telegram
area: connections
summary: 自分専用のボットを使って、ダッシュボードと同じボタン付きのToDoをTelegramで受け取れます。任意で設定できます。
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## できること

自分専用のボットから、[勤務時間](work-hours.md)内にTelegramでToDoを受け取れます。各ToDoには、ダッシュボードと同じボタンが表示されます。**実行**、**スヌーズ**、**修正を依頼**、**完了にする**、**不要**、準備済みのメッセージを送る**送信**です。代わりにThe MachineにTelegramのチャットを読み取らせる方法については、[Telegramのチャット](telegram-chats.md)をご覧ください。

設定は任意です。スマホアプリでも同じToDoを通知で受け取れます。

## 送信できる内容

自分専用のボットから自分宛てに送信するメッセージのみです。ほかの人宛てのメッセージを送信するには、引き続きToDoでの承認が必要です。

## 接続する

ホスト型のMachineの場合：

1. Telegramで@BotFatherにメッセージを送り、/newbotを送信します。発行されたトークンをコピーします。
2. セットアップページの**いつでも追加**からTelegramを開き、トークンを貼り付けて**自分のボットを追加**を押します。

いつでも追加できます。

自分のパソコンで使う場合は、インストーラーで入力するか、TelegramのユーザーIDを指定して`assistant telegram on`を実行します。

## 削除する

- ホスト型のMachineの場合：セットアップページで**Telegramの接続を解除**を押します。ボットとそのトークンがMachineから削除されます。
- 自分のパソコンで使う場合：`assistant telegram off`。ボットの情報も削除するには`--remove-bot`を追加します。

## Telegramでボットを削除する

@BotFatherにメッセージを送り、/deletebotを送信して、ボットを選びます。
