---
title: Nenhuma tarefa nova
area: troubleshooting
summary: As verificações estão desligadas, aguardando ou pararam por causa do limite de uso do seu modelo. Veja como identificar o motivo e o que fazer.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: 07aca53acc41694d
---
As tarefas vêm das verificações: sua Machine analisa o que chegou nos últimos 15 minutos, aproximadamente.

## Acabou de se cadastrar

Em uma Machine hospedada nova, as verificações começam automaticamente quando você conecta a IA e o e-mail. Enquanto sua Machine lê seus e-mails, Tarefas mostra "Lendo seus e-mails. As primeiras tarefas chegam em alguns minutos." Depois de calcular quanto há para ler, ela mostra uma estimativa: "Primeiras tarefas em cerca de 10 min." Se faltar alguma etapa, **Precisa de você** indica qual é, como **Conectar e-mail**, com um link para essa etapa.

Enquanto lê, ela mostra o progresso ("20 de 132 mensagens lidas. Lendo as próximas 40…"), algumas das pessoas e organizações encontradas e sua primeira tarefa assim que ela aparece. O número conta as mensagens que ela terminou de ler; a barra continua avançando enquanto lê as próximas. Os nomes vêm dos seus e-mails, e só você pode vê-los.

Se a primeira análise não encontrar nada para você, ela informa o que leu e sugere os próximos passos, como conectar um serviço de onde você recebe muitos e-mails ou perguntar o que mudou nesta semana.

## As verificações estão desligadas

No topo de Tarefas, aparece "As verificações estão desligadas. Nenhuma tarefa nova vai chegar por enquanto." Em uma Machine hospedada, selecione **Ligar as verificações**. No seu computador, execute `./install.sh --activate`.

## Limite do seu modelo

Para deixar espaço para seus próprios chats, as verificações pausam quando chegam a cerca de 65% do limite de 5 horas do seu plano de IA e a 90% do limite semanal. Com um modelo reserva em outro plano, as verificações não precisam esperar. Saiba mais em [Modelo](model.md).

Enquanto as verificações aguardam, o topo do painel informa até quando, por exemplo: "As verificações aguardam até 07:15 para poupar seu limite semanal do ChatGPT." **Verificar agora** inicia uma verificação mesmo assim. Em **Configurações**, **Modelo** mostra seus limites.

Nada se perde: o que chegou será verificado assim que possível.

## À noite

Das 00:00 às 06:30, as verificações pausam e as novas mensagens ficam aguardando. Elas são verificadas juntas às 06:30, antes do resumo da manhã. **Verificações** mostra "Pausadas durante a noite. Retomam às 06:30". Use o app, escreva no chat ou toque em uma tarefa para as verificações voltarem a ser executadas. Elas continuam até você ficar uma hora sem usar o app. **Verificar agora** inicia uma verificação imediatamente.

## Uma execução falhou

**Execuções recentes**, em **Conexões**, **Verificações**, mostra cada execução. Uma execução que falhou é repetida automaticamente.

Uma execução interrompida por causa do limite de uso do seu plano de IA mostra **O limite de uso da IA foi atingido.** e informa quando o limite será liberado. Isso é uma pausa, não uma falha: as mensagens aguardam e são verificadas depois que o limite é redefinido. Nada vai para os [relatórios de erro](error-reports.md).

## Deixados de lado

Quando uma verificação deixa uma mensagem de lado duas vezes, ela fica nessa lista. **Conexões**, **Verificações** mostra quantas há, e **Deixados de lado** lista as mensagens. Uma mensagem de alguém que escreveu para você, de alguém que você conhece ou de um cliente recebe mais uma análise cerca de 3 dias depois de chegar. Essa análise cria uma tarefa ou encerra a mensagem. O que você descartou ou adiou continua assim.
