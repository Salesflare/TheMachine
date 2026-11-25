---
title: Chat da tarefa
area: cards
summary: Pergunte sobre uma tarefa ou altere o rascunho no chat vinculado a ela.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 18a428fbe38a70e7
---
## Abrir

Toque em **Chat** na tarefa ou selecione-a na lista da barra lateral. Toque ou clique no título para editá-lo.

## E-mails no chat

Cada e-mail mostra apenas o que há de novo. As mensagens anteriores citadas ficam recolhidas em **Mensagens anteriores**. **Ler a conversa** abre os e-mails completos.

## O que ela fez

Enquanto trabalha, **Trabalhando nisso…** aparece acima da caixa de mensagem, e pontos de digitação aparecem no chat. Quando ela usa o navegador, também aparece uma imagem pequena da página.

O que acontece em cada execução aparece em uma única linha discreta, com uma contagem progressiva, como "Verificou 12 itens". Abra a linha para ver cada tipo de etapa uma vez, junto com o número de vezes que ocorreu: "Usou o navegador em example.com · 7". Ela indica o site, nunca o endereço, um comando ou um arquivo.

Com Claude Code, as etapas não aparecem no chat enquanto ela trabalha. A etapa mais recente aparece acima dos pontos de digitação, como "Lendo o e-mail", e não aparece nada acima da caixa de mensagem.

Quando ela para para perguntar algo, a pergunta também aparece em uma linha discreta, como "Perguntou: Envio hoje ou na segunda?", e sua mensagem logo abaixo mostra apenas a sua resposta.

## O que perguntar

Antes de você escrever, o chat pode sugerir até três opções com base na tarefa, como "Ofereça terça-feira às 10h em vez disso". Ao tocar em uma opção, ela aparece na caixa de mensagem para você enviar ou alterar. Se nenhuma sugestão específica for adequada, nenhuma aparece.

- Sobre a conversa, as pessoas ou o contexto: "O que pediram da última vez?"
- Para alterar o rascunho: "Deixe mais curto" ou "Mencione a nova data".

Uma pergunta recebe uma resposta e não altera o rascunho. Para enviar, use os botões da tarefa: o chat nunca envia um rascunho na mesma resposta em que o escreveu. Uma alteração que você pedir e que não chegue a mais ninguém, como uma correção em um documento, é feita na hora, sem precisar confirmar. Qualquer coisa além do que você pediu fica aguardando sua aprovação. Uma tarefa com mais de uma etapa permanece aberta até que todas sejam concluídas.

No computador, Enter ou Ctrl+Enter (Cmd+Enter no Mac) envia a mensagem, e Shift+Enter inicia uma nova linha. No celular, use o botão de envio.

## Quando algo estiver errado

Avise no chat, por exemplo: "Essa pessoa não é a CEO" ou "Ela saiu da empresa". A Machine corrige a informação na origem: um cargo, uma empresa, um título, a etapa de um projeto, o projeto da tarefa ou uma regra que aprendeu. O chat mostra o que mudou, como "Corrigido: Sam é Diretor de Vendas, segundo a assinatura de e-mail", com **Desfazer**. Desfazer restaura o valor anterior, a menos que ele tenha mudado desde então.

Os outros rascunhos baseados no valor incorreto são gerados novamente, um por vez. No chat deles, aparece **Refazendo o rascunho após uma correção**. Rascunhos que você editou ou aprovou, e os que estão sendo enviados, permanecem como estão. A resposta informa quantos há de cada tipo.

Em uma página do GBrain, só muda a seção da própria The Machine. O que você escreveu ali permanece. Quando ela não consegue identificar a origem de algo, aprende com sua observação.

## Modelo e raciocínio

Abaixo da caixa de mensagem, o chat mostra o modelo e o nível de raciocínio, como "GPT-6.2 Sol" e "Raciocínio baixo". Toque em qualquer um dos dois para escolher outro apenas para este chat. Novos chats usam as opções definidas em **Configurações**, **Modelo** (veja [Modelo](model.md)).

**Rápido**, no fim do menu de modelos, faz os chats de tarefas responderem mais rápido, por cerca do dobro do custo (ou consumindo o dobro do seu plano). Isso vale para as mensagens que você envia e para **Fazer**, em todos os chats de tarefas, nunca para o trabalho em segundo plano. O recurso fica desativado por padrão e aparece em cinza nos modelos que não o oferecem.

## Parar uma resposta

Enquanto uma resposta está sendo escrita, o botão de envio muda para **Parar**. Ao parar, a resposta é encerrada na hora e o que ela escreveu até então é mantido, com a indicação **Parada**. Escreva uma nova mensagem para continuar ou toque em **Tentar de novo**.

## Adicionar arquivos

Toque no clipe, cole uma captura de tela ou arraste arquivos para o chat. Cada arquivo aparece acima da caixa de mensagem, e × o remove. A mensagem pode conter apenas arquivos.

- Imagens (PNG, JPEG, GIF, WebP) de até 5 MB são enviadas ao modelo como imagens.
- PDFs, arquivos de texto, planilhas (CSV) e arquivos do Office de até 10 MB: The Machine lê esses arquivos e pode anexá-los a um rascunho.
- Até 5 arquivos por mensagem.

Os arquivos ficam na sua Machine, criptografados como suas mensagens. Os arquivos que você adicionar, mas nunca enviar, são removidos depois de um dia. Uma nova tarefa também pode incluir arquivos, em **Nova tarefa** (veja [Criar uma por conta própria](cards.md#make-one-yourself)).
