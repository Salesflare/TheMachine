---
title: O Graph
area: graph
summary: As pessoas, organizações e projetos nas suas mensagens, sempre atualizados automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Sua Machine cria um mapa das pessoas com quem você se relaciona e do que está acontecendo, com base nas suas mensagens, reuniões e decisões. Não precisa configurar nada, e tudo fica na sua Machine.

- [Pessoas](people.md): todas as pessoas com quem você mantém contato, com um resumo e uma linha do tempo de cada uma.
- [Organizações](organizations.md): as empresas onde elas trabalham, com as pessoas e os projetos de cada uma.
- [Projetos](projects.md): o que está acontecendo, em quadros com etapas, como oportunidades em um CRM.

## Atualizado hoje

Uma linha discreta no topo de cada lista mostra o que sua Machine atualizou hoje, como **4 pessoas atualizadas hoje**. Toque nela para ver quem e o que mudou. Ao tocar em um nome, você abre a página da pessoa com **Mudanças recentes** abertas. Um pequeno ponto marca cada linha e bloco do quadro que mudou hoje. São contabilizadas apenas as mudanças feitas pela sua Machine, desde meia-noite.

## Filtrar e ordenar

**Filtrar**, ao lado das abas, reduz a lista. Cada lista tem seus próprios filtros. Pessoas: proximidade, último contato, organização, proprietário, tag e **Tem um projeto aberto**. Organizações: setor, especialidade, tamanho, país, último contato, proprietário, tag e **Tem um projeto aberto**. Projetos: proprietário, quadro, etapa, tag, organização, valor, data prevista de fechamento e **Sem resposta há mais de 10 dias**.

Os filtros selecionados aparecem acima da lista, junto de **Limpar**. Em Projetos, a lista e o quadro usam o mesmo filtro. No celular, os filtros abrem em uma folha.

O menu de ordenação organiza a lista. Pessoas e Organizações podem ser ordenadas por proximidade, contato mais recente ou mais antigo e nome. Organizações também podem ser ordenadas por tamanho. Projetos podem ser ordenados por atividade mais recente, nome, etapa, **Valor** e **Data de fechamento**. **Baixar CSV**, abaixo do menu de ordenação, salva a aba aberta como planilha.

## Campos e tags

Em **Campos**, na página de uma pessoa, organização ou projeto, clique em um valor para alterá-lo: **Salvar** ou Enter confirma, **Cancelar** ou Escape cancela, e **Remover** apaga o valor.

**Gerenciar campos** (**Adicionar um campo** quando não houver nenhum) adiciona ou remove campos de todos os registros daquele tipo. **Novo campo** adiciona um campo de texto, número, data ou seleção de uma lista.

**+ Tag** adiciona uma tag, como VIP ou parceiro. **×** remove a tag. As tags aparecem nas listas, e **Filtrar** permite encontrá-las.

## Aniversário

O aniversário de uma pessoa aparece em **Contato**, junto da origem: o contato do Google, um aniversário no Google Calendar (a rotina de aniversários salva essa informação para contatos próximos), uma importação do Facebook, suas anotações ou você. **Editar** permite definir ou corrigir a data: mês e dia, além do ano, se você souber. Nesse caso, a idade também aparece.

A data informada por você tem prioridade sobre todas as outras fontes e permanece. **Remover** apaga a data. Ela não volta a ser adicionada por um contato ou uma importação.

Se não houver aniversário, **Adicionar aniversário**, em Campos, permite incluí-lo. A rotina de aniversários lê a mesma data que aparece na página. O aniversário é uma informação pessoal: nunca é compartilhado com sua equipe, nem mesmo em um registro compartilhado.

## Importar uma planilha

**Importar CSV…**, abaixo do menu de ordenação de Pessoas, Organizações ou Projetos, adiciona uma planilha salva como CSV.

1. Confira as colunas. Sua Machine tenta identificar cada uma pelos cabeçalhos e pelo conteúdo. Você pode alterar qualquer identificação. Quando seu modelo puder ser executado, ele também confere as colunas e informa brevemente quando não tem certeza. Ele vê apenas os cabeçalhos, alguns valores por coluna e as células que as regras não conseguiram interpretar.
2. Confira as correções. **Revisar** mostra cada alteração, antes e depois: espaços extras, nomes em maiúsculas, números de telefone no formato internacional, erros de digitação em e-mails (gmial.com), sites convertidos para o domínio, datas e valores em qualquer formato ("€12k" é 12000), várias tags em uma célula, uma etapa escrita de outra forma e linhas duplicadas. Desmarque um tipo de correção ou uma linha para mantê-la como está.
3. Confira a prévia. Cada linha é nova, corresponde a um registro que já existe no Graph ou será ignorada, com o motivo. Uma pessoa é identificada pelo e-mail (ou, se não houver, pelo nome e pela organização); uma organização, pelo site ou nome; um projeto, pelo nome.
4. **Importar** adiciona os novos registros e preenche os correspondentes. Uma célula vazia não altera nada.

**Desfazer**, logo após a importação, ou **Desfazer última importação**, abaixo do menu de ordenação, reverte a última importação, desde que esses registros não tenham sido alterados. Se isso substituir uma correção feita depois, a ferramenta explica o motivo. O arquivo permanece na sua Machine.

## Proprietário

Em uma Fleet de trabalho, cada pessoa, organização e projeto tem um proprietário: **Proprietário**, em **Com você**, na página do registro. O proprietário é você, a menos que escolha alguém da sua Fleet de trabalho. **Proprietário** em **Filtrar** mostra apenas os registros que são seus. Cada alteração aparece na linha do tempo.

## Equipe

**Equipe**, ao lado de **Minhas**, mostra o que seus colegas de equipe compartilharam, com as mesmas abas e o mesmo menu de ordenação. **Filtrar** permite restringir por quem compartilhou, por uma organização (em Pessoas) ou pelo status (em Projetos). O que você adicionar ali será seu.

O trabalho com clientes é compartilhado com as Machines dos seus colegas de equipe, incluindo o proprietário, os campos e as tags. O trabalho deles também aparece na sua. Cada conversa mostra **Equipe** ou **Só você**. Consulte [Graph da equipe](team-graph.md).
