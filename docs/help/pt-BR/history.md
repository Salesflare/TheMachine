---
title: Histórico
area: connections
summary: Cerca de um ano de e-mails, reuniões e mensagens antigas do WhatsApp, Slack e Teams para pesquisar, ler e conhecer melhor as pessoas. Nunca cria uma tarefa.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 93575cd78b3085f7
---
## O que ela guarda

Sua Machine importa cerca de um ano de e-mails, reuniões e mensagens antigas do WhatsApp, Slack e Teams. A busca encontra essas mensagens, inclusive por significado, as conversas agrupadas também as mostram, e o [Calendário](calendar.md) exibe reuniões passadas.

Cada conexão em **Conexões** informa até quando ela volta, por exemplo, **Histórico: até** novembro de 2025.

## O que ela acrescenta ao Graph

Seu [Graph](graph.md) leva isso em conta: sua proximidade com as pessoas, quando conversou com elas pela última vez, quem conhece quem e as próprias pessoas e organizações. A Linha do tempo de uma pessoa ou organização também mostra essas informações, para que o último contato esteja sempre visível. As respostas do seu Fleet para "quem conhece alguém" usam esses dados das contas de trabalho, seguindo as mesmas [regras de compartilhamento](sharing-rules.md) dos e-mails novos.

## O que ela nunca faz

Ela nunca cria uma tarefa nem faz uma promessa, nunca conta como algo novo, nunca inicia uma verificação e nunca adiciona nada a um projeto. O histórico pessoal continua pessoal, assim como os e-mails pessoais. Fora a busca por significado, nenhum modelo de IA lê esse conteúdo.

## Quando ela é executada

Ela começa depois da primeira análise das suas mensagens. Para cada conexão, só começa depois que ela completa a primeira semana, inclusive se você a adicionar mais tarde. Ela é executada devagar em segundo plano e pausa enquanto uma verificação ou sincronização está em andamento, quando um serviço pede para reduzir o ritmo ou quando sua Machine está com pouco espaço. As mensagens novas sempre vêm primeiro.

Depois que o histórico de uma caixa de e-mail é importado, sua Machine lê mais uma vez os e-mails que guarda para encontrar detalhes de reservas e passagens. Assim, reservas antigas também aparecem em [viagens e eventos](calendar.md#trips-and-events). Essa leitura é igualmente lenta e pausa pelos mesmos motivos.

Ela usa o acesso que cada conexão já tem. Você não precisa aprovar mais nada.

## Até quando ela volta

Cerca de um ano. No seu próprio computador, `history_days` no arquivo de configurações altera esse período (0 desativa o recurso, até 730). O Telegram e outras fontes não importam histórico antigo.

As mensagens do LinkedIn e do X voltam 90 dias e são lidas bem devagar: algumas leituras pequenas por hora, só durante o dia, e nenhuma por um dia se o site impuser limites, para manter sua conta segura (`social_history_days`, 0 desativa o recurso).
