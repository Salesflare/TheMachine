---
title: Chat da tarefa
area: cards
summary: Pergunte sobre uma tarefa ou altere o rascunho dela em um chat vinculado à tarefa.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 340b9cfc0e3a424d
---
## Abrir

No celular, toque no título da tarefa. No computador, clique em **Ver no chat ›** ou no link do chat da tarefa. Clicar no título no computador renomeia a tarefa.

## E-mails no chat

Cada e-mail mostra apenas o que há de novo. As mensagens anteriores citadas nele ficam recolhidas em **Mensagens anteriores**. **Ler a conversa** abre os e-mails na íntegra.

## O que ela fez

Cada execução aparece em uma linha discreta, como "Verificou 12 itens". Abra a linha para ver cada tipo de etapa uma vez, com a quantidade de vezes que ocorreu: "Usou o navegador em example.com · 7". Ela mostra o nome do site, nunca o endereço, um comando ou um arquivo.

Quando ela para para perguntar algo, a pergunta também aparece em uma linha discreta, como "Perguntou: Envio hoje ou na segunda-feira?", e sua mensagem abaixo mostra apenas sua resposta.

## O que perguntar

Antes de escrever, o chat pode sugerir até três mensagens para enviar, criadas com base nesta tarefa, como "Ofereça terça-feira às 10h em vez disso". Ao tocar em uma sugestão, ela vai para o campo de mensagem, onde você pode enviar ou alterar o texto. Quando nenhuma sugestão específica se encaixa, nenhuma aparece.

- Sobre a conversa, as pessoas ou o contexto: "O que pediram da última vez?"
- Para alterar o rascunho: "Deixe mais curto" ou "Mencione a nova data".

Uma pergunta recebe uma resposta e não altera o rascunho. Para enviar, use os botões da tarefa: o chat nunca envia um rascunho na mesma resposta em que o escreve. Uma alteração que você pedir e que não afete mais ninguém, como uma revisão em um documento, é feita na hora, sem precisar confirmar. Qualquer coisa além do que você pediu aguarda sua aprovação. Uma tarefa com mais de uma etapa continua aberta até que todas sejam concluídas.

No computador, Enter ou Ctrl+Enter (Cmd+Enter no Mac) envia a mensagem, e Shift+Enter inicia uma nova linha. No celular, use o botão de enviar.

## Quando algo está errado

Avise no chat, por exemplo: "Essa pessoa não é a CEO" ou "Ela saiu da empresa". A Machine corrige a informação na origem: um cargo, uma empresa, um título, a etapa de um projeto, o projeto da tarefa ou uma regra que aprendeu. O chat mostra o que mudou, como "Corrigido: o cargo de Sam é Head of Sales, de acordo com a assinatura do e-mail", com **Desfazer**. Desfazer restaura o valor anterior, a menos que ele tenha mudado desde então.

Seus outros rascunhos criados com base no valor incorreto são refeitos, um de cada vez. No chat deles, aparece **Refazendo o rascunho após uma correção**. Os rascunhos que você editou ou aprovou, e os que estão sendo enviados, continuam como estão. A resposta informa quantos há de cada tipo.

Em uma página do GBrain, só a seção da própria The Machine é alterada. O que você escreveu nela permanece. Quando ela não consegue identificar a origem de algo, aprende com sua observação.

## Modelo e raciocínio

Abaixo do campo de mensagem, o chat mostra o modelo e o nível de raciocínio, como "GPT-6.2 Sol" e "Raciocínio baixo". Toque em um deles para escolher outra opção, só para este chat. Os novos chats usam o que você definiu em **Configurações**, **Modelo** (veja [Modelo](model.md)).

**Rápido**, no fim do menu de modelos, faz os chats de tarefas responderem mais rápido, por cerca do dobro do custo (ou consumindo o dobro do seu plano). Isso vale para as mensagens que você envia e para **Fazer**, em todos os seus chats de tarefas, mas nunca para o trabalho em segundo plano. A opção fica desativada por padrão e esmaecida para modelos que não são compatíveis.

## Parar uma resposta

Enquanto uma resposta está sendo escrita, o botão de enviar muda para **Parar**. Parar encerra a resposta na hora e mantém o que foi escrito até então, com o status **Parada**. Escreva uma nova mensagem para continuar ou toque em **Tentar de novo**.

## Adicionar arquivos

Toque no clipe de papel, cole uma captura de tela ou arraste arquivos para o chat. Cada arquivo aparece acima do campo de mensagem, e × remove o arquivo. Uma mensagem pode conter apenas arquivos.

- Imagens (PNG, JPEG, GIF, WebP) de até 5 MB são enviadas ao modelo como imagens.
- PDFs, arquivos de texto, planilhas (CSV) e arquivos do Office de até 10 MB: A Machine lê esses arquivos e pode anexá-los a um rascunho.
- Até 5 arquivos por mensagem.

Os arquivos ficam na sua Machine, criptografados como suas mensagens. Os arquivos que você adiciona, mas nunca envia, são removidos depois de um dia. Uma nova tarefa também pode incluir arquivos, em **Nova tarefa** (veja [Criar uma tarefa](cards.md#make-one-yourself)).
