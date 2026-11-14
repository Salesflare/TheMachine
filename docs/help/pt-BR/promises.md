---
title: Promessas
area: cards
summary: O que você disse que faria e o que outras pessoas prometeram. Acompanhadas automaticamente.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: dbac0241c54b0ec6
---
Acompanhe o que você prometeu e o que outras pessoas prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Em **Promessas**, na página Tarefas:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer** nas suas: ela vira uma tarefa agora, e sua Machine a prepara. **Lembrar** nas promessas de outras pessoas: sua Machine prepara um breve lembrete no canal em que fizeram a promessa, enquanto você continua na lista. Uma nota curta informa que está a caminho, com **Abrir tarefa**, e a promessa aparece como “tarefa agora”. Nada é enviado até você enviar. Se a promessa já for uma tarefa, ela abre essa tarefa.
- **Marcar como feita**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la, sem criar uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente quando chega o prazo (as suas, na manhã anterior, para você ter um dia para fazer), e aparece no dia correspondente no [Calendário](calendar.md). Se ela já for uma tarefa, haverá um link para ela, e **Marcar como feita** ou **Não vai acontecer** também fecha essa tarefa. Quando sua Machine identifica que a tarefa foi concluída, as duas são fechadas, com uma observação informando isso.

Uma promessa já cumprida, como uma resposta que você enviou ou uma reunião que deu conta dela? Ela é fechada automaticamente, sem criar uma tarefa.

Se a promessa receber uma nova data mais tarde, como “na semana que vem, então”, a mesma promessa é transferida, junto com a tarefa, sem criar outra. A página mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia para acompanhamento: três dias depois de você fazê-la ou uma semana depois de outra pessoa fazê-la. Se continuar em aberto até lá, vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

Uma promessa por e-mail de alguém para quem você nunca escreveu também é registrada, marcada como **remetente não verificado**: ela depende apenas da palavra dessa pessoa. A tarefa começa com “Não verificado: você nunca escreveu para essa pessoa antes.”

A [recapitulação semanal](weekly-recap.md) conta as promessas cumpridas e as que estão em aberto. No seu próprio computador, `assistant promises` lista essas promessas em um terminal.
