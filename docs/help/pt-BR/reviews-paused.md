---
title: Nenhuma tarefa nova
area: troubleshooting
summary: As revisões estão desativadas, esperando ou paradas no limite de uso do seu modelo. Como saber e o que fazer.
covers: 
code: dashboard.html, assistant.py
order: 3
---
As tarefas vêm das revisões: sua Machine lê o que chegou, em pequenos lotes, em cerca de 15 minutos.

## Acabou de se cadastrar

Em uma Machine hospedada nova, as revisões começam sozinhas assim que sua IA e seu e-mail estão conectados. Enquanto sua Machine lê seus e-mails, Tarefas mostra "Lendo seus e-mails, primeiras tarefas em poucos minutos". Se faltar uma etapa, **Precisa de você** mostra qual, como **Conectar e-mail**, com um link para essa etapa.

## As revisões estão desativadas

O topo de Tarefas diz "As revisões estão desligadas, então nenhuma tarefa chega ainda." Em uma Machine hospedada, clique em **Ativar revisões**. No seu próprio computador, execute `./install.sh --activate`.

## O limite do seu modelo

As revisões do que chegou pausam em cerca de 65% do limite de 5 horas do seu plano e em 90% do limite semanal, para sobrar espaço para os seus próprios chats. Um quadro que percorre seu histórico vai mais devagar, em cerca de um sétimo da semana por dia. Com um modelo reserva funcionando, em outro plano ou provedor, as revisões não esperam. Veja [Modelo](model.md).

Enquanto as revisões esperam, o topo do painel diz até quando, como "As revisões esperam até 07:15 para poupar sua semana do ChatGPT." **Revisar agora** inicia uma na hora. Quando um limite é atingido, o topo do painel diz qual foi e quando ele reinicia. **Conexões** e depois **Revisões** mostra isso ao lado da execução. **Configurações**, **Modelo** mostra seus limites. Veja [Modelo](model.md).

Nada se perde enquanto espera: o que chegou é revisado assim que for possível.

## Uma execução falhou

**Execuções recentes** em **Revisões** mostra cada execução. Um lote que falhou é tentado de novo sozinho.
