---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu sim. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 81b65d513aa5941b
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** agrupa tudo:

- **Feito agora**: no topo, uma última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema, foi concluída enquanto você estava longe. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e seu celular também avisa.
- **Para você**: tudo que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (o trabalho está pronto, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, você precisa decidir ou responder), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Aguardando outras pessoas**: tarefas recolhidas cuja próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e aquelas sem resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, começando pela mais recente e mostrando quando foram concluídas, como "Concluída há 5 minutos". Tarefas que parecem já estar concluídas recebem a marca **Parece feito**.

Depois que você envia algo, uma nota curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". **Abrir** leva você até a tarefa. A pesquisa encontra tarefas pelo título ou pela pessoa para quem foram enviadas, inclusive em Mais tarde e Feito.

Em **Para você**, primeiro aparecem as tarefas atrasadas ou com prazo até amanhã, depois as perguntas da sua Fleet, em seguida os acompanhamentos de um quadro e, por fim, o restante. Dentro de cada grupo, as mais recentes aparecem primeiro. A tarefa mantém o mesmo lugar enquanto sua Machine a prepara e quando é concluída. Só a marca muda. Nos outros grupos abertos, primeiro aparecem as tarefas atrasadas ou com prazo até amanhã, e depois as mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** quer dizer que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 mesclado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, ela é encerrada automaticamente, e você pode usar **Desfazer**. Uma tarefa que você já resolveu por conta própria, como respondendo no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que parece ser de alguém que você conhece, mas não é, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa avisa claramente: "Esta pessoa não é Sam Lee." Ela mostra a pessoa pelo endereço verdadeiro, nunca pelo nome que ela usou. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem trazer a tarefa de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte depois que o prazo passar. Ela também informa quem ainda precisa responder.

Quando uma tarefa depende de algo que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra isso em **Concluído quando**. Enviar a sua parte não encerra a tarefa. Ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou e, então, é encerrada automaticamente. Você pode usar **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como conclusão para mudar isso.

Se ninguém mexer em uma tarefa por uma semana, ela pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa. Você pode usar **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, a tarefa fica recolhida em Volta mais tarde, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, fazer uma edição, adiá-la ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto sem atividade e sem tarefas abertas pode receber uma tarefa com uma próxima etapa específica, no máximo três vezes por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa com a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, uma linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou só as de um tipo. Seu celular e computador mostram a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta a mostrar todas. Um alerta sobre a própria Machine, como uma parte que continua reiniciando, não é de Trabalho nem Pessoal, então aparece apenas em Todos.

A linha no topo da lista também leva direto à outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do resumo mais recente da manhã ou do fim do dia e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque na linha para ler o resumo de novo e use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele aparecerá em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua aberto, para Trabalho e Pessoal ou só para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto** em **Detalhes** permite trocar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área** em **Detalhes** move uma tarefa para a outra área. O que ela pode ler e enviar também muda com a tarefa. **Desfazer** na nota move a tarefa de volta.

Quando uma tarefa precisa da outra área para continuar e todas as mensagens relacionadas estão nela, a tarefa é movida para essa área automaticamente e continua. Caso contrário, ela mostra **Mover para Trabalho**, e nada é movido até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens relacionadas a ela. Quando precisa de outras mensagens da outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa, e uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada ao seu endereço de trabalho, é Pessoal desde o início.

O trabalho que chega a uma conta pessoal, como uma mensagem de um cliente pelo WhatsApp ou um pedido na sua caixa de entrada pessoal, é de Trabalho desde o início. Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a colocou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde. A resposta sempre vai para onde está a conversa, mesmo depois de uma mudança de área, a menos que você escolha outra forma.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho em que o e-mail chegou e nunca aparece em uma Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer** no cabeçalho de Para você mostra cada uma por vez, na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc para. Abaixo do título, o cabeçalho também informa quanto tempo elas levam no seu ritmo, como "cerca de 2 min".

Uma tarefa que faz uma pergunta para você não aparece nesse fluxo: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, de dia e de noite. Ela verifica as mensagens recebidas quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Boletins informativos, notificações e recibos entram na próxima verificação, em até uma hora.

À noite, das 00:00 às 06:30, as verificações ficam pausadas. As novas mensagens continuam sendo lidas e armazenadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Verificações, em Conexões, aparece "Pausadas durante a noite. Atualização às 06:30". Se você abrir o app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação na hora.

**Verificar agora** lê todas as fontes na hora. Se não houver tarefas abertas, toque na linha da sua Machine para ver o status e **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção aparece no topo no computador. Uma linha curta aparece ali apenas enquanto uma verificação está em andamento ou quando ela falha ou atrasa. Você também pode perguntar no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu novas mensagens, aparece uma linha acima das tarefas com o que ela encontrou em todas as fontes lidas, como "13 mensagens verificadas às 16:11 · nada precisa de você" ou "· 2 novas tarefas". Quando uma nova tarefa fica esperando por um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte, quem escreveu, o assunto ou as primeiras palavras e a nova tarefa ou o motivo de não precisar fazer nada. Por exemplo: "Você estava em cópia, outra pessoa da equipe está respondendo" ou "A reunião já está marcada para quinta-feira". Uma conversa não mostra o motivo se a verificação encontrou apenas um motivo vago. Toque em uma conversa para ler a mensagem.

As primeiras 10 aparecem na lista. Toque abaixo delas para ver o restante. O número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação no celular sobre uma mensagem que já aparece na lista é exibida apenas uma vez. A linha fica visível por 12 horas depois da verificação.

A contagem inclui apenas os e-mails enviados para você. Suas próprias respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails que The Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. Mensagens sobre cobrança, período de avaliação ou convite são lidas normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que deve ser alterado: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como feita** indica que a tarefa está resolvida. A opção fica visível em uma tarefa pronta sem rascunho ou, caso contrário, no topo de **…**, inclusive nas tarefas que precisam da sua decisão. A tarefa sai da lista na hora, e a mensagem mostra **Desfazer**. Deslize a mensagem para dispensá-la ou arraste-a para fora com o mouse para encerrá-la antes. A alteração é mantida.

Para fazer a tarefa de outro jeito, diga como no **Chat** dela.

Em **…**:

- **Passar…**: passe a tarefa para alguém da equipe, para [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta com uma frequência definida](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha um motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome** em **Detalhes** para renomear a tarefa. O título que você escolheu é mantido.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você responde.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento que aparecem na conta. Contas pagas automaticamente, como por débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior mostra que a conta foi paga, como uma confirmação de que o pagamento foi recebido, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só é importante até determinado horário, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / dispensado** com o status "Não é mais necessário". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou repasse para alguém aparecer como pronto, sua Machine verifica as conversas recentes com as pessoas envolvidas, inclusive os chats em grupo, e espera o Slack terminar de lê-las. Quando uma mensagem posterior mostra que a tarefa já foi resolvida, como quando alguém pediu algo e a pessoa respondeu que sim, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa que foi transferida para outro lugar ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda importa acompanha os novos planos. Uma tarefa sem mais nada a fazer vai para **Feito / dispensado** com o status "Não precisa". No chat dela aparece "Atualização:" com o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**, e informa que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão correspondente ou toca em ×.

No primeiro dia, o topo de Tarefas dá as boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo mostra de quem ou do que se trata, a organização quando houver uma relação com ela (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

O nome e a organização mostram a foto ou o logotipo, se houver um no Graph. Caso contrário, mostram as iniciais. Um logotipo que não fique legível nesse tamanho, como texto branco em fundo transparente ou um nome largo, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail. Nada desde então." Ela aparece quando a última interação com a pessoa já faz tempo ou ficou sem resposta, e indica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, **Conectar**, ao lado dele, abre essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com a forma como foi encerrada logo abaixo, como "Concluída: Sam assinou na terça-feira".

Acima do rascunho, uma linha discreta identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você saber de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho usa informações de outra conversa, como a sugestão de alguém da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas depois dela. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa vem marcada como "Esta tarefa" e abre na conversa. **Mostrar mensagens anteriores** exibe mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo dele.

Em **Detalhes**, um e-mail mostra apenas o que não aparece no cabeçalho, como endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver mais nada para mostrar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link da tarefa para a própria mensagem também abre a mensagem aqui, com **Abrir no Slack** na parte de baixo.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. Toque no título para abrir o chat. Uma tarefa concluída fica resumida, e a mensagem de origem aparece em **Detalhes**.

Uma tarefa que mostra "Aguardando" inclui um link para sua última mensagem para a pessoa, aquela cuja resposta você está esperando: "E-mail para Pat · ter.".

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, **+** no celular ou `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, ela vai para a área certa, de acordo com a pessoa e o assunto. A tarefa também encontra o e-mail ao qual dá continuidade, inclusive mensagens antigas.

- **Vence**: digite um dia ou horário, como "amanhã", "sex. que vem", "3 nov.", "14h" ou "daqui a 2 horas". Você também pode usar seu próprio idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta com uma frequência definida. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule as pessoas ou empresas relacionadas à tarefa, até 5.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa, como um e-mail, mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que The Machine tenha. Pesquise por texto ou remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, a câmera ao lado tira uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa usando um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho real.
