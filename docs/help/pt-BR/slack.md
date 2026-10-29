---
title: Slack
area: connections
summary: Os canais e as mensagens diretas de que você participa. Envia uma mensagem direta só depois que você aprova.
covers: connector:slack
code: assistant.py, slack_api.py, next_actions.py, onboarding.py
site: Sign in with Slack, Connect, More sources, Remove
---
## O que ele lê

As conversas de que você participa: canais, canais privados, mensagens diretas e mensagens em grupo, dos últimos 7 dias quando você conecta, e depois tudo o que for novo. Ele nunca entra em um canal nem abre uma conversa sozinho.

## O que ele pode enviar

Uma mensagem direta para uma pessoa, em seu nome, e só depois que você aprova na tarefa. Ele nunca publica em um canal.

## Conecte

Entre com o Slack, o jeito fácil:

1. No painel: **Conexões**, **+ Adicionar**, Slack. Ou na página de configuração de uma Machine hospedada em app.themachine.computer/setup: **Mais fontes**, Slack. No seu próprio computador, vincule-o à sua conta antes.
2. Clique em **Entrar com Slack**. O Slack pergunta qual workspace e mostra o que The Machine pode ler e enviar.
3. Clique em **Allow**. Você volta para onde estava, e o Slack está conectado.

Em alguns workspaces só admins aprovam apps novos. O Slack pede antes a um admin; depois que aprovar, entre de novo.

Ou use o Maton:

1. Entre em maton.ai, conecte o Slack lá e copie sua chave de API do Maton em Home.
2. Abra o Slack como acima (ou rode `assistant connect slack`), abra **Ou use uma chave de API do Maton**, cole a chave e clique em **Conectar**.

Já conectou o Slack pelo Maton? Continua funcionando. Conexões mostra **Reconectar Slack**: clique e entre com o Slack para parar de usar o Maton. O que o Slack já trouxe fica.

## Remova

- No painel: **Conexões**, abra o Slack, **Detalhes** e depois **Desconectar**. O que ele já trouxe continua lá.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Desinstale no Slack

- Com login do Slack: no Slack, abra a página Manage apps do seu workspace (ou Configurações, Apps), encontre The Machine e remova. Um admin do Slack também pode remover para todo o workspace.
- Pelo Maton: remova a conexão do Slack no Maton e apague a chave de API do Maton que você deu.
