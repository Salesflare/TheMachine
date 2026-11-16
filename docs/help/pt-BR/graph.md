---
title: The Graph
area: graph
summary: As pessoas, organizações e projetos nas suas mensagens, sempre atualizados automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Sua Machine cria um mapa de quem você conhece e do que está acontecendo com base nas suas mensagens, reuniões e decisões. Não é preciso configurar nada, e tudo fica na sua Machine.

- [Pessoas](people.md): todas as pessoas com quem você mantém contato, com um resumo e uma linha do tempo para cada uma.
- [Organizações](organizations.md): as empresas onde elas trabalham, com as pessoas e os projetos de cada uma.
- [Projetos](projects.md): o que está acontecendo, em quadros com etapas, como negócios em um CRM.

## Atualizado hoje

Uma linha discreta no topo de cada lista mostra o que sua Machine atualizou hoje, como **4 pessoas atualizadas hoje**. Toque nela para ver quem e o que mudou. Ao tocar em um nome, a página da pessoa abre com **Mudanças recentes** abertas. Um pequeno ponto marca cada linha e bloco do quadro que mudou hoje. A contagem considera apenas as mudanças feitas pela sua Machine desde a meia-noite.

## Filtrar e ordenar

**Filtrar**, ao lado das abas, restringe a lista. Cada lista tem seus próprios filtros. Pessoas: proximidade, último contato, organização, proprietário, tag e **Tem um projeto aberto**. Organizações: setor, especialidade, tamanho, país, último contato, proprietário, tag e **Tem um projeto aberto**. Projetos: proprietário, quadro, etapa, tag, organização, valor, data prevista de fechamento e **Sem resposta há mais de 10 dias**.

Os filtros selecionados aparecem acima da lista, junto de **Limpar**. Em Projetos, a lista e o quadro compartilham o mesmo filtro. No celular, eles abrem em uma janela deslizante.

O menu de ordenação organiza a lista. Pessoas e Organizações podem ser ordenadas por proximidade, contato mais recente ou mais antigo e nome. Organizações também podem ser ordenadas por tamanho. Projetos podem ser ordenados por atividade mais recente, nome, etapa, **Valor** e **Data de fechamento**. **Baixar CSV**, abaixo do menu de ordenação, salva a aba aberta como planilha.

## Campos e tags

Em **Campos**, na página de uma pessoa, organização ou projeto, clique em um valor para alterá-lo: **Salvar** ou Enter confirma, **Cancelar** ou Escape descarta a alteração, e **Remover** apaga o valor.

**Gerenciar campos** (**Adicionar um campo** quando não houver nenhum) adiciona ou remove campos de todos os registros daquele tipo. **Novo campo** adiciona um campo: texto, número, data ou uma opção de uma lista.

**+ Tag** adiciona uma tag, como VIP ou parceiro. **×** remove a tag. As tags aparecem nas listas, e **Filtrar** permite encontrá-las.

## Aniversário

O aniversário de uma pessoa aparece em Contato, junto com a origem da informação: o contato do Google, um aniversário no Google Calendar (a rotina de aniversários salva essa informação para contatos próximos), uma importação do Facebook, suas anotações ou você. **Editar** permite definir ou corrigir a data: mês e dia, e o ano se você souber. Nesse caso, a idade também aparece.

A data informada por você tem prioridade sobre todas as outras fontes e é mantida. **Remover** apaga a data. Ela não volta a aparecer a partir de um contato ou de uma importação.

Se não houver uma data, **Adicionar aniversário**, em Campos, permite incluí-la. A rotina de aniversários usa a mesma data exibida na página. O aniversário é uma informação pessoal: nunca é compartilhado com sua equipe, mesmo em um registro compartilhado.

## Importar uma planilha

**Importar CSV…**, abaixo do menu de ordenação em Pessoas, Organizações ou Projetos, adiciona uma planilha salva como CSV.

1. Confira as colunas. Sua Machine tenta identificar cada uma pelos cabeçalhos e pelo conteúdo. Você pode alterar qualquer identificação. Quando seu modelo estiver disponível, ele também verifica as colunas e explica brevemente quando tiver dúvidas. O modelo só vê os cabeçalhos, alguns valores de cada coluna e as células que as regras não conseguiram ler.
2. Confira as correções. **Revisar** mostra cada alteração, com o antes e o depois: espaços extras, nomes em maiúsculas, números de telefone no formato internacional, erros de digitação em e-mails (gmial.com), sites convertidos para o domínio, datas e valores em qualquer formato ("€12k" equivale a 12000), várias tags em uma célula, uma etapa escrita de outro jeito e linhas duplicadas. Desmarque um tipo de correção ou uma linha para mantê-la como está.
3. Confira a prévia. Cada linha será adicionada, corresponde a um registro que já existe no seu Graph ou será ignorada, com uma explicação. Uma pessoa é identificada pelo e-mail (ou pelo nome e pela organização, se não houver e-mail), uma organização pelo site ou pelo nome e um projeto pelo nome.
4. **Importar** adiciona os novos registros e preenche os correspondentes. Uma célula vazia não altera nada.

Use **Desfazer** logo após a importação ou **Desfazer última importação**, abaixo do menu de ordenação, para reverter a última importação, desde que esses registros não tenham sido alterados depois. Se a reversão substituir uma correção feita posteriormente, uma explicação será exibida. O arquivo permanece na sua Machine.

## Proprietário

Em uma Fleet de trabalho, cada pessoa, organização e projeto tem um proprietário, exibido em **Com você**, na página do registro. O proprietário é você, a menos que escolha alguém da sua Fleet de trabalho. **Proprietário** em Filtrar mostra apenas os registros que pertencem a você. Cada alteração aparece na linha do tempo.

## Equipe

**Equipe**, ao lado de **Minha**, mostra o que seus colegas de equipe compartilharam, com as mesmas abas e o mesmo menu de ordenação. **Filtrar** permite restringir por quem compartilhou, por organização (em Pessoas) ou por estado (em Projetos). O que você adicionar ali será seu.

O trabalho com clientes é compartilhado com as Machines dos seus colegas de equipe, incluindo o proprietário, os campos e as tags. O que eles adicionarem também aparece na sua. Cada conversa mostra **Equipe** ou **Só você**. Veja [Graph da equipe](team-graph.md).
