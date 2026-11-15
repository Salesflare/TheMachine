---
title: Remetentes que imitam alguém
area: security
summary: E-mails de um endereço que imita alguém com quem você se relaciona são sinalizados na tarefa correspondente, e os rascunhos nunca são direcionados a esse endereço.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## O que é detectado

Alguns golpes vêm de um endereço parecido com um que você conhece: `examp1e.com` para `example.com`, `example-billing.com` ou com uma letra trocada. The Machine compara o domínio de cada remetente com os domínios com os quais você já se relaciona. Quando o domínio mais recente apenas se parece com um conhecido, ele é considerado um sósia.

O mesmo nome com outro sufixo, como `example.nl` ao lado de `example.com`, é a mesma organização, não um sósia. Serviços de e-mail gratuitos, como gmail.com, nunca são considerados.

## Em uma tarefa

Uma tarefa sobre esse tipo de mensagem deixa isso claro, por exemplo: "Este não é o Alex. A mensagem veio de examp1e.com, não de example.com." O remetente aparece apenas com o endereço, sem foto nem link para a pessoa que está imitando.

## O que The Machine não fará

- Nunca atribui a um remetente sósia uma função na sua Graph.
- Nunca o mescla com a pessoa que ele está imitando nem o sugere em **Mesma pessoa?**.
- Uma resposta que ela prepara é direcionada ao endereço registrado, não ao endereço do sósia.

Sua decisão sempre prevalece: você ainda pode atribuir uma função a esses remetentes, mesclá-los ou escrever para qualquer endereço.
