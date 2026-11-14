---
title: Promessas
area: cards
summary: O que você disse que faria e o que outras pessoas prometeram a você. Tudo é acompanhado automaticamente.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 0779d3fc9d3f3407
---
Acompanhe o que você prometeu e o que outras pessoas prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Em **Promessas**, na página de tarefas:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer** nas suas: ela vira uma tarefa, e sua Machine a prepara. **Lembrar** nas promessas de outras pessoas: sua Machine cria um rascunho de uma mensagem curta para dar seguimento, no mesmo lugar onde a pessoa fez a promessa, enquanto você continua na lista. Uma nota curta informa que a mensagem está a caminho, com **Abrir tarefa**, e a promessa aparece como "uma tarefa agora". Nada é enviado até você enviar. Se a promessa já for uma tarefa, ela abre essa tarefa.
- **Marcar como feita**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la e não cria uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente quando chega a data dela. No caso das suas promessas, isso acontece na manhã anterior, para você ter um dia para fazer a tarefa. Ela também aparece no dia correspondente no [Calendário](calendar.md). Se a promessa já for uma tarefa, ela terá um link para ela. **Marcar como feita** ou **Não vai acontecer** também fecha essa tarefa. Quando sua Machine percebe que a promessa foi cumprida, ela fecha as duas e informa isso.

Se a promessa já foi cumprida, como quando você enviou uma resposta ou uma reunião resolveu a questão, ela é fechada automaticamente, sem criar uma tarefa.

Se uma nova data for combinada depois, como em "na semana que vem, então", a mesma promessa é atualizada, assim como a tarefa, sem criar outra. A página da promessa mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia para acompanhamento: três dias depois de você fazê-la ou uma semana depois de outra pessoa fazê-la. Se ainda estiver em aberto nessa data, ela vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

O [resumo semanal](weekly-recap.md) contabiliza as promessas cumpridas e em aberto. No seu próprio computador, `assistant promises` mostra uma lista delas no terminal.
