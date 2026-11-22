---
title: Resumo semanal
area: weekly
summary: Uma vez por semana, veja como sua Machine foi: tarefas, promessas, pessoas e projetos, além do que ela percebeu. Ativado por padrão.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 223b143a6efd5692
---
## O que vem no resumo

- Precisa de você: promessas atrasadas feitas a você e suas próprias promessas atrasadas ou com vencimento nas próximas duas semanas.
- Próxima semana: suas reuniões (com um link quando a preparação estiver pronta), tarefas com vencimento e promessas que outras pessoas fizeram para esse período.
- O que mudou: quantas tarefas valeram a pena em comparação com a semana anterior, quantas vezes **Fazer** acertou de primeira, o que ela ajustou na sua forma de escrever e nos filtros dela e quantos rascunhos foram enviados como estavam.
- Para a equipe da The Machine: aprendizados para compartilhar, se houver algum aguardando você. Veja [Compartilhar aprendizados com a equipe](share-learnings.md).
- Pessoas e projetos: projetos em alta ou em baixa, quem é novo e quem ficou em silêncio.
- Nos bastidores: quantos sinais ela verificou nesta semana e quantos ainda estão pendentes.
- No [Telegram](telegram.md), as opções aparecem em seguida, cada uma em sua própria mensagem: uma fonte movimentada sem resultados (**Parar de verificar** ou **Continuar verificando**) e uma tarefa adiada mais de uma vez (**Não precisa**, **Fazer** ou **Manter**). Nada muda até você tocar.

## Quando e onde

Por padrão, uma vez por semana, na sexta-feira, depois das 16:00 no seu fuso horário. Você recebe o resumo pelo [Telegram](telegram.md) ou como uma notificação com o título "Sua semana", enviada pelo [app para celular](phone-app.md) e pelo app do painel. Você também recebe por e-mail quando o e-mail está ativado para **Resumo da manhã** em Configurações › Notificações. Com o nível [Cuidadoso](security-levels.md), ou com **Texto nas notificações** desativado, o resumo não é enviado por e-mail.

## Desativar

O resumo fica ativado por padrão. Desative-o em Configurações › Notificações com a opção **Resumo semanal**. Se você desativar, ele continua desativado. No seu próprio computador, também é possível definir `weekly_recap` em config.json: `enabled` false com `chosen` true e, opcionalmente, `weekday` (1 a 7, sexta-feira é 5) e `at` ("16:00"). Consulte o [guia de configuração](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
