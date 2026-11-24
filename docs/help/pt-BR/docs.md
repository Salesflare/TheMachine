---
title: Microsoft OneDrive
area: connections
summary: Comentários, menções e alterações controladas nos seus arquivos do Word no OneDrive. Novos documentos e edições aguardam sua aprovação.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: d79388a1c8811d5f
---
## O que ela lê

O **Microsoft OneDrive** lê seus arquivos do Word no OneDrive, em uma Machine hospedada e no seu próprio computador. Não é necessário conectar o Outlook. Para o Google Docs, veja abaixo. Ela traz:

- Comentários e respostas nos seus arquivos do Word, além de comentários que mencionam você.
- Alterações controladas nos seus arquivos do Word.

A primeira sincronização busca os últimos 7 dias. Cada item tem links para as pessoas e os projetos do seu [Graph](graph.md). Um comentário que exige sua atenção vira uma tarefa.

## Arquivos que outras pessoas compartilham com você

A Microsoft vai parar de listar esses arquivos em novembro de 2026. A partir daí, os compartilhamentos e as menções em arquivos de outras pessoas só chegam à sua Machine por e-mails da própria Microsoft. Conecte também o [Outlook](microsoft.md) e mantenha esses e-mails ativados. Uma tarefa criada a partir de um e-mail abre a mensagem, e o botão dela abre o arquivo. Compartilhamentos e menções sem e-mail não são detectados.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê apenas aquele documento, e somente enquanto trabalha na tarefa. Ela pode ler arquivos do Word, PDF e texto.

Ela também procura arquivos de qualquer tipo no seu próprio OneDrive e mostra o link. Não pesquisa em sites do SharePoint nem em arquivos compartilhados com você. Não consegue ler o texto de um PDF digitalizado.

Ela pode criar um rascunho de resposta a um comentário. Como o Word não permite publicar respostas de fora dele, você precisa copiar o rascunho para o Word.

Ela nunca aceita uma sugestão, resolve um comentário, compartilha um arquivo ou altera um documento sem sua aprovação.

Para usá-la apenas para executar tarefas, desative **Traz sinais** em **Detalhes**. Assim, ela só encontra e lê os arquivos necessários para suas tarefas e cria novos arquivos.

## Criar e editar documentos

Sua Machine pode criar um documento ou alterar um documento relacionado a uma tarefa:

- Ela cria um documento na hora quando a tarefa ou uma habilidade pede. O documento é privado e fica no seu OneDrive ou Google Drive. A tarefa mostra **Abrir o documento**. Compartilhar o documento ou enviar o link aguarda sua aprovação.
- Para alterar um documento existente, ela prepara as mudanças. Pressione **Revisar alterações** para ver cada parágrafo antes e depois e, em seguida, pressione **Salvar**. Uma alteração que você pedir no chat da tarefa é feita na hora.
- Ela só escreve no documento exatamente como você o viu. Se alguém o alterar nesse meio-tempo, nada será escrito e a tarefa avisará. Peça um novo rascunho.
- No Talk, ela lê a alteração inteira em voz alta e espera uma confirmação clara.
- Se a Microsoft ou o Google não permitir criar um documento, a tarefa explica o motivo e mostra **Revisar e criar** para tentar novamente.

Ela pode substituir e adicionar texto, parágrafos e títulos. Tabelas, imagens, alterações controladas e campos permanecem como estão.

O documento de uma tarefa de Trabalho vai para a conta da empresa, nunca para uma conta pessoal. No seu próprio computador, uma conta do Google conectada ao Gmail e com acesso ao Drive também pode receber novos Google Docs. Se nenhuma conta servir, a tarefa informa o que conectar para o Trabalho: Microsoft OneDrive ou Google Docs, quando sua Machine puder usá-lo.

Quando o documento não é a última etapa, como no caso de uma resposta com o link dele, a tarefa continua aberta e prepara essa etapa para sua aprovação.

A edição é incluída ao conectar. Uma conexão antiga que só permite leitura mostra **Permitir edições** em **Conexões**. Pressione uma vez e aceite.

## O que ela solicita

A Microsoft pede uma única aprovação para ler e alterar seus arquivos, inclusive os compartilhados com você. Cada alteração ainda aguarda sua aprovação na tarefa. O acesso ao seu e-mail e calendário não muda.

Se você retirar essa aprovação depois, o Microsoft OneDrive mostrará **Aguardando seu OK para ler documentos** em **Conexões**.

## Conectar

Em uma Machine hospedada ou no seu próprio computador pareado com sua conta:

- Abra **Conexões**, depois **Documentos e arquivos**, e escolha **Microsoft OneDrive**.
- Pressione **Entrar com a Microsoft** e permita a leitura e a edição dos seus arquivos.

Se a Microsoft não permitir a leitura, a conexão não será adicionada. Se você pressionar **Permitir edições** e a Microsoft não permitir a edição, ela avisará.

## Google Docs

Em uma Machine hospedada, abra **Conexões**, depois **Documentos e arquivos**, e escolha **Google Docs**. O Google pedirá permissão para ver e editar os documentos que você indicar e criar novos documentos. Não é necessário conectar o Gmail, e o acesso ao Gmail não muda.

Sua Machine:

- Lê um Google Doc vinculado às mensagens de uma tarefa ou colado no chat dela, somente enquanto trabalha nessa tarefa.
- Prepara alterações nesse documento. Cada uma aguarda sua aprovação, como descrito acima.
- Cria novos documentos privados no seu Google Drive.

Ela não pesquisa no seu Drive. Só vê comentários, compartilhamentos e sugestões nos documentos que criou. Para ver mais, precisaria de acesso ao seu Drive inteiro, que ela não solicita.

## Google Sheets e Slides

Se **Google Docs** em **Conexões** mostrar **Permitir acesso ao Sheets e ao Slides**, pressione essa opção e permita o acesso aos dois. O Google pedirá permissão para sua Machine ver seus arquivos do Sheets e do Slides. Ela não pode alterá-los.

Sua Machine também lê um arquivo do Google Sheets ou do Slides vinculado às mensagens de uma tarefa ou colado no chat dela, somente enquanto trabalha nessa tarefa:

- Em uma planilha, primeiro a guia ou as células vinculadas e, depois, as outras guias, até um total de 2.000 células. Uma fórmula aparece como seu valor. Guias ocultas só são lidas quando estão vinculadas ou quando alguém pede.
- Em apresentações, o texto e as notas do apresentador, na ordem. Imagens e gráficos não são lidos.

Se o arquivo for grande, peça no chat a guia, as células ou os slides que você quer. Se o arquivo for privado de outra pessoa, tiver sido excluído ou for um arquivo do Excel ou do PowerPoint, a tarefa avisará. Um link do Google Drive funciona da mesma forma quando leva a um arquivo do Google Docs, Sheets ou Slides.

## Google Docs no seu próprio computador

No seu próprio computador, sua Machine pode criar um Google Doc em uma conta do Gmail conectada ali que já tenha acesso ao Drive. Ela não lê seus outros Google Docs nem os comentários deles. **Documentos e arquivos** mostra essa conexão como Google Docs, nessa conta. Ela também pode alterar um documento que criou ali para uma tarefa.

Ela também lê um arquivo do Google Sheets ou do Slides vinculado a uma tarefa ou colado no chat dela, se esse login do Google já tiver acesso ao Drive, Sheets ou Slides. Ela nunca solicita mais acesso ao Google. Se o Google negar o acesso, ative a API do Google Sheets ou do Slides no projeto do Google dessa conta.

## Trabalho ou pessoal

Ela segue o rótulo Trabalho ou Pessoal da conexão, como acontece com o e-mail. Os documentos de Trabalho podem chegar ao Graph da sua equipe, de acordo com suas [regras de compartilhamento](sharing-rules.md). Os pessoais nunca chegam.

## Remover a conexão

Abra **Conexões**, depois Microsoft OneDrive ou Google Docs, **Detalhes** e **Desconectar**. A leitura será interrompida. O conteúdo que ela já trouxe continuará disponível. Em uma Machine hospedada, **Desconectar ↗** abre sua página de configuração, onde fica o login.
