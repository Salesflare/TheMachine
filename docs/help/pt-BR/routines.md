---
title: Rotinas
area: cards
summary: Trabalhos que sua Machine faz sozinha, em uma frequência definida, como um resumo das suas negociações em aberto toda segunda-feira. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: e0d519d5927cdde0
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga em uma linha o que ela deve fazer e quando: "toda segunda-feira às 9h, faça um resumo das minhas negociações em aberto" ou "todas as manhãs dos dias úteis, liste os e-mails que ainda preciso responder". Depois, **Adicionar**.

Se você não definir um horário, ela roda às 8:00. O horário segue o relógio da sua Machine. Na primeira execução, ela recebe um nome curto.

Ao tocar em **Adicionar**, primeiro é feita uma execução de teste para você ver o resultado antes de manter a rotina. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina na frequência definida, **Mudar** testa outras palavras ou um nome novo, e **Cancelar** descarta tudo.

## Modelos

Em **Modelos**, no fim da seção Rotinas, **Adicionar** ativa uma rotina pronta. Ela roda uma vez na hora e, depois, todas as manhãs às 7:30 (a Limpeza de spam roda a cada hora, Achados de usados a cada 3 horas, e Assinaturas e testes uma vez por mês). O cartão mostra as palavras usadas, como em qualquer rotina, e **Editar** permite mudar as palavras ou o nome.

Quando chegam muitas newsletters e a Limpeza de newsletters está desativada (25 ou mais em uma semana, de pelo menos 5 remetentes), uma mensagem acima das tarefas informa quantas chegaram e o que a rotina faria, com as opções **Ativar** e **Não, obrigado**.

A Limpeza de spam é oferecida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para spam em uma semana. **Ativar** adiciona a rotina, como **Adicionar** faz aqui. Ao tocar em **Não, obrigado**, ela não será oferecida novamente. O mesmo vale para um modelo que você já tinha.

A **Limpeza de newsletters** cria uma tarefa por área (trabalho e pessoal) com as newsletters do último dia. Cada uma tem as opções **Manter** e **Cancelar inscrição**. Para cancelar a inscrição, a rotina usa o link de um clique da lista ou envia um e-mail de cancelamento do seu endereço, se o envio estiver ativado. Caso contrário, a The Machine cancela sua inscrição na página da lista, usando o próprio navegador. Se a página exigir login, captcha ou alguma escolha sua, a tarefa explica o motivo e mostra a opção **Abrir página de cancelamento**.

Recibos, pedidos e avisos de pagamento ficam de fora. E-mails recebidos por um endereço de grupo, como um Google Group, aparecem com o nome de quem os escreveu. A rotina nunca cancela sua inscrição no grupo. Quando o remetente não tem uma opção própria para cancelar a inscrição, a tarefa mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa por área com e-mails de remetentes desconhecidos que parecem spam. Cada e-mail tem as opções **Spam** e **Não é spam**. No Outlook, os e-mails são movidos para a pasta de lixo eletrônico. No Gmail, são marcados como spam. A rotina verifica os e-mails a cada hora, então o spam costuma aparecer antes de você conferir. Novos e-mails de spam são adicionados à mesma tarefa enquanto ela estiver aberta.

Uma conta do Gmail conectada em modo somente leitura, como em uma Machine hospedada, não pode mover e-mails para spam. Nesse caso, **Spam** mostra um link para marcar o e-mail como spam no Gmail, e a The Machine memoriza o remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Remetente desconhecido significa que você nunca escreveu para ele. Um "Re:" só conta como conversa em uma conversa que você iniciou. Se você marcar como spam um e-mail de um remetente, na tarefa ou na sua caixa de entrada, e outro e-mail dele passar pelo filtro, ele aparecerá na próxima tarefa como **Já marcado como spam**. Os e-mails que você mesmo moveu para spam também ajudam a rotina a identificar mensagens parecidas.

Nada muda até você confirmar na tarefa. Toque em um remetente para ler o e-mail primeiro: ele continua como não lido e nada muda. Na Limpeza de spam, as imagens da internet não são carregadas, então o remetente não consegue ver que o e-mail foi aberto. A rotina não pergunta de novo sobre os remetentes cuja decisão você já tomou. Se não houver newsletters nem spam em um dia, nenhuma tarefa é criada. Essas tarefas nunca enviam uma notificação.

Quando você decidir o que fazer com todos os remetentes, a tarefa informa que foi concluída e mostra a opção **Marcar como concluída**.

O **Resumo diário** seleciona, uma vez por dia, algumas newsletters que valem seu tempo e reúne tudo em uma tarefa. Cada item explica em uma linha por que é relevante para você. Toque no item para ler o e-mail ou use **Abrir no seu e-mail**. A rotina considera apenas newsletters, nunca e-mails de pessoas, recibos ou remetentes cuja inscrição você cancelou. Também deixa de fora o que você já leu. Se nada se destacar, nenhuma tarefa é criada.

A rotina aprende o que interessa para você pelo que abre, marca com estrela ou arquiva sem ler, além das opções **Mais assim** e **Menos assim** em cada sugestão. Os assuntos que ela seleciona aparecem no cartão da rotina, em **Mais de** e **Menos de**. Remova um assunto com × ou adicione um. Os assuntos tracejados foram identificados pela própria rotina. Um novo resumo substitui o que ainda estiver aberto. Ele nunca envia uma notificação.

A rotina só lê o remetente, o assunto e o início de cada newsletter nova e faz uma pergunta curta sobre eles para sua IA. Há um limite diário para manter o custo baixo. **Mudar quando** define o horário. Depois que você muda as palavras da rotina, ela passa a funcionar como qualquer outra, seguindo as palavras que você definiu.

**Aniversários** cria uma tarefa para cada pessoa próxima que faz aniversário hoje: pessoas com quem você conversa por conta própria, como amigos, familiares e contatos frequentes. Para cada pessoa, a tarefa inclui uma mensagem curta de parabéns, escrita no lugar em que você costuma conversar com ela, como no chat do WhatsApp ou na conversa por e-mail, e no idioma dela. A mensagem só é enviada quando você a envia. Se não houver aniversários no dia, nenhuma tarefa é criada.

Os aniversários vêm dos seus calendários (eventos de aniversário e o calendário Aniversários do Google, lidos todas as manhãs mesmo que não estejam sincronizados, e o calendário Aniversários do Outlook), dos seus contatos do Google em uma Machine hospedada por você e de um campo de data chamado Birthday em uma pessoa no Graph. Se nenhum deles tiver uma data de aniversário, o resultado mostra **Ainda não há informações de aniversário** e explica como adicionar uma.

**Importar aniversários do Facebook**: depois que Aniversários estiver ativado, uma tarefa oferece a leitura da página de aniversários do Facebook. Toque em **Importar** e a The Machine abre a página no próprio navegador, rola até carregar todos os meses e lê o nome e o aniversário de cada amigo. Ela mostra quantas pessoas encontrou e quem corresponde a pessoas no seu Graph, comparando nome e sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela não importa ninguém com esse nome e mostra a lista.

Só **Salvar** importa os dados, na página de cada pessoa: a data de aniversário e a foto de perfil do Facebook, se a pessoa ainda não tiver uma foto. Uma data de aniversário ou foto que você definir na página permanece como está, e uma foto que a pessoa já tiver nunca será substituída. Nada é publicado no Facebook.

A rotina não lê os dados novamente sozinha. Para isso, toque em **Importar de novo** na tarefa. O navegador precisa estar conectado ao Facebook. Se não estiver, toque em **Entrar no Facebook** na tarefa e faça login por lá. Depois que você entrar, a rotina lê a página sozinha. A The Machine nunca faz login por você.

A rotina conta os amigos que ninguém no seu Graph tem como contato e mostra alguns nomes. **Adicionar … como contatos pessoais** adiciona todos de uma vez, inclusive depois de tocar em Salvar. Cada pessoa é adicionada com o nome e a data de aniversário, sem compartilhar os dados com um Fleet de Trabalho. A rotina ignora alguém cujo nome já esteja no seu Graph ou que você tenha excluído permanentemente. Os lembretes de aniversário continuam aparecendo apenas para pessoas com quem você conversa.

A opção **Desfazer** na tarefa remove exatamente essas pessoas, inclusive depois de tocar em **Importar de novo**.

**Assinaturas e testes** lê recibos, faturas e avisos de renovação uma vez por mês e reúne suas assinaturas em uma tarefa. Ela mostra o custo de cada uma, a próxima data de cobrança e um aviso quando um período de teste termina ou o preço aumenta. Só aparecem as assinaturas que a rotina consegue identificar com segurança. Se nada for encontrado, nenhuma tarefa é criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. Uma assinatura mantida não volta a aparecer, a menos que o preço mude. **Cancelar** leva à página de cancelamento ou cria um rascunho pedindo o cancelamento. A mensagem só é enviada quando você a envia. Entre uma execução e outra, a rotina verifica as assinaturas diariamente e cria uma tarefa quando uma cobrança de teste ou renovação estiver prevista para os próximos 7 dias.

**Manter contato** lembra você de vez em quando de falar com alguém próximo, mas só quando há um motivo de verdade. No cartão da rotina, escolha quem incluir em uma lista curta de pessoas com quem você conversa por conta própria, nos dois sentidos, ao longo de vários meses. Para remover alguém, toque em ×.

A rotina só envia um lembrete quando faz muito mais tempo do que o normal desde a última conversa e há algo específico para dizer: uma novidade que a pessoa compartilhou, uma promessa ainda pendente ou uma mensagem que você nunca respondeu. Ela cria uma tarefa com o motivo e uma mensagem curta, escrita no lugar em que você costuma conversar com a pessoa e no idioma dela. A mensagem só é enviada quando você a envia. Se não houver nada a dizer, nenhuma tarefa é criada.

A rotina envia no máximo dois lembretes por semana e um por pessoa por mês. Ela não envia lembretes para alguém com quem você conversou recentemente. **Não precisa** em um lembrete faz a rotina esperar mais tempo antes de lembrar você dessa pessoa. Cada vez que você escolhe essa opção, ela espera ainda mais. A rotina nunca envia uma notificação e fica na área Pessoal: nunca é compartilhada com um Fleet de Trabalho.

**Achados de usados** acompanha uma busca em um site de usados, como Marktplaats, Vinted, eBay ou Facebook Marketplace. Faça uma busca no site com os filtros que quiser, copie o endereço dos resultados e cole depois de tocar em **Adicionar**. Se quiser, escreva outros filtros com suas próprias palavras, como "abaixo de 300, até 30 km, sem 'para peças'". Cada busca é uma rotina própria, então adicione outra para cada busca nova.

A cada 3 horas, a rotina abre a busca no próprio navegador da The Machine e procura anúncios que ainda não viu. Primeiro, ela verifica o preço, a distância e as palavras que você excluiu, usando código simples.

A rotina abre cada anúncio novo que passar pelos filtros. Sua IA avalia o estado do item pela foto e descrição, e o vendedor pelas avaliações, nota e tempo de existência da conta. Os anúncios que parecem bons aparecem em uma única tarefa, cada um com foto, título, preço e uma avaliação em uma linha. Toque em um anúncio para abri-lo no navegador da The Machine.

Enquanto a tarefa estiver aberta, novos achados aparecem no topo, a quantidade aumenta e você recebe outra notificação, porque boas ofertas somem rápido. Quando você marca a tarefa como concluída, o próximo achado inicia uma nova tarefa. Uma execução sem anúncios bons não altera nada.

A rotina é cuidadosa e econômica: faz uma leitura da busca por execução, abre no máximo 6 anúncios por execução, com uma pausa entre eles, e verifica no máximo 40 anúncios por dia em todas as suas buscas. Cada verificação é uma pergunta curta para sua IA, com uma foto. Na primeira execução, ela verifica alguns dos anúncios mais recentes e considera o restante como já visto. Assim, nas próximas execuções, mostra apenas as novidades.

Se o site pedir que você entre, mostrar uma verificação de robô ou impedir a leitura, uma tarefa avisa você e mostra **Abrir** para ver o site no navegador da The Machine. Entre na sua conta ou passe pela verificação por conta própria. Na próxima execução, a rotina tenta ler o site novamente. A The Machine nunca faz login nem resolve uma verificação por você, e nunca entra em contato com vendedores, faz ofertas ou compra.

**Alterar busca** no cartão da rotina permite usar outro endereço ou filtros. **Mudar quando** define outra frequência, como "a cada 6 horas".

**Recompras** lê as confirmações de pedido de lojas on-line que estão no seu e-mail e identifica o que você compra repetidamente, como café, ração ou vitaminas. Quando a próxima compra provavelmente estiver chegando, a rotina cria uma tarefa com o item, a loja, o último preço e a data da última compra. **Abrir na loja** leva você à página do item para comprá-lo. Nada é comprado por você.

A rotina precisa encontrar pelo menos três pedidos do mesmo item em intervalos regulares. Por isso, uma compra única ou um intervalo fora do normal não cria uma tarefa. Por enquanto, ela lê pedidos de lojas que usam Shopify. Sua IA lê apenas e-mails novos de pedidos dessas lojas, com uma pergunta curta por execução. Essas tarefas nunca enviam uma notificação. Quando você faz outro pedido do item, a tarefa em aberto é encerrada.

Enquanto a rotina de um modelo mantiver as palavras do modelo, ela funciona com código próprio, sem usar seu plano de IA. Por exemplo, a Limpeza de spam primeiro lista com código os e-mails novos de remetentes desconhecidos e só faz uma pergunta curta à sua IA quando há algum. Manter contato só pergunta sobre uma ou duas pessoas que a rotina selecionou. Depois que você muda as palavras do modelo, ele passa a funcionar como qualquer outra rotina, seguindo as palavras que você definiu.

A Limpeza de newsletters e a Limpeza de spam continuam criando a mesma tarefa, com uma escolha para cada e-mail. Uma versão editada de Aniversários mostra o resultado e, no máximo, um rascunho, em vez de criar uma tarefa por pessoa. **Voltar ao modelo**, em **Editar**, restaura as palavras originais.

## O que uma rotina faz

No horário definido, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e coloca o resultado na página Rotinas. Cada resultado mostra **Para revisar**, **Nada de novo** (com o motivo) ou **Não funcionou** (com o motivo). Uma execução que termina sem resultado conta como uma execução que não funcionou, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da web, GitHub e sites como X no navegador. Elas não enviam mensagens, respondem, publicam nem alteram nada. Elas abrem páginas encontradas no conteúdo que leram ou em uma busca, endereços de páginas simples e sites conhecidos. Nunca abrem um endereço inventado para transportar o conteúdo lido. Só um modelo altera e-mails, e apenas o que você confirmar na tarefa dele.

Quando o trabalho de uma rotina inclui publicar ou enviar uma mensagem, ela faz tudo até essa etapa e mostra o rascunho, como em **Publicaria no X:**. Depois de uma execução real, ele aparece em uma tarefa para você aprovar. Uma execução de teste apenas o mostra.

O nome da tarefa indica o assunto e onde ela será publicada ou enviada. **Da sua rotina**, logo abaixo, abre a rotina. O botão indica a etapa, como **Preparar publicação**: ele prepara a publicação, mas não publica nada. Você publica pelo resultado. Se a The Machine não puder publicar por você, o botão abre a página em que você pode fazer isso.

A tarefa começa na área da conta de onde será enviada, como Trabalho para a conta da sua empresa no X, para que você não precise movê-la.

Uma rotina pode seguir suas [habilidades](skills.md) ativadas, escolhidas de acordo com o que ela faz. Só as habilidades relevantes são lidas na íntegra. O resultado as lista em **Usadas:**. Uma habilidade nunca faz uma rotina enviar ou alterar nada.

Suas rotinas ficam em **Suas rotinas**, abaixo das sugestões. Se um resultado for longo, ele aparece como uma prévia curta. Toque em **Mostrar mais** ou no resultado para abri-lo.

Cada execução considera o resultado anterior e pode indicar o que mudou desde então.

Depois de uma execução bem-sucedida, sua Machine pode criar uma receita para as partes da leitura que se repetem, como quais e-mails ou mudanças no GitHub verificar. Nas próximas execuções, ela começa lendo essas informações com código simples. A IA só seleciona o que importa e escreve o resultado, usando menos tokens. Uma receita só lê. Se parar de funcionar, a rotina faz a leitura sem ela e corrige o problema. A receita aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias sem execução

Se sua Machine estava desligada ou ocupada, as execuções perdidas não se acumulam: apenas a mais recente roda, uma vez. Cada data tem uma única execução, mesmo depois de reiniciar.

As rotinas são executadas uma de cada vez e ficam aguardando quando o uso do seu plano de IA está baixo, como todo trabalho em segundo plano. **Rodar agora** executa a rotina na hora. O resultado aparece no cartão quando estiver pronto.

## Alterar ou parar uma rotina

Essas opções ficam no menu ⋯ da rotina. **Editar** permite mudar o nome e o que ela faz. O horário e os resultados anteriores permanecem. **Mudar quando** permite definir outra frequência com suas próprias palavras, como "todos os dias úteis às 8h". As duas opções têm **Salvar** e **Cancelar**. No computador, a tecla Esc ou um clique fora da janela também cancela.

Em **Editar**, **Testar** executa uma vez usando as novas palavras e mostra o resultado. A rotina continua igual até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar** no cartão. Rotinas pausadas ficam em **Pausado**, abaixo das suas rotinas. As execuções perdidas durante a pausa não são feitas depois. **Parar** encerra a rotina de vez.

Você pode ter até 20 rotinas, incluindo as pausadas. Para adicionar outra, pare uma das que já tem.

Quando você usa **Pedir mudanças** na tarefa de uma rotina ou escreve no chat dela, e a observação vale para todas as execuções, como "nunca use emojis", a tarefa mostra a opção **Mudar também a rotina**. Ela aparece na tarefa e no chat, abaixo da resposta. A rotina mostra o que será alterado nas instruções e só muda quando você toca em **Mudar**. **Deixar como está** mantém tudo igual. Se a correção se aplicar apenas ao rascunho, essa opção não aparece.

## Avançado: etapas de script

Não precisa de script: diga com suas próprias palavras o que a rotina deve fazer, e sua Machine cuida do resto.

Para quem tem mais experiência, uma rotina também pode executar seus próprios comandos na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** só mostra as etapas quando a rotina já tem alguma. **Buscar dados** executa primeiro um comando, na pasta indicada (ou na sua pasta pessoal, se o campo estiver vazio), por até o número de segundos definido. O que o comando exibir fica disponível para a rotina usar. Se não houver instruções, o que ele exibir será o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se o comando terminar com erro, a execução mostra **Não funcionou** e o texto da verificação. Se um comando de Buscar dados falhar, a execução mostra a mesma mensagem.

Cada comando precisa estar em uma única linha e é executado sem um shell: não use pipes nem variáveis. As etapas de script são suas e ficam definidas apenas no seu painel. Uma execução de teste e **Testar** também executam Buscar dados e avisam você. Mesmo assim, não enviam nem salvam nada. Uma rotina nunca envia nada, então uma etapa de script deve apenas ler.

## Dos seus jobs do OpenClaw

Se você criou jobs agendados no OpenClaw, sua Machine os lê (nunca os altera) e oferece os que servem como rotinas em **Sugerido**. Cada job é executado uma vez para mostrar um resultado real.

A rotina mantém suas correções no job e deixa de fora o que ele enviou ou publicou. Um job que executou um script ou leu dados coletados por um job de script traz o script como uma etapa de Buscar dados. **Adicionar** transforma o job em uma rotina. **Não, obrigado** faz com que a rotina não volte a perguntar sobre esse job. Um job que lembrava você de fazer algo aparece como uma oferta de tarefa recorrente na seção Tarefas.

Antes de adicionar uma sugestão, você pode usar **Editar** e **Mudar quando** no menu ⋯ para alterá-la, como faria com qualquer rotina. **Rodar de novo** executa a rotina com as instruções atuais para mostrar resultados mais recentes, por exemplo, depois de um fim de semana tranquilo. Ela só lê, executa uma vez por toque e substitui o resultado anterior pelo novo.

No máximo três sugestões podem ficar aguardando ao mesmo tempo. Depois de uma semana de execuções bem-sucedidas, a rotina pergunta **Desativar o antigo job do OpenClaw?**. Ela só é desativada quando você toca em **Desativar**. Você pode ativá-la de novo no OpenClaw. **Manter** deixa os dois em execução.

## Com base no que você faz

Sua Machine também identifica tarefas que você faz com frequência e oferece transformá-las em uma rotina em **Sugerido**, mesmo sem usar o OpenClaw. Ela procura por:

- o mesmo pedido feito três vezes seguidas ou mais, como "faça um resumo dos chamados de suporte em aberto" toda segunda-feira;
- um e-mail que você envia com frequência, como um relatório semanal para sua equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas conversam toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como mensagens da escola e do clube para seu par. Um resumo semanal evita que você precise encaminhá-las;
- o mesmo pedido que você responde com frequência, como uma aprovação mensal para a mesma pessoa.

Cada sugestão explica o que a rotina identificou, como "Pedido 4 vezes seguidas" ou "6 e-mails encaminhados para Sam em 3 semanas". Ela também é executada uma vez para mostrar um resultado real. Pense em um resumo da equipe, um briefing antes de uma reunião semanal, um resumo de suporte ou desenvolvimento, uma atualização dos seus números ou um resumo das newsletters que você recebe.

A rotina só sugere algo que seja específico para você e claramente útil: um resumo de notícias, por exemplo, considera apenas as newsletters que você recebe, nunca um resumo genérico. Se nada servir, nenhuma sugestão será criada.

A rotina verifica isso no máximo uma vez por dia e traz no máximo uma sugestão nova por semana, sem enviar uma notificação. **Não, obrigado** faz com que a sugestão não volte a aparecer. Os encaminhamentos e as respostas continuam na conta de onde foram enviados, para que Trabalho e Pessoal não se misturem. Tudo fica na sua Machine. Uma tarefa que você conclui com frequência aparece como uma oferta de tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma [tarefa recorrente](recurring.md) lembra você de fazer algo. Uma rotina é um trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para "pagar o aluguel no dia 1" e uma rotina para "toda sexta-feira, me diga quais negociações esfriaram".
