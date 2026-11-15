---
title: Rotinas
area: cards
summary: Tarefas que sua Machine faz sozinha, em uma frequência definida, como um resumo das suas oportunidades em aberto toda segunda-feira. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours
translated: 3e6d9d8d446a5dde
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga em uma linha o que a rotina deve fazer e quando: "toda segunda-feira às 9h, faça um resumo das minhas oportunidades em aberto" ou "todas as manhãs dos dias úteis, liste os e-mails que ainda preciso responder". Depois, toque em **Adicionar**.

Se você não definir um horário, ela será executada às 8h. O horário segue o relógio da sua Machine. A primeira execução dá um nome curto à rotina.

**Adicionar** começa com uma execução de teste para você ver o resultado antes de manter a rotina. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina na frequência definida, **Mudar** testa outras palavras ou um novo nome e **Cancelar** descarta a rotina.

## Modelos

Em **Modelos**, no fim de Rotinas, **Adicionar** ativa uma rotina pronta. Ela é executada uma vez imediatamente e, depois, todas as manhãs às 7h30 (Limpeza de spam a cada hora, Achados de usados a cada 3 horas, Assinaturas e testes uma vez por mês). O cartão mostra as palavras usadas, como em qualquer rotina, e **Editar** permite mudar essas palavras ou o nome.

Quando chegam muitas newsletters e a Limpeza de newsletters está desativada (25 ou mais em uma semana, de pelo menos 5 remetentes), uma mensagem acima das suas tarefas informa quantas chegaram e o que a rotina faria, com as opções **Ativar** e **Não, obrigado**.

A Limpeza de spam é oferecida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para o spam em uma semana. **Ativar** adiciona a rotina, como **Adicionar** faz aqui. Se você tocar em **Não, obrigado**, ela não será oferecida novamente. Um modelo que você já tinha também não será oferecido de novo.

A **Limpeza de newsletters** cria uma tarefa por área (trabalho e pessoal) com as newsletters do último dia. Cada uma tem as opções **Manter** ou **Cancelar inscrição**. Para cancelar a inscrição, a rotina usa o link de cancelamento com um clique da lista ou envia um e-mail de cancelamento do seu endereço, se o envio estiver ativado. Caso contrário, The Machine cancela a inscrição na página da lista, usando o próprio navegador. Se a página pedir login, captcha ou uma escolha, você precisa resolver: a tarefa informa o motivo e oferece **Abrir página de cancelamento**.

Recibos, pedidos e avisos de pagamento são excluídos. E-mails recebidos por um endereço de grupo, como um Google Group, aparecem com o nome de quem os escreveu, e a rotina nunca cancela sua inscrição no grupo. Se o remetente não tiver uma opção própria para cancelar a inscrição, a tarefa mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa por área com e-mails de remetentes desconhecidos que parecem spam. Cada e-mail tem as opções **Spam** ou **Não é spam**. Outlook move o spam para a pasta de lixo eletrônico, e Gmail marca o e-mail como spam. A rotina verifica os e-mails a cada hora, então o spam geralmente já está lá quando você chega. Novos e-mails de spam são adicionados à mesma tarefa enquanto ela estiver aberta.

Uma conta do Gmail conectada como somente leitura, como em uma Machine hospedada, não pode mover e-mails para o spam. Nesse caso, **Spam** mostra um link para marcar o e-mail no Gmail, e The Machine memoriza o remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Remetente desconhecido significa que você nunca escreveu para essa pessoa. Um “Re:” só conta como conversa se você tiver escrito na conversa. Se um e-mail de um remetente que você marcou como spam, na tarefa ou na sua caixa de entrada, voltar a chegar, ele aparecerá na próxima tarefa como **Já marcado como spam**. Os e-mails que você mesmo moveu para o spam também ajudam a rotina a identificar mensagens parecidas.

Nada muda até você confirmar na tarefa. Toque em um remetente para ler o e-mail antes: ele continuará como não lido e nada mudará. Na Limpeza de spam, as imagens da web não são carregadas, então o remetente não consegue saber que você abriu o e-mail. A rotina não pergunta de novo sobre os remetentes que você já avaliou. Se não houver newsletters ou spam em um dia, nenhuma tarefa será criada. Essas tarefas nunca enviam uma notificação.

Quando você avaliar todos os remetentes, a tarefa indicará que foi concluída e mostrará **Marcar como feita**.

O **Resumo diário** escolhe, uma vez por dia, algumas newsletters que valem seu tempo e reúne os destaques em uma tarefa. Cada item explica em uma linha por que é relevante para você. Toque em um item para ler o e-mail ou use **Abrir no seu e-mail**. A rotina considera apenas newsletters, nunca e-mails de pessoas, recibos ou remetentes cuja inscrição você cancelou, e nunca itens que você já leu. Se nada se destacar, nenhuma tarefa será criada.

A rotina aprende o que importa para você com o que você abre, marca com estrela ou arquiva sem ler, além das opções **Mais assim** e **Menos assim** em cada destaque. Os temas que ela seleciona aparecem no cartão da rotina, em **Mais de** e **Menos de**. Remova um tema com × ou adicione o seu. Os temas com linha tracejada foram aprendidos pela rotina. Um novo resumo substitui o que estiver aberto, e a rotina nunca envia uma notificação.

A rotina lê apenas o remetente, o assunto e o início de cada newsletter nova. Ela faz uma pergunta curta por dia à sua IA sobre as newsletters, com um limite diário para manter o custo baixo. **Mudar quando** define o horário. Depois que você mudar as palavras da rotina, ela será executada com suas instruções, como qualquer outra rotina.

**Aniversários** cria uma tarefa para cada pessoa próxima cujo aniversário é hoje: pessoas para quem você mesmo escreve, como amigos, familiares e contatos frequentes. Cada pessoa vem com uma saudação curta, preparada no lugar em que você costuma conversar com ela, como o chat dela no WhatsApp ou a conversa por e-mail, no idioma da pessoa. A mensagem só é enviada quando você a envia. Se não houver aniversários em um dia, nenhuma tarefa será criada.

Os aniversários vêm dos seus calendários (eventos de aniversário do Google e o calendário Aniversários, lidos todas as manhãs mesmo quando não estão sincronizados, e o calendário Aniversários do Outlook), dos seus contatos do Google em uma Machine auto-hospedada e de um campo de data chamado Birthday em uma pessoa no Graph. Se ainda não houver nenhum aniversário nessas fontes, o resultado mostra **Ainda não há informações de aniversário** e explica como adicionar essas informações.

**Importar aniversários do Facebook**: depois que Aniversários estiver ativado, uma tarefa oferece a opção de ler a página de aniversários do Facebook. Toque em **Importar** e The Machine abre a página no próprio navegador, rola até todos os meses carregarem e lê o nome e o aniversário de cada amigo. A rotina mostra quantos aniversários encontrou e quais pessoas correspondem a contatos no seu Graph, comparando nome e sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela será ignorada e listada.

Só **Salvar** importa os dados, na página de cada pessoa: o aniversário e a foto do perfil do Facebook, se a pessoa ainda não tiver foto. Um aniversário ou uma foto que você definir ali será mantido, e uma foto que a pessoa já tiver nunca será substituída. Nada é publicado no Facebook.

A rotina nunca lê a página de novo sozinha. Para isso, toque em **Importar de novo** na tarefa. O navegador precisa estar conectado ao Facebook. Se não estiver, toque em **Entrar no Facebook** na tarefa e faça login ali. Depois que você entrar, a rotina lê a página automaticamente. The Machine nunca faz login por você.

A rotina conta os amigos que ainda não estão no seu Graph e mostra alguns nomes. **Adicionar … como contatos pessoais** adiciona todos de uma vez, também depois de tocar em **Salvar**: cada contato com nome e aniversário, nunca compartilhado com uma Work Fleet. A rotina ignora nomes que já estejam no seu Graph ou de pessoas que você excluiu permanentemente. Você só recebe lembretes de aniversário das pessoas para quem escreve.

**Desfazer** na tarefa remove exatamente essas pessoas, inclusive depois de **Importar de novo**.

**Assinaturas e testes** lê recibos, faturas e avisos de renovação uma vez por mês e reúne suas assinaturas em uma tarefa: quanto custa cada uma, quando será a próxima cobrança e um aviso quando um período de teste terminar ou o preço aumentar. A lista inclui apenas assinaturas que a rotina consegue identificar com certeza. Se nada for encontrado, nenhuma tarefa será criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. A rotina não pergunta de novo sobre uma assinatura mantida, a menos que o preço mude. **Cancelar** mostra a página de cancelamento ou um rascunho pedindo o cancelamento, que só é enviado quando você envia. Entre uma execução e outra, a rotina verifica as assinaturas diariamente e cria uma tarefa se um período de teste ou uma renovação for cobrado nos próximos 7 dias.

**Manter contato** lembra você de vez em quando de falar com alguém próximo, mas só quando há um motivo real. No cartão da rotina, escolha quem incluir em uma lista curta de pessoas com quem você mesmo conversa, nos dois sentidos, ao longo de vários meses. Remova alguém com ×.

A rotina só envia um lembrete quando faz bem mais tempo que o normal desde a última conversa e há algo específico para dizer: uma novidade que a pessoa compartilhou, uma promessa ainda pendente ou uma mensagem que você nunca respondeu. A tarefa explica o motivo e inclui uma mensagem curta, preparada no lugar em que você costuma conversar com a pessoa, no idioma dela. A mensagem só é enviada quando você a envia. Se não houver nada a dizer, nenhuma tarefa será criada.

A rotina envia no máximo dois lembretes por semana e um por pessoa por mês. Ela não envia lembretes para alguém com quem você conversou recentemente. **Não precisa** em um lembrete faz a rotina esperar mais tempo antes de lembrar você daquela pessoa, e esse intervalo aumenta a cada vez. Ela nunca envia notificações e fica sempre na área Pessoal: nunca é compartilhada com uma Work Fleet.

**Achados de usados** acompanha uma busca em um site de usados, como Marktplaats, Vinted, eBay ou Facebook Marketplace. Faça uma busca com os filtros que quiser, copie o endereço dos resultados e cole depois de tocar em **Adicionar**. Se quiser, inclua filtros com suas próprias palavras, como “menos de 300, a até 30 km, sem ‘para peças’”. Cada busca é uma rotina separada, então adicione outra para fazer uma nova busca.

A cada 3 horas, a rotina abre a busca no próprio navegador de The Machine e procura anúncios que ainda não viu. Primeiro, ela verifica o preço, a distância e os termos que você excluiu, usando código simples.

A rotina abre cada novo anúncio que atende aos critérios. Sua IA avalia o estado do item com base na foto e na descrição, e o vendedor com base nas avaliações, na classificação e no tempo de existência da conta. Os bons anúncios são reunidos em uma tarefa, cada um com foto, título, preço e uma avaliação em uma linha. Toque em um anúncio para abri-lo no navegador de The Machine.

Enquanto a tarefa estiver aberta, novos anúncios são adicionados ao topo, o total aumenta e a rotina envia outra notificação, porque boas ofertas acabam rápido. Marque a tarefa como feita para que a próxima descoberta crie uma nova. Se uma execução não encontrar nada bom, nada muda.

A rotina é cuidadosa e mantém o custo baixo: lê a busca uma vez por execução, abre no máximo 6 anúncios por execução com uma pausa entre eles e verifica no máximo 40 anúncios por dia em todas as suas buscas. Cada verificação é uma pergunta curta à sua IA, com uma foto. Na primeira execução, a rotina verifica os anúncios mais recentes e considera os outros como já vistos. Assim, nas próximas execuções, ela só traz novidades.

Se o site pedir para você entrar, mostrar uma verificação de robô ou impedir a leitura, uma tarefa informa o que aconteceu e oferece **Abrir** para ver a página no navegador de The Machine. Entre ou conclua a verificação por conta própria. A próxima execução tentará ler a página de novo. The Machine nunca faz login nem resolve verificações por você, e nunca entra em contato com vendedores, dá lances ou compra.

**Alterar busca** no cartão da rotina permite usar outro endereço ou outros filtros. **Mudar quando** permite escolher outra frequência, como “a cada 6 horas”.

Enquanto uma rotina de modelo mantiver as instruções do modelo, ela será executada com o próprio código, sem usar seu plano de IA. A Limpeza de spam, por exemplo, primeiro lista em código os novos e-mails de remetentes desconhecidos e só faz uma pergunta curta à sua IA se houver algum. Manter contato só pergunta sobre uma ou duas pessoas selecionadas. Um novo nome não muda isso. Depois que você mudar as palavras da rotina, ela será executada com suas instruções, como qualquer outra rotina.

A Limpeza de newsletters e a Limpeza de spam continuam criando a mesma tarefa, com uma opção para cada e-mail. Uma rotina de Aniversários editada mostra o resultado e, no máximo, um rascunho, em vez de criar uma tarefa por pessoa. **Voltar ao modelo** em **Editar** restaura as instruções do modelo.

## O que uma rotina faz

No horário definido, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e mostra o resultado na página Rotinas. Cada resultado aparece como **Para revisar**, **Nada de novo** (com o motivo) ou **Não funcionou** (com o motivo). Uma execução que termina sem resultado conta como uma execução que não funcionou, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da web, GitHub e sites como X no navegador. Elas não enviam mensagens, respondem, publicam nem mudam nada. Apenas um modelo altera e-mails, e somente o que você confirmar na tarefa correspondente.

Se a rotina tiver uma publicação ou mensagem como etapa final, ela executa tudo até essa etapa e mostra o rascunho, como **Publicaria no X:**. Depois de uma execução real, o rascunho aparece como uma tarefa para você aprovar. Uma execução de teste apenas o mostra. O nome indica o assunto e o destino, o botão indica a etapa, como **Publicar**, e **Da sua rotina**, logo abaixo, abre a rotina.

A tarefa começa na área da conta de onde será enviada, como Trabalho para a conta X da sua empresa, então nunca pede para você movê-la.

Uma execução pode seguir suas [habilidades](skills.md) ativadas, selecionadas de acordo com o que a rotina faz. A rotina lê na íntegra apenas as habilidades relevantes. O resultado lista as habilidades usadas em **Usadas:**. Uma habilidade nunca faz uma rotina enviar ou alterar nada.

Suas rotinas ficam em **Suas rotinas**, abaixo das sugestões, se houver. Um resultado longo é reduzido a uma prévia curta. Toque nele ou em **Mostrar mais** para abrir o resultado.

Cada execução conhece o resultado anterior, então pode indicar o que mudou desde então.

Depois de uma execução bem-sucedida, sua Machine pode criar uma receita para automatizar a leitura que se repete, como quais e-mails ou alterações no GitHub verificar. Nas próximas execuções, a rotina lê esses dados primeiro, usando código simples, e a IA seleciona e escreve apenas o que importa, com menos tokens. Uma receita só lê dados. Se parar de funcionar, a rotina faz a leitura por conta própria e corrige o problema. A receita aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias sem execução

Se sua Machine estiver desligada ou ocupada, as execuções perdidas não se acumulam: apenas a mais recente é executada, uma vez. Cada data tem uma única execução, mesmo depois de uma reinicialização.

As rotinas são executadas uma de cada vez e ficam aguardando quando o uso do seu plano de IA está baixo, como todo trabalho em segundo plano. **Rodar agora** executa a rotina imediatamente. O resultado aparece no cartão quando estiver pronto.

## Mudar ou parar uma rotina

As opções ficam no menu ⋯ da rotina. **Editar** muda o nome e o que ela faz. O horário de execução e os resultados anteriores são mantidos. **Mudar quando** define uma nova frequência com suas próprias palavras, como “todos os dias úteis às 8h”. As duas opções têm **Salvar** e **Cancelar**. No computador, você também pode cancelar com Esc ou clicando fora.

Em **Editar**, **Testar** executa uma vez as novas instruções e mostra o resultado ali. A rotina continua como estava até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar** no cartão. As rotinas pausadas ficam em **Pausado**, abaixo das suas rotinas, e as execuções que não aconteceram durante a pausa não são realizadas depois. **Parar** encerra uma rotina definitivamente.

Você pode ter até 20 rotinas, incluindo as pausadas. Pare uma rotina para adicionar outra.

Se você usar **Pedir mudanças** na tarefa de uma rotina ou escrever no chat dela, e a observação valer para todas as execuções, como “nunca use emojis”, a tarefa oferecerá a opção **Mudar também a rotina**, tanto na tarefa quanto no chat, abaixo da resposta. A opção mostra o que será alterado nas instruções da rotina. A rotina só muda quando você toca em **Mudar**. **Deixar como está** mantém tudo igual. Uma correção que se aplica apenas àquele rascunho não oferece essa opção.

## Avançado: etapas de script

Não é preciso escrever scripts: diga com suas próprias palavras o que a rotina deve fazer e sua Machine resolve o resto.

Para quem tem mais experiência, uma rotina também pode executar comandos próprios na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** mostra as etapas somente quando a rotina já tem alguma. **Buscar dados** executa primeiro um comando, na pasta dele (ou na sua pasta pessoal, se estiver vazia), por no máximo o número de segundos definido. O que o comando exibir fica disponível para a execução usar. Se você não escrever instruções, o que ele exibir será o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se o comando terminar com um erro, a execução mostra **Não funcionou** e o que a verificação informou. Um comando de Buscar dados que falhar também mostra a mesma mensagem.

Um comando deve estar em uma linha e é executado sem shell: não use pipes nem variáveis. As etapas de script são suas e ficam definidas apenas no seu painel. Uma execução de teste e **Testar** também executam Buscar dados e avisam você. Mesmo assim, nada é enviado nem salvo. Uma rotina nunca envia nada, então uma etapa de script deve apenas ler.

## Dos seus jobs do OpenClaw

Se você já criou jobs agendados no OpenClaw, sua Machine os lê (nunca os altera) e oferece como rotinas, em **Sugerido**, os que forem compatíveis. Cada job já foi executado uma vez, então você vê um resultado real.

A rotina mantém as correções que você fez no job e exclui o que ele enviou ou publicou. Se o job executou um script ou leu dados coletados por um job de script, a rotina inclui isso em Buscar dados. **Adicionar** transforma o job em uma rotina. **Não, obrigado** impede que a rotina volte a perguntar sobre esse job. Um job que lembrava você de fazer algo aparece em Tarefas, como uma oferta para criar uma tarefa recorrente.

Antes de adicionar uma sugestão, **Editar** e **Mudar quando**, no menu ⋯, permitem alterá-la como qualquer rotina. **Rodar de novo** executa a rotina agora com as instruções atuais para mostrar resultados mais recentes, por exemplo, depois de um fim de semana tranquilo. Ela apenas lê os dados, é executada uma vez a cada toque e substitui o resultado anterior pelo novo.

No máximo três sugestões ficam disponíveis ao mesmo tempo. Depois de uma semana de execuções bem-sucedidas, a rotina pergunta **Desativar o antigo job do OpenClaw?**. Ela só será desativada se você tocar em **Desativar**. Você pode ativá-la de novo no OpenClaw. **Manter** deixa os dois jobs em execução.

## Com base no que você faz

Sua Machine também percebe tarefas que você realiza com frequência e sugere uma rotina em **Sugerido**, mesmo sem usar OpenClaw. Ela procura:

- o mesmo pedido feito pelo menos três vezes seguidas, como “resuma os chamados de suporte em aberto” toda segunda-feira;
- um e-mail que você envia regularmente, como um relatório semanal para sua equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como mensagens da escola e do clube encaminhadas para seu parceiro: um resumo semanal poupa você de encaminhar cada mensagem;
- o mesmo pedido que você responde com frequência, como uma aprovação mensal para a mesma pessoa.

Cada sugestão informa o que a rotina identificou, como “Pedido 4 vezes seguidas” ou “Encaminhados 6 e-mails para Sam em 3 semanas”, e já foi executada uma vez para você ver um resultado real. Pense em um resumo da equipe, um briefing antes de uma reunião semanal, um resumo de suporte ou desenvolvimento, um panorama dos seus números ou um resumo das newsletters que você recebe.

A rotina sugere apenas tarefas específicas para você e claramente úteis. Por exemplo, um resumo de notícias inclui só as suas newsletters, nunca um resumo genérico. Se nada for relevante, nenhuma sugestão será criada.

A rotina verifica no máximo uma vez por dia e mostra no máximo uma nova sugestão por semana, sem enviar uma notificação. **Não, obrigado** impede que essa sugestão apareça de novo. Os encaminhamentos e as respostas ficam na conta de onde foram enviados, então as áreas Trabalho e Pessoal não se misturam. Tudo fica na sua Machine. Uma tarefa que você conclui com frequência aparece como uma oferta para criar uma tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma [tarefa recorrente](recurring.md) lembra você de fazer algo. Uma rotina é um trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para “pagar o aluguel no primeiro dia do mês” e uma rotina para “toda sexta-feira, me diga quais oportunidades ficaram sem movimentação”.
