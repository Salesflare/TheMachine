---
title: Nenhuma tarefa nova
area: troubleshooting
summary: As verificações estão desativadas, aguardando ou pausadas por causa do limite de uso do seu modelo. Saiba como identificar o motivo e o que fazer.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: d8a15909ab8164e8
---
As tarefas vêm das verificações: sua Machine analisa o que chegou nos últimos 15 minutos, aproximadamente.

## Acabou de se cadastrar

Em uma Machine hospedada nova, as verificações começam automaticamente quando você conecta sua IA e seu e-mail. Enquanto sua Machine lê seus e-mails, em Tarefas aparece "Lendo seus e-mails. As primeiras tarefas chegam em alguns minutos." Quando ela sabe quanto conteúdo há, informa aproximadamente quanto tempo vai levar: "Primeiras tarefas em cerca de 10 min." Se faltar alguma etapa, **Precisa de você** indica qual, como **Conectar e-mail**, e inclui um link para essa etapa.

Enquanto lê, Tarefas mostra até onde ela chegou ("20 de 132 mensagens lidas. Lendo as próximas 40…"), algumas das pessoas e organizações que encontrou e sua primeira tarefa assim que ela estiver pronta. O número conta as mensagens que ela terminou de ler; a barra continua avançando enquanto ela lê as próximas. Os nomes vêm dos seus próprios e-mails, e só você pode vê-los.

Quando a primeira análise não encontra nada para você, ela informa o que leu e sugere próximos passos, como conectar um serviço que costuma enviar e-mails ou perguntar o que mudou nesta semana.

## As verificações estão desativadas

No topo de Tarefas aparece "As verificações estão desativadas, então nenhuma tarefa nova vai chegar." Em uma Machine hospedada, clique em **Ligar as verificações**. No seu próprio computador, execute `./install.sh --activate`.

## Limite do seu modelo

Para deixar espaço para seus próprios chats, as verificações pausam quando o uso chega a cerca de 65% do limite de 5 horas do seu plano de IA e a 90% do limite semanal. Se você tiver um modelo alternativo em outro plano, as verificações não precisam esperar. Consulte [Modelo](model.md).

Enquanto as verificações aguardam, no topo do painel aparece até quando, como "As verificações aguardam até 07:15 para poupar seu limite semanal do ChatGPT." **Verificar agora** inicia uma verificação mesmo assim. Em **Configurações**, **Modelo** mostra seus limites.

Nada se perde: o que chegou será verificado assim que possível. Depois de uma espera longa, as mensagens recentes de pessoas são verificadas primeiro, e cada verificação também analisa parte das mais antigas.

Até alcançar as mensagens pendentes, as tarefas novas chegam sem um rascunho, para que seu plano seja usado primeiro nas mensagens. Os rascunhos chegam depois, e as tarefas urgentes não precisam esperar. Clique em **Fazer** para receber um rascunho agora.

## À noite

Das 00:00 às 06:30, as verificações pausam e as mensagens novas ficam aguardando. Elas são verificadas juntas às 06:30, antes do resumo da manhã. Em **Verificações** aparece "Pausadas durante a noite. As mensagens serão verificadas às 06:30." Use o app, escreva no chat ou toque em uma tarefa para que as verificações sejam retomadas. Elas continuam até você ficar uma hora sem usar o app. **Verificar agora** faz uma verificação imediatamente.

## Uma execução falhou

**Execuções recentes**, em **Conexões**, **Verificações**, mostra cada execução. Uma execução que falhou é tentada novamente automaticamente. Se sua IA parar de responder, por exemplo, porque sua sessão expirou, entre novamente em **Configurações**, **Modelo**. As verificações serão retomadas logo em seguida.

Uma execução interrompida porque o limite de uso do seu plano de IA foi atingido mostra **O limite de uso da IA foi atingido.** e informa quando ele será renovado. Isso é uma pausa, não uma falha: as mensagens ficam aguardando e são verificadas depois da renovação. Nada é enviado para [relatórios de erro](error-reports.md).

## Deixados de lado

Quando uma verificação adia uma mensagem duas vezes, ela é deixada de lado. **Conexões**, **Verificações** mostra quantas há, e **Deixados de lado** lista essas mensagens.

Uma mensagem que faz todas as verificações falharem, mesmo quando sua IA está funcionando, também é deixada de lado, para que as outras sejam verificadas.

Uma mensagem de alguém que está escrevendo para você, de uma pessoa que você conhece ou de um cliente é analisada mais uma vez cerca de 3 dias depois de chegar. Essa análise cria uma tarefa ou encerra a mensagem. O que você descartou ou adiou continua assim.
