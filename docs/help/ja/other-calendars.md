---
title: iCloudなどのカレンダー（CalDAV）
area: connections
summary: iCloud CalendarやFastmail、Nextcloud、ZohoなどのCalDAVカレンダーの予定を読み込みます。読み取り専用です。
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
translated: 0ff916ed2bb877e1
---
## 読み込む内容

ゲスト、会議室、メモを含む予定を読み込みます。接続時は過去1週間分と今後1か月分、その後は変更があるたびに読み込みます。予定はCalendarに表示され、GoogleやOutlookの予定と同じように会議の準備にも使われます。アカウント内のすべてのカレンダー、または指定した1つのカレンダーを読み込みます。

読み取り専用のため、予定の追加、移動、削除は行いません。

## iCloud Calendarを接続する

1. [appleid.apple.com](https://appleid.apple.com)で、**サインインとセキュリティ**からApp用パスワードを作成します。iCloud Mail用に作成したパスワードも使えます。
2. ダッシュボードで**接続**を開き、**Calendar**を選んでから、**iCloud Calendar**を選びます。
3. Apple IDとApp用パスワードを入力し、**接続**を押します。

## 別のカレンダーを接続する

1. **接続**を開き、**Calendar**を選んでから、**その他のカレンダー**を選びます。
2. メールアドレスとパスワードを入力します。多くのプロバイダーでは、アカウント設定で作成したApp用パスワードが必要です。
3. **接続**を押します。

Fastmail、Yahoo、Zoho、およびサーバー情報を公開しているサーバーは、自動的に見つかります。見つからない場合は、**サーバー設定**を開き、`nextcloud.example.com/remote.php/dav`のようなCalDAVアドレスを入力します。**このカレンダーのみ**を選ぶと、名前を指定した1つのカレンダーだけを読み込みます。

GoogleまたはMicrosoftのカレンダーを使う場合は、代わりに**Google Calendar**または**Outlook Calendar**を選びます。

## 接続が停止した場合

- **カレンダーサーバーがパスワードを拒否しました**：パスワードを変更したか、App用パスワードが削除されています。新しいパスワードで再接続してください。
- **カレンダーサーバーに接続できませんでした**：自動的に再試行します。失敗が続く場合は、サーバー設定のアドレスを確認してください。

## 接続を解除する

**接続**を開き、カレンダーを選んで、**詳細**から**接続を解除**します。すでに読み込まれた内容は残ります。プロバイダー側でもApp用パスワードを削除してください。
