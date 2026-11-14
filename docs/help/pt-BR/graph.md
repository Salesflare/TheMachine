---
title: O Graph
area: graph
summary: As pessoas, organizações e projetos das suas mensagens, sempre atualizados automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 4dbe1a4e1702b1c1
---
Sua Machine cria um mapa das pessoas com quem você se relaciona e do que está acontecendo, com base nas suas mensagens, reuniões e decisões. Não é preciso configurar nada, e tudo fica na sua Machine.

- [Pessoas](people.md): todas as pessoas com quem você mantém contato, com um resumo e uma linha do tempo para cada uma.
- [Organizações](organizations.md): as empresas onde elas trabalham, com suas pessoas e projetos.
- [Projetos](projects.md): o que está acontecendo em quadros com etapas, como negócios em um CRM.

## Atualizado hoje

Uma linha discreta no topo de cada lista informa o que sua Machine atualizou hoje, como **4 pessoas atualizadas hoje**. Toque nela para ver quem e o que mudou. Ao tocar em um nome, você abre a página da pessoa com **Mudanças recentes** abertas. Um pequeno ponto marca cada linha e cartão do quadro que mudou hoje. A contagem inclui apenas as mudanças feitas pela sua própria Machine, desde a meia-noite.

## Filtrar e ordenar

**Filtrar**, ao lado das abas, reduz a lista. Cada lista tem seus próprios filtros. Pessoas: proximidade, último contato, organização, proprietário, tag e **Tem um projeto aberto**. Organizações: setor, especialidade, tamanho, país, último contato, proprietário, tag e **Tem um projeto aberto**. Projetos: proprietário, quadro, etapa, tag, organização, valor, data de fechamento prevista e **Sem resposta há mais de 10 dias**.

Os filtros escolhidos aparecem acima da lista, com **Limpar**. Em Projetos, a lista e o quadro compartilham o mesmo filtro. No celular, eles abrem em um painel deslizante.

O menu de ordenação permite ordenar a lista. Pessoas e Organizações podem ser ordenadas por proximidade, contato mais recente ou mais antigo e nome. Organizações também podem ser ordenadas por tamanho. Projetos também podem ser ordenados por **Valor** e **Data de fechamento**. **Baixar CSV**, abaixo do menu de ordenação, salva a aba aberta como uma planilha.

## Campos e tags

Em Campos, na página de uma pessoa, organização ou projeto, clique em um valor para alterá-lo: **Salvar** ou Enter confirma, **Cancelar** ou Escape cancela e **Remover** apaga o valor.

**Gerenciar campos** adiciona ou remove campos de todos os registros desse tipo. **Novo campo** adiciona um campo de texto, número, data ou com opções de uma lista.

**+ Tag** adiciona uma tag, como VIP ou parceiro. **×** remove a tag. As tags aparecem nas listas, e **Filtrar** permite encontrá-las.

## Aniversário

O aniversário de uma pessoa aparece em Contato, junto com a origem: o contato dela no Google, um aniversário no Google Calendar (a rotina de aniversários salva essa informação para contatos próximos), uma importação do Facebook ou você. **Editar** permite definir ou corrigir o aniversário: informe o mês e o dia e, se souber, o ano. Assim, a idade também aparece. O valor que você informa prevalece sobre todas as outras fontes e não é substituído. **Remover** apaga o aniversário. Ele não será adicionado novamente por um contato ou uma importação.

Se ainda não houver um aniversário, **Adicionar aniversário**, em Campos, permite adicioná-lo. A rotina de aniversários lê o mesmo aniversário que aparece na página. O aniversário é uma informação pessoal: nunca é compartilhado com sua equipe, mesmo em um registro compartilhado.

## Importar uma planilha

**Importar CSV…**, abaixo do menu de ordenação em Pessoas, Organizações ou Projetos, permite adicionar uma planilha salva como CSV.

1. Confira as colunas. Sua Machine tenta identificá-las com base nos cabeçalhos e no conteúdo. Você pode alterar qualquer uma delas. Quando o modelo estiver disponível, ele também verifica as colunas e explica brevemente quando não tem certeza. Ele só vê os cabeçalhos, alguns valores de cada coluna e as células que as regras não conseguiram ler.
2. Confira as correções. **Revisar** mostra o antes e o depois: espaços extras, nomes em letras maiúsculas, números de telefone no formato internacional, erros de digitação em e-mails (gmial.com), sites convertidos para o domínio, datas e valores em qualquer formato ("€12k" equivale a 12000), várias tags em uma célula, etapas escritas de forma diferente e linhas duplicadas. Desmarque um tipo de correção ou uma linha para mantê-la como está.
3. Confira a prévia. Cada linha aparece como nova, correspondente a um registro já existente no seu Graph ou ignorada, com o motivo. Uma pessoa é identificada pelo e-mail (ou pelo nome e pela organização, se não houver e-mail); uma organização, pelo site ou nome; e um projeto, pelo nome.
4. **Importar** adiciona os novos registros e preenche os que correspondem aos existentes. Uma célula vazia não altera nada.

**Desfazer** logo após a importação, ou **Desfazer última importação** abaixo do menu de ordenação, reverte a última importação, desde que os registros não tenham mudado desde então. Se a reversão substituir uma correção feita depois, a mensagem explica o motivo. O arquivo permanece na sua Machine.

## Proprietário

Em uma Fleet de trabalho, cada pessoa, organização e projeto tem um proprietário: **Proprietário**, em Com você, na página do registro. O proprietário é você, a menos que escolha alguém da sua Fleet de trabalho. **Proprietário** em Filtrar mostra apenas os registros seus. Cada alteração aparece na linha do tempo.

## Equipe

**Equipe**, ao lado de Minhas, mostra o que seus colegas compartilharam, com as mesmas abas e o mesmo menu de ordenação. **Filtrar** permite restringir por quem compartilhou, por organização (em Pessoas) ou por estado (em Projetos). O que você adicionar ali é seu.

O trabalho com clientes é compartilhado com as Machines dos seus colegas, junto com o proprietário, os campos e as tags. E o que eles compartilham aparece na sua. Cada conversa mostra **Equipe** ou **Só você**. Consulte [Graph da equipe](team-graph.md).
