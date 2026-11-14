---
title: Nenhuma tarefa nova
area: troubleshooting
summary: As verificações estão desativadas, esperando ou paradas no limite de uso do seu modelo. Como saber e o que fazer.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: 39b4aa749445dfba
---
As tarefas vêm das verificações: sua Machine lê o que chegou, em pequenos lotes, em cerca de 15 minutos.

## Acabou de se cadastrar

Em uma Machine hospedada nova, as verificações começam sozinhas assim que sua IA e seu e-mail estão conectados. Enquanto sua Machine lê seus e-mails, Tarefas mostra "Lendo seus e-mails, primeiras tarefas em poucos minutos". Assim que sabe quanto há, ela diz mais ou menos quanto falta: "Primeiras tarefas em cerca de 10 min." Se faltar uma etapa, **Precisa de você** mostra qual, como **Conectar e-mail**, com um link para essa etapa.

Enquanto lê, Tarefas mostra até onde ela chegou, algumas das pessoas e organizações que encontrou e sua primeira tarefa assim que chega. Os nomes vêm do seu próprio e-mail, e só você os vê.

Se na primeira olhada ela não encontrar nada para você, diz o que leu e oferece próximos passos, como conectar um serviço que te escreve com frequência ou perguntar o que mudou esta semana.

## As verificações estão desativadas

O topo de Tarefas diz "As verificações estão desligadas, então nenhuma tarefa chega ainda." Em uma Machine hospedada, clique em **Ligar as verificações**. No seu próprio computador, execute `./install.sh --activate`.

## O limite do seu modelo

As verificações do que chegou pausam em cerca de 65% do limite de 5 horas do seu plano e em 90% do limite semanal, para sobrar espaço para os seus próprios chats. Um quadro que percorre seu histórico vai mais devagar, em cerca de um sétimo da semana por dia. Com um modelo reserva funcionando, em outro plano ou provedor, as verificações não esperam. Veja [Modelo](model.md).

Enquanto as verificações esperam, o topo do painel diz até quando, como "As verificações esperam até 07:15 para poupar sua semana do ChatGPT." **Verificar agora** inicia uma na hora. Quando um limite é atingido, o topo do painel diz qual foi e quando ele reinicia. **Conexões** e depois **Verificações** mostra isso ao lado da execução. **Configurações**, **Modelo** mostra seus limites. Veja [Modelo](model.md).

Nada se perde enquanto espera: o que chegou é verificado assim que for possível.

## À noite

Das 00:00 às 06:30, as verificações pausam e as mensagens novas esperam. Elas são verificadas juntas às 06:30, antes do seu resumo da manhã. **Verificações** diz então "Em pausa durante a noite, põe tudo em dia às 06:30". Se você usar o app, escrever no chat ou tocar numa tarefa, as verificações voltam até você ficar uma hora sem usar. **Verificar agora** verifica na hora.

## Uma execução falhou

**Execuções recentes** em **Verificações** mostra cada execução. Um lote que falhou é tentado de novo sozinho.

## Deixados de lado

Quando uma verificação adia uma mensagem duas vezes, ela é deixada de lado. **Conexões**, **Verificações** mostra quantas, e **Deixados de lado** lista todas. Uma de uma pessoa que escreve direto para você, de alguém que você conhece ou de um cliente recebe uma última olhada cerca de 3 dias depois de chegar. Essa olhada cria uma tarefa ou a fecha. O que você dispensou ou adiou continua assim.
