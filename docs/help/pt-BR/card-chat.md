---
title: Chat da tarefa
area: cards
summary: Pergunte sobre uma tarefa ou altere o rascunho dela em um chat vinculado a essa tarefa.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 224f6163a84e80ca
---
## Abrir

Toque em **Chat** na tarefa ou escolha-a na lista da barra lateral. Toque ou clique no título para editá-lo.

## E-mails no chat

Cada e-mail mostra apenas o que há de novo nele. As mensagens anteriores que ele cita ficam recolhidas em **Mensagens anteriores**. **Ler a conversa** abre os e-mails na íntegra.

## O que ela fez

Enquanto trabalha na sua mensagem, a etapa mais recente aparece acima dos indicadores de digitação, como “Lendo o e-mail”, assim como acontece na tarefa enquanto a assistente se prepara. Quando usa o navegador, uma pequena imagem da página também aparece.

Cada execução concluída aparece em uma linha discreta, como “Verificou 12 itens”. Abra-a para ver cada tipo de etapa uma vez, com a quantidade de vezes que ocorreu: “Usou o navegador em example.com · 7”. Ela mostra o nome do site, nunca o endereço, um comando ou um arquivo.

Quando ela para para fazer uma pergunta, a pergunta também aparece em uma linha discreta, como “Perguntou: Envio hoje ou na segunda?”, e sua mensagem abaixo mostra apenas a sua resposta.

## O que perguntar

Antes de você escrever, o chat pode oferecer até três sugestões clicáveis baseadas nesta tarefa, como “Ofereça terça-feira às 10h em vez disso”. Ao tocar em uma delas, o texto vai para a caixa de mensagem, onde você pode enviá-lo ou alterá-lo. Quando não há nenhuma sugestão específica, nenhuma aparece.

- Sobre a conversa, as pessoas ou o contexto: “O que pediram da última vez?”
- Para alterar o rascunho: “Deixe mais curto” ou “Mencione a nova data”.

Uma pergunta recebe uma resposta e não altera o rascunho. O envio é feito pelos botões da tarefa: o chat nunca envia um rascunho na mesma resposta em que o criou. Uma alteração que você pedir e que não afete mais ninguém, como uma revisão em um documento, é feita na hora, sem pedir uma confirmação extra. Qualquer coisa além do que você pediu aguarda sua aprovação. Uma tarefa com mais de uma etapa continua aberta até que todas sejam concluídas.

No computador, Enter ou Ctrl+Enter (Cmd+Enter no Mac) envia a mensagem, e Shift+Enter inicia uma nova linha. No celular, use o botão de envio.

## Quando algo está errado

Avise no chat, por exemplo: “Eles não são o CEO” ou “Eles saíram da empresa”. A Machine corrige o dado na origem: um cargo, uma empresa, um título, a etapa de um projeto, o projeto da tarefa ou uma regra que aprendeu. O chat mostra o que mudou, como “Corrigido: o cargo de Sam é Diretor de vendas, conforme a assinatura de e-mail”, com **Desfazer**. Desfazer restaura o valor anterior, a menos que ele tenha mudado desde então.

Os outros rascunhos baseados no valor incorreto são refeitos, um de cada vez. O chat deles mostra **Refazendo o rascunho após uma correção**. Os rascunhos que você editou ou aprovou, e os que estão sendo enviados, continuam como estão. A resposta informa quantos há de cada tipo.

Em uma página do GBrain, só a seção da própria The Machine muda. O que você escreveu nela permanece. Quando ela não consegue identificar a origem de algo, aprende com sua observação.

## Modelo e raciocínio

Abaixo da caixa de mensagem, o chat mostra o modelo e o nível de raciocínio, como “GPT-6.2 Sol” e “Raciocínio baixo”. Toque em um deles para escolher outro, apenas para esse chat. Os novos chats usam o que você definiu em **Configurações**, **Modelo** (consulte [Modelo](model.md)).

**Rápido**, no fim do menu de modelos, faz os chats de tarefas responderem mais rápido, por cerca do dobro do custo (ou consome o dobro do seu plano). Isso vale para as mensagens que você envia e para Fazer, em todos os seus chats de tarefas, nunca para o trabalho em segundo plano. A opção fica desativada por padrão e esmaecida nos modelos que não oferecem esse recurso.

## Interromper uma resposta

Enquanto uma resposta está sendo escrita, o botão de envio muda para **Parar**. Parar encerra a resposta na hora e mantém o que foi escrito até então, marcado como **Parada**. Escreva uma nova mensagem para continuar ou toque em **Tentar de novo**.

## Adicionar arquivos

Toque no clipe, cole uma captura de tela ou arraste arquivos para o chat. Cada arquivo aparece acima da caixa de mensagem, e × o remove. A mensagem pode conter apenas arquivos.

- Imagens (PNG, JPEG, GIF, WebP) de até 5 MB são enviadas ao modelo como imagens.
- PDFs, arquivos de texto, planilhas (CSV) e arquivos do Office de até 10 MB: a The Machine lê esses arquivos e pode anexá-los a um rascunho.
- Até 5 arquivos por mensagem.

Os arquivos ficam na sua Machine, criptografados como suas mensagens. Os arquivos que você adiciona, mas não envia, são removidos depois de um dia. Uma nova tarefa também pode incluir arquivos, em **Nova tarefa** (consulte [Crie uma tarefa por conta própria](cards.md#make-one-yourself)).
