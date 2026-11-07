---
title: Resumo semanal
area: weekly
summary: Uma vez por semana, como sua Machine se saiu: tarefas, promessas, pessoas e projetos, e o que ela notou. Ativado por padrão.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
---
## O que vem nele

- Sua semana com a The Machine, e quantas tarefas valeram a pena, comparado com a semana anterior.
- Tarefas: novas, feitas, dispensadas e adiadas, e com que rapidez você respondeu.
- Promessas: as suas cumpridas e em aberto, as de outras pessoas que foram cumpridas ou ainda estão pendentes.
- Aprendizados para compartilhar com a equipe da The Machine, se algum estiver esperando por você. Veja [Compartilhar aprendizados com a equipe](share-learnings.md).
- Pessoas e projetos, como quem sumiu.
- O que eu notei: rascunhos enviados como estavam ou editados, tarefas dispensadas em poucos minutos, tarefas adiadas mais de uma vez.
- Nos bastidores: quantos sinais ela verificou nesta semana e quantos ainda aguardam.
- Opções, cada uma em sua própria mensagem depois do resumo: uma fonte movimentada sem resultados (**Parar de verificar** ou **Continuar verificando**) e uma tarefa adiada mais de uma vez (**Descartar**, **Fazer agora** ou **Manter**). Nada muda até você tocar.

## Quando e onde

Uma vez por semana, por padrão na sexta-feira depois das 16:00 no seu fuso horário. Ele chega pelo [Telegram](telegram.md), ou como uma notificação com o título "Sua semana" no [app do celular](phone-app.md) e no app do painel. Também chega por e-mail quando o e-mail está ligado para **Resumo da manhã** em Configurações › Notificações. Com [Cuidadoso](security-levels.md), não chega por e-mail.

## Desativar

Ele vem ativado por padrão. Desative em Configurações › Notificações com o botão **Resumo semanal**. Se você desativou, continua desativado. No seu próprio computador você também pode definir `weekly_recap` no config.json: `enabled` false com `chosen` true e, se quiser, `weekday` (1 a 7, sexta-feira é 5) e `at` ("16:00"). Veja o [guia de configuração](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
