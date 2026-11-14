---
title: Remetentes que imitam outras pessoas
area: security
summary: E-mails de um endereço que imita alguém com quem você se relaciona são sinalizados na tarefa, e os rascunhos nunca são endereçados a esse endereço.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## O que isso identifica

Alguns golpes vêm de um endereço que se parece com um que você conhece: `examp1e.com` para `example.com`, `example-billing.com` ou com uma letra diferente. A Machine compara o domínio de cada remetente com os domínios com que você já se relaciona. Quando o domínio mais recente apenas se parece com um domínio conhecido, ele é considerado semelhante.

O mesmo nome com outra terminação, como `example.nl` ao lado de `example.com`, é a mesma organização, não um caso de imitação. Endereços de e-mail gratuitos, como gmail.com, nunca são considerados semelhantes.

## Em uma tarefa

Uma tarefa sobre uma mensagem desse tipo deixa isso claro, por exemplo: "Este não é o Alex. A mensagem veio de examp1e.com, não de example.com." O remetente aparece como endereço puro, sem foto nem link para a pessoa que está sendo imitada.

## O que The Machine não fará

- Ela nunca atribui a um remetente semelhante um papel no seu Graph.
- Ela nunca mescla esse remetente com a pessoa que está sendo imitada nem o sugere em **Mesma pessoa?**.
- Uma resposta que ela prepara fica endereçada ao endereço registrado, não ao endereço semelhante.

Sua decisão sempre prevalece: você ainda pode atribuir um papel a essas pessoas, mesclá-las ou escrever para qualquer endereço.
