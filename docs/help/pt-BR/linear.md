---
title: Linear
area: connections
summary: Suas issues do Linear, menções, comentários, solicitações de revisão e prazos. Comentários, mudanças de status e de responsável e novas issues aguardam sua aprovação.
covers: connector:linear
code: connectors/linear.py, linear_writes.py
site: Sign in with Linear, Connect, More sources, Remove
translated: 1e16b6abdf4fefad
---
## O que ela lê

Sua caixa de entrada do Linear e as issues atribuídas a você. Ela traz:

- Issues atribuídas a você: novas issues e aquelas cujo status, prazo ou título mudou. Quando uma issue é concluída ou cancelada no Linear, a tarefa correspondente é fechada automaticamente. **Desfazer** reabre a tarefa.
- Menções a você, além de comentários e respostas em issues que você acompanha.
- Solicitações de revisão e issues adicionadas à triagem.
- Lembretes de prazo.

Cada item vira uma tarefa apenas quando precisa da sua atenção, com base no conteúdo. Suas próprias alterações nunca aparecem. A primeira sincronização considera os últimos 7 dias. As pessoas são vinculadas ao seu [Graph](graph.md) pelo endereço de e-mail que o Linear mostra para elas.

Para usar a integração apenas para ações, desative **Traz sinais** em **Detalhes**.

## O que ela pode fazer

Cada uma destas ações aguarda sua aprovação na tarefa correspondente:

- Comentar em uma issue relacionada à tarefa ou responder em uma conversa de comentários. O comentário será publicado em seu nome.
- Alterar o status da issue para um dos status da equipe.
- Atribuir a issue a alguém da equipe ou a você.
- Criar uma issue em uma das suas equipes.

Ela nunca exclui, arquiva ou move uma issue para outra equipe.

## Conectar

1. No painel: **Conexões**, **+ Adicionar**, Linear. Ou, na página de configuração de uma Machine hospedada em app.themachine.computer/setup: **Mais fontes**, Linear. No seu próprio computador, primeiro conecte sua conta à Machine.
2. Pressione **Entrar com o Linear**, escolha seu espaço de trabalho e autorize o acesso.
3. De volta à The Machine, a conexão é verificada na hora e o nome do espaço de trabalho é exibido.

Para adicionar outro espaço de trabalho, adicione o Linear novamente. Escolha **Trabalho** ou **Pessoal**, como em qualquer conexão.

## Colar uma chave de API

Em **Ou cole uma chave de API**, pressione **Criar seu token**. O Linear abre **Configurações**, **Segurança e acesso**. Crie uma chave de API pessoal, copie e cole a chave e pressione **Conectar**. No seu próprio computador, `assistant connect linear` também pede a chave.

## Remover

- No painel: **Conexões**, abra o Linear e selecione **Detalhes** e **Desconectar**. O que já foi trazido continua disponível.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado do Linear na página de configuração.

## Revogar o acesso no Linear

No Linear: **Configurações**, **Segurança e acesso** e revogue o acesso da The Machine em aplicativos autorizados. Se você colou uma chave, revogue-a na mesma página.
