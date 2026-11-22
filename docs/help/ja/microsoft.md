---
title: Microsoft Outlookとカレンダー
area: connections
summary: Microsoft 365とOutlook.comのメールと予定に対応します。メールは承認後にのみ送信されます。
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: c10bf70a327b8ec0
---
## 読み取る情報

- **Outlook**：接続時には過去7日間のメールをすべて読み取り、その後は新着メールを読み取ります。
- **Outlookカレンダー**：会議の予定を読み取ります。読み取り専用です。

「その他」フォルダーのメールとニュースレターは、まず送信者、件名、本文の一部だけを確認します。重要なメールは全文を読み取り、ToDoにできます。

## 送信・変更できる内容

- ToDoからメールを送信できます。送信前に承認が必要です。メールはエイリアスではなく、メールボックス自体のアドレスから送信されます。
- 返信は、返信対象のメールがあるOutlookの会話に追加されます。
- 返信を送信すると、そのスレッドのメールは数日間（ToDoに別の指定がなければ3日間）Outlookの「スヌーズ」フォルダーに移動し、その後受信トレイに戻ります。相手から返信があれば、それより早く戻ります。送信前の確認画面にこの内容が表示されます。

カレンダーが変更されることはありません。

## 同僚や連絡先の写真

Microsoftには、組織内の基本プロフィール（名前、メールアドレス、写真）とOutlookの連絡先の読み取りも求められます。Machineは、Graphに登録済みの人の写真、役職、会社名の確認にのみ使用し、写真の確認は1日あたり最大200枚です。写真がない人は、30日後に再確認します。

同僚の写真を読み取るには、組織の管理者による承認が必要な場合があります。承認されなくてもOutlookには接続できますが、写真は取得されません。この変更より前に接続したアカウントには、ToDoが1件届きます。**再接続**を押すか、今後表示しない場合は**不要**を押してください。個人用アカウント（Outlook.com、Hotmail）には同僚がいないため、連絡先の写真についてのみToDoが表示されます。

## 接続する

ホスティング版のMachineの場合：

1. app.themachine.computer/setupでセットアップページを開きます。
2. **Microsoftに接続**を押して、ログインします。
3. Microsoftから管理者の承認を求められた場合は、リンク（**リンクをコピー**）をMicrosoft 365の管理者に送ります。承認されると、組織内の全員が接続できるようになります。自分が管理者の場合は、**管理者です：今すぐ承認**を押します。

または、ダッシュボードで**接続**、**メール**の順に開き、Outlookを選んで**Microsoftでログイン**を押します。管理者用リンクはボタンのすぐ下にあります。

自分のコンピューターの場合は、[アカウントとペアリング](friends.md#a-machine-on-your-own-computer)した後、**接続**を開き、**メール**を選択して、Outlookを選んで**Microsoftでログイン**を押します。メールとカレンダーは同時に接続されます。Microsoftでの操作後、ダッシュボードの**接続**に戻ります。

独自のMicrosoft Entraアプリを使うITチームは、ここで**自分のアプリを使用**を開くか、`assistant connect outlook`を実行してください。

## 接続を解除する

- ホスティング版のMachineの場合：セットアップページでアカウントの横にある**接続を解除**を押します。接続ページの**接続を解除 ↗**からも移動できます。
- 自分のコンピューターの場合：**接続**を開き、アカウントを選んで**詳細**を開き、**接続を解除**を押します。

## Microsoftでアプリをアンインストールする

Microsoftではログインの取り消しができないため、Microsoft側でも削除してください。

- 職場または学校のアカウント：myapps.microsoft.com
- 個人用アカウント：account.live.com/consent/Manage
