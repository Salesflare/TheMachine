---
title: Nenhuma tarefa nova
area: troubleshooting
summary: As revisões estão desativadas, esperando ou paradas no limite de uso do seu modelo. Como saber e o que fazer.
covers: 
code: dashboard.html, assistant.py
order: 3
---
As tarefas vêm das revisões: sua Machine lê o que chegou, em pequenos lotes, em cerca de uma hora.

## As revisões estão desativadas

O topo de Sugestões diz "As revisões estão desativadas, então ainda não chegam sugestões." Em uma Machine hospedada, clique em **Ativar revisões**. No seu próprio computador, execute `./install.sh --activate`.

## O limite do seu modelo

As revisões pausam em cerca de 65% do limite de 5 horas do seu plano e dosam o limite semanal, para sobrar espaço para os seus próprios chats. Quando um limite é atingido, o topo do painel diz qual foi e quando ele reinicia. **Conexões** e depois **Revisões** mostra isso ao lado da execução. **Configurações**, **Modelo** mostra seus limites. Veja [Modelo](model.md).

Nada se perde enquanto espera: o que chegou é revisado assim que for possível.

## Uma execução falhou

**Execuções recentes** em **Revisões** mostra cada execução. Um lote que falhou é tentado de novo sozinho.
