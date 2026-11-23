---
title: X
area: connections
summary: Suas menções, respostas e mensagens diretas no X, lidas no próprio navegador da sua Machine. Só envia depois da sua aprovação.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: e8997ab6eb32523f
---
## O que ela lê

Suas menções, respostas e mensagens diretas no X, no próprio navegador da sua Machine, com sua conta conectada. Ela não marca nada como lido e não consegue ler o X Chat criptografado.

## O que ela pode enviar

Uma resposta ou mensagem direta, e somente depois da sua aprovação na tarefa.

O X está migrando contas para um novo app web. Se sua conta já tiver migrado, ainda não será possível enviar respostas pela sua Machine. Nesse caso, uma resposta que você aprovar será interrompida antes de ser publicada, e você verá um aviso. As mensagens diretas ainda são enviadas.

Isso não passa pela API oficial do X. É muito improvável que a leitura e o envio ocasional de uma resposta aprovada por você causem problemas. O envio em massa ou automatizado pode levar ao bloqueio da conta.

## Conectar

Em uma Machine hospedada:

1. Acesse sua página de configuração em app.themachine.computer/setup e vá para **Mais fontes**.
2. Abra o X, digite seu nome de usuário sem o @, entre no X pelo navegador da sua Machine quando solicitado e pressione **Conectar**.

No seu próprio computador:

1. No painel, abra **Conexões**, depois **Chat** e escolha X.
2. Escolha **Trabalho** com a empresa correspondente ou **Pessoal**, digite seu nome de usuário sem o @ e pressione **Conectar**.
3. Pressione **Entrar no X** e entre pelo navegador da sua Machine. A conexão acontece automaticamente quando você entra.

Ou execute `assistant connect x` em um terminal.

Se o X desconectar sua Machine, consulte [Um site desconectou sua Machine](signed-out.md).

## Remover

- No painel: abra **Conexões**, escolha X, toque em **Detalhes** e depois em **Desconectar**. A leitura será interrompida. O conteúdo que ela já trouxe continuará disponível.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado do X na página de configuração.

## Encerrar a sessão no X

No X, abra Configurações, Segurança e acesso à conta, Aplicativos e sessões, Sessões e encerre a sessão do navegador da sua Machine.
