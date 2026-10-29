---
title: Fleets
area: fleet
summary: Um Fleet de Trabalho para sua equipe, um Fleet de Família para casa. Machines que se ajudam, seguindo suas regras de compartilhamento.
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

## Respondido sozinho em um Fleet de Trabalho

Em um Fleet de Trabalho Padrão, sua Machine responde sozinha a **quem conhece alguém**, **contexto de reunião** ("quem é este convidado?") e **quem cuida dos e-mails compartilhados** de um colega. Ela usa só o que o [Graph da equipe](team-graph.md) já compartilha. Conversas privadas, pessoais e sensíveis nunca contam, e só há nomes de pessoas que ele já compartilha. Cada resposta fica na aba Fleet, em **Atividade**.

Para parar uma delas, defina como **Nunca** em **Compartilhamento**. Uma regra salva como **Perguntar antes** agora funciona como **Sempre**. Enquanto o compartilhamento do Graph da equipe do seu Fleet está desligado, quem conhece alguém e contexto de reunião continuam perguntando a você antes.

Fleets de Trabalho Cuidadosos, Amigos e Família continuam perguntando a você antes. Apresentações, passagens de trabalho, acompanhamentos compartilhados e perguntas livres mantêm suas próprias regras.

## Aprendizados da equipe

No máximo uma vez por dia, sua Machine lê algumas conversas com clientes que o Graph da equipe já compartilha e anota como a equipe trabalha. Por exemplo: "Pedidos de reembolso são respondidos pela caixa de suporte com o modelo de reembolso." Eles aparecem no painel do seu Fleet de Trabalho, em **Aprendizados da equipe**, para todos no Fleet, e cada um fica em **Atividade**. Ninguém é consultado antes.

- Só conversas em que alguém da sua equipe escreveu. Nunca as privadas, pessoais ou sensíveis.
- Só o que vale para vários clientes: um processo, uma ferramenta, um estilo de escrita ou quem cuida do quê. Nunca algo sobre um só cliente, nunca feedback sobre o seu próprio produto, e nunca nomes, endereços, números ou citações.
- Cada um tem um rótulo: que tipo é, que veio de conversas da equipe e que é para este Fleet. Os que ela não tem certeza são descartados.

Qualquer pessoa no Fleet pode **Remover** um aprendizado. Ele some para todos e não é criado de novo. Para parar, desative **Oferecer compartilhar aprendizados** em Configurações, Segurança. Fleets de Trabalho Cuidadosos não recebem nenhum.

## Pedidos de resumo da equipe

Um colega com o resumo da equipe ativado pede à sua Machine números e datas toda manhã. Em um Fleet de Trabalho, ela responde sozinha, só com o que o [Graph da equipe](team-graph.md) já compartilha. Conversas privadas e pessoais nunca contam, e nada vai enquanto o compartilhamento do Graph da equipe está desligado. Cada resposta fica na aba Fleet, em **Atividade**. Isso nunca vira uma tarefa nem uma notificação.

Para parar, desative **Compartilhar meus dados do resumo com a equipe** na aba Fleet, em **Compartilhamento**. O resumo do colega então mostra você como sem resposta.

Em um Fleet Cuidadoso, os pedidos esperam por você na aba Fleet, em **Pedidos de resumo da equipe**: **Compartilhar uma vez**, **Sempre compartilhar**, **Recusar** ou **Nunca**. Só o último pedido de cada colega espera, e os sem resposta expiram. Nada é compartilhado até você escolher.

## Team Graph

Em um Fleet de Trabalho, o trabalho com clientes é compartilhado com sua equipe depois que você revisa. Veja [Graph da equipe](team-graph.md).

## Conexões compartilhadas

Um proprietário ou admin pode conectar o Stripe ou o Intercom uma vez e compartilhar com a equipe, pela caixa **Conexões compartilhadas** da aba Fleet. As Machines dos colegas leem, só leitura, e veem quem compartilhou. Só admins mudam ou param. Veja [Stripe](stripe.md) e [Intercom](intercom.md).

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
- **Atividade**: quem fez o quê e quando. Convites, entradas, remoções, funções, Machines hospedadas e cobrança, conectores compartilhados e aprovações. Também lista cada vez que nossa equipe abriu a Machine de um membro ou os logs dela. Nunca o conteúdo das mensagens. **Baixar CSV** exporta tudo. Guardado por 12 meses.

Depois de **Parar de compartilhar**, um conector compartilhado mostra **Removido, confirmado** quando todas as Machines excluírem o token.
