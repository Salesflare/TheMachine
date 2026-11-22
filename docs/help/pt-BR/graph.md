---
title: Graph
area: graph
summary: As pessoas, organizações e projetos nas suas mensagens, sempre atualizados automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 9052c679e45207f7
---
Sua Machine cria um mapa de quem você conhece e do que está acontecendo, com base nas suas mensagens, reuniões e decisões. Não precisa configurar nada, e tudo fica na sua Machine.

- [Pessoas](people.md): todas as pessoas com quem você mantém contato, com um resumo e uma linha do tempo de cada uma.
- [Organizações](organizations.md): as empresas onde elas trabalham, com suas pessoas e projetos.
- [Projetos](projects.md): o que está acontecendo, em quadros com etapas, como negócios em um CRM.

## Atualizado hoje

Uma linha discreta no topo de cada lista mostra o que sua Machine atualizou hoje, como **4 pessoas atualizadas hoje**. Toque nela para ver quem e o que mudou. Ao tocar em um nome, a página da pessoa abre com **Mudanças recentes**. Um pequeno ponto marca cada linha e bloco do quadro que mudou hoje. A contagem inclui apenas as mudanças feitas pela sua Machine desde a meia-noite.

## Filtrar e ordenar

**Filtrar**, ao lado das abas, restringe a lista. Cada lista tem seus próprios filtros. Pessoas: proximidade, último contato, organização, proprietário, tag e **Tem um projeto aberto**. Organizações: setor, especialidade, tamanho, país, último contato, proprietário, tag e **Tem um projeto aberto**. Projetos: proprietário, quadro, etapa, tag, organização, valor, data prevista de fechamento e **Sem resposta há mais de 10 dias**.

Os filtros escolhidos aparecem acima da lista, junto com **Limpar**. Em Projetos, a lista e o quadro compartilham o mesmo filtro. No celular, eles abrem em uma janela deslizante.

O menu de ordenação organiza a lista. Pessoas e Organizações podem ser ordenadas por proximidade, contato mais recente ou mais antigo e nome. Organizações também podem ser ordenadas por tamanho. Projetos podem ser ordenados por atividade mais recente, nome, etapa, **Valor** e **Data de fechamento**. **Baixar CSV**, no menu de ordenação, salva a aba aberta como uma planilha.

## Campos e tags

Em **Campos**, na página de uma pessoa, organização ou projeto, clique em um valor para alterá-lo. **Salvar** ou Enter confirma a alteração, **Cancelar** ou Escape sai sem salvar, e **Remover** apaga o valor.

**Gerenciar campos** (ou **Adicionar um campo**, quando não houver nenhum) adiciona ou remove campos de todos os registros desse tipo. **Novo campo** adiciona um campo de texto, número, data ou opções de uma lista.

**+ Tag** adiciona uma tag, como VIP ou parceiro. **×** remove a tag. As tags aparecem nas listas (no celular, as tags de uma pessoa aparecem na página dela) e **Filtrar** permite encontrá-las.

## Aniversário

O aniversário de uma pessoa aparece em Contato, junto com a origem: contato do Google, aniversário no Google Calendar (a rotina de aniversários salva essa data para contatos próximos), importação do Facebook, suas anotações ou você. **Editar** permite adicionar ou corrigir a data: mês e dia, e o ano, se souber (nesse caso, a idade também aparece).

A data informada por você tem prioridade sobre todas as outras fontes e não é removida. **Remover** apaga a data. Ela não volta a ser adicionada por um contato nem por uma importação.

Se a pessoa ainda não tiver uma data, **Adicionar aniversário**, em Campos, permite adicioná-la. A rotina de aniversários usa a mesma data que aparece na página. O aniversário é pessoal: nunca é compartilhado com sua equipe, mesmo em um registro compartilhado.

## Importar uma planilha

**Importar CSV…**, no menu de ordenação de Pessoas, Organizações ou Projetos, adiciona uma planilha salva como CSV.

1. Confira as colunas. Sua Machine tenta identificá-las pelos cabeçalhos e pelo conteúdo. Você pode alterar qualquer uma. Quando seu modelo puder ser executado, ele também verifica as colunas e explica brevemente os casos em que não tem certeza. Ele só vê os cabeçalhos, alguns valores de cada coluna e as células que as regras não conseguiram interpretar.
2. Confira as correções. **Revisar** mostra cada uma com o antes e o depois: espaços extras, nomes em maiúsculas, números de telefone no formato internacional, erros de digitação em e-mails (gmial.com), sites convertidos para o domínio, datas e valores em qualquer formato ("€12k" equivale a 12000), várias tags em uma célula, uma etapa escrita de outra forma e linhas duplicadas. Desmarque um tipo de correção ou uma linha para mantê-la como está.
3. Confira a prévia. Cada linha é identificada como nova, correspondente a algo que já existe no Graph ou ignorada, com uma explicação. Uma pessoa corresponde por e-mail (ou, se não houver, por nome e organização), uma organização por site ou nome e um projeto por nome.
4. **Importar** adiciona os novos registros e preenche os correspondentes. Uma célula vazia não altera nada.

**Desfazer** logo após a importação, ou **Desfazer última importação** no menu de ordenação, reverte a última importação, desde que esses registros não tenham mudado. Se isso substituir uma correção feita depois, uma mensagem explica o motivo. O arquivo permanece na sua Machine.

## Proprietário

Em um Fleet de Trabalho, cada pessoa, organização e projeto tem um proprietário: **Proprietário**, em **Com você** na página do registro. O proprietário é você, a menos que escolha alguém do seu Fleet de Trabalho. **Proprietário** em Filtrar mostra apenas os seus registros. Cada alteração aparece na linha do tempo.

## Equipe

**Equipe**, ao lado de **Meu**, mostra o que seus colegas de equipe compartilham, com as mesmas abas e o menu de ordenação. **Filtrar** restringe a lista por quem compartilhou, por organização (Pessoas) ou por estado (Projetos). O que você adicionar ali será seu.

O trabalho com clientes é compartilhado com as Machines dos seus colegas de equipe, junto com o proprietário, os campos e as tags. O que eles compartilham aparece na sua Machine. Cada conversa mostra **Equipe** ou **Só você**. Veja [Graph da equipe](team-graph.md).
