---
title: Histórico
area: connections
summary: Cerca de um ano de e-mails, reuniões e conversas do WhatsApp antigos, para pesquisar e ler. Nunca uma tarefa.
covers: history
code: machine/app/history.py, machine/store/history.py
keywords: older messages, backfill, archive, past emails
---
## O que ele guarda

Cada conta de e-mail, agenda e WhatsApp guarda cerca de um ano de mensagens e reuniões antigas. A pesquisa as encontra, uma conversa as mostra e a [Agenda](calendar.md) mostra as reuniões passadas.

O cartão diz até onde ele vai: **Histórico: até** um mês, quando já chegou.

## O que ele nunca faz

O histórico serve só para consultar. Ele nunca cria uma tarefa ou uma promessa, nunca entra numa revisão, nunca conta como novo e nunca vai para o seu Graph ou a sua equipe. Nenhum modelo de IA o lê.

Tarefas e promessas continuam vindo só de mensagens novas, como antes.

## Quando ele roda

Ele começa quando a primeira olhada nas suas mensagens termina e anda devagar em segundo plano. Ele espera enquanto uma revisão ou uma sincronização roda, e quando a sua Machine tem pouco espaço em disco ou pouca memória. Depois de reiniciar, ele continua de onde parou.

Ele usa o acesso que cada conexão já tem. Nada novo é pedido.

## Até onde

Cerca de um ano por padrão. Machines auto-hospedadas podem definir `history_days` na configuração (0 desliga, até 730). Telegram, Slack e outras fontes guardam o que leem hoje.
