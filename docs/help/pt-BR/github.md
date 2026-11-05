---
title: GitHub
area: connections
summary: Pedidos de revisão, menções, atribuições e execuções de CI que falharam. Ele só lê.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## O que ele lê

Suas notificações do GitHub: pedidos de revisão, menções, atribuições, respostas e execuções de CI que falharam. Ele nunca marca uma notificação como lida.

## O que ele pode fazer

Ler não muda nada no GitHub. Quando uma tarefa termina em um passo no GitHub, como abrir uma issue, esse passo roda com o mesmo login do gh assim que você toca em **Confirmar**, e a tarefa avisa antes. As capturas de tela ainda entram pelo navegador da sua Machine, porque a ferramenta do GitHub não adiciona imagens. Sem o GitHub conectado, a tarefa diz que vai usar o navegador, com **Conectar o GitHub**.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup e vá em **Mais fontes**.
2. Abra GitHub e clique em **Entrar com GitHub**.
3. Digite no GitHub o código que aparece, no celular ou no computador.

No seu próprio computador:

1. Primeiro, entre na CLI do GitHub: `gh auth login`.
2. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha GitHub. Ou execute `assistant connect github`.
3. Confirme seu login do GitHub. A The Machine verifica se ele confere a cada sincronização.

## Remover

- No painel: **Conexões**, abra GitHub, **Detalhes** e depois **Desconectar**. Ele para de ler. O que ele já trouxe continua.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Desinstalar no GitHub

Revogue o acesso da CLI do GitHub no GitHub, em Settings, Applications, Authorized OAuth Apps. No seu próprio computador, `gh auth logout` também desconecta a CLI.
