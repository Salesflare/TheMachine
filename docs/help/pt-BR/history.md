---
title: Histórico
area: connections
summary: Cerca de um ano de e-mails, reuniões e mensagens antigas do WhatsApp, Slack e Teams para pesquisar, ler e conhecer melhor as pessoas. Nunca vira uma tarefa.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 2b5e84c61892c8e4
---
## O que ela guarda

Sua Machine importa cerca de um ano de e-mails, reuniões e mensagens antigas do WhatsApp, Slack e Teams. A Busca encontra esse conteúdo, inclusive por significado. As conversas mostram as mensagens relacionadas, e o [Calendário](calendar.md) mostra reuniões passadas.

Cada conexão em **Conexões** informa até quando o histórico volta, por exemplo: **Histórico: desde** novembro de 2025.

## O que ela acrescenta ao seu Graph

Seu [Graph](graph.md) usa esse histórico para mostrar o quanto você é próximo das pessoas, quando conversou com elas pela última vez, quem conhece quem e quem são as pessoas e organizações. A Linha do tempo de cada pessoa ou organização também mostra esse histórico, para que o último contato esteja sempre disponível. As respostas do seu Fleet à pergunta “quem conhece alguém” usam esse histórico das contas de trabalho, seguindo as mesmas [regras de compartilhamento](sharing-rules.md) das mensagens novas.

## O que ela nunca faz

Ela nunca cria uma tarefa nem uma promessa, nunca conta como conteúdo novo, nunca inicia uma verificação e nunca adiciona nada a um projeto. O histórico pessoal continua sendo pessoal, assim como os e-mails pessoais.

Além da Busca por significado, seu modelo de IA só lê esse histórico em três situações:

- quando uma pesquisa encontra algo, por exemplo, para responder a uma pergunta sua ou trabalhar em uma tarefa
- em e-mails com detalhes de reservas, para [viagens e eventos](calendar.md#trips-and-events)
- em um [briefing de reunião](calendar.md#ready-for-your-meetings): anotações de reuniões anteriores e algumas mensagens antigas com as pessoas que você vai encontrar

## Quando ela funciona

Ela começa depois da primeira análise das suas mensagens. Para cada conexão, só começa depois que a primeira semana de mensagens é importada, inclusive para conexões adicionadas mais tarde. Ela funciona devagar em segundo plano e pausa enquanto uma verificação ou sincronização está em andamento, quando um serviço pede que ela reduza o ritmo ou quando sua Machine está com pouco espaço. As mensagens novas sempre têm prioridade.

Depois que o histórico de uma caixa de e-mail é importado, sua Machine lê mais uma vez os e-mails que guarda para encontrar detalhes de reservas e ingressos. Assim, reservas antigas também aparecem em [viagens e eventos](calendar.md#trips-and-events). Essa leitura também é lenta e pausa pelos mesmos motivos.

Ela usa o acesso que cada conexão já tem. Não é preciso aprovar nada novo.

## Até quando o histórico volta

Cerca de um ano. No seu próprio computador, `history_days` no arquivo de configurações altera esse período (0 desativa o recurso, até 730 dias). O Telegram e outras fontes não importam o histórico antigo.

As mensagens do LinkedIn e do X voltam 90 dias e são lidas bem devagar: algumas consultas curtas por hora, apenas durante o dia. Se o site limitar o acesso, ela não faz nenhuma consulta por um dia, para manter sua conta segura (`social_history_days`, 0 desativa o recurso).
