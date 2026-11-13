---
title: Exchange Server
area: connections
summary: 会社で運用している Exchange Server（2013～2019 または Subscription Edition）の予定を読み込みます。読み取り専用です。
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## 読み込む情報

予定と、参加者、会議室、メモを読み込みます。接続時に過去1週間分と翌月分を読み込み、その後は変更があるたびに反映します。予定はカレンダーと会議の準備画面に表示されます。

読み取り専用のため、予定の追加、移動、削除は行いません。Exchange Server のメールはまだ読み込めません。

## Microsoft 365 と Exchange Server の違い

Exchange Server は会社で運用するサーバーです。Microsoft 365（Exchange Online）は Microsoft のクラウドサービスなので、代わりに **Outlook カレンダー** を選んでください。メールアドレスが Microsoft 365 のものだと判明した場合は、フォームにその旨が表示されます。

## 接続する

1. ダッシュボードで **接続** を開き、**カレンダー** を選んでから **Exchange Server** を選びます。
2. 仕事用のメールアドレスと Windows のパスワードを入力します。
3. **接続** を押します。

サーバーはメールアドレスから自動検出されます（Autodiscover）。見つからない場合は、**サーバー設定** を開き、IT チームから案内された Outlook のサーバーを入力してください。例：`mail.example.com`。メールアドレスとは異なる名前でサインインする場合は、**ユーザー名** に `DOMAIN\name` を入力してください。

サインインには NTLM または Basic を使用し、https 経由でのみ接続します。

## 接続できなくなった場合

- **カレンダーサーバーでパスワードが拒否されました**：Windows のパスワードが変更されています。もう一度接続してください。
- **Microsoft 365 のメールボックスです**：メールボックスが Microsoft 365 に移動されています。この接続を解除して、**Outlook カレンダー** を接続してください。
- **カレンダーサーバーに接続できませんでした**：自動的に再試行します。会社のネットワークまたは VPN 内でしか接続できないサーバーもあります。

## 接続を解除する

**接続** を開き、カレンダーを選んで **詳細**、**接続を解除** の順に選びます。すでに読み込まれた情報はそのまま残ります。
