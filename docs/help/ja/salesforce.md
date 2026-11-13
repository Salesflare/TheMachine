---
title: Salesforce
area: connections
summary: Salesforceの商談、ToDo、人物やプロジェクトに関するアクティビティを確認できます。有効にすると、連絡先の詳細を最新の状態に保てます。
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
---
## 読み取る情報

新しい商談、ステージや金額が変更された商談。未完了のToDo、通話、メモ付きで完了として記録されたほかのToDo、説明付きのミーティングです。接続時に過去7日分を読み取り、その後は15分ごとに新しい情報を確認します。

各商談はGraph内のプロジェクトになり、商談に関連付けられた連絡先は、それぞれの人物ページにアカウントのSalesforce連絡先として表示されます。

## 変更できる情報

**連絡先の詳細を更新**を有効にするまでは、何も変更しません。Salesforceのサインイン情報はMachineに保存されます。

## 接続する

ホスト型のMachineの場合：

1. app.themachine.computer/setupでセットアップページを開き、**その他のソース**に移動します。
2. Salesforceを開き、**Salesforceに接続**を押します。
3. Salesforceにサインインし、The Machine（Salesflare製）へのアクセスを許可します。

または、ダッシュボードで**接続**、**顧客**の順に選び、Salesforceを選択して**Salesforceでサインイン**を押します。

SalesforceユーザーにはAPIアクセス権が必要です。ほとんどのエディションに含まれています。

## 連絡先の詳細を更新する

MachineがSalesforceの連絡先について、より新しい情報を把握している場合、連絡先の役職、電話番号、LinkedInリンクを更新できます。LinkedInリンクの更新には、組織の連絡先にLinkedIn項目が必要です。

1. **接続**でSalesforceを開き、**変更内容を確認**を押します。
2. 一覧を確認し、**有効にする**または**今はしない**を押します。

更新の条件：

- LinkedInやSlackのプロフィール、または人物ページに設定した情報など、本人の言葉で確認できる情報だけを使います。推測はしません。
- Salesforceで連絡先が最後に変更された日時より新しい情報だけを使います。Salesforceでの編集が優先されます。
- 変更が必要な項目だけを更新し、空欄で上書きすることはありません。メールアドレスやアカウントは変更しません。
- 変更内容は、日付付きで人物ページに記録されます。

停止するには、**無効にする**を押します。Fleetで共有されている接続は読み取り専用です。

## 削除する

- ダッシュボードで**接続**を開き、Salesforceの**詳細**から**接続を解除**します。すでに取り込まれた情報は残ります。
- ホスト型のMachineでは、セットアップページでSalesforceの横にある**削除**を押すこともできます。

## Salesforceでアクセスを取り消す

Salesforceで個人設定を開き、Connected Apps OAuth Usageに移動します。または管理者に依頼して、The Machineへのアクセスを取り消します。以後、情報の読み取りや変更はできなくなります。
