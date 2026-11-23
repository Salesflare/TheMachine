---
title: Microsoft OneDrive
area: connections
summary: Comentários, menções e alterações controladas nos seus arquivos do Word no OneDrive. Novos documentos e edições aguardam sua aprovação.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 41e5651f29782588
---
## O que ela lê

**Microsoft OneDrive** lê seus arquivos do Word no OneDrive, tanto em uma Machine hospedada quanto no seu próprio computador. Não é necessário conectar o Outlook. Para saber mais sobre o Google Docs, veja abaixo. Ela traz:

- Comentários e respostas nos seus arquivos do Word, além de comentários que mencionam você.
- Alterações controladas nos seus arquivos do Word.

A primeira sincronização busca os últimos 7 dias. Cada item se conecta às pessoas e aos projetos do seu [Graph](graph.md). Um comentário que precisa da sua atenção vira uma tarefa.

## Arquivos compartilhados com você

A Microsoft deixará de listar esses arquivos em novembro de 2026. A partir daí, compartilhamentos e menções em arquivos de outras pessoas só chegam à sua Machine pelos e-mails enviados pela própria Microsoft. Conecte também o [Outlook](microsoft.md) e mantenha esses e-mails. Uma tarefa criada a partir de um deles abre o e-mail, e o botão nele abre o arquivo. Compartilhamentos ou menções sem e-mail não são detectados.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê apenas esse documento, e somente enquanto trabalha nessa tarefa. Ela pode ler arquivos do Word, PDF e texto.

Ela também procura arquivos de qualquer tipo no seu OneDrive e mostra o link. Não pesquisa em sites do SharePoint nem em arquivos compartilhados com você. Ela não consegue ler o texto de um PDF digitalizado.

Ela pode criar um rascunho de resposta a um comentário. Como o Word não permite publicar respostas de fora dele, você precisa copiar o rascunho para o Word.

Ela nunca aceita uma sugestão, resolve um comentário, compartilha um arquivo nem altera um documento sem sua aprovação.

Para usar o recurso apenas para executar tarefas, desative **Traz sinais** em **Detalhes**. Aí, ela só encontra e lê os arquivos necessários para suas tarefas e cria novos arquivos.

## Criar e editar documentos

Sua Machine pode criar um documento ou alterar um documento relacionado a uma tarefa:

- Ela cria um documento imediatamente quando a tarefa ou uma habilidade pede. O documento é privado e fica no seu OneDrive ou Google Drive. A tarefa mostra **Abrir o documento**. Compartilhar o documento ou enviar o link aguarda sua aprovação.
- Para alterar um documento existente, ela primeiro prepara as alterações. Pressione **Revisar alterações** para ver cada parágrafo antes e depois e, em seguida, pressione **Salvar**. Se você pedir uma alteração no chat da tarefa, ela será feita na hora.
- Ela só escreve no documento tal como você o viu. Se alguém tiver alterado o documento nesse meio-tempo, nada será escrito e a tarefa avisará. Peça um novo rascunho.
- No Talk, ela lê toda a alteração em voz alta e espera um sim claro.
- Se a Microsoft ou o Google não permitir criar um documento, a tarefa explica o motivo e mostra **Revisar e criar** para tentar novamente.

Ela pode substituir e adicionar texto, parágrafos e títulos. Tabelas, imagens, alterações controladas e campos permanecem como estão.

O documento de uma tarefa de Trabalho vai para a conta da empresa, nunca para uma conta pessoal. No seu próprio computador, uma conta do Google conectada para o Gmail e com acesso ao Drive também pode criar novos documentos do Google. Se nenhuma conta for adequada, a tarefa informa o que você precisa conectar para Trabalho: Microsoft OneDrive ou Google Docs, quando sua Machine puder usá-lo.

Quando o documento não é a última etapa, como no caso de uma resposta com o link para ele, a tarefa continua aberta e prepara essa etapa para sua aprovação.

A edição fica disponível ao conectar. Uma conexão antiga que só permite leitura mostra **Permitir edições** em **Conexões**. Pressione uma vez e aceite.

## O que ela pede

A Microsoft pede uma única autorização: para ler e alterar seus arquivos, inclusive os compartilhados com você. Cada alteração ainda aguarda sua aprovação na tarefa correspondente. O acesso ao seu e-mail e calendário não muda.

Se essa autorização for revogada depois, Microsoft OneDrive mostrará **Aguardando seu OK para ler documentos** em **Conexões**.

## Conectar

Em uma Machine hospedada ou no seu próprio computador emparelhado com sua conta:

- Abra **Conexões**, depois **Documentos e arquivos**, e selecione **Microsoft OneDrive**.
- Pressione **Entrar com a Microsoft** e permita que ela leia e edite seus arquivos.

Se a Microsoft não permitir a leitura, a conexão não será adicionada. Se você pressionar **Permitir edições** e a Microsoft não permitir a edição, ela avisará.

## Google Docs

Em uma Machine hospedada, abra **Conexões**, depois **Documentos e arquivos**, e selecione **Google Docs**. O Google pedirá permissão para ver e editar os documentos que você indicar e criar novos. Não é necessário conectar o Gmail, e o acesso ao Gmail não muda.

Depois disso, sua Machine:

- Lê um documento do Google vinculado às mensagens de uma tarefa, somente enquanto trabalha nela.
- Prepara alterações nesse documento. Cada uma aguarda sua aprovação, como explicado acima.
- Cria novos documentos privados no seu Google Drive.

Ela não pesquisa no seu Drive. Só vê comentários, compartilhamentos e sugestões nos documentos que criou. Para ver mais, precisaria de acesso ao seu Drive inteiro, que ela não pede.

No seu próprio computador, sua Machine pode criar um documento do Google em uma conta do Gmail conectada nele que já tenha acesso ao Drive. Ela não lê seus outros documentos do Google nem os comentários deles. **Documentos e arquivos** mostra essa conexão como Google Docs, nessa conta. Ela também pode alterar um documento que criou nessa conta para uma tarefa.

## Trabalho ou pessoal

Ela segue a classificação Trabalho ou Pessoal da conexão, como acontece com o e-mail. Documentos de Trabalho podem chegar ao Graph da sua equipe, de acordo com suas [regras de compartilhamento](sharing-rules.md). Documentos pessoais nunca chegam.

## Remover

Abra **Conexões**, selecione Microsoft OneDrive ou Google Docs, depois **Detalhes** e **Desconectar**. A Machine para de ler os documentos. O que ela já trouxe continua disponível. Em uma Machine hospedada, **Desconectar ↗** abre a página de configuração, onde fica o login.
