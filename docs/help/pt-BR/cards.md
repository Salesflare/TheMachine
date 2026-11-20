---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para sua aprovação. Saiba o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 16f31364b3da3827
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, não importa quantas mensagens ele envolva.

## Onde ficam as tarefas

A página **Tarefas** reúne todas elas:

- **Feito agora**: no topo, fica a última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema. Ela foi concluída enquanto você estava fora. Continua ali até você tocar em **Entendi**, por no máximo um dia, e você também recebe uma notificação no celular.
- **Para você**: tudo que está esperando por você, em ordem de urgência. Cada tarefa indica **Preparada** (o trabalho está feito, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, você precisa decidir ou responder), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Consulte [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, da mais recente para a mais antiga, com o horário em que foram concluídas, como “Feita há 5 minutos”. Tarefas que parecem já estar concluídas recebem a indicação **Parece feito**.

Depois que você envia, uma nota curta informa para onde a tarefa foi, como “Enviado. Movido para Feito.” ou “Enviado. Movido para Volta mais tarde até seg.”. **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou pelo destinatário, inclusive em Volta mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet, as tarefas de acompanhamento de um quadro e, por fim, o restante. Em cada grupo, as mais recentes aparecem primeiro. A tarefa mantém o lugar enquanto sua Machine a prepara e quando é concluída. Só a indicação muda. Nos outros grupos abertos, o que está atrasado ou vence até amanhã aparece primeiro, e o restante vem em ordem da mais recente para a mais antiga. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine vê que a tarefa foi concluída, como “PR #3451 integrado”, mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, ela é encerrada automaticamente, e você pode usar **Desfazer**. Uma tarefa que você já resolveu por conta própria, como respondendo no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que só se parece com o de alguém que você conhece, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa informa isso claramente: “Esta pessoa não é Sam Lee.” Ela identifica a pessoa pelo endereço verdadeiro, nunca pelo nome que ela usou. Sua Machine verifica esse tipo de mensagem com a pessoa do endereço que você já conhece, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, indica a etapa em **Aguardando:**. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem fazê-la voltar. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo quando ele for mais tarde, ou na manhã seguinte se o prazo já tiver passado. Ela informa quem ainda precisa responder.

Quando uma tarefa depende de algo que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra isso em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem mostrar que o resultado chegou. Então, é encerrada automaticamente, e você pode usar **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para alterar isso.

Se ninguém mexer em uma tarefa por uma semana, ela pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, e você pode usar **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela fica recolhida em Volta mais tarde, e deixa de ser contada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nenhuma tarefa aberta pode ganhar uma tarefa com uma próxima etapa específica. São no máximo três por semana. Consulte [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa com a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhou ou está atrasada, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal**, no topo da barra lateral, mostram todas as tarefas ou só um tipo. Seu celular e computador mostram a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta à lista completa. Um alerta sobre a própria Machine, como uma parte que fica reiniciando, não é Trabalho nem Pessoal e só aparece em Todos.

A linha no topo da lista também leva direto à outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do último resumo da manhã ou do fim do dia e quantas tarefas ele incluiu, como **Resumo do fim do dia de ontem** · 12 feitas, 3 abertas. Toque na linha para ler o resumo novamente e use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, em Trabalho e Pessoal ou somente na opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite mudar o projeto ou remover a tarefa dele. Consulte [Tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para a outra área. O que ela pode ler e enviar também muda com ela. **Desfazer**, na mensagem, move a tarefa de volta.

Quando uma tarefa precisa ir para a outra área para continuar e todas as mensagens de origem estão nessa área, ela é movida para lá e continua automaticamente. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal é movida automaticamente quando encontra a área certa. Até lá, ela não aparece em Trabalho nem em Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa. Uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada ao seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega por uma conta pessoal, como uma mensagem de um cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é Trabalho desde o início. Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a deixou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança de área, a menos que você escolha outro jeito.

Mesmo sendo Pessoal, uma tarefa assim ainda responde pelo endereço de trabalho que recebeu o e-mail. Ela nunca aparece em uma Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando por você, **Percorrer**, no cabeçalho de Para você, passa por elas uma de cada vez, na ordem da lista, com cada rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. Abaixo do título, o cabeçalho também informa quanto tempo elas levam no seu ritmo, como “cerca de 2 min”.

Uma tarefa que faz uma pergunta para você não entra nessa opção: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações ficam pausadas: as mensagens novas continuam sendo lidas e armazenadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Verificações, em Conexões, aparece “Pausadas durante a noite. As mensagens serão verificadas às 06:30”. Se você clicar, digitar ou rolar o app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam a acontecer normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação na hora.

**Verificar agora** lê todas as fontes na hora. Se não houver tarefas abertas, toque na linha da sua Machine para ver a opção, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção fica no topo da tela no computador. Uma linha curta aparece ali somente enquanto uma verificação está em andamento ou quando uma falhou ou está atrasada. Você também pode pedir no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que encontrou em cada fonte consultada, como “13 mensagens verificadas às 16:11 · nada precisa de você” ou “· 2 tarefas novas”. Quando uma tarefa nova fica esperando um momento melhor, como o resumo da manhã, a linha informa até quando: “1 tarefa aguardando até amanhã, às 08:30”.

Toque na linha para ver cada conversa por e-mail, chat e notificação, com o ícone do serviço de origem: quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo para não criar uma, como “Você estava em cópia, uma pessoa da equipe está respondendo” ou “Reunião já marcada para quinta-feira”. Uma conversa não mostra o motivo se a verificação encontrou apenas um motivo vago. Toque em uma conversa para ler a mensagem.

As 10 primeiras aparecem de início. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas há naquele chat. Uma notificação no celular sobre uma mensagem que já está na lista aparece uma só vez. A linha fica visível por 12 horas depois da verificação.

A contagem inclui somente e-mails enviados para você. Suas próprias respostas são lidas para dar contexto e identificar promessas, mas não contam como novos e-mails. Os e-mails que a própria Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem aparecem na lista. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Consulte [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que deve ser alterado: como fazer ou, quando um rascunho está pronto, o que mudar nele. **Marcar como feita** indica que a tarefa foi resolvida. Ela aparece em uma tarefa pronta sem rascunho; nos outros casos, fica no topo de **…**, inclusive em tarefas que precisam da sua decisão. A tarefa sai da lista na hora, e uma mensagem mostra **Desfazer**. Dispense a mensagem com um gesto ou arraste-a para fora com o mouse para fechá-la antes. A alteração continua valendo.

Para fazer de outro jeito, diga isso no **Chat** da tarefa.

Em **…**:

- **Passar…**: encaminhe a tarefa para alguém da equipe, para [Claude Code ou Codex](hand-to-agent.md), ou [peça para alguém revisar](ask-to-review.md).
- **Repetir…**: a tarefa [volta periodicamente](recurring.md).
- **Não é relevante**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. O título que você escolher será mantido.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece como nova na lista. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como por débito automático ou cartão cadastrado, não viram tarefas. Se um e-mail posterior indicar que a conta foi paga, como uma confirmação de recebimento do pagamento, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até um horário definido, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / dispensado** com a indicação “Não é mais necessário”. **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de um repasse para alguém aparecer como pronto, sua Machine verifica as conversas recentes com as pessoas envolvidas, inclusive conversas em grupo, e espera o Slack terminar de lê-las. Se uma mensagem posterior mostrar que a tarefa já foi resolvida, como quando alguém foi consultado e disse que sim, ela é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa transferida para outro local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda importa acompanha os novos planos. Se não há mais nada a fazer, ela vai para **Feito / dispensado** com a indicação “Não precisa”. No chat, aparece “Atualizado:” com o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as principais ações: **Pedir mudanças** e **Não precisa**, e explica que nada é enviado antes de você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão ou toca em ×.

No seu primeiro dia, uma mensagem de boas-vindas aparece no topo de Tarefas e informa quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem ou do que se trata, a organização quando o assunto for uma organização (não apenas porque alguém trabalha nela), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Nomes e organizações mostram a foto ou o logotipo quando há um no Graph. Caso contrário, mostram as iniciais. Se um logotipo não puder ser lido em tamanho pequeno, como um logotipo branco em fundo transparente ou um nome comprido, ele também é substituído pela inicial.

Às vezes, uma linha discreta informa o que não se sabe, como “Último contato há 12 dias por e-mail; nada desde então”. Ela aparece quando a última conversa com a pessoa é antiga ou não teve resposta, e indica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, **Conectar**, ao lado dele, abre essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como foi encerrada, como “Feita: Sam assinou na terça-feira”.

Acima do rascunho, uma linha discreta identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como “Com base na mensagem de Sam em #ops”. Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) mostra uma conversa única, da mensagem mais antiga à mais recente: as mensagens anteriores àquela de que a tarefa trata e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa vem marcada como “Esta tarefa” e abre em destaque. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo da mensagem.

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, abre o app Gmail se você tiver o app instalado.

**Detalhes** de um e-mail mostra somente o que não aparece no cabeçalho, como os endereços completos de Cc, Bcc ou um endereço diferente para respostas. Se não houver nada a acrescentar, a opção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link da tarefa para a mensagem original também abre a mensagem aqui, com **Abrir no Slack** na parte inferior.

**Detalhes** mostra o nome, o projeto e a área (toque em um deles para alterar), sua última observação e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída permanece compacta; a mensagem de origem fica em **Detalhes**.

Uma tarefa em “Aguardando” inclui um link para a última mensagem que você enviou à pessoa, aquela cuja resposta você espera: “E-mail para Pat · ter.”

## Criar uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador, **+** no celular ou `N`) cria uma tarefa para qualquer assunto. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, ela vai para a área adequada, de acordo com quem e com o que se trata. A tarefa também encontra o e-mail relacionado, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como “amanhã”, “sexta que vem”, “3 nov”, “14h” ou “daqui a 2 horas”. Você também pode escrever no seu idioma. O ícone do calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta periodicamente. Consulte [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa, seja um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou outro serviço de mensagens que The Machine tenha. Pesquise por texto ou remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, a câmera ao lado tira uma foto. Você pode adicionar até 5 arquivos, como no chat (consulte [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: The Machine preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
