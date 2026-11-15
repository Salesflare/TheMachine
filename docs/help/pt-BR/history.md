---
title: Histórico
area: connections
summary: Cerca de um ano de e-mails antigos, reuniões e mensagens do WhatsApp, Slack e Teams para pesquisar, ler e conhecer as pessoas. Nunca vira uma tarefa.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: c10fe5fb8d7b2d8b
---
## O que ele guarda

Sua Machine importa cerca de um ano de e-mails antigos, reuniões e mensagens do WhatsApp, Slack e Teams. A pesquisa encontra esse conteúdo, inclusive por significado, as conversas mostram as mensagens, e o [Calendário](calendar.md) mostra as reuniões anteriores.

Cada conexão em **Conexões** informa até que data ela volta, como **Histórico: desde** novembro de 2025.

## O que isso acrescenta ao seu Graph

Seu [Graph](graph.md) usa essas informações para mostrar o quanto você é próximo das pessoas, quando conversou com elas pela última vez, quem conhece quem e quem são as pessoas e organizações. A linha do tempo de uma pessoa ou organização também mostra essas informações, para que o último contato esteja sempre disponível. As respostas da sua Fleet para "quem conhece alguém" usam essas informações das contas de trabalho, seguindo as mesmas [regras de compartilhamento](sharing-rules.md) dos e-mails novos.

## O que isso nunca faz

Nunca cria uma tarefa nem uma promessa, nunca conta como conteúdo novo, nunca inicia uma verificação e nunca é adicionado a um projeto. O histórico pessoal continua pessoal, como os e-mails pessoais. Com exceção da pesquisa por significado, nenhum modelo de IA lê esse conteúdo.

## Quando isso acontece

Começa depois que suas mensagens são verificadas pela primeira vez. Para cada conexão, só começa depois que a primeira semana dela termina. Isso também vale para conexões adicionadas depois. O processo acontece devagar, em segundo plano, e pausa enquanto uma verificação ou sincronização está em andamento, quando um serviço pede para reduzir o ritmo ou quando falta espaço na sua Machine. As mensagens novas sempre têm prioridade.

Quando o histórico de uma caixa de e-mail termina de ser importado, sua Machine lê novamente os e-mails guardados para encontrar detalhes de reservas e passagens, para que as reservas antigas também apareçam em [Viagens e eventos](notes.md). A leitura acontece no mesmo ritmo lento e pausa pelos mesmos motivos.

O processo usa o acesso que cada conexão já tem. Não é preciso aprovar nada de novo.

## Até que data

Cerca de um ano. No seu próprio computador, `history_days` no arquivo de configurações altera esse período (0 desativa o recurso; o máximo é 730 dias). O Telegram e outras fontes não importam o histórico antigo.

As mensagens do LinkedIn e do X voltam 90 dias e são lidas bem devagar: algumas leituras pequenas por hora, apenas durante o dia, e nenhuma leitura por um dia se o site restringir o acesso, para manter sua conta segura (`social_history_days`, 0 desativa o recurso).
