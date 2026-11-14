---
title: Fleets
area: fleet
summary: Uma Work Fleet para sua equipe, uma Family Fleet para sua casa. Machines que ajudam umas às outras, de acordo com suas regras de compartilhamento.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: c9650fc4ffe00e16
---
Uma Fleet permite que sua Machine trabalhe com as Machines da sua equipe, família ou amigos pela The Machine Network. Tudo o que elas compartilham é criptografado de ponta a ponta, e sua Machine só responde de acordo com suas regras.

## Tipos de Fleet

- **Work Fleet**: sua equipe. Passe tarefas adiante, pergunte quem conhece alguém, consiga apresentações e receba um resumo da equipe.
- **Family Fleet**: até 6 pessoas. Quando todo mundo estiver disponível, compartilhe tarefas e planos. Grátis. Veja [Família](family.md).
- **Amigos**: qualquer pessoa na The Machine, individualmente. Grátis. Veja [Amigos](friends.md).

## A aba Fleet

Ela aparece quando você entra em uma Fleet, com um painel para cada Fleet, Família, Amigos, Network, Compartilhamento e Atividade.

## Quanto custa, como sair e como criar outra Fleet

Abaixo do nome de cada Fleet, **Quanto custa** mostra as vagas, quem paga pela sua Machine e, para a pessoa proprietária, o cartão e as faturas da Fleet. **Sair deste Fleet** faz você sair da Fleet. Antes disso, a pessoa proprietária precisa passar a Fleet para outra pessoa. **Criar outro Fleet** cria uma nova Fleet.

Cada opção abre essa etapa da sua conta, e, se houver uma mudança de preço, o valor aparece para você confirmar primeiro. Em uma Machine hospedada por você, elas abrem sua conta em uma nova aba, onde você faz login.

## Pergunte à sua Fleet

Pergunte “quem conhece alguém na Acme?” na aba Fleet ou use **Perguntar à Fleet** em uma organização no [Graph](graph.md). A Machine de cada pessoa da equipe responde de acordo com as próprias regras de compartilhamento e pergunta antes, se a regra exigir.

## Respostas automáticas em uma Work Fleet

Em uma Work Fleet Standard, sua Machine responde automaticamente a três tipos de perguntas da equipe: **quem conhece alguém**, **contexto de reunião** (“quem é essa pessoa convidada?”) e **quem cuida dos e-mails compartilhados**. Ela usa apenas o que o [Team Graph](team-graph.md) já compartilha com sua equipe, nunca conversas privadas, pessoais ou confidenciais. Cada resposta aparece na aba Fleet, em **Atividade**.

Para desativar uma delas, escolha **Nunca** em **Compartilhamento**. Uma regra salva como **Perguntar antes** funciona como **Sempre**. Enquanto o compartilhamento do Team Graph estiver desativado, as perguntas sobre quem conhece alguém e contexto de reunião serão direcionadas a você primeiro.

Em Fleets de trabalho no modo cuidadoso, Amigos e Família, sua Machine ainda pergunta antes. Apresentações, tarefas passadas adiante e perguntas gratuitas continuam seguindo as próprias regras.

## Aprendizados da equipe

Sua Machine registra como sua equipe trabalha, com base em conversas com clientes que o Team Graph já compartilha, no máximo uma vez por dia. Por exemplo: “As solicitações de reembolso são respondidas pela caixa de entrada do suporte usando o modelo de reembolso.” Os aprendizados aparecem no painel da sua Work Fleet, em **Aprendizados da equipe**, para todas as pessoas da Fleet, e cada um fica registrado em **Atividade**. Ninguém precisa aprovar antes.

- Apenas conversas em que alguém da sua equipe participou. Nunca conversas privadas, pessoais ou confidenciais.
- Apenas o que se aplica a vários clientes: um processo, uma ferramenta, um estilo de escrita ou quem cuida de cada coisa. Nunca algo sobre um cliente específico, feedback sobre seu próprio produto, nomes, endereços, números ou citações.
- O que não for claro para sua Machine é descartado.

Sua Machine usa os aprendizados pertinentes ao preparar uma tarefa de trabalho para essa empresa. Seus próprios dados, regras e habilidades vêm primeiro, e tarefas pessoais nunca usam esses aprendizados. Uma tarefa que usou um deles informa isso, por exemplo: “Usou um aprendizado da equipe: os reembolsos são enviados pela caixa de entrada do suporte.” Toque em **Remover** para excluir esse aprendizado de toda a Fleet.

Qualquer pessoa da Fleet pode **Remover** um aprendizado. Ele desaparece para todas as pessoas e não é criado novamente. Para impedir isso, desative **Oferecer compartilhar aprendizados** em Configurações, Segurança. Fleets de trabalho no modo cuidadoso não recebem aprendizados.

## Resumo da equipe

Escolha **Diário** ou **Semanal** para o **Resumo da equipe** na aba Fleet, em **Compartilhamento**. Sua Machine passa a pedir às Machines das pessoas da equipe quantidades e datas. O que precisa da sua atenção aparece em Tarefas, em Trabalho: um cliente esperando por alguém da equipe, uma empresa sem atividade há duas semanas ou mais, duas pessoas da equipe escrevendo para os mesmos contatos ou uma reunião compartilhada.

- Uma tarefa informa quem precisa agir, desde quando, o que essa pessoa pediu e o que está em jogo, como um projeto em andamento. Se não houver algo específico para dizer, o item continua no resumo, sem virar uma tarefa.
- A empresa e as pessoas da equipe têm links para suas páginas. **Detalhes** mostra o que escreveram (toque para ler), o que está em jogo, quem da equipe está em contato e as conversas mais recentes. Só inclui o que o [Team Graph](team-graph.md) compartilha.
- Quando o que foi escrito só está no e-mail de alguém da equipe, a tarefa informa quem você deve consultar.
- **Perguntar à equipe** envia uma pergunta sobre o assunto, já preenchida. As respostas aparecem na tarefa.
- **Não precisa** encerra a tarefa e ajuda o resumo a aprender. Ela só volta a aparecer se houver algo novo.
- Quando alguém responde ou assume a tarefa, ela é encerrada automaticamente. Se já houver uma tarefa sobre a mesma empresa, a nova informação é adicionada a ela.

## Pedidos de resumo

Uma pessoa da equipe que ativou o resumo pede à sua Machine quantidades e datas todas as manhãs. Em uma Work Fleet, sua Machine responde automaticamente, usando apenas o que o [Team Graph](team-graph.md) já compartilha, e não responde enquanto o compartilhamento do Team Graph estiver desativado. Cada resposta aparece na aba Fleet, em **Atividade**, nunca como tarefa ou notificação.

Para parar, desative **Compartilhar meus dados do resumo com a equipe** na aba Fleet, em **Compartilhamento**. A pessoa verá você como alguém que não respondeu no resumo.

Em uma Fleet no modo cuidadoso, os pedidos ficam na aba Fleet, em **Pedidos de resumo da equipe**. Você pode escolher **Compartilhar uma vez**, **Sempre compartilhar**, **Recusar** ou **Nunca**. Nada é compartilhado até você escolher, e os pedidos sem resposta expiram.

## Team Graph

Em uma Work Fleet, o trabalho com clientes é compartilhado com sua equipe depois que você o revisa. Veja [Team Graph](team-graph.md).

## Conexões compartilhadas

Uma pessoa proprietária ou administradora pode conectar Stripe ou Intercom uma vez e compartilhar a conexão com a equipe em **Conexões compartilhadas**, na aba Fleet. As outras pessoas da equipe podem ler os dados, mas não alterá-los, e podem ver quem compartilhou a conexão. Somente pessoas administradoras podem alterá-la ou interromper o compartilhamento. Veja [Stripe](stripe.md) e [Intercom](intercom.md).

## O que sua Machine responde

Configure por Fleet, no painel Compartilhamento. Veja [Regras de compartilhamento](sharing-rules.md). **Configurações** tem um atalho: **Regras do Fleet**.

## Login da empresa

Permita que as pessoas da equipe entrem com a conta da empresa. Em uma Work Fleet hospedada, uma pessoa proprietária ou administradora que tenha entrado com o Google Workspace ou o Microsoft 365 pode ativar **Login da empresa** na página Conta.

As pessoas que entrarem com o domínio da empresa verão **Pedir para entrar**, e uma pessoa proprietária ou administradora precisará **Aprovar** cada pedido. Contas pessoais do Gmail e do Outlook.com nunca são consideradas contas da empresa.

Remover alguém da Fleet desconecta essa pessoa de todos os lugares.

Para entrar em uma Fleet, criar uma ou parear uma Machine no seu próprio computador, veja [Planos e cobrança](plans-and-billing.md) e [Amigos e Network](friends.md).

## Para pessoas proprietárias e administradoras

**Gerenciar**, na aba Fleet, mostra cada Fleet que você administra, as pessoas, suas funções e os convites. Em uma Machine hospedada, você pode convidar pessoas, alterar funções, removê-las e responder a pedidos para entrar ali mesmo. Se uma alteração afetar o preço, sua conta será aberta para você confirmar primeiro. Em uma Machine hospedada por você, aparecem as pessoas que fazem parte da Fleet e um link para as configurações da Fleet na sua conta, onde você pode gerenciar pessoas e convites.

**Configurações do Fleet**, abaixo do nome de cada Fleet no painel e também em Gerenciar, abre as configurações dessa Fleet na sua conta: conexões compartilhadas, segurança, login da empresa, qual Machine responde e estas duas opções:

- **Removidos recentemente**: mostra cada pessoa removida ou que saiu. “Removida, confirmado” significa que a Machine dessa pessoa excluiu os dados de trabalho e ela foi desconectada de todos os lugares. Até isso acontecer, aparece **Pendente** com o motivo.
- **Atividade**: mostra quem fez o quê e quando: convites, entradas, remoções, funções, Machines hospedadas, cobrança, conexões compartilhadas e aprovações. Também mostra cada vez que nossa equipe de suporte leu o relatório da Machine de uma pessoa ou os registros dela. Nunca mostra o conteúdo das mensagens. **Baixar CSV** exporta os dados. Eles são mantidos por 12 meses.

**Perguntar antes de iniciar a Machine de alguém da equipe**, para a pessoa proprietária: quando ativado, a Machine de uma pessoa nova aguarda sua aprovação, mesmo em uma Fleet gratuita. Quando desativado, em uma Fleet gratuita, ela inicia imediatamente e você recebe um aviso. Uma Machine paga sempre aguarda sua confirmação do valor.

Depois de **Parar de compartilhar**, a conexão compartilhada mostra “Removida, confirmado” quando todas as Machines perdem o acesso a ela.
