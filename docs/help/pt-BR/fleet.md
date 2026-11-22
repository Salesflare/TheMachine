---
title: Fleets
area: fleet
summary: Um Fleet de Trabalho para sua equipe, um Fleet da Família para sua casa. Machines que ajudam umas às outras, de acordo com suas regras de compartilhamento.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 974bbbb54608efc3
---
Um Fleet permite que sua Machine trabalhe com as Machines da sua equipe, da sua família ou dos seus amigos pela The Machine Network. O que elas compartilham é criptografado de ponta a ponta, e sua Machine só responde de acordo com suas regras.

## Tipos de Fleet

- **Fleet de Trabalho**: sua equipe. Passe tarefas adiante, pergunte quem conhece alguém, consiga apresentações e receba um resumo da equipe.
- **Fleet da Família**: até 6 pessoas. Quando todos estão livres, compartilhem tarefas e planos. É grátis; as Machines hospedadas nele têm preço para família. Veja [Família](family.md).
- **Amigos**: qualquer pessoa na The Machine, uma por vez. É grátis. Veja [Amigos](friends.md).

## A aba Fleet

Ela aparece quando você entra em um Fleet, com um painel para cada Fleet, além de Amigos, Network, Compartilhamento e Atividade. Proprietários e administradores também veem **Gerenciar**, e um Fleet de Trabalho que compartilha seu Graph também tem **O que é compartilhado**.

## Quanto custa, como sair e como criar outro Fleet

A opção **Quanto custa**, abaixo do nome de cada Fleet, mostra as vagas, quem paga pela sua Machine e, para o proprietário, o cartão e as faturas do Fleet. **Sair deste Fleet** faz você sair dele; antes, o proprietário precisa passar a propriedade para outra pessoa. **Criar outro Fleet** inicia um novo Fleet.

Cada opção abre essa etapa da sua conta, e uma mudança de preço mostra o valor para você confirmar antes. Em uma Machine hospedada por você, elas abrem sua conta em uma nova aba, onde você entra.

## Pergunte ao seu Fleet

Pergunte “quem conhece alguém na Acme?” na aba Fleet ou selecione **Perguntar ao Fleet** em uma organização no [Graph](graph.md). A Machine de cada colega de equipe responde de acordo com as próprias regras de compartilhamento e pergunta antes, quando a regra exige.

Para qualquer outra coisa, use **Pergunte qualquer coisa** no painel do seu Fleet de Trabalho. Cada colega recebe um rascunho de resposta criado com as próprias contas de trabalho, e nada é compartilhado até que a pessoa envie.

## Respostas automáticas em um Fleet de Trabalho

Em um Fleet de Trabalho padrão, sua Machine responde automaticamente a três tipos de pergunta dos colegas de equipe: **quem conhece alguém**, **contexto de reunião** (“quem é essa pessoa convidada?”) e **quem cuida dos e-mails compartilhados**. Ela usa apenas o que o [Graph da equipe](team-graph.md) já compartilha com sua equipe, nunca conversas privadas, pessoais ou confidenciais. Cada resposta aparece na aba Fleet, em **Atividade**.

Para interromper uma resposta, escolha **Nunca** em **Compartilhamento**. Uma regra definida como **Perguntar antes** funciona como **Sempre**. Enquanto o compartilhamento do Graph da equipe estiver desativado, as perguntas sobre quem conhece alguém e contexto de reunião perguntam antes.

Fleets de Trabalho no nível Cuidadoso, Amigos e Fleets da Família ainda perguntam antes. Apresentações, repasses e perguntas livres continuam seguindo suas próprias regras.

## Aprendizados da equipe

Sua Machine registra como sua equipe trabalha, com base nas conversas com clientes que o Graph da equipe já compartilha, no máximo uma vez por dia. Por exemplo: “As solicitações de reembolso são respondidas pela caixa de entrada de suporte usando o modelo de reembolso.” Os aprendizados aparecem no painel do seu Fleet de Trabalho, em **Aprendizados da equipe**, para todos no Fleet. Cada um também é registrado em **Atividade**. Ninguém precisa aprovar antes.

- Apenas conversas em que alguém da sua equipe escreveu. Nunca conversas privadas, pessoais ou confidenciais.
- Apenas informações válidas para vários clientes: um processo, uma ferramenta, um estilo de escrita ou quem cuida de cada coisa. Nunca algo sobre um único cliente, comentários sobre seu próprio produto, nomes, endereços, números ou citações.
- Os aprendizados sobre os quais sua Machine não tem certeza são descartados.

Sua Machine usa os aprendizados relevantes ao preparar uma tarefa de trabalho para esta empresa. Seus dados, regras e habilidades vêm primeiro, e tarefas pessoais nunca usam esses aprendizados. Uma tarefa que usou um deles informa isso, por exemplo: “Usou um aprendizado da equipe: os reembolsos são enviados pela caixa de entrada de suporte.” Toque em **Remover** para excluir esse aprendizado de todo o Fleet.

Qualquer pessoa no Fleet pode **Remover** um aprendizado. Ele desaparece para todos e não é criado novamente. Para impedir isso, desative **Oferecer compartilhar aprendizados** em Configurações, Segurança. Fleets de Trabalho no nível Cuidadoso não recebem aprendizados.

## Resumo da equipe

Escolha **Diário** ou **Semanal** para **Resumo da equipe** na aba Fleet, em **Compartilhamento**. Sua Machine pede então às Machines dos colegas de equipe contagens e datas. O que precisa da sua atenção aparece em Tarefas, em Trabalho: um cliente esperando por um colega, uma empresa sem atividade há duas semanas ou mais, duas pessoas da equipe escrevendo para as mesmas pessoas ou uma reunião compartilhada.

- A tarefa informa quem precisa agir, desde quando, o que foi pedido e o que está em jogo, como um projeto em andamento. Se não houver nada específico para dizer, a informação fica no resumo, sem virar tarefa.
- A empresa e os colegas de equipe têm links para suas páginas. **Detalhes** mostra o que escreveram (toque para ler), o que está em jogo, quem da equipe está em contato e as conversas mais recentes, apenas com informações compartilhadas pelo [Graph da equipe](team-graph.md).
- Quando o que escreveram aparece apenas no e-mail de um colega, a tarefa informa a quem perguntar.
- **Perguntar à equipe** envia uma pergunta sobre o assunto, já preenchida. As respostas aparecem na tarefa.
- **Não precisa** encerra a tarefa, e o resumo aprende com isso. Ela só volta a aparecer se houver algo novo.
- Quando alguém responde ou assume a tarefa, ela é encerrada automaticamente. Uma tarefa sobre uma empresa para a qual você já tem uma tarefa é adicionada a essa tarefa.

## Pedidos de resumo da equipe

Todas as manhãs, uma Machine de um colega de equipe com o resumo da equipe ativado pede à sua Machine contagens e datas. Em um Fleet de Trabalho, sua Machine responde automaticamente, usando apenas o que o [Graph da equipe](team-graph.md) já compartilha, e não responde enquanto o compartilhamento do Graph da equipe estiver desativado. Cada resposta aparece na aba Fleet, em **Atividade**, nunca como tarefa ou notificação.

Para interromper, desative **Compartilhar meus dados do resumo com a equipe** na aba Fleet, em **Compartilhamento**. A pessoa verá no resumo que você não respondeu.

Em um Fleet no nível Cuidadoso, os pedidos ficam na aba Fleet, em **Pedidos de resumo da equipe**. Escolha **Compartilhar uma vez**, **Sempre compartilhar**, **Recusar** ou **Nunca**. Nada é compartilhado até você escolher, e os pedidos sem resposta expiram.

## Graph da equipe

Em um Fleet de Trabalho, o trabalho com clientes é compartilhado com sua equipe depois que você o revisa. Veja [Graph da equipe](team-graph.md).

## Conexões compartilhadas

Um proprietário ou administrador pode conectar Stripe ou Intercom uma vez e compartilhar com a equipe, em **Conexões compartilhadas** na aba Fleet. Os colegas podem consultar as informações, mas não alterá-las, e veem quem compartilhou. Somente administradores podem alterar ou interromper o compartilhamento. Veja [Stripe](stripe.md) e [Intercom](intercom.md).

## O que sua Machine responde

Defina por Fleet, no painel Compartilhamento. Veja [Regras de compartilhamento](sharing-rules.md). **Configurações** tem um atalho: **Regras do Fleet**.

## Login da empresa

Permita que os colegas entrem com a conta da empresa. Em um Fleet de Trabalho hospedado, um proprietário ou administrador que entrou com o Google Workspace ou o Microsoft 365 pode ativar **Login da empresa** na página Conta.

Os colegas que entrarem com o domínio da empresa verão **Pedir para entrar**, e um proprietário ou administrador precisará **Aprovar** cada pedido. Contas pessoais do Gmail e do Outlook.com nunca são aceitas.

Remover alguém do Fleet desconecta essa pessoa de todos os lugares.

Para entrar em um Fleet, criar um ou parear uma Machine no seu próprio computador, veja [Planos e cobrança](plans-and-billing.md) e [Amigos e Network](friends.md).

## Para proprietários e administradores

**Gerenciar** na aba Fleet lista cada Fleet que você administra, com as pessoas, as funções e os convites. Em uma Machine hospedada, você pode convidar pessoas, alterar funções, remover pessoas e responder a pedidos para entrar ali mesmo. Uma alteração que afeta o preço abre sua conta para você confirmar antes. Em uma Machine hospedada por você, a tela mostra quem está no Fleet e tem um link para as configurações desse Fleet na sua conta, onde você pode gerenciar as pessoas e os convites.

**Configurações do Fleet**, abaixo do nome de cada Fleet no painel e em Gerenciar, abre as configurações desse Fleet na sua conta: conexões compartilhadas, segurança, login da empresa, qual Machine responde e estas duas opções:

- **Removidos recentemente**: cada pessoa removida ou que saiu. “Removido, confirmado” significa que a Machine dessa pessoa excluiu os dados de trabalho e que ela foi desconectada de todos os lugares. Até lá, aparece **Pendente** com o motivo.
- **Atividade**: quem fez o quê e quando: convites, entradas, remoções, funções, Machines hospedadas, cobrança, conexões compartilhadas e aprovações. Também registra todas as vezes que nossa equipe de suporte leu o relatório ou os registros da Machine de um membro. Nunca inclui o conteúdo das mensagens. **Baixar CSV** exporta os dados. Eles são mantidos por 12 meses.

**Perguntar antes de iniciar a Machine de um membro**, para o proprietário: quando ativada, a Machine de um novo membro espera sua aprovação, mesmo em um Fleet grátis. Quando desativada, a Machine começa a funcionar imediatamente em um Fleet grátis, e você recebe um aviso. Uma Machine com custo sempre espera sua confirmação do valor.

Depois de **Parar de compartilhar**, uma conexão compartilhada mostra “Removido, confirmado” quando todas as Machines perdem acesso a ela.
