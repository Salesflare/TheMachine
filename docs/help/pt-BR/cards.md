---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 51db64e67403d2ea
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** agrupa tudo:

- **Feito agora**: no topo, mostra uma última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema, concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia. Seu celular também recebe uma notificação.
- **Para você**: tudo que está esperando por você, começando pelo mais urgente. Cada tarefa indica **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (ela precisa primeiro de uma decisão ou resposta sua; se o trabalho parou por algo que só você pode fornecer, como uma informação, um login ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não recebem novidades há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, começando pela mais recente, com o horário em que foram concluídas, como "Concluída há 5 minutos". Tarefas que parecem já ter sido concluídas aparecem com a indicação **Parece feito**.

Depois que você envia, uma nota curta mostra para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Volta mais tarde até seg.". Uma resposta que só promete fazer o trabalho, como "Vou enviar até terça-feira", mantém a tarefa aberta: "Enviado. Mantido em aberto." **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou por quem as recebeu, inclusive em Volta mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet, os follow-ups de um quadro e, por fim, o restante. Em cada grupo, a tarefa mais recente aparece primeiro. Uma tarefa continua no mesmo lugar enquanto sua Machine a prepara e quando é concluída: só a indicação muda. Nos outros grupos abertos, o que está atrasado ou vence até amanhã aparece primeiro, e o restante vem do mais recente para o mais antigo. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine identificou que a tarefa foi concluída, como "PR #3451 integrado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista e ajuda sua Machine a aprender com ela. Essas tarefas nunca aparecem como atrasadas. Quando essa indicação aparece em uma mensagem, a tarefa é encerrada automaticamente depois de um dia, e você pode usar **Desfazer**. Caso contrário, ela espera que você toque em **Concluir**. Uma tarefa que você já resolveu por conta própria, por exemplo respondendo no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa avisa claramente: "Esta pessoa não é Sam Lee." Ela identifica a pessoa pelo endereço de e-mail, nunca pelo nome que ela usou. Sua Machine confirma esse tipo de mensagem com a pessoa pelo endereço que você já tem, nunca com quem escreveu a mensagem.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até que uma nova mensagem a traga de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde naquele dia, ou na manhã seguinte se o prazo já tiver passado. Ela informa quem ainda precisa responder.

Quando a tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até que uma mensagem mostre o resultado. Então, é encerrada automaticamente, e você pode usar **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para alterar isso.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas novas apareçam primeiro depois de alguns dias fora. Não há novidades quando não chega nenhuma mensagem nova e você não faz nada na tarefa, como enviar uma mensagem no chat, editar ou adiar. Só abrir a tarefa não conta.

Tarefas urgentes, com vencimento próximo ou com um envio em andamento continuam em Para você. **Descartar tudo** marca todas as tarefas de Mais antigos como desnecessárias depois de uma confirmação, assim como **Não precisa** faz com uma tarefa por vez. Você pode usar **Desfazer**. Uma novidade faz a tarefa voltar para Para você.

Uma tarefa sem atividade por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, e você pode usar **Desfazer**. **Manter** mantém a tarefa e ela não pergunta de novo. Se você não responder durante mais uma semana, ela vai para Volta mais tarde, recolhida, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editá-la, adiá-la ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem tarefas abertas pode receber uma tarefa com uma próxima etapa específica. O limite é de três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e deixa a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhou ou está atrasada, a linha informa isso e mostra **Verificar agora**.

**Todos**, **Trabalho** e **Pessoal**, no topo da barra lateral, mostram todas as tarefas ou só as de um tipo. Seu celular e computador mostram a mesma seleção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta à lista completa. Um alerta sobre a própria Machine, como uma parte que reinicia sem parar, não é de Trabalho nem de Pessoal e aparece somente em Todos.

A linha no topo da lista também permite trocar direto para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do resumo mais recente, da manhã ou da noite, e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque na linha para ler o resumo novamente e use **Copiar** para colá-lo onde quiser. Depois que você abre o resumo ou toca no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, a linha mostra **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, para Trabalho e Pessoal ou só para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite alterar o projeto ou removê-lo. Veja [Tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para sua outra área. O acesso às mensagens que ela pode ler e enviar também muda. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar e todas as mensagens relacionadas já estão nela, a tarefa é movida automaticamente e segue adiante. Caso contrário, ela mostra **Mover para Trabalho**, e nada é movido até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando sua Machine identifica a área certa. Até lá, ela não aparece em Trabalho nem em Pessoal e permanece privada.

Uma tarefa sempre pode ler as mensagens que deram origem a ela. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa. Uma tarefa sobre sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega a uma conta pessoal, como um cliente no WhatsApp ou um pedido na sua caixa de e-mail pessoal, é de Trabalho desde o início. Uma tarefa que você mesmo moveu ou classificou sempre fica onde você colocou. Trabalho ou Pessoal define onde a tarefa aparece e com quem é compartilhada, nunca de onde ela responde: a resposta sempre vai para a conversa original, mesmo depois de uma mudança, a menos que você escolha outra forma.

Mesmo sendo Pessoal, essa tarefa responde pelo endereço de trabalho onde o e-mail chegou e nunca aparece em uma Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, mostra uma por vez na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc para. O cabeçalho informa quanto tempo elas levam no seu ritmo, como "cerca de 2 min".

No fim, a lista mostra quantas tarefas foram enviadas ou encerradas e quantas ainda estão sendo preparadas.

Uma tarefa que faz uma pergunta para você fica de fora das duas opções: ela espera sua resposta, não um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, de dia e de noite. Ela verifica o que chegou quando há 40 mensagens aguardando ou quando a mensagem mais antiga de alguém está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, entre 00:00 e 06:30, as verificações pausam: as mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a seção Verificações mostra "Pausadas durante a noite, serão retomadas às 06:30". Se você clicar, digitar ou rolar a tela no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas em aberto, toque na linha da sua Machine para ver o status e **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção fica no topo da tela no computador. Uma linha curta aparece ali somente enquanto uma verificação está em andamento ou quando uma falhou ou está atrasada. Você também pode pedir no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas mostra o que foi encontrado em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 tarefas novas". Ela se refere somente a essa verificação: as tarefas que já estavam na sua lista continuam aguardando como antes. Quando uma tarefa nova fica para um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa por e-mail, chat e notificação, com o ícone da fonte. Ela mostra quem escreveu, o assunto ou as primeiras palavras, além da nova tarefa ou do motivo para não criar uma, como "Você só estava em cópia; uma pessoa da equipe está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra motivo quando a verificação só encontrou um motivo vago. Toque em uma delas para ler.

As primeiras 10 aparecem de início. Toque abaixo delas para ver as demais. Um número depois de um nome, como (3), indica quantas mensagens novas há naquele chat. Uma notificação no celular sobre uma mensagem que já está na lista aparece uma vez só. A linha fica visível por 12 horas depois da verificação.

A contagem inclui somente e-mails enviados para você. Suas próprias respostas são lidas como contexto e para identificar promessas, mas não contam como e-mails novos. Os e-mails que The Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que deve ser alterado: como fazer a tarefa ou, quando um rascunho está pronto, o que mudar nele. **Concluir** indica que a tarefa foi resolvida. Essa opção aparece diretamente em tarefas prontas sem rascunho ou em tarefas que fazem uma pergunta. Nos outros casos, ela fica no topo do menu **…**. A tarefa sai da lista na hora, e a mensagem mostra **Desfazer**. Deslize a mensagem para longe ou arraste-a com o mouse para fechá-la antes. A alteração continua valendo.

Para fazer a tarefa de outro jeito, diga como no **Chat** dela. A resposta informa somente o que mudou, como o adiamento e até quando. Se não foi possível alterar alguma coisa, como a data de vencimento, ela avisa.

No menu **…**:

- **Passar…**: encaminhe para uma pessoa da equipe, [Claude Code ou Codex](hand-to-agent.md), ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta com uma frequência definida](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir no chat, por exemplo: "Mude o nome para…". O título escolhido permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece como nova na lista. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior indica que ela foi paga, como uma confirmação de recebimento enviada por quem cobrou, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só fazia sentido até determinado horário, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / descartado** com a indicação "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou repasse para outra pessoa aparecer como pronto, sua Machine verifica as conversas recentes que você teve com as pessoas envolvidas, inclusive em chats de grupo, e espera o Slack carregá-las. Se uma mensagem posterior mostrar que a tarefa já foi resolvida, por exemplo, porque alguém pediu algo e a outra pessoa aceitou, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escreveu na mesma conversa depois que o rascunho foi criado, **Enviar** pausa o envio e mostra: "Não enviado: há uma mensagem nova na conversa". A tarefa mostra essa mensagem com **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de local ou uma reserva cancelada, The Machine atualiza as tarefas por conta própria. Uma tarefa que continua sendo necessária acompanha os novos planos. Se não há mais nada a fazer, ela vai para **Feito / descartado** com a indicação "Não precisa", o chat explica o motivo depois de "Atualizado:" e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**. Ela também explica que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão ou toca em ×.

No seu primeiro dia, o topo da página Tarefas dá as boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo mostra de quem ou do que se trata, a organização quando houver uma relação com ela, o projeto, se é de Trabalho ou Pessoal e quando chegou. Toque em um nome para abrir a página da pessoa no Graph.

O nome e a organização mostram a foto ou o logotipo, se houver um no Graph. Caso contrário, mostram as iniciais. Se um logotipo não for legível em tamanho pequeno, como texto branco em fundo transparente ou uma marca muito larga, ele também dá lugar à inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias, por e-mail; nenhuma novidade desde então". Ela aparece quando a última conversa com a pessoa já faz tempo ou ainda não teve resposta. Também indica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha indica um canal que não está conectado, **Conectar**, ao lado dele, abre essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, e a linha abaixo explica como foi encerrada, como "Concluída: Sam assinou na terça-feira".

Acima do rascunho, uma linha discreta identifica a mensagem que deu origem à tarefa, com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você saber na hora se é uma resposta no Slack ou um e-mail.

Quando o rascunho leva em conta a contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Uma conversa no Slack, WhatsApp, Telegram, Intercom e outros serviços aparece em ordem cronológica, da mais antiga para a mais recente: primeiro, as mensagens anteriores à mensagem relacionada à tarefa e, depois, as respostas seguintes. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa vem marcada como "Esta tarefa" e aparece em destaque. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo dele.

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, ele abre no app Gmail, se você tiver o app.

**Detalhes** de um e-mail mostram somente o que não aparece no cabeçalho, como os endereços completos de Cc, Bcc ou um endereço de resposta diferente. Se não houver nada a acrescentar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link de uma tarefa para a própria mensagem também abre a mensagem aqui, com **Abrir no Slack** no fim.

**Detalhes** mostram o nome da tarefa, o projeto, a área (toque em uma opção para alterar), sua última anotação e o resultado de um agente de programação. Toque no título para abrir o chat. Uma tarefa concluída permanece compacta; a mensagem que deu origem a ela fica em **Detalhes**.

Uma tarefa com a indicação "Aguardando" inclui um link para sua última mensagem enviada à pessoa, aquela cuja resposta você está aguardando: "E-mail para Pat · ter.".

## Crie uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador, **+** no celular ou `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não selecionar **Trabalho** ou **Pessoal**, ela vai para a área certa conforme o assunto e as pessoas envolvidas. A tarefa também encontra o e-mail ao qual dá follow-up, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "sexta que vem", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone do calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta com uma frequência definida. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada, seja um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra que The Machine tenha. Pesquise pelo texto ou por quem enviou. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, use a câmera ao lado para tirar uma foto. Você pode anexar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa a partir de um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho real.
