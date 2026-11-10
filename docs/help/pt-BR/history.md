---
title: Histórico
area: connections
summary: Cerca de um ano de e-mails, reuniões e mensagens do WhatsApp, Slack e Teams antigos, para pesquisar, ler e conhecer as suas pessoas. Nunca uma tarefa.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
---
## O que ele guarda

Cada conta de e-mail, agenda, WhatsApp, Slack e Teams guarda cerca de um ano de mensagens e reuniões antigas. A pesquisa as encontra, também por significado, uma conversa as mostra e a [Agenda](calendar.md) mostra as reuniões passadas.

O cartão diz até onde ele vai: **Histórico: até** um mês, quando já chegou.

## O que ele traz para o seu Graph

O seu [Graph](graph.md) conta com ele: o quanto você é próximo das pessoas, quando vocês se falaram pela última vez, quem conhece quem, e as próprias pessoas e organizações. A Linha do tempo de uma pessoa ou organização também mostra ele, então o último contato sempre aparece lá. As respostas da sua Fleet a "quem conhece alguém" usam ele a partir das contas de trabalho, com as mesmas [regras de compartilhamento](sharing-rules.md) dos e-mails novos.

## O que ele nunca faz

Ele nunca cria uma tarefa ou uma promessa, nunca conta como novo, nunca inicia uma verificação e nunca entra num projeto. O histórico pessoal continua pessoal, como o e-mail pessoal. Fora a pesquisa por significado, nenhum modelo de IA o lê.

## Quando ele roda

Ele começa quando a primeira olhada nas suas mensagens termina, e em cada conexão só quando a primeira semana dela já chegou, também numa que você adicionar depois. Ele anda devagar em segundo plano e espera enquanto uma verificação ou uma sincronização roda, quando um serviço pede para ir mais devagar ou quando a sua Machine tem pouco espaço. Mensagens novas sempre vêm primeiro.

Ele usa o acesso que cada conexão já tem. Nada novo é pedido.

## Até onde

Cerca de um ano por padrão. Machines auto-hospedadas podem definir `history_days` na configuração (0 desliga, até 730). Telegram e outras fontes guardam o que leem hoje.

Mensagens do LinkedIn e do X voltam 90 dias e são lidas bem devagar: poucas leituras pequenas por hora, só de dia, e nenhuma por um dia se o site resistir, para sua conta ficar segura (`social_history_days`, 0 desliga).
