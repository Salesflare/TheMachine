---
title: Rotinas
area: cards
summary: Trabalhos que sua Machine faz sozinha, em uma frequência definida, como um resumo das suas oportunidades em aberto toda segunda-feira. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: ed2171ef31eb6213
---
## Criar uma rotina

Abra **Rotinas** na barra lateral e diga, em uma linha, o que ela deve fazer e quando: "toda segunda-feira às 9h, resuma minhas oportunidades em aberto" ou "todas as manhãs de dias úteis, liste os e-mails que ainda preciso responder". Depois, toque em **Adicionar**.

Se você não definir um horário, ela será executada às 8h. O horário segue o relógio da sua Machine. Na primeira execução, ela recebe um nome curto.

Ao tocar em **Adicionar**, a rotina é testada primeiro para você ver o resultado antes de mantê-la. Nada é enviado nem salvo. Depois, **Adicionar** mantém a rotina na frequência definida, **Mudar** testa outras palavras ou um novo nome, e **Cancelar** descarta a rotina.

## Modelos

Em **Modelos**, no fim da página Rotinas, toque em **Adicionar** para ativar uma rotina pronta. Ela é executada uma vez na hora e, depois, todas as manhãs às 7h30 (a Limpeza de spam é executada de hora em hora, e Assinaturas e testes, uma vez por mês). O cartão mostra as instruções da rotina, como qualquer outra, e **Editar** permite alterar as instruções ou o nome.

Quando você recebe muitas newsletters e a Limpeza de newsletters está desativada (25 ou mais em uma semana, de pelo menos 5 remetentes), uma linha acima das suas tarefas informa quantas chegaram e o que a rotina faria, com as opções **Ativar** e **Não, obrigado**.

A Limpeza de spam é sugerida da mesma forma quando 5 ou mais e-mails foram movidos manualmente para spam em uma semana. **Ativar** adiciona a rotina, como **Adicionar** faz aqui. Se você tocar em **Não, obrigado**, ela não será sugerida de novo. Isso também vale para um modelo que você já tinha.

A **Limpeza de newsletters** cria uma tarefa por área (trabalho e pessoal) com as newsletters do último dia. Para cada uma, você pode escolher **Manter** ou **Cancelar inscrição**. Para cancelar a inscrição, a rotina usa o link de cancelamento com um clique da lista ou envia um e-mail de cancelamento pelo seu endereço, se o envio estiver ativado. Caso contrário, The Machine cancela sua inscrição na página da lista, pelo navegador da própria Machine. Se for preciso fazer login, preencher um captcha ou escolher opções nessa página, você fica responsável por isso. A linha informa o motivo e mostra **Abrir página de cancelamento**.

Recibos, pedidos e avisos de pagamento são excluídos. Os e-mails enviados por um endereço de grupo, como um Google Group, são listados com o nome de quem os escreveu, e a rotina nunca cancela sua inscrição no grupo. Quando o remetente não tem uma opção própria de cancelamento, a linha mostra **Cancelar manualmente**.

A **Limpeza de spam** cria uma tarefa por área com e-mails de remetentes desconhecidos que parecem spam. Para cada um, você pode escolher **Spam** ou **Não é spam**. No Outlook, os e-mails são movidos para Lixo Eletrônico; no Gmail, são marcados como spam. A rotina verifica os e-mails de hora em hora, então o spam geralmente já está identificado quando você chega à tarefa. Novos e-mails de spam são adicionados à mesma tarefa enquanto ela estiver aberta.

Se o Gmail estiver conectado no modo somente leitura, como em uma Machine hospedada, a rotina não poderá mover e-mails para spam. Nesse caso, **Spam** mostra um link para marcar o e-mail no Gmail, e The Machine memoriza o remetente como spam. Se nenhuma conta de e-mail estiver conectada, o modelo mostra **Conectar e-mail** no lugar de **Adicionar**.

Um remetente é desconhecido quando você nunca escreveu para ele. Um assunto começando com “Re:” só é considerado parte de uma conversa em uma conversa na qual você já escreveu. Se você voltar a receber e-mails de um remetente que marcou como spam, na tarefa ou na caixa de entrada, eles aparecerão na próxima tarefa com a indicação **Já marcado como spam**. O que você mesmo moveu para spam também ajuda a rotina a identificar e-mails semelhantes.

Nada muda até você confirmar na tarefa. Toque no remetente para ler o e-mail primeiro: ele continua não lido e nada muda. Na Limpeza de spam, as imagens da internet não são carregadas, então o remetente não consegue saber que você abriu o e-mail. Os remetentes sobre os quais você já decidiu não são perguntados de novo. Se passar um dia sem newsletters ou spam, nenhuma tarefa será criada. Essas tarefas nunca enviam notificações.

Quando você decidir sobre todos os remetentes, a tarefa indicará que foi concluída e mostrará **Marcar como feita**.

O **Resumo diário** escolhe as poucas partes de newsletters que valem seu tempo e reúne tudo em uma tarefa por dia. Cada item explica em uma linha por que é relevante para você. Toque nele para ler o e-mail ou use **Abrir no seu e-mail**. A rotina considera apenas newsletters, nunca e-mails de pessoas, recibos ou remetentes dos quais você cancelou a inscrição, e nunca inclui algo que você já leu. Se nada se destacar, nenhuma tarefa será criada.

A rotina aprende o que é importante para você com base no que você abre, marca com estrela ou arquiva sem ler, além das opções **Mais assim** e **Menos assim** em cada sugestão. Os assuntos que ela escolhe aparecem no cartão da rotina, em **Mais de** e **Menos de**. Toque em × para remover um assunto ou adicione o seu. Os assuntos com linhas tracejadas foram identificados pela própria rotina. Um novo resumo substitui o anterior que ainda estiver aberto e nunca envia notificações.

A rotina lê apenas o remetente, o assunto e o início de cada newsletter nova, e faz uma pergunta curta sobre elas à sua IA, com um limite diário para manter os custos baixos. **Mudar quando** define o horário. Depois que você altera as instruções, a rotina passa a funcionar como qualquer outra, usando as instruções que você definiu.

**Aniversários** cria uma tarefa para cada contato próximo que faz aniversário hoje: pessoas para quem você costuma escrever, como amigos, familiares e contatos frequentes. Cada tarefa inclui uma saudação curta, preparada no lugar onde você costuma conversar com a pessoa, como o chat dela no WhatsApp ou a conversa por e-mail, no idioma da pessoa. A saudação só é enviada quando você envia. Se ninguém fizer aniversário, nenhuma tarefa será criada.

Os aniversários vêm dos seus calendários (eventos de aniversário do Google e o calendário Aniversários, lidos todas as manhãs mesmo quando não estão sincronizados, e o calendário Aniversários do Outlook), dos seus contatos do Google em uma Machine auto-hospedada e de um campo de data chamado Birthday no perfil da pessoa no Graph. Se nenhum deles tiver uma data de aniversário, o resultado mostra **Ainda não há informações de aniversário** e explica como adicionar uma.

**Importar aniversários do Facebook**: depois que Aniversários estiver ativado, uma tarefa oferece a opção de ler a página de aniversários do Facebook. Toque em **Importar** e The Machine abre a página no próprio navegador, rola até carregar todos os meses e lê o nome e o aniversário de cada amigo. Ela mostra quantos aniversários encontrou e quais pessoas correspondem a alguém no seu Graph pelo nome e sobrenome. Se mais de uma pessoa tiver o mesmo nome, ela será ignorada e listada.

Só **Salvar** importa os dados, na página de cada pessoa: o aniversário e, se a pessoa ainda não tiver uma foto, a foto de perfil do Facebook. O aniversário ou a foto que você definir ali serão mantidos, e uma foto que a pessoa já tenha nunca será substituída. Nada é escrito no Facebook.

A rotina não lê os dados novamente por conta própria. Para isso, toque em **Importar de novo** na tarefa. É preciso estar conectado ao Facebook no navegador. Se não estiver, toque em **Entrar no Facebook** na tarefa e faça login. Depois que você entrar, a rotina lê a página automaticamente. The Machine nunca faz login por você.

Os amigos que não estão no seu Graph são contabilizados e alguns nomes são mostrados. **Adicionar … como contatos pessoais** adiciona todos de uma vez, inclusive depois de tocar em Salvar. Cada pessoa fica com seu nome e aniversário e nunca é compartilhada com uma Fleet de trabalho. Uma pessoa com um nome que alguém no seu Graph já tenha, ou que alguém que você excluiu permanentemente tinha, será ignorada. Os lembretes de aniversário continuam sendo enviados apenas para as pessoas para quem você escreve.

**Desfazer** na tarefa remove exatamente essas pessoas, inclusive depois de **Importar de novo**.

**Assinaturas e testes** lê seus recibos, faturas e avisos de renovação uma vez por mês e reúne suas assinaturas em uma tarefa. Para cada uma, mostra o custo, a próxima cobrança e um aviso quando um período de teste termina ou o preço aumenta. Só as assinaturas identificadas com certeza são listadas. Se nada for encontrado, nenhuma tarefa será criada.

Escolha **Manter** ou **Cancelar** para cada assinatura. Uma assinatura mantida não será mostrada de novo, a menos que o preço mude. **Cancelar** mostra a página de cancelamento ou um rascunho pedindo o cancelamento. Ele só será enviado quando você enviar. Entre as execuções mensais, a rotina verifica as assinaturas todos os dias e cria uma tarefa quando um período de teste ou uma renovação será cobrado nos próximos 7 dias.

Enquanto uma rotina de modelo mantiver as instruções originais, ela será executada com o próprio código, sem usar seu plano de IA. A Limpeza de spam, por exemplo, primeiro lista no código os novos e-mails de remetentes desconhecidos e só faz uma pergunta curta à sua IA quando encontra algum. Se você der um novo nome à rotina, ela continuará assim. Depois que você altera as instruções, ela passa a funcionar como qualquer outra rotina, usando as instruções que você definiu.

A Limpeza de newsletters e a Limpeza de spam continuam criando a mesma tarefa, com uma opção para cada e-mail. Se você editar Aniversários, a rotina mostra o resultado e, no máximo, um rascunho, em vez de criar uma tarefa por pessoa. **Voltar ao modelo**, em **Editar**, restaura as instruções originais.

## O que uma rotina faz

No horário definido, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e mostra o resultado na página Rotinas. Cada resultado informa **Para revisar**, **Nada de novo** (e explica o motivo) ou **Não funcionou** (e explica o motivo). Uma execução que termina sem resultado conta como uma falha, nunca como concluída.

As rotinas só leem: suas mensagens, páginas da web, GitHub e sites como X no navegador. Elas não enviam mensagens, respondem, publicam nem alteram nada. Só um modelo altera e-mails, e apenas o que você confirmar na tarefa.

Quando a rotina terminaria com uma publicação ou mensagem, ela faz tudo até essa etapa e mostra o rascunho, como **Publicaria no X:**. Depois de uma execução real, o rascunho aparece como tarefa para você aprovar. Uma execução de teste apenas mostra o rascunho. O nome indica o assunto e onde será publicado, o botão identifica a etapa, como **Publicar**, e **Da sua rotina**, logo abaixo, abre a rotina.

A tarefa começa na área da conta usada para enviar, como Trabalho para a conta X da sua empresa, então você nunca precisa movê-la.

Uma rotina pode seguir suas [habilidades](skills.md) ativadas, escolhidas de acordo com o que ela faz. Só as habilidades relevantes são lidas na íntegra. O resultado lista as habilidades em **Usadas:**. Uma habilidade nunca faz uma rotina enviar ou alterar nada.

Suas rotinas ficam em **Suas rotinas**, abaixo das sugestões. Quando um resultado é longo, ele aparece como uma prévia curta. Toque em **Mostrar mais** ou no próprio resultado para abri-lo.

Cada execução conhece o resultado anterior e pode informar o que mudou desde então.

Depois de uma execução bem-sucedida, sua Machine pode criar uma receita para as partes da leitura que são iguais em todas as execuções, como quais e-mails ou alterações no GitHub verificar. Nas próximas execuções, a rotina lê essas informações primeiro, usando código simples. A IA só escolhe o que importa e escreve o resultado, com menos tokens. A receita só lê. Se parar de funcionar, a rotina lê por conta própria e corrige o problema. A receita aparece em **Avançado: etapas de script**, no menu ⋯.

## Dias perdidos

Se sua Machine estiver desligada ou ocupada, as execuções perdidas não se acumulam. Apenas a mais recente será executada, uma vez. Cada data é executada uma única vez, mesmo depois de uma reinicialização.

As rotinas são executadas uma de cada vez e aguardam quando há pouco uso disponível no seu plano de IA, como todo trabalho em segundo plano. **Rodar agora** executa a rotina imediatamente. Quando o resultado estiver pronto, ele aparece no cartão.

## Alterar ou parar uma rotina

Essas opções ficam no menu ⋯ da rotina. **Editar** altera o nome e as instruções. O horário e os resultados anteriores são mantidos. **Mudar quando** permite definir uma nova frequência com suas próprias palavras, como "todos os dias úteis às 8h". As duas opções têm **Salvar** e **Cancelar**. No computador, você também pode cancelar com Esc ou clicando fora.

Em **Editar**, **Testar** executa as novas instruções uma vez e mostra o resultado ali. A rotina continua como estava até você tocar em **Salvar**.

**Pausar** interrompe as execuções até você tocar em **Retomar** no cartão. As rotinas pausadas ficam em **Pausado**, abaixo das suas rotinas, e nada do que foi perdido durante a pausa será executado depois. **Parar** encerra uma rotina definitivamente.

Você pode ter até 20 rotinas, incluindo as pausadas. Pare uma rotina para adicionar outra.

Quando você usa **Pedir mudanças** em uma tarefa da rotina, ou escreve no chat dela, e sua observação vale para todas as execuções, como "nunca use emojis", a tarefa oferece **Mudar também a rotina**. A opção aparece na tarefa e no chat, abaixo da resposta. Você verá o que muda nas instruções da rotina, que só será alterada quando você tocar em **Mudar**. **Deixar como está** mantém tudo igual. Se a correção for apenas para aquele rascunho, a opção não será oferecida.

## Avançado: etapas de script

Não é preciso usar scripts: diga com suas próprias palavras o que a rotina deve fazer, e sua Machine cuida do resto.

Para usuários avançados, uma rotina também pode executar seus próprios comandos na sua Machine. No menu ⋯, escolha **Avançado: etapas de script**. **Editar** só mostra as etapas quando a rotina já tem alguma. **Buscar dados** executa um comando primeiro, na pasta indicada (ou na sua pasta pessoal, se o campo estiver vazio), por no máximo o número de segundos definido. O que o comando exibe fica disponível para a rotina usar. Se não houver instruções, o resultado será o que o comando exibir.

**Verificação** recebe o resultado como entrada depois da execução. Se terminar com um erro, a rotina mostra **Não funcionou** e informa o que a verificação retornou. Se um comando de Buscar dados falhar, a rotina mostra a mesma mensagem.

Cada comando deve estar em uma linha e é executado sem um shell: não use pipes nem variáveis. As etapas de script são suas e só podem ser definidas no seu painel. Uma execução de teste e **Testar** também executam Buscar dados e informam isso. Elas não enviam nem guardam nada. Uma rotina nunca envia nada, então as etapas de script devem servir apenas para leitura.

## Dos seus jobs do OpenClaw

Se você já criou jobs agendados no OpenClaw, sua Machine os lê, mas nunca os altera, e sugere como rotinas os que forem adequados, em **Sugerido**. Cada um já foi executado uma vez, então você verá um resultado real.

A rotina mantém as correções que você fez no job e exclui o que ele enviou ou publicou. Se um job executou um script ou leu algo coletado por um job de script, esse conteúdo é incluído como Buscar dados. **Adicionar** transforma o job em uma rotina. **Não, obrigado** impede que aquele job seja sugerido de novo. Um job que lembrava você de fazer algo aparece como uma sugestão de tarefa recorrente em Tarefas.

Antes de adicionar uma sugestão, **Editar** e **Mudar quando**, no menu ⋯, permitem alterá-la como qualquer rotina. **Rodar de novo** executa a rotina com as instruções atuais para buscar resultados mais recentes, por exemplo, depois de um fim de semana tranquilo. Ela só lê, é executada uma vez por toque, e o novo resultado substitui o anterior.

No máximo três sugestões ficam disponíveis por vez. Depois de uma semana de execuções bem-sucedidas, a rotina pergunta **Desativar o antigo job do OpenClaw?**. O job só será desativado se você tocar em **Desativar**. Você pode ativá-lo de novo no OpenClaw. **Manter** deixa os dois em execução.

## Com base no que você faz

Sua Machine também identifica trabalhos que você faz com frequência e os sugere como rotinas em **Sugerido**, mesmo que você não use o OpenClaw. Ela procura:

- a mesma solicitação três vezes seguidas ou mais, como "resuma os chamados de suporte em aberto" toda segunda-feira;
- um e-mail que você envia com frequência, como um relatório semanal para sua equipe;
- newsletters e e-mails de atualização que chegam toda semana;
- um canal movimentado do Slack em que outras pessoas escrevem toda semana;
- e-mails que você encaminha um a um para a mesma pessoa, como e-mails da escola e do clube para sua parceria. Um resumo semanal para essa pessoa evita que você precise encaminhar cada e-mail;
- a mesma solicitação que você responde com frequência, como uma aprovação mensal para a mesma pessoa.

Cada sugestão explica o que identificou, como "Solicitado 4 vezes seguidas" ou "6 e-mails encaminhados para Sam em 3 semanas", e já foi executada uma vez para você ver um resultado real. Pense em um resumo para a equipe, uma preparação para uma reunião semanal, um resumo de suporte ou desenvolvimento, um panorama dos seus números ou um resumo das newsletters que você recebe.

A rotina só sugere algo que seja específico para você e claramente útil: um resumo de notícias inclui apenas as suas newsletters, nunca notícias genéricas. Se nada for adequado, nenhuma sugestão será criada.

A rotina verifica isso no máximo uma vez por dia e traz no máximo uma nova sugestão por semana, sem enviar notificações. **Não, obrigado** impede que aquela sugestão apareça de novo. Os encaminhamentos e as respostas continuam na conta de onde foram enviados, então Trabalho e Pessoal não se misturam. Tudo fica na sua Machine. Uma tarefa que você conclui com frequência aparece como uma sugestão de tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma [tarefa recorrente](recurring.md) lembra você de fazer algo. Uma rotina é um trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para "pagar o aluguel no primeiro dia do mês" e uma rotina para "toda sexta-feira, me dizer quais oportunidades ficaram paradas".
