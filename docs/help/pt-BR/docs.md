---
title: Docs: Word, OneDrive e SharePoint
area: connections
summary: Comentários, menções, alterações controladas e compartilhamentos nos seus arquivos do Word no OneDrive e no SharePoint. O Google Docs vem depois.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## O que ela lê

Docs lê arquivos do Word no OneDrive e no SharePoint, com o login da Microsoft que você já tem para esse endereço. Funciona em uma Machine hospedada e no seu próprio computador vinculado à sua conta. O Google Docs vem depois: o login do Google da The Machine ainda não consegue ler documentos. Ela traz:

- Documentos que alguém compartilha com você.
- Comentários e respostas em documentos seus, e comentários que mencionam você.
- Alterações controladas em arquivos do Word seus.

A primeira sincronização olha 30 dias para trás. Cada item vira um evento, ligado às pessoas e aos projetos do seu [Graph](graph.md). Quando um comentário precisa de você, ele vira uma tarefa.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê só esse documento, e só enquanto trabalha nessa tarefa.

Ela pode escrever o rascunho de uma resposta a um comentário. Arquivos do Word não permitem publicar uma resposta de fora do Word, então a resposta fica como rascunho para você copiar no Word.

Ela nunca aceita uma sugestão, resolve um comentário, compartilha um arquivo ou altera um documento sem o seu OK.

## Criar e editar documentos

Sua Machine pode escrever um novo documento do Word, ou alterar um documento de que trata uma das suas tarefas. Ela nunca escreve sozinha:

- Ela prepara a alteração na tarefa. Um novo documento aparece inteiro. Uma edição mostra cada parágrafo antes e depois.
- Toque em **Revisar e criar** ou **Revisar alterações**, leia e depois **Criar** ou **Salvar**.
- Ela escreve uma vez só, e só no documento como você o viu. Se alguém o alterou nesse meio-tempo, nada é escrito e a tarefa avisa. Peça um novo rascunho.
- No Talk, ela lê a alteração inteira em voz alta e espera um sim claro.

Ela substitui texto, adiciona texto e adiciona parágrafos e títulos. Não mexe em tabelas, imagens, alterações controladas nem campos. Um novo documento fica no seu OneDrive e é privado até você compartilhá-lo.

Para ativar, toque em **Permitir edições** no cartão do Docs em **Conexões**. A Microsoft pede para deixar alterar seus arquivos, separado da leitura. Entrar de novo mantém isso.

## O que ela pede

Ler documentos precisa de um OK próprio, separado do login do seu e-mail: a Microsoft pede para você permitir a leitura dos seus arquivos, incluindo os compartilhados com você no OneDrive e no SharePoint. Seu acesso ao e-mail e à agenda continua como está.

Se esse OK for retirado depois, o cartão do Docs mostra **Aguardando seu OK para ler documentos**.

## Conecte

Conecte primeiro o Outlook desse endereço. Depois:

- Machine hospedada: no painel, abra **Conexões**, **+ Adicionar**, escolha **Documentos** e clique em **Entrar com a Microsoft**. A Microsoft pede para você permitir a leitura dos seus arquivos, e você volta para o painel.
- Seu próprio computador, pareado com sua conta: abra **Conexões**, **+ Adicionar**, escolha **Documentos** e clique em **Entrar com a Microsoft**.

Ela confere se o login pode ler documentos. Sem esse OK, Docs não é adicionado.

## Trabalho ou pessoal

Docs segue o rótulo de trabalho ou pessoal da conexão dele, como o e-mail. Documentos de trabalho podem chegar ao Graph da sua equipe conforme suas [regras de compartilhamento](sharing-rules.md). Os pessoais nunca chegam.

## Remova

No painel: **Conexões**, abra Docs, **Detalhes** e depois **Desconectar**. Ela para de ler. O que já foi trazido continua lá.
