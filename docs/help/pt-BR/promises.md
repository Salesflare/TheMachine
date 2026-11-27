---
title: Promessas
area: cards
summary: O que você disse que faria e o que outras pessoas prometeram a você. Acompanhe tudo automaticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: b624394de7ff77b1
---
Acompanhe o que você prometeu e o que outras pessoas prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Em **Promessas**, na página Tarefas:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer** nas suas: ela vira uma tarefa na hora, e sua Machine a prepara. **Lembrar** nas delas: sua Machine prepara um follow-up curto no lugar em que fizeram a promessa, enquanto você continua na lista. Uma nota curta avisa que ele está a caminho, com **Abrir tarefa**, e a promessa mostra "uma tarefa agora". Nada é enviado até você enviar. Se ela já for uma tarefa, abre essa tarefa.
- **Marcar como feito**: a promessa foi cumprida.
- **Não vai acontecer**: não vai acontecer, então sua Machine para de acompanhar a promessa, sem criar uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente perto da data: as suas, na manhã anterior, para você ter um dia para fazer; as delas, na manhã seguinte, se ainda estiverem em aberto. Ela também aparece no dia correspondente no [Calendário](calendar.md). Se já for uma tarefa, ela leva até essa tarefa. **Marcar como feito** ou **Não vai acontecer** também encerra essa tarefa. Quando sua Machine percebe que ela foi concluída, as duas são encerradas, com uma mensagem informando isso.

Uma resposta que só promete fazer o trabalho, como "Vou enviar os arquivos até terça-feira", não conclui a tarefa. A tarefa continua em aberto com essa data, e a promessa fica vinculada a ela. A revisão do envio avisa isso antes de você enviar. Se você mudar o texto primeiro, a promessa antiga e a data são removidas: a tarefa continua em aberto até sua Machine perceber que o trabalho foi concluído, e uma promessa na mensagem enviada é vinculada a ela.

Já foi cumprida, como uma resposta que você enviou ou algo resolvido em uma reunião? Ela é encerrada automaticamente, sem criar uma tarefa.

Quando alguém responde a uma promessa que fez, ela continua em aberto até a resposta mostrar que foi cumprida. Um "Claro" ou o cumprimento de apenas parte dela não conta. Se um lembrete estiver prestes a ser enviado, ele é cancelado e a tarefa continua em aberto com a indicação "A pessoa escreveu de novo". Uma resposta automática de ausência não muda nada.

A pessoa informou uma nova data, como "na semana que vem, então"? A mesma promessa é atualizada, assim como a tarefa, sem criar outra. A página dela mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia de **follow-up**: três dias depois de você fazê-la, ou uma semana depois de outra pessoa fazê-la. Se ainda estiver em aberto nessa data, vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

Uma promessa por e-mail de alguém com quem você nunca trocou mensagens também é registrada, marcada como **remetente não verificado**: é apenas a palavra da pessoa. A tarefa começa com "Não verificado: você ainda não escreveu para essa pessoa."

## Reembolsos

Quando uma loja, companhia aérea, proprietário ou seguradora promete devolver seu dinheiro, como um reembolso por um pedido cancelado ou uma solicitação aprovada, sua Machine registra o valor, quem vai pagar e a data prevista para o pagamento. A promessa aparece em **Prometido a você**. Isso só acontece quando a mensagem deixa os três pontos claros.

Se o dinheiro voltar primeiro, como em um e-mail dizendo "reembolso processado", uma notificação de um serviço de pagamento ou um aviso do app do seu banco no celular, a promessa é encerrada automaticamente, sem criar uma tarefa.

O dinheiro não chegou até essa data? Uma tarefa discreta é criada: "Cobrar o reembolso de €42 de …", com um e-mail curto para a pessoa ou empresa, mencionando o número do pedido ou do caso. Nada é enviado até você enviar. Se o dinheiro chegar depois, a tarefa é encerrada automaticamente. **Desfazer** restaura a tarefa por um dia.

A [recapitulação semanal](weekly-recap.md) conta as promessas cumpridas e em aberto. No seu próprio computador, `assistant promises` lista essas promessas em um terminal.
