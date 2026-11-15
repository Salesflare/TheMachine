---
title: 似たアドレスの送信者
area: security
summary: やり取りしたことのある相手に似せたアドレスからのメールは、関連するToDoで警告され、下書きの返信がそのアドレスに送られることはありません。
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## 検知するメール

知っているアドレスに似せたアドレスから詐欺メールが届くことがあります。たとえば、`example.com` や `example-billing.com` の代わりに `examp1e.com` を使ったり、1文字だけ変えたりするものです。The Machineは、各送信者のドメインを、これまでやり取りした相手のドメインと照合します。新しいドメインが既知のドメインに似せたものだけであれば、似たアドレスとして扱います。

末尾が異なるだけで、同じ名前を使っている場合は、たとえば `example.nl` と `example.com` のように、同じ組織のアドレスであり、似たアドレスではありません。gmail.comのようなフリーメールも対象外です。

## ToDoでの表示

このようなメールに関するToDoには、「これはAlexではありません。example.comではなく、examp1e.comから届いています」のように、はっきり表示されます。送信者はアドレスのみで表示され、画像や、なりすました相手へのリンクは表示されません。

## The Machineがしないこと

- 似たアドレスの送信者に、Graphで役割を与えることはありません。
- なりすました相手と統合したり、**同じ人ですか？** の候補として表示したりすることはありません。
- 返信の下書きは、記録されているアドレスに送られ、似たアドレスには送られません。

最終的な判断はいつでもご自身でできます。送信者に役割を与えたり、統合したり、任意のアドレスにメールを書いたりできます。
