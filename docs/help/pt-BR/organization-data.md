---
title: Detalhes da organização
area: graph
summary: Setor, porte, localização e um logotipo para cada organização, consultados pelo endereço do site.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: f403410953e50582
---
## De onde vêm os dados

- Em uma Machine hospedada, os detalhes da organização são consultados para você, sem custo.
- No seu próprio computador, esse recurso fica desativado até você adicionar uma chave de um serviço de consulta, como Apollo, People Data Labs ou Hunter. Consulte o [guia de configuração](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Só o endereço do site da organização é enviado, nunca suas mensagens nem quem você conhece nela. Uma Machine hospedada ou uma na The Machine Network faz até 1.000 consultas por dia. Nos outros casos, são até 50. Os dados são atualizados a cada 90 dias. Sites compartilhados e provedores de e-mail, como gmail.com, nunca são consultados. As pessoas têm uma consulta própria: veja [Cargo e foto](people.md#job-title-and-photo).

Se a consulta não encontrar um logotipo, The Machine usa o ícone do próprio site da organização, salvo na sua Machine. Nenhum serviço de logotipos fica sabendo com quem você trabalha. Quando tem os dois, espaços pequenos, como a linha de uma tarefa, mostram o ícone quadrado.

Quando a consulta encontra especialidades, até 5 delas aparecem abaixo da descrição. Também é possível filtrar a lista de organizações por uma delas: **Filtrar** e depois **Especialidade**. Quando a consulta de uma pessoa também traz os dados da empresa, eles preenchem os dados da organização, sem que ela precise de uma consulta própria. Os dados consultados nos últimos 90 dias permanecem como estão.

## Corrigir uma organização errada

Na página da organização:

- Use **Editar** para alterar o nome, setor, porte, localização, ano de fundação, descrição, site, LinkedIn, observações e sua relação com ela. Suas alterações são mantidas. Apague o conteúdo de um campo para voltar a usar o valor consultado.
- Se a empresa selecionada estiver errada, use **Empresa errada, apagar detalhes** em **Editar**.
- **Buscar de novo**, exibido depois que os dados são apagados, busca detalhes atualizados.
