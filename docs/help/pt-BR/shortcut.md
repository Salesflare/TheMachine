---
title: Shortcut
area: connections
summary: Histórias que mudam de estado, com responsáveis e prazos. Ela só lê.
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
translated: 68419e11fabc157c
---
## O que ela lê

Histórias no seu espaço de trabalho do Shortcut que mudam de estado, com responsáveis e prazos.

## O que ela pode fazer

Nada no Shortcut. Ela só lê.

## Conectar

1. No painel: **Conexões**, **Projetos e código**, Shortcut. Ou, na página de configuração de uma Machine hospedada, em app.themachine.computer/setup: **Mais fontes**, Shortcut. No seu computador, primeiro pareie a Machine com a sua conta.
2. Pressione **Entrar com o Shortcut** e permita o acesso de leitura. Ela pede ao Shortcut somente acesso de leitura.
3. Ao voltar para a The Machine, ela verifica o login na hora e mostra com qual conta se conectou e em qual espaço de trabalho.

Tem mais de um espaço de trabalho no Shortcut? Primeiro, mude para o espaço desejado no Shortcut. Para outro espaço de trabalho, adicione o Shortcut novamente.

## Cole um token

Em **Ou cole um token de API**, pressione **Criar seu token**. O Shortcut abre a página API Tokens em uma nova guia: crie um token, copie, cole e pressione **Conectar**. No seu computador, `assistant connect shortcut` também solicita o token. Ele dá acesso total à sua conta, mas The Machine só o usa para leitura.

## Remover

- No painel: **Conexões**, abra Shortcut, **Detalhes** e depois **Desconectar**. O que ela já importou continua lá.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado dela na página de configuração.

## Revogar no Shortcut

Se você colou um token, exclua-o na página API Tokens. Se você fez login, desconectar aqui interrompe toda a leitura.
