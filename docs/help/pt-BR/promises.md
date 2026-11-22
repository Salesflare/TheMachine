---
title: Promessas
area: cards
summary: O que você disse que faria e o que prometeram a você. Acompanhe tudo automaticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 22b81ed3f7c4801f
---
Acompanhe o que você prometeu e o que prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Na página Tarefas, em **Promessas**:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer**, nas suas promessas: ela vira uma tarefa na hora, e sua Machine a prepara. **Lembrar**, nas promessas de outras pessoas: sua Machine prepara um rascunho curto de acompanhamento no mesmo lugar em que a pessoa fez a promessa, enquanto você continua na lista. Uma nota curta informa que ele está a caminho, com a opção **Abrir tarefa**, e a promessa mostra "uma tarefa agora". Nada é enviado até você enviar. Se ela já for uma tarefa, essa tarefa será aberta.
- **Marcar como feita**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la, sem criar uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente perto da data: as suas, na manhã anterior, para você ter um dia para realizá-la; as de outras pessoas, na manhã seguinte, se ainda estiverem em aberto. Ela também aparece no dia correspondente no [Calendário](calendar.md). Se já for uma tarefa, ela terá um link para essa tarefa. **Marcar como feita** ou **Não vai acontecer** também encerra a tarefa. Quando sua Machine percebe que ela foi concluída, as duas são encerradas, com uma mensagem informando isso.

A promessa já foi cumprida, como quando você enviou uma resposta ou uma reunião resolveu a questão? Ela é encerrada automaticamente, sem criar uma tarefa.

A promessa recebeu uma nova data, como "na semana que vem, em vez disso"? A mesma promessa é atualizada, assim como a tarefa, sem criar outra. A página mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia de **follow-up**: três dias depois de você fazê-la ou uma semana depois de outra pessoa fazê-la. Se continuar em aberto até lá, ela vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

Uma promessa feita por e-mail por alguém com quem você nunca trocou mensagens também é registrada, com a marca **remetente não verificado**: é apenas uma promessa dessa pessoa. A tarefa começa com "Não verificado: você nunca escreveu para essa pessoa antes."

## Reembolsos

Quando uma loja, companhia aérea, locador ou seguradora promete devolver um valor, como um reembolso por um pedido cancelado ou uma solicitação aprovada, sua Machine registra o valor, quem vai pagar e a data prevista para o recebimento. A promessa aparece em **Prometido a você**. Isso só acontece quando a mensagem deixa claros os três detalhes.

Quando o dinheiro chega primeiro, como em um e-mail dizendo "reembolso processado", uma notificação de um serviço de pagamento ou um aviso do app do banco no seu celular, a promessa é encerrada automaticamente, sem criar uma tarefa.

O dinheiro não chegou até essa data? Você recebe uma tarefa discreta: "Cobrar o reembolso de €42 de …", com um e-mail curto para a pessoa que menciona o número do pedido ou do caso. Nada é enviado até você enviar. Se o dinheiro chegar depois, a tarefa é encerrada automaticamente. **Desfazer** restaura a tarefa por um dia.

A [recapitulação semanal](weekly-recap.md) conta as promessas cumpridas e em aberto. No seu próprio computador, `assistant promises` lista as promessas em um terminal.
