---
title: Relatórios de erro
area: security
summary: Quando algo dá errado, sua Machine informa à equipe da The Machine o que falhou e onde no código. Nunca envia suas mensagens, nomes ou endereços.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: f67d18a44999cfce
---
## O que são

Quando algo dá errado na The Machine, sua Machine envia à nossa equipe uma nota curta e anônima sobre o erro, para que possamos corrigir antes que alguém relate o problema. O envio fica ativado por padrão e precisa da [The Machine Network](/network).

## O que é enviado

Somente estas informações, para cada tipo de erro:

- o tipo de erro, como `KeyError`;
- a mensagem, sem informações específicas: números, IDs, textos entre aspas, endereços de e-mail, links, caminhos de arquivos, chaves e qualquer palavra que possa ser um nome;
- onde o erro aconteceu no próprio código da The Machine, nunca em uma pasta do seu computador;
- a versão do app, quantas vezes aconteceu e quando aconteceu pela primeira e pela última vez.

Por exemplo: `IndexError`, `list index out of range`, em `machine/faults.py:fault_event:246`, versão `05b17ee6ac79`, 1 vez.

## O que nunca é enviado

O conteúdo das suas mensagens, tarefas, rascunhos ou chats. Nomes, endereços de e-mail, números de telefone, links ou senhas. A conta ou a pessoa a que o erro se refere.

## De onde vêm os erros

- tarefas em segundo plano: verificação de novas mensagens, preparação de tarefas, chats, conexões e sincronizações;
- o painel, no navegador ou no app, incluindo erros exibidos para você;
- solicitações do painel que falham ou expiram: qual solicitação, nunca o que ela enviou;
- tarefas de agentes de programação que falham: somente a ferramenta e o tipo de falha;
- o teste rápido da sua IA quando falha: o erro da IA, sem informações específicas.

Um conector que você adicionou por conta própria (seu próprio arquivo em `connectors/`) nunca envia os erros. Eles aparecem no cartão da conexão.

Erros repetidos são contabilizados, não enviados novamente. No máximo, um lote é enviado a cada 10 minutos. Os relatórios ficam armazenados por 30 dias.

## Limites de envio

As tarefas em segundo plano aguardam quando os limites do seu plano de IA estão quase no fim, para deixar espaço para seus próprios chats (veja [Seu modelo de IA](model.md)).

Com o envio de relatórios de erro ativado, sua Machine também nos informa uma vez por dia com que frequência isso aconteceu: para cada pausa, a hora, qual limite foi atingido, quanto tempo durou e quantas tarefas aguardaram. Nada sobre o conteúdo das tarefas.

## Desativar

Em **Configurações**, **Segurança**, desative **Enviar relatórios de erro**. Nenhuma outra informação será registrada ou enviada, e os dados que estavam aguardando serão apagados. Os erros ainda aparecem na sua Machine, que pode sugerir uma correção.

Veja [Segurança e privacidade](security-and-privacy.md).
