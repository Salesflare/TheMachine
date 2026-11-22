---
title: Rotinas
area: cards
summary: Tarefas que sua Machine realiza sozinha, em uma frequência definida, como um resumo das suas oportunidades em aberto toda segunda-feira. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: b5704836b00227a5
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga o que ela deve fazer e quando, em uma linha: "toda segunda-feira às 9h, resuma minhas oportunidades em aberto" ou "todas as manhãs de dias úteis, liste os e-mails que ainda preciso responder". Depois, **Adicionar**.

Se você não definir um horário, ela será executada às 8h. O horário segue o relógio da sua Machine. Na primeira execução, ela recebe um nome curto.

Ao tocar em **Adicionar**, a rotina é executada para teste primeiro, para você ver o resultado antes de mantê-la. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina na frequência definida, **Mudar** testa outras palavras ou um nome novo, e **Cancelar** a remove.

## Modelos

Em **Modelos**, na parte de baixo de Rotinas, **Adicionar** ativa uma rotina pronta. Ela é executada uma vez na hora e, depois, todas as manhãs às 7h30. A Limpeza de spam é executada a cada hora, Achados de usados a cada 3 horas, e Assinaturas e testes uma vez por mês. O cartão mostra as palavras da rotina, como em qualquer outra, e **Editar** permite mudar essas palavras ou o nome.

Quando chegam muitas newsletters e a Limpeza de newsletters está desativada, uma linha acima das suas tarefas informa quantas chegaram e o que a rotina faria. Isso acontece quando chegam 25 ou mais newsletters em uma semana, de pelo menos 5 remetentes. A linha mostra as opções **Ativar** e **Não, obrigado**.

A Limpeza de spam é oferecida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para spam em uma semana. **Ativar** adiciona a rotina, como **Adicionar** faz aqui. Se você tocar em **Não, obrigado**, ela não será oferecida novamente. O mesmo vale para um modelo que você já teve.

A **Limpeza de newsletters** cria uma tarefa para cada área, trabalho e pessoal, com as newsletters do último dia. Cada uma tem as opções **Manter** e **Cancelar inscrição**. Para cancelar a inscrição, a rotina usa o link de cancelamento com um clique da lista ou envia um e-mail de cancelamento do seu endereço, se o envio de e-mails estiver ativado. Caso contrário, The Machine cancela a inscrição na página da lista, usando o próprio navegador. Se a página exigir login, um captcha ou que você escolha opções, isso fica por sua conta. A tarefa explica o motivo e mostra **Abrir página de cancelamento**.

Recibos, pedidos e avisos de pagamento ficam de fora. E-mails recebidos por um endereço de grupo, como um Grupo do Google, aparecem com o nome de quem os escreveu. A rotina nunca cancela sua inscrição no grupo. Se o remetente não tiver uma opção própria de cancelamento, a tarefa mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa para cada área com e-mails de remetentes desconhecidos que parecem spam. Cada e-mail tem as opções **Spam** e **Não é spam**. No Outlook, a rotina move o spam para a pasta de lixo eletrônico. No Gmail, marca o e-mail como spam. Ela verifica a cada hora, então o spam costuma aparecer antes de você chegar até ele. Se a tarefa ainda estiver aberta, novos e-mails de spam são adicionados a ela.

Se o Gmail estiver conectado somente para leitura, como em uma Machine hospedada, a rotina não poderá mover e-mails para spam. Nesse caso, **Spam** mostra um link para marcar o e-mail como spam no Gmail, e The Machine guarda o remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Remetentes desconhecidos são aqueles para quem você nunca escreveu. Um "Re:" só conta como uma conversa em uma conversa na qual você escreveu. Se um e-mail de um remetente que você marcou como spam, na tarefa ou na sua caixa de entrada, chegar de novo, ele aparecerá na próxima tarefa como **Já marcado como spam**. Os e-mails que você mesmo moveu para spam também ajudam a rotina a encontrar e-mails parecidos.

Nada muda até você confirmar na tarefa. Toque no remetente para ler o e-mail primeiro: ele continua não lido e nada muda. Na Limpeza de spam, as imagens da internet não carregam, para que o remetente não saiba que você abriu o e-mail. Os remetentes sobre os quais você já decidiu não serão perguntados de novo. Se não houver newsletters ou spam em um dia, nenhuma tarefa será criada. Essas tarefas nunca enviam notificações.

Quando você decidir sobre todos os remetentes, a tarefa informa que foi concluída e mostra **Marcar como feita**.

O **Resumo diário** escolhe, uma vez por dia, as poucas notícias de newsletters que valem seu tempo e reúne tudo em uma tarefa. Cada item explica em uma linha por que é relevante para você. Toque em um item para ler o e-mail ou use **Abrir no seu e-mail**. A rotina considera somente newsletters, nunca e-mails de pessoas, recibos ou remetentes de cuja lista você cancelou a inscrição. Também não inclui e-mails que você já leu. Se nada se destacar, nenhuma tarefa será criada.

A rotina aprende o que interessa para você com base no que abre, marca com estrela ou arquiva sem ler, além das opções **Mais assim** e **Menos assim** em cada sugestão. Os assuntos usados para escolher os itens aparecem no cartão da rotina, em **Mais de** e **Menos de**. Toque em × para remover um assunto ou adicione o seu. Os assuntos com linha tracejada foram aprendidos pela rotina. Um novo resumo substitui o que ainda estiver aberto e nunca envia notificações.

Ela lê somente o remetente, o assunto e o início de cada newsletter nova, e faz uma pergunta curta sobre elas à sua IA, com um limite diário para manter os custos baixos. **Mudar quando** define o horário. Depois que você muda as palavras da rotina, ela passa a ser executada como qualquer outra, com base nas palavras que você definiu.

**Aniversários** cria uma tarefa para cada pessoa próxima que faz aniversário hoje: pessoas para quem você mesmo escreve, como amigos, familiares e contatos frequentes. Para cada pessoa, a rotina prepara uma mensagem curta de aniversário no lugar em que você costuma conversar com ela, como o chat do WhatsApp ou a conversa de e-mail, e no idioma dela. A mensagem só é enviada quando você envia. Se ninguém fizer aniversário naquele dia, nenhuma tarefa será criada.

Os aniversários vêm dos seus calendários: eventos de aniversário do Google e o calendário Aniversários, que é lido todas as manhãs mesmo quando não está sincronizado, e o calendário Aniversários do Outlook. Também podem vir dos seus contatos do Google, em uma Machine auto-hospedada, e de um campo de data chamado Birthday em uma pessoa do Graph. Se nenhum deles tiver um aniversário, o resultado mostra **Ainda não há informações de aniversário** e explica como adicionar essas informações.

**Importar aniversários do Facebook**: quando Aniversários estiver ativada, uma tarefa oferecerá a opção de ler a página de aniversários do Facebook. Toque em **Importar** e The Machine abrirá a página no navegador, rolará até que todos os meses tenham carregado e lerá o nome e o aniversário de cada amigo. Ela mostra quantos aniversários encontrou e quais nomes correspondem a pessoas no seu Graph, com base no nome e sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela será ignorada e listada.

Só **Salvar** adiciona as informações, na página de cada pessoa: o aniversário e a foto de perfil do Facebook, se a pessoa ainda não tiver uma foto. Um aniversário ou uma foto que você já adicionou permanece como está. Uma foto que a pessoa já tem nunca é substituída. Nada é escrito no Facebook.

A rotina nunca lê a página de novo sozinha. Para fazer isso, toque em **Importar de novo** na tarefa. O navegador precisa estar conectado ao Facebook. Se não estiver, toque em **Entrar no Facebook** na tarefa e entre por lá. Depois que você entrar, a rotina lê a página sozinha. The Machine nunca entra na sua conta por você.

A rotina conta os amigos que não estão no seu Graph e mostra alguns nomes. **Adicionar … como contatos pessoais** adiciona todos de uma vez, inclusive depois de tocar em Salvar: cada pessoa é adicionada com nome e aniversário, e nunca é compartilhada com um Fleet de Trabalho. Uma pessoa cujo nome já existe no seu Graph, ou que você excluiu permanentemente, é ignorada. Os lembretes de aniversário continuam aparecendo somente para as pessoas com quem você conversa.

**Desfazer** na tarefa remove exatamente essas pessoas, inclusive depois de tocar em **Importar de novo**.

**Assinaturas e testes** lê recibos, faturas e avisos de renovação uma vez por mês e reúne as assinaturas em uma tarefa. Ela mostra o custo de cada uma, a próxima data de cobrança e um aviso quando um período de teste está terminando ou o preço aumenta. A lista inclui somente as assinaturas que a rotina consegue identificar com segurança. Se ela não encontrar nenhuma, nenhuma tarefa será criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. Uma assinatura mantida não será mencionada de novo, a menos que o preço mude. **Cancelar** mostra a página de cancelamento ou prepara uma mensagem pedindo o cancelamento, que só é enviada quando você envia. Entre uma execução e outra, a rotina verifica tudo diariamente e cria uma tarefa quando um teste ou uma renovação será cobrado nos próximos 7 dias.

**Manter contato** lembra você de vez em quando de falar com alguém próximo, mas só quando há um motivo concreto. No cartão da rotina, escolha quem incluir, em uma lista curta de pessoas com quem você conversa diretamente, nos dois sentidos, ao longo de vários meses. Toque em × para remover alguém.

A rotina só envia um lembrete quando faz muito mais tempo do que o normal que você não conversa com a pessoa e há algo específico para dizer: uma novidade que ela compartilhou, uma promessa ainda em aberto ou uma mensagem que você nunca respondeu. Ela cria uma tarefa com o motivo e uma mensagem curta preparada no lugar em que você costuma conversar com a pessoa, no idioma dela. A mensagem só é enviada quando você envia. Se não houver nada a dizer, nenhuma tarefa será criada.

A rotina envia no máximo dois lembretes por semana e um por pessoa por mês. Ela não envia lembretes para alguém com quem você conversou recentemente. Se você tocar em **Não precisa** em um lembrete, ela esperará mais tempo antes de lembrar você daquela pessoa. O tempo de espera aumenta a cada vez. A rotina nunca envia notificações e fica sempre em Pessoal: nunca é compartilhada com um Fleet de Trabalho.

**Achados de usados** acompanha uma busca em um site de usados, como Marktplaats, Vinted, eBay ou Facebook Marketplace. Faça a busca no site com os filtros que quiser, copie o endereço dos resultados e cole-o depois de tocar em **Adicionar**. Se quiser, adicione filtros com suas próprias palavras, como "até 300, em um raio de 30 km, sem ‘para peças’". Cada busca é uma rotina própria, então adicione outra para a próxima busca.

A cada 3 horas, a rotina abre a busca no próprio navegador da Machine e procura anúncios que ainda não viu. O preço, a distância e os termos que você excluiu são verificados primeiro, usando código simples.

Cada novo anúncio que passar por essa verificação é aberto. Sua IA avalia o estado do produto com base na foto e na descrição, e o vendedor com base nas avaliações, na nota e no tempo de existência da conta. Os bons anúncios aparecem em uma tarefa, cada um com foto, título, preço e uma avaliação em uma linha. Toque em um anúncio para abri-lo no navegador da Machine.

Enquanto a tarefa estiver aberta, novos anúncios serão adicionados no início da lista, o número de anúncios aumentará e você receberá outra notificação, porque boas ofertas podem desaparecer rápido. Marque a tarefa como feita para que o próximo anúncio crie uma nova. Se uma execução não encontrar nada bom, nada muda.

A rotina é econômica e cuidadosa: lê a busca uma vez por execução, abre no máximo 6 anúncios por execução, com uma pausa entre eles, e verifica no máximo 40 anúncios por dia em todas as suas buscas. Cada verificação é uma pergunta curta à sua IA, com uma foto. Na primeira execução, a rotina verifica os anúncios mais recentes e marca o restante como já visto. Assim, nas próximas execuções, ela mostra somente o que há de novo.

Se o site pedir que você entre na sua conta, mostrar um teste de verificação de robô ou impedir a leitura, uma tarefa avisará você. Toque em **Abrir** para ver a página no navegador da Machine. Entre na sua conta ou faça a verificação por lá. Na próxima execução, a rotina tentará ler a página de novo. The Machine nunca entra na sua conta nem resolve testes de verificação por você, e nunca entra em contato com vendedores, faz lances ou compra.

**Alterar busca** no cartão da rotina permite usar um novo endereço ou filtros. **Mudar quando** define outra frequência, como "a cada 6 horas".

**Reordenações** lê as confirmações de pedidos de lojas online no seu e-mail e percebe o que você compra repetidamente, como café, ração ou vitaminas. Quando provavelmente chegar a hora de comprar algo de novo, a rotina cria uma tarefa com o produto, a loja, o último preço e a data da última compra. **Abrir na loja** leva você à página do produto para comprá-lo. Nada é comprado por você.

A rotina precisa encontrar pelo menos três pedidos do mesmo produto em intervalos regulares. Por isso, uma compra isolada ou um intervalo fora do normal não cria uma tarefa. Por enquanto, ela lê pedidos de lojas que usam Shopify. A sua IA lê somente novos e-mails de pedido dessas lojas, com uma pergunta curta por execução. Essas tarefas nunca enviam notificações. Quando você pede o produto de novo, a tarefa aberta é encerrada.

Enquanto a rotina de um modelo mantiver as palavras do modelo, ela será executada com seu próprio código, sem usar o plano da sua IA. A Limpeza de spam, por exemplo, lista primeiro no código os e-mails novos de remetentes desconhecidos e só faz uma pergunta curta à sua IA quando encontra algum. Manter contato só pergunta sobre uma ou duas pessoas escolhidas. Se você mudar as palavras da rotina, ela passa a ser executada como qualquer outra, com base nas palavras que você definiu.

A Limpeza de newsletters e a Limpeza de spam ainda criam uma tarefa com uma escolha para cada e-mail. Se você editar Aniversários, ela mostrará o resultado e, no máximo, um rascunho, em vez de uma tarefa por pessoa. Em **Editar**, toque em **Voltar ao modelo** para restaurar as palavras do modelo.

## O que uma rotina faz

No horário programado, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e mostra o resultado na página Rotinas. Cada resultado mostra **Para revisar**, **Nada de novo** com o motivo ou **Não funcionou** com o motivo. Uma execução que termina sem resultado conta como uma execução que não funcionou, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da Web, GitHub e sites como X no navegador. Elas não enviam mensagens, respondem, publicam nem alteram nada. Elas abrem páginas encontradas no que leram ou em uma busca, endereços diretos de páginas e sites conhecidos. Nunca abrem um endereço inventado para transportar o que leram. Somente um modelo altera e-mails, e apenas o que você confirmar na tarefa correspondente.

Quando uma rotina deve publicar ou enviar uma mensagem, ela faz tudo até essa etapa e mostra o rascunho, como em **Publicaria no X:**. Depois de uma execução real, o rascunho aparece como uma tarefa para você aprovar. Em uma execução de teste, ele apenas é mostrado. O nome da rotina informa o assunto e o destino, e o botão indica a etapa, como **Publicar**. Toque em **Da sua rotina**, abaixo do botão, para abrir a rotina.

A tarefa começa na área da conta de onde será enviada, como Trabalho para a conta X da sua empresa, então não é preciso pedir para movê-la.

Uma execução pode seguir suas [habilidades](skills.md) ativadas, escolhidas de acordo com o que a rotina faz. Somente as habilidades relevantes são lidas por inteiro. O resultado as lista em **Usou:**. Uma habilidade nunca faz uma rotina enviar ou alterar nada.

Suas rotinas aparecem em **Suas rotinas**, abaixo das sugestões, se houver. Um resultado longo é recolhido e mostrado como uma prévia curta. Toque em **Mostrar mais** ou no próprio resultado para abri-lo.

Cada execução conhece o resultado anterior, então pode explicar o que mudou desde então.

Depois de uma execução bem-sucedida, sua Machine pode criar uma receita para ler informações da mesma forma em todas as vezes, como quais e-mails ou alterações no GitHub verificar. Nas próximas execuções, ela lê esses dados primeiro, usando código simples. Assim, a IA só escolhe o que importa e escreve o resultado, usando menos tokens. Uma receita só lê. Se parar de funcionar, a rotina lê por conta própria e corrige o problema. A receita aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias sem execução

Se sua Machine estiver desligada ou ocupada, uma execução perdida não fica acumulada. Só a mais recente é executada, uma vez. Cada data é processada uma vez, mesmo depois de reiniciar.

As rotinas são executadas uma de cada vez e aguardam quando o uso do plano da sua IA está baixo, como todo trabalho em segundo plano. **Rodar agora** executa a rotina na hora. O resultado aparece no cartão quando estiver pronto.

## Mudar ou parar uma rotina

Essas opções ficam no menu ⋯ da rotina. **Editar** muda o nome e o que ela faz. A frequência e os resultados anteriores permanecem. **Mudar quando** define uma nova frequência com suas próprias palavras, como "todos os dias úteis às 8h". As duas opções têm **Salvar** e **Cancelar**. No computador, você também pode cancelar com Esc ou clicando fora da janela.

Em **Editar**, **Testar** executa uma vez a rotina com as novas palavras e mostra o resultado ali. A rotina continua igual até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar** no cartão da rotina. Rotinas pausadas ficam em **Pausado**, abaixo das suas rotinas. As execuções que deveriam acontecer durante a pausa não serão feitas depois. **Parar** encerra a rotina de vez.

Você pode ter até 20 rotinas, incluindo as pausadas. Pare uma rotina para adicionar outra.

Quando você usa **Pedir mudanças** na tarefa de uma rotina ou escreve no chat dela, e sua observação vale para todas as execuções, como "nunca use emojis", a tarefa oferece a opção **Mudar também a rotina**. Ela aparece na tarefa e no chat, abaixo da resposta. A rotina mostra as mudanças nas palavras e só é alterada quando você toca em **Mudar**. **Deixar como está** mantém tudo igual. Se a correção valer somente para aquele rascunho, essa opção não será oferecida.

## Avançado: etapas de script

Não é preciso usar scripts. Diga com suas próprias palavras o que a rotina deve fazer e sua Machine cuida do resto.

Para quem tem mais experiência, uma rotina também pode executar comandos próprios na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** só mostra os comandos depois que a rotina tiver algum. **Buscar dados** executa primeiro um comando na pasta dele, ou na sua pasta pessoal se nenhuma pasta for definida, por no máximo o número de segundos indicado. O que o comando mostrar é enviado à rotina para ser processado. Se você não inserir palavras, o que o comando mostrar será o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se terminar com um erro, a execução mostra **Não funcionou** e a mensagem da verificação. Se um comando de Buscar dados falhar, a mensagem será mostrada da mesma forma.

Cada comando deve ocupar uma linha e é executado sem shell: não use pipes nem variáveis. As etapas de script são suas e ficam definidas somente no seu painel. Uma execução de teste e **Testar** também executam Buscar dados e informam isso. Mesmo assim, não enviam nem mantêm nada. Uma rotina nunca envia nada, então as etapas de script devem servir somente para ler.

## Dos seus jobs do OpenClaw

Se você criou jobs programados no OpenClaw, sua Machine os lê, mas nunca os altera, e oferece como rotinas, em **Sugerido**, aqueles que se encaixam. Cada um já foi executado uma vez, então você vê um resultado real.

A rotina mantém as correções que você fez no job e exclui o que ele enviou ou publicou. Se um job executou um script ou leu dados coletados por um job de script, a rotina inclui isso como Buscar dados. **Adicionar** transforma o job em uma rotina. **Não, obrigado** faz com que ela não pergunte de novo sobre esse job. Se o job lembrava você de fazer algo, ele aparece como uma oferta de tarefa recorrente em Tarefas.

Antes de adicionar uma sugestão, use **Editar** e **Mudar quando**, no menu ⋯, para alterá-la como qualquer rotina. **Rodar de novo** executa a rotina com as palavras atuais para mostrar resultados mais recentes, por exemplo, depois de um fim de semana tranquilo. Ela só lê, é executada uma vez por toque e substitui o resultado anterior pelo novo.

A rotina pode ter no máximo três sugestões em espera por vez. Depois de uma semana de execuções bem-sucedidas, ela pergunta **Desativar o antigo job do OpenClaw?**. O job só é desativado quando você toca em **Desativar**. Você pode ativá-lo de novo no OpenClaw. **Manter** deixa os dois em execução.

## Com base no que você faz

Sua Machine também percebe trabalhos que você faz com frequência e os oferece como rotinas em **Sugerido**, mesmo sem OpenClaw. Ela procura:

- o mesmo pedido feito três vezes seguidas ou mais, como "resuma os chamados de suporte em aberto" toda segunda-feira;
- um e-mail que você envia regularmente, como um relatório semanal para sua equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como e-mails da escola e do clube que você encaminha para seu parceiro ou sua parceira. Um resumo semanal para essa pessoa evita que você tenha que encaminhá-los;
- o mesmo pedido que você responde regularmente, como uma aprovação mensal para a mesma pessoa.

Cada sugestão explica o que a rotina percebeu, como "Pedido feito 4 vezes seguidas" ou "6 e-mails encaminhados para Sam em 3 semanas", e já foi executada uma vez para você ver um resultado real. Pense em um resumo da equipe, uma preparação para uma reunião semanal, um resumo de suporte ou desenvolvimento, uma visão geral dos seus números ou um resumo das newsletters que você recebe.

A rotina só sugere o que é específico para você e claramente útil: um resumo de notícias feito somente com as suas newsletters, nunca um resumo genérico. Se nada se encaixar, nenhuma sugestão será feita.

A rotina verifica isso no máximo uma vez por dia e traz no máximo uma nova sugestão por semana, sem enviar notificações. Se você tocar em **Não, obrigado**, a sugestão não voltará. E-mails encaminhados e respostas continuam na conta de onde foram enviados, então Trabalho e Pessoal não se misturam. Tudo permanece na sua Machine. Uma tarefa que você conclui regularmente é oferecida como tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma [tarefa recorrente](recurring.md) lembra você de fazer algo. Uma rotina é um trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para "pagar o aluguel no dia primeiro" e uma rotina para "toda sexta-feira, me diga quais oportunidades ficaram paradas".
