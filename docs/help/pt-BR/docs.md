---
title: Google Docs e Word
area: connections
summary: Comentários, menções, sugestões de edição e compartilhamentos nos seus arquivos do Google Docs ou Word. Ela lê, e só publica uma resposta a um comentário quando você der o OK.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
site: More sources, Connect documents, Sign in with Microsoft
---
## O que ela lê

Docs usa o login do Google ou da Microsoft que você já tem para esse endereço. Ela traz:

- Documentos que alguém compartilha com você.
- Comentários e respostas em documentos seus, e comentários que mencionam você.
- Sugestões de edição em documentos do Google Docs seus, e alterações controladas em arquivos do Word seus.

A primeira sincronização olha 30 dias para trás. Cada item vira um evento, ligado às pessoas e aos projetos do seu [Graph](graph.md). Quando um comentário precisa de você, ele vira uma tarefa.

## O que ela pode fazer

Quando uma tarefa precisa do texto de um documento, sua Machine lê só esse documento, e só enquanto trabalha nessa tarefa.

Ela pode escrever o rascunho de uma resposta a um comentário. No Google Docs, a resposta espera na tarefa: clique em **Revisar e publicar**, confira e depois clique em **Publicar agora**. Nada é publicado até você fazer isso. Arquivos do Word não permitem publicar uma resposta de fora do Word, então essas respostas ficam como rascunhos para você copiar no Word.

Ela nunca edita um documento, aceita uma sugestão, resolve um comentário ou compartilha um arquivo.

## O que ela pede

Ler documentos precisa de um OK próprio, separado do login do seu e-mail. Seu acesso ao Gmail e à agenda continua como está.

- Google: acesso só de leitura aos seus arquivos do Drive e aos comentários. Publicar respostas precisa de mais um OK, que você pode pular.
- Microsoft: acesso de leitura aos seus arquivos, incluindo os compartilhados com você no OneDrive e no SharePoint.

Se esse OK for retirado depois, o cartão do Docs mostra **Aguardando seu OK para ler documentos**.

## Conecte

Conecte primeiro o Outlook desse endereço. Depois:

- Machine hospedada: na sua página de configuração, abra **Docs** em **Mais fontes** e clique em **Conectar documentos** ao lado desse endereço. A Microsoft pede para você permitir a leitura dos seus arquivos.
- Seu próprio computador, pareado com sua conta: abra **Conexões**, **+ Adicionar**, escolha **Documentos** e clique em **Entrar com a Microsoft**.

Ela confere se o login pode ler documentos. Sem esse OK, Docs não é adicionado. O Google Docs ainda não está disponível pelo login da The Machine.

## Trabalho ou pessoal

Docs segue o rótulo de trabalho ou pessoal da conexão dele, como o e-mail. Documentos de trabalho podem chegar ao Graph da sua equipe conforme suas [regras de compartilhamento](sharing-rules.md). Os pessoais nunca chegam.

## Remova

No painel: **Conexões**, abra Docs, **Detalhes** e depois **Desconectar**. Ela para de ler. O que já foi trazido continua lá.
