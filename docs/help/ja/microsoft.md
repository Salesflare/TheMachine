---
title: Microsoft Outlook とカレンダー
area: connections
summary: Microsoft 365 と Outlook.com のメールと予定に接続します。メールは承認後にのみ送信されます。
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
---
## 読み取る情報

- **Outlook**：すべてのメールを読み取ります。接続時は過去7日分、その後は新着メールを読み取ります。
- **Outlook カレンダー**：予定を読み取ります。変更はしません。

「その他」のメールやニュースレターは、まず送信者、件名、本文の一部だけを確認します。重要なものは全文を読み取り、ToDoにできます。

## 送信・変更できる内容

- ToDoからメールを送信できます。送信前に承認が必要です。メールはエイリアスではなく、メールボックス自体のアドレスから送信されます。
- 返信は、返信先メールのOutlookの会話に追加されます。
- メールに関するToDoをスヌーズすると、そのスレッドのメールはOutlookの「スヌーズ済み」フォルダーに移動し、ToDoの再開時に戻ります。

カレンダーが変更されることはありません。

## 同僚や連絡先の写真

Microsoftに、組織内の基本プロフィール（名前、メールアドレス、写真）とOutlookの連絡先の読み取りも許可します。The Machineは、Graphにすでに登録されている人の写真、役職、会社名の表示にのみ使用します。写真は1日あたり最大200枚まで取得します。写真がない人は、30日後に再確認します。

同僚の写真の取得には、組織の管理者による承認が必要な場合があります。承認されなくてもOutlookには接続できますが、写真は表示されません。この機能の追加前に接続したアカウントには、ToDoが1件届きます。**再接続**を押すか、**不要**を押して完全に閉じてください。個人アカウント（Outlook.com、Hotmail）には同僚がいないため、ToDoでは連絡先の写真のみを確認します。

## 接続する

ホスト型のMachineの場合：

1. app.themachine.computer/setupでセットアップページを開きます。
2. **Microsoftに接続**を押して、サインインします。
3. Microsoftから管理者の承認を求められた場合は、Microsoft 365の管理者にリンクを送信します（**リンクをコピー**）。承認されると、組織内の全員が接続できるようになります。管理者の場合は、**管理者です：今すぐ承認**を押します。

または、ダッシュボードで**接続**、**メール**の順に開き、Outlookを選んで**Microsoftでサインイン**を押します。管理者用のリンクはボタンのすぐ下にあります。

自分のコンピューターの場合は、[アカウントとペアリング](friends.md#a-machine-on-your-own-computer)した後、**接続**を開き、**メール**からOutlookを選んで**Microsoftでサインイン**を押します。メールとカレンダーは一緒に接続されます。Microsoftでの操作後、ダッシュボードの**接続**に戻ります。

独自のMicrosoft Entraアプリを使うITチームの場合は、そこで**独自のアプリを使用**を開くか、`assistant connect outlook`を実行します。

## 接続を解除する

- ホスト型のMachineの場合：セットアップページでアカウントの横にある**接続を解除**を押します。接続ページの**接続を解除 ↗**からも移動できます。
- 自分のコンピューターの場合：**接続**を開き、アカウントを選んで、**詳細**、**接続を解除**の順に選びます。

## Microsoftでアプリをアンインストールする

Microsoftではサインインの取り消しができないため、Microsoft側でも削除してください。

- 職場または学校のアカウント：myapps.microsoft.com
- 個人アカウント：account.live.com/consent/Manage
