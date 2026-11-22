---
title: Promessas
area: cards
summary: O que você prometeu e o que outras pessoas prometeram a você. Tudo acompanhado automaticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Acompanhe o que você prometeu e o que outras pessoas prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Na página Tarefas, em **Promessas**:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer**, nas suas: ela vira uma tarefa na hora, e sua Machine a prepara. **Lembrar**, nas promessas de outras pessoas: sua Machine prepara um follow-up curto no mesmo lugar em que a pessoa fez a promessa, enquanto você continua na lista. Uma notificação curta avisa que está a caminho, com **Abrir tarefa**, e a promessa mostra "uma tarefa agora". Nada é enviado até você enviar. Se a promessa já for uma tarefa, essa tarefa é aberta.
- **Marcar como feita**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la, sem criar uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente perto da data: as suas, na manhã anterior, para você ter um dia para cumprir; as de outras pessoas, na manhã seguinte, se ainda estiverem em aberto. Ela também aparece na data correspondente no [Calendário](calendar.md). Se a promessa já virou tarefa, ela leva até essa tarefa. **Marcar como feita** ou **Não vai acontecer** também encerra a tarefa. Quando sua Machine identifica que a promessa foi cumprida, os dois itens são encerrados, com uma mensagem informando isso.

Uma resposta que apenas promete fazer o trabalho, como "Vou enviar os arquivos até terça-feira", não conclui a tarefa. Ela continua em aberto com essa data, e a promessa fica vinculada a ela. A revisão do envio informa isso antes de você enviar.

Se a promessa já tiver sido cumprida, como em uma resposta que você enviou ou em uma reunião que tratou do assunto, ela é encerrada automaticamente, sem criar uma tarefa.

Se a pessoa informar uma nova data depois, como "melhor deixar para a semana que vem", a mesma promessa e a tarefa correspondente são adiadas, sem criar outra tarefa. A página mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia de follow-up: três dias depois de você fazer a promessa ou uma semana depois de outra pessoa fazê-la. Se ainda estiver em aberto nessa data, vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

Uma promessa recebida por e-mail de alguém para quem você nunca escreveu também é acompanhada, com a marca **remetente não verificado**: ela se baseia apenas no que a pessoa diz. A tarefa começa com "Não verificado: você ainda não escreveu para essa pessoa."

## Reembolsos

Quando uma loja, companhia aérea, locador ou seguradora promete devolver seu dinheiro, como em um reembolso por um pedido cancelado ou uma indenização aprovada, sua Machine registra o valor, quem vai pagar e a data prevista para o pagamento. A promessa aparece em **Prometido a você**. Isso só acontece quando a mensagem deixa os três pontos claros.

Se o dinheiro voltar antes, por exemplo, com um e-mail informando que o "reembolso foi processado", um aviso do serviço de pagamento ou uma notificação do app do seu banco no celular, a promessa é encerrada automaticamente, sem criar uma tarefa.

Se o dinheiro não chegar até essa data, aparece uma tarefa discreta: "Cobrar o reembolso de €42 de …", com um e-mail curto para a pessoa que menciona o número do pedido ou do caso. Nada é enviado até você enviar. Se o dinheiro acabar chegando, a tarefa é encerrada automaticamente. **Desfazer** reabre a tarefa por um dia.

O [Resumo semanal](weekly-recap.md) contabiliza as promessas cumpridas e em aberto. No seu próprio computador, `assistant promises` lista as promessas no terminal.
