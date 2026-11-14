---
title: Nenhuma tarefa nova
area: troubleshooting
summary: As verificações estão desativadas, aguardando ou pausadas por causa do limite de uso do seu modelo. Veja como identificar o motivo e o que fazer.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: d265e540d9ecef0e
---
As tarefas vêm das verificações: sua Machine analisa o que chegou nos últimos 15 minutos, aproximadamente.

## Acabou de se cadastrar

Em uma Machine hospedada nova, as verificações começam automaticamente quando você conecta sua IA e seu e-mail. Enquanto sua Machine lê seus e-mails, a seção Tarefas mostra "Lendo seus e-mails. Primeiras tarefas em alguns minutos." Depois que ela sabe quanto conteúdo há para ler, informa o tempo aproximado: "Primeiras tarefas em cerca de 10 min." Se faltar alguma etapa, **Precisa de você** indica qual, como **Conectar e-mail**, e inclui um link para essa etapa.

Enquanto lê, ela mostra até onde chegou ("20 de 132 mensagens lidas. Lendo as próximas 40…"), algumas pessoas e organizações que encontrou e sua primeira tarefa assim que ela aparecer. O número conta as mensagens que ela terminou de ler; a barra continua avançando enquanto ela lê as próximas. Os nomes vêm dos seus próprios e-mails e só você pode vê-los.

Se a primeira análise não encontrar nada para você, ela informa o que leu e sugere os próximos passos, como conectar um serviço de onde você recebe e-mails com frequência ou perguntar o que mudou nesta semana.

## As verificações estão desativadas

No topo da seção Tarefas, aparece "As verificações estão desativadas, então nenhuma tarefa nova será criada." Em uma Machine hospedada, pressione **Ligar as verificações**. No seu próprio computador, execute `./install.sh --activate`.

## Limite do seu modelo

Para reservar espaço para seus próprios chats, as verificações pausam quando chegam a cerca de 65% do limite de 5 horas do seu plano de IA e a 90% do limite semanal. Se você tiver um modelo reserva em outro plano, as verificações não precisam esperar. Veja [Modelo](model.md).

Enquanto as verificações aguardam, o topo do painel mostra até quando, por exemplo: "As verificações aguardam até 07:15 para economizar seu limite semanal do ChatGPT." **Verificar agora** inicia uma verificação mesmo assim. Em **Configurações**, **Modelo** mostra seus limites.

Nada se perde: o que chegou é verificado assim que possível.

## À noite

Das 00:00 às 06:30, as verificações pausam e as mensagens novas aguardam. Elas são verificadas juntas às 06:30, antes do seu resumo da manhã. **Verificações** mostra "Pausadas durante a noite. As mensagens serão verificadas às 06:30". Use o app, escreva no chat ou toque em uma tarefa para que as verificações voltem a funcionar. Elas continuam até você ficar uma hora sem usar o app. **Verificar agora** faz uma verificação na hora.

## Uma execução falhou

**Execuções recentes**, em **Conexões**, **Verificações**, mostra cada execução. Uma execução que falhou é tentada novamente automaticamente.

## Deixados de lado

Quando uma verificação adia uma mensagem duas vezes, ela é deixada de lado. **Conexões**, **Verificações** mostra quantas mensagens há, e **Deixados de lado** lista essas mensagens. Uma mensagem de alguém que escreve para você, de alguém que você conhece ou de um cliente é analisada mais uma vez cerca de 3 dias depois de chegar. Essa análise cria uma tarefa ou encerra a mensagem. O que você descartou ou adiou continua assim.
