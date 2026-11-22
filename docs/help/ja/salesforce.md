---
title: Salesforce
area: connections
summary: Salesforceの商談、タスク、アクティビティを人物やプロジェクトに表示します。有効にすると、Salesforceの連絡先情報を最新の状態に保てます。
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## 読み取る情報

新しい商談、ステージが変わった商談、金額が変わった商談。未完了のタスク、通話、メモ付きで完了として記録されたその他のタスク、説明付きの会議。接続時に過去7日分を読み取り、その後は15分ごとに新しい情報を読み取ります。

商談はそれぞれGraphのプロジェクトになり、商談に関連付けられた連絡先は、Salesforceアカウントの連絡先として人物ページに表示されます。

## 変更できる情報

**連絡先情報を更新**を有効にするまで、何も変更しません。Salesforceへのログイン情報はMachine上に保存されます。

## 接続する

ホスティング版Machineの場合：

1. app.themachine.computer/setupでセットアップページを開き、**その他のソース**に移動します。
2. Salesforceを開き、**Salesforceに接続**を押します。
3. Salesforceにログインし、Salesflare製のThe Machineを許可します。

または、ダッシュボードで**接続**、**顧客**の順に開き、Salesforceを選んで**Salesforceでログイン**を押します。自分のコンピューターで使う場合は、先にアカウントとペアリングしてください。

SalesforceのユーザーにはAPIアクセス権が必要です。ほとんどのエディションに含まれています。

## 連絡先情報を更新する

Salesforceの連絡先について、Machineがより新しい情報を把握している場合、連絡先の役職、電話番号、LinkedInのリンクをSalesforceで更新できます。LinkedInのリンクを更新するには、Salesforce組織の連絡先にLinkedIn項目が必要です。

1. **接続**でSalesforceを開き、**変更内容を確認**を押します。
2. 一覧を確認して、**オンにする**または**今はしない**を押します。

更新の条件：

- 本人のLinkedInやSlackのプロフィールに書かれた情報、または人物ページで設定した情報だけを使います。推測はしません。
- Salesforceで連絡先が最後に変更された日時より、新しい情報だけを使います。Salesforceで編集された情報が優先されます。
- 値が異なる項目だけを更新し、空欄にはしません。メールアドレスやアカウントは変更しません。
- 変更内容は、人物ページに日付付きで記録されます。

停止するには**オフにする**を押します。Fleetで共有されている接続では、読み取りのみを行います。

## 接続を解除する

- ダッシュボードで**接続**を開き、Salesforce、**詳細**、**接続を解除**の順に選びます。すでに取り込まれた情報は残ります。
- ホスティング版Machineでは、**接続を解除 ↗**を押すとセットアップページが開きます。Salesforceの横にある**削除**を押します。

## Salesforceでアクセスを取り消す

Salesforceで個人設定を開き、Connected Apps OAuth Usageに移動してThe Machineのアクセスを取り消します。管理者に依頼することもできます。取り消すと、The Machineは情報を読み取ったり変更したりできなくなります。
