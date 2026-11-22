---
title: Chat da tarefa
area: cards
summary: Pergunte sobre uma tarefa ou altere o rascunho dela em um chat vinculado a essa tarefa.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 64a15c6ce46c6679
---
## Abrir

No celular, toque no título da tarefa. No computador, clique em **Ver no chat ›** ou no link do chat da tarefa. Clicar no título no computador renomeia a tarefa.

## E-mails no chat

Cada e-mail mostra apenas o que há de novo. As mensagens anteriores citadas nele ficam recolhidas em **Mensagens anteriores**. **Ler a conversa** abre os e-mails completos.

## O que ela fez

Enquanto trabalha na sua mensagem, a etapa mais recente aparece acima dos pontos de digitação, como "Lendo o e-mail", assim como acontece na tarefa enquanto ela está sendo preparada. Quando usa o navegador, também aparece uma pequena imagem da página.

Cada execução concluída aparece em uma linha discreta, como "Verificou 12 itens". Abra a linha para ver cada tipo de etapa uma vez, com a quantidade de vezes: "Usou o navegador em example.com · 7". Ela informa o site, nunca o endereço, um comando ou um arquivo.

Quando pausa para fazer uma pergunta, ela também aparece em uma linha discreta, como "Perguntou: Envio hoje ou segunda-feira?". A mensagem seguinte mostra apenas a sua resposta.

## O que perguntar

Antes de escrever, o chat pode sugerir até três opções com base nessa tarefa, como "Ofereça terça-feira às 10h em vez disso". Toque em uma opção para colocá-la na caixa de mensagem e enviá-la ou alterá-la. Quando nenhuma opção específica se encaixa, nenhuma é exibida.

- Sobre a conversa, as pessoas ou o contexto: "O que perguntaram da última vez?"
- Para alterar o rascunho: "Deixe mais curto" ou "Mencione a nova data".

Uma pergunta recebe uma resposta sem alterar o rascunho. Para enviar, use os botões da tarefa: o chat nunca envia um rascunho na mesma resposta em que o escreveu. Uma alteração que você pede e que não chega a mais ninguém, como uma revisão em um documento, acontece na hora, sem pedir confirmação extra. Qualquer coisa além do que você pediu fica aguardando sua autorização. Uma tarefa com mais de uma etapa permanece aberta até que todas sejam concluídas.

No computador, Enter ou Ctrl+Enter (Cmd+Enter no Mac) envia a mensagem, e Shift+Enter inicia uma nova linha. No celular, use o botão de envio.

## Quando algo estiver errado

Avise no chat, por exemplo: "Essa pessoa não é a CEO" ou "Ela saiu da empresa". A Machine corrige a informação na origem: um cargo, uma empresa, um título, a etapa de um projeto, o projeto da tarefa ou uma regra que aprendeu. O chat mostra o que mudou, como "Corrigido: o cargo de Sam é Head of Sales, conforme a assinatura do e-mail", com **Desfazer**. Desfazer restaura o valor anterior, a menos que ele tenha mudado desde então.

Os outros rascunhos que usam o valor incorreto são refeitos, um de cada vez. No chat deles, aparece **Refazendo o rascunho após uma correção**. Os rascunhos que você editou ou aprovou, e os que estão sendo enviados, permanecem como estão. A resposta informa quantos há de cada tipo.

Em uma página do GBrain, só muda a seção da própria The Machine. O que você escreveu ali permanece. Quando não consegue identificar a origem de algo, ela aprende com a sua observação.

## Modelo e raciocínio

Abaixo da caixa de mensagem, o chat mostra o modelo e o nível de raciocínio, como "GPT-6.2 Sol" e "Pouco raciocínio". Toque em qualquer um deles para escolher outro, apenas para esse chat. Os novos chats usam o que você definiu em **Configurações**, **Modelo** (veja [Modelo](model.md)).

**Rápido**, no fim do menu de modelos, faz os chats de tarefas responderem mais depressa, por cerca do dobro do custo (ou consumindo o dobro do seu plano). A opção se aplica às mensagens que você envia e ao comando Fazer em todos os seus chats de tarefas, nunca ao trabalho em segundo plano. Ela fica desativada por padrão e indisponível para modelos que não oferecem esse recurso.

## Parar uma resposta

Enquanto uma resposta está sendo escrita, o botão de envio muda para **Parar**. Parar encerra a resposta na hora e mantém o que ela escreveu até então, marcado como **Parada**. Escreva uma nova mensagem para continuar ou toque em **Tentar de novo**.

## Adicionar arquivos

Toque no clipe, cole uma captura de tela ou arraste arquivos para o chat. Cada arquivo aparece acima da caixa de mensagem, e × o remove. A mensagem pode conter apenas arquivos.

- Imagens (PNG, JPEG, GIF, WebP) de até 5 MB são enviadas ao modelo como imagens.
- PDFs, arquivos de texto, planilhas (CSV) e arquivos do Office de até 10 MB: The Machine lê esses arquivos e pode anexá-los a um rascunho.
- Até 5 arquivos por mensagem.

Os arquivos ficam na sua Machine, criptografados como suas mensagens. Os arquivos que você adicionar, mas nunca enviar, são removidos após um dia. Uma nova tarefa também pode incluir arquivos, em **Nova tarefa** (veja [Criar uma tarefa](cards.md#make-one-yourself)).
