---
title: O Graph
area: graph
summary: As pessoas, organizações e projetos das suas mensagens, sempre atualizados automaticamente.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 181ff5fa2a9d8f47
---
Sua Machine cria um mapa das pessoas com quem você se relaciona e do que está acontecendo, com base nas suas mensagens, reuniões e decisões. Não precisa configurar nada, e tudo fica na sua Machine.

- [Pessoas](people.md): todas as pessoas com quem você mantém contato, com um resumo e uma linha do tempo para cada uma.
- [Organizações](organizations.md): as empresas onde elas trabalham, com suas pessoas e projetos.
- [Projetos](projects.md): o que está acontecendo, em quadros com etapas, como negócios em um CRM.

Suas próprias alterações aparecem na hora. Novas pessoas, novas mensagens nas linhas do tempo e detalhes pesquisados aparecem em até 30 minutos.

## Atualizado hoje

Uma linha discreta no topo de cada lista mostra o que sua Machine atualizou hoje, como **4 pessoas atualizadas hoje**. Toque nela para ver quem e o que mudou. Ao tocar em um nome, a página da pessoa abre com **Mudanças recentes**. Um pequeno ponto marca cada linha e cartão do quadro que mudou hoje. A contagem inclui apenas as alterações feitas pela sua Machine desde a meia-noite.

## Filtrar e ordenar

**Filtrar**, ao lado das abas, reduz os resultados da lista. Cada lista tem seus próprios filtros. Pessoas: proximidade, último contato, organização, proprietário, tag e **Tem um projeto aberto**. Organizações: setor, especialidade, porte, país, último contato, proprietário, tag e **Tem um projeto aberto**. Projetos: proprietário, quadro, etapa, tag, organização, valor, data prevista de fechamento e **Sem resposta há mais de 10 dias**.

Os filtros escolhidos aparecem acima da lista, com **Limpar**. Em Projetos, a lista e o quadro usam o mesmo filtro. No celular, os filtros abrem em uma janela deslizante.

O menu de ordenação organiza a lista. Pessoas e Organizações podem ser ordenadas por proximidade, contato mais recente ou mais antigo e nome. Organizações também podem ser ordenadas por porte. Projetos podem ser ordenados por atividade mais recente, nome, etapa, **Valor** e **Data de fechamento**. **Baixar CSV**, abaixo do menu de ordenação, salva a aba aberta como uma planilha.

## Campos e tags

Em Campos, na página de uma pessoa, organização ou projeto, clique em um valor para alterá-lo: **Salvar** ou Enter confirma, **Cancelar** ou Escape descarta, e **Remover** apaga o valor.

**Gerenciar campos** (**Adicionar um campo** quando ainda não houver nenhum) adiciona ou remove campos de todos os registros daquele tipo. **Novo campo** adiciona um campo de texto, número, data ou com opções de uma lista.

**+ Tag** adiciona uma tag, como VIP ou parceiro. **×** remove a tag. As tags aparecem nas listas. No celular, as tags de uma pessoa aparecem na página dela. **Filtrar** permite encontrá-las.

## Aniversário

O aniversário de uma pessoa aparece em Contato, junto com a origem: o contato dela no Google, um aniversário no Google Calendar (a rotina de aniversários salva essa informação para contatos próximos), uma importação do Facebook, suas anotações ou você. **Editar** define ou corrige a data: mês e dia, e o ano, se você souber. Nesse caso, a idade também aparece.

A data informada por você prevalece sobre todas as outras fontes e não muda. **Remover** apaga a data. Ela não volta a aparecer mesmo que esteja em um contato ou em uma importação.

Se não houver uma data, **Adicionar aniversário**, em Campos, permite adicioná-la. A rotina de aniversários usa a mesma data exibida na página. O aniversário é pessoal e nunca é compartilhado com sua equipe, mesmo em um registro compartilhado.

## Importar uma planilha

**Importar CSV…**, no menu de ordenação de Pessoas, Organizações ou Projetos, adiciona uma planilha salva como CSV.

1. Confira as colunas. Sua Machine tenta identificar cada uma pelos cabeçalhos e pelo conteúdo. Você pode alterar qualquer identificação. Quando seu modelo puder ser executado, ele também verifica as colunas e explica brevemente quando não tem certeza. Ele vê apenas os cabeçalhos, alguns valores de cada coluna e as células que as regras não conseguiram interpretar.
2. Confira as correções. **Revisar** mostra cada valor original e corrigido: espaços extras, nomes em letras maiúsculas, números de telefone no formato internacional, erros de digitação em e-mails (gmial.com), sites no formato de domínio, datas e valores em qualquer formato ("€12k" equivale a 12000), várias tags em uma célula, uma etapa escrita de outra forma e linhas duplicadas. Desmarque um tipo de correção ou uma linha para mantê-la como está.
3. Confira a prévia. Cada linha será adicionada, corresponderá a um registro que já existe no seu Graph ou será ignorada, com uma explicação. Uma pessoa corresponde pelo e-mail (ou pelo nome e pela organização, se não houver e-mail); uma organização, pelo site ou pelo nome; e um projeto, pelo nome.
4. **Importar** adiciona os novos registros e preenche os que correspondem aos existentes. Células vazias não alteram nada.

Use **Desfazer** logo depois da importação ou **Desfazer última importação**, no menu de ordenação, para reverter a última importação, desde que esses registros não tenham mudado. Se isso substituir uma correção feita depois, a mensagem explica o motivo. O arquivo fica na sua Machine.

## Proprietário

Em um Fleet de Trabalho, cada pessoa, organização e projeto tem um proprietário. Essa informação aparece em **Proprietário**, em Com você, na página do registro. O proprietário é você, a menos que escolha alguém do seu Fleet de Trabalho. **Proprietário** em Filtrar mostra apenas os seus registros. Cada alteração aparece na linha do tempo.

## Equipe

**Equipe**, ao lado de Meu, mostra o que seus colegas de equipe compartilham, com as mesmas abas e o mesmo menu de ordenação. **Filtrar** permite restringir os resultados por quem compartilhou, por organização (Pessoas) ou por estado (Projetos). O que você adicionar ali será seu.

O trabalho com clientes é compartilhado com as Machines dos seus colegas de equipe, incluindo o proprietário, os campos e as tags. O que eles compartilham também aparece na sua. Cada conversa mostra **Equipe** ou **Só você**. Saiba mais em [Graph da equipe](team-graph.md).
