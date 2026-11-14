---
title: Google Meet
area: connections
summary: 開催したGoogle Meetの会議の文字起こしとGeminiのメモを読み込みます。読み取り専用です。
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
translated: cea7230915b5a536
---
## 読み込む内容

Google Meetで開催した会議の文字起こしとGeminiのメモを読み込みます。Meetへの接続時には過去7日分を、その後は新しいものが追加されるたびに読み込みます。Meetでの保存期間は30日間です。

会議中に文字起こしかGeminiのメモが有効になっていた場合のみ、Meetが作成します。

読み込んだ内容は、カレンダーの該当する会議に追加されます。Geminiのメモは「メモ」に、文字起こしは「文字起こし」に追加され、**Google Meet から**と表示されます。自分で追加した内容はそのまま残ります。

## できること

Meet、Docs、Driveでは何も操作しません。読み取り専用で、文字起こしを有効にすることもありません。

## 求められる権限

メールとは別に、Google Meet専用の許可が必要です。Googleから、The Machineに次の権限を許可するよう求められます。

- Google Meetの会議、文字起こし、Geminiのメモを表示する
- Geminiのメモのドキュメントを読むために、Google Docsを表示する

Driveへのアクセスは求めません。Gmailとカレンダーのアクセス権は変わりません。

## 接続する

Gmailを接続する必要はありません。接続するには、次の手順に従ってください。

- ホスト型Machine：ダッシュボードで**接続**を開き、**会議**、**Google Meet**の順に選んで、**Googleでログイン**を押します。上記の権限を許可すると、ダッシュボードに戻ります。
- 自分のコンピューターでアカウントとペアリングする場合も、同じ手順です。ログイン画面は新しいタブで開きます。

Google Meetの権限を許可しないと、接続されません。貼り付けや更新は必要ありません。

あとで権限を取り消すと、**接続**のGoogle Meetから再度ログインするよう求められます。

## 接続を解除する

ダッシュボードで**接続**を開き、Google Meetの**詳細**から**接続を解除**します。すでに読み込んだ内容はそのまま残ります。

## Googleで権限を取り消す

myaccount.google.com/permissionsを開き、The MachineによるGoogle Meetへのアクセスを削除します。Gmailとカレンダーは引き続き使えます。
