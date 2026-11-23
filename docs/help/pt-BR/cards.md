---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que significa cada parte de uma tarefa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 88ccf5426e5a538f
---
Sua Machine lê tudo que chega e cria uma tarefa somente quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo assim:

- **Feito agora**: no topo, mostra uma última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema enquanto você estava ausente. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e também aparece no seu celular.
- **Para você**: tudo o que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (ela precisa primeiro de uma decisão ou resposta sua; quando o trabalho parou por depender de algo que só você tem, como uma informação, um login ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não tiveram novidades na última semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, da mais recente para a mais antiga, com a hora em que foram concluídas, como "Feito há 5 minutos". As tarefas que parecem já estar concluídas aparecem como **Parece feito**.

Depois que você envia, uma nota curta mostra para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Volta mais tarde até seg.". Uma resposta que só promete concluir o trabalho, como "Envio até terça-feira", mantém a tarefa aberta: "Enviado. Mantido em aberto." **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou pela pessoa para quem foram enviadas, inclusive em Volta mais tarde e Feito.

Em **Para você**, primeiro aparecem as tarefas atrasadas ou com prazo até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por fim, o restante. Dentro de cada grupo, as mais recentes aparecem primeiro. A tarefa permanece no mesmo lugar enquanto sua Machine a prepara e quando é concluída: só o marcador muda. Nos outros grupos abertos, aparecem primeiro as tarefas atrasadas ou com prazo até amanhã, seguidas das mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine vê que a tarefa foi concluída, como "PR #3451 aprovado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem mostra que a tarefa foi concluída, ela é encerrada automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, fica aguardando você tocar em **Marcar como feito**. Uma tarefa que você já resolveu por conta própria, como ao responder no Gmail ou no Slack, também é encerrada automaticamente.

Quando a mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa avisa com clareza: "Esta pessoa não é Sam Lee." Ela mostra o endereço verdadeiro, nunca o nome usado pela pessoa. Sua Machine confirma se a mensagem é legítima com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem fazê-la voltar. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde naquele dia, ou na manhã seguinte se o prazo já passou. Ela também informa quem ainda precisa responder.

Quando uma tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem mostrar o resultado e, então, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com a opção **Escreva um lembrete curto** no chat. Para mudar o que conta como concluído, diga isso no chat.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as mais recentes apareçam primeiro depois de alguns dias longe do app. Não há novidades quando não chega uma mensagem nova nem acontece nada que você faça na tarefa, como enviar uma mensagem no chat, editar ou adiar. Só olhar a tarefa não conta.

Tarefas urgentes, com prazo próximo ou com um envio em andamento continuam em Para você. **Descartar tudo** marca todas as tarefas de Mais antigos como desnecessárias após uma confirmação, assim como **Não precisa** faz com uma tarefa por vez, com a opção **Desfazer**. Se houver novidades em uma tarefa, ela volta para Para você.

Uma tarefa que ninguém mexeu por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa e ela não pergunta novamente. Se não houver resposta por mais uma semana, ela é recolhida em Volta mais tarde, e deixa de contar no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem tarefas em aberto pode receber uma tarefa com uma próxima etapa específica, até três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e mostra uma lista vazia. Enquanto verifica, ela volta e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou só as de um tipo. Seu celular e computador mostram a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta para a lista completa. Um alerta sobre a sua Machine, como uma peça que fica reiniciando, não é de Trabalho nem Pessoal, e aparece somente em Todos.

A linha no topo da lista também leva direto à outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do seu último resumo da manhã ou da noite e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque nela para ler o resumo novamente e use **Copiar** para colar onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, para Trabalho e Pessoal ou somente para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto** em **Detalhes** permite trocar de projeto ou remover a tarefa do projeto. Veja [tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área** em **Detalhes** move uma tarefa para a outra área. O que ela pode ler e enviar também muda com ela. A opção **Desfazer** na nota move a tarefa de volta.

Quando uma tarefa precisa estar na outra área para continuar e todas as mensagens de origem estão lá, ela é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal é movida automaticamente quando a Machine encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens de onde veio. Quando precisa de outras mensagens da outra área, ela pede com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa. Uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada ao seu endereço de trabalho, é Pessoal desde o início.

O trabalho que chega por uma conta pessoal, como uma mensagem de um cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é de Trabalho desde o início. Uma tarefa que você moveu ou colocou em uma área permanece onde você a colocou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança de área, a menos que você escolha outro caminho.

Mesmo sendo Pessoal, uma tarefa assim responde pelo endereço de trabalho em que o e-mail chegou e nunca aparece em um Fleet de Trabalho ou no Graph da equipe.

Se houver duas ou mais tarefas aguardando, **Percorrer** no cabeçalho de Para você mostra cada uma por vez, na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo isso leva no seu ritmo, como "cerca de 2 min".

No fim, ele mostra quantas tarefas foram enviadas ou encerradas e quantas ainda estão sendo preparadas.

Uma tarefa que faz uma pergunta para você fica de fora dos dois grupos: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, de dia e de noite. Ela verifica o que chegou quando há 40 mensagens aguardando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações são pausadas: as mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, as verificações mostram "Pausadas durante a noite. Atualização às 06:30". Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações continuam normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes na hora. Se não houver tarefas em aberto, toque na linha da sua Machine para ver o status e **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção fica no topo da lista no computador. Uma linha curta aparece ali somente durante uma verificação ou quando uma falha ou atraso acontece. Você também pode perguntar no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas mostra o que foi encontrado em todas as fontes verificadas, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 novas tarefas". Ela fala somente daquela verificação: as tarefas que já estavam na sua lista continuam como estão. Se uma tarefa nova estiver aguardando o momento certo, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação com o ícone do serviço de origem, quem escreveu, o assunto ou as primeiras palavras, e a tarefa nova ou o motivo de ela não ser necessária, como "Você só está em cópia, outra pessoa está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação só deu um motivo vago. Toque em uma conversa para lê-la.

As 10 primeiras aparecem de início. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas há naquele chat. Uma notificação no celular sobre uma mensagem que já está na lista aparece apenas uma vez. A linha fica visível por 12 horas após a verificação.

A contagem inclui somente e-mails enviados a você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como novos e-mails. Os próprios e-mails da The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que precisa ser alterado: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como feito** indica que a tarefa foi resolvida: aparece à vista em uma tarefa pronta sem rascunho; nos outros casos, fica no topo de **…**, inclusive em tarefas que precisam da sua decisão. A tarefa sai da lista na hora, com a opção **Desfazer** na mensagem. Deslize a mensagem para longe ou arraste-a para fora com o mouse para encerrar a tarefa antes. A alteração continua valendo.

Para concluir a tarefa de outro jeito, diga como no **Chat**. A resposta informa somente o que mudou, como o adiamento e até quando. Se algo não puder ser alterado, como uma data de vencimento, ela avisa.

Em **…**:

- **Passar…**: encaminhe a tarefa para alguém da equipe, para o [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta em um intervalo regular](recurring.md).
- **Não precisa**: a tarefa é removida. Se quiser, escolha um motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, como "Mude o nome para …". O título que você escolher será mantido.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece como nova na lista. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou cartão cadastrado, não viram tarefa. Quando um e-mail posterior confirma o pagamento, como uma mensagem do remetente confirmando que recebeu, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só é importante até determinado horário, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / descartado** como "Não é mais necessário". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou tarefa repassada aparecer como pronta, sua Machine verifica as conversas recentes com as pessoas envolvidas, inclusive em chats em grupo, e aguarda o Slack ler as mensagens. Se uma mensagem posterior mostrar que a tarefa já foi resolvida, como quando alguém recebeu o pedido e aceitou, ela é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escrever na mesma conversa depois da criação do rascunho, **Enviar** pausa o envio: "Não enviado: há uma mensagem nova na conversa". A tarefa mostra essa mensagem com **Ler** e **Refazer para esta mensagem**. Pressione **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de local ou uma reserva cancelada, a The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda for necessária acompanha os novos planos. Uma tarefa que não tiver mais nada a fazer vai para **Feito / descartado** como "Não precisa". No chat, aparece "Atualização:" com o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as ações principais: **Pedir mudanças** e **Não precisa**, além de explicar que nada é enviado até você pressionar **Enviar**. A dica desaparece de vez quando você usa o botão ou pressiona ×.

No seu primeiro dia, uma saudação aparece no topo de Tarefas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa a pessoa envolvida, a organização quando o assunto é sobre ela (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Os nomes e as organizações mostram uma foto ou um logotipo quando há um no Graph; caso contrário, mostram as iniciais. Um logotipo que não fique legível em tamanho pequeno, como letras brancas em um fundo transparente ou uma marca escrita muito larga, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail; nenhuma novidade desde então." Ela aparece quando a última conversa é antiga ou não teve resposta e informa canais que não estão conectados, como o WhatsApp. Sua Machine diz o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, toque em Conectar ao lado dele para abrir essa conexão.

O título diz o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como foi encerrada, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino para você saber de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho considera a contribuição de alguém em outro lugar, como a sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa única, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa tem a marcação "Esta tarefa" e abre a conversa nessa mensagem. **Mostrar mensagens anteriores** exibe mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo da mensagem.

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, o e-mail abre no app Gmail se você o tiver instalado.

**Detalhes** de um e-mail mostram somente as informações que não aparecem no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver mais nada para mostrar, a seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a própria mensagem também abre a mensagem aqui, com **Abrir no Slack** na parte de baixo.

**Detalhes** mostram o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída continua compacta; a mensagem de origem fica em **Detalhes**.

Uma tarefa "Aguardando" tem um link para sua última mensagem enviada à pessoa, aquela cuja resposta você aguarda: "E-mail para Pat · ter".

## Criar uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, **+** no celular ou `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** nem **Pessoal**, ela vai para a área certa com base em quem e no que diz respeito. A tarefa também encontra o e-mail relacionado ao follow-up, inclusive se for antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "próxima sex", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone do calendário mostra sugestões rápidas e **Escolher data**.
- **Repete**: a tarefa volta em um intervalo regular. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule as pessoas ou empresas envolvidas, até 5.
- Ícone de mensagem: anexe a mensagem relacionada, como um e-mail, mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que a The Machine tenha. Pesquise pelo texto ou pelo remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa e a The Machine os lê ao trabalhar nela. Só os arquivos já bastam: a The Machine preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho real.
