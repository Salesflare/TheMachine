---
title: Microsoft OneDrive
area: connections
summary: Comentários, menções e alterações controladas nos seus arquivos do Word no OneDrive. Novos documentos e edições aguardam sua aprovação.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 057429e4c3b6408c
---
## O que ela lê

**Microsoft OneDrive** lê seus arquivos do Word no OneDrive, em uma Machine hospedada e no seu próprio computador. Não é necessário conectar o Outlook. Para o Google Docs, veja abaixo. Ela traz:

- Comentários e respostas nos seus arquivos do Word, além de comentários que mencionam você.
- Alterações controladas nos seus arquivos do Word.

A primeira sincronização considera os últimos 7 dias. Cada item leva às pessoas e aos projetos no seu [Graph](graph.md). Um comentário que precisa da sua atenção vira uma tarefa.

## Arquivos compartilhados com você

A Microsoft vai deixar de listar esses arquivos em novembro de 2026. A partir daí, compartilhamentos e menções em arquivos de outras pessoas só chegam à sua Machine como e-mails da própria Microsoft. Conecte também o [Outlook](microsoft.md) e mantenha esses e-mails ativados. Uma tarefa criada a partir de um desses e-mails abre a mensagem, e o botão dela abre o arquivo. Compartilhamentos ou menções sem e-mail não são detectados.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê apenas esse documento e somente enquanto trabalha na tarefa. Ela pode ler arquivos do Word, PDF e texto.

Ela também procura arquivos de qualquer tipo no seu próprio OneDrive e fornece o link. Não pesquisa em sites do SharePoint nem em arquivos compartilhados com você. Não consegue ler o texto de PDFs digitalizados.

Ela pode preparar uma resposta a um comentário. Como o Word não permite publicar respostas de fora dele, você precisa copiar o rascunho para o Word.

Ela nunca aceita uma sugestão, resolve um comentário, compartilha um arquivo ou altera um documento sem sua aprovação.

Para usar a integração apenas para executar tarefas, desative **Traz sinais** em **Detalhes**. Assim, ela só encontra e lê os arquivos necessários para suas tarefas e cria arquivos novos.

## Criar e editar documentos

Sua Machine pode criar um documento ou alterar um documento relacionado a uma tarefa:

- Ela cria um documento novo imediatamente quando a tarefa ou uma habilidade pede. O documento é privado e fica no seu próprio OneDrive ou Google Drive. A tarefa mostra **Abrir o documento**. Compartilhar o documento ou enviar o link aguarda sua aprovação.
- Uma alteração em um documento existente é apenas preparada. Pressione **Revisar alterações** para ver cada parágrafo antes e depois e, em seguida, **Salvar**. Uma alteração que você pede no chat da tarefa é feita imediatamente.
- Ela só escreve no documento da forma como você o viu. Se alguém o tiver alterado nesse meio-tempo, nada será escrito, e a tarefa avisará. Peça um novo rascunho.
- No Talk, ela lê toda a alteração em voz alta e aguarda um sim claro.
- Se a Microsoft ou o Google não permitir criar um documento, a tarefa explicará o motivo e mostrará **Revisar e criar** para tentar novamente.

Ela pode substituir e adicionar texto, parágrafos e títulos. No Google Docs, também pode aplicar formatação: negrito, itálico, sublinhado, links, títulos, listas com marcadores e numeradas e quebra de página. **Revisar alterações** mostra cada alteração. Ela não pode criar tabelas. Imagens, alterações controladas e campos permanecem como estão.

O documento de uma tarefa de trabalho vai para a conta da empresa, nunca para uma conta pessoal. No seu próprio computador, uma conta do Google conectada para o Gmail e com acesso ao Drive também pode receber novos arquivos do Google Docs. Se nenhuma conta for adequada, a tarefa dirá o que conectar para o trabalho: Microsoft OneDrive ou Google Docs, quando sua Machine puder usá-lo.

Quando o documento não for a última etapa, como no caso de uma resposta com o link dele, a tarefa continua aberta e prepara essa etapa para sua aprovação.

A edição é ativada ao conectar a integração. Uma conexão antiga que permite apenas leitura mostra **Permitir edições** em **Conexões**. Pressione essa opção uma vez e aceite.

## O que ela solicita

A Microsoft pede uma única autorização: para ler e alterar seus arquivos, inclusive os compartilhados com você. Cada alteração ainda aguarda sua aprovação na tarefa. O acesso ao seu e-mail e calendário não muda.

Se você retirar essa autorização depois, Microsoft OneDrive mostrará **Aguardando seu OK para ler documentos** em **Conexões**.

## Conectar

Em uma Machine hospedada ou no seu próprio computador emparelhado com sua conta:

- Abra **Conexões**, depois **Documentos e arquivos**, e escolha **Microsoft OneDrive**.
- Pressione **Entrar com a Microsoft** e permita a leitura e a edição dos seus arquivos.

Se a Microsoft não permitir a leitura, a integração não será adicionada. Se você pressionar **Permitir edições** e a Microsoft não permitir edições, ela avisará.

## Google Docs

Em uma Machine hospedada, abra **Conexões**, depois **Documentos e arquivos**, e escolha **Google Docs**. O Google pedirá autorização para ver e editar os documentos que você indicar e criar novos. Não é necessário conectar o Gmail, e o acesso ao Gmail não muda.

Depois, sua Machine:

- Lê um Google Doc vinculado às mensagens de uma tarefa ou colado no chat dela, somente enquanto trabalha nessa tarefa.
- Prepara alterações nesse documento. Cada alteração aguarda sua aprovação, como explicado acima.
- Cria documentos privados novos no seu Google Drive.

Ela não pesquisa no seu Drive. Só vê comentários, compartilhamentos e sugestões nos documentos que criou. Para ver mais, precisaria de acesso ao seu Drive inteiro, que ela não solicita.

## Google Sheets e Slides

Se o Google Docs em **Conexões** mostrar **Permitir acesso ao Sheets e ao Slides**, pressione essa opção e permita o acesso a ambos. O Google pedirá autorização para sua Machine ver seus arquivos do Sheets e Slides. Ela não pode alterá-los.

Depois, sua Machine também lê uma planilha do Google Sheets ou um arquivo do Slides vinculado às mensagens de uma tarefa ou colado no chat dela, somente enquanto trabalha nessa tarefa:

- Em uma planilha, primeiro a guia ou as células vinculadas e, depois, as outras guias, até o limite de 2.000 células. Uma fórmula aparece como o valor dela. Guias ocultas só são lidas quando há um link para elas ou quando são solicitadas.
- Em apresentações, o texto e as notas do apresentador, na ordem. Imagens e gráficos não são lidos.

### Editar Sheets e Slides

Depois que sua Machine os ler, o Google Docs também poderá mostrar **Permitir edições em Sheets e Slides**. Pressione essa opção e permita o acesso a ambos. Assim, sua Machine poderá alterar uma planilha vinculada do Sheets ou um arquivo do Slides da mesma forma que altera um documento: ela apenas prepara a alteração, **Revisar alterações** mostra o que mudou e nada é salvo até você pressionar **Salvar**.

- Em uma planilha: novos valores para células de uma guia, linhas adicionadas depois da última linha ou uma guia nova. Cada célula mostra o antes e o depois. Os valores são inseridos como texto. Uma fórmula só é inserida como fórmula quando a tarefa pedir.
- Em apresentações: texto substituído em um slide, com o antes e o depois, ou um slide novo com título e texto.
- Ela só escreve no arquivo da forma como você o viu. Se alguém tiver alterado essas células ou os slides nesse meio-tempo, nada será escrito, e a tarefa avisará.

A formatação, os gráficos, as imagens e os arquivos do Excel ou PowerPoint permanecem como estão.

Para um arquivo grande, indique no chat a guia, as células ou os slides que você quer. Se o arquivo for privado de outra pessoa, tiver sido excluído ou for um arquivo do Excel ou PowerPoint, a tarefa avisará. Um link do Google Drive funciona da mesma forma quando leva a um arquivo do Google Docs, Sheets ou Slides.

## Google Docs no seu próprio computador

No seu próprio computador, sua Machine pode criar um Google Doc novo em uma conta do Gmail que esteja conectada e já tenha acesso ao Drive. Ela não lê seus outros documentos do Google Docs nem os comentários deles. **Documentos e arquivos** mostra essa opção como Google Docs, nessa conta. Ela também pode alterar um documento que criou ali para uma tarefa.

Ela também lê um arquivo do Google Sheets ou Slides vinculado a uma tarefa ou colado no chat dela, se essa conta do Google já tiver acesso ao Drive, Sheets ou Slides. Ela nunca pede mais acesso ao Google nem altera esses arquivos. Se o Google não permitir, ative a API do Google Sheets ou Slides no próprio projeto do Google dessa conta.

## Trabalho ou pessoal

A integração segue a classificação Trabalho ou Pessoal da conexão, como acontece com o e-mail. Documentos de trabalho podem chegar ao Graph da sua equipe, conforme suas [regras de compartilhamento](sharing-rules.md). Documentos pessoais nunca chegam.

## Remover

Abra **Conexões**, depois Microsoft OneDrive ou Google Docs, **Detalhes** e **Desconectar**. A integração para de ler os arquivos. O que ela já trouxe permanece. Em uma Machine hospedada, **Desconectar ↗** abre a página de configuração, que mantém a sessão conectada.
