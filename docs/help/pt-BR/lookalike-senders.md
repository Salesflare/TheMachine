---
title: Remetentes que se passam por alguém
area: security
summary: Mensagens de um endereço que imita alguém com quem você se comunica são sinalizadas na tarefa, e os rascunhos nunca são enviados para esse endereço.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 15a6a5dafcfa807b
---
## O que é identificado

Alguns golpes vêm de um endereço parecido com um que você conhece: `examp1e.com` no lugar de `example.com`, `example-billing.com`, com uma letra diferente ou duas letras trocadas. A Machine compara o domínio de cada remetente com os domínios com os quais você já se comunica.

Quando dois remetentes são parecidos, aquele com quem você já trocou mensagens, se encontrou ou cujo contato você mesmo configurou é o verdadeiro, mesmo que o outro tenha escrito primeiro. Se nenhum se destacar dessa forma, o mais recente é considerado o impostor.

O mesmo nome com outra terminação, como `example.nl` e `example.com`, indica a mesma organização, não um impostor. Endereços de e-mail gratuitos, como gmail.com, nunca são considerados impostores.

## Em uma tarefa

Uma tarefa sobre uma mensagem assim avisa claramente, por exemplo: "Este não é o Alex. A mensagem veio de examp1e.com, não de example.com." O remetente aparece como endereço simples, sem foto nem link para a pessoa que está imitando.

## O que a The Machine não fará

- Ela nunca atribui uma função a um remetente impostor no seu Graph, nem define o domínio dele como organização de um projeto.
- Ela nunca o mescla com a pessoa que ele imita, nem mesmo quando escreve na mesma conversa com o mesmo nome, e nunca o sugere em **Mesma pessoa?**.
- Uma resposta preparada por ela vai para o endereço registrado, não para o endereço do impostor.

Sua decisão sempre prevalece: você ainda pode atribuir uma função a esse remetente, mesclá-lo com outra pessoa ou escrever para qualquer endereço.
