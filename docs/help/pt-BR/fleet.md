---
title: Fleets
area: fleet
summary: Um Fleet de Trabalho para sua equipe, um Fleet de Família para casa. Machines que se ajudam, com o seu sim em cada resposta.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV
order: 1
---
A The Machine Network conecta Machines. O que elas dizem umas às outras é criptografado de ponta a ponta, e cada Machine só responde seguindo as suas regras.

## Tipos de Fleet

- **Fleet de Trabalho**: sua equipe. Passe trabalho adiante, pergunte quem conhece alguém, consiga apresentações e um resumo da equipe.
- **Fleet de Família**: até 6 pessoas. Quando todo mundo está livre, tarefas e planos compartilhados. Grátis. Veja [Família](family.md).
- **Amigos**: qualquer pessoa na The Machine, uma por uma. Grátis. Veja [Amigos](friends.md).

## A aba Fleet

Ela aparece quando você está em um Fleet, com um painel para cada Fleet, Família, Amigos, Network, Compartilhamento e Atividade.

## Pergunte ao seu Fleet

Pergunte "quem conhece alguém na Acme?" na aba Fleet, ou use **Perguntar ao Fleet** em uma organização no [Graph](graph.md). A Machine de cada colega responde seguindo as regras de compartilhamento dessa pessoa, e pergunta a ela primeiro quando a regra pede.

## Pedidos de resumo da equipe

Um colega com o resumo da equipe ativado pede à sua Machine números e datas toda manhã. Isso nunca vira uma tarefa. O pedido espera na aba Fleet, no painel do seu Fleet de Trabalho, em **Pedidos de resumo da equipe**: **Compartilhar uma vez**, **Sempre compartilhar**, **Recusar** ou **Nunca**. Só o último pedido de cada colega espera, e os sem resposta expiram. Nada é compartilhado até você escolher.

## Team Graph

Em um Fleet de Trabalho, o trabalho com clientes é compartilhado com sua equipe depois que você revisa. Veja [Graph da equipe](team-graph.md).

## O que sua Machine responde

Defina isso por Fleet, no painel Compartilhamento. Veja [Regras de compartilhamento](sharing-rules.md). **Configurações** tem um atalho: **Regras do Fleet**.

## Login da empresa

Para um Fleet de Trabalho hospedado. Um proprietário ou admin conectado com uma conta Google Workspace ou Microsoft 365 da empresa pode ativar **Login da empresa** na página Conta. Ele usa o domínio dessa conta.

Colegas que entram com uma conta desse domínio passam a ver **Pedir para entrar**. Um proprietário ou admin precisa **Aprovar** cada pedido. Contas pessoais do Gmail e do Outlook.com nunca contam.

Remover alguém do Fleet desconecta essa pessoa em todos os lugares.

Para entrar em um Fleet, criar um ou parear uma Machine no seu próprio computador, veja [Planos e cobrança](plans-and-billing.md) e [Amigos e a Network](friends.md).

## Para proprietários e admins

A parte do Fleet na página da sua conta mostra mais duas coisas:

- **Removidos recentemente**: cada pessoa removida ou que saiu. Mostra **Removido, confirmado** quando a Machine dela removeu os dados de trabalho, o Google confirmou a saída e qualquer token compartilhado que ela tinha foi trocado. Até lá, mostra **Pendente** e o motivo.
- **Atividade**: quem fez o quê e quando. Convites, entradas, remoções, funções, servidores e cobrança, conectores compartilhados e aprovações. Também lista cada vez que nossa equipe abriu o servidor de um membro ou os logs dele. Nunca o conteúdo das mensagens. **Baixar CSV** exporta tudo. Guardado por 12 meses.

Depois de **Parar de compartilhar**, um conector compartilhado mostra **Removido, confirmado** quando todas as Machines excluírem o token.
