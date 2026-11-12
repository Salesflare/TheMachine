---
title: Rotinas
area: cards
summary: Trabalho que sua Machine faz sozinha, num ritmo, como um resumo de segunda-feira dos seus deals abertos. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays
---
## Criar uma

Abra **Rotinas** na barra lateral e diga numa linha o que ela deve fazer e quando: "toda segunda às 9, resuma meus deals abertos" ou "todo dia útil de manhã, liste os e-mails que ainda devo responder". Depois **Adicionar**.

Sem horário, ela roda às 8:00. O horário é o do relógio da sua Machine.

## Modelos

Em **Modelos**, no fim de Rotinas, **Adicionar** liga uma rotina pronta. Ela roda uma vez na hora e depois toda manhã às 7:30 (Limpeza de spam a cada hora). O cartão dela mostra as palavras como qualquer rotina, e **Editar** muda as palavras ou o nome.

Quando chegam muitas newsletters e a Limpeza de newsletters está desligada (25 ou mais numa semana, de pelo menos 5 remetentes), uma linha acima dos seus to-dos diz quantas chegaram e o que ela faria, com **Ativar** e **Não, obrigado**.

A Limpeza de spam é oferecida do mesmo jeito quando 5 ou mais e-mails foram movidos para o spam à mão numa semana. **Ativar** a adiciona como **Adicionar** aqui. Depois de **Não, obrigado** ela não é oferecida de novo, e um modelo que você já teve nunca é.

**Limpeza de newsletters** cria uma tarefa por área (trabalho e pessoal) com as newsletters do último dia, cada uma com **Manter** ou **Cancelar inscrição**. O cancelamento usa o link de um clique da lista, ou o e-mail de cancelamento a partir do seu endereço se o envio estiver ligado. Se não, mostra **Abrir página de cancelamento**.

Recibos, pedidos e avisos de pagamento ficam de fora. Um e-mail que chega por um endereço de grupo, como um Google Group, aparece sob quem o escreveu e nunca cancela sua inscrição no grupo.

**Limpeza de spam** cria uma tarefa por área com e-mails de remetentes desconhecidos que parecem spam, cada um com **Spam** ou **Não é spam**. O Outlook move o spam para Lixo eletrônico e o Gmail marca como spam. Ela verifica a cada hora, então o spam costuma estar lá antes de você chegar nele. Spam novo vai para a mesma tarefa enquanto ela estiver aberta.

Só funciona com e-mails que a The Machine pode mover. O Gmail conectado só para leitura, como numa Machine hospedada, não pode: o modelo diz isso no lugar de **Adicionar**. O Outlook funciona.

Desconhecido quer dizer que você nunca escreveu para a pessoa, e um “Re:” só conta como conversa numa conversa em que você escreveu. Se e-mail de um remetente que você marcou como spam, na tarefa ou na sua caixa, passar de novo, ele aparece na próxima tarefa como **Já marcado como spam**. O que você mesmo moveu para o spam também ajuda a reconhecer e-mails parecidos.

Nada muda até você confirmar na tarefa. Toque num remetente para ler o e-mail antes: ele continua não lido e nada muda. Na Limpeza de spam, as imagens da web não carregam, então o remetente não vê que ele foi aberto. Remetentes já decididos não voltam. Um dia sem newsletters nem spam não cria tarefa, e essas tarefas nunca enviam notificação.

**Resumo diário** escolhe uma vez por dia as poucas matérias das suas newsletters que valem seu tempo, em uma tarefa. Cada uma diz em uma linha por que importa para você. Toque para ler o e-mail, ou use **Abrir no seu e-mail**. Só newsletters: nunca e-mails de pessoas, recibos ou remetentes que você cancelou, e nunca o que você já leu. Quando nada se destaca, não há tarefa.

Ele aprende o que importa para você pelo que você abre, marca com estrela ou arquiva sem ler, e por **Mais assim** e **Menos assim** em cada matéria. Os assuntos pelos quais ele escolhe ficam no cartão da rotina em **Mais de** e **Menos de**. Remova um com ×, ou adicione os seus. Os tracejados ele aprendeu sozinho. Um novo resumo substitui o que está aberto, e ele nunca envia uma notificação.

Ele lê só o remetente, o assunto e o começo de cada newsletter nova, e faz uma pergunta curta à sua IA sobre elas, com um limite diário, para continuar barato. **Mudar quando** define o horário. Se você mudar as palavras, ele roda como qualquer rotina com as suas palavras.

**Aniversários** cria uma tarefa para cada contato próximo que faz aniversário hoje: pessoas para quem você mesmo escreve, como amigos, família e contatos frequentes. Cada uma traz uma mensagem curta escrita onde vocês costumam conversar, como o chat do WhatsApp ou sua conversa por e-mail, no idioma da pessoa. Ela só sai quando você envia. Um dia sem aniversários não cria tarefa.

Os aniversários vêm das suas agendas (os aniversários e a agenda Aniversários do Google, lidos toda manhã mesmo sem sincronizar, e a agenda Aniversários do Outlook), dos seus contatos do Google numa Machine auto-hospedada e de um campo de data chamado Aniversário numa pessoa do Graph. Se nenhuma delas tiver um aniversário ainda, o resultado diz **Ainda não há aniversários** e como adicionar.

**Importar aniversários do Facebook**: com Aniversários ligado, uma tarefa oferece ler a página de aniversários do Facebook. Toque em **Importar** e a The Machine a abre no navegador dela, rola até todos os meses carregarem e lê o nome e o aniversário de cada amigo. Ela mostra quantos encontrou e quem corresponde por nome e sobrenome a pessoas do seu Graph. Um nome que mais de uma pessoa tem é ignorado e listado.

Só **Salvar** os guarda, na página de cada pessoa: o aniversário e, para quem ainda não tem foto, a foto de perfil do Facebook. Um aniversário ou uma foto que você informou lá continua, e uma foto que a pessoa já tem nunca é substituída. Nada é escrito no Facebook.

Ela nunca lê de novo sozinha: quem faz isso é **Importar de novo** na tarefa. O navegador precisa estar conectado ao Facebook. Se não estiver, toque em **Entrar em Facebook** na tarefa e entre lá; depois ela lê a página sozinha. A The Machine nunca entra por você.

Amigos que ninguém no seu Graph tem são contados, com alguns nomes. **Adicionar … como contatos pessoais** adiciona todos de uma vez, também depois de Salvar: cada um com nome e aniversário, nunca compartilhado com uma Work Fleet. Um nome que alguém do seu Graph já tem, ou que tinha alguém que você excluiu de vez, é pulado. Os lembretes de aniversário continuam vindo só para pessoas para quem você escreve.

**Desfazer** na tarefa remove exatamente essas pessoas, também depois de **Importar de novo**.

Enquanto as palavras forem as do modelo, ela roda com código próprio, sem o seu plano de IA (Limpeza de spam primeiro lista por código os e-mails novos de remetentes desconhecidos, e só faz uma pergunta curta à sua IA quando há algum). Um nome novo não muda isso. Se você mudar as palavras, ela roda como qualquer rotina com as suas palavras.

Limpeza de newsletters e Limpeza de spam continuam terminando na mesma tarefa com uma escolha por e-mail. Aniversários editado dá o resultado e no máximo um rascunho, não uma tarefa por pessoa. **Voltar ao modelo** em **Editar** devolve as palavras.

## O que uma rotina faz

Na hora marcada, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e coloca o resultado na página Rotinas. Cada resultado diz **Para revisar**, **Nada de novo** (com o porquê) ou **Não funcionou** (com o porquê). Uma execução que termina sem resultado conta como uma que não funcionou, nunca como feita.

Rotinas só leem: suas mensagens, páginas da web, o GitHub e sites como o X no navegador. Elas não enviam, respondem, publicam nem mudam nada. Só um modelo muda e-mails, e só o que você confirma na tarefa dele.

Quando a tarefa de uma rotina termina num post ou numa mensagem, ela faz tudo até essa etapa e mostra o rascunho, como **Postaria no X:**. Depois de uma execução real, você recebe como tarefa para aprovar; uma execução de teste só mostra. O nome diz do que se trata e para onde vai, o botão diz a etapa, como **Publicar**, e **Da sua rotina** embaixo abre a rotina.

A tarefa começa na área da conta de onde sai, como Trabalho para a conta do X da sua empresa, então nunca pede para mudar.

Cada execução conhece o último resultado, então pode dizer o que mudou desde então.

Depois de uma boa execução, sua Machine pode escrever para si uma receita para a leitura que é igual toda vez, como quais e-mails ou mudanças no GitHub olhar. As próximas execuções leem isso primeiro, em código simples, e a IA só escolhe o que importa e escreve, com menos tokens. Uma receita só lê; se parar de funcionar, a execução lê por conta própria e a conserta. Ela aparece em **Avançado: etapas de script** no menu ⋯.

## Dias perdidos

Se sua Machine estava desligada ou ocupada, as execuções perdidas não se acumulam: só a mais recente roda, uma vez. Cada data roda uma vez, mesmo depois de reiniciar.

As rotinas rodam uma de cada vez e esperam quando o uso do seu plano de IA está baixo, como todo o trabalho em segundo plano. **Rodar agora** roda na hora.

## Mudar ou parar

Fica no menu ⋯ da rotina. **Mudar quando** aceita um novo ritmo com suas próprias palavras, como "todo dia útil às 8". **Pausar** para as execuções até **Retomar**; o que foi perdido durante a pausa não roda depois. **Parar** encerra uma rotina de vez.

Quando você usa **Pedir mudanças** em uma tarefa de uma rotina, ou escreve no chat dela, e sua nota vale para toda execução, como "nunca use emoji", a tarefa oferece **Mudar também a rotina**, na tarefa e no chat dela, abaixo da resposta. Ela mostra o que muda nas palavras da rotina, e a rotina só muda quando você toca em **Mudar**. **Deixar como está** a deixa como está. Uma correção só desse rascunho não oferece nada.

## Avançado: etapas de script

Você nunca precisa de um script: diga com suas palavras o que uma rotina deve fazer.

Para usuários avançados, uma rotina também pode rodar seus próprios comandos na sua Machine: no menu ⋯, escolha **Avançado: etapas de script**. **Editar** só as mostra se uma rotina já tiver. **Buscar dados** roda primeiro um comando, na pasta dele (vazia: sua pasta pessoal) e no máximo pelos segundos dele. O que ele imprime vai para a execução trabalhar. Sem palavras, o que ele imprime é o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se terminar com erro, a execução mostra **Não funcionou** com o que a verificação disse. Um comando de Buscar dados que falha aparece do mesmo jeito.

Um comando é uma linha e roda sem shell: sem pipes nem variáveis. As etapas de script são suas, definidas só no seu painel. Uma execução de teste e **Testar** também rodam Buscar dados e avisam; continuam sem enviar nem guardar nada. Uma rotina nunca envia, então uma etapa de script deve só ler.

## Dos seus jobs do OpenClaw

Se você criou jobs agendados no OpenClaw antes, sua Machine os lê (ela nunca os muda) e oferece os que servem como rotinas em **Sugerido**. Cada um rodou uma vez, para você ver um resultado real.

Ela mantém suas correções no job e deixa de fora o que ele enviava ou publicava. Um job que rodava um script, ou lia o que um job de script coletava, traz isso como Buscar dados. **Adicionar** transforma em rotina, **Não, obrigado** nunca mais pergunta sobre esse job. Um job que lembrava você de fazer algo chega como oferta de tarefa recorrente em Tarefas.

Antes de adicionar uma sugestão, **Editar** e **Mudar quando** no menu ⋯ dela a mudam como qualquer rotina. **Rodar de novo** a executa agora com as palavras atuais, para ver resultados mais novos, por exemplo depois de um fim de semana tranquilo. Ela só lê, roda uma vez por toque e o novo resultado substitui o anterior.

No máximo três sugestões esperam ao mesmo tempo. Depois de uma semana de boas execuções, a rotina pergunta **Desativar o antigo job do OpenClaw?** Ele só é desativado quando você toca em **Desativar**, e você pode reativá-lo no OpenClaw.

## Do que você faz

Sua Machine também percebe trabalho que você faz num ritmo e o oferece como rotina em **Sugerido**, mesmo sem OpenClaw. Ela procura:

- o mesmo pedido, três vezes ou mais seguidas, como "resuma os tickets de suporte abertos" toda segunda;
- um e-mail que você envia num ritmo, como um relatório semanal para sua equipe;
- newsletters e e-mails de novidades que chegam toda semana;
- um canal do Slack movimentado onde outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como os da escola e do clube para quem divide a casa com você: um resumo semanal para essa pessoa poupa os encaminhamentos;
- o mesmo pedido que você responde num ritmo, como uma aprovação mensal para a mesma pessoa.

Cada sugestão diz o que viu, como "Pedido 4 vezes seguidas" ou "6 emails encaminhados para Sam em 3 semanas", e rodou uma vez para você ver um resultado real. Pense num resumo da equipe, um briefing antes de uma call semanal, um resumo de suporte ou de desenvolvimento, o pulso dos seus números ou um resumo das newsletters que você recebe.

Ela só sugere o que é seu e claramente útil: um resumo de notícias só das suas próprias newsletters, nunca um genérico. Quando nada serve, não há sugestão.

Ela olha no máximo uma vez por dia e traz no máximo uma sugestão nova por semana, sem notificação. **Não, obrigado** nunca a traz de volta. Encaminhamentos e respostas ficam com a conta de onde saíram, para que Trabalho e Pessoal não se misturem. Tudo fica na sua Machine. Uma tarefa que você fecha num ritmo chega como oferta de tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma tarefa recorrente (recurring.md) lembra você de fazer algo. Uma rotina é trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para "pagar o aluguel no dia 1", e uma rotina para "toda sexta, diga quais deals ficaram parados".
