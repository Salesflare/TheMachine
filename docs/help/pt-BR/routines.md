---
title: Rotinas
area: cards
summary: Trabalhos que sua Machine faz sozinha, em uma frequência definida, como um resumo das suas oportunidades abertas toda segunda-feira. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in
translated: 2be351a9cef42215
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga em uma linha o que ela deve fazer e quando: "toda segunda-feira às 9h, resuma minhas oportunidades abertas" ou "todas as manhãs dos dias úteis, liste os e-mails que ainda preciso responder". Depois, toque em **Adicionar**.

Se você não definir um horário, ela roda às 8h, no horário da sua Machine. Na primeira execução, ela recebe um nome curto.

Ao tocar em **Adicionar**, primeiro é feita uma execução de teste, para você ver o resultado antes de manter a rotina. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina na frequência definida, **Mudar** tenta outras palavras ou um novo nome, e **Cancelar** descarta a rotina.

## Modelos

Em **Modelos**, no fim da página de Rotinas, **Adicionar** ativa uma rotina pronta. Ela roda uma vez na hora e, depois, todas as manhãs às 7h30. A Limpeza de spam roda a cada hora, e Assinaturas e testes, uma vez por mês. O cartão mostra as palavras usadas, como em qualquer rotina, e **Editar** permite mudar essas palavras ou o nome.

Quando chegam muitas newsletters e a Limpeza de newsletters está desativada (25 ou mais em uma semana, de pelo menos 5 remetentes), aparece uma linha acima das suas tarefas informando quantas chegaram e o que a rotina faria, com as opções **Ativar** e **Não, obrigado**.

A Limpeza de spam é oferecida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para spam em uma semana. **Ativar** adiciona a rotina, como **Adicionar** nesta página. Se você tocar em **Não, obrigado**, ela não será oferecida novamente. Um modelo que você já teve também não será oferecido novamente.

A **Limpeza de newsletters** cria uma tarefa por área (trabalho e pessoal) com as newsletters do último dia. Cada uma tem a opção **Manter** ou **Cancelar inscrição**. A opção de cancelamento usa o link de cancelamento com um clique da lista ou envia um e-mail de cancelamento pelo seu endereço, se o envio estiver ativado. Caso contrário, The Machine cancela sua inscrição na página da lista, usando o próprio navegador. Se a página exigir login, captcha ou alguma escolha, você decide: a linha explica o motivo e mostra **Abrir página de cancelamento**.

Recibos, pedidos e avisos de pagamento são excluídos. E-mails recebidos por um endereço de grupo, como um Google Group, são listados com o nome de quem os escreveu, e sua inscrição no grupo nunca é cancelada. Se o remetente não tiver uma opção própria para cancelar a inscrição, a linha mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa por área com e-mails de remetentes desconhecidos que parecem spam. Cada um tem as opções **Spam** e **Não é spam**. Outlook move o spam para Lixo eletrônico, e Gmail o marca como spam. A rotina verifica a cada hora, então o spam geralmente aparece antes de você abrir a caixa de entrada. Enquanto a tarefa estiver aberta, novos e-mails de spam são adicionados a ela.

Uma conta Gmail conectada em modo somente leitura, como em uma Machine hospedada, não pode mover e-mails para spam. Nesse caso, **Spam** mostra um link para marcar o e-mail no Gmail, e The Machine se lembra do remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Um remetente é considerado desconhecido se você nunca escreveu para ele. E uma mensagem com "Re:" só conta como conversa se você tiver escrito na conversa. Se um e-mail de um remetente que você marcou como spam, na tarefa ou na caixa de entrada, voltar a passar, ele aparecerá na próxima tarefa como **Já marcado como spam**. Os e-mails que você mesmo moveu para spam também ajudam a rotina a identificar mensagens parecidas.

Nada muda até você confirmar na tarefa. Toque no remetente para ler o e-mail primeiro: ele continua como não lido e nada muda. Na Limpeza de spam, as imagens da internet não carregam, então o remetente não consegue ver que você abriu o e-mail. Os remetentes sobre os quais você já decidiu não serão perguntados novamente. Se não houver newsletters ou spam em um dia, nenhuma tarefa será criada. Essas tarefas nunca enviam notificações.

Depois que você decidir sobre todos os remetentes, a tarefa indica que foi concluída e mostra **Marcar como feita**.

O **Resumo diário** seleciona, uma vez por dia e em uma única tarefa, algumas newsletters que valem seu tempo. Cada uma explica em uma linha por que é importante para você. Toque para ler o e-mail ou use **Abrir no seu e-mail**. Só entram newsletters, nunca e-mails de pessoas, recibos ou mensagens de remetentes dos quais você cancelou a inscrição. E-mails que você já leu também não entram. Se nada se destacar, nenhuma tarefa será criada.

A rotina aprende com o que você abre, marca com estrela ou arquiva sem ler, e com as opções **Mais assim** e **Menos assim** em cada seleção. Os temas usados na seleção aparecem no cartão da rotina, em **Mais de** e **Menos de**. Toque em × para remover um tema ou adicione um seu. Os temas com linha tracejada foram identificados pela rotina. Um novo resumo substitui o que ainda estiver aberto, e nunca envia uma notificação.

A rotina lê apenas o remetente, o assunto e o início de cada newsletter nova, e faz uma pergunta curta sobre elas à sua IA, com um limite diário para manter o custo baixo. **Mudar quando** define o horário. Depois que você mudar as palavras da rotina, ela passa a funcionar como qualquer outra rotina, usando as palavras que você definiu.

**Aniversários** cria uma tarefa para cada contato próximo que faz aniversário hoje: pessoas com quem você conversa por conta própria, como amigos, familiares e contatos frequentes. Para cada pessoa, a rotina prepara uma saudação curta no canal em que vocês costumam conversar, como o chat do WhatsApp ou a conversa por e-mail, no idioma da pessoa. A saudação só é enviada quando você a envia. Se ninguém fizer aniversário naquele dia, nenhuma tarefa será criada.

Os aniversários vêm dos seus calendários (eventos de aniversário e calendário de Aniversários do Google, lidos todas as manhãs mesmo quando não estão sincronizados, e o calendário de Aniversários do Outlook), dos seus contatos do Google em uma Machine auto-hospedada e de um campo de data chamado Birthday em uma pessoa do Graph. Se nenhum deles tiver um aniversário, o resultado mostra **Ainda não há informações de aniversário** e explica como adicionar uma.

**Importar aniversários do Facebook**: depois que Aniversários estiver ativada, uma tarefa oferece a opção de ler a página de aniversários do Facebook. Toque em **Importar** e The Machine abre a página no próprio navegador, rola até carregar todos os meses e lê o nome e o aniversário de cada amigo. Ela mostra quantos aniversários encontrou e quais pessoas correspondem a pessoas no seu Graph, usando o nome e o sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela será ignorada e listada.

Só **Salvar** guarda os dados na página de cada pessoa: a data de aniversário e a foto do perfil do Facebook, se a pessoa ainda não tiver uma foto. Uma data de aniversário ou foto que você definir ali será mantida, e uma foto que a pessoa já tiver nunca será substituída. Nada é escrito no Facebook.

A rotina não lê a página novamente por conta própria. Para isso, toque em **Importar de novo** na tarefa. O navegador precisa estar conectado ao Facebook. Se não estiver, toque em **Entrar no Facebook** na tarefa e faça login. Depois que você entrar, a rotina lê a página automaticamente. The Machine nunca faz login por você.

Amigos que ninguém no seu Graph conhece são contabilizados, e alguns nomes são exibidos. **Adicionar … como contatos pessoais** adiciona todos de uma vez, inclusive depois de tocar em Salvar: cada pessoa com seu nome e aniversário, sem nunca compartilhar os dados com uma Work Fleet. Pessoas com um nome que alguém no seu Graph já tem, ou que alguém que você excluiu permanentemente tinha, são ignoradas. Os lembretes de aniversário continuam sendo enviados apenas para pessoas com quem você conversa.

**Desfazer** na tarefa remove exatamente essas pessoas, inclusive depois de **Importar de novo**.

**Assinaturas e testes** lê seus recibos, faturas e avisos de renovação uma vez por mês e reúne suas assinaturas em uma tarefa: o preço de cada uma, a próxima data de cobrança e um aviso quando um teste termina ou o preço aumenta. Só aparecem as assinaturas que a rotina consegue identificar com certeza. Se nada for encontrado, nenhuma tarefa será criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. Você não será perguntado novamente sobre uma assinatura mantida, a menos que o preço mude. **Cancelar** mostra a página de cancelamento ou um rascunho pedindo o cancelamento. A mensagem só será enviada quando você enviar. Entre uma execução e outra, a rotina verifica diariamente e cria uma tarefa se um teste ou uma renovação for cobrado nos próximos 7 dias.

**Manter contato** lembra você de vez em quando de falar com alguém próximo, mas só quando houver um motivo de verdade. No cartão da rotina, escolha quem incluir em uma lista curta de pessoas com quem você conversa por conta própria, nos dois sentidos, ao longo de vários meses. Toque em × para remover alguém.

Você só recebe um lembrete quando faz muito mais tempo do que o normal que vocês não conversam e há algo específico para dizer: uma novidade que a pessoa compartilhou, uma promessa ainda pendente ou uma mensagem que você nunca respondeu. A rotina cria uma tarefa com o motivo e uma mensagem curta, no idioma da pessoa, preparada no canal em que vocês costumam conversar. Ela só é enviada quando você a envia. Se não houver nada a dizer, nenhuma tarefa será criada.

A rotina envia no máximo dois lembretes por semana, um por pessoa a cada mês, e nenhum para alguém com quem você conversou recentemente. Se você tocar em **Não precisa** em um lembrete, a rotina vai esperar mais tempo antes de lembrar você sobre essa pessoa. E vai esperar ainda mais a cada vez que você tocar nessa opção. Ela nunca envia notificações e permanece pessoal: nunca é compartilhada com uma Work Fleet.

Enquanto a rotina de um modelo mantiver as palavras do modelo, ela usará o próprio código, sem usar seu plano de IA. A Limpeza de spam, por exemplo, primeiro lista no código novos e-mails de remetentes desconhecidos e só faz uma pergunta curta à sua IA quando encontra algum. Manter contato só pergunta sobre uma ou duas pessoas que selecionou. Dar um novo nome à rotina não muda isso. Depois que você mudar as palavras, ela passa a funcionar como qualquer outra rotina, usando as palavras que você definiu.

A Limpeza de newsletters e a Limpeza de spam continuam criando a mesma tarefa, com uma opção para cada e-mail. Uma rotina de Aniversários editada mostra o resultado e, no máximo, um rascunho, em vez de criar uma tarefa por pessoa. **Voltar ao modelo**, em **Editar**, restaura as palavras do modelo.

## O que uma rotina faz

No horário definido, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e mostra o resultado na página Rotinas. Cada resultado indica **Para revisar**, **Nada de novo** (com o motivo) ou **Não funcionou** (com o motivo). Uma execução que termina sem resultado conta como uma execução que não funcionou, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da web, GitHub e sites como X no navegador. Elas não enviam, respondem, publicam nem mudam nada. Só um modelo altera e-mails, e apenas o que você confirmar na tarefa dele.

Quando o trabalho de uma rotina termina com uma publicação ou mensagem, ela faz tudo até essa etapa e mostra o rascunho, como **Publicaria no X:**. Depois de uma execução real, o rascunho aparece como uma tarefa para você aprovar. Uma execução de teste apenas o mostra. O nome da tarefa indica o assunto e onde será publicada. O botão indica a etapa, como **Publicar**, e **Da sua rotina**, abaixo dele, abre a rotina.

A tarefa começa na área da conta de onde será enviada, como Trabalho para a conta da sua empresa no X, então você nunca precisa movê-la.

Uma execução pode seguir suas [habilidades](skills.md) ativadas, escolhidas com base no que a rotina faz. A rotina lê por inteiro apenas as habilidades relevantes. O resultado lista as habilidades em **Usadas:**. Uma habilidade nunca faz uma rotina enviar ou alterar nada.

Suas rotinas ficam em **Suas rotinas**, abaixo das sugestões, se houver. Resultados longos são recolhidos e mostram uma prévia curta. Toque em **Mostrar mais**, ou no próprio resultado, para abri-lo.

Cada execução sabe qual foi o último resultado, então pode dizer o que mudou desde então.

Depois de uma boa execução, sua Machine pode escrever uma receita para as etapas de leitura que se repetem, como quais e-mails ou mudanças no GitHub consultar. Nas próximas execuções, ela começa por essas etapas, escritas em código simples. A IA só escolhe o que importa e escreve o resultado, usando menos tokens. Uma receita só lê. Se parar de funcionar, a rotina faz a leitura por conta própria e corrige a receita. Ela aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias sem execução

Se sua Machine estava desligada ou ocupada, as execuções perdidas não se acumulam: só a mais recente é executada, uma vez. Cada data tem uma única execução, mesmo depois de uma reinicialização.

As rotinas rodam uma de cada vez e aguardam quando há pouco uso disponível no seu plano de IA, como todo trabalho em segundo plano. **Rodar agora** inicia a rotina imediatamente. O resultado aparece no cartão quando estiver pronto.

## Mudar ou parar uma rotina

Essas opções ficam no menu ⋯ da rotina. **Editar** muda o nome e o que ela faz. O horário e os resultados anteriores continuam iguais. **Mudar quando** permite definir uma nova frequência com suas próprias palavras, como "todos os dias úteis às 8h". As duas opções têm **Salvar** e **Cancelar**. No computador, Esc ou um clique fora da janela também cancela.

Em **Editar**, **Testar** executa uma vez as novas instruções e mostra o resultado ali. A rotina continua como estava até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar** no cartão. Rotinas pausadas ficam em **Pausado**, abaixo das suas rotinas. As execuções perdidas durante a pausa não são realizadas depois. **Parar** encerra uma rotina de vez.

Você pode ter até 20 rotinas, incluindo as pausadas. Pare uma rotina para adicionar outra.

Quando você usa **Pedir mudanças** na tarefa de uma rotina ou escreve no chat dela, e a observação vale para todas as execuções, como "nunca use emoji", a tarefa oferece **Mudar também a rotina**. Essa opção aparece na tarefa e no chat, abaixo da resposta. A rotina mostra o que vai mudar nas instruções e só muda quando você toca em **Mudar**. **Deixar como está** mantém tudo igual. Se a correção for só para aquele rascunho, essa opção não aparece.

## Avançado: etapas de script

Não é preciso escrever scripts: diga com suas próprias palavras o que uma rotina deve fazer, e sua Machine cuida do resto.

Para usuários avançados, uma rotina também pode executar seus próprios comandos na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** só mostra os comandos quando a rotina já tem algum. **Buscar dados** executa um comando primeiro, na pasta dele (ou na sua pasta pessoal, se o campo estiver vazio), pelo tempo máximo definido em segundos. O que o comando exibe fica disponível para a rotina usar. Se não houver instruções, o que o comando exibir será o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se terminar com erro, a execução mostra **Não funcionou** e a mensagem da verificação. Se um comando de Buscar dados falhar, a execução mostra a mesma coisa.

Cada comando deve ocupar uma linha e é executado sem um shell: não use pipes nem variáveis. As etapas de script são suas e só são configuradas no seu painel. Uma execução de teste e **Testar** também executam Buscar dados e informam isso, mas não enviam nem mantêm nada. Uma rotina nunca envia nada, então uma etapa de script deve apenas ler.

## Das suas tarefas do OpenClaw

Se você já criou tarefas agendadas no OpenClaw, sua Machine as lê, sem nunca alterá-las, e oferece as que podem virar rotinas em **Sugerido**. Cada tarefa foi executada uma vez, então você pode ver um resultado real.

A rotina mantém as correções que você fez na tarefa e exclui o que ela enviou ou publicou. Se a tarefa executou um script ou leu dados coletados por um script, ela traz o script como uma etapa de Buscar dados. **Adicionar** transforma a tarefa em rotina, e **Não, obrigado** impede que a rotina volte a perguntar sobre ela. Uma tarefa que lembrava você de fazer algo aparece como uma sugestão de tarefa recorrente em Tarefas.

Antes de adicionar uma sugestão, use **Editar** e **Mudar quando**, no menu ⋯, para alterá-la como faria com qualquer rotina. **Rodar de novo** executa a rotina com as instruções atuais para mostrar resultados mais recentes, por exemplo, depois de um fim de semana tranquilo. Ela apenas lê, roda uma vez por toque e substitui o resultado anterior pelo novo.

No máximo três sugestões podem ficar pendentes ao mesmo tempo. Depois de uma semana de boas execuções, a rotina pergunta **Desativar o antigo job do OpenClaw?**. Ela só desativa o job se você tocar em **Desativar**. Você pode ativá-lo novamente no OpenClaw. **Manter** deixa os dois em execução.

## Com base no que você faz

Sua Machine também percebe tarefas que você faz com frequência e as oferece como rotinas em **Sugerido**, mesmo que você não use OpenClaw. Ela procura:

- a mesma solicitação três vezes ou mais seguidas, como "resuma os chamados de suporte em aberto" toda segunda-feira;
- um e-mail que você envia com frequência, como um relatório semanal para sua equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como e-mails da escola e do clube para seu parceiro ou sua parceira. Um resumo semanal para essa pessoa evita que você tenha de encaminhar cada e-mail;
- a mesma solicitação que você responde com frequência, como uma aprovação mensal para a mesma pessoa.

Cada sugestão diz o que a rotina percebeu, como "Pedido 4 vezes seguidas" ou "6 e-mails encaminhados para Sam em 3 semanas", e foi executada uma vez para você ver um resultado real. Pense em um resumo da equipe, uma pauta antes de uma reunião semanal, um resumo de suporte ou desenvolvimento, um panorama dos seus números ou um resumo das newsletters que você recebe.

A rotina só sugere tarefas específicas para você e claramente úteis: um resumo de notícias feito apenas com as suas newsletters, nunca um resumo genérico. Se nada se encaixar, nenhuma sugestão será criada.

A rotina faz essa verificação no máximo uma vez por dia e oferece no máximo uma nova sugestão por semana, sem enviar notificações. **Não, obrigado** impede que a sugestão volte a aparecer. Os encaminhamentos e as respostas continuam na conta de onde foram enviados, então Trabalho e Pessoal não se misturam. Tudo permanece na sua Machine. Uma tarefa que você conclui com frequência aparece como uma sugestão de tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma [tarefa recorrente](recurring.md) lembra você de fazer algo. Uma rotina é um trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para "pagar o aluguel no primeiro dia do mês" e uma rotina para "toda sexta-feira, me diga quais oportunidades estão paradas".
