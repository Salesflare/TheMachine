---
title: そっくりな差出人
area: security
summary: やり取りのある相手になりすましたアドレスからのメールには、ToDoで警告が表示され、下書きの宛先になることはありません。
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## 検出されるもの

知っているアドレスに似たアドレスから届く詐欺メールがあります。たとえば、`examp1e.com`が`example.com`や`example-billing.com`になっていたり、1文字だけ違っていたりする場合です。The Machineは、差出人のドメインを、これまでやり取りした相手のドメインと比較します。新しいドメインが既知のドメインに似ているだけの場合、そっくりな差出人と判定します。

`example.nl`と`example.com`のように、末尾だけが異なる同じ名前のドメインは、同じ組織のものであり、そっくりな差出人ではありません。gmail.comのようなフリーメールも該当しません。

## ToDoでの表示

このようなメールに関するToDoには、「これはAlexさんではありません。example.comではなく、examp1e.comから届きました」のように、はっきり表示されます。差出人は、写真やなりすましの相手へのリンクなしで、アドレスのみが表示されます。

## The Machineがしないこと

- そっくりな差出人に、Graphでの役割を割り当てることはありません。
- なりすましの相手と統合したり、**同じ人ですか？**の候補として表示したりすることはありません。
- 返信を作成する場合、そっくりな差出人ではなく、登録されているアドレス宛に送ります。

最終的にはいつでも自分で決められます。役割を割り当てたり、統合したり、どのアドレス宛にもメールを書いたりできます。
