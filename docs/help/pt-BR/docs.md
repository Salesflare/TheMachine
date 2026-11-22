---
title: Microsoft OneDrive
area: connections
summary: Comentários, menções, alterações controladas e compartilhamentos nos seus arquivos do Word no OneDrive e no SharePoint. Novos documentos e alterações aguardam seu OK.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: b06d8ca4f35e5a38
---
## O que ela lê

**Microsoft OneDrive** lê seus arquivos do Word no OneDrive e no SharePoint, em uma Machine hospedada ou no seu próprio computador. Não é necessário conectar o Outlook. Para saber mais sobre o Google Docs, veja abaixo. Ela traz:

- Documentos que alguém compartilha com você.
- Comentários e respostas nos seus documentos, além de comentários que mencionam você.
- Alterações controladas nos seus arquivos do Word.

A primeira sincronização busca os últimos 7 dias. Cada item leva às pessoas e aos projetos no seu [Graph](graph.md). Um comentário que precisa de você vira uma tarefa.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê esse documento enquanto trabalha na tarefa.

Ela pode criar um rascunho de resposta a um comentário. Como o Word não permite responder de fora, você precisa copiar o rascunho para o Word.

Ela nunca aceita uma sugestão, resolve um comentário, compartilha um arquivo ou altera um documento sem seu OK.

Para usar a integração apenas para executar ações, desative **Traz sinais** em **Detalhes**. Assim, ela só encontra e lê os documentos necessários para suas tarefas e cria novos documentos.

## Criar e editar documentos

Sua Machine pode criar um documento ou alterar um documento relacionado a uma tarefa:

- Ela cria um documento novo na hora, quando uma tarefa ou habilidade solicita. Ele é privado e fica no seu OneDrive ou Google Drive. A tarefa mostra **Abrir o documento**. Compartilhar o documento ou enviar o link dele aguarda seu OK.
- Uma alteração em um documento existente é apenas preparada. Pressione **Revisar alterações** para ver cada parágrafo antes e depois e, em seguida, **Salvar**. Uma alteração solicitada no chat da tarefa é feita na hora.
- Ela só escreve no documento da forma como você o viu. Se alguém o tiver alterado nesse meio-tempo, nada será escrito e a tarefa avisará. Peça um novo rascunho.
- No Talk, ela lê a alteração inteira em voz alta e aguarda uma confirmação clara.
- Se a Microsoft ou o Google não permitir criar um documento, a tarefa explica o motivo e mostra **Revisar e criar** para tentar novamente.

Ela pode substituir e adicionar texto, parágrafos e títulos. Tabelas, imagens, alterações controladas e campos permanecem como estão.

O documento de uma tarefa de Trabalho fica na conta da empresa, nunca em uma conta pessoal. No seu próprio computador, uma conta Google conectada ao Gmail e com acesso ao Drive também pode criar novos documentos do Google. Se nenhuma conta for adequada, a tarefa informa o que você precisa conectar para Trabalho: Microsoft OneDrive ou Google Docs, quando sua Machine puder usá-lo.

Quando o documento não for a última etapa, como no caso de uma resposta com o link dele, a tarefa permanece aberta e prepara essa etapa para você aprovar.

A edição é ativada ao conectar. Uma conexão antiga que só permite leitura mostra **Permitir edições** em **Conexões**. Pressione essa opção uma vez e aceite.

## O que ela solicita

A Microsoft pede um único OK para ler e alterar seus arquivos, inclusive os compartilhados com você. Cada alteração ainda aguarda seu OK na tarefa. O acesso ao seu e-mail e calendário não muda.

Se você revogar essa autorização, Microsoft OneDrive mostrará **Aguardando seu OK para ler documentos** em **Conexões**.

## Conectar

Em uma Machine hospedada ou no seu próprio computador pareado com sua conta:

- Abra **Conexões**, depois **Documentos e arquivos**, e escolha **Microsoft OneDrive**.
- Pressione **Entrar com a Microsoft** e permita que ela leia e edite seus arquivos.

Se a Microsoft não permitir a leitura, a conexão não será adicionada. Se você pressionar **Permitir edições** e a Microsoft não permitir a edição, ela avisará.

## Google Docs

Em uma Machine hospedada, abra **Conexões**, depois **Documentos e arquivos**, e escolha **Google Docs**. O Google pedirá sua autorização para ver e editar os documentos que você indicar e criar novos. Não é necessário conectar o Gmail, e o acesso ao Gmail não muda.

Depois disso, sua Machine:

- Lê um documento do Google vinculado às mensagens de uma tarefa, apenas enquanto trabalha nela.
- Prepara alterações nesse documento. Cada uma aguarda seu OK, como explicado acima.
- Cria novos documentos privados no seu Google Drive.

Ela não pesquisa no seu Drive. Só vê comentários, compartilhamentos e sugestões nos documentos que criou. Para acessar outros documentos, precisaria ter acesso a todo o seu Drive, mas ela não solicita isso.

No seu próprio computador, sua Machine pode criar um novo documento do Google em uma conta do Gmail conectada que já tenha acesso ao Drive. Ela não lê seus outros documentos do Google nem os comentários neles. **Documentos e arquivos** mostra essa opção como Google Docs, nessa conta. Ela também pode alterar um documento que criou nessa conta para uma tarefa.

## Trabalho ou uso pessoal

A integração segue a classificação Trabalho ou Pessoal da conexão, como acontece com o e-mail. Os documentos de Trabalho podem chegar ao Graph da sua equipe, de acordo com suas [regras de compartilhamento](sharing-rules.md). Os documentos pessoais nunca chegam lá.

## Remover

Abra **Conexões**, depois Microsoft OneDrive ou Google Docs, **Detalhes** e **Desconectar**. Ela deixará de ler. O que já tiver sido importado permanecerá. Em uma Machine hospedada, **Desconectar ↗** abre a página de configuração, onde ficam os dados de login.
