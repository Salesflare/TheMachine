---
title: Rotinas
area: cards
summary: Trabalho que sua Machine faz sozinha, em um ritmo definido, como um resumo das suas negociações em aberto às segundas-feiras. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 3b0405616881de74
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga em uma linha o que ela deve fazer e quando: «toda segunda-feira às 9h, resuma minhas negociações em aberto» ou «todas as manhãs dos dias úteis, liste os e-mails que ainda preciso responder». Depois, toque em **Adicionar**.

Se você não definir um horário, ela será executada às 8h. O horário segue o relógio da sua Machine. Na primeira execução, ela recebe um nome curto.

Ao tocar em **Adicionar**, primeiro é feita uma execução de teste para você ver o resultado antes de manter a rotina. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina no ritmo definido, **Mudar** testa outras palavras ou um novo nome, e **Cancelar** descarta a rotina.

## Modelos

Em **Modelos**, no fim de Rotinas, toque em **Adicionar** para ativar uma rotina pronta. Ela é executada uma vez na hora e, depois, todas as manhãs às 7h30 (Limpeza de spam, a cada hora; Achados de usados, a cada 3 horas; Assinaturas e testes, uma vez por mês). O cartão mostra as instruções da rotina, como em qualquer outra, e **Editar** permite mudar as instruções ou o nome.

Quando você recebe muitas newsletters e a Limpeza de newsletters está desativada (25 ou mais em uma semana, de pelo menos 5 remetentes), uma linha acima das tarefas informa quantas chegaram e o que a rotina faria, com as opções **Ativar** e **Não, obrigado**.

A Limpeza de spam é oferecida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para spam em uma semana. **Ativar** adiciona a rotina, assim como **Adicionar** faz aqui. **Não, obrigado** significa que ela não será oferecida de novo. Um modelo que você já recusou também não será oferecido novamente.

A **Limpeza de newsletters** cria uma tarefa para cada área (trabalho e pessoal) com as newsletters do último dia. Cada uma tem as opções **Manter** e **Cancelar inscrição**. Para cancelar a inscrição, é usado o link de cancelamento com um clique da lista ou, se o envio estiver ativado, o e-mail de cancelamento enviado do seu endereço. Caso contrário, a The Machine cancela sua inscrição na página da lista, usando o próprio navegador. Se a página exigir login, captcha ou escolhas, isso fica por sua conta: a tarefa explica o motivo e mostra **Abrir página de cancelamento**.

Se você só quer evitar tarefas de uma lista, mas continuar recebendo os e-mails, diga «Nenhuma mensagem desta lista precisa virar tarefa» no chat de uma delas.

Recibos, pedidos e avisos de pagamento ficam de fora. E-mails recebidos por um endereço de grupo, como um Google Group, aparecem com o nome de quem escreveu e nunca cancelam sua inscrição no grupo. Se o remetente não tiver uma opção própria para cancelar a inscrição, a tarefa mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa para cada área com e-mails de remetentes desconhecidos que parecem spam. Cada e-mail tem as opções **Spam** e **Não é spam**. O Outlook move o spam para a pasta Lixo eletrônico, e o Gmail marca como spam. A rotina verifica os e-mails a cada hora, então o spam geralmente já está lá quando você chega. Enquanto a tarefa estiver aberta, novos e-mails de spam são adicionados a ela.

Uma conta do Gmail conectada somente para leitura, como em uma Machine hospedada, não pode mover e-mails para spam. Nesse caso, **Spam** mostra um link para marcar o e-mail como spam no Gmail, e a The Machine memoriza o remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Remetentes desconhecidos são aqueles para quem você nunca escreveu. Um «Re:» só conta como conversa em uma troca de mensagens na qual você escreveu. Se voltar a chegar um e-mail de alguém que você marcou como spam, na tarefa ou na sua caixa de entrada, ele aparece na próxima tarefa como **Já marcado como spam**. Os e-mails que você mesmo moveu para spam também ajudam a rotina a identificar mensagens parecidas.

Nada muda até você confirmar na tarefa. Toque no remetente para ler o e-mail primeiro: ele continua não lido e nada muda. Na Limpeza de spam, as imagens da internet não carregam, então o remetente não consegue saber que você abriu o e-mail. Os remetentes sobre os quais você já decidiu não são perguntados de novo. Se não houver newsletters ou spam em um dia, nenhuma tarefa será criada. Essas tarefas nunca enviam notificações.

Depois que você decidir sobre todos os remetentes, a tarefa indica que foi concluída e mostra **Marcar como concluída**.

O **Resumo diário** seleciona, uma vez por dia e em uma única tarefa, algumas newsletters que valem a pena. Cada uma explica em uma linha por que é importante para você. Toque para ler o e-mail ou use **Abrir no seu e-mail**. Só entram newsletters, nunca e-mails de pessoas, recibos ou remetentes dos quais você cancelou a inscrição, nem e-mails que você já leu. Se nada se destacar, nenhuma tarefa será criada.

A rotina aprende o que interessa para você com base no que abre, marca com estrela ou arquiva sem ler, além das opções **Mais assim** e **Menos assim** em cada seleção. Os temas escolhidos aparecem no cartão da rotina, em **Mais de** e **Menos de**. Remova um tema com × ou adicione o seu. Os temas tracejados foram identificados pela rotina. Um novo resumo substitui o que estiver aberto e nunca envia uma notificação.

A rotina lê somente o remetente, o assunto e o começo de cada newsletter nova, e faz uma pergunta curta à sua IA sobre elas, com um limite diário para reduzir os custos. **Mudar quando** define o horário. Depois que você mudar as instruções, a rotina será executada como qualquer outra, seguindo as instruções que você definiu.

**Aniversários** cria uma tarefa para cada pessoa próxima cujo aniversário seja hoje: pessoas para quem você mesmo escreve, como amigos, familiares e contatos frequentes. Cada pessoa vem com uma saudação curta, escrita no idioma dela e preparada no lugar em que você costuma conversar, como o chat do WhatsApp ou uma conversa por e-mail. A mensagem só é enviada quando você envia. Se não houver aniversários no dia, nenhuma tarefa será criada.

Os aniversários vêm dos seus calendários (eventos de aniversário e o calendário Birthdays do Google, lidos todas as manhãs mesmo quando não estão sincronizados, e o calendário Birthdays do Outlook), dos seus contatos do Google em uma Machine auto-hospedada e de um campo de data chamado Birthday para uma pessoa no Graph. Se ainda não houver nenhum aniversário nessas fontes, o resultado informa **Ainda não há informações de aniversário** e explica como adicionar.

**Importar aniversários do Facebook**: depois que Aniversários estiver ativado, uma tarefa oferece a opção de ler a página de aniversários do Facebook. Toque em **Importar** e a The Machine abre a página no próprio navegador, rola até carregar todos os meses e lê o nome e a data de aniversário de cada amigo. Ela mostra quantos aniversários encontrou e quem corresponde a pessoas no seu Graph, com base no nome e sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela será ignorada e listada.

Só **Salvar** adiciona as informações, na página de cada pessoa: a data de aniversário e a foto de perfil do Facebook, caso ela ainda não tenha uma foto. A data de aniversário ou a foto que você adicionar ali será mantida, e uma foto que a pessoa já tenha nunca será substituída. Nada é escrito no Facebook.

A rotina não lê os dados novamente por conta própria. Para isso, toque em **Importar de novo** na tarefa. O navegador precisa estar conectado ao Facebook. Se não estiver, toque em **Entrar no Facebook** na tarefa e faça login ali. Depois que você entrar, a rotina lê a página automaticamente. A The Machine nunca faz login por você.

Os amigos que não estão no seu Graph são contados, e alguns nomes são mostrados. **Adicionar … como contatos pessoais** adiciona todos de uma vez, inclusive depois de tocar em Salvar: cada pessoa fica com o nome e a data de aniversário, e nunca é compartilhada com um Fleet de Trabalho. Uma pessoa cujo nome já esteja no seu Graph, ou que você tenha excluído permanentemente, é ignorada. Os lembretes de aniversário continuam sendo enviados somente para pessoas com quem você conversa.

**Desfazer** na tarefa remove exatamente essas pessoas, inclusive depois de **Importar de novo**.

**Assinaturas e testes** lê seus recibos, faturas e avisos de renovação uma vez por mês e reúne suas assinaturas em uma tarefa: o custo de cada uma, a próxima data de cobrança e um aviso quando um período de teste termina ou o preço aumenta. Só são listadas as assinaturas sobre as quais a rotina tem certeza. Se nada for encontrado, nenhuma tarefa será criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. Uma assinatura mantida não será perguntada de novo, a menos que o preço mude. **Cancelar** mostra a página de cancelamento ou um rascunho pedindo o cancelamento. A mensagem só é enviada quando você envia. Entre uma execução e outra, a rotina verifica as assinaturas todos os dias e cria uma tarefa quando um período de teste ou uma renovação estiver a até 7 dias de ser cobrado.

**Manter contato** lembra você de vez em quando de falar com alguém próximo, mas só quando houver um motivo real. No cartão da rotina, escolha quem incluir em uma lista curta de pessoas com quem você mesmo conversa há alguns meses, nos dois sentidos. Remova alguém com ×.

Você só recebe um lembrete quando faz muito mais tempo do que o habitual desde a última conversa e há algo específico para dizer: uma novidade que a pessoa compartilhou, uma promessa ainda pendente ou uma mensagem que você nunca respondeu. A rotina cria uma tarefa com o motivo e uma mensagem curta no idioma da pessoa, preparada no lugar em que você costuma conversar. A mensagem só é enviada quando você envia. Se não houver nada a dizer, nenhuma tarefa será criada.

A rotina envia no máximo dois lembretes por semana e um por pessoa por mês. Ela não envia lembretes para alguém com quem você conversou recentemente. **Não precisa** em um lembrete faz a rotina esperar mais tempo antes de lembrar você daquela pessoa, e cada vez ela espera ainda mais. A rotina nunca envia notificações e permanece pessoal: nunca é compartilhada com um Fleet de Trabalho.

**Achados de usados** acompanha uma busca em um site de produtos usados, como Marktplaats, Vinted, eBay ou Facebook Marketplace. Faça a busca no site com os filtros desejados, copie o endereço dos resultados e cole-o depois de tocar em **Adicionar**. Se quiser, escreva filtros com suas próprias palavras, como «menos de 300, até 30 km, sem “para peças”». Cada busca é uma rotina independente, então adicione outra para fazer uma nova busca.

A cada 3 horas, a rotina abre a busca no próprio navegador da The Machine e procura anúncios que ainda não viu. Primeiro, verifica o preço, a distância e as palavras que você excluiu, usando código simples.

Cada anúncio novo que passar por esses filtros é aberto. Sua IA avalia o estado do produto com base na foto e na descrição, e o vendedor com base nas avaliações, na classificação e no tempo de existência da conta. Os anúncios promissores aparecem em uma única tarefa, cada um com foto, título, preço e uma avaliação em uma linha. Toque em um anúncio para abri-lo no navegador da The Machine.

Enquanto a tarefa estiver aberta, novos anúncios são adicionados no início, o número de anúncios aumenta e você recebe outra notificação, porque boas ofertas não duram muito. Marque a tarefa como concluída e o próximo achado começa uma nova tarefa. Se uma execução não encontrar nada bom, nada muda.

A rotina é cuidadosa e econômica: uma leitura da busca por execução, no máximo 6 anúncios abertos por execução, com uma pausa entre eles, e no máximo 40 anúncios verificados por dia em todas as suas buscas. Cada verificação é uma pergunta curta à sua IA, com uma foto. Na primeira execução, a rotina verifica os anúncios mais recentes e considera os demais como vistos, para que as execuções seguintes mostrem somente novidades.

Se o site pedir que você faça login, mostrar uma verificação de robô ou impedir a leitura, uma tarefa avisará, com a opção **Abrir** para ver a página no navegador da The Machine. Faça login ou conclua a verificação por conta própria. Na próxima execução, a rotina tentará ler a página de novo. A The Machine nunca faz login nem resolve uma verificação por você, e nunca entra em contato com vendedores, faz lances ou compra.

**Alterar busca** no cartão da rotina permite usar outro endereço ou mudar os filtros. **Mudar quando** permite escolher outro ritmo, como «a cada 6 horas».

**Recompras** lê as confirmações de pedidos de lojas on-line na sua caixa de e-mail e identifica o que você compra com frequência, como café, ração ou vitaminas. Quando estiver na hora provável de comprar algo de novo, ela cria uma tarefa com o produto, a loja, o último preço e a data da última compra. **Abrir na loja** leva você à página do produto para comprar por conta própria. Nada é comprado por você.

A rotina precisa identificar pelo menos três pedidos do mesmo produto em intervalos regulares. Por isso, uma compra única ou um intervalo fora do comum não cria uma tarefa. Por enquanto, ela lê lojas que usam o Shopify. Sua IA lê somente novos e-mails de pedidos dessas lojas, com uma pergunta curta por execução. Essas tarefas nunca enviam notificações. Fazer um novo pedido do produto fecha a tarefa que estiver aberta.

Enquanto a rotina de um modelo mantiver as instruções do modelo, ela será executada com o próprio código, sem usar seu plano de IA. A Limpeza de spam, por exemplo, primeiro lista por código os novos e-mails de remetentes desconhecidos e só faz uma pergunta curta à sua IA se encontrar algum. Manter contato só pergunta sobre uma ou duas pessoas selecionadas. Quando você mudar as instruções, a rotina será executada como qualquer outra, seguindo as instruções que você definiu.

A Limpeza de newsletters e a Limpeza de spam continuam criando uma tarefa com uma opção para cada e-mail. Uma rotina Aniversários editada mostra o resultado e no máximo um rascunho, em vez de criar uma tarefa por pessoa. **Voltar ao modelo**, em **Editar**, restaura as instruções do modelo.

## O que uma rotina faz

No horário definido, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e mostra o resultado na página Rotinas. Cada resultado indica **Para revisar**, **Nada de novo** (com o motivo) ou **Não funcionou** (com o motivo). Uma execução que termina sem resultado conta como uma execução que não funcionou, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da web, GitHub e sites como X no navegador. Elas não enviam mensagens, respondem, publicam nem alteram nada. Elas abrem páginas encontradas no que leram ou em uma busca, endereços de páginas simples e sites conhecidos, nunca um endereço inventado para carregar o que leram. Só um modelo pode alterar e-mails, e apenas o que você confirmar na tarefa correspondente.

Quando o trabalho de uma rotina termina com uma publicação ou mensagem, ela executa todas as etapas até esse ponto e mostra o rascunho, por exemplo, **Publicaria no X:**. Depois de uma execução real, o rascunho vira uma tarefa para você aprovar. Uma execução de teste só mostra o rascunho.

O nome da rotina indica o assunto e onde o resultado será publicado. A opção **Da sua rotina**, logo abaixo, abre a rotina. O botão indica a etapa, como **Preparar publicação**: ele prepara o conteúdo, mas não publica nada. Você publica pelo resultado. Se a The Machine não puder publicar por você, o botão abre a página em que você pode fazer isso.

A tarefa começa na área da conta de onde será enviada, como Trabalho para a conta X da sua empresa, então você nunca precisa pedir para movê-la.

Uma execução pode seguir suas [habilidades](skills.md) ativadas, escolhidas de acordo com o que a rotina faz. Só as que se aplicam são lidas por completo. O resultado lista as habilidades em **Usadas:**. Uma habilidade nunca faz uma rotina enviar ou alterar nada.

Suas rotinas aparecem em **Suas rotinas**, abaixo de qualquer sugestão. Um resultado longo é recolhido e mostra uma prévia curta. Toque em **Mostrar mais** ou no próprio resultado para abri-lo.

Cada execução conhece o resultado anterior e pode indicar o que mudou desde então.

Depois de uma execução bem-sucedida, sua Machine pode criar por conta própria uma receita para as partes da leitura que se repetem, como quais e-mails ou alterações no GitHub devem ser verificadas. Nas próximas execuções, essas partes são lidas primeiro, usando código simples. A IA seleciona e redige somente o que importa, com menos tokens. Uma receita só lê. Se parar de funcionar, a rotina lê por conta própria e corrige a receita. Ela aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias sem execução

Se sua Machine estiver desligada ou ocupada, as execuções perdidas não se acumulam. Só a mais recente é executada, uma vez. Cada data é processada uma única vez, mesmo depois de uma reinicialização.

As rotinas são executadas uma de cada vez e aguardam quando há pouco uso disponível no seu plano de IA, como todo trabalho em segundo plano. **Rodar agora** executa a rotina imediatamente. O resultado aparece no cartão quando estiver pronto.

## Mudar ou parar uma rotina

As opções ficam no menu ⋯ da rotina. **Editar** muda o nome e o que a rotina faz. O horário e os resultados anteriores são mantidos. **Mudar quando** permite definir outro ritmo com suas próprias palavras, como «todos os dias úteis às 8h». As duas opções mostram **Salvar** e **Cancelar**. No computador, você também pode cancelar com Esc ou clicando fora.

Em **Editar**, **Testar** executa as novas instruções uma vez e mostra o resultado ali. A rotina continua como estava até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar** no cartão. As rotinas pausadas ficam em **Pausado**, abaixo das suas rotinas, e as execuções perdidas durante a pausa não são realizadas depois. **Parar** encerra a rotina definitivamente.

É possível ter até 20 rotinas, incluindo as pausadas. Pare uma para adicionar outra.

Quando você usa **Pedir mudanças** na tarefa de uma rotina ou escreve no chat dela, e o comentário vale para todas as execuções, como «nunca use emojis», a tarefa oferece **Mudar também a rotina**, na própria tarefa e no chat, abaixo da resposta. A opção mostra o que vai mudar nas instruções da rotina. A rotina só muda quando você toca em **Mudar**. **Deixar como está** mantém tudo igual. Se o ajuste valer só para aquele rascunho, a opção não aparece.

## Avançado: etapas de script

Não é preciso usar scripts: diga com suas próprias palavras o que a rotina deve fazer, e sua Machine cuida do resto.

Para usuários avançados, uma rotina também pode executar comandos próprios na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** só aparece quando a rotina já tem etapas. **Buscar dados** executa um comando primeiro, na pasta correspondente (sua pasta pessoal, se o campo estiver vazio), pelo número de segundos definido. O que o comando exibir fica disponível para a rotina usar. Se você não escrever instruções, o resultado será o que o comando exibir.

**Verificação** recebe o resultado como entrada depois da execução. Se o comando terminar com um erro, o resultado da rotina será **Não funcionou**, com a mensagem da verificação. Se um comando de Buscar dados falhar, o resultado será o mesmo.

Um comando deve ocupar uma linha e é executado sem um shell: não use pipes nem variáveis. As etapas de script são suas e só podem ser configuradas no seu painel. Uma execução de teste e **Testar** também executam Buscar dados e avisam você. Mesmo assim, elas não enviam nem guardam nada. Uma rotina nunca envia nada, então uma etapa de script deve apenas ler.

## Dos jobs do OpenClaw

Se você criou jobs programados no OpenClaw, sua Machine os lê, sem alterá-los, e oferece como rotinas, em **Sugerido**, os que se encaixam. Cada job foi executado uma vez, então você pode ver um resultado real.

A rotina mantém suas correções ao job e exclui o que ele enviou ou publicou. Se o job executou um script ou leu dados coletados por um job de script, o script é incluído como Buscar dados. **Adicionar** transforma o job em uma rotina. **Não, obrigado** faz com que o job não seja oferecido novamente. Um job que lembrava você de fazer algo aparece em Tarefas como uma sugestão de tarefa recorrente.

Antes de adicionar uma sugestão, use **Editar** e **Mudar quando**, no menu ⋯, para alterá-la como qualquer outra rotina. **Rodar de novo** executa a rotina agora, com as instruções atuais, para mostrar resultados mais recentes, por exemplo, depois de um fim de semana tranquilo. Ela só lê, é executada uma vez por toque e substitui o resultado anterior pelo novo.

No máximo três sugestões ficam disponíveis de cada vez. Depois de uma semana de execuções bem-sucedidas, a rotina pergunta **Desativar o antigo job do OpenClaw?**. O job só é desativado quando você toca em **Desativar**. Você pode reativá-lo no OpenClaw. **Manter** deixa os dois em execução.

## Com base no que você faz

Sua Machine também identifica tarefas que você faz com frequência e as oferece como rotinas em **Sugerido**, mesmo que você não use o OpenClaw. Ela procura:

- o mesmo pedido feito três vezes seguidas ou mais, como «resuma os chamados de suporte em aberto» toda segunda-feira;
- um e-mail que você envia com frequência, como um relatório semanal para a equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como mensagens da escola e do clube para sua pessoa parceira: um resumo semanal evita que você precise encaminhá-los;
- o mesmo pedido ao qual você responde com frequência, como uma aprovação mensal para a mesma pessoa.

Cada sugestão explica o que a rotina identificou, como «Pedido 4 vezes seguidas» ou «Encaminhou 6 e-mails para Sam em 3 semanas», e foi executada uma vez para mostrar um resultado real. Considere um resumo da equipe, um informe antes de uma reunião semanal, um resumo de suporte ou desenvolvimento, uma visão geral dos seus números ou um resumo das newsletters que você recebe.

A rotina só sugere o que é específico para você e claramente útil: um resumo de notícias feito somente com as suas próprias newsletters, nunca um resumo genérico. Se nada se encaixar, nenhuma sugestão será criada.

A rotina verifica essas atividades no máximo uma vez por dia e apresenta no máximo uma nova sugestão por semana, sem enviar notificações. **Não, obrigado** impede que aquela sugestão apareça de novo. Encaminhamentos e respostas continuam na conta de onde foram enviados, então Trabalho e Pessoal não se misturam. Tudo permanece na sua Machine. Uma tarefa que você conclui com frequência aparece como uma sugestão de tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma [tarefa recorrente](recurring.md) lembra você de fazer algo. Uma rotina é um trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para «pagar o aluguel no dia 1» e uma rotina para «toda sexta-feira, me diga quais negociações ficaram paradas».
