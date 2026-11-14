---
title: X
area: connections
summary: Suas menções, respostas e mensagens diretas no X, lidas no navegador da sua Machine. Ela só envia depois da sua aprovação.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## O que ela lê

Suas menções, respostas e mensagens diretas no X, no navegador da sua Machine, com a sessão iniciada como você. Ela não marca nada como lido e não consegue ler as conversas criptografadas do X Chat.

## O que ela pode enviar

Uma resposta ou mensagem direta, e somente depois que você aprovar na tarefa.

Isso não passa pela API oficial do X. Ler e enviar ocasionalmente uma resposta que você aprovou dificilmente vai causar problemas. O envio em massa ou automatizado pode levar ao bloqueio de uma conta.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup e acesse **Mais fontes**.
2. Abra o X, digite seu nome de usuário sem o @ e entre no X no navegador da sua Machine quando solicitado. Depois, pressione **Conectar**.

No seu próprio computador:

1. No painel, abra **Conexões**, depois **Chat**, e escolha X.
2. Escolha **Trabalho** e a empresa correspondente, ou **Pessoal**. Digite seu nome de usuário sem o @ e pressione **Conectar**.
3. Pressione **Entrar no X** e entre no X no navegador da sua Machine. A conexão acontece automaticamente assim que você entra.

Ou execute `assistant connect x` em um terminal.

Se o X desconectar sua Machine, consulte [Saiu de um site](signed-out.md).

## Remover

- No painel: abra **Conexões**, escolha X e acesse **Detalhes**. Depois, pressione **Desconectar**. Ela para de ler, mas o que já importou permanece.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado dela na página de configuração.

## Encerrar a sessão da sua Machine no X

No X, abra Configurações, Segurança e acesso à conta, Aplicativos e sessões e Sessões. Depois, encerre a sessão do navegador da sua Machine.
