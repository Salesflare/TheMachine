---
title: Nenhuma tarefa nova
area: troubleshooting
summary: As verificações estão desligadas, aguardando ou pausadas pelo limite de uso do seu modelo. Veja como identificar o motivo e o que fazer.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: f0e9e4dc6c850b25
---
As tarefas vêm das verificações: sua Machine analisa o que chegou nos últimos 15 minutos, aproximadamente.

## Acabou de se cadastrar

Em uma nova Machine hospedada, as verificações começam automaticamente quando sua IA e seu e-mail estão conectados. Enquanto sua Machine lê seus e-mails, Tarefas mostra "Lendo seus e-mails. Primeiras tarefas em alguns minutos." Depois de saber quanto há para ler, ela informa aproximadamente quanto tempo vai levar: "Primeiras tarefas em cerca de 10 min." Se faltar alguma etapa, **Precisa de você** indica qual, como **Conectar e-mail**, e inclui um link para essa etapa.

Enquanto lê, ela mostra até onde chegou ("20 de 132 mensagens lidas. Lendo as próximas 40…"), algumas das pessoas e organizações que encontrou e sua primeira tarefa assim que ela aparecer. O número conta as mensagens que ela terminou de ler. A barra continua avançando enquanto ela lê as próximas. Os nomes vêm dos seus próprios e-mails, e só você pode vê-los.

Se a primeira análise não encontrar nada para você, ela informa o que leu e sugere próximos passos, como conectar um serviço que costuma enviar e-mails para você ou perguntar o que mudou nesta semana.

## As verificações estão desligadas

No topo de Tarefas, aparece "As verificações estão desligadas, então ainda não chegam tarefas." Em uma Machine hospedada, toque em **Ligar as verificações**. No seu próprio computador, execute `./install.sh --activate`.

## Limite do seu modelo

Para deixar espaço para seus próprios chats, as verificações são pausadas quando chegam a cerca de 65% do limite de 5 horas do seu plano de IA e a 90% do limite semanal. Se você tiver um modelo reserva em outro plano, as verificações não esperam. Consulte [Modelo](model.md).

Enquanto as verificações aguardam, o topo do painel mostra até quando, por exemplo: "As verificações aguardam até 07:15 para economizar seu limite semanal do ChatGPT." **Verificar agora** inicia uma verificação mesmo assim. Em **Configurações**, **Modelo** mostra seus limites.

Nada se perde: tudo o que chegou é verificado assim que possível. Depois de uma espera longa, as mensagens recentes de outras pessoas são verificadas primeiro, e cada verificação também analisa parte das mensagens mais antigas.

## À noite

Entre 00:00 e 06:30, as verificações são pausadas e as mensagens novas aguardam. Elas são verificadas juntas às 06:30, antes do resumo da manhã. **Verificações** mostra "Pausadas durante a noite. Atualização às 06:30." Use o app, escreva no chat ou toque em uma tarefa para que as verificações voltem a ser executadas. Elas continuam até você ficar uma hora sem usar o app. **Verificar agora** verifica as mensagens na hora.

## Uma execução falhou

**Execuções recentes**, em **Conexões**, **Verificações**, mostra cada execução. Se uma falhar, ela será repetida automaticamente.

Uma execução interrompida pelo limite de uso do seu plano de IA mostra **O limite de uso da IA foi atingido.** e informa quando o limite será renovado. Isso é uma pausa, não uma falha: as mensagens aguardam e são verificadas depois da renovação. Nada é enviado para [relatórios de erro](error-reports.md).

## Deixados de lado

Quando uma verificação adia uma mensagem duas vezes, ela é deixada de lado. **Conexões**, **Verificações** mostra quantas há, e **Deixados de lado** mostra quais são. Uma mensagem de alguém que escreve para você, de alguém que você conhece ou de um cliente é analisada mais uma vez cerca de 3 dias depois de chegar. Essa análise cria uma tarefa ou encerra a mensagem. O que você descartou ou adiou continua assim.
