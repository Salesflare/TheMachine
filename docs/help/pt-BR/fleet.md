---
title: Fleets
area: fleet
summary: Um Fleet de Trabalho para sua equipe, um Fleet da Família para casa. Machines que ajudam umas às outras, de acordo com suas regras de compartilhamento.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 17927ccd0e4aa40d
---
Um Fleet permite que sua Machine trabalhe com as Machines da sua equipe, família ou amigos pela The Machine Network. O que elas compartilham é criptografado de ponta a ponta, e sua Machine só responde de acordo com suas regras.

## Tipos de Fleet

- **Fleet de Trabalho**: sua equipe. Passe tarefas adiante, pergunte quem conhece alguém, receba apresentações e um resumo da equipe.
- **Fleet da Família**: até 6 pessoas. Quando todos estão livres, compartilhem tarefas e planos, e façam perguntas à Machine uns dos outros. É grátis; as Machines hospedadas nele têm preço familiar. Veja [Família](family.md).
- **Amigos**: qualquer pessoa na The Machine, uma de cada vez. É grátis. Veja [Amigos](friends.md).

## A aba Fleet

Ela aparece quando você entra em um Fleet, com um painel para cada Fleet, seguido de Amigos, Network, Compartilhamento e Atividade. Proprietários e admins também têm **Gerenciar**, e um Fleet de Trabalho que compartilha seu Graph também tem **O que é compartilhado**.

## Quanto custa, como sair e como criar um Fleet

Abaixo do nome de cada Fleet, **Quanto custa** mostra suas vagas, quem paga pela sua Machine e, para o proprietário, o cartão e as faturas do Fleet. **Sair deste Fleet** faz você sair dele; antes, o proprietário precisa passar o Fleet para outra pessoa. **Criar outro Fleet** inicia um novo.

Cada opção abre essa etapa da sua conta. Se houver uma mudança de preço, o valor aparece para você confirmar primeiro. Em uma Machine hospedada por você, elas abrem sua conta em uma nova aba, onde você entra.

## Pergunte ao seu Fleet

Pergunte “quem conhece alguém na Acme?” na aba Fleet ou use **Perguntar ao Fleet** em uma organização no [Graph](graph.md). A Machine de cada colega responde de acordo com as próprias regras de compartilhamento e pergunta a essa pessoa primeiro quando a regra exige.

Para qualquer outra coisa, use **Pergunte qualquer coisa** no painel do seu Fleet de Trabalho. Cada colega recebe um rascunho de resposta com base nas próprias contas de trabalho, e nada é compartilhado até que a pessoa envie. O rascunho considera apenas o que ela escreveu ou discutiu em reuniões. E-mails que só chegaram, como uma newsletter ou uma mensagem em cópia, aparecem como encontrados, mas não geram rascunho.

## Respostas automáticas em um Fleet de Trabalho

Em um Fleet de Trabalho padrão, sua Machine responde automaticamente a três tipos de perguntas dos colegas: **quem conhece alguém**, **contexto de reunião** (“quem é essa pessoa convidada?”) e **quem cuida dos e-mails compartilhados**. Ela usa apenas o que o [Graph da equipe](team-graph.md) já compartilha com sua equipe, nunca conversas privadas, pessoais ou sensíveis. Cada resposta aparece na aba Fleet, em **Atividade**.

Para parar isso, escolha **Nunca** em **Compartilhamento**. Uma regra definida como **Perguntar antes** funciona como **Sempre**. Enquanto o compartilhamento do Graph da equipe estiver desativado, as perguntas sobre quem conhece alguém e o contexto de reunião serão feitas primeiro a você.

Os Fleets de Trabalho cuidadosos, os Amigos e os Fleets da Família continuam perguntando a você primeiro. Apresentações, repasses e perguntas gratuitas seguem suas próprias regras.

## Aprendizados da equipe

Sua Machine registra como sua equipe trabalha, com base em conversas com clientes que o Graph da equipe já compartilha, no máximo uma vez por dia. Por exemplo: “Os pedidos de reembolso são respondidos pela caixa de entrada do suporte usando o modelo de reembolso.” Eles aparecem no painel do seu Fleet de Trabalho, em **Aprendizados da equipe**, para todas as pessoas do Fleet, e cada um fica registrado em **Atividade**. Ninguém precisa aprovar antes.

- Apenas conversas em que alguém da sua equipe escreveu. Nunca conversas privadas, pessoais ou sensíveis.
- Apenas informações que se aplicam a vários clientes: um processo, uma ferramenta, um estilo de escrita ou quem cuida de cada coisa. Nunca algo sobre um único cliente, comentários sobre seu próprio produto, nomes, endereços, números ou citações.
- Aprendizados sobre os quais ela não tem certeza são descartados.

Sua Machine usa os aprendizados relevantes ao preparar uma tarefa de trabalho para esta empresa. Seus dados, regras e habilidades vêm primeiro, e as tarefas pessoais nunca usam esses aprendizados. Uma tarefa que usou um deles informa isso, por exemplo: “Usou um aprendizado da equipe: os reembolsos são enviados pela caixa de entrada do suporte.” Toque em **Remover** para excluir o aprendizado de todo o Fleet.

Qualquer pessoa do Fleet pode **Remover** um aprendizado. Ele desaparece para todos e não é criado de novo. Para impedir isso, desative **Oferecer para compartilhar aprendizados** em **Configurações**, Segurança. Fleets de Trabalho cuidadosos não recebem aprendizados.

## Resumo da equipe

Escolha **Diário** ou **Semanal** para **Resumo da equipe** na aba Fleet, em **Compartilhamento**. Sua Machine então pede às Machines dos colegas números e datas. O que precisa da sua atenção aparece em Tarefas, em Trabalho: um cliente esperando por um colega, uma empresa sem novidades há duas semanas ou mais, duas pessoas da equipe escrevendo para os mesmos contatos ou uma reunião compartilhada.

- A tarefa informa quem precisa agir, desde quando, o que a pessoa pediu e o que está em jogo, como um projeto em andamento. Se não houver nada específico a dizer, ela fica no resumo, mas não vira uma tarefa.
- A empresa e os colegas têm links para suas páginas. **Detalhes** mostra o que escreveram (toque para ler), o que está em jogo, quem da equipe está em contato e as conversas mais recentes, apenas o que o [Graph da equipe](team-graph.md) compartilha.
- Se o que escreveram estiver apenas no e-mail de um colega, a tarefa informa quem você deve consultar.
- **Perguntar à equipe** envia uma pergunta já preenchida sobre o assunto. As respostas aparecem na tarefa.
- **Não precisa** fecha a tarefa, e o resumo aprende com isso. Ela só volta se houver novidades.
- Quando alguém responde ou assume a tarefa, ela é fechada automaticamente. Uma tarefa sobre uma empresa para a qual você já tem uma tarefa é adicionada a essa tarefa.

## Pedidos de resumo da equipe

Todas as manhãs, a Machine de um colega com o resumo da equipe ativado pede à sua Machine números e datas. Em um Fleet de Trabalho, sua Machine responde automaticamente usando apenas o que o [Graph da equipe](team-graph.md) já compartilha. Ela não responde quando o compartilhamento do Graph da equipe está desativado. Cada resposta aparece na aba Fleet, em **Atividade**, nunca como tarefa ou notificação.

Para parar, desative **Compartilhar meus dados do resumo com a equipe** na aba Fleet, em **Compartilhamento**. Seu nome aparecerá no resumo da equipe como alguém que não respondeu.

Em um Fleet cuidadoso, os pedidos ficam na aba Fleet, em **Pedidos de resumo da equipe**. Escolha **Compartilhar uma vez**, **Sempre compartilhar**, **Recusar** ou **Nunca**. Nada é compartilhado até você escolher, e os pedidos sem resposta expiram.

## Graph da equipe

Em um Fleet de Trabalho, o trabalho com clientes é compartilhado com sua equipe depois que você confere. Veja [Graph da equipe](team-graph.md).

## Conexões compartilhadas

Um proprietário ou admin pode conectar Stripe ou Intercom uma vez e compartilhar com a equipe em **Conexões compartilhadas**, na aba Fleet. Os colegas podem consultar a conexão, mas não alterá-la, e podem ver quem a compartilhou. Só admins podem alterá-la ou interromper o compartilhamento. Veja [Stripe](stripe.md) e [Intercom](intercom.md).

## O que sua Machine responde

Defina isso para cada Fleet, no painel Compartilhamento. Veja [Regras de compartilhamento](sharing-rules.md). **Configurações** tem um atalho: **Regras do Fleet**.

## Login com a conta da empresa

Permita que os colegas entrem com a conta da empresa. Em um Fleet de Trabalho hospedado, um proprietário ou admin que entrou com o Google Workspace ou o Microsoft 365 pode ativar **Login com a conta da empresa** na página da conta.

Os colegas que entrarem com o domínio da empresa verão **Pedir para entrar**, e um proprietário ou admin precisará **Aprovar** cada pedido. Contas pessoais do Gmail e do Outlook.com nunca são aceitas.

Quando alguém é removido do Fleet, essa pessoa sai de todas as sessões.

Para entrar em um Fleet, criar um ou parear uma Machine no seu próprio computador, veja [Planos e cobrança](plans-and-billing.md) e [Amigos e a Network](friends.md).

## Para proprietários e admins

**Gerenciar**, na aba Fleet, lista cada Fleet que você administra, com as pessoas, suas funções e os convites. Em uma Machine hospedada, você pode convidar pessoas, alterar funções, removê-las e responder a pedidos para entrar, tudo ali mesmo. Se uma alteração afetar o preço, sua conta será aberta para você confirmar primeiro. Em uma Machine hospedada por você, a lista mostra quem faz parte do Fleet e inclui um link para as configurações desse Fleet na sua conta, onde você administra as pessoas e os convites.

**Configurações do Fleet**, abaixo do nome de cada Fleet no painel e em Gerenciar, abre as configurações desse Fleet na sua conta: conexões compartilhadas, segurança, login com a conta da empresa, quais Machines respondem e estas duas opções:

- **Removidos recentemente**: cada pessoa removida ou que saiu. “Removido, confirmado” significa que a Machine da pessoa excluiu os dados de trabalho e ela saiu de todas as sessões. Até isso acontecer, aparece **Pendente** e o motivo.
- **Atividade**: quem fez o quê e quando: convites, entradas, remoções, funções, Machines hospedadas, cobrança, conexões compartilhadas e aprovações. Também registra todas as vezes que nossa equipe de suporte leu o relatório da Machine de alguém ou os registros dela. Nunca inclui o conteúdo das mensagens. **Baixar CSV** exporta os dados. O histórico é mantido por 12 meses.

**Perguntar antes de iniciar a Machine de um membro**, para o proprietário: ativada, a Machine de um novo membro espera sua aprovação, mesmo em um Fleet gratuito. Desativada, em um Fleet gratuito, ela inicia imediatamente e você recebe um aviso. Uma Machine paga sempre espera sua confirmação do valor.

Depois de **Parar de compartilhar**, uma conexão compartilhada mostra “Removido, confirmado” quando todas as Machines perderem acesso a ela.
