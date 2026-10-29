---
title: LinkedIn
area: connections
summary: Suas mensagens do LinkedIn, lidas no navegador da sua Machine, já com login feito. Ela só responde depois que você aprova.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py
site: Connect, More sources, Remove
---
## O que ela lê

Suas mensagens do LinkedIn. Ela lê em uma aba do navegador da sua Machine, com login feito como você, de vez em quando durante o dia. Ela não usa chave de API e não marca nada como lido.

## O que ela pode enviar

Uma resposta a uma mensagem, e só depois que você aprovar na tarefa. Até lá, ela só escreve o rascunho.

## Conecte

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup e vá para **Mais fontes**.
2. Abra LinkedIn, entre no LinkedIn no navegador da sua Machine quando ela pedir e depois clique em **Conectar**.

No seu próprio computador:

1. Entre no LinkedIn uma vez no navegador da sua Machine (Configurações, **Abrir o navegador da Machine ↗**).
2. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha LinkedIn. Ou rode `assistant connect linkedin`.

Uma segunda conta do LinkedIn ganha um navegador próprio. Se o LinkedIn desconectar sua Machine, veja [Desconectado de um site](signed-out.md).

## Se o LinkedIn pedir um código

Na primeira vez que sua Machine entra, o LinkedIn costuma enviar um código por e-mail. Digite-o na janela de login, em **Código**, e toque em **Entrar**. A página fica parada enquanto você digita.

Se o LinkedIn voltar ao início, ou nada acontecer por dois minutos, ele interrompeu este login. Espere um minuto e toque em **Tentar de novo**. Se o LinkedIn mostrar uma verificação de robô, conclua-a no navegador da sua Machine.

## Remova

- No painel: **Conexões**, abra LinkedIn, **Detalhes** e depois **Desconectar**. Ela para de ler. O que já foi trazido continua lá.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Saia no LinkedIn

No LinkedIn, abra Configurações, Login e segurança, Onde você está conectado, e encerre a sessão do navegador da sua Machine.
