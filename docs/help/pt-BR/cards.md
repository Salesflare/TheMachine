---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que significa cada parte de uma tarefa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e7e5d78b3291e556
---
Sua Machine lê tudo o que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo:

- **Feito agora**: no topo, uma última etapa que você confirmou, como um formulário ou uma issue, foi concluída enquanto você estava ausente. Ela fica lá até você tocar em **Entendi**, por no máximo um dia, e também aparece no seu celular.
- **Para você**: tudo o que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, ela precisa da sua decisão ou resposta; quando o trabalho parou em algo que só você tem, como uma informação, um login ou uma escolha, uma linha abaixo do título diz o quê), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigas**: tarefas recolhidas sem nada novo há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, começando pela mais recente, com o horário em que foram concluídas, como "Concluída há 5 minutos". Tarefas que parecem já estar concluídas aparecem como **Parece feito**.

Depois que você envia algo, uma nota curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Depois até seg.". Uma resposta que só promete o trabalho, como "Envio até terça", mantém a tarefa aberta: "Enviado. Mantida aberta." **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou por quem as recebeu, inclusive em Depois e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas do seu Fleet, em seguida os follow-ups de um quadro e, por fim, o restante. Em cada grupo, as mais recentes aparecem primeiro. A tarefa mantém o lugar enquanto sua Machine a prepara e quando ela é concluída: só o status muda. Nos outros grupos abertos, o que está atrasado ou vence até amanhã aparece primeiro, e o restante vem por ordem de chegada, começando pelo mais recente. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 merged", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, ela é encerrada automaticamente, com a opção **Desfazer**. Uma tarefa que você já resolveu por conta própria, como respondendo no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que só parece pertencer a alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa deixa isso claro: "Esta pessoa não é Sam Lee." Ela mostra a pessoa pelo próprio endereço, nunca pelo nome que ela usou. Sua Machine verifica esse tipo de mensagem com a pessoa no endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, indica a etapa em **Aguardando:**. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você envia uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio prazo se ele for mais tarde hoje, ou na manhã seguinte se o prazo já tiver passado. Ela informa quem ainda está sendo aguardado.

Quando a tarefa depende de algo que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra isso em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Depois, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para mudar isso.

Uma tarefa sem nada novo há uma semana sai de Para você e vai para **Mais antigas**, para que as novas apareçam primeiro depois de alguns dias fora. Nada novo significa nenhuma mensagem nova sobre ela e nada que você tenha feito nela, como uma mensagem no chat, uma edição ou um adiamento. Só olhar não conta.

As urgentes, as que vencem em breve e as que têm um envio a caminho ficam em Para você. **Descartar todas** marca todas as tarefas de Mais antigas como desnecessárias depois de uma confirmação, como **Não precisa** faz uma a uma, com **Desfazer**. Qualquer novidade em uma delas a traz de volta para Para você.

Uma tarefa que ninguém mexeu por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela fica recolhida em Volta mais tarde, e deixa de ser contabilizada no ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar ou adiar a tarefa, ou receber uma nova mensagem, faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nenhuma tarefa aberta pode receber uma tarefa com uma próxima etapa específica. No máximo, são três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e a lista fica vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou apenas um tipo. Seu celular e computador mantêm a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta para a lista completa. Um alerta sobre a própria Machine, como uma parte que fica reiniciando, não é Trabalho nem Pessoal e aparece apenas em Todos.

A linha no topo da lista também leva direto à outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do último resumo da manhã ou do fim do dia e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque nela para ler o resumo novamente. Use **Copiar** para colar em qualquer lugar. Depois que você abre o resumo ou toca no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, em Trabalho e Pessoal ou apenas na opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto** em **Detalhes** permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área** em **Detalhes** move uma tarefa para sua outra área. O que ela pode ler e enviar também muda. **Desfazer** na mensagem move a tarefa de volta.

Quando uma tarefa precisa ir para sua outra área e todas as mensagens relacionadas estão lá, ela é movida e continua automaticamente. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando sua Machine encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e fica privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Um e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outras empresas suas vão para as tarefas daquela empresa. Uma tarefa sobre a sua vida pessoal, como uma mensagem de um familiar para o seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega por uma conta pessoal, como uma mensagem de um cliente no WhatsApp ou um pedido no seu e-mail pessoal, é Trabalho desde o início. Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a deixou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca de onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança, a menos que você escolha outra forma.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho em que o e-mail chegou e nunca aparece em um Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer** no cabeçalho de Para você mostra uma de cada vez, na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. Abaixo do título, o cabeçalho também informa quanto tempo isso leva no seu ritmo, como "cerca de 2 min".

Uma tarefa que faz uma pergunta para você não entra nessa lista: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica as mensagens recebidas quando há 40 mensagens aguardando ou quando a mensagem mais antiga de uma pessoa está aguardando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, no máximo dentro de uma hora.

À noite, entre 00:00 e 06:30, as verificações ficam pausadas: as mensagens novas continuam sendo lidas e guardadas. Todas são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a opção Verificações informa: "Pausadas durante a noite. As mensagens serão verificadas às 06:30". Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para ver a opção, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção fica no topo da lista no computador. Uma linha curta aparece ali apenas enquanto uma verificação está em andamento ou quando ela falha ou atrasa. Você também pode pedir no chat.

LinkedIn, X e Salesflare têm seu próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que foi encontrado em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nada precisa de você" ou "· 2 novas tarefas". Quando uma nova tarefa fica aguardando o momento certo, como o resumo da manhã, a linha informa até quando: "1 tarefa aguardando até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone do serviço de origem: quem escreveu, o assunto ou as primeiras palavras, e a tarefa criada ou o motivo para não criar uma, como "Você estava em cópia, um colega está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo se a verificação deu apenas uma explicação vaga. Toque em uma delas para ler.

As primeiras 10 aparecem na lista. Toque abaixo delas para ver as demais. Um número depois de um nome, como (3), indica quantas mensagens novas há naquele chat. Uma notificação no celular sobre uma mensagem que já está na lista aparece apenas uma vez. A linha fica visível por 12 horas após a verificação.

A contagem inclui apenas os e-mails enviados para você. Suas próprias respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails da própria The Machine, como o resumo da manhã ou um aviso de correção, nunca são lidos nem aparecem na lista. E-mails sobre cobrança, seu período de teste ou um convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** indica o que mudar: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como feita** significa que a tarefa foi resolvida: essa opção aparece em uma tarefa pronta sem rascunho ou, nos outros casos, no topo de **…**, inclusive nas tarefas que precisam da sua decisão. A tarefa sai da lista na hora, e a mensagem mostra **Desfazer**. Deslize a mensagem para removê-la ou arraste-a para fora com o mouse para encerrar a tarefa antes. A mudança continua valendo.

Para resolver a tarefa de outra forma, diga isso no **Chat**.

Em **…**:

- **Passar…**: passe a tarefa para um colega, [Claude Code ou Codex](hand-to-agent.md), ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta de acordo com uma frequência](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome** em **Detalhes** para mudar o nome da tarefa. Você também pode pedir isso no chat, por exemplo: "Mude o nome para…". O título escolhido por você não muda.

**Reabrir** traz uma tarefa encerrada de volta. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece na lista como nova. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, o vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como as de débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior informa que ela foi paga, como uma confirmação do remetente, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só fazia sentido até um horário determinado, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / descartado** com o status "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de um repasse para alguém aparecer como pronto, sua Machine verifica as conversas recentes com as pessoas envolvidas, inclusive chats em grupo, e espera o Slack terminar de lê-las. Se uma mensagem posterior mostrar que a tarefa já foi resolvida, como um pedido seguido de um sim, ela é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa transferida para outro local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda for necessária acompanha os novos planos. Se não houver mais nada a fazer, ela vai para **Feito / descartado** com o status "Não precisa". O chat informa "Atualizado:" e o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**, além de avisar que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão ou toca em ×.

No seu primeiro dia, uma mensagem de boas-vindas aparece no topo de Tarefas e informa quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro, para ficar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem se trata, a organização quando o assunto envolve uma (não apenas porque a pessoa trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Os nomes e as organizações mostram uma foto ou um logotipo quando o Graph tem um. Caso contrário, mostram as iniciais. Se um logotipo não ficar legível nesse tamanho, como um logo branco em fundo transparente ou uma marca horizontal com palavras, as iniciais também aparecem.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail; sem novidades desde então." Ela aparece quando a última conversa com a pessoa é antiga ou não teve resposta, e cita canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, toque em Conectar ao lado dele para abrir a conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como terminou, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem de origem, com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho leva em conta a opinião de alguém em outro lugar, como a sugestão de um colega no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa única, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa é identificada como "Esta tarefa" e abre a conversa nessa mensagem. **Mostrar mensagens anteriores** exibe mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo dele.

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, o e-mail abre no app Gmail, se você tiver o app instalado.

Em **Detalhes**, um e-mail mostra apenas as informações que não aparecem no cabeçalho, como endereços completos em Cc, Bcc ou um endereço de resposta diferente. Se não houver nada a acrescentar, a seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link da tarefa para a mensagem original também a abre aqui, com **Abrir no Slack** na parte inferior.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para mudar), sua última observação e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída aparece de forma resumida. A mensagem que deu origem a ela fica em **Detalhes**.

Uma tarefa com status "Aguardando" tem um link para sua última mensagem enviada à pessoa, aquela cuja resposta você espera: "E-mail para Pat · ter.".

## Crie uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador, **+** no celular ou `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, ela vai para a área certa de acordo com quem e com o que ela envolve. Ela também encontra o e-mail relacionado, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "próxima sex.", "3 nov.", "14h" ou "daqui a 2 horas". Você também pode escrever no seu idioma. O ícone do calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta de acordo com uma frequência. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa. Pode ser um e-mail, mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que The Machine tenha. Pesquise por texto ou remetente. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou solte arquivos no formulário. No celular, use a câmera ao lado para tirar uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho real.
