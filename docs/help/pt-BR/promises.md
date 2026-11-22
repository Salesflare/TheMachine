---
title: Promessas
area: cards
summary: O que você disse que faria e o que prometeram a você. Tudo acompanhado automaticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Acompanhe o que você prometeu e o que prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Em **Promessas**, na página de tarefas:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer**, nas suas promessas: ela vira uma tarefa na hora, e sua Machine a prepara. **Lembrar**, nas promessas de outras pessoas: sua Machine prepara um lembrete curto no lugar onde a pessoa fez a promessa, enquanto você continua na lista. Uma nota curta informa que está a caminho, com **Abrir tarefa**, e a promessa mostra “tarefa criada”. Nada é enviado até você enviar. Se já for uma tarefa, ela abre.
- **Marcar como feita**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la, sem criar uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente perto da data combinada: as suas, na manhã anterior, para você ter um dia para cumprir; as de outras pessoas, na manhã seguinte, se ainda estiverem em aberto. Ela também aparece no dia correspondente no [Calendário](calendar.md). Se já for uma tarefa, a promessa terá um link para ela. **Marcar como feita** ou **Não vai acontecer** também encerra a tarefa. Quando sua Machine identifica que ela foi cumprida, as duas são encerradas, com uma mensagem informando isso.

Uma resposta que só promete que o trabalho será feito, como “Envio os arquivos até terça-feira”, não conclui a tarefa. Ela continua em aberto com essa data, e a promessa tem um link para ela. A revisão do envio informa isso antes de você enviar.

Se a promessa já foi cumprida, como em uma resposta que você enviou ou em uma reunião que resolveu a questão, ela é encerrada automaticamente, sem criar uma tarefa.

Se a pessoa der uma nova data depois, como “melhor na semana que vem”, a mesma promessa é atualizada, assim como a tarefa. Não é criada uma segunda tarefa. A página da promessa mostra a nova data e a mensagem mais recente.

Promessas sem data recebem um dia para **acompanhamento**: três dias depois de você fazer a promessa, ou uma semana depois de outra pessoa fazê-la. Se ainda estiverem em aberto nesse dia, viram uma tarefa.

As promessas do Slack mostram o nome da pessoa.

Promessas recebidas por e-mail de alguém com quem você nunca trocou mensagens também são registradas, com a indicação **remetente não verificado**: só temos a palavra dessa pessoa. A tarefa começa com “Não verificado: você nunca escreveu para essa pessoa.”

## Reembolsos

Quando uma loja, companhia aérea, proprietário ou seguradora promete devolver seu dinheiro, como no caso de um reembolso por um pedido cancelado ou de uma solicitação aprovada, sua Machine registra o valor, quem vai pagar e a data prevista. A promessa aparece em **Prometido a você**. Isso só acontece quando a mensagem deixa os três pontos claros.

Se o dinheiro voltar primeiro, por exemplo, com um e-mail informando que o reembolso foi processado, um aviso do serviço de pagamento ou uma notificação do app do banco no seu celular, a promessa é encerrada automaticamente, sem criar uma tarefa.

Se o dinheiro não chegar até essa data, você recebe uma tarefa discreta: “Cobrar o reembolso de €42 de …”, com um e-mail curto para a pessoa que menciona o número do pedido ou do caso. Nada é enviado até você enviar. Se o dinheiro chegar depois, a tarefa é encerrada automaticamente. **Desfazer** reabre a tarefa por um dia.

A [recapitulação semanal](weekly-recap.md) conta as promessas cumpridas e as que continuam em aberto. No seu próprio computador, `assistant promises` lista as promessas no terminal.
