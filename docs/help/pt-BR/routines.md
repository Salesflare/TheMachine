---
title: Rotinas
area: cards
summary: Trabalhos que sua Machine faz sozinha, em uma frequência definida, como um resumo das suas oportunidades em aberto às segundas-feiras. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 57b97c44b031845f
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga, em uma linha, o que ela deve fazer e quando: "toda segunda-feira às 9h, faça um resumo das minhas oportunidades em aberto" ou "todas as manhãs dos dias úteis, liste os e-mails que ainda preciso responder". Depois, toque em **Adicionar**.

Se você não definir um horário, ela será executada às 8h. O horário segue o relógio da sua Machine. A primeira execução dá um nome curto à rotina.

Primeiro, **Adicionar** faz um teste para você ver o resultado antes de manter a rotina. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina na frequência definida, **Mudar** testa outras palavras ou um nome novo, e **Cancelar** exclui a rotina.

## Modelos

Em **Modelos**, no fim de Rotinas, toque em **Adicionar** para ativar uma rotina pronta. Ela é executada uma vez na hora e, depois, todas as manhãs às 7h30. A Limpeza de spam é executada de hora em hora, Achados de usados a cada 3 horas, e Assinaturas e testes uma vez por mês. O cartão mostra as instruções da rotina, e **Editar** permite alterá-las ou mudar o nome.

Quando chegam muitas newsletters e a Limpeza de newsletters está desativada, aparece uma linha acima das suas tarefas informando quantas chegaram e o que a rotina faria, com as opções **Ativar** e **Não, obrigado**. Isso acontece quando chegam 25 ou mais newsletters de pelo menos 5 remetentes em uma semana.

A Limpeza de spam é oferecida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para spam em uma semana. **Ativar** adiciona a rotina, assim como **Adicionar** nesta seção. Ao tocar em **Não, obrigado**, ela não será oferecida novamente. Isso também vale para um modelo que você já tenha usado.

A **Limpeza de newsletters** cria uma tarefa para cada área, trabalho e pessoal, com as newsletters do dia anterior. Cada uma tem as opções **Manter** ou **Cancelar inscrição**. Para cancelar a inscrição, a rotina usa o link de cancelamento com um clique da lista ou, se o envio estiver ativado, envia uma mensagem de cancelamento do seu endereço. Caso contrário, The Machine cancela sua inscrição na página da lista, usando o próprio navegador. Se for preciso fazer login, resolver um CAPTCHA ou escolher alguma opção, você cuida disso. A tarefa explica o motivo e mostra **Abrir página de cancelamento**.

Se você só quer parar de receber tarefas de uma lista, sem deixar de receber os e-mails dela, diga "Nenhum e-mail desta lista precisa virar uma tarefa" no chat de uma mensagem da lista.

Recibos, pedidos e avisos de pagamento são ignorados. E-mails enviados por um endereço de grupo, como um Google Group, aparecem com o nome de quem os escreveu e nunca cancelam sua inscrição no grupo. Quando o remetente não oferece uma forma própria de cancelamento, a tarefa mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa por área com e-mails de remetentes desconhecidos que parecem spam. Cada um tem as opções **Spam** e **Não é spam**. O Outlook move o spam para a pasta Lixo Eletrônico, e o Gmail marca o e-mail como spam. A rotina verifica os e-mails de hora em hora, então o spam geralmente já está lá antes de você. Enquanto a tarefa estiver aberta, novos e-mails de spam são adicionados a ela.

Uma conta do Gmail conectada com acesso somente para leitura, como em uma Machine hospedada, não pode mover e-mails para spam. Nesse caso, **Spam** mostra um link para marcar o e-mail como spam no Gmail, e The Machine memoriza o remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Um remetente é desconhecido quando você nunca escreveu para ele. Um "Re:" só conta como conversa em uma conversa por e-mail na qual você escreveu. Se um e-mail de um remetente que você marcou como spam, na tarefa ou na caixa de entrada, chegar de novo, ele será incluído na próxima tarefa com o aviso **Já marcado como spam**. Os e-mails que você mesma marcou como spam também ajudam a rotina a identificar mensagens parecidas.

Nada muda até você confirmar na tarefa. Toque em um remetente para ler o e-mail primeiro. Ele continua como não lido e nada muda. Na Limpeza de spam, as imagens da internet não são carregadas, para que o remetente não saiba que o e-mail foi aberto. A rotina não pergunta de novo sobre remetentes que você já avaliou. Se não houver newsletters ou spam em um dia, nenhuma tarefa será criada. Essas tarefas nunca enviam notificações.

Depois que você avaliar todos os remetentes, a tarefa informa que foi concluída e mostra **Marcar como feito**.

O **Resumo diário** escolhe, uma vez por dia, as poucas matérias de newsletters que valem seu tempo e as reúne em uma tarefa. Cada uma explica em uma linha por que é relevante para você. Toque em uma matéria para ler o e-mail ou use **Abrir no seu e-mail**. A rotina considera apenas newsletters, nunca e-mails de pessoas, recibos ou mensagens de remetentes dos quais você cancelou a inscrição, e nunca inclui algo que você já leu. Se nada se destacar, nenhuma tarefa será criada.

A rotina aprende o que é importante para você com base no que abre, marca com estrela ou arquiva sem ler, além do que você indica com **Mais assim** e **Menos assim** em cada sugestão. Os temas que ela seleciona aparecem no cartão da rotina, em **Mais de** e **Menos de**. Toque em × para remover um tema ou adicione o seu. Os temas com linha tracejada foram aprendidos pela rotina. Um novo resumo substitui o anterior que ainda estiver aberto e nunca envia notificações.

A rotina lê apenas o remetente, o assunto e o início de cada newsletter nova e faz uma pergunta curta à sua IA sobre elas, com um limite diário para manter o custo baixo. **Mudar quando** altera o horário. Depois que você muda as instruções, a rotina passa a funcionar como qualquer outra, seguindo o que você escreveu.

**Aniversários** cria uma tarefa para cada contato próximo que faz aniversário hoje: pessoas para quem você mesma escreve, como amigos, familiares e contatos frequentes. Cada tarefa inclui uma mensagem curta de felicitação, escrita no lugar em que você costuma conversar com a pessoa, como o chat dela no WhatsApp ou a conversa por e-mail, no idioma dela. A mensagem só é enviada quando você a envia. Se ninguém fizer aniversário, nenhuma tarefa será criada.

Os aniversários vêm dos seus calendários: eventos de aniversário do Google e o calendário Aniversários, que são lidos todas as manhãs mesmo quando não estão sincronizados, e o calendário Aniversários do Outlook. Também podem vir dos seus contatos do Google em uma Machine auto-hospedada e de um campo de data chamado Birthday de uma pessoa no Graph. Se ainda não houver aniversários nessas fontes, o resultado mostrará **Ainda não há informações de aniversário** e explicará como adicionar algumas.

**Importar aniversários do Facebook**: depois que Aniversários estiver ativado, uma tarefa oferece a opção de ler a página de aniversários do Facebook. Toque em **Importar** e The Machine abre a página no próprio navegador, rola até carregar todos os meses e lê o nome e a data de aniversário de cada amizade. Ela informa quantos aniversários encontrou e quais pessoas correspondem a contatos no seu Graph, usando o nome e o sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela não será incluída e aparecerá na lista.

Só **Salvar** adiciona os dados à página de cada pessoa: o aniversário e a foto do perfil do Facebook, se a pessoa ainda não tiver uma foto. Um aniversário ou uma foto que você definir na página da pessoa será mantido, e uma foto que ela já tenha nunca será substituída. Nada é escrito no Facebook.

A rotina não lê os dados de novo sozinha. Para isso, toque em **Importar de novo** na tarefa. O navegador precisa estar conectado ao Facebook. Se não estiver, toque em **Entrar no Facebook** na tarefa e faça login. Depois que você entrar, a rotina lê a página automaticamente. The Machine nunca faz login por você.

A rotina conta as amizades que não correspondem a ninguém no seu Graph e mostra alguns nomes. **Adicionar … como contatos pessoais** adiciona todas de uma vez, também depois de tocar em Salvar: cada pessoa com nome e aniversário, sem compartilhar os dados com um Fleet de Trabalho. A rotina ignora nomes que já pertençam a alguém no seu Graph ou a alguém que você tenha excluído permanentemente. Você só recebe lembretes de aniversário de pessoas para quem escreve.

**Desfazer** na tarefa remove exatamente aquelas pessoas, mesmo depois de tocar em **Importar de novo**.

**Assinaturas e testes** lê recibos, faturas e avisos de renovação uma vez por mês e reúne suas assinaturas em uma tarefa. A tarefa mostra o custo de cada uma, a próxima data de cobrança e um aviso quando um período de teste termina ou o preço aumenta. Só aparecem as assinaturas que a rotina consegue identificar com segurança. Se nenhuma for encontrada, nenhuma tarefa será criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. A rotina não pergunta de novo sobre uma assinatura mantida, a menos que o preço mude. **Cancelar** mostra a página de cancelamento ou um rascunho pedindo o cancelamento, que só é enviado quando você o envia. Entre as execuções mensais, a rotina verifica tudo diariamente e cria uma tarefa quando um período de teste termina ou uma cobrança de renovação acontece em até 7 dias.

**Manter contato** lembra você de falar com alguém próximo de vez em quando, mas só quando há um motivo concreto. No cartão da rotina, escolha quem incluir a partir de uma lista curta de pessoas com quem você mesma conversa há meses, nos dois sentidos. Toque em × para remover alguém.

A rotina só envia um lembrete quando faz muito mais tempo que o normal desde a última conversa e há algo específico a dizer: novidades que a pessoa compartilhou, inclusive as do resumo na página dela, uma promessa ainda pendente ou uma mensagem que você nunca respondeu.

Se uma novidade tem uma data futura, como uma mudança no mês que vem, a rotina volta a verificá-la logo depois dessa data, junto com as mensagens mais recentes da pessoa. A novidade aparece em uma tarefa com o motivo e uma mensagem curta escrita no lugar em que você costuma conversar com a pessoa, no idioma dela. A mensagem só é enviada quando você a envia. Se não houver nada a dizer, nenhuma tarefa será criada.

A rotina envia no máximo dois lembretes por semana e um por pessoa por mês. Ela não envia lembretes para quem recebeu uma mensagem sua recentemente. Ao tocar em **Não precisa** em um lembrete, você aumenta o intervalo até o próximo lembrete para aquela pessoa. Esse intervalo aumenta de novo a cada vez. A rotina nunca envia notificações e permanece pessoal: não é compartilhada com um Fleet de Trabalho e nunca se baseia no que chegou às suas contas de trabalho.

**Achados de usados** acompanha uma busca em um site de produtos usados, como Marktplaats, Vinted, eBay ou Facebook Marketplace. Faça a busca com os filtros que quiser, copie o endereço dos resultados e cole-o depois de tocar em **Adicionar**. Se quiser, inclua filtros nas suas próprias palavras, como “menos de 300, até 30 km, sem ‘para peças’”. Cada busca é uma rotina separada, então adicione uma nova para acompanhar outra busca.

A cada 3 horas, a rotina abre a busca no navegador da própria The Machine e procura anúncios que ainda não viu. O preço, a distância e os termos que você quer excluir são verificados primeiro, com código simples.

Cada novo anúncio que passar por essa verificação é aberto. Sua IA avalia o estado do produto com base na foto e na descrição, e avalia o vendedor com base nas avaliações, na classificação e no tempo de existência da conta. Os anúncios que parecem bons são reunidos em uma tarefa, cada um com foto, título, preço e uma avaliação em uma linha. Toque em um anúncio para abri-lo no navegador da The Machine.

Enquanto a tarefa estiver aberta, novos achados são adicionados ao início da lista, a quantidade aumenta e você recebe outra notificação, porque as boas ofertas acabam rápido. Marque a tarefa como feita para que o próximo achado inicie uma nova. Se uma execução não encontrar nada bom, nada muda.

A rotina é cuidadosa e econômica: lê a busca uma vez por execução, abre no máximo 6 anúncios por execução, com uma pausa entre eles, e verifica no máximo 40 anúncios por dia em todas as suas buscas. Cada verificação é uma pergunta curta à sua IA com uma foto. Na primeira execução, a rotina verifica os anúncios mais recentes e marca os demais como vistos, para que as próximas execuções tragam apenas novidades.

Se o site pedir que você entre, mostrar uma verificação de robô ou impedir a leitura, uma tarefa avisa você e mostra **Abrir** para ver a página no navegador da The Machine. Entre ou resolva a verificação você mesma. A próxima execução fará uma nova leitura. The Machine nunca faz login nem resolve verificações por você, e nunca entra em contato com vendedores, dá lances ou compra.

**Alterar busca** no cartão da rotina permite usar outro endereço ou outros filtros. **Mudar quando** altera a frequência, por exemplo, para “a cada 6 horas”.

**Recompras** lê as confirmações de pedidos de lojas on-line no seu e-mail e identifica os produtos que você compra repetidamente, como café, ração ou vitaminas. Quando provavelmente estiver na hora de comprar um deles de novo, a rotina cria uma tarefa com o produto, a loja, o último preço e a data da última compra. **Abrir na loja** leva você à página do produto para comprá-lo. A rotina não compra nada por você.

A rotina precisa encontrar pelo menos três pedidos do mesmo produto em intervalos regulares. Por isso, uma compra única ou um intervalo incomum não cria uma tarefa. Por enquanto, ela lê e-mails de lojas que usam Shopify. Sua IA lê apenas e-mails novos de pedidos dessas lojas, com uma pergunta curta por execução. Essas tarefas nunca enviam notificações. Fazer um novo pedido do produto fecha a tarefa aberta.

Enquanto uma rotina de modelo mantiver as instruções do modelo, ela será executada com código próprio, sem usar o plano da sua IA. A Limpeza de spam, por exemplo, primeiro lista com código os e-mails novos de remetentes desconhecidos e só faz uma pergunta curta à sua IA quando encontra algum. Manter contato só pergunta sobre uma ou duas pessoas que selecionou. Quando você muda as instruções, a rotina passa a funcionar como qualquer outra, seguindo o que você escreveu.

A Limpeza de newsletters e a Limpeza de spam continuam criando uma única tarefa, com uma opção para cada e-mail. Uma rotina Aniversários editada mostra o resultado e, no máximo, um rascunho, em vez de criar uma tarefa por pessoa. Em **Editar**, toque em **Voltar ao modelo** para restaurar as instruções originais.

## Como uma rotina funciona

No horário definido, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e coloca o resultado na página Rotinas. Cada resultado mostra **Para revisar**, **Nada de novo** com o motivo ou **Não funcionou** com o motivo. Uma execução que termina sem resultado conta como uma falha, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da Web, GitHub e sites como X no navegador. Elas não enviam mensagens, respondem, publicam nem alteram nada. Elas abrem páginas encontradas no que leram ou em uma busca, endereços simples de páginas e sites conhecidos. Nunca abrem um endereço inventado para transportar o conteúdo que leram. Só um modelo pode alterar e-mails, e apenas aquilo que você confirmar na tarefa correspondente.

Quando a tarefa de uma rotina termina com uma publicação ou mensagem, ela faz tudo até essa etapa e mostra o rascunho, por exemplo, **Publicaria no X:**. Depois de uma execução real, o rascunho vira uma tarefa para você aprovar. Uma execução de teste só mostra o rascunho.

O nome da rotina informa do que ela trata e onde o resultado será publicado. **Da sua rotina**, abaixo do nome, abre a rotina. O botão indica a etapa, como **Preparar publicação**. Ele prepara o conteúdo, mas não publica nada. Você publica a partir do resultado. Se The Machine não puder publicar por você, o botão abre a página em que você pode fazer isso.

A tarefa começa na área da conta pela qual será enviada, como Trabalho para a conta da sua empresa no X. Assim, a rotina nunca pede que você a mova.

Uma execução pode seguir suas [habilidades](skills.md) ativadas, selecionadas de acordo com o que a rotina faz. Ela lê por inteiro apenas as habilidades pertinentes. O resultado lista essas habilidades em **Usadas:**. Uma habilidade nunca faz uma rotina enviar ou alterar algo.

Suas rotinas aparecem em **Suas rotinas**, abaixo de qualquer sugestão. Resultados longos são recolhidos em uma prévia curta. Toque em **Mostrar mais** ou no resultado para abri-lo.

Cada execução conhece o resultado anterior e pode dizer o que mudou desde então.

Depois de uma execução bem-sucedida, sua Machine pode criar uma receita para fazer a leitura que se repete da mesma forma, como verificar determinados e-mails ou alterações no GitHub. Nas próximas execuções, ela lê esses dados primeiro, usando código simples. Depois, a IA seleciona o que importa e escreve o resultado, com menos tokens. Uma receita só lê. Se deixar de funcionar, a execução faz a leitura por conta própria e corrige o problema. A receita aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias sem execução

Se sua Machine estiver desligada ou ocupada, as execuções perdidas não se acumulam. Só a mais recente é executada, uma vez. Cada data é processada uma vez, mesmo depois de uma reinicialização.

As rotinas são executadas uma de cada vez e aguardam quando o uso do plano da sua IA está baixo, assim como qualquer tarefa em segundo plano. **Rodar agora** executa a rotina imediatamente. O resultado aparece no cartão quando estiver pronto.

## Alterar ou interromper uma rotina

Essas opções estão no menu ⋯ da rotina. **Editar** permite mudar o nome e o que ela faz. O horário e os resultados anteriores são mantidos. **Mudar quando** permite definir outra frequência com suas próprias palavras, como “todos os dias úteis às 8h”. As duas opções têm **Salvar** e **Cancelar**. No computador, você também pode cancelar com Esc ou clicando fora da janela.

Em **Editar**, **Testar** executa as novas instruções uma vez e mostra o resultado ali. A rotina continua como estava até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar** no cartão. Rotinas pausadas ficam em **Pausado**, abaixo das suas rotinas, e as execuções perdidas durante a pausa não são retomadas. **Parar** encerra uma rotina definitivamente.

Você pode ter até 20 rotinas, incluindo as pausadas. Pare uma rotina para adicionar outra.

Quando você usa **Pedir mudanças** na tarefa de uma rotina ou escreve no chat dela, e sua observação vale para todas as execuções, como “nunca use emojis”, a tarefa oferece **Mudar também a rotina**. Essa opção aparece na tarefa e no chat, abaixo da resposta. Ela mostra as alterações nas instruções da rotina, que só são aplicadas quando você toca em **Mudar**. **Deixar como está** mantém tudo igual. Se a alteração servir apenas para aquele rascunho, a opção não será oferecida.

## Avançado: etapas de script

Não precisa escrever um script: diga com suas próprias palavras o que a rotina deve fazer, e sua Machine cuida do resto.

Usuários avançados também podem executar comandos próprios na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** só mostra as etapas quando a rotina já tem alguma. **Buscar dados** executa um comando primeiro, na pasta definida, ou na sua pasta pessoal se o campo estiver vazio, por no máximo o número de segundos indicado. O que o comando imprimir será usado pela execução. Se você não escrever instruções, o que ele imprimir será o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se o comando terminar com um erro, a execução mostrará **Não funcionou** com a mensagem da verificação. Um comando de Buscar dados que falhar também mostrará a mesma mensagem.

Cada comando deve ficar em uma linha e é executado sem um shell. Não use pipes nem variáveis. As etapas de script são suas e só podem ser configuradas no seu painel. Uma execução de teste e uma execução de **Testar** também executam Buscar dados e informam isso. Elas continuam sem enviar nem manter nada. Uma rotina nunca envia nada, então uma etapa de script só deve ler.

## Dos seus jobs do OpenClaw

Se você já criou jobs programados no OpenClaw, sua Machine os lê, sem alterá-los, e oferece como rotinas em **Sugerido** aqueles que forem adequados. Cada um foi executado uma vez para que você veja um resultado real.

A rotina mantém as correções que você fez no job e exclui o que ele enviou ou publicou. Se o job executava um script ou lia dados coletados por um job de script, esse conteúdo é incluído como Buscar dados. **Adicionar** cria uma rotina. **Não, obrigado** impede que a rotina pergunte de novo sobre aquele job. Um job que lembrava você de fazer algo é oferecido como uma tarefa recorrente em Tarefas.

Antes de adicionar uma sugestão, **Editar** e **Mudar quando**, no menu ⋯, permitem alterá-la como qualquer rotina. **Rodar de novo** executa a rotina imediatamente com as instruções atuais para mostrar resultados mais recentes, por exemplo, depois de um fim de semana tranquilo. Ela só lê, executa uma vez por toque e substitui o resultado anterior pelo novo.

No máximo três sugestões podem ficar pendentes ao mesmo tempo. Depois de uma semana de execuções bem-sucedidas, a rotina pergunta **Desativar o antigo job do OpenClaw?**. O job só é desativado se você tocar em **Desativar**. Você pode reativá-lo no OpenClaw. **Manter** deixa os dois em execução.

## Com base no que você faz

Sua Machine também percebe tarefas que você faz com frequência e as oferece como rotinas em **Sugerido**, mesmo sem o OpenClaw. Ela procura:

- o mesmo pedido feito três vezes seguidas ou mais, como “resuma os chamados de suporte em aberto” toda segunda-feira;
- um e-mail que você envia com frequência, como um relatório semanal para sua equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como mensagens da escola e do clube para seu parceiro. Um resumo semanal poupa o trabalho de encaminhá-las;
- o mesmo pedido que você atende com frequência, como uma aprovação mensal para a mesma pessoa.

Cada sugestão explica o que a rotina identificou, como “Pedido feito 4 vezes seguidas” ou “6 e-mails encaminhados para Sam em 3 semanas”, e já foi executada uma vez para que você veja um resultado real. Experimente criar um resumo da equipe, um briefing antes de uma reunião semanal, um resumo de suporte ou desenvolvimento, um acompanhamento dos seus números ou um resumo das newsletters que você recebe.

A rotina só sugere algo específico para você e claramente útil. Por exemplo, um resumo de notícias inclui apenas as suas newsletters, nunca um resumo genérico. Se nada for adequado, nenhuma sugestão será criada.

A rotina procura sugestões no máximo uma vez por dia e mostra no máximo uma nova sugestão por semana, sem enviar notificações. **Não, obrigado** impede que aquela sugestão apareça de novo. Os encaminhamentos e as respostas permanecem na conta pela qual foram enviados, então Trabalho e Pessoal não se misturam. Tudo permanece na sua Machine. Uma tarefa que você conclui com frequência é oferecida como tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma [tarefa recorrente](recurring.md) lembra você de fazer algo. Uma rotina é um trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para “pagar o aluguel no dia 1º” e uma rotina para “toda sexta-feira, me diga quais oportunidades estão paradas”.
