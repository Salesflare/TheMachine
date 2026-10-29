---
title: Intercom
area: connections
summary: Conversas com clientes no seu workspace do Intercom. Ele só responde depois que você envia, em seu nome.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
---
## O que ele lê

Conversas com clientes no seu workspace do Intercom: os últimos 7 dias quando você conecta, depois as novas conforme chegam. Ele também lê a qual workspace e a qual admin o login pertence.

## O que ele pode fazer

Ele lê conversas. Com o seu próprio **Entrar com o Intercom**, ele também pode responder em uma conversa em seu nome, só depois que você toca em **Enviar** naquele texto exato. Ele nunca atribui, fecha, marca ou escreve notas. Um Intercom compartilhado com você pelo seu Fleet só lê.

## Tarefas do Intercom

Uma tarefa de uma conversa do Intercom mostra de onde veio: **Ler mensagem** abre a conversa, com um link para ela no Intercom, e o cliente aparece na tarefa. A resposta é uma resposta do Intercom nessa conversa, a menos que você peça um e-mail.

Quando o Intercom não consegue responder pela sua Machine (compartilhado com você só para leitura, respostas não ativadas ou não conectado), o rascunho vai por e-mail. A tarefa diz por quê, e a revisão pergunta **Enviar por e-mail em vez disso?** Para responder você mesmo no Intercom, toque em **Conecte seu próprio Intercom** na tarefa e entre. Nada sai antes de você enviar.

## Conectar

1. No painel: **Conexões**, **+ Adicionar**, Intercom. Ou na página de configuração de uma Machine hospedada, em app.themachine.computer/setup: **Mais fontes**, Intercom. No seu próprio computador, pareie-o primeiro com sua conta.
2. Clique em **Entrar com o Intercom**.
3. Aprove a The Machine no Intercom. Ela é feita pela Salesflare. Quando terminar, você volta para onde começou.

Entrar em outro workspace adiciona uma segunda conta do Intercom.

O Intercom sempre conta como trabalho, para a empresa que o workspace indica.

## Remover

- No painel: **Conexões**, abra Intercom, **Detalhes** e depois **Desconectar**. Ele para de ler. O que já foi trazido fica.
- Em uma Machine hospedada, você também pode tocar em **Remover** ao lado dele na sua página de configuração.

## Desinstalar no Intercom

No Intercom, abra Settings, Apps, Installed apps, e remova a The Machine.
