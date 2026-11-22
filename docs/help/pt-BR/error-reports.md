---
title: Relatórios de erro
area: security
summary: Quando algo dá errado, sua Machine conta à equipe da The Machine o que falhou e onde no código. Nunca envia suas mensagens, nomes ou endereços.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: e1d4d602255cde39
---
## O que é

Quando algo dá errado na The Machine, sua Machine envia à nossa equipe uma nota curta e anônima sobre o erro, para podermos corrigir antes que alguém o relate. O recurso vem ativado por padrão e precisa da [The Machine Network](/network).

## O que é enviado

Somente estas informações, para cada tipo de erro:

- o tipo de erro, como `KeyError`;
- a mensagem, sem informações específicas: números, IDs, trechos entre aspas, endereços de e-mail, links, caminhos de arquivos, chaves e qualquer palavra que possa ser um nome;
- onde o erro ocorreu no próprio código da The Machine, nunca em uma pasta do seu computador;
- a versão do app, quantas vezes aconteceu e quando ocorreu pela primeira e pela última vez.

Por exemplo: `IndexError`, `list index out of range`, em `machine/faults.py:fault_event:246`, versão `05b17ee6ac79`, 1 vez.

## O que nunca é enviado

O conteúdo das suas mensagens, tarefas, rascunhos ou chats. Nomes, endereços de e-mail, números de telefone, links ou senhas. A conta ou a pessoa envolvida.

## De onde vêm os erros

- tarefas em segundo plano: verificações de novas mensagens, preparação de tarefas, chat, conexões e sincronizações;
- o painel, no navegador ou no app, incluindo erros exibidos para você;
- solicitações do painel que falham ou excedem o tempo limite: qual solicitação foi feita, nunca o que ela enviou;
- tarefas de agentes de programação que falham: somente a ferramenta e o tipo de falha;
- o teste rápido da sua IA quando ele falha: o erro da IA, sem informações específicas.

Uma verificação interrompida porque atingiu o limite de uso do seu plano de IA não é um erro e não é enviada. Ela aguarda a renovação do limite.

Um conector que você adicionou, ou seja, seu próprio arquivo em `connectors/`, envia somente o nome do serviço e o rótulo do erro, como `notes` e `notes_http: HTTP unauthorized`, para podermos ajudar a corrigir o problema. Nenhuma outra informação do código é enviada. O cartão da conexão mostra o erro completo.

Erros repetidos são contabilizados, mas não enviados de novo. No máximo um lote é enviado a cada 10 minutos. Guardamos os relatórios por 30 dias.

## Controle de ritmo

As tarefas em segundo plano aguardam quando os limites do seu plano de IA estão perto de acabar, para deixar espaço para seus próprios chats (consulte [Seu modelo de IA](model.md)).

Com os relatórios de erro ativados, sua Machine também nos informa uma vez por dia com que frequência isso aconteceu: para cada pausa, a hora, o limite atingido, a duração e quantas tarefas aguardaram. Nada sobre o que as tarefas faziam.

## Desativar

Em **Configurações**, **Segurança**, desative **Enviar relatórios de erro**. Nada mais será registrado ou enviado, e o que estava na fila será excluído. Os erros ainda aparecem na sua Machine, que pode sugerir uma solução.

Consulte [Segurança e privacidade](security-and-privacy.md).
