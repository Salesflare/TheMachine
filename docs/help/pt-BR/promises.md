---
title: Promessas
area: cards
summary: O que você disse que faria e o que outras pessoas prometeram a você. Tudo acompanhado automaticamente.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 8e5ce7b371ab7fd0
---
Acompanhe o que você prometeu e o que outras pessoas prometeram a você. Sua Machine identifica promessas nas suas mensagens automaticamente.

## Onde encontrar

Na página de tarefas, em **Promessas**:

- O que você disse que faria e para quem: **Você prometeu**.
- O que outras pessoas disseram que fariam: **Prometido a você**.

Cada promessa tem um menu **⋯**:

- **Fazer** nas suas promessas: ela vira uma tarefa na hora, e sua Machine a prepara. **Lembrar** nas promessas de outras pessoas: sua Machine cria um rascunho de mensagem curta para acompanhar a promessa, no mesmo lugar onde ela foi feita, enquanto você continua na lista. Uma nota curta informa que a mensagem está a caminho, com a opção **Abrir tarefa**, e a promessa mostra "uma tarefa agora". Nada é enviado até você enviar. Se ela já for uma tarefa, essa tarefa será aberta.
- **Marcar como feita**: a promessa foi cumprida.
- **Não vai acontecer**: a promessa não será cumprida, então sua Machine para de acompanhá-la, sem criar uma tarefa.

Uma promessa em aberto também vira uma tarefa automaticamente perto da data prevista (as suas, na manhã anterior, para você ter um dia para cumpri-las; as de outras pessoas, na manhã seguinte, se ainda estiverem em aberto) e aparece na data correspondente no [Calendário](calendar.md). Se a promessa já virou tarefa, há um link para ela, e **Marcar como feita** ou **Não vai acontecer** também encerra essa tarefa. Quando sua Machine percebe que a promessa foi cumprida, as duas são encerradas, com uma mensagem informando isso.

A promessa já foi cumprida, como no caso de uma resposta que você enviou ou de uma reunião que resolveu a questão? Ela é encerrada automaticamente, sem criar uma tarefa.

A promessa recebeu uma nova data depois, como "na próxima semana, então"? A mesma promessa é atualizada, assim como a tarefa, sem criar outra. A página dela mostra a nova data e a mensagem mais recente.

Uma promessa sem data recebe um dia para acompanhamento: três dias depois de você criá-la, ou uma semana depois de outra pessoa criá-la. Se ainda estiver em aberto nessa data, vira uma tarefa.

As promessas do Slack mostram o nome da pessoa.

Uma promessa por e-mail de alguém com quem você nunca escreveu também é registrada, com a marca **remetente não verificado**: ela se baseia apenas na palavra dessa pessoa. A tarefa começa com "Não verificado: você nunca escreveu para essa pessoa."

A [recapitulação semanal](weekly-recap.md) contabiliza as promessas cumpridas e em aberto. No seu próprio computador, `assistant promises` as lista em um terminal.
