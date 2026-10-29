---
title: Detalhes da organização
area: graph
summary: Setor, tamanho, local e um logo ao lado de cada organização, buscados pelo endereço do site dela.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 2
---
## De onde eles vêm

- Em uma Machine hospedada, os detalhes das organizações são buscados para você, sem custo.
- No seu próprio computador, isso fica desativado até você adicionar uma chave de um serviço de busca que você usa, como Apollo, People Data Labs ou Hunter. Veja o [guia de configuração](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Só o endereço do site da organização é enviado, nunca as suas mensagens nem quem você conhece lá. Algumas são buscadas por vez, no máximo 50 por dia, e atualizadas a cada 90 dias. As pessoas têm a própria busca: veja [Cargo e foto](graph.md#job-title-and-photo). Hospedagens compartilhadas e provedores de e-mail, como google.com, sites.google.com ou gmail.com, nunca são buscados: não são o site de uma empresa específica.

Quando a busca não traz logo, ou não há busca, o logo vem do próprio site da organização: o ícone que a página inicial indica. Ele fica salvo na sua Machine, então nenhum serviço de logos fica sabendo com quem você lida. Um site sem ícone é consultado de novo depois de 30 dias. Se a busca encontrou a organização mas não o logo, ela é feita mais uma vez depois de uma semana, e o logo que ela trouxer então substitui o ícone do site.

## Corrigir um detalhe errado

Na página da organização:

- **Editar** para mudar o nome, o setor, o tamanho, o local, o ano de fundação, a descrição, o site, o LinkedIn e o que ela é para você. Suas edições ficam. Esvazie um campo para usar de novo o valor buscado.
- **Empresa errada, apagar detalhes** se ele pegou a empresa errada.
- **Buscar de novo** para trazer detalhes atualizados.
