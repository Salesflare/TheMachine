---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para você aprovar. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: baa6b797e040a271
---
Sua Machine lê tudo o que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo assim:

- **Feito agora**: no topo, uma última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema, foi concluída enquanto você estava longe. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e seu celular também recebe um aviso.
- **Para você**: tudo o que está esperando por você, começando pelo mais urgente. Cada tarefa indica **Preparada** (o trabalho está pronto, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, ela precisa da sua decisão ou resposta), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, começando pela mais recente, com o horário da conclusão, como "Feito há 5 minutos". Tarefas que parecem concluídas já aparecem como **Parece feito**.

Depois que você envia algo, uma nota curta diz para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". **Abrir** leva você até ela. A busca encontra tarefas pelo título ou por quem as recebeu, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet, em seguida os acompanhamentos de um quadro e, por fim, o restante. Dentro de cada grupo, a tarefa mais recente vem primeiro. Ela mantém a posição enquanto sua Machine a prepara e depois de concluída: só o marcador muda. Nos outros grupos abertos, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, e depois as mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como em "PR #3451 foi mesclado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista e ajuda sua Machine a aprender. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, elas são encerradas automaticamente, e você pode usar **Desfazer**. Uma tarefa que você já resolveu por conta própria, como respondendo no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa deixa isso claro: "Esta pessoa não é Sam Lee." Ela mostra a pessoa pelo endereço verdadeiro, nunca pelo nome que ela usou. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem a enviou.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, indica a etapa com **Aguardando:**. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte se o prazo já tiver passado. Ela também informa de quem ainda está aguardando uma resposta.

Quando uma tarefa depende de algo que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra essa condição em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, é encerrada automaticamente, e você pode usar **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com **Escreva um lembrete curto** no chat. Para mudar o que conta como concluído, explique no chat.

Uma tarefa que ninguém tocou por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, e você pode usar **Desfazer**. **Manter** mantém a tarefa, que não pergunta de novo. Se você não responder por mais uma semana, ela fica recolhida em Volta mais tarde, e deixa de ser contabilizada no ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar ou adiar a tarefa, ou receber uma nova mensagem, faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem tarefas em aberto pode receber uma tarefa com uma próxima etapa específica, até três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e deixa a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhou ou está atrasada, a linha informa isso e mostra **Verificar agora**.

Os filtros **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou apenas um tipo. No celular e no computador, a seleção é a mesma. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta a exibir tudo. Um alerta sobre a própria Machine, como uma peça que reinicia sem parar, não é de Trabalho nem Pessoal e aparece apenas em Todos.

A linha no topo da lista também leva direto ao outro filtro: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o título do seu último resumo da manhã ou da noite e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque nela para ler o resumo de novo. Use **Copiar** para colar o texto onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua em aberto, em Trabalho e Pessoal ou apenas no filtro selecionado.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para a sua outra área. O acesso às mensagens que ela pode ler e enviar também muda. **Desfazer** na nota move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar e todas as mensagens relacionadas já estão nela, a tarefa é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens que deram origem a ela. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa. Uma tarefa sobre a sua vida pessoal, como uma mensagem da família para o seu endereço de trabalho, é Pessoal desde o início.

O trabalho que chega a uma conta pessoal, como uma mensagem de um cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é Trabalho desde o início. Uma tarefa que você mesmo moveu ou colocou em uma área permanece nela. Trabalho ou Pessoal define onde a tarefa aparece e com quem ela é compartilhada, nunca para onde ela envia respostas: a resposta sempre vai para a conversa, mesmo depois de uma mudança de área, a menos que você escolha outra forma.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho que recebeu o e-mail e nunca aparece em uma Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, percorre cada uma na ordem da lista, mostrando o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc encerra. Abaixo do título, o cabeçalho também informa quanto tempo elas levam no seu ritmo, como "cerca de 2 min".

Uma tarefa que faz uma pergunta para você não entra nessa sequência: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, em até uma hora.

À noite, entre 00:00 e 06:30, as verificações ficam pausadas: as mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Verificações, em **Conexões**, aparece "Pausadas durante a noite. Atualização às 06:30". Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam a acontecer normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas em aberto, toque na linha da sua Machine para ver o status e **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção fica no topo da tela no computador. Uma linha curta aparece ali somente durante uma verificação ou quando uma falha ou atraso é detectado. Você também pode pedir isso no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas mostra o que ela encontrou em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nada precisa de você" ou "· 2 novas tarefas". Quando uma nova tarefa fica esperando o momento certo, como o resumo da manhã, a linha informa até quando: "1 tarefa aguardando até amanhã, às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação com o ícone da fonte. Você verá quem escreveu, o assunto ou as primeiras palavras e a nova tarefa ou o motivo de não precisar fazer nada, como "Você estava em cópia; uma pessoa da equipe está respondendo" ou "A reunião já está marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação encontrou apenas uma explicação vaga. Toque em uma conversa para ler a mensagem.

As primeiras 10 aparecem na lista. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação no celular sobre uma mensagem que já está na lista aparece uma vez só. A linha fica visível por 12 horas depois da verificação.

A contagem inclui apenas e-mails enviados para você. Suas próprias respostas são lidas para dar contexto e identificar promessas, mas não contam como novos e-mails. Os e-mails enviados pela The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de avaliação ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** permite dizer o que precisa mudar: como a tarefa deve ser feita ou, quando o rascunho estiver pronto, o que mudar nele. **Marcar como feita** indica que a tarefa foi resolvida. A opção fica visível em uma tarefa pronta sem rascunho. Nos outros casos, aparece no topo de **…**, inclusive em tarefas que precisam da sua decisão. A tarefa sai da lista na hora, e você pode usar **Desfazer** na mensagem. Para encerrá-la mais rápido, deslize a mensagem para o lado ou arraste-a para fora com o mouse. A alteração permanece.

Para fazer a tarefa de outra forma, explique no **Chat**.

Em **…**:

- **Passar…**: encaminhe a tarefa para alguém da equipe, para [Claude Code ou Codex](hand-to-agent.md), ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta periodicamente](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. O título que você escolher permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você responde.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, o vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como por débito automático ou com um cartão cadastrado, não viram tarefas. Quando um e-mail posterior informa que a conta foi paga, como uma confirmação do remetente, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até um horário definido, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / dispensado** com o status "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de um repasse aparecer como pronto, sua Machine verifica as conversas recentes com as pessoas envolvidas, inclusive chats em grupo, e espera o Slack terminar de lê-las. Quando uma mensagem posterior mostra que o assunto já foi resolvido, como quando alguém pediu algo e recebeu uma resposta positiva, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de lugar ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Se a tarefa ainda for necessária, ela acompanha os novos planos. Se não houver mais nada a fazer, ela vai para **Feito / dispensado** com o status "Não precisa", e o chat informa "Atualizado:" e o motivo. **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as principais ações: **Pedir mudanças** e **Não precisa**. Ela também explica que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão correspondente ou toca em ×.

No seu primeiro dia, o topo da página Tarefas dá boas-vindas e informa quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro, para já estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo mostra de quem se trata, a organização quando o assunto envolve uma (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Os nomes e as organizações mostram a foto ou o logotipo, se houver um no Graph; caso contrário, mostram as iniciais. Um logotipo que não ficaria legível nesse tamanho, como texto branco em fundo transparente ou uma marca muito larga, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail; nenhuma mensagem desde então". Ela aparece quando a última conversa com a pessoa é antiga ou ainda não teve resposta, e indica canais que não estão conectados, como o WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha indica um canal que não está conectado, **Conectar**, ao lado dele, abre essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com o desfecho abaixo, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem que deu origem à tarefa e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do serviço para onde será enviado, para você ver de cara se é uma resposta no Slack ou um e-mail.

Quando o rascunho considera a contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) mostra uma conversa completa, da mensagem mais antiga à mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa aparece marcada como "Esta tarefa" e fica aberta na conversa. **Mostrar mensagens anteriores** exibe mensagens mais antigas. Em uma conversa por e-mail, o restante da conversa aparece recolhido acima e abaixo da mensagem.

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, ele abre no app Gmail, se você tiver o app instalado.

Em **Detalhes**, um e-mail mostra apenas o que não aparece no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver mais nada para mostrar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a mensagem relacionada abre essa mensagem aqui também, com **Abrir no Slack** na parte de baixo.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para mudar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída aparece de forma resumida; a mensagem que deu origem a ela fica em **Detalhes**.

Uma tarefa com status "Aguardando" tem um link para a sua última mensagem enviada à pessoa, aquela cuja resposta você está esperando: "E-mail para Pat · ter".

## Crie uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador, em **+** no celular ou com `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não selecionar **Trabalho** nem **Pessoal**, ela vai para a área certa com base em quem e no que está relacionado. Ela também encontra o e-mail ao qual dá continuidade, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "sex. que vem", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone de calendário tem opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta periodicamente. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa, como um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que The Machine tenha. Pesquise por texto ou remetente. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode anexar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam anexados à tarefa e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
