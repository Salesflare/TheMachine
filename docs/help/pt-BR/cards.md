---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para sua aprovação. Veja o que significa cada parte de uma tarefa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e1656daff6fc566a
---
Sua Machine lê tudo o que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, não importa quantas mensagens ele envolva.

## Onde ficam as tarefas

A página **Tarefas** agrupa as tarefas:

- **Feito agora**: no topo, mostra uma última etapa que você confirmou, como um formulário ou problema, concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia. Seu celular também recebe uma notificação.
- **Para você**: tudo o que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (primeiro, você precisa decidir ou responder; quando o trabalho não pode continuar ou ser usado sem algo que só você tem, como um preço, uma informação ou uma escolha, uma linha abaixo do título diz o que falta), **Preparando…** (sua Machine está trabalhando na tarefa) ou **Para ler** (um resumo ou briefing, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não tiveram novidades por uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas cuja próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e as que ficaram sem resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, da mais recente para a mais antiga, com o horário em que foram concluídas, como "Concluída há 5 minutos". Tarefas que parecem concluídas já aparecem como **Parece feito**.

Depois que você envia algo, uma nota curta diz para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". Uma resposta que só promete fazer o trabalho, como "Vou enviar até terça-feira", mantém a tarefa aberta: "Enviado. Mantido em aberto." **Abrir** leva você até a tarefa. A pesquisa encontra tarefas pelo título ou por quem as recebeu, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por fim, o restante. Em cada grupo, as tarefas aparecem da mais recente para a mais antiga. Uma tarefa mantém sua posição enquanto sua Machine a prepara e quando é concluída: só o indicador muda. Nos outros grupos abertos, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã; as demais vêm da mais recente para a mais antiga. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 foi mesclado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem mostra que a tarefa foi concluída, ela é encerrada automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, ela espera você tocar em **Marcar como feito**. Uma tarefa que você já resolveu por conta própria, por exemplo, respondendo no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa avisa claramente: "Esta pessoa não é Sam Lee." Ela identifica a pessoa pelo próprio endereço, nunca pelo nome que ela usou. Sua Machine verifica a mensagem com a pessoa do endereço que você já conhece, nunca com quem a escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo vale depois que você responde com uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for hoje, ou na manhã seguinte quando o prazo já passou. Ela informa de quem ainda está aguardando uma resposta.

Quando a tarefa depende de um resultado que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra **Concluído quando**. Enviar sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem mostrar o resultado e, então, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para alterar isso.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as novas apareçam primeiro depois de alguns dias sem entrar. Não há novidades quando não chega nenhuma mensagem nova e você não faz nada na tarefa, como mandar uma mensagem no chat, editar ou adiar. Só visualizar não conta.

Tarefas urgentes, que vencem em breve ou que têm um envio em andamento continuam em Para você. **Descartar tudo** marca todas as tarefas de Mais antigos como desnecessárias depois de uma única confirmação, como **Não precisa** faz com uma tarefa por vez, com a opção **Desfazer**. Se uma delas tiver alguma novidade, ela volta para Para você.

Uma tarefa sem nenhuma interação por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela é recolhida em Volta mais tarde, e deixa de contar no número do ícone do app e no resumo da manhã. Abrir a tarefa, mandar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem tarefas abertas pode receber uma tarefa com uma próxima etapa específica. No máximo, três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa com a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou só um tipo. Seu celular e computador mostram a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta para todas as tarefas. Um alerta sobre a própria Machine, como uma parte que fica reiniciando, não é de Trabalho nem Pessoal e aparece somente em Todos.

A linha no topo da lista também permite mudar diretamente para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do último resumo da manhã ou da noite e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque nela para ler o resumo de novo. Use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está aberto, para Trabalho e Pessoal ou apenas para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque no nome para abrir o projeto. **Projeto**, em **Detalhes**, permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para sua outra área. O que ela pode ler e enviar também muda de área. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar e todas as mensagens de origem estão lá, ela muda de área e continua automaticamente. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa criada por você sem selecionar Trabalho ou Pessoal muda de área automaticamente quando descobre a qual pertence. Até lá, ela não aparece como Trabalho nem Pessoal e fica privada.

Uma tarefa sempre pode ler as mensagens de origem. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho marcada como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa. Já uma tarefa sobre sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega a uma conta pessoal, como uma mensagem de um cliente no WhatsApp, um pedido na sua caixa de entrada pessoal ou uma [promessa](promises.md) sobre trabalho, é de Trabalho desde o início.

Uma tarefa que você moveu ou classificou por conta própria sempre fica onde você a colocou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca o endereço para o qual ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança, a menos que você escolha outra opção.

Mesmo sendo Pessoal, essa tarefa responde pelo endereço de trabalho que recebeu o e-mail e nunca aparece em um Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, passa por elas uma de cada vez, na ordem da lista. Cada rascunho aparece completo, com as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo isso leva no seu ritmo, como "cerca de 2 min".

No final, ele conta o que foi enviado ou encerrado e o que ainda está sendo preparado.

Uma tarefa que faz uma pergunta fica de fora das duas opções: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de alguém está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações são pausadas. As mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a seção Verificações diz "Pausadas durante a noite. Tudo será verificado às 06:30". Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa à noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para ver a opção **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção fica no topo da tela no computador. Uma linha curta só aparece enquanto uma verificação está em andamento ou quando ela falhou ou atrasou. Você também pode perguntar no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que foi encontrado em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 tarefas novas". Ela se refere somente àquela verificação: as tarefas que já estavam na sua lista continuam como estão. Quando uma tarefa nova fica esperando um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras e a tarefa nova ou o motivo para não criar uma, como "Você estava em cópia. Uma pessoa da equipe está respondendo" ou "A reunião já está marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação encontrou apenas um motivo vago. Toque em uma delas para ler a mensagem e o que foi dito ao redor dela.

As 10 primeiras aparecem na lista. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação no celular sobre uma mensagem que já está na lista aparece uma só vez. A linha fica visível por 12 horas após a verificação.

A contagem inclui somente e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails da The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** permite dizer o que alterar: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como feito** indica que a tarefa foi resolvida. A opção aparece à vista em tarefas prontas sem rascunho ou que fazem uma pergunta. Nas demais, fica no topo de **…**. A tarefa sai da lista imediatamente, com a opção **Desfazer** na mensagem. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para encerrá-la mais rápido. A alteração fica salva.

Para que a tarefa seja feita de outra forma, diga como no **Chat** dela. A resposta informa somente o que mudou, como o adiamento e até quando. Se algo não puder ser alterado, como o prazo, ela avisa.

Em **…**:

- **Passar…**: encaminhe a tarefa para alguém da equipe, [Claude Code ou Codex](hand-to-agent.md), ou [peça para alguém revisar](ask-to-review.md).
- **Repetir…**: a tarefa [volta periodicamente](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, como em "Mude o nome para…". Seu título permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece como nova na lista. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, o prazo e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou um cartão cadastrado, não viram tarefas. Se um e-mail posterior mostrar que a conta foi paga, como uma confirmação do remetente de que o pagamento foi recebido, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só era relevante até determinado horário, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / descartado** como "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou repasse para alguém aparecer como pronto, sua Machine verifica as conversas recentes com as pessoas envolvidas, inclusive conversas em grupo, e espera o Slack terminar de lê-las. Se uma mensagem posterior mostrar que a tarefa já foi concluída, como quando alguém recebe um pedido e responde que sim, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escrever na mesma conversa depois que o rascunho for criado, **Enviar** fica bloqueado: "Não enviado: há uma nova mensagem na conversa". A tarefa mostra essa mensagem com as opções **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa transferida para outro local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda é necessária acompanha o novo plano. Uma tarefa que não tem mais nada a fazer vai para **Feito / descartado** como "Não precisa", e o chat informa "Atualizado:" e o motivo. **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais ações: **Pedir mudanças** e **Não precisa**. Ela também explica que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão ou toca em ×.

No seu primeiro dia, o topo de Tarefas dá as boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa a pessoa a quem ela se refere, a organização quando o assunto for sobre uma (não apenas porque alguém trabalha nela), o projeto, Trabalho ou Pessoal e quando a mensagem chegou. Toque em um nome para abrir a página dessa pessoa no Graph.

Os nomes e as organizações mostram uma foto ou um logotipo, se houver um no Graph, ou as iniciais. Um logotipo que não dê para ler em tamanho pequeno, como um texto branco em fundo transparente ou uma marca muito larga, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail. Nada desde então." Ela aparece quando a última conversa com a pessoa é antiga ou não teve resposta e identifica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, a opção Conectar ao lado dele abre essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com a forma como foi encerrada logo abaixo, como "Concluída: Sam assinou na terça-feira".

Acima do rascunho, uma linha discreta identifica a mensagem de origem com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você saber de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho depende da contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem. Ela desaparece quando uma atualização substitui o rascunho.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma só conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens ficam à direita, como no app. A mensagem da tarefa aparece marcada como "Esta tarefa" e fica aberta. **Mostrar mensagens anteriores** exibe mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo da mensagem.

Uma mensagem também abre dessa forma na pesquisa, no Graph, nas respostas do Ask ou na última verificação, marcada como "Esta mensagem" ou "Mensagens novas".

**Abrir no Gmail** abre o e-mail na conta do Gmail que o recebeu. No Android, ele abre no app Gmail, se estiver instalado.

**Detalhes** de um e-mail mostram somente as informações que não aparecem no cabeçalho, como os endereços completos em Cc, Cco ou um endereço de resposta diferente. Se não houver outras informações, a seção fica vazia.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link da tarefa para a própria mensagem também abre a conversa aqui, com **Abrir no Slack** no fim.

**Detalhes** mostram o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída aparece de forma resumida; a mensagem de origem fica em **Detalhes**.

Uma tarefa com status "Aguardando" tem um link para sua última mensagem enviada à pessoa, aquela que você está aguardando: "E-mail para Pat · ter".

## Criar uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, em **+** no celular ou com `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não selecionar **Trabalho** ou **Pessoal**, ela vai para a área certa conforme as pessoas e o assunto envolvidos. Ela também encontra o e-mail relacionado, mesmo que seja antigo.

- **Prazo**: digite um dia ou horário, como "amanhã", "na próxima sex", "3 nov", "14h" ou "daqui a 2 horas". Você também pode escrever no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta periodicamente. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada, como um e-mail, mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra que The Machine tenha. Pesquise pelo texto ou pelo remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, a câmera ao lado tira uma foto. É possível adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam anexados à tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
