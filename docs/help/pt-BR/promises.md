---
title: Promessas
area: cards
summary: O que você prometeu fazer e o que prometeram a você. Acompanhe tudo automaticamente.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: dbac0241c54b0ec6
---
Acompanhe o que você prometeu fazer e o que prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Na página de tarefas, em **Promessas**:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer** nas suas: ela vira uma tarefa na hora, e sua Machine a prepara. **Lembrar** nas promessas de outras pessoas: sua Machine cria um rascunho curto de acompanhamento no lugar onde a pessoa fez a promessa, enquanto você continua na lista. Uma nota curta informa que a mensagem está a caminho, com **Abrir tarefa**, e a promessa aparece como "uma tarefa agora". Nada é enviado até você enviar. Se ela já for uma tarefa, essa tarefa será aberta.
- **Marcar como feita**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la, sem criar uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente quando vence (as suas, na manhã anterior, para você ter um dia para fazer), e aparece no dia correspondente na [Agenda](calendar.md). Se ela já for uma tarefa, terá um link para ela. **Marcar como feita** ou **Não vai acontecer** também fecha essa tarefa. Quando sua Machine percebe que a promessa foi cumprida, ela fecha as duas e informa isso.

A promessa já foi cumprida, como uma resposta que você enviou ou uma reunião que resolveu a questão? Ela é fechada automaticamente, sem criar uma tarefa.

A promessa ganhou uma nova data, como em "na semana que vem, em vez disso"? A mesma promessa é adiada, assim como a tarefa, sem criar outra. A página dela mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia de **acompanhamento**: três dias depois de você ter feito a promessa ou uma semana depois de outra pessoa ter feito. Se ainda estiver em aberto nessa data, ela vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

Uma promessa por e-mail de alguém com quem você nunca escreveu também é registrada, com a indicação **remetente não verificado**: ela se baseia apenas na palavra dessa pessoa. A tarefa começa com "Não verificado: você nunca escreveu para essa pessoa antes."

O [resumo semanal](weekly-recap.md) contabiliza as promessas cumpridas e em aberto. No seu próprio computador, `assistant promises` as lista em um terminal.
