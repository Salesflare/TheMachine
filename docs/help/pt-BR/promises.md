---
title: Promessas
area: cards
summary: O que você disse que faria e o que prometeram a você. Acompanhe tudo automaticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 0bc6594bbd8f4c0b
---
Acompanhe o que você prometeu e o que prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Na seção **Promessas**, na página Tarefas:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer**, nas suas promessas: ela vira uma tarefa na hora, e sua Machine a prepara. **Lembrar**, nas promessas de outras pessoas: sua Machine prepara um follow-up curto no mesmo canal em que a pessoa fez a promessa, sem tirar você da lista. Uma nota curta informa que ele está a caminho, com a opção **Abrir tarefa**, e a promessa mostra “agora é uma tarefa”. Nada é enviado até você enviar. Se a promessa já for uma tarefa, ela abre essa tarefa.
- **Marcar como feito**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la, sem criar uma tarefa.

Uma promessa em aberto também vira tarefa automaticamente perto da data: as suas, na manhã anterior, para você ter um dia para cumpri-las; as de outras pessoas, na manhã seguinte, se ainda estiverem em aberto. Ela também aparece no dia correspondente no [Calendário](calendar.md). Se já for uma tarefa, ela leva até essa tarefa, e **Marcar como feito** ou **Não vai acontecer** também a fecha. Quando sua Machine percebe que a promessa foi cumprida, fecha as duas e informa isso.

Uma resposta que só promete fazer o trabalho, como “Vou enviar os arquivos até terça-feira”, não conclui a tarefa. A tarefa continua em aberto com essa data, e a promessa fica vinculada a ela. A revisão do envio informa isso antes de você enviar.

Se a promessa já foi cumprida, como quando você enviou uma resposta ou uma reunião resolveu a questão, ela é fechada automaticamente, sem criar uma tarefa.

Quando alguém responde a uma promessa que fez, ela continua em aberto até que a resposta mostre que foi cumprida. Um “Claro” ou o cumprimento de apenas parte da promessa não conta. Se havia um lembrete prestes a ser enviado, ele é cancelado, e a tarefa continua em aberto com a indicação “A pessoa escreveu novamente”. Uma resposta automática de ausência não muda nada.

Se a pessoa der uma nova data, como “melhor deixar para a semana que vem”, a mesma promessa é remarcada, assim como a tarefa. Não é criada uma segunda tarefa. A página da promessa mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia de **follow-up**: três dias depois de você fazê-la ou uma semana depois de outra pessoa fazê-la. Se ainda estiver em aberto nessa data, ela vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

Uma promessa por e-mail de alguém com quem você nunca trocou mensagens também é registrada, marcada como **remetente não verificado**: é só a palavra dessa pessoa. A tarefa começa com “Não verificado: você nunca escreveu para essa pessoa”.

## Reembolsos

Quando uma loja, companhia aérea, proprietário ou seguradora promete devolver dinheiro, como um reembolso por um pedido cancelado ou uma indenização aprovada, sua Machine registra o valor, quem vai pagar e a data prevista para o dinheiro chegar. A promessa aparece em **Prometido a você**. Isso só acontece quando a mensagem deixa claros os três dados.

Se o dinheiro chegar antes, como quando você recebe um e-mail dizendo que o “reembolso foi processado”, um aviso de um serviço de pagamento ou uma notificação do app do banco no celular, a promessa é fechada automaticamente, sem criar uma tarefa.

O dinheiro não chegou até essa data? Uma única tarefa discreta aparece: “Cobrar o reembolso de €42 de …”, com um e-mail curto para a empresa mencionando o número do pedido ou do caso. Nada é enviado até você enviar. Se o dinheiro chegar depois, a tarefa é fechada automaticamente. **Desfazer** a reabre por um dia.

O [resumo semanal](weekly-recap.md) conta as promessas cumpridas e as que continuam em aberto. No seu próprio computador, `assistant promises` lista as promessas no terminal.
