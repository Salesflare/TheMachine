---
title: Notion
area: connections
summary: Comentários, menções e tarefas atribuídas a você no Notion. Respostas, novas páginas, edições e conclusão de tarefas aguardam sua aprovação.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 2e93c261cc09e401
---
## O que ela lê

As páginas às quais sua conexão com o Notion tem acesso. Ela traz:

- Comentários nas suas páginas, respostas em discussões das quais você participa e comentários que mencionam você. Os que precisam da sua atenção viram tarefas.
- Itens de banco de dados atribuídos a você, com prazo e status. Cada um vira uma tarefa, e o prazo aparece no **Calendário**. Quando o item é concluído no Notion, a tarefa é encerrada automaticamente. **Desfazer** reabre a tarefa.
- Novas páginas que outras pessoas adicionam e que você pode ver.
- Um aviso discreto quando alguém altera uma página que você pediu para ser alterada. Ele nunca toca.

A primeira sincronização inclui os últimos 7 dias. As pessoas são associadas à sua [Graph](graph.md) pelo endereço de e-mail. Quando o Notion não informa um endereço, a associação é feita pelo nome completo somente se exatamente uma pessoa na sua Graph tiver esse nome.

Para usar a integração apenas para realizar ações, desative **Traz sinais** em **Detalhes**.

## O que ela pode fazer

Quando uma tarefa ou reunião precisa do texto de uma página, sua Machine lê essa página, somente enquanto trabalha nela. De um arquivo nessa página, ela vê apenas o nome. Ela encontra páginas pelo título, não pelos arquivos nelas.

Cada uma destas ações aguarda sua aprovação na tarefa correspondente:

- Responder a um comentário na discussão correspondente.
- Criar uma nova página. Ela fica privada até você compartilhá-la.
- Editar uma página. Pressione **Revisar alterações** para ver cada parágrafo antes e depois e, em seguida, **Salvar**. Ela só escreve na página como você a viu. Se alguém a alterar nesse meio-tempo, nada será escrito e a tarefa avisará você.
- Marcar como concluída uma tarefa atribuída a você. Somente o status muda.

Ela nunca exclui, compartilha ou move uma página.

## Conectar

1. No painel: **Conexões**, **Documentos e arquivos**, Notion. Ou, na página de configuração de uma Machine hospedada em app.themachine.computer/setup: **Mais fontes**, Notion. No seu próprio computador, primeiro pareie sua conta.
2. Pressione **Entrar com Notion**, escolha seu espaço de trabalho e as páginas às quais ela pode ter acesso e autorize o acesso.
3. De volta à The Machine, ela verifica o login na hora e mostra o nome do espaço de trabalho.

Para conectar outro espaço de trabalho, adicione o Notion novamente.

## Colar um token

Em **Ou cole um token de integração**, pressione **Criar seu token**. O Notion abre a página de integrações: crie uma integração interna, permita que ela leia e insira conteúdo e comentários, e leia informações de usuário com endereços de e-mail. Copie o token, cole-o e pressione **Conectar**.

Depois, compartilhe suas páginas com ela no Notion, em **Conexões** em cada página. No seu próprio computador, `assistant connect notion` também solicita o token.

## Remover a integração

- No painel: **Conexões**, abra o Notion, selecione **Detalhes** e pressione **Desconectar**. O conteúdo que ela já trouxe permanece.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado da integração na página de configuração.

## Revogar o acesso no Notion

No Notion: **Configurações**, **Conexões** e desconecte a conexão com a The Machine. Se você colou um token, exclua a integração na página de integrações.
