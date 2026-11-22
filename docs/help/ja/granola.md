---
title: Granola
area: connections
summary: Granolaでの会議のメモと文字起こし。読み取り専用です。
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## 読み取る内容

参加した会議のGranolaのメモと文字起こしです。接続時に過去7日分を取り込み、その後は新しいものが届くたびに取り込みます。作成中のメモは、Granolaで完成してから取り込まれます。

メモはカレンダーにある該当の会議に追加されます。Granolaが示す会議、なければ同じ時間の会議です。Granolaのメモは「メモ」に、文字起こしは「文字起こし」に追加され、**Granolaから**と表示されます。自分で追加した内容はそのまま残ります。

会議後、The Machineはメモと文字起こしを読み、約束されたこと、決まったこと、まだ対応が必要なこと（「資料を送ります」など）を確認します。明確な次のステップだけをToDoにします。会議の参加者は、メールアドレスを使って[Graph](graph.md)にリンクされます。

## できること

Granola内では何も行いません。読み取り専用で、メモの変更、共有、削除はしません。

## 必要なもの

Granolaの個人用APIキーが必要です。GranolaのAPIキーはBusinessプランとEnterpriseプランで利用できます。このキーで読み取れるのは、自分のメモと、自分に共有されたメモです。Granolaで表示される内容と同じです。

## 接続する

1. Granolaのデスクトップアプリで、**Settings**、**Connectors**、**API keys**の順に開きます。Personal notesへのアクセス権を付けてキーを作成し、コピーします。
2. ダッシュボードで、**接続**、**会議**、Granolaの順に開きます。または、ホスティング版のMachineのセットアップページ（app.themachine.computer/setup）で、**その他のソース**、Granolaの順に開きます。自分のコンピューターでは、`assistant connect granola`でもキーの入力を求められます。
3. キーを貼り付け、**仕事**または**個人**を選んで、**接続**を押します。

キーはすぐに確認されます。後でGranolaがキーを受け付けなくなった場合は、**接続**にあるGranolaから新しいキーを求められます。

## 接続を解除する

- ダッシュボードで、**接続**を開き、Granolaの**詳細**から**接続を解除**を選びます。すでに取り込まれた内容は残ります。
- ホスティング版のMachineでは、セットアップページでGranolaの横にある**削除**を押して接続を解除することもできます。

## Granolaでキーを無効にする

Granolaのデスクトップアプリで、**Settings**、**Connectors**、**API keys**の順に開き、キーを削除します。
