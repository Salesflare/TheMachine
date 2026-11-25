---
title: Nenhuma tarefa nova
area: troubleshooting
summary: As verificações estão desligadas, aguardando ou pausadas por causa do limite de uso do seu modelo. Veja como identificar o motivo e o que fazer.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: 40617b8ac692660b
---
As tarefas vêm das verificações: sua Machine analisa o que chegou nos últimos 15 minutos, aproximadamente.

## Acabou de se cadastrar

Em uma Machine hospedada nova, as verificações começam sozinhas assim que sua IA e seu e-mail estão conectados. Enquanto sua Machine lê seus e-mails, Tarefas mostra "Lendo seus e-mails. As primeiras tarefas chegam em alguns minutos." Quando sabe quantas mensagens há, informa uma estimativa: "As primeiras tarefas chegam em cerca de 10 min." Se faltar alguma etapa, **Precisa de você** indica qual, como **Conectar e-mail**, com um link para essa etapa.

Enquanto lê, Tarefas mostra até onde chegou ("20 de 132 mensagens lidas. Lendo as próximas 40…"), algumas das pessoas e organizações que encontrou e sua primeira tarefa assim que ela fica pronta. O número conta as mensagens que já terminou de ler; a barra continua avançando enquanto lê as próximas. Os nomes vêm dos seus e-mails, e só você pode vê-los.

Se a primeira análise não encontrar nada para você, ela informa o que leu e sugere próximos passos, como conectar um serviço que costuma enviar e-mails para você ou perguntar o que mudou nesta semana.

## As verificações estão desligadas

No topo de Tarefas, aparece "As verificações estão desligadas. Ainda não há tarefas." Em uma Machine hospedada, toque em **Ligar as verificações**. No seu computador, execute `./install.sh --activate`.

## Limite do seu modelo

Para deixar espaço para seus próprios chats, as verificações pausam quando você chega a cerca de 65% do limite de 5 horas do seu plano de IA e a 90% do limite semanal. Se você tiver um modelo reserva em outro plano, as verificações não precisam esperar. Consulte [Modelo](model.md).

Enquanto as verificações aguardam, o topo do painel informa até quando, por exemplo: "As verificações aguardam até 07:15 para preservar seu limite semanal do ChatGPT." **Verificar agora** inicia uma verificação mesmo assim. Em **Configurações**, **Modelo** mostra seus limites.

Nada se perde: as mensagens recebidas são verificadas assim que possível. Depois de uma espera longa, as mensagens recentes de outras pessoas são verificadas primeiro, e cada verificação também analisa parte das mensagens mais antigas.

Até que tudo esteja em dia, as tarefas novas chegam sem rascunho, para que seu plano seja usado primeiro nas mensagens. Os rascunhos vêm depois, e as tarefas urgentes não esperam por eles. Toque em **Fazer** para criar um agora.

## À noite

Das 00:00 às 06:30, as verificações pausam e as mensagens novas ficam aguardando. Elas são verificadas juntas às 06:30, antes do resumo da manhã. **Verificações** mostra "Pausadas durante a noite. Em dia às 06:30". Use o app, escreva no chat ou toque em uma tarefa para as verificações voltarem a funcionar. Elas continuam até você ficar uma hora sem usar o app. **Verificar agora** inicia uma verificação na hora.

## Uma execução falhou

**Execuções recentes**, em **Conexões**, **Verificações**, mostra cada execução. Uma execução que falhou é iniciada novamente automaticamente.

Uma execução interrompida por causa do limite de uso do seu plano de IA mostra **O limite de uso da IA foi atingido.** e informa quando o limite será liberado. Isso é uma pausa, não uma falha: as mensagens aguardam e são verificadas depois que o limite é redefinido. Nada vai para [relatórios de erro](error-reports.md).

## Deixados de lado

Quando uma verificação adia uma mensagem duas vezes, ela é deixada de lado. **Conexões**, **Verificações** mostra quantas mensagens há, e **Deixados de lado** lista todas elas. Uma mensagem de alguém que escreveu para você, de alguém que você conhece ou de um cliente é verificada mais uma vez cerca de 3 dias depois de chegar. Essa verificação cria uma tarefa ou encerra a mensagem. O que você descartou ou adiou continua assim.
