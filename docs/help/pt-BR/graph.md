---
title: Graph
area: graph
summary: As pessoas, organizações e projetos nas suas mensagens, sempre atualizados automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: e437109f98725e65
---
Sua Machine cria um mapa de com quem você se relaciona e do que está acontecendo, com base nas suas mensagens, reuniões e decisões. Não precisa configurar nada, e tudo fica na sua Machine.

- [Pessoas](people.md): todas as pessoas com quem você tem contato, com um resumo e uma linha do tempo para cada uma.
- [Organizações](organizations.md): as empresas onde elas trabalham, com as pessoas e os projetos de cada uma.
- [Projetos](projects.md): o que está acontecendo, em quadros com etapas, como negócios em um CRM.
- [Notas](notes.md): uma página fácil de ler para cada assunto, como uma viagem ou a sua Casa.

## Atualizado hoje

Uma mensagem discreta no topo de cada lista mostra o que sua Machine atualizou hoje, como **4 pessoas atualizadas hoje**. Toque nela para ver quem e o que mudou. Toque em um nome para abrir a página da pessoa com **Mudanças recentes** abertas. Um ponto pequeno marca cada linha e cada item do quadro que mudou hoje. A contagem considera apenas as mudanças feitas pela sua Machine, desde a meia-noite.

## Filtrar e ordenar

**Filtrar**, ao lado das abas, reduz a lista. Cada lista tem seus próprios filtros. Pessoas: proximidade, último contato, organização, proprietário, tag e **Tem um projeto aberto**. Organizações: setor, especialidade, tamanho, país, último contato, proprietário, tag e **Tem um projeto aberto**. Projetos: proprietário, quadro, etapa, tag, organização, valor, data prevista de fechamento e **Sem resposta há mais de 10 dias**.

Os filtros selecionados aparecem acima da lista, junto com **Limpar**. Em Projetos, a lista e o quadro compartilham o mesmo filtro. No celular, os filtros abrem em uma folha.

O menu de ordenação organiza a lista. Pessoas e Organizações podem ser ordenadas por proximidade, contato mais recente ou mais antigo e nome. Organizações também podem ser ordenadas por tamanho. Projetos podem ser ordenados por atividade mais recente, nome, etapa, **Valor** e **Data de fechamento**. **Baixar CSV**, abaixo do menu de ordenação, salva a aba aberta como uma planilha.

## Campos e tags

Em Campos, na página de uma pessoa, organização ou projeto, clique em um valor para alterá-lo: **Salvar** ou Enter confirma, **Cancelar** ou Escape descarta e **Remover** apaga o valor.

**Gerenciar campos** (**Adicionar um campo** quando ainda não houver nenhum) adiciona ou remove campos de todos os registros desse tipo. **Novo campo** adiciona um campo: texto, número, data ou uma opção de uma lista.

**+ Tag** adiciona uma tag, como VIP ou parceiro. **×** remove a tag. As tags aparecem nas listas e você pode encontrá-las com **Filtrar**.

## Aniversário

O aniversário de uma pessoa aparece em Contato, junto com a origem da informação: o contato dela no Google, um aniversário no Google Calendar (a rotina de aniversários salva a data para contatos próximos), uma importação do Facebook, suas notas ou você. **Editar** permite definir ou corrigir a data: mês e dia, e o ano se você souber (nesse caso, a idade também aparece).

A data que você informar tem prioridade sobre todas as outras fontes e permanece salva. **Remover** apaga a data. Ela não volta a ser adicionada por um contato ou uma importação.

Se não houver uma data, **Adicionar aniversário**, em Campos, permite adicioná-la. A rotina de aniversários usa a mesma data que aparece na página. O aniversário é uma informação pessoal: nunca é compartilhado com sua equipe, mesmo em um registro compartilhado.

## Importar uma planilha

**Importar CSV…**, no menu de ordenação de Pessoas, Organizações ou Projetos, adiciona uma planilha salva como CSV.

1. Confira as colunas. Sua Machine tenta identificar cada uma pelos cabeçalhos e pelo conteúdo. Você pode alterar qualquer identificação. Quando seu modelo puder ser executado, ele também verifica as colunas e explica brevemente quando não tem certeza. Ele vê apenas os cabeçalhos, alguns valores por coluna e as células que as regras não conseguiram ler.
2. Confira as correções. **Revisar** mostra cada valor antes e depois: espaços extras, nomes em maiúsculas, números de telefone no formato internacional, erros de digitação em e-mails (gmial.com), sites convertidos para o domínio, datas e valores em qualquer formato ("€12k" é 12000), várias tags em uma célula, uma etapa escrita de outra forma e linhas repetidas. Desmarque um tipo ou uma linha para deixá-lo como está.
3. Confira a prévia. Cada linha é nova, corresponde a um registro existente no seu Graph ou será ignorada, com o motivo. Uma pessoa corresponde pelo e-mail (ou, se não houver, pelo nome e pela organização); uma organização, pelo site ou pelo nome; um projeto, pelo nome.
4. **Importar** adiciona os novos registros e preenche os correspondentes. Uma célula vazia não altera nada.

Use **Desfazer** logo após a importação ou **Desfazer última importação**, no menu de ordenação, para revertê-la, desde que esses registros não tenham sido alterados desde então. Se isso substituir uma correção feita depois, a mensagem explica o motivo. O arquivo permanece na sua Machine.

## Proprietário

Em uma Fleet de trabalho, cada pessoa, organização e projeto tem um proprietário: **Proprietário**, em Com você, na página do registro. O proprietário é você, a menos que escolha alguém da sua Fleet de trabalho. **Proprietário** em Filtrar mostra apenas os registros seus. Cada alteração aparece na linha do tempo.

## Equipe

**Equipe**, ao lado de Meus, mostra o que as pessoas da sua equipe compartilharam, com as mesmas abas e o mesmo menu de ordenação. **Filtrar** permite restringir por quem compartilhou, por organização (Pessoas) ou por estado (Projetos). O que você adicionar ali será seu.

O trabalho com clientes é compartilhado com as Machines das pessoas da sua equipe, junto com o proprietário, os campos e as tags. O que elas compartilham aparece na sua Machine. Cada conversa mostra **Equipe** ou **Só você**. Saiba mais em [Graph da equipe](team-graph.md).
