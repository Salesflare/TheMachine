---
title: Resumo semanal
area: weekly
summary: Uma vez por semana, como sua Machine se saiu: tarefas, promessas, pessoas e projetos, e o que ela notou. Desativado por padrão.
covers: weekly-recap
code: assistant.py, config.example.json
order: 1
---
## O que vem nele

- Sua semana com a The Machine, e quantas tarefas valeram a pena, comparado com a semana anterior.
- Tarefas: novas, feitas, dispensadas e adiadas, e com que rapidez você respondeu.
- Promessas: as suas cumpridas e em aberto, as de outras pessoas que foram cumpridas ou ainda estão pendentes.
- Aprendizados para compartilhar com a equipe da The Machine, se algum estiver esperando por você. Veja [Compartilhar aprendizados com a equipe](share-learnings.md).
- Pessoas e projetos, como quem sumiu.
- O que eu notei: rascunhos enviados como estavam ou editados, tarefas dispensadas em poucos minutos, tarefas adiadas mais de uma vez.
- Nos bastidores: o que ela revisou e quanto isso custou.

## Quando e onde

Uma vez por semana, por padrão na sexta-feira depois das 16:00 no seu fuso horário. Ele chega pelo [Telegram](telegram.md), ou como uma notificação com o título "Sua semana" no [app do celular](phone-app.md).

## Ativar

Ele vem desativado, e o painel ainda não tem um botão para ele, então uma Machine hospedada não consegue ativá-lo hoje. No seu próprio computador, defina `weekly_recap` no config.json da sua Machine: `enabled` true e, se quiser, `weekday` (1 a 7, sexta-feira é 5) e `at` ("16:00"). Veja o [guia de configuração](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
