---
title: Saúde da Machine
area: connections
summary: O registro da própria Machine ajuda a detectar os problemas dela. É somente leitura.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 7d66ff6a6a5d5b1d
---
## O que ela lê

O registro da própria Machine: execuções com falha, repasses recusados, mensagens do Telegram que não foram enviadas e erros da própria The Machine. Uma tarefa avisa quando algo precisa ser corrigido. No seu computador, isso inclui **Terminar de instalar a última atualização**: uma parte da atualização precisa de uma reinicialização rápida durante a noite, mas isso não foi possível por algumas noites. Peça isso no chat dela, e ela conclui. A tarefa se fecha sozinha quando essa parte estiver instalada.

## Correções deixadas de lado por uma atualização

Quando The Machine é atualizada e uma de suas próprias correções não funciona mais na nova versão, a atualização deixa essa correção de lado e continua, para que sua Machine nunca fique em uma versão antiga. Uma tarefa, **Refazer uma correção que a atualização deixou de lado**, informa qual é a correção.

Com **Refazer**, sua Machine cria a correção novamente na nova versão, como faz com qualquer correção própria: você vê a alteração e toca em **Mesclar correção**. Depois que ela é mesclada, a cópia antiga é descartada. Ou feche a tarefa.

## Seus arquivos que uma atualização manteve

Quando uma nova versão traz um arquivo com o mesmo nome de um arquivo que você adicionou, a atualização renomeia o seu em vez de substituí-lo e continua. Uma tarefa informa quantos arquivos foram mantidos e lista cada nome antigo e novo. Feche-a depois de conferir.

## O que ela pode fazer

Nada. Ela apenas lê o registro da sua própria Machine.

## Conectar

- Em uma Machine hospedada, ela aparece na página de configuração, em **Mais fontes**, como Saúde da Machine. Uma por Machine.
- No seu computador: **Conexões**, **Outras**, Saúde da Machine. Ou execute `assistant connect gateway`.

## Remover

- No painel: **Conexões**, abra a conexão, toque em **Detalhes** e depois em **Desconectar**.
- Em uma Machine hospedada, você também pode tocar em **Remover** ao lado dela na página de configuração.

Não é preciso desinstalar nada em nenhum outro lugar.
