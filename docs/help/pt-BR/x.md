---
title: X
area: connections
summary: Suas menções, respostas e mensagens diretas no X, lidas no próprio navegador da sua Machine. Só envia depois que você aprova.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
---
## O que ele lê

Suas menções, respostas e mensagens diretas no X. Ele lê tudo no próprio navegador da sua Machine, conectado como você. Ele não usa a API de desenvolvedor do X, não marca nada como visto e não consegue ler o X Chat criptografado.

## O que ele pode enviar

Uma resposta ou uma mensagem direta, e só depois que você aprova na tarefa.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup e vá em **Mais fontes**.
2. Abra X, digite seu nome de usuário sem o @, entre no X no navegador da sua Machine quando ela pedir, e depois clique em **Conectar**.

No seu próprio computador:

1. Entre no X uma vez no navegador da sua Machine (Configurações, **Abrir o navegador da Machine ↗**).
2. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha X. Ou execute `assistant connect x`.
3. Digite seu nome de usuário e o nome de usuário com que o navegador costuma estar conectado.

Se o X desconectar sua Machine, veja [Desconectado de um site](signed-out.md).

## Remover

- No painel: **Conexões**, abra X, **Detalhes** e depois **Desconectar**. Ele para de ler. O que ele já trouxe continua.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Sair no X

No X, abra Settings, Security and account access, Apps and sessions, Sessions, e encerre a sessão do navegador da sua Machine.
