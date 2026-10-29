---
title: Log da Machine
area: connections
summary: O log da sua própria Machine, para ela notar os próprios problemas. Ele só lê.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
---
## O que ele lê

O log do seu OpenClaw Gateway: execuções que falharam, repasses recusados, mensagens do Telegram que não saíram e os próprios erros da The Machine. Uma tarefa avisa quando algo precisa de conserto.

## O que ele pode fazer

Nada. Ele só lê o log na sua própria Machine.

## Conectar

- Em uma Machine hospedada, ele fica na sua página de configuração, em **Mais fontes**, como OpenClaw Gateway log. Um por Machine.
- No seu próprio computador: execute `assistant connect gateway`.

## Remover

- No painel: **Conexões**, abra o log, **Detalhes** e depois **Desconectar**.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

Não há nada para desinstalar em outro lugar.
