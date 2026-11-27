---
title: Microsoft OneDrive
area: connections
summary: Comentários, menções e alterações controladas nos seus arquivos do Word no OneDrive. Novos documentos e edições aguardam sua aprovação.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: e931920c74158c98
---
## O que ela lê

**Microsoft OneDrive** lê seus arquivos do Word no OneDrive, seja em uma Machine hospedada ou no seu próprio computador. Não é necessário conectar o Outlook. Para saber mais sobre o Google Docs, veja abaixo. Ela traz:

- Comentários e respostas nos seus arquivos do Word, incluindo comentários que mencionam você.
- Alterações controladas nos seus arquivos do Word.

A primeira sincronização inclui os últimos 7 dias. Cada item é vinculado às pessoas e aos projetos no seu [Graph](graph.md). Um comentário que precisa da sua atenção vira uma tarefa.

## Arquivos compartilhados com você por outras pessoas

A Microsoft deixará de listar esses arquivos em novembro de 2026. A partir daí, compartilhamentos e menções em arquivos de outras pessoas só chegam à sua Machine por e-mails enviados pela própria Microsoft. Conecte também o [Outlook](microsoft.md) e mantenha esses e-mails ativados. Uma tarefa criada a partir de um deles abre o e-mail, e o botão na mensagem abre o arquivo. Compartilhamentos ou menções sem e-mail não são detectados.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê apenas esse documento, e somente enquanto trabalha na tarefa. Ela pode ler arquivos do Word, PDF e texto.

Ela também procura arquivos de qualquer tipo no seu OneDrive e mostra o link. Não pesquisa em sites do SharePoint nem em arquivos compartilhados com você. Ela não consegue ler o texto de um PDF digitalizado.

Ela pode preparar uma resposta a um comentário. Como o Word não permite publicar respostas de fora do aplicativo, você precisa copiar o rascunho para o Word.

Ela nunca aceita uma sugestão, resolve um comentário, compartilha um arquivo ou altera um documento sem sua aprovação.

Para usar sua Machine apenas para executar tarefas, desative **Traz sinais** em **Detalhes**. Assim, ela só encontra e lê os arquivos necessários para suas tarefas e cria novos arquivos.

## Criar e editar documentos

Sua Machine pode criar um documento ou alterar um documento relacionado a uma tarefa:

- Ela cria um documento imediatamente quando a tarefa ou uma habilidade solicita. O documento é privado e fica no seu OneDrive ou Google Drive. A tarefa mostra **Abrir o documento**. Compartilhar o documento ou enviar o link dele aguarda sua aprovação.
- Uma alteração em um documento existente é apenas preparada. Pressione **Revisar alterações** para ver cada parágrafo antes e depois da alteração e, em seguida, **Salvar**. Se você pedir uma alteração no chat da tarefa, ela será feita imediatamente.
- Ela só escreve no documento da forma como você o viu. Se alguém o alterar nesse meio-tempo, nada será escrito e a tarefa avisará. Peça um novo rascunho.
- No Talk, ela lê a alteração completa em voz alta e espera um sim claro.
- Se a Microsoft ou o Google não permitir a criação de um documento, a tarefa explica o motivo e mostra **Revisar e criar** para tentar novamente.

Ela pode substituir e adicionar texto, parágrafos e títulos. No Google Docs, também pode aplicar formatação: negrito, itálico, sublinhado, links, títulos, listas com marcadores e numeradas, além de quebra de página. **Revisar alterações** mostra cada alteração. Ela não pode criar tabelas, e imagens, alterações controladas e campos permanecem como estão.

O documento de uma tarefa de Trabalho vai para a conta da empresa, nunca para uma conta pessoal. No seu próprio computador, uma conta do Google conectada ao Gmail e com acesso ao Drive também pode receber novos documentos do Google Docs. Se nenhuma conta for adequada, a tarefa informa o que conectar para Trabalho: Microsoft OneDrive ou Google Docs, quando sua Machine puder usá-lo.

Quando o documento não é a última etapa, como no caso de uma resposta com o link dele, a tarefa continua aberta e prepara essa etapa para sua aprovação.

A edição fica disponível ao conectar. Uma conexão mais antiga, que permite apenas leitura, mostra **Permitir edições** em **Conexões**. Pressione essa opção uma vez e aceite.

## O que ela solicita

A Microsoft pede uma única aprovação para ler e alterar seus arquivos, inclusive os compartilhados com você. Cada alteração ainda aguarda sua aprovação na tarefa. O acesso ao seu e-mail e calendário não muda.

Se essa aprovação for revogada depois, o Microsoft OneDrive mostrará **Aguardando seu OK para ler documentos** em **Conexões**.

## Conectar

Em uma Machine hospedada ou no seu próprio computador vinculado à sua conta:

- Abra **Conexões**, depois **Documentos e arquivos**, e selecione **Microsoft OneDrive**.
- Pressione **Entrar com a Microsoft** e permita que seus arquivos sejam lidos e editados.

Se a Microsoft não permitir a leitura, a conexão não será adicionada. Se você pressionar **Permitir edições** e a Microsoft não permitir edições, ela avisará.

## Google Docs

Em uma Machine hospedada, abra **Conexões**, depois **Documentos e arquivos**, e selecione **Google Docs**. O Google pedirá permissão para ver e editar os documentos que você indicar e criar novos. Não é necessário conectar o Gmail, e o acesso ao seu Gmail não muda.

Depois disso, sua Machine:

- Lê um documento do Google Docs vinculado às mensagens de uma tarefa ou colado no chat dela, somente enquanto trabalha nessa tarefa.
- Prepara alterações nesse documento. Cada alteração aguarda sua aprovação, como explicado acima.
- Cria novos documentos privados no seu Google Drive.

Se houver mais de uma conexão do Google Docs na área de uma tarefa, ela lê e altera um arquivo usando uma conexão que consiga abri-lo e talvez alterá-lo.

Ela não pesquisa no seu Drive. Só vê comentários, compartilhamentos e sugestões nos documentos que criou. Para acessar outros documentos, seria necessário ter acesso a todo o seu Drive, algo que ela não solicita.

## Google Sheets e Slides

Se o Google Docs mostrar **Permitir acesso ao Sheets e ao Slides** em **Conexões**, pressione essa opção e permita o acesso a ambos. O Google pedirá permissão para sua Machine ver seus arquivos do Sheets e do Slides. Ela não pode alterá-los.

Depois disso, sua Machine também lê uma planilha ou apresentação do Google vinculada às mensagens de uma tarefa ou colada no chat dela, somente enquanto trabalha nessa tarefa:

- De uma planilha, ela lê primeiro a guia ou as células vinculadas e, depois, as outras guias, até o limite de 2.000 células. Uma fórmula aparece como seu valor. Guias ocultas só são lidas quando são vinculadas ou solicitadas.
- De uma apresentação, ela lê o texto e as notas do apresentador, na ordem. Imagens e gráficos não são lidos.

### Editar Sheets e Slides

Depois que sua Machine puder lê-los, o Google Docs também poderá mostrar **Permitir edições em Sheets e Slides**. Pressione essa opção e permita as duas edições. Assim, sua Machine poderá alterar um arquivo do Sheets ou do Slides vinculado a uma tarefa ou colado no chat dela, da mesma forma que altera um documento: ela apenas prepara a alteração, **Revisar alterações** mostra o que será alterado, e nada é salvo até você pressionar **Salvar**.

- Em uma planilha: novos valores para células de uma guia, linhas adicionadas abaixo da última linha ou uma nova guia. Cada célula mostra o antes e o depois. Os valores são inseridos como texto; uma fórmula só é inserida como fórmula quando a tarefa solicitar.
- Em apresentações: texto substituído em um slide, com o antes e o depois, ou um novo slide com título e texto.
- Ela só escreve no arquivo da forma como você o viu. Se alguém alterar essas células ou os slides nesse meio-tempo, nada será escrito e a tarefa avisará.

A formatação, os gráficos, as imagens e os arquivos do Excel ou do PowerPoint permanecem como estão.

Para um arquivo grande, especifique no chat a guia, as células ou os slides desejados. Se o arquivo for privado de outra pessoa, tiver sido excluído ou for um arquivo do Excel ou do PowerPoint, a tarefa avisará. Um link do Google Drive funciona da mesma forma quando aponta para um arquivo do Google Docs, Sheets ou Slides.

## Google Docs no seu próprio computador

No seu próprio computador, sua Machine pode criar um documento do Google Docs em uma conta do Gmail que esteja conectada e já tenha acesso ao Drive. Ela não lê seus outros documentos do Google Docs nem os comentários neles. **Documentos e arquivos** mostra a conexão como Google Docs, nessa conta. Ela também pode alterar um documento que criou ali para uma tarefa.

Ela também lê um arquivo do Sheets ou do Slides vinculado a uma tarefa ou colado no chat dela, se essa conta do Google já tiver acesso ao Drive, ao Sheets ou ao Slides. Ela nunca solicita mais acesso ao Google e não altera esses arquivos. Se o Google negar o acesso, ative a API do Google Sheets ou do Slides no projeto do Google usado por essa conta.

## Trabalho ou pessoal

Ela segue a classificação Trabalho ou Pessoal da conexão, como no caso do e-mail. Os documentos de Trabalho podem chegar ao Graph da sua equipe, de acordo com suas [regras de compartilhamento](sharing-rules.md). Os documentos pessoais nunca chegam.

## Remover

Abra **Conexões**, selecione Microsoft OneDrive ou Google Docs, depois **Detalhes** e **Desconectar**. Ela deixará de ler os arquivos. O que já foi importado continuará disponível. Em uma Machine hospedada, **Desconectar ↗** abre a página de configuração, onde fica a conexão da conta.
