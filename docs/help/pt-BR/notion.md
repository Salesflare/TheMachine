---
title: Notion
area: connections
summary: Comentários, menções e tarefas atribuídas a você no Notion. Respostas, novas páginas, edições e conclusão de tarefas aguardam sua aprovação.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 8544baf8c60cc40b
---
## O que ela lê

As páginas que sua conexão com o Notion pode acessar. Ela traz:

- Comentários nas suas páginas, respostas em discussões das quais você participa e comentários que mencionam você. Os que exigirem sua atenção viram tarefas.
- Itens de banco de dados atribuídos a você, com prazo e status. Cada um vira uma tarefa, e o prazo aparece no **Calendário**. Quando o item é concluído no Notion, a tarefa é encerrada automaticamente. **Desfazer** reabre a tarefa.
- Novas páginas que outras pessoas adicionarem e que você possa acessar.
- Um aviso discreto quando alguém altera uma página que você pediu para alterar. Ele nunca gera um alerta sonoro.

A primeira sincronização inclui os últimos 7 dias. As pessoas são associadas ao seu [Graph](graph.md) pelo endereço de e-mail. Quando o Notion não compartilha um endereço, a associação só é feita pelo nome completo, desde que exatamente uma pessoa no seu Graph tenha esse nome.

Para usar a integração apenas para executar ações, desative **Traz sinais** em **Detalhes**.

## O que ela pode fazer

Quando uma tarefa ou reunião precisar do texto de uma página, sua Machine lê essa página somente enquanto trabalha nela.

Cada uma destas ações aguarda sua aprovação na tarefa correspondente:

- Responder a um comentário na discussão correspondente.
- Criar uma nova página. Ela fica privada até você compartilhá-la.
- Editar uma página. Pressione **Revisar alterações** para ver cada parágrafo antes e depois e, em seguida, **Salvar**. As alterações são gravadas somente na página como você a viu. Se alguém tiver alterado a página nesse meio-tempo, nada será gravado e a tarefa informará isso.
- Marcar como concluída uma tarefa atribuída a você. Só o status dela muda.

Ela nunca exclui, compartilha ou move uma página.

## Conectar

1. No painel: **Conexões**, **Documentos e arquivos**, Notion. Ou, na página de configuração de uma Machine hospedada em app.themachine.computer/setup: **Mais fontes**, Notion. No seu próprio computador, primeiro conecte sua conta.
2. Pressione **Entrar com o Notion**, escolha seu espaço de trabalho e as páginas que ela pode acessar e autorize o acesso.
3. De volta à The Machine, ela verifica o login na hora e mostra o nome do espaço de trabalho.

Para conectar outro espaço de trabalho, adicione o Notion novamente.

## Colar um token

Em **Ou cole um token de integração**, pressione **Criar seu token**. O Notion abre a página de integrações: crie uma integração interna, permita a leitura e a inserção de conteúdo e comentários, além da leitura de informações de usuários com endereços de e-mail. Copie o token, cole-o e pressione **Conectar**.

Depois, compartilhe suas páginas com a integração no Notion, em **Conexões** em cada página. No seu próprio computador, `assistant connect notion` também solicita esse token.

## Remover a conexão

- No painel: **Conexões**, abra Notion, **Detalhes** e pressione **Desconectar**. O conteúdo que ela já trouxe continua disponível.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado dela na página de configuração.

## Revogar o acesso no Notion

No Notion: **Configurações**, **Conexões** e desconecte a The Machine. Se você colou um token, exclua a integração na página de integrações.
