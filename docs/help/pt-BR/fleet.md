---
title: Fleets
area: fleet
summary: Um Fleet de Trabalho para sua equipe e um Fleet da Família para sua casa. Machines que ajudam umas às outras, seguindo suas regras de compartilhamento.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: f75a79e685f3a0cc
---
Um Fleet permite que sua Machine trabalhe com as Machines da sua equipe, família ou dos seus amigos pela The Machine Network. O que elas compartilham é criptografado de ponta a ponta, e sua Machine só responde de acordo com suas regras.

## Tipos de Fleet

- **Fleet de Trabalho**: sua equipe. Passe tarefas, pergunte **quem conhece alguém**, peça apresentações e receba um resumo da equipe.
- **Fleet da Família**: até 6 pessoas. Quando todo mundo está livre, compartilhe tarefas e planos e faça perguntas à Machine das outras pessoas. É grátis. As Machines hospedadas nele têm preço familiar. Veja [Família](family.md).
- **Amigos**: qualquer pessoa no The Machine, uma por vez. É grátis. Veja [Amigos](friends.md).

## A aba Fleet

Ela aparece quando você entra em um Fleet, com um painel para cada Fleet, seguido de Amigos, Network, Compartilhamento e Atividade. Donos e administradores também têm **Gerenciar**. Um Fleet de Trabalho que compartilha o Graph também tem **O que é compartilhado**.

## Quanto custa, como sair e como criar um Fleet

Abaixo do nome de cada Fleet, **Quanto custa** mostra as vagas, quem paga pela sua Machine e, para o dono, o cartão e as faturas do Fleet. **Sair deste Fleet** faz você sair dele. Antes disso, o dono precisa passar a responsabilidade para outra pessoa. **Criar outro Fleet** inicia um novo Fleet.

Cada opção abre essa etapa da sua conta, e qualquer mudança de preço mostra o valor para você confirmar antes. Em uma Machine hospedada por você, elas abrem sua conta em uma nova aba, onde você faz login.

## Pergunte ao seu Fleet

Pergunte “quem conhece alguém na Acme?” na aba Fleet ou selecione **Perguntar ao Fleet** em uma organização no [Graph](graph.md). A Machine de cada colega de equipe responde de acordo com as próprias regras de compartilhamento e pergunta antes quando a regra exigir.

Para qualquer outra pergunta, use **Pergunte qualquer coisa** no painel do seu Fleet de Trabalho. Cada colega recebe um rascunho de resposta das próprias contas de trabalho. Nada é compartilhado até que a pessoa envie a resposta.

## Respostas automáticas em um Fleet de Trabalho

Em um Fleet de Trabalho padrão, sua Machine responde automaticamente a três tipos de perguntas dos colegas: **quem conhece alguém**, **contexto de reunião** (“quem é essa pessoa convidada?”) e **quem cuida dos e-mails compartilhados**. Ela usa apenas o que o [Graph da equipe](team-graph.md) já compartilha com sua equipe, nunca conversas privadas, pessoais ou sensíveis. Cada resposta aparece na aba Fleet, em **Atividade**.

Para desativar uma resposta, selecione **Nunca** em **Compartilhamento**. Uma regra definida como **Perguntar antes** funciona como **Sempre**. Enquanto o compartilhamento do Graph da equipe estiver desativado, as perguntas sobre quem conhece alguém e o contexto de reunião exigirão sua aprovação.

Em Fleets de Trabalho com regras cuidadosas, em Amigos e na Família, a resposta sempre depende da sua aprovação. Apresentações, repasses e perguntas gratuitas seguem suas próprias regras.

## Aprendizados da equipe

Sua Machine registra como sua equipe trabalha com base nas conversas com clientes que o Graph da equipe já compartilha, no máximo uma vez por dia. Por exemplo: “Os pedidos de reembolso são respondidos pela caixa de entrada do suporte com o modelo de reembolso”. Esses aprendizados aparecem no painel do seu Fleet de Trabalho, em **Aprendizados da equipe**, para todas as pessoas no Fleet, e cada um fica registrado em **Atividade**. Ninguém precisa aprovar antes.

- Apenas conversas escritas por alguém da sua equipe. Nunca conversas privadas, pessoais ou sensíveis.
- Apenas informações que se aplicam a vários clientes: um processo, uma ferramenta, um estilo de escrita ou quem cuida de cada tarefa. Nunca informações sobre um único cliente, comentários sobre seu próprio produto, nomes, endereços, números ou citações.
- Aprendizados sobre os quais sua Machine não tem certeza são descartados.

Sua Machine usa os aprendizados relevantes ao preparar uma tarefa de trabalho para esta empresa. Seus próprios dados, regras e habilidades vêm primeiro, e tarefas pessoais nunca usam esses aprendizados. Uma tarefa que usou um aprendizado informa isso, por exemplo: “Usou um aprendizado da equipe: os reembolsos são enviados pela caixa de entrada do suporte”. Toque em **Remover** para excluir esse aprendizado de todo o Fleet.

Qualquer pessoa no Fleet pode **Remover** um aprendizado. Ele desaparece para todas as pessoas e não é criado novamente. Para desativar esse recurso, desligue **Oferecer para compartilhar aprendizados** em Configurações, Segurança. Fleets de Trabalho com regras cuidadosas não recebem aprendizados.

## Resumo da equipe

Selecione **Diário** ou **Semanal** para **Resumo da equipe** na aba Fleet, em **Compartilhamento**. Sua Machine então pede às Machines dos colegas de equipe contagens e datas. O que precisa da sua atenção aparece em Tarefas, em Trabalho: um cliente esperando por um colega, uma empresa sem contato há duas semanas ou mais, duas pessoas da equipe escrevendo para as mesmas pessoas ou uma reunião compartilhada.

- Uma tarefa informa quem precisa responder, desde quando, o que a pessoa pediu e o que está em jogo, como um projeto em andamento. Se não houver nada específico para dizer, ela fica como uma linha no resumo, não como uma tarefa.
- A empresa e os colegas de equipe têm links para suas páginas. **Detalhes** mostra o que escreveram (toque para ler), o que está em jogo, quem da equipe está em contato e as conversas mais recentes, apenas o que o [Graph da equipe](team-graph.md) compartilha.
- Quando o que escreveram está apenas no e-mail de um colega, a tarefa informa quem você deve consultar.
- **Perguntar à equipe** envia uma pergunta sobre o assunto, já preenchida. As respostas aparecem na tarefa.
- **Não precisa** fecha a tarefa e ajuda o resumo a aprender. Ela só aparece novamente se houver algo novo.
- Quando alguém responde ou assume a tarefa, ela é fechada automaticamente. Uma tarefa sobre uma empresa para a qual você já tem outra tarefa é adicionada àquela tarefa.

## Pedidos de resumo da equipe

Todas as manhãs, um colega com o resumo da equipe ativado pede à sua Machine contagens e datas. Em um Fleet de Trabalho, sua Machine responde automaticamente, usando apenas o que o [Graph da equipe](team-graph.md) já compartilha, e não responde enquanto o compartilhamento do Graph da equipe estiver desativado. Cada resposta aparece na aba Fleet, em **Atividade**, nunca como tarefa ou notificação.

Para desativar esse recurso, desligue **Compartilhar meus dados do resumo com a equipe** na aba Fleet, em **Compartilhamento**. O resumo do colega mostrará que você não respondeu.

Em um Fleet com regras cuidadosas, os pedidos ficam na aba Fleet, em **Pedidos de resumo da equipe**: **Compartilhar uma vez**, **Sempre compartilhar**, **Recusar** ou **Nunca**. Nada é compartilhado até você escolher, e os pedidos sem resposta expiram.

## Graph da equipe

Em um Fleet de Trabalho, o trabalho com clientes é compartilhado com sua equipe depois que você o revisa. Veja [Graph da equipe](team-graph.md).

## Conexões compartilhadas

Um dono ou administrador pode conectar o Stripe ou o Intercom uma vez e compartilhar a conexão com a equipe em **Conexões compartilhadas**, na aba Fleet. Os colegas podem consultar a conexão, mas não alterá-la, e podem ver quem a compartilhou. Só administradores podem alterá-la ou parar de compartilhá-la. Veja [Stripe](stripe.md) e [Intercom](intercom.md).

## O que sua Machine responde

Defina isso para cada Fleet, no painel Compartilhamento. Veja [Regras de compartilhamento](sharing-rules.md). **Configurações** tem um atalho: **Regras do Fleet**.

## Login com conta corporativa

Permita que os colegas entrem com a conta da empresa. Em um Fleet de Trabalho hospedado, um dono ou administrador que entrou com o Google Workspace ou o Microsoft 365 pode ativar **Login com conta corporativa** na página da conta.

Os colegas que entrarem com o domínio da empresa verão **Solicitar entrada**, e um dono ou administrador precisará **Aprovar** cada solicitação. Contas pessoais do Gmail e do Outlook.com não são aceitas.

Remover alguém do Fleet encerra a sessão dessa pessoa em todos os lugares.

Para entrar em um Fleet, criar um ou parear uma Machine no seu próprio computador, veja [Planos e cobrança](plans-and-billing.md) e [Amigos e a Network](friends.md).

## Para donos e administradores

**Gerenciar**, na aba Fleet, lista cada Fleet que você administra, com as pessoas, as funções e os convites. Em uma Machine hospedada, você pode convidar pessoas, alterar funções, removê-las e responder a pedidos de entrada ali mesmo. Se uma mudança afetar o preço, sua conta será aberta para você confirmar antes. Em uma Machine hospedada por você, a lista mostra quem faz parte do Fleet e inclui um link para as configurações dele na sua conta, onde você gerencia as pessoas e os convites.

**Configurações do Fleet**, abaixo do nome de cada Fleet no painel e em Gerenciar, abre as configurações desse Fleet na sua conta. Lá você encontra conexões compartilhadas, segurança, login com conta corporativa, as Machines que respondem e estas duas opções:

- **Removidos recentemente**: cada pessoa removida ou que saiu. “Removido, confirmado” significa que a Machine da pessoa excluiu os dados de trabalho e encerrou a sessão dela em todos os lugares. Até isso acontecer, aparece **Pendente** e o motivo.
- **Atividade**: quem fez o quê e quando: convites, entradas, remoções, funções, Machines hospedadas, cobrança, conexões compartilhadas e aprovações. Também registra cada vez que a equipe de suporte leu o relatório da Machine de uma pessoa ou os registros dela. Nunca inclui o conteúdo das mensagens. **Baixar CSV** exporta o registro. Os dados ficam armazenados por 12 meses.

**Perguntar antes de iniciar a Machine de um membro**, para o dono: ativada, a Machine de um novo membro espera sua aprovação, mesmo em um Fleet gratuito. Desativada, em um Fleet gratuito, ela inicia na hora e você recebe um aviso. Uma Machine paga sempre espera você confirmar o valor.

Depois de **Parar de compartilhar**, uma conexão compartilhada mostra “Removido, confirmado” quando todas as Machines perderam acesso a ela.
