---
title: Saúde da Machine
area: connections
summary: O próprio registro da sua Machine, para ela detectar problemas. Só leitura.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 3a06400a28396465
---
## O que ela lê

O registro da sua própria Machine: execuções com falha, repasses recusados, mensagens do Telegram que não foram enviadas e erros da própria The Machine. Uma tarefa avisa quando algo precisa de correção. No seu computador, isso inclui **Terminar de instalar a última atualização**: uma parte da atualização precisa de uma reinicialização rápida à noite, mas isso não foi possível em algumas noites. Peça no chat dela e The Machine termina a instalação. Ela se fecha sozinha assim que essa parte estiver instalada.

## Correções deixadas de lado por uma atualização

Quando The Machine se atualiza e uma das correções dela não é mais compatível com a nova versão, a atualização deixa essa correção de lado e continua, para sua Machine nunca ficar em uma versão antiga. Uma tarefa, **Refazer uma correção que a atualização deixou de lado**, identifica a correção.

**Refazer** faz sua Machine criar a correção novamente na nova versão, como em qualquer correção própria: você vê a mudança e toca em **Mesclar correção**. Depois que ela é mesclada, a cópia antiga é descartada. Ou feche a tarefa.

## Seus arquivos mantidos por uma atualização

Quando uma nova versão traz um arquivo com o mesmo nome de um arquivo que você adicionou, a atualização renomeia o seu em vez de substituí-lo e continua. Uma tarefa informa quantos arquivos foram mantidos e lista cada nome antigo e novo. Feche a tarefa depois de conferir os nomes.

## O que ela pode fazer

Nada. Ela só lê o registro da sua própria Machine.

## Conectar

- Em uma Machine hospedada, ela aparece na página de configuração, em **Mais fontes**, como Saúde da Machine. Uma por Machine.
- No seu computador: execute `assistant connect gateway`.

## Remover

- No painel: **Conexões**, abra a conexão, toque em **Detalhes** e depois em **Desconectar**.
- Em uma Machine hospedada, você também pode tocar em **Remover** ao lado dela na página de configuração.

Não há nada para desinstalar em nenhum outro lugar.
