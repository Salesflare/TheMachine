---
title: Dados da organização
area: graph
summary: Setor, porte, localização e um logotipo ao lado de cada organização, consultados pelo endereço do site.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: 1690f417d7a70829
---
## De onde vêm os dados

- Em uma Machine hospedada, os dados da organização são consultados para você, sem custo.
- No seu próprio computador, esse recurso fica desativado até você adicionar uma chave de um serviço de consulta, como Apollo, People Data Labs ou Hunter. Consulte o [guia de configuração](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Só o endereço do site da organização é enviado, nunca suas mensagens nem quem você conhece lá. Uma Machine hospedada ou uma Machine na The Machine Network pode fazer até 1.000 consultas por dia. Nos outros casos, o limite é de 50. Os dados de cada organização são atualizados a cada 90 dias. Sites compartilhados e provedores de e-mail, como gmail.com, nunca são consultados. A consulta de pessoas funciona de outro jeito: consulte [Cargo e foto](people.md#job-title-and-photo).

Se a consulta não encontrar um logotipo, The Machine usa o ícone indicado pelo site da organização e o salva na sua Machine. Nenhum serviço de logotipos fica sabendo com quem você trabalha. Quando há os dois, espaços pequenos, como a linha de uma tarefa, exibem o ícone quadrado.

Quando disponíveis na consulta, até 5 especialidades da organização aparecem abaixo da descrição. Também é possível filtrar a lista de organizações por uma delas: **Filtrar** e depois **Especialidade**. Quando a consulta de uma pessoa também traz os dados da empresa, esses dados preenchem a organização, sem necessidade de uma consulta própria. Os dados consultados nos últimos 90 dias não mudam.

## Corrigir uma organização

Na página da organização:

- **Editar** para mudar o nome, o setor, o porte, a localização, o ano de fundação, a descrição, o site, o LinkedIn, as notas e o que ela representa para você. Suas alterações são mantidas. Apague o conteúdo de um campo para voltar a usar o valor consultado.
- **Empresa errada, apagar detalhes**, em **Editar**, se a consulta encontrou a empresa errada.
- **Buscar de novo**, que aparece depois que os dados são apagados, busca dados atualizados.
