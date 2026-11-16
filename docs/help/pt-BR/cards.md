---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 6cbbad37c4dfaf07
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde as tarefas ficam

A página **Tarefas** organiza as tarefas:

- **Feito agora**: no topo, aparece uma última etapa que você confirmou, como um formulário ou problema resolvido enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e também aparece no seu celular.
- **Para você**: tudo que está esperando você, começando pelo mais urgente. Cada tarefa aparece como **Preparada** (o trabalho está feito, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, você precisa decidir ou responder), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, começando pela mais recente, com o horário em que foram concluídas, como “Feita há 5 minutos”. As tarefas que parecem já concluídas aparecem como **Parece feito**.

Depois que você envia, uma nota curta mostra para onde a tarefa foi, como “Enviado. Movida para Feito.” ou “Enviado. Movida para Mais tarde até seg.”. **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou por quem as recebeu, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet, os acompanhamentos de um quadro e, por fim, o restante. Dentro de cada grupo, as tarefas aparecem começando pelas mais recentes. A tarefa mantém seu lugar enquanto sua Machine a prepara e quando é concluída: só o status muda. Nos outros grupos abertos, primeiro aparecem as tarefas atrasadas ou que vencem até amanhã, e depois as mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine vê que a tarefa foi concluída, como “PR #3451 integrado”, mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, ela é encerrada automaticamente, com a opção **Desfazer**. Uma tarefa que você já resolveu por conta própria, por exemplo, respondendo no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa informa isso claramente: “Esta pessoa não é Sam Lee.” Ela mostra o remetente pelo endereço de e-mail, nunca pelo nome que ele usou. Sua Machine verifica esse tipo de mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte se o prazo já tiver passado. Ela informa quem ainda precisa responder.

Quando uma tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com **Escreva um lembrete curto** no chat dela. Diga no chat o que conta como concluído para alterar isso.

Se ninguém mexer em uma tarefa por uma semana, ela pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela fica recolhida em Volta mais tarde, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar ou adiar a tarefa, ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nada em aberto pode receber uma tarefa com uma próxima etapa específica, até três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine fica em repouso e a lista fica vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou só um tipo. Seu celular e computador mostram a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta para a lista completa. Um alerta sobre sua própria Machine, como uma parte que fica reiniciando, não é Trabalho nem Pessoal e aparece somente em Todos.

A linha no topo da lista também leva diretamente à outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do seu último resumo da manhã ou do fim do dia e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque para ler o resumo novamente. Use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua em aberto, em Trabalho e Pessoal ou apenas na opção que você filtrou.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. Em **Detalhes**, **Projeto** permite alterar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

Em **Detalhes**, **Área** move uma tarefa para sua outra área. O que ela pode ler e enviar também muda com ela. **Desfazer** na nota move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar e todas as mensagens relacionadas estão nela, a tarefa é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada é movido até você tocar nessa opção. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal é movida automaticamente quando encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens relacionadas a ela. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa, e uma tarefa sobre sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um trabalho que chega a uma conta pessoal, como uma mensagem de cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é Trabalho desde o início. Uma tarefa que você mesmo moveu ou criou em uma área permanece onde você a colocou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca de onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança, a menos que você escolha outra opção.

Mesmo uma tarefa Pessoal desse tipo responde pelo endereço de trabalho que recebeu o e-mail e nunca aparece em uma Fleet de Trabalho ou no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, passa por elas uma de cada vez, na ordem da lista, mostrando o rascunho completo de cada uma, com **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. Abaixo do título, o cabeçalho também informa quanto tempo elas levam no seu ritmo, como “cerca de 2 min”.

Uma tarefa que faz uma pergunta para você fica de fora das duas opções: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de alguém está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, da meia-noite às 06:30, as verificações são pausadas: as mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30. Assim, suas tarefas ficam prontas antes do resumo da manhã. Em **Conexões**, a opção Verificações informa: “Pausadas durante a noite. Serão retomadas às 06:30”. Se você clicar, digitar ou rolar a tela no app, escrever no chat ou tocar em uma tarefa à noite, as verificações são retomadas normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação imediata.

**Verificar agora** lê todas as fontes imediatamente. Se não houver nada em aberto, toque na linha da sua Machine para vê-la, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção aparece no topo da lista no computador. Uma linha curta aparece ali somente enquanto uma verificação está em andamento ou quando ela falha ou atrasa. Você também pode pedir isso no chat.

LinkedIn, X e Salesflare seguem seu próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que foi encontrado em todas as fontes lidas, como “13 mensagens verificadas às 16:11 · nada precisa de você” ou “· 2 novas tarefas”. Quando uma nova tarefa fica esperando o momento certo, como o resumo da manhã, a linha informa até quando: “1 tarefa aguardando até amanhã às 08:30”.

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo de não precisar de nada, como “Você só estava em cópia, outra pessoa da equipe está respondendo” ou “Reunião já marcada para quinta-feira”. Uma conversa não mostra o motivo quando a verificação encontrou apenas um motivo vago. Toque em uma conversa para ler.

As 10 primeiras aparecem, e um toque abaixo delas mostra o restante. Um número depois do nome, como (3), indica quantas mensagens novas esse chat tem. Uma notificação no celular sobre uma mensagem que já está na lista aparece apenas uma vez. A linha fica disponível por 12 horas após a verificação.

A contagem inclui somente os e-mails enviados para você. Suas próprias respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails que The Machine envia para você, como o resumo da manhã ou um aviso sobre uma correção, nunca são lidos nem listados. E-mails sobre cobrança, período de avaliação ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** permite dizer o que mudar: como fazer a tarefa ou, depois que um rascunho estiver pronto, o que mudar nele. **Marcar como feita** indica que a tarefa foi resolvida: aparece à vista em uma tarefa pronta sem rascunho; nos outros casos, fica no topo de **…**, inclusive em uma tarefa que precisa da sua decisão. A tarefa sai da lista na hora, e a mensagem mostra **Desfazer**. Deslize para dispensar a mensagem ou arraste-a para fora com o mouse para fechá-la mais rápido. A alteração continua valendo.

Para fazer de outro jeito, diga como no **Chat** da tarefa.

Em **…**:

- **Passar…**: passe a tarefa para alguém da equipe, para [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta com certa frequência](recurring.md).
- **Não é relevante**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. O título que você escolher permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você mesmo responde.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, o prazo de vencimento e os dados de pagamento que aparecem na conta. Contas pagas automaticamente, como um débito automático ou um cartão salvo, não viram tarefas. Quando um e-mail posterior informa que ela foi paga, por exemplo, quando o remetente confirma que recebeu o pagamento, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só é importante até um horário específico, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / dispensado** com o status “Não precisa mais”. **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou repasse para alguém aparecer como pronto, sua Machine verifica as conversas recentes com as pessoas envolvidas, inclusive conversas em grupo, e aguarda o Slack terminar de lê-las. Quando uma mensagem posterior mostra que a tarefa já foi resolvida, por exemplo, porque alguém pediu e recebeu uma confirmação, ela é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda é necessária segue o novo plano. Uma tarefa sem nada a fazer vai para **Feito / dispensado** com o status “Não precisa”. No chat, aparece “Atualização:” com o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as ações principais: **Pedir mudanças** e **Não é relevante**, além de informar que nada é enviado até você tocar em **Enviar**. A dica desaparece para sempre quando você usa o botão ou toca em ×.

No seu primeiro dia, o topo de Tarefas dá as boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é o primeiro rascunho, para ficar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem se trata, a organização quando ela for relevante (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

O nome e a organização mostram uma foto ou um logo, se houver no Graph, ou as iniciais. Se um logo não ficar legível nesse tamanho, como texto branco em fundo transparente ou uma marca horizontal, as iniciais também aparecem.

Às vezes, uma linha discreta informa o que não se sabe, como “Último contato há 12 dias por e-mail; nada desde então”. Ela aparece quando a última conversa com a pessoa é antiga ou não teve resposta, e indica os canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha indica um canal que não está conectado, a opção Conectar ao lado abre essa conexão.

O título diz o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como terminou, por exemplo, “Concluída: Sam assinou na terça-feira”.

Acima do rascunho, uma linha discreta identifica a mensagem de origem, com o logo do serviço. Toque nela para ler a conversa. O rascunho mostra o logo do serviço para o qual será enviado, para você saber de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, por exemplo, “Com base na mensagem de Sam em #ops”. Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) mostra uma conversa inteira, da mensagem mais antiga à mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa aparece marcada como “Esta tarefa” e é aberta na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo dele.

Em **Detalhes**, um e-mail mostra apenas o que não aparece no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver mais nada para mostrar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a mensagem também abre a mensagem aqui, com **Abrir no Slack** na parte inferior.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída permanece compacta; a mensagem de origem fica em **Detalhes**.

Uma tarefa com status “Aguardando” inclui um link para sua última mensagem para a pessoa, aquela pela qual você está esperando: “E-mail para Pat · ter”.

## Crie uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador, em **+** no celular ou por `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, ela vai para a área certa, com base em quem e no que se trata. Ela também encontra o e-mail relacionado, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como “amanhã”, “próxima sex.”, “3 nov.”, “14h” ou “daqui a 2 horas”, inclusive no seu idioma. O ícone do calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta com certa frequência. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa, como um e-mail ou uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra que The Machine tenha. Pesquise pelo texto ou pelo remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, a câmera ao lado tira uma foto. Você pode anexar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam anexados à tarefa, e The Machine os lê ao trabalhar nela. Só os arquivos já bastam: The Machine preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho real.
