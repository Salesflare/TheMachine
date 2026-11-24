---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fcb9a016c9af8551
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, não importa quantas mensagens estejam envolvidas.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo:

- **Feito agora**: no topo, aparece uma última etapa que você confirmou, como um formulário ou um problema, concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e também aparece no seu celular.
- **Para você**: tudo que está esperando por você, começando pelo que vence até amanhã. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (ela precisa primeiro de uma decisão ou resposta sua; quando o trabalho não pode continuar ou ser usado sem algo que só você tem, como um preço, uma informação ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não recebem novidades há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas cuja próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas, mensagens que [chegam mais tarde](send-later.md) e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, da mais recente para a mais antiga, com o horário em que foram concluídas, como “Feito há 5 minutos”. Tarefas que parecem já estar concluídas aparecem como **Parece feito**.

Depois que você envia algo, uma nota curta informa para onde a tarefa foi, como “Enviado. Movido para Feito.” ou “Enviado. Movido para Mais tarde até seg.”. Uma resposta que só promete fazer o trabalho, como “Vou enviar até terça”, mantém a tarefa aberta: “Enviado. Mantido em aberto.” **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou por quem recebeu a mensagem, inclusive em Mais tarde e Feito.

Em **Para você**, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por fim, o restante. Dentro de cada grupo, da mais recente para a mais antiga. A tarefa mantém a posição enquanto sua Machine a prepara e quando é concluída: só o marcador muda. Nos outros grupos abertos, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, seguidas pelas mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que algo foi concluído, como “PR #3451 mesclado”, mas a tarefa ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista e ajuda sua Machine a aprender. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem mostra que a tarefa foi concluída, ela é encerrada automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, ela espera você tocar em **Marcar como concluída**.

Uma tarefa que você já resolveu por conta própria, como respondendo no Gmail ou no Slack, também é encerrada automaticamente. Uma resposta que diz que há um arquivo anexado quando não há nenhum não encerra a tarefa.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa avisa claramente: “Esta pessoa não é Sam Lee.” A pessoa aparece pelo próprio endereço, nunca pelo nome que usou. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem a enviou.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou uma resposta, mostra **Aguardando:** e a etapa pendente. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem fazê-la voltar. O mesmo acontece depois que você faz uma pergunta: ela volta na manhã anterior ao prazo, no próprio prazo se ele for mais tarde no mesmo dia ou na manhã seguinte depois que o prazo passar. A tarefa informa quem ainda precisa responder.

Quando uma tarefa depende de um resultado que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem mostrar que o resultado chegou. Então, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com **Escreva um lembrete curto** no chat. Para mudar o que conta como concluído, diga isso no chat.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas recentes apareçam primeiro depois de alguns dias fora. Não há novidades quando a tarefa não recebe mensagens nem é afetada por algo que você faz, como enviar uma mensagem no chat, editar ou adiar. Só olhar para ela não conta.

Tarefas urgentes, que vencem em breve ou com um envio a caminho continuam em Para você. **Descartar tudo** marca como desnecessárias todas as tarefas em Mais antigos, após uma única confirmação, assim como **Não precisa** faz uma de cada vez, com a opção **Desfazer**. Qualquer novidade em uma tarefa a traz de volta para Para você.

Uma tarefa sem atividade por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** conserva a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, a tarefa fica recolhida em Volta mais tarde, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem tarefas abertas pode receber uma tarefa com uma próxima etapa específica, até três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine fica em repouso, com a lista vazia. Enquanto verifica, ela acorda e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou apenas um tipo. Seu celular e computador usam a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta para a lista completa. Um alerta sobre a própria Machine, como uma peça que reinicia sem parar, não é de Trabalho nem Pessoal e aparece apenas em Todos.

A linha no topo da lista também permite alternar diretamente para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do resumo mais recente da manhã ou da noite e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque para ler o resumo novamente e use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua em aberto, para Trabalho e Pessoal ou apenas para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite alterá-lo ou removê-lo. Veja [tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para a outra área. O acesso às mensagens que ela pode ler e enviar também muda. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa estar na outra área para continuar e todas as mensagens de origem estão lá, ela é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada é movido até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando sua Machine descobre a área certa. Até lá, ela não aparece em Trabalho nem em Pessoal e permanece privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa, e uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

O trabalho que chega a uma conta pessoal, como uma mensagem de um cliente no WhatsApp, um pedido na sua caixa de entrada pessoal ou uma [promessa](promises.md) relacionada ao trabalho, é de Trabalho desde o início.

Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a colocou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para a conversa original, mesmo depois de uma mudança, a menos que você escolha outra opção.

Mesmo sendo Pessoal, uma tarefa desse tipo responde pelo endereço de trabalho que recebeu o e-mail. Ela nunca aparece em um Fleet de Trabalho ou no Graph da equipe.

Quando houver duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, passa por elas uma de cada vez, na ordem da lista, mostrando cada rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo isso leva no seu ritmo, como “cerca de 2 min”.

No final, ele mostra quantas tarefas foram enviadas ou encerradas e quantas ainda estão sendo preparadas.

Uma tarefa que faz uma pergunta para você fica de fora dos dois casos: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, de dia e de noite. Ela verifica o que chegou quando há 40 mensagens aguardando ou quando a mensagem mais antiga de uma pessoa está aguardando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, em até uma hora.

À noite, da 00:00 às 06:30, as verificações são pausadas: as novas mensagens continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a mensagem das verificações diz “Pausadas durante a noite, retomam às 06:30”. Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações acontecem normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para vê-la e acesse **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção fica no topo da tela no computador. Uma linha curta aparece ali apenas enquanto uma verificação está em andamento ou quando alguma falhou ou atrasou. Você também pode perguntar no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que encontrou em todas as fontes consultadas, como “13 mensagens verificadas às 16:11 · nenhuma tarefa nova” ou “· 2 tarefas novas”. A linha se refere apenas àquela verificação: as tarefas que já estavam na sua lista continuam como antes. Quando uma tarefa nova fica aguardando um momento melhor, como o resumo da manhã, a linha informa até quando: “1 tarefa aguardando até amanhã às 08:30”.

Toque na linha para ver cada conversa de e-mail, chat e notificação com o ícone da fonte, quem escreveu, o assunto ou as primeiras palavras e a nova tarefa ou o motivo de não precisar fazer nada, como “Você estava em cópia, outra pessoa da equipe está respondendo” ou “Reunião já marcada para quinta-feira”. Uma conversa não mostra o motivo quando a verificação só encontrou um motivo vago. Toque em uma delas para ler a mensagem e o contexto.

As 10 primeiras aparecem de início. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação no celular sobre uma mensagem que já aparece na lista só é mostrada uma vez. A linha fica visível por 12 horas após a verificação.

A contagem inclui apenas os e-mails recebidos. Suas próprias respostas são lidas para dar contexto e identificar promessas, mas não são e-mails novos. Os e-mails que sua Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que alterar: como fazer ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como concluída** indica que a tarefa foi resolvida: fica visível em uma tarefa pronta sem rascunho ou em uma que faz uma pergunta para você; nos outros casos, fica no topo de **…**. A tarefa sai da lista na hora, e a mensagem mostra **Desfazer**. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para encerrá-la mais rápido. A alteração é mantida.

Para concluir a tarefa de outra forma, diga como no **Chat** dela. A resposta informa apenas o que mudou, como o adiamento e até quando. Se algo não puder ser alterado, como o prazo, ela avisa.

Em **…**:

- **Passar…**: encaminhe a tarefa para alguém da equipe, para [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta em um intervalo regular](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, como “Mude o nome para …”. O título escolhido é mantido.

**Reabrir** traz uma tarefa encerrada de volta. Ela também volta automaticamente quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e é organizada como nova. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas com pagamento automático, como débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior mostra que ela foi paga, como uma confirmação do remetente, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só precisava ser resolvida até um horário específico, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / descartado** como “Não precisa mais”. **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou tarefa encaminhada para alguém aparecer como pronta, sua Machine verifica as conversas recentes que você teve com as pessoas envolvidas, inclusive conversas em grupo, e espera o Slack terminar de lê-las. Se uma mensagem posterior mostrar que a tarefa já foi resolvida, como quando alguém recebeu um pedido e aceitou, ela é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escreveu na mesma conversa depois que o rascunho foi criado, **Enviar** pausa o envio: “Não enviado: há uma mensagem nova na conversa”. A tarefa mostra a mensagem com as opções **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de lugar ou uma reserva cancelada, a The Machine atualiza as tarefas por conta própria. Uma tarefa que ainda é necessária segue os novos planos. Uma tarefa sem mais nada a fazer vai para **Feito / descartado** como “Não precisa”, o chat mostra “Atualizado:” e o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais ações: **Pedir mudanças** e **Não precisa**. Ela também explica que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão dela ou toca em ×.

No primeiro dia, o topo de Tarefas dá as boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com um título. A linha abaixo informa de quem se trata, a organização quando ela é relevante, o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Os nomes e as organizações mostram uma foto ou um logotipo quando o Graph tem um. Caso contrário, mostram as iniciais. Um logotipo que não ficaria legível nesse tamanho, como um texto branco em fundo transparente ou uma marca horizontal, também mostra a inicial.

Às vezes, uma linha discreta informa o que não se sabe, como “Último contato há 12 dias por e-mail; nenhuma novidade desde então”. Ela aparece quando a última conversa com a pessoa é antiga ou não teve resposta, e cita os canais que não estão conectados, como o WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha cita um canal que não está conectado, toque em Conectar ao lado dele para abrir essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com a forma como foi encerrada logo abaixo, como “Concluída: Sam assinou na terça-feira”.

Acima do rascunho, uma linha discreta identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como uma sugestão de um colega no Slack, uma linha informa isso, como “Com base na mensagem de Sam em #ops”. Toque nela para ler a mensagem. Essa informação desaparece quando uma atualização substitui o rascunho.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa só, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela que gerou a tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa aparece marcada como “Esta tarefa” e é aberta na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo da mensagem.

Uma mensagem também é aberta da mesma forma na pesquisa, no Graph, nas respostas do Ask ou na última verificação, marcada como “Esta mensagem” (ou “Mensagens novas”).

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, ele abre no app do Gmail, se você tiver o app instalado.

**Detalhes** de um e-mail mostra apenas as informações que não aparecem no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver mais informações, nenhum detalhe é exibido.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link da tarefa para a própria mensagem também a abre aqui, com **Abrir no Slack** na parte inferior.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para alterá-lo), sua última nota e o resultado de um agente de programação. Toque no título para abrir o chat. Uma tarefa concluída fica compacta, e a mensagem que a originou aparece em **Detalhes**.

Uma tarefa “Aguardando” inclui um link para sua última mensagem para a pessoa, aquela cuja resposta você espera: “E-mail para Pat · ter”.

## Criar uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, em **+** no celular ou por `N`) cria uma tarefa para qualquer coisa. Criá-la não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, ela vai para a área certa, de acordo com quem e com o que ela está relacionada. Ela também encontra o e-mail relacionado, mesmo que seja antigo.

- **Prazo**: digite um dia ou horário, como “amanhã”, “sex. que vem”, “3 nov.”, “14h” ou “daqui a 2 horas”, também no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta em um intervalo regular. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule as pessoas ou empresas relacionadas, até 5.
- Ícone de mensagem: anexe a mensagem relacionada, como um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que a The Machine tenha. Pesquise por texto ou remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode anexar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e a The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho real.
