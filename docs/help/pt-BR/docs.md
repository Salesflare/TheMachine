---
title: Microsoft OneDrive
area: connections
summary: Comentários, menções e alterações controladas nos seus arquivos do Word no OneDrive. Novos documentos e alterações aguardam seu OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: c8fca3cf0299e327
---
## O que ela lê

**Microsoft OneDrive** lê seus arquivos do Word no OneDrive, tanto em uma Machine hospedada quanto no seu próprio computador. Não é necessário conectar o Outlook. Para saber mais sobre o Google Docs, veja abaixo. Ela traz:

- Comentários e respostas nos seus arquivos do Word, além de comentários que mencionam você.
- Alterações controladas nos seus arquivos do Word.

A primeira sincronização considera os últimos 7 dias. Cada item tem links para as pessoas e os projetos no seu [Graph](graph.md). Um comentário que exige sua atenção vira uma tarefa.

## Arquivos compartilhados com você por outras pessoas

A Microsoft vai parar de listar esses arquivos em novembro de 2026. A partir daí, compartilhamentos e menções em arquivos de outras pessoas só chegam à sua Machine pelos e-mails enviados pela própria Microsoft. Conecte também o [Outlook](microsoft.md) e mantenha esses e-mails ativados. Uma tarefa criada a partir de um e-mail abre a mensagem, e o botão dela abre o arquivo. Compartilhamentos ou menções sem e-mail não são detectados.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê esse documento enquanto trabalha na tarefa. Ela pode ler arquivos do Word, PDF e texto.

Ela também procura arquivos de qualquer tipo no seu OneDrive e mostra o link. Não pesquisa em sites do SharePoint nem em arquivos compartilhados com você. Também não consegue ler o texto de PDFs digitalizados.

Ela pode preparar uma resposta a um comentário. Como o Word não permite publicar respostas de fora dele, você precisa copiar o rascunho para o Word.

Ela nunca aceita uma sugestão, resolve um comentário, compartilha um arquivo ou altera um documento sem seu OK.

Para usar a integração apenas para realizar tarefas, desative **Traz sinais** em **Detalhes**. Assim, ela só encontra e lê os arquivos necessários para suas tarefas e cria novos arquivos.

## Criar e editar documentos

Sua Machine pode criar um documento ou alterar um documento relacionado a uma tarefa:

- Ela cria um documento na hora quando a tarefa ou uma habilidade pede. O documento é privado e fica no seu OneDrive ou Google Drive. A tarefa mostra **Abrir o documento**. Compartilhar o documento ou enviar o link dele aguarda seu OK.
- Para alterar um documento existente, ela apenas prepara as mudanças. Pressione **Revisar alterações** para ver cada parágrafo antes e depois e, em seguida, **Salvar**. Uma alteração solicitada no chat da tarefa é feita na hora.
- Ela só escreve no documento que você viu. Se alguém tiver alterado o documento nesse meio-tempo, nada será escrito e a tarefa avisará. Peça um novo rascunho.
- No Talk, ela lê a alteração inteira em voz alta e aguarda um sim claro.
- Se a Microsoft ou o Google não permitir criar um documento, a tarefa explica o motivo e mostra **Revisar e criar** para tentar de novo.

Ela pode substituir e adicionar texto, parágrafos e títulos. No Google Docs, também pode aplicar formatação: negrito, itálico, sublinhado, links, títulos, listas com marcadores e numeradas, além de quebra de página. **Revisar alterações** mostra cada mudança. Ela não pode criar tabelas. Imagens, alterações controladas e campos permanecem como estão.

O documento de uma tarefa de trabalho fica na conta da empresa, nunca em uma conta pessoal. No seu próprio computador, uma conta Google conectada ao Gmail e com acesso ao Drive também pode receber novos documentos do Google Docs. Se nenhuma conta for adequada, a tarefa informa o que conectar para o trabalho: Microsoft OneDrive ou Google Docs, onde sua Machine puder usá-lo.

Quando o documento não for a última etapa, como no caso de uma resposta com o link dele, a tarefa continua aberta e prepara essa etapa para seu OK.

A edição é habilitada ao conectar. Uma conexão antiga que só permite leitura mostra **Permitir edições** em **Conexões**. Pressione uma vez e aceite.

## O que ela solicita

A Microsoft pede um único OK: para ler e alterar seus arquivos, inclusive os compartilhados com você. Cada alteração ainda aguarda seu OK na tarefa correspondente. O acesso ao seu e-mail e calendário não muda.

Se você retirar esse OK depois, Microsoft OneDrive mostrará **Aguardando seu OK para ler documentos** em **Conexões**.

## Conectar

Em uma Machine hospedada ou no seu próprio computador pareado com sua conta:

- Abra **Conexões**, depois **Documentos e arquivos**, e escolha **Microsoft OneDrive**.
- Pressione **Entrar com a Microsoft** e permita a leitura e a edição dos seus arquivos.

Se a Microsoft não permitir a leitura, a integração não será adicionada. Se você pressionar **Permitir edições** e a Microsoft não permitir alterações, ela avisará.

## Google Docs

Em uma Machine hospedada, abra **Conexões**, depois **Documentos e arquivos**, e escolha **Google Docs**. O Google pede permissão para acessar e editar os documentos que você indicar e criar novos. Não é necessário conectar o Gmail, e o acesso ao Gmail não muda.

Depois disso, sua Machine:

- Lê um documento do Google Docs vinculado às mensagens de uma tarefa ou colado no chat dela, somente enquanto trabalha nessa tarefa.
- Prepara alterações nesse documento. Cada alteração aguarda seu OK, como explicado acima.
- Cria novos documentos privados no seu Google Drive.

Ela não pesquisa no seu Drive. Só vê comentários, compartilhamentos e sugestões nos documentos que criou. Para acessar outros documentos, seria necessário acessar todo o seu Drive, e ela não pede essa permissão.

## Google Sheets e Slides

Se o Google Docs mostrar **Permitir acesso ao Sheets e ao Slides** em **Conexões**, pressione essa opção e permita o acesso aos dois. O Google pede permissão para que sua Machine veja seus arquivos do Sheets e Slides. Ela não pode alterá-los.

Depois disso, sua Machine também lê um arquivo do Google Sheets ou Slides vinculado às mensagens de uma tarefa ou colado no chat dela, somente enquanto trabalha nessa tarefa:

- Em uma planilha, primeiro a guia ou as células vinculadas e, em seguida, as outras guias, até 2.000 células. Uma fórmula aparece como seu valor. Guias ocultas só são lidas quando estão vinculadas ou quando você pede.
- Em apresentações, o texto e as notas do apresentador, na ordem. Imagens e gráficos não são lidos.

Se o arquivo for grande, especifique no chat a guia, as células ou os slides que você quer. Se o arquivo for particular de outra pessoa, tiver sido excluído ou for um arquivo do Excel ou PowerPoint, a tarefa avisará. Um link do Google Drive funciona da mesma forma quando leva a um arquivo do Google Docs, Sheets ou Slides.

## Google Docs no seu próprio computador

No seu próprio computador, sua Machine pode criar um documento do Google Docs em uma conta do Gmail já conectada, que tenha acesso ao Drive. Ela não lê seus outros documentos do Google Docs nem os comentários deles. **Documentos e arquivos** mostra a opção Google Docs nessa conta. Ela também pode alterar um documento que criou ali para uma tarefa.

Ela também lê um arquivo do Google Sheets ou Slides vinculado a uma tarefa ou colado no chat dela, se essa conta Google já tiver acesso ao Drive, Sheets ou Slides. Ela nunca pede mais permissões ao Google. Se o Google não permitir o acesso, ative a API do Google Sheets ou Slides no projeto Google da própria conta conectada.

## Trabalho ou pessoal

A integração segue a classificação Trabalho ou Pessoal da conexão, como acontece com o e-mail. Documentos de trabalho podem chegar ao Graph da sua equipe de acordo com suas [regras de compartilhamento](sharing-rules.md). Documentos pessoais nunca chegam.

## Remover a integração

Abra **Conexões**, depois Microsoft OneDrive ou Google Docs, **Detalhes** e **Desconectar**. A integração para de ler. O que ela já trouxe continua disponível. Em uma Machine hospedada, **Desconectar ↗** abre a página de configuração que contém a conta conectada.
