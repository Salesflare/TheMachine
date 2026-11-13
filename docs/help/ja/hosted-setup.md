---
title: ホスト型のMachineを設定する
area: getting-started
summary: サインインして無料期間を開始し、メールを接続してAIを選びます。数分で完了します。
code: onboarding.py, dashboard.html
site: Mail and Calendar, Your AI, Continue with Google, Continue with Microsoft, Turn on, Add more any time, More sources, Open your dashboard, Sources, Ask for a source, Build it, Add a passkey, Use an authenticator app instead, Add to Claude, First to-dos, Back
order: 1
---
ホスト型のMachineは、EU内のクラウドで専用に動作します。The Machineが稼働を維持し、更新します。

## 登録する

1. app.themachine.computerで**Googleで続行**または**Microsoftで続行**を押します。アカウントが作成されます。Googleの場合、同じ画面でGmailとカレンダーへのアクセスも求められます。許可すると、Googleの画面をもう一度開かずにメールが接続されます。
2. Machineのサイズとアドレスを選びます。最初の{trial_days}日間は無料で、期間が終わるまでは請求されません。設定中に支払いカードを求められなかった場合は、その前にアカウントページで追加してください。
3. **パスキーを追加**を押し、指紋、顔認証、またはデバイスのPINを使います。認証アプリを使う場合は、**代わりに認証アプリを使う**を開き、コードをスキャンして6桁の数字を入力し、**オンにする**を押します。続けて表示されるリカバリーコードを保存してください。

## 設定ページ

設定は画面ごとに1ステップずつ進みます。プラン、パスキーのあとに、**メールとカレンダー**、**AI**、**最初のToDo**が続きます。上部に現在のステップが表示されます。Machineはバックグラウンドで起動するため、待つ必要はありません。

1. **メールとカレンダー**：**Googleに接続**または**Microsoftに接続**を押します。登録に使ったアカウントが最初に表示されます。Googleで登録したときにGmailとカレンダーへのアクセスを許可している場合、このステップは省略され、AIの設定に進みます。仕事用か個人用かはメールアドレスから判断されます。あとからアカウントで変更できます。[Gmail](gmail.md)と[Microsoft](microsoft.md)をご覧ください。
2. **AI**：ChatGPTまたはClaudeでサインインするか、AIプロバイダーのキーを貼り付けます。Claudeの場合は、Claudeのページに表示されるコードを貼り付けます。プランがない場合は、ChatGPTかClaudeを利用するか、キーを使ってください。このステップから各プロバイダーのキーのページを開けます。料金はプロバイダーから使用量に応じて請求されます。[ChatGPT](chatgpt.md)をご覧ください。
3. **最初のToDo**：Machineはまず最新のメールを確認し、その後、過去7日間のメールを確認します。対応が必要なものがない場合は、確認した内容と次に接続するものが表示されます。確認に失敗した場合は数分以内に再試行します。失敗が続く場合はリストに表示されます。

**戻る**またはブラウザーの戻るボタンで、ひとつ前のステップに戻れます。メールとAIが使えるようになると、ダッシュボードが表示されます。

設定に任意の項目はありません。設定後は、設定ページの**いつでも追加**から**その他のソース**を開き、Slack、WhatsApp、GitHub、[Telegram](telegram.md)、[Codex](hand-to-agent.md)などを追加できます。ダッシュボードでも、役立つタイミングでソースが提案されます。たとえばGitHubからのメールが届き続けると、GitHubが提案されます。

Machineの準備ができると、上部に**ダッシュボードを開く**が表示されます。**Claudeに追加**すると、ClaudeでメールやToDoについて質問できます。通知を受け取るには、The Machineをスマートフォンのホーム画面に追加してください。[アプリをインストールして通知をオンにする](phone-app.md)をご覧ください。

## ソースをリクエストする

必要なソースがありませんか？**ソース**の**ソースをリクエスト**で、サービス名と読み取る内容を入力し、**作成する**を押します。使用中のAIがMachine上でソースを作成し、テストします。共有を選ぶと、The MachineがGitHubで公開し、誰でも使えるようにします。GitHubアカウントは不要です。[GitHubを接続](github.md)すると、作成者として記録されます。

## あとで戻る

設定ページはapp.themachine.computer/setupにあります。ここではいつでもソースを追加、削除できます。ダッシュボードの**設定**から**アカウントを開く**を選べます。
