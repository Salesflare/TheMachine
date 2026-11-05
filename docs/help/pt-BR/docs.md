---
title: Microsoft OneDrive: arquivos do Word no OneDrive e no SharePoint
area: connections
summary: Comentários, menções, alterações controladas e compartilhamentos nos seus arquivos do Word no OneDrive e no SharePoint, além de novos documentos privados, e edições que você aprova. O Google Docs vem depois.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## O que ela lê

A conexão **Microsoft OneDrive** lê arquivos do Word no OneDrive e no SharePoint. Você entra com a Microsoft para ela, com ou sem o Outlook conectado. Funciona em uma Machine hospedada e no seu próprio computador vinculado à sua conta. O Google Docs vem depois: o login do Google da The Machine ainda não consegue ler documentos. Ela traz:

- Documentos que alguém compartilha com você.
- Comentários e respostas em documentos seus, e comentários que mencionam você.
- Alterações controladas em arquivos do Word seus.

A primeira sincronização olha 30 dias para trás. Cada item vira um evento, ligado às pessoas e aos projetos do seu [Graph](graph.md). Quando um comentário precisa de você, ele vira uma tarefa.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê só esse documento, e só enquanto trabalha nessa tarefa.

Ela pode escrever o rascunho de uma resposta a um comentário. Arquivos do Word não permitem publicar uma resposta de fora do Word, então a resposta fica como rascunho para você copiar no Word.

Ela nunca aceita uma sugestão, resolve um comentário, compartilha um arquivo ou altera um documento sem o seu OK.

Uma conexão de documentos pode só fazer coisas: desligue **Traz sinais** em **Detalhes**, e ela só encontra e lê os documentos de que seus to-dos precisam, e cria novos. Uma do Google sem acesso a todo o Drive lê documentos pelo link, e os que sua Machine criou.

## Criar e editar documentos

Sua Machine pode escrever um novo documento, ou alterar um documento de que trata uma das suas tarefas:

- Um novo documento ela cria na hora, quando a tarefa ou uma habilidade pede um: um documento privado no seu próprio Google Drive ou OneDrive, sem compartilhar com ninguém. A tarefa o mostra com **Abrir o documento**. Compartilhar, ou enviar o link para alguém, espera o seu OK.
- Uma alteração em um documento existente ela só prepara, cada parágrafo antes e depois. Toque em **Revisar alterações**, leia e depois **Salvar**.
- Ela escreve uma alteração uma vez só, e só no documento como você o viu. Se alguém o alterou nesse meio-tempo, nada é escrito e a tarefa avisa. Peça um novo rascunho.
- No Talk, ela lê a alteração inteira em voz alta e espera um sim claro.
- Se o Google ou a Microsoft recusar um novo documento, a tarefa diz o que foi recusado e mostra **Revisar e criar** para tentar de novo.

Ela substitui texto, adiciona texto e adiciona parágrafos e títulos. Não mexe em tabelas, imagens, alterações controladas nem campos. Um novo documento fica no seu Google Drive ou OneDrive e é privado até você compartilhá-lo.

Um novo documento vai para uma conta da área da tarefa: o documento de uma tarefa de Trabalho para a conta dessa empresa, a da conversa quando dá, nunca para uma pessoal. No seu próprio computador, uma conta do Google conectada para o Gmail que já tem acesso ao Drive também pode receber um novo Google Doc. Se nenhuma conta servir, a tarefa diz **Conecte o Google Docs ou o Microsoft OneDrive para Trabalho**.

Quando o documento não é o fim da tarefa, como uma resposta com o link, a tarefa continua aberta e prepara esse próximo passo para o seu OK.

Conectar o Microsoft OneDrive já permite isso: não há um passo à parte. Uma conexão antiga do Microsoft OneDrive que só lê mostra **Permitir edições** no cartão dela em **Conexões**. Toque uma vez e aceite.

## O que ela pede

O Microsoft OneDrive pede um único OK à Microsoft, separado do login do seu e-mail: ler e alterar seus arquivos, incluindo os compartilhados com você no OneDrive e no SharePoint. Cada alteração ainda espera seu OK na tarefa dela. Seu acesso ao e-mail e à agenda continua como está. Sem o Outlook, o login só cobre seus arquivos, nunca seu e-mail ou sua agenda.

Se esse OK for retirado depois, o cartão do Microsoft OneDrive mostra **Aguardando seu OK para ler documentos**.

## Conecte

Você não precisa do Outlook conectado.

- Machine hospedada: no painel, abra **Conexões**, **+ Adicionar**, escolha **Microsoft OneDrive** e clique em **Entrar com a Microsoft**. A Microsoft pede para você permitir a leitura e a edição dos seus arquivos, e você volta para o painel.
- Seu próprio computador, pareado com sua conta: abra **Conexões**, **+ Adicionar**, escolha **Microsoft OneDrive** e clique em **Entrar com a Microsoft**.

Ela confere se o login pode ler documentos. Sem esse OK, o Microsoft OneDrive não é adicionado. Se você tocar em **Permitir edições** e a Microsoft não permitir edições, ela avisa em vez de mostrar Conectado.

## Trabalho ou pessoal

Microsoft OneDrive segue o rótulo de trabalho ou pessoal da conexão dele, como o e-mail. Documentos de trabalho podem chegar ao Graph da sua equipe conforme suas [regras de compartilhamento](sharing-rules.md). Os pessoais nunca chegam.

## Remova

No painel: **Conexões**, abra Microsoft OneDrive, **Detalhes** e depois **Desconectar**. Ela para de ler. O que já foi trazido continua lá.
