---
title: Promessas
area: cards
summary: O que você disse que faria e o que outras pessoas prometeram a você. Acompanhe tudo automaticamente.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: ba0e2190e1b8b791
---
Acompanhe o que você prometeu e o que outras pessoas prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Na página Tarefas, em **Promessas**:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer** nas suas promessas: ela vira uma tarefa na hora, e sua Machine a prepara. **Lembrar** nas promessas de outras pessoas: sua Machine prepara um follow-up curto no lugar onde a pessoa fez a promessa, enquanto você continua na lista. Uma nota curta diz que ele está a caminho, com **Abrir tarefa**, e a promessa mostra "uma tarefa agora". Nada é enviado até você enviar. Se a promessa já for uma tarefa, ela abre essa tarefa.
- **Marcar como feito**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la, sem criar uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente perto da data prevista (as suas, na manhã anterior, para você ter um dia para cumprir; as de outras pessoas, na manhã seguinte, se ainda estiverem em aberto) e aparece no dia correspondente no [Calendário](calendar.md). Se já tiver virado uma tarefa, ela terá um link para a tarefa, e **Marcar como feito** ou **Não vai acontecer** também fecha essa tarefa. Quando sua Machine identifica que a promessa foi cumprida, as duas são fechadas, com uma observação informando isso.

Uma resposta que apenas promete o trabalho, como "Vou enviar os arquivos até terça-feira", não conclui a tarefa. A tarefa continua em aberto com essa data, e a promessa fica vinculada a ela. A revisão do envio informa isso antes de você enviar.

Se a promessa já tiver sido cumprida, por exemplo, com uma resposta que você enviou ou em uma reunião que resolveu o assunto, ela é fechada automaticamente, sem criar uma tarefa.

Quando alguém responde a uma promessa que fez, ela continua em aberto até a resposta indicar que foi cumprida. Um "Claro", uma resposta automática ou o cumprimento de apenas parte da promessa não contam. Se um lembrete estiver prestes a ser enviado, ele é cancelado, e a tarefa continua em aberto com a indicação "A pessoa escreveu de novo".

Se a pessoa informar uma nova data posterior, como "melhor deixar para a semana que vem", a mesma promessa é atualizada, assim como a tarefa, sem criar outra. A página da promessa mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia de **follow-up**: três dias depois de você fazê-la ou uma semana depois de outra pessoa fazê-la. Se ainda estiver em aberto nessa data, vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

As promessas por e-mail de alguém com quem você nunca escreveu também são acompanhadas, com a indicação **remetente não verificado**: elas se baseiam apenas na palavra dessa pessoa. A tarefa começa com "Não verificado: você nunca escreveu para essa pessoa antes."

## Reembolsos

Quando uma loja, companhia aérea, proprietário ou seguradora promete devolver seu dinheiro, como no caso de um pedido cancelado ou de uma solicitação aprovada, sua Machine registra o valor, quem vai pagar e a data prevista para o pagamento. A promessa aparece em **Prometido a você**. Isso só acontece quando a mensagem deixa claras as três informações.

Se o dinheiro voltar primeiro, por exemplo, com um e-mail informando que o "reembolso foi processado", uma notificação de um serviço de pagamento ou um aviso do app do banco no seu celular, a promessa é fechada automaticamente, sem criar uma tarefa.

O dinheiro ainda não chegou nessa data? Você recebe uma tarefa discreta: "Cobrar o reembolso de €42 de …", com um e-mail curto para a pessoa ou empresa, mencionando o número do pedido ou do caso. Nada é enviado até você enviar. Se o dinheiro chegar depois, a tarefa é fechada automaticamente. **Desfazer** restaura a tarefa por um dia.

O [resumo semanal](weekly-recap.md) contabiliza as promessas cumpridas e em aberto. No seu próprio computador, `assistant promises` lista essas promessas no terminal.
