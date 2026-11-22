---
title: GitHub
area: connections
summary: Confira solicitações de revisão, menções, atribuições e execuções de CI com falha. Só cria issues quando você confirma.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## O que ele lê

Suas notificações do GitHub: solicitações de revisão, menções, atribuições, respostas e execuções de CI com falha. Ele nunca as marca como lidas.

## O que ele pode fazer

A leitura não altera nada no GitHub. Quando uma tarefa termina com uma etapa do GitHub, como abrir uma issue, a tarefa avisa, e a etapa só é executada depois que você toca em **Confirmar** ou quando você pede exatamente isso no chat dela. As capturas de tela são enviadas pelo navegador da sua Machine. Se o GitHub não estiver conectado, a tarefa avisa que vai usar o navegador e mostra **Conectar o GitHub**.

## Conectar

Em uma Machine hospedada:

1. Abra **Conexões**, depois **Projetos e código**, e selecione GitHub.
2. Escolha **Trabalho** ou **Pessoal** e toque em **Entrar com o GitHub**.
3. Toque em **Abrir GitHub ↗**, digite o código exibido e autorize o acesso. A conexão será feita automaticamente.

A página de configuração em app.themachine.computer/setup tem a mesma opção de login em **Mais fontes**.

No seu computador:

1. Abra **Conexões**, depois **Projetos e código**, e selecione GitHub.
2. Escolha **Trabalho** e a empresa correspondente, ou **Pessoal**, e toque em **Conectar**.
3. Se solicitado, toque em **Abrir GitHub ↗**, digite o código e autorize o acesso. A conexão será feita automaticamente.

Ou execute `assistant connect github` e confirme seu login do GitHub.

## Remover

- Abra **Conexões**, selecione GitHub, **Detalhes** e **Desconectar**. A leitura será interrompida. O que já foi importado continuará disponível.
- Em uma Machine hospedada, você também pode tocar em **Remover** ao lado do GitHub na página de configuração.

## Desinstalar no GitHub

No GitHub, abra Configurações, Aplicativos, Aplicativos OAuth autorizados e revogue o GitHub CLI. No seu computador, `gh auth logout` também encerra a sessão.
