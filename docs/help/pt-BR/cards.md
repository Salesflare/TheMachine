---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 84b8879d98f26aa2
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo assim:

- **Feito agora**: no topo, uma última etapa que você confirmou, como um formulário ou problema, foi concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e você também recebe uma notificação no celular.
- **Para você**: tudo que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (o trabalho está pronto, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, você precisa decidir ou responder), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigas**: tarefas recolhidas que não recebem novidades há uma semana (mais abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (mais abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta para **Ainda precisa?** (mais abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, da mais recente para a mais antiga, com o horário em que foram concluídas, como "Concluída há 5 minutos". Tarefas que parecem já estar concluídas aparecem como **Parece feito**.

Depois que você envia, uma nota curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". Se a resposta só promete que o trabalho será feito, como "Vou enviar até terça-feira", a tarefa continua aberta: "Enviado. Mantido em aberto." **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou pela pessoa para quem foram enviadas, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet, em seguida os acompanhamentos de um quadro e, por fim, o restante. Dentro de cada grupo, as tarefas mais recentes aparecem primeiro. Uma tarefa não muda de lugar enquanto sua Machine a prepara nem quando é concluída. Só o status muda. Nos outros grupos abertos, o que está atrasado ou vence até amanhã aparece primeiro, e o restante vem da tarefa mais recente para a mais antiga. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine vê que a tarefa foi concluída, como "PR #3451 mesclada", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, elas são encerradas automaticamente, com a opção **Desfazer**. Uma tarefa que você já resolveu por conta própria, como ao responder no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que só parece pertencer a alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa avisa isso claramente: "Esta pessoa não é Sam Lee." Ela mostra a pessoa pelo endereço de e-mail, nunca pelo nome que ela usou. Sua Machine confirma a mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo vale depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte se o prazo já tiver passado. Ela informa de quem ainda está esperando.

Quando uma tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem confirmar o resultado. Então, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar, ela volta com a opção **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para alterar isso.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigas**, para que as tarefas recentes apareçam primeiro quando você voltar depois de alguns dias. Não há novidades quando não chega nenhuma mensagem nova e você não faz nada na tarefa, como enviar uma mensagem no chat, editar ou adiar. Só olhar a tarefa não conta.

Tarefas urgentes, com prazo próximo ou com um envio a caminho continuam em Para você. **Descartar tudo** marca todas as tarefas de Mais antigas como não necessárias, depois de uma confirmação. O mesmo acontece ao marcar cada uma como **Não precisa**, com a opção **Desfazer**. Se uma delas receber algo novo, volta para Para você.

Uma tarefa que ninguém tocou por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela é recolhida em Volta mais tarde, e deixa de ser contada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nada em aberto pode receber uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e deixa a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, a mensagem informa isso e mostra **Verificar agora**.

**Todos**, **Trabalho** e **Pessoal**, no topo da barra lateral, mostram todas as tarefas ou só um tipo. No celular e no computador, a seleção é a mesma. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta a mostrar tudo. Um alerta sobre a própria Machine, como uma parte que fica reiniciando, não é de Trabalho nem Pessoal e só aparece em Todos.

A mensagem no topo da lista também permite mudar direto para outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o resumo mais recente da manhã ou da noite e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque nela para ler o resumo novamente. Use **Copiar** para colar onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua em aberto, em Trabalho e Pessoal, ou só na opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. Em **Detalhes**, a opção **Projeto** permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

Em **Detalhes**, **Área** move a tarefa para a outra área. O acesso às mensagens que ela pode ler e enviar também muda. A opção **Desfazer** na nota a leva de volta.

Quando uma tarefa precisa da outra área para continuar e todas as mensagens de que ela depende estão lá, ela é movida e continua automaticamente. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas daquela empresa, e uma tarefa sobre a sua vida pessoal, como uma mensagem da família para o seu endereço de trabalho, começa como Pessoal.

Um assunto de trabalho que chega a uma conta pessoal, como uma mensagem de um cliente no WhatsApp ou um pedido na sua caixa de e-mail pessoal, começa como Trabalho. Uma tarefa que você mesmo moveu ou criou em uma área fica onde você a colocou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança de área, a menos que você escolha outro caminho.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho que recebeu o e-mail e nunca aparece em uma Fleet de Trabalho nem no Team Graph.

Quando há duas ou mais tarefas esperando por você, **Percorrer**, no cabeçalho de Para você, passa por elas uma de cada vez, na ordem da lista. Cada rascunho aparece completo, com as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. Abaixo do título, o cabeçalho também informa quanto tempo elas levam no seu ritmo, como "cerca de 2 min".

Uma tarefa que faz uma pergunta fica fora dessa opção: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, em até uma hora.

À noite, entre 00:00 e 06:30, as verificações pausam: as novas mensagens continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, as verificações mostram "Pausadas durante a noite, retomam às 06:30". Se você clicar, digitar ou rolar a tela no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam a acontecer normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre faz a verificação na mesma hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas em aberto, toque na linha da sua Machine para vê-la, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção fica no topo da lista no computador. Uma mensagem curta aparece ali somente enquanto uma verificação está em andamento ou quando falha ou atrasa. Você também pode pedir no chat.

LinkedIn, X e Salesflare mantêm o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que encontrou em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nada precisa de você" ou "· 2 novas tarefas". Quando uma tarefa nova fica aguardando um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa aguardando até amanhã às 08:30".

Toque na linha para ver cada conversa por e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras, e a tarefa criada ou o motivo para não precisar de uma, como "Você estava só em cópia, uma pessoa da equipe está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação só encontrou um motivo vago. Toque em uma delas para ler.

As 10 primeiras aparecem de cara. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação no celular sobre uma mensagem que já está na lista aparece só uma vez. A linha fica disponível por 12 horas depois da verificação.

A contagem inclui apenas os e-mails enviados para você. Suas respostas são lidas para entender o contexto e as promessas, mas não contam como e-mails novos. Os e-mails que sua Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, seu período de teste ou um convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** permite dizer o que mudar: como fazer a tarefa ou, quando um rascunho já está pronto, o que mudar nele. **Marcar como feito** indica que a tarefa foi resolvida. Em tarefas prontas sem rascunho, a opção fica visível; nos outros casos, fica no topo do **…**, inclusive nas tarefas que precisam da sua decisão. A tarefa sai da lista na mesma hora, e a mensagem mostra a opção **Desfazer**. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para encerrá-la mais rápido. A alteração continua valendo.

Para fazer de outro jeito, diga como no **Chat** da tarefa.

Em **…**:

- **Passar…**: passe a tarefa para uma pessoa da equipe, para [Claude Code ou Codex](hand-to-agent.md), ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta em intervalos regulares](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir no chat, por exemplo: "Renomeie para…". O título escolhido continua valendo.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece na lista como nova. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar, em qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como um débito automático ou uma cobrança no cartão cadastrado, não viram tarefas. Quando um e-mail posterior confirma o pagamento, como uma mensagem do remetente confirmando que recebeu, a tarefa é encerrada automaticamente. **Desfazer** a traz de volta por um dia.

Uma tarefa que só era necessária até um horário específico, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / dispensado** como "Não precisa mais". **Desfazer** a traz de volta por um dia.

Antes que uma mensagem ou um repasse para alguém apareça como pronto, sua Machine confere seus chats recentes com as pessoas envolvidas, incluindo chats em grupo, e aguarda o Slack ler as mensagens. Quando uma mensagem posterior mostra que a tarefa já foi resolvida, como quando alguém foi consultado e respondeu que sim, ela é encerrada automaticamente. **Desfazer** a traz de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de lugar ou uma reserva cancelada, The Machine atualiza as tarefas por conta própria. Uma tarefa que ainda importa acompanha os novos planos. Uma tarefa sem nada a fazer vai para **Feito / dispensado** como "Não precisa", e o chat mostra "Atualizado:" seguido do motivo. **Desfazer** a traz de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**, e avisa que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão correspondente ou toca em ×.

No seu primeiro dia, uma mensagem no topo de Tarefas dá as boas-vindas e informa quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem se trata, a organização, quando houver uma (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Um nome ou uma organização mostra a foto ou o logotipo quando o Graph tem um. Caso contrário, mostra as iniciais. Um logotipo difícil de ler nesse tamanho, como um logo branco em fundo transparente ou uma marca com palavras compridas, também aparece como inicial.

Às vezes, uma mensagem discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail; nada desde então". Ela aparece quando já faz tempo desde a última conversa ou quando uma mensagem ficou sem resposta, e cita canais que não estão conectados, como o WhatsApp. Sua Machine diz o que não sabe em vez de tentar adivinhar.

Quando a mensagem cita um canal que não está conectado, toque em **Conectar** ao lado dela para abrir essa conexão.

O título diz o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com uma indicação de como terminou abaixo, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do serviço para onde será enviado, para você ver logo se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha avisa, como "Com base em Sam no #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa só, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas depois dela. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa aparece marcada como "Esta tarefa" e abre direto na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo dele.

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, abre no app Gmail se você tiver o app instalado.

Em **Detalhes**, um e-mail mostra apenas o que não aparece no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver nada a acrescentar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link da tarefa para a própria mensagem também abre a mensagem aqui, com **Abrir no Slack** na parte de baixo.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para mudar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída aparece resumida. A mensagem de origem fica em **Detalhes**.

Uma tarefa que está "Aguardando" mostra um link para sua última mensagem para a outra pessoa, aquela pela qual está esperando: "E-mail para Pat · ter.".

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, em **+** no celular ou em `N`) cria uma tarefa para qualquer coisa. Criar a tarefa não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, ela vai para a área certa, conforme a pessoa e o assunto. A tarefa também encontra o e-mail relacionado, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "sex. que vem", "3 nov.", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta em intervalos regulares. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada, como um e-mail, mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra que The Machine tenha. Pesquise pelo texto ou pelo remetente. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, a câmera ao lado tira uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Você pode adicionar só arquivos: The Machine preenche a tarefa a partir de um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
