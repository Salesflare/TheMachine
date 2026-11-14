---
title: Relatórios de erro
area: security
summary: Quando algo dá errado, sua Machine informa à equipe da The Machine o que falhou e onde no código. Nunca suas mensagens, nomes ou endereços.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: fd3e1c2d68b93a35
---
## O que é

Quando algo na The Machine dá errado, sua Machine envia à nossa equipe uma nota curta e anônima sobre o erro, para que possamos corrigi-lo antes que alguém relate o problema. Isso vem ativado por padrão e precisa da [The Machine Network](/network).

## O que é enviado

Só estas informações, para cada tipo de erro:

- o tipo de erro, como `KeyError`;
- a mensagem sem informações específicas: números, IDs, trechos entre aspas, endereços de e-mail, links, caminhos de arquivos, chaves e qualquer palavra que possa ser um nome;
- onde isso aconteceu no código da própria The Machine, nunca em uma pasta do seu computador;
- a versão do app, quantas vezes aconteceu e quando aconteceu pela primeira e pela última vez.

Um exemplo real: `IndexError`, `list index out of range`, em `assistant.py:fault_event:7899`, versão `05b17ee6ac79`, 1 vez.

## O que nunca é enviado

O conteúdo das suas mensagens, tarefas, rascunhos ou chats. Nomes, endereços de e-mail, números de telefone, links ou senhas. Qual conta ou pessoa estava envolvida.

## De onde vêm os erros

- tarefas em segundo plano: verificações de novas mensagens, preparação de tarefas, chat, Conexões e sincronizações;
- o painel, no navegador ou no app, incluindo erros que ele mostrou a você;
- solicitações do painel que falham ou expiram: qual foi a solicitação, nunca o que ela enviou;
- tarefas de agentes de programação que falham: apenas a ferramenta e o tipo de falha.

Erros repetidos são contabilizados, não enviados novamente. No máximo, um lote é enviado a cada 10 minutos. Nós os mantemos por 30 dias.

## Ritmo

As tarefas em segundo plano aguardam quando os limites do seu plano de IA ficam baixos, para reservar espaço para seus próprios chats (veja [Seu modelo de IA](model.md)).

Com os relatórios de erro ativados, sua Machine também nos informa uma vez por dia com que frequência isso aconteceu: para cada pausa, a hora, qual limite, por quanto tempo e quantas tarefas ficaram aguardando. Nada sobre o que as tarefas faziam.

## Desativar

Em **Configurações**, **Segurança**, desative **Enviar relatórios de erro**. Nada mais é registrado ou enviado, e o que estava aguardando é apagado. Os erros ainda aparecem na sua própria Machine, que pode sugerir uma correção.

Veja [Segurança e privacidade](security-and-privacy.md).
