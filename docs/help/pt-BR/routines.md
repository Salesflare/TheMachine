---
title: Rotinas
area: cards
summary: Tarefas que sua Machine faz sozinha, em uma frequência definida, como um resumo das oportunidades em aberto toda segunda-feira. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 6d74cb93df1bf494
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga em uma linha o que ela deve fazer e quando: "toda segunda-feira às 9h, faça um resumo das minhas oportunidades em aberto" ou "todas as manhãs dos dias úteis, liste os e-mails que ainda preciso responder". Depois, toque em **Adicionar**.

Se você não definir um horário, a rotina será executada às 8h, no horário da sua Machine. A primeira execução dá um nome curto para ela.

Ao tocar em **Adicionar**, a rotina é executada para teste primeiro, para você ver o resultado antes de mantê-la. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina nessa frequência, **Mudar** tenta outras palavras ou um nome novo, e **Cancelar** descarta tudo.

## Modelos

Em **Modelos**, no fim de Rotinas, toque em **Adicionar** para ativar uma rotina pronta. Ela é executada uma vez na hora e, depois, todas as manhãs às 7h30 (Limpeza de spam a cada hora, Achados de usados a cada 3 horas, Assinaturas e testes uma vez por mês). O cartão mostra as instruções dela, como em qualquer rotina, e **Editar** permite mudar as instruções ou o nome.

Quando você recebe muitas newsletters e a Limpeza de newsletters está desativada (25 ou mais em uma semana, de pelo menos 5 remetentes), aparece uma linha acima das tarefas com a quantidade recebida e o que a rotina faria, além das opções **Ativar** e **Não, obrigado**.

A Limpeza de spam é oferecida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para o spam em uma semana. **Ativar** adiciona a rotina, como **Adicionar** faz aqui. Se você tocar em **Não, obrigado**, ela não será oferecida de novo. O mesmo vale para um modelo que você já usou.

A **Limpeza de newsletters** cria uma tarefa por área (trabalho e pessoal) com as newsletters do dia anterior. Cada uma tem as opções **Manter** ou **Cancelar inscrição**. A opção Cancelar inscrição usa o link de cancelamento com um clique da lista ou envia um e-mail de cancelamento pelo seu endereço, se o envio estiver ativado. Caso contrário, The Machine cancela a inscrição na página da lista, pelo próprio navegador. Se for preciso fazer login, passar por um captcha ou escolher opções, você cuida disso: a linha explica o motivo e mostra **Abrir página de cancelamento**.

Quer apenas impedir que uma lista gere tarefas, sem deixar de receber os e-mails? Escreva "Esta lista não precisa gerar tarefas" no chat de uma das mensagens.

Recibos, pedidos e avisos de pagamento ficam de fora. Os e-mails recebidos por um endereço de grupo, como um Google Group, aparecem com o nome de quem os enviou, e você nunca terá a inscrição no grupo cancelada. Se o remetente não tiver um processo próprio de cancelamento, a linha mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa por área com e-mails de remetentes desconhecidos que parecem spam. Cada um tem as opções **Spam** ou **Não é spam**. O Outlook move o spam para a pasta Lixo Eletrônico, e o Gmail marca como spam. A rotina verifica os e-mails a cada hora, então o spam costuma aparecer antes de você chegar até ele. Novos e-mails de spam são adicionados à mesma tarefa enquanto ela estiver aberta.

Uma conta do Gmail conectada só para leitura, como em uma Machine hospedada, não pode mover e-mails para o spam. Nesse caso, **Spam** mostra um link para marcar a mensagem como spam no Gmail, e The Machine memoriza o remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Remetentes desconhecidos são aqueles para quem você nunca escreveu. Um "Re:" só conta como conversa em uma troca de mensagens na qual você escreveu. Se você voltar a receber e-mails de um remetente que marcou como spam, na tarefa ou na sua caixa de entrada, eles aparecem na próxima tarefa com o rótulo **Já marcado como spam**. O que você mesmo moveu para o spam também ajuda a rotina a identificar e-mails parecidos.

Nada muda até você confirmar na tarefa. Toque no remetente para ler o e-mail primeiro: ele continua não lido e nada muda. Na Limpeza de spam, as imagens da internet não são carregadas, então o remetente não consegue ver que você abriu o e-mail. A rotina não volta a perguntar sobre os remetentes que você já avaliou. Se não houver newsletters ou spam em um dia, nenhuma tarefa será criada. Essas tarefas nunca enviam notificações.

Depois que você avaliar todos os remetentes, a tarefa informa que foi concluída e mostra **Marcar como feito**.

O **Resumo diário** seleciona, uma vez por dia, as poucas matérias de newsletters que valem seu tempo e as reúne em uma tarefa. Cada uma explica em uma linha por que é relevante para você. Toque nela para ler o e-mail ou use **Abrir no seu e-mail**. A seleção inclui apenas newsletters, nunca e-mails de pessoas, recibos ou remetentes de cuja lista você cancelou a inscrição. Ela também não inclui e-mails que você já leu. Se nada se destacar, nenhuma tarefa será criada.

A rotina aprende o que interessa para você com base no que abre, marca com estrela ou arquiva sem ler, e nas opções **Mais assim** e **Menos assim** de cada sugestão. Os temas que ela seleciona aparecem no cartão da rotina, em **Mais de** e **Menos de**. Toque em × para remover um tema ou adicione os seus. Os temas com linha tracejada foram identificados pela rotina. Um novo resumo substitui o que estiver aberto, e ele nunca envia notificações.

A rotina lê apenas o remetente, o assunto e o início de cada newsletter nova. Depois, faz uma pergunta curta sobre elas à sua IA, com um limite diário para manter o custo baixo. **Mudar quando** define o horário. Depois que você muda as instruções, a rotina passa a funcionar como qualquer outra, com base nelas.

**Aniversários** cria uma tarefa para cada pessoa próxima cujo aniversário é hoje: pessoas para quem você mesmo escreve, como amigos, familiares e contatos frequentes. Para cada pessoa, a tarefa inclui uma sugestão curta de mensagem no lugar onde você costuma conversar com ela, como o chat do WhatsApp ou uma conversa por e-mail, no idioma dela. A mensagem só é enviada quando você envia. Se ninguém fizer aniversário naquele dia, nenhuma tarefa será criada.

Os aniversários vêm dos seus calendários (eventos de aniversário do Google e o calendário Aniversários, que são lidos todas as manhãs mesmo quando não estão sincronizados, e o calendário Aniversários do Outlook), dos seus contatos do Google em uma Machine auto-hospedada e de um campo de data chamado Birthday para uma pessoa no Graph. Se nenhum desses lugares tiver aniversários, o resultado mostra **Ainda não há informações de aniversário** e explica como adicionar algumas.

**Importar aniversários do Facebook**: depois que Aniversários estiver ativado, uma tarefa oferece a opção de ler a página de aniversários do Facebook. Toque em **Importar** e The Machine abre a página no próprio navegador, rola até carregar todos os meses e lê o nome e o aniversário de cada amigo. A rotina mostra quantos aniversários encontrou e quais pessoas correspondem a contatos do seu Graph pelo nome e sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela não será incluída e aparecerá na lista.

Só **Salvar** adiciona os dados à página de cada pessoa: o aniversário e a foto do perfil do Facebook, se ela ainda não tiver uma foto. O aniversário ou a foto que você adicionar ali permanece, e uma foto que a pessoa já tenha nunca é substituída. Nada é publicado no Facebook.

A rotina não lê os dados novamente por conta própria. Para isso, toque em **Importar de novo** na tarefa. É preciso estar conectado ao Facebook no navegador. Caso não esteja, toque em **Entrar no Facebook** na tarefa e faça login. Depois que você entrar, a rotina lê a página automaticamente. The Machine nunca faz login por você.

A rotina conta os amigos que não estão no seu Graph e mostra alguns nomes. **Adicionar … como contatos pessoais** adiciona todos de uma vez, inclusive depois de tocar em Salvar. Cada pessoa é adicionada com nome e aniversário, sem compartilhar os dados com um Fleet de Trabalho. Pessoas com nomes que já estão no seu Graph, ou que você excluiu permanentemente, não são incluídas. Os lembretes de aniversário continuam sendo enviados apenas para pessoas com quem você conversa.

**Desfazer** na tarefa remove exatamente essas pessoas, mesmo depois de tocar em **Importar de novo**.

**Assinaturas e testes** lê recibos, faturas e avisos de renovação uma vez por mês e reúne suas assinaturas em uma tarefa. Para cada uma, mostra o custo, a próxima cobrança e um aviso se um período de teste estiver acabando ou se o preço aumentar. A rotina só lista assinaturas que conseguiu identificar com certeza. Se não encontrar nenhuma, nenhuma tarefa será criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. A rotina não volta a perguntar sobre uma assinatura que você decidiu manter, a menos que o preço mude. **Cancelar** mostra a página de cancelamento ou um rascunho pedindo o cancelamento. A mensagem só é enviada quando você envia. Entre uma execução e outra, a rotina verifica as assinaturas todos os dias e cria uma tarefa quando uma cobrança de teste ou renovação estiver prevista para os próximos 7 dias.

**Manter contato** lembra você de vez em quando de falar com alguém próximo, mas só quando há um motivo concreto. No cartão da rotina, escolha quem incluir em uma lista curta de pessoas com quem você conversa diretamente, nos dois sentidos, ao longo dos meses. Toque em × para remover alguém.

Você só recebe um lembrete quando faz muito mais tempo do que o normal que vocês não conversam e há algo específico para dizer: uma novidade que a pessoa compartilhou, inclusive no resumo da página dela, uma promessa ainda pendente ou uma mensagem que você nunca respondeu.

Se uma novidade tiver uma data futura, como uma mudança no mês que vem, a rotina volta a verificá-la logo depois dessa data, junto com as mensagens mais recentes. Ela cria uma única tarefa com o motivo e uma sugestão curta de mensagem no lugar onde você costuma conversar com a pessoa, no idioma dela. A mensagem só é enviada quando você envia. Se não houver nada a dizer, nenhuma tarefa será criada.

A rotina envia no máximo dois lembretes por semana e um por pessoa por mês. Ela não envia lembretes para alguém com quem você conversou recentemente. Se você tocar em **Não precisa** em um lembrete, a rotina espera mais tempo antes de voltar a lembrar você sobre essa pessoa. O intervalo aumenta a cada vez.

A rotina nunca envia notificações e permanece pessoal: nunca é compartilhada com um Fleet de Trabalho, nunca usa informações de trabalho como base (o que chegou às suas contas de trabalho, ou uma promessa ou informação sobre o trabalho) e, quando possível, cria o rascunho em uma conversa fora do trabalho.

**Achados de usados** acompanha buscas em sites de produtos usados, como Marktplaats, Vinted, eBay ou Facebook Marketplace. Faça uma busca com os filtros que quiser, copie o endereço dos resultados e cole-o depois de tocar em **Adicionar**. Se quiser, acrescente filtros com suas próprias palavras, como “abaixo de 300, em um raio de 30 km, sem anúncios de ‘peças’”. Cada busca é uma rotina separada, então adicione outra para fazer uma nova busca.

A cada 3 horas, a rotina abre a busca no próprio navegador da The Machine e procura anúncios que ainda não viu. Primeiro, ela verifica o preço, a distância e as palavras que você excluiu, usando código simples.

Cada novo anúncio que passar por esses filtros é aberto. Sua IA avalia o estado do produto com base na foto e na descrição, e o vendedor com base nas avaliações, na classificação e no tempo de existência da conta. Os bons anúncios são reunidos em uma tarefa, cada um com foto, título, preço e uma avaliação em uma linha. Toque em um deles para abrir o anúncio no navegador da The Machine.

Enquanto a tarefa estiver aberta, novos achados são adicionados no início da lista, o contador aumenta e você recebe outra notificação, porque boas ofertas desaparecem rápido. Marque a tarefa como feita e o próximo achado começa uma nova tarefa. Uma execução sem anúncios interessantes não muda nada.

A rotina é cuidadosa e econômica: lê a busca uma vez por execução, abre no máximo 6 anúncios por execução, com uma pausa entre eles, e verifica no máximo 40 anúncios por dia em todas as suas buscas. Cada avaliação é uma pergunta curta para sua IA com uma foto. Na primeira execução, a rotina verifica os anúncios mais recentes e considera os restantes como vistos, para que as próximas execuções mostrem apenas novidades.

Se o site pedir para você entrar, mostrar uma verificação para saber se você é um robô ou impedir a leitura, uma tarefa informa o que aconteceu e mostra **Abrir** para você ver a página no navegador da The Machine. Entre ou passe pela verificação por conta própria. A próxima execução tentará ler a página novamente. The Machine nunca faz login nem resolve verificações por você, e nunca entra em contato com vendedores, dá lances ou compra.

**Alterar busca** no cartão da rotina permite usar um novo endereço ou mudar os filtros. **Mudar quando** permite escolher outra frequência, como “a cada 6 horas”.

**Recompras** lê as confirmações de pedidos de lojas on-line no seu e-mail e identifica os produtos que você compra com frequência, como café, ração ou vitaminas. Quando um produto provavelmente estiver para acabar, a rotina cria uma tarefa com o item, a loja, o último preço e a data da última compra. **Abrir na loja** leva você à página do produto para comprá-lo. Nada é comprado por você.

A rotina precisa identificar pelo menos três pedidos do mesmo item em intervalos regulares. Uma compra isolada ou um intervalo fora do comum não gera uma tarefa. No momento, ela lê lojas que usam Shopify. Sua IA lê apenas os novos e-mails de pedidos dessas lojas, com uma pergunta curta por execução. Essas tarefas nunca enviam notificações, e uma nova compra do item fecha a tarefa aberta.

Enquanto a rotina de um modelo mantiver as instruções originais, ela será executada com código próprio, sem usar o plano da sua IA. Por exemplo, a Limpeza de spam lista primeiro, usando código, os novos e-mails de remetentes desconhecidos e só faz uma pergunta curta à sua IA se houver algum. Manter contato pergunta apenas sobre uma ou duas pessoas selecionadas. Dar um nome novo não muda isso. Depois que você mudar as instruções, a rotina passa a funcionar como qualquer outra, com base nelas.

A Limpeza de newsletters e a Limpeza de spam continuam gerando uma única tarefa com uma escolha para cada e-mail. Uma rotina Aniversários editada mostra o resultado e, no máximo, um rascunho, não uma tarefa por pessoa. **Voltar ao modelo**, em **Editar**, restaura as instruções originais.

## O que uma rotina faz

No horário definido, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e mostra o resultado na página Rotinas. Cada resultado mostra **Para revisar**, **Nada de novo** (com o motivo) ou **Não funcionou** (com o motivo). Uma execução que termina sem resultado conta como uma execução que não funcionou, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da web, GitHub e sites como X no navegador. Elas não enviam mensagens, respondem, publicam nem alteram nada. Elas abrem páginas encontradas no que leram ou em uma busca, endereços de páginas simples e sites conhecidos, nunca um endereço criado para levar o que foi lido. Só um modelo pode alterar e-mails, e apenas o que você confirmar na tarefa dele.

Se a tarefa de uma rotina terminar com uma publicação ou mensagem, ela faz tudo até essa etapa e mostra o rascunho, por exemplo, **Publicaria no X:**. Depois de uma execução real, o rascunho aparece como uma tarefa para você aprovar. Uma execução de teste apenas o mostra.

O nome da tarefa indica o assunto e onde ela será publicada. **Da sua rotina**, abaixo do nome, abre a rotina. O botão indica a etapa, como **Preparar publicação**: ele prepara o conteúdo, mas não publica nada. Você publica pelo resultado. Se The Machine não puder publicar por você, o botão abre a página onde você pode fazer isso.

A tarefa começa na área da conta de onde será enviada, como Trabalho para a conta da empresa no X, então você nunca precisa movê-la.

Uma execução pode seguir suas [habilidades](skills.md) ativadas, escolhidas de acordo com o que a rotina faz. Só as que forem relevantes são lidas por inteiro. O resultado mostra os nomes delas em **Usado:**. Uma habilidade nunca faz uma rotina enviar ou alterar nada.

Suas rotinas ficam em **Suas rotinas**, abaixo das sugestões. Se um resultado for longo, ele aparece em uma prévia curta. Toque em **Mostrar mais** ou no próprio resultado para abri-lo.

Cada execução conhece o resultado anterior e pode indicar o que mudou desde então.

Depois de uma execução bem-sucedida, sua Machine pode criar uma receita para as etapas de leitura que se repetem, como quais e-mails ou alterações do GitHub verificar. Nas próximas execuções, ela verifica primeiro esses dados com código simples. A IA seleciona apenas o que importa e escreve o resultado, usando menos tokens. Uma receita só lê. Se parar de funcionar, a rotina volta a ler por conta própria e a corrige. A receita aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias sem execução

Se sua Machine estiver desligada ou ocupada, as execuções perdidas não se acumulam. Só a mais recente é executada, uma vez. Cada data é executada uma única vez, mesmo depois de uma reinicialização.

As rotinas são executadas uma de cada vez e aguardam quando há pouco uso disponível no plano da sua IA, como todo trabalho em segundo plano. **Rodar agora** executa a rotina na hora. O resultado aparece no cartão quando estiver pronto.

## Alterar ou interromper uma rotina

Essas opções ficam no menu ⋯ da rotina. **Editar** muda o nome e o que ela faz. O horário e os resultados anteriores permanecem. **Mudar quando** permite definir outra frequência com suas próprias palavras, como "todos os dias úteis às 8h". Ambas as opções têm **Salvar** e **Cancelar**. No computador, Esc ou um clique fora da janela também cancela.

Em **Editar**, **Testar** executa uma vez com as novas instruções e mostra o resultado ali. A rotina continua como estava até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar** no cartão. As rotinas pausadas ficam em **Pausado**, abaixo das suas rotinas, e as execuções perdidas durante a pausa não acontecem depois. **Parar** encerra a rotina de vez.

Você pode ter até 20 rotinas, incluindo as pausadas. Pare uma para adicionar outra.

Se você usar **Pedir mudanças** em uma tarefa da rotina ou escrever no chat dela, e a observação valer para todas as execuções, como "nunca use emojis", a tarefa oferecerá **Mudar também a rotina**, tanto na própria tarefa quanto no chat, abaixo da resposta. A opção mostra o que mudaria nas instruções da rotina, que só são alteradas quando você toca em **Mudar**. **Deixar como está** mantém tudo igual. Se você pedir para corrigir apenas aquele rascunho, essa opção não aparece.

## Avançado: etapas de script

Não é preciso criar scripts. Diga com suas próprias palavras o que a rotina deve fazer, e sua Machine cuida do resto.

Para usuários avançados, uma rotina também pode executar seus próprios comandos na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** mostra as etapas apenas quando a rotina já tiver alguma. **Buscar dados** executa primeiro um comando, na pasta definida para ele (sua pasta pessoal, se o campo estiver vazio) e pelo tempo máximo indicado em segundos. O que o comando imprimir é enviado à rotina para ela usar. Se não houver instruções, o que ele imprimir será o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se o comando terminar com um erro, a execução mostra **Não funcionou** e a mensagem da verificação. Se um comando de Buscar dados falhar, a rotina mostra a mesma mensagem.

Cada comando deve ocupar uma linha e é executado sem shell: não use pipes nem variáveis. As etapas de script são suas e só podem ser configuradas no seu painel. Uma execução de teste e **Testar** também executam Buscar dados e avisam você. Elas continuam sem enviar nem manter nada. Como uma rotina nunca envia nada, as etapas de script devem apenas ler.

## Dos seus jobs do OpenClaw

Se você já tinha criado jobs programados no OpenClaw, sua Machine os lê (nunca os altera) e sugere como rotinas os que forem adequados, em **Sugerido**. Cada um é executado uma vez, para você ver um resultado real.

A rotina mantém as correções que você fez no job e remove o que ele enviou ou publicou. Se um job executava um script ou lia dados coletados por um job de script, a rotina inclui essa etapa em Buscar dados. **Adicionar** transforma o job em uma rotina. **Não, obrigado** impede que a rotina pergunte novamente sobre esse job. Se um job lembrava você de fazer algo, ele aparece como uma sugestão de tarefa recorrente em Tarefas.

Antes de adicionar uma sugestão, use **Editar** e **Mudar quando** no menu ⋯ para alterá-la como qualquer rotina. **Rodar de novo** executa a rotina agora com as instruções atuais, para mostrar resultados mais recentes, como depois de um fim de semana tranquilo. Ela só lê, é executada uma vez por toque e o novo resultado substitui o anterior.

No máximo três sugestões ficam disponíveis ao mesmo tempo. Depois de uma semana de execuções bem-sucedidas, a rotina pergunta **Desativar o antigo job do OpenClaw?**. O job só é desativado quando você toca em **Desativar**. Você pode ativá-lo novamente no OpenClaw. **Manter** deixa os dois em execução.

## Com base no que você faz

Sua Machine também identifica tarefas que você faz com frequência e sugere transformá-las em rotinas em **Sugerido**, mesmo que você não use OpenClaw. Ela procura:

- o mesmo pedido feito três ou mais vezes seguidas, como "faça um resumo dos chamados de suporte em aberto" toda segunda-feira;
- um e-mail que você envia com frequência, como um relatório semanal para sua equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como e-mails da escola e de clubes para sua parceira ou seu parceiro. Um resumo semanal evita que você precise encaminhá-los;
- o mesmo pedido ao qual você responde com frequência, como uma aprovação mensal para a mesma pessoa.

Cada sugestão diz o que a rotina identificou, como "Pedido 4 vezes seguidas" ou "6 e-mails encaminhados para Sam em 3 semanas", e é executada uma vez para você ver um resultado real. Pense em um resumo da equipe, um briefing antes de uma reunião semanal, um resumo de suporte ou desenvolvimento, um panorama dos seus números ou um resumo das newsletters que você recebe.

A rotina só sugere tarefas específicas para você e que sejam claramente úteis, como um resumo de notícias apenas das suas newsletters, nunca um resumo genérico. Se nada for adequado, nenhuma sugestão será feita.

A rotina faz essa análise no máximo uma vez por dia e mostra no máximo uma sugestão nova por semana, sem enviar notificações. **Não, obrigado** impede que a sugestão apareça de novo. Os encaminhamentos e as respostas continuam na conta de onde foram enviados, então Trabalho e Pessoal não se misturam. Tudo permanece na sua Machine. Uma tarefa que você conclui com frequência aparece como uma sugestão de tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma [tarefa recorrente](recurring.md) lembra você de fazer algo. Uma rotina é uma tarefa que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para "pagar o aluguel no dia primeiro" e uma rotina para "toda sexta-feira, me diga quais oportunidades esfriaram".
