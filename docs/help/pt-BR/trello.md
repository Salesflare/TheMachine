---
title: Trello
area: connections
summary: Mudanças em cartões, comentários e atividade em um quadro do Trello. Ela só lê.
covers: connector:trello
code: connectors/trello.py
site: Connect, More sources, Remove
---
## O que ela lê

Mudanças em cartões, comentários e atividade em um quadro do Trello por conexão. Ela nunca marca um quadro como visto.

## O que ela pode fazer

Nada no Trello. Ela só lê.

## Conecte

1. Em trello.com/power-ups/admin, crie um Power-Up com qualquer nome.
2. Abra a página da chave de API dele e copie a chave de API (não o secret).
3. Clique no link Token ao lado, permita o acesso de leitura e copie o token.
4. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, vá para **Mais fontes** e abra Trello. No seu próprio computador: **Conexões**, **+ Adicionar**, Trello, ou `assistant connect trello`.
5. Informe o endereço do quadro, a chave de API e o token, e depois clique em **Conectar**.

## Remova

- No painel: **Conexões**, abra o quadro, **Detalhes** e depois **Desconectar**. O que já foi trazido continua lá.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Revogue no Trello

Revogue o token nas configurações da sua conta do Trello, em Applications, ou exclua o Power-Up.
