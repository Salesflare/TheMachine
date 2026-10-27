---
title: Stripe
area: connections
summary: Pagamentos que falharam, disputas, cancelamentos e grandes assinaturas novas. Ele só lê.
covers: connector:stripe
code: connectors/stripe.py
site: Connect, More sources, Remove
---
## O que ele lê

Eventos na sua conta do Stripe que podem precisar de você: pagamentos que falharam, disputas, cancelamentos e grandes assinaturas novas, com o cliente a que pertencem.

## O que ele pode fazer

Nada no Stripe. Ele nunca escreve, reembolsa ou tenta de novo um pagamento.

## Conectar

1. No Stripe, crie uma chave restrita com Read em Events, Customers e Account, e None em todo o resto.
2. Encontre o ID da sua conta (acct_...) em Settings, Business details.
3. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, vá em **Mais fontes** e abra Stripe. No seu próprio computador: **Conexões**, **+ Adicionar**, Stripe, ou `assistant connect stripe`.
4. Cole o ID da conta e a chave, depois clique em **Conectar**.

## Remover

- No painel: **Conexões**, abra Stripe, **Detalhes** e depois **Desconectar**. O que ele já trouxe continua.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Revogar no Stripe

No Stripe, abra Developers, API keys, e exclua ou troque a chave restrita.
