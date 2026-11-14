---
title: Rotinas
area: cards
summary: Tarefas que sua Machine faz sozinha, em uma frequência definida, como um resumo das suas negociações em aberto toda segunda-feira. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: 9c3559a910b9dd37
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga o que ela deve fazer e quando, em uma linha: "toda segunda-feira às 9h, resuma minhas negociações em aberto" ou "todas as manhãs dos dias úteis, liste os e-mails que ainda preciso responder". Depois, toque em **Adicionar**.

Se você não definir um horário, ela será executada às 8h. O horário segue o relógio da sua Machine. Na primeira execução, ela recebe um nome curto.

Ao tocar em **Adicionar**, primeiro é feita uma execução de teste para você ver o resultado antes de manter a rotina. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina na frequência definida, **Mudar** testa outras palavras ou um novo nome e **Cancelar** descarta a rotina.

## Modelos

Em **Modelos**, na parte de baixo de Rotinas, toque em **Adicionar** para ativar uma rotina pronta. Ela é executada uma vez na hora e, depois, todas as manhãs às 7h30 (Limpeza de spam, a cada hora; Assinaturas e testes, uma vez por mês). O cartão mostra as palavras usadas, como em qualquer rotina, e **Editar** permite mudar essas palavras ou o nome.

Quando você recebe muitas newsletters e a Limpeza de newsletters está desativada (25 ou mais em uma semana, de pelo menos 5 remetentes), aparece uma linha acima das suas tarefas informando quantas chegaram e o que a rotina faria, com as opções **Ativar** e **Não, obrigado**.

A Limpeza de spam é sugerida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para o spam em uma semana. **Ativar** adiciona a rotina da mesma forma que **Adicionar** faz aqui. Se você tocar em **Não, obrigado**, ela não será sugerida novamente. O mesmo vale para um modelo que você já teve.

A **Limpeza de newsletters** cria uma tarefa para cada área (trabalho e pessoal) com as newsletters do último dia. Em cada uma, você pode escolher **Manter** ou **Cancelar inscrição**. Para cancelar a inscrição, a rotina usa o link de cancelamento com um clique da lista ou envia um e-mail de cancelamento pelo seu endereço, se o envio estiver ativado. Caso contrário, The Machine cancela sua inscrição na página da lista, usando o próprio navegador. Você cuida de qualquer login, captcha ou escolha nessa página. A linha explica o motivo e mostra **Abrir página de cancelamento**.

Recibos, pedidos e avisos de pagamento ficam de fora. E-mails recebidos por um endereço de grupo, como um Google Group, são listados com o nome de quem os enviou e nunca cancelam sua inscrição no grupo. Se o remetente não tiver uma opção própria de cancelamento, a linha mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa para cada área com e-mails de remetentes desconhecidos que parecem spam. Em cada um, você pode escolher **Spam** ou **Não é spam**. Outlook move o spam para a pasta de lixo eletrônico, e Gmail marca o e-mail como spam. A rotina verifica a cada hora, então o spam geralmente já está lá quando você chega. Enquanto a tarefa estiver aberta, novos e-mails de spam são adicionados a ela.

Uma conta Gmail conectada como somente leitura, como em uma Machine hospedada, não pode mover e-mails para o spam. Nesse caso, **Spam** mostra um link para marcar o e-mail no Gmail, e The Machine se lembra do remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Remetentes desconhecidos são aqueles para quem você nunca escreveu. Um "Re:" só conta como uma conversa se estiver em uma conversa em que você escreveu. Se um e-mail de um remetente que você marcou como spam, na tarefa ou na sua caixa de entrada, chegar de novo, ele aparecerá na próxima tarefa como **Já marcado como spam**. Os e-mails que você mesmo moveu para o spam também ajudam a rotina a identificar mensagens parecidas.

Nada muda até você confirmar na tarefa. Toque no remetente para ler o e-mail primeiro: ele continua como não lido e nada muda. Na Limpeza de spam, as imagens da web não são carregadas, então o remetente não consegue saber que você abriu o e-mail. A rotina não pergunta de novo sobre remetentes que você já avaliou. Se passar um dia sem newsletters ou spam, nenhuma tarefa será criada. Essas tarefas nunca enviam uma notificação.

Depois que você decidir sobre todos os remetentes, a tarefa informa que foi concluída e mostra **Marcar como feita**.

O **Resumo diário** escolhe, uma vez por dia, algumas newsletters que valem seu tempo e reúne tudo em uma tarefa. Cada item explica em uma linha por que é relevante para você. Toque nele para ler o e-mail ou use **Abrir no seu e-mail**. Só entram newsletters, nunca e-mails de pessoas, recibos ou remetentes dos quais você cancelou a inscrição, e nunca algo que você já leu. Se nada se destacar, nenhuma tarefa será criada.

A rotina aprende o que interessa para você com base no que abre, marca com estrela ou arquiva sem ler, além das opções **Mais assim** e **Menos assim** em cada sugestão. Os temas escolhidos aparecem no cartão da rotina, em **Mais de** e **Menos de**. Remova um tema com × ou adicione o seu. Os temas com linhas pontilhadas foram aprendidos pela própria rotina. Um novo resumo substitui o que estiver aberto e nunca envia uma notificação.

A rotina lê apenas o remetente, o assunto e o início de cada newsletter nova, e faz uma pergunta curta sobre elas à sua IA, com um limite diário para manter o custo baixo. **Mudar quando** define o horário. Depois que você muda as palavras, a rotina passa a funcionar como qualquer outra, com base nas suas palavras.

**Aniversários** cria uma tarefa para cada contato próximo que faz aniversário hoje: pessoas para quem você mesmo escreve, como amigos, familiares e contatos frequentes. Cada pessoa recebe uma mensagem curta de felicitações, elaborada no lugar onde você costuma conversar com ela, como o chat de WhatsApp ou a conversa por e-mail, no idioma dela. A mensagem só é enviada quando você a envia. Se ninguém fizer aniversário naquele dia, nenhuma tarefa será criada.

Os aniversários vêm dos seus calendários (eventos de aniversário do Google e o calendário Aniversários, lidos todas as manhãs mesmo quando não estão sincronizados, e o calendário Aniversários do Outlook), dos seus contatos do Google em uma Machine auto-hospedada e de um campo de data chamado Birthday em uma pessoa no Graph. Se ainda não houver nenhum aniversário nessas fontes, o resultado mostrará **Ainda não há informações de aniversário** e explicará como adicionar algumas.

**Importar aniversários do Facebook**: depois que Aniversários estiver ativado, uma tarefa oferece a opção de ler a página de aniversários do Facebook. Toque em **Importar** e The Machine abre a página no próprio navegador, rola até carregar todos os meses e lê o nome e o aniversário de cada amigo. Ela mostra quantos aniversários encontrou e quem correspondeu a pessoas no seu Graph, com base no nome e sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela será ignorada e listada.

Só **Salvar** importa os dados para a página de cada pessoa: o aniversário e, se a pessoa ainda não tiver uma foto, a foto do perfil do Facebook. Um aniversário ou uma foto que você definir ali será mantido, e uma foto que a pessoa já tiver nunca será substituída. Nada é escrito no Facebook.

A rotina não lê os dados novamente por conta própria. Para isso, toque em **Importar de novo** na tarefa. O navegador precisa estar conectado ao Facebook. Se não estiver, toque em **Entrar no Facebook** na tarefa e faça login. Depois que você entrar, a rotina lê a página automaticamente. The Machine nunca faz login por você.

A rotina contabiliza amigos que ninguém no seu Graph tem, mostrando alguns nomes. **Adicionar … como contatos pessoais** adiciona todos de uma vez, inclusive depois de tocar em Salvar: cada contato é criado com nome e aniversário, e nunca é compartilhado com uma Fleet de trabalho. A rotina ignora nomes que alguém no seu Graph já tenha ou que já tenham pertencido a alguém que você excluiu permanentemente. Você só recebe lembretes de aniversário de pessoas para quem escreve.

**Desfazer** na tarefa remove exatamente essas pessoas, inclusive depois de tocar em **Importar de novo**.

**Assinaturas e testes** lê recibos, faturas e avisos de renovação uma vez por mês e reúne suas assinaturas em uma tarefa: quanto custa cada uma, quando será a próxima cobrança e um aviso quando um teste terminar ou o preço aumentar. Só são listadas as assinaturas identificadas com segurança. Se nada for encontrado, nenhuma tarefa será criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. Uma assinatura mantida não será mencionada de novo, a menos que o preço mude. **Cancelar** mostra a página de cancelamento ou um rascunho pedindo o cancelamento, que só será enviado quando você enviar. Entre as execuções mensais, a rotina verifica as assinaturas todos os dias e cria uma tarefa quando um teste ou uma renovação tiver cobrança nos próximos 7 dias.

Enquanto a rotina de um modelo mantiver as palavras do modelo, ela será executada com o próprio código, sem usar seu plano de IA (a Limpeza de spam primeiro lista no código os e-mails novos de remetentes desconhecidos e só faz uma pergunta curta à sua IA quando encontra algum). Um novo nome mantém esse comportamento. Depois que você muda as palavras, a rotina passa a funcionar como qualquer outra, com base nas suas palavras.

A Limpeza de newsletters e a Limpeza de spam continuam criando a mesma tarefa, com uma opção para cada e-mail. Uma rotina Aniversários editada mostra o resultado e, no máximo, um rascunho, em vez de criar uma tarefa por pessoa. Toque em **Voltar ao modelo** em **Editar** para restaurar as palavras do modelo.

## O que uma rotina faz

No horário definido, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e coloca o resultado na página Rotinas. Cada resultado mostra **Para revisar**, **Nada de novo** (com o motivo) ou **Não funcionou** (com o motivo). Uma execução que termina sem resultado conta como uma execução que não funcionou, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da web, GitHub e sites como X no navegador. Elas não enviam, respondem, publicam nem mudam nada. Só um modelo altera e-mails, e apenas o que você confirma na tarefa dele.

Quando a tarefa de uma rotina termina com uma publicação ou mensagem, ela faz tudo até essa etapa e mostra o rascunho, por exemplo, **Publicaria no X:**. Depois de uma execução real, o rascunho aparece como uma tarefa para você aprovar. Uma execução de teste só mostra o rascunho. O nome informa o assunto e onde será publicado, o botão identifica a etapa, como **Publicar**, e **Da sua rotina**, logo abaixo, abre a rotina.

A tarefa começa na área da conta de onde será enviada, como Trabalho para a conta X da sua empresa, então ela nunca pede que você a mova.

Uma execução pode seguir suas [habilidades](skills.md) ativadas, escolhidas de acordo com o que a rotina faz: só as habilidades adequadas são lidas por completo. O resultado lista as habilidades em **Usadas:**. Uma habilidade nunca faz uma rotina enviar ou alterar nada.

Suas rotinas aparecem em **Suas rotinas**, abaixo de todas as sugestões. Resultados longos são recolhidos e viram uma prévia curta. **Mostrar mais** ou tocar no resultado abre o conteúdo completo.

Cada execução conhece o resultado anterior, então pode indicar o que mudou desde então.

Depois de uma execução bem-sucedida, sua Machine pode criar uma receita para as etapas de leitura que se repetem, como quais e-mails ou mudanças no GitHub verificar. Nas próximas execuções, essas etapas são feitas primeiro, em código simples. A IA só escolhe o que importa e escreve o resultado, usando menos tokens. Uma receita só lê. Se parar de funcionar, a execução faz a leitura por conta própria e corrige a receita. Ela aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias sem execução

Se sua Machine estiver desligada ou ocupada, as execuções perdidas não se acumulam: só a mais recente é executada, uma vez. Cada data tem uma única execução, mesmo depois de uma reinicialização.

As rotinas são executadas uma de cada vez e aguardam quando o uso do seu plano de IA está baixo, como todo trabalho em segundo plano. **Rodar agora** executa a rotina na hora. Quando estiver pronto, o resultado aparecerá no cartão.

## Mudar ou parar uma rotina

Essas opções ficam no menu ⋯ da rotina. **Editar** muda o nome e o que ela faz. O horário das execuções e os resultados anteriores são mantidos. **Mudar quando** permite definir uma nova frequência com suas próprias palavras, como "todos os dias úteis às 8h". As duas opções têm **Salvar** e **Cancelar**. No computador, você também pode cancelar com Esc ou clicando fora.

Em **Editar**, **Testar** executa as novas palavras uma vez e mostra o resultado ali. A rotina continua como estava até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar**. Rotinas pausadas ficam em **Pausado**, na parte de baixo, e nada do que foi perdido durante a pausa será executado depois. **Parar** encerra uma rotina de vez.

Quando você usa **Pedir mudanças** na tarefa de uma rotina ou escreve no chat dela, e sua observação vale para todas as execuções, como "nunca use emoji", a tarefa oferece **Mudar também a rotina**, tanto na tarefa quanto no chat, abaixo da resposta. Ela mostra o que mudaria nas palavras da rotina, que só será alterada quando você tocar em **Mudar**. **Deixar como está** mantém a rotina. Se a correção for só para aquele rascunho, essa opção não será oferecida.

## Avançado: etapas de script

Não precisa de script: diga com suas próprias palavras o que uma rotina deve fazer, e sua Machine cuida do resto.

Para quem tem mais experiência, uma rotina também pode executar comandos próprios na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** só mostra as etapas quando a rotina já tem alguma. **Buscar dados** executa um comando primeiro, na pasta definida (na sua pasta pessoal, se o campo estiver vazio), por no máximo o tempo indicado em segundos. O que o comando imprimir fica disponível para a rotina usar. Se não houver palavras, o que ele imprimir será o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se o comando terminar com um erro, a execução mostra **Não funcionou** e o que a verificação informou. Se um comando de Buscar dados falhar, o resultado será mostrado da mesma forma.

Cada comando deve ocupar uma linha e é executado sem um shell: não use pipes nem variáveis. As etapas de script são suas e só podem ser configuradas no seu painel. Uma execução de teste e **Testar** também executam Buscar dados e informam isso. Elas continuam sem enviar nem guardar nada. Uma rotina nunca envia nada, então uma etapa de script deve apenas ler.

## Das suas tarefas do OpenClaw

Se você já criou tarefas agendadas no OpenClaw, sua Machine as lê (nunca as altera) e sugere as que servem como rotinas em **Sugerido**. Cada uma foi executada uma vez, então você vê um resultado real.

A rotina mantém as correções que você fez na tarefa e remove o que ela enviou ou publicou. Uma tarefa que executou um script ou leu dados coletados por uma tarefa de script traz esse script como Buscar dados. **Adicionar** cria uma rotina, e **Não, obrigado** impede que a tarefa volte a ser sugerida. Uma tarefa que lembrava você de fazer algo aparece como uma sugestão de tarefa recorrente em Tarefas.

Antes de adicionar uma sugestão, **Editar** e **Mudar quando**, no menu ⋯, permitem alterá-la como qualquer rotina. **Rodar de novo** executa a rotina com as palavras atuais para mostrar resultados mais recentes, por exemplo, depois de um fim de semana tranquilo. Ela só lê, é executada uma vez por toque e o novo resultado substitui o antigo.

Pode haver no máximo três sugestões aguardando ao mesmo tempo. Depois de uma semana de execuções bem-sucedidas, a rotina pergunta **Desativar o antigo job do OpenClaw?**. O job só é desativado quando você toca em **Desativar**, e você pode reativá-lo no OpenClaw.

## Com base no que você faz

Sua Machine também percebe tarefas que você faz com frequência e as sugere como rotinas em **Sugerido**, mesmo sem OpenClaw. Ela procura:

- o mesmo pedido feito três vezes seguidas ou mais, como "resuma os chamados de suporte em aberto" toda segunda-feira;
- um e-mail que você envia com frequência, como um relatório semanal para sua equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como mensagens da escola e do clube que você encaminha para seu parceiro: um resumo semanal poupa você de encaminhá-las;
- o mesmo pedido que você responde com frequência, como uma aprovação mensal para a mesma pessoa.

Cada sugestão informa o que a rotina observou, como "Pedido feito 4 vezes seguidas" ou "6 e-mails encaminhados para Sam em 3 semanas", e já foi executada uma vez para você ver um resultado real. Pense em um resumo da equipe, um briefing antes de uma reunião semanal, um resumo de suporte ou desenvolvimento, um acompanhamento dos seus números ou um resumo das newsletters que você recebe.

A rotina só sugere algo específico para você e claramente útil: um resumo de notícias baseado apenas nas suas newsletters, nunca um resumo genérico. Se nada se encaixar, nenhuma sugestão será exibida.

A rotina verifica isso no máximo uma vez por dia e traz no máximo uma sugestão nova por semana, sem enviar uma notificação. **Não, obrigado** impede que aquela sugestão volte. Os encaminhamentos e as respostas continuam associados à conta de onde foram enviados, então Trabalho e Pessoal não se misturam. Tudo fica na sua Machine. Uma tarefa que você conclui com frequência aparece como uma sugestão de tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma tarefa recorrente (recurring.md) lembra você de fazer algo. Uma rotina é um trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para "pagar o aluguel no dia primeiro" e uma rotina para "toda sexta-feira, me diga quais negociações ficaram sem novidades".
