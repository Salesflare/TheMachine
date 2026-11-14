---
title: Relatórios de erro
area: security
summary: Quando algo dá errado, sua Machine informa à equipe do The Machine o que falhou e onde no código. Nunca envia suas mensagens, nomes ou endereços.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 03a8649f2f634b59
---
## O que é

Quando algo dá errado no The Machine, sua Machine envia à nossa equipe uma nota curta e anônima sobre o erro, para que possamos corrigir antes que alguém precise avisar. O recurso vem ativado por padrão e precisa da [The Machine Network](/network).

## O que é enviado

Somente estas informações, para cada tipo de erro:

- o tipo de erro, como `KeyError`;
- a mensagem, sem informações específicas: números, IDs, trechos entre aspas, endereços de e-mail, links, caminhos de arquivos, chaves e qualquer palavra que possa ser um nome;
- onde o erro aconteceu no próprio código do The Machine, nunca em uma pasta do seu computador;
- a versão do app, quantas vezes aconteceu e quando aconteceu pela primeira e pela última vez.

Por exemplo: `IndexError`, `list index out of range`, em `machine/faults.py:fault_event:246`, versão `05b17ee6ac79`, 1 vez.

## O que nunca é enviado

O conteúdo das suas mensagens, tarefas, rascunhos ou chats. Nomes, endereços de e-mail, números de telefone, links ou senhas. A conta ou pessoa a que o erro se referia.

## De onde vêm os erros

- tarefas em segundo plano: verificações de novas mensagens, preparação de tarefas, chats, conexões e sincronizações;
- o painel, no navegador ou no app, incluindo erros que ele mostrou a você;
- solicitações do painel que falham ou atingem o tempo limite: qual solicitação falhou, nunca o que ela enviou;
- tarefas de agentes de programação que falham: somente a ferramenta e o tipo de falha.

Erros repetidos são contabilizados, mas não são enviados novamente. No máximo, um lote é enviado a cada 10 minutos. Guardamos os relatórios por 30 dias.

## Intervalo entre tarefas

As tarefas em segundo plano aguardam quando os limites do seu plano de IA estão perto de acabar, para deixar espaço para seus próprios chats (consulte [Seu modelo de IA](model.md)).

Com os relatórios de erro ativados, sua Machine também nos informa uma vez por dia quantas vezes isso aconteceu: para cada pausa, a hora, o limite atingido, quanto tempo durou e quantas tarefas aguardaram. Nada sobre o conteúdo das tarefas.

## Desativar

Em **Configurações**, **Segurança**, desative **Enviar relatórios de erro**. Nada mais será registrado nem enviado, e o que estiver aguardando será excluído. Os erros ainda aparecem na sua própria Machine, que pode sugerir uma correção.

Consulte [Segurança e privacidade](security-and-privacy.md).
