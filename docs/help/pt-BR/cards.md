---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para você aprovar. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, não importa quantas mensagens ele envolva.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo:

- **Para você**: tudo que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (o trabalho está pronto, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, ela precisa da sua decisão ou resposta) ou **Preparando…** (sua Machine está trabalhando nela).
- **Feito agora**: uma última etapa que você confirmou, como um formulário ou uma solicitação, foi concluída enquanto você estava fora. Ela fica aqui até você tocar em **Entendi**, por no máximo um dia, e você também recebe uma notificação no celular.
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta para **Ainda precisa?** (abaixo).
- **Promessas**: o que você prometeu e o que prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, começando pelas mais recentes, com o horário em que foram concluídas, como "Feita há 5 minutos". Tarefas que parecem já concluídas aparecem marcadas como **Parece feito**.

Depois que você envia algo, uma nota curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Volta mais tarde até seg.". **Abrir** leva você até ela. A pesquisa encontra uma tarefa pelo título ou por quem a recebeu, inclusive em Volta mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet e, por fim, o restante. Dentro de cada grupo, as tarefas mais recentes aparecem primeiro. Uma tarefa mantém seu lugar enquanto sua Machine a prepara e quando ela é concluída: só a marca muda. Nos outros grupos abertos, o que está atrasado ou vence até amanhã aparece primeiro, e o restante vem em ordem de data, começando pelo mais recente. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 foi integrado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, elas são encerradas automaticamente, com a opção **Desfazer**. Uma tarefa que você já resolveu por conta própria, por exemplo respondendo no Gmail ou no Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa informa isso claramente: "Esta pessoa não é Sam Lee." Ela mostra a pessoa pelo endereço que realmente usou, nunca pelo nome que ela informou. Sua Machine confirma a mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou uma resposta, mostra essa etapa em **Aguardando:**. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte depois que o prazo passar, e informa quem ainda precisa responder.

Quando uma tarefa depende de algo que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra isso em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para alterar isso.

Se ninguém mexer em uma tarefa por uma semana, ela pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela é recolhida em Volta mais tarde, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar ou adiar a tarefa, ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto sem atividade e sem tarefas abertas pode receber uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa com a lista vazia. Enquanto verifica, ela desperta e informa o que está fazendo. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal**, no alto da barra lateral, mostram todas as tarefas ou apenas um tipo. No celular e no computador, a seleção é a mesma. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta à lista completa. Um alerta sobre a própria Machine, como uma peça que fica reiniciando, não é Trabalho nem Pessoal e aparece apenas em Todos.

A linha no alto da lista também permite mudar direto para outra opção: **Só Pessoal · Trabalho · Mostrar todas**.

A linha no alto da lista mostra o nome do último resumo da manhã ou do fim do dia e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque nela para ler o resumo de novo e use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Quando não há um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua em aberto, para Trabalho e Pessoal ou apenas para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite alterar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-projects-to-dos).

**Área**, em **Detalhes**, move uma tarefa para sua outra área. O que ela pode ler e enviar também muda com ela. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar, e todas as mensagens relacionadas estão lá, ela é movida automaticamente para essa área e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal é movida automaticamente quando encontra a área certa. Até lá, ela não aparece em Trabalho nem em Pessoal e permanece privada.

Uma tarefa sempre pode ler as mensagens relacionadas a ela. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. Mensagens de outra empresa sua vão para as tarefas dessa empresa, e uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega a uma conta pessoal, como uma mensagem de cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é de Trabalho desde o início. Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a deixou. Trabalho ou Pessoal define onde uma tarefa aparece e com quem ela é compartilhada, nunca de onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança de área, a menos que você escolha outro jeito.

Mesmo sendo Pessoal, uma tarefa desse tipo ainda responde pelo endereço de trabalho que recebeu o e-mail, e nunca aparece em uma Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando por você, **Percorrer**, no cabeçalho de Para você, mostra uma de cada vez, na ordem da lista, com cada rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. Abaixo do título, o cabeçalho também informa quanto tempo elas levam no seu ritmo, como "cerca de 2 min".

Uma tarefa que faz uma pergunta para você não entra nesse fluxo: ela espera uma resposta sua, não um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de alguém está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações ficam pausadas: as mensagens novas ainda são lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a opção Verificações mostra "Pausadas durante a noite. Atualização às 06:30". Se você abrir o app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para vê-la, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção aparece no alto da tela no computador. Uma linha curta aparece ali apenas enquanto uma verificação está em andamento ou quando ela falha ou atrasa. Você também pode perguntar no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que encontrou em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nada precisa de você" ou "· 2 novas tarefas". Quando uma nova tarefa fica para um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo para não criar uma, como "Você estava em cópia, outra pessoa da equipe está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação indicou apenas um motivo vago. Toque em uma conversa para lê-la.

As 10 primeiras aparecem de início. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas há naquele chat. Uma notificação no celular sobre uma mensagem que já está na lista aparece só uma vez. A linha fica visível por 12 horas após a verificação.

A contagem inclui apenas mensagens enviadas para você. Suas próprias respostas são lidas para dar contexto e identificar promessas, mas não são mensagens novas. Os e-mails que The Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. Mensagens sobre cobrança, seu período de teste ou um convite são lidas normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que deve ser alterado: como fazer a tarefa ou, quando o rascunho estiver pronto, o que mudar nele. **Marcar como feita** indica que a tarefa foi resolvida: essa opção aparece diretamente em uma tarefa pronta sem rascunho. Nos outros casos, fica no alto de **…**, inclusive em tarefas que precisam da sua decisão. A tarefa sai da lista na hora, e a mensagem mostra **Desfazer**. Deslize a mensagem para dispensá-la ou arraste-a para fora com o mouse para fechá-la mais rápido. A alteração fica salva.

Para fazer de outro jeito, diga como no **Chat** da tarefa.

Em **…**:

- **Passar…**: passe a tarefa para alguém da equipe, para [Claude Code ou Codex](hand-to-agent.md) ou [peça a alguém para revisar](ask-to-review.md).
- **Repetir…**: a tarefa [volta em um ritmo definido](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. O título escolhido por você fica salvo.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, o vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior informa que a conta foi paga, como uma confirmação de pagamento enviada por quem cobrou, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até um horário determinado, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / dispensado** com o status "Não é mais necessário". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de um repasse para alguém aparecer como pronto, sua Machine verifica suas conversas recentes com as pessoas envolvidas, inclusive conversas em grupo, e aguarda o Slack terminar de lê-las. Se uma mensagem posterior indicar que a tarefa já foi concluída, como quando alguém recebeu um pedido e aceitou, ela é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa transferida para outro local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda importa acompanha os novos planos. Uma tarefa sem mais nada a fazer vai para **Feito / dispensado** com o status "Não precisa". O chat informa "Atualizado:" e o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**, e avisa que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão ou toca em ×.

No seu primeiro dia, uma mensagem no alto da página Tarefas dá as boas-vindas e informa quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem se trata, a organização quando ela é relevante (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

O nome de uma pessoa ou organização mostra a foto ou o logotipo quando há um disponível no Graph; caso contrário, mostra as iniciais. Um logotipo difícil de ler nesse tamanho, como texto branco em fundo transparente ou uma marca escrita muito larga, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail; nada desde então". Ela aparece quando a última conversa com a pessoa é antiga ou não teve resposta, e cita os canais que não estão conectados, como WhatsApp. Sua Machine diz o que não sabe em vez de adivinhar.

Quando a linha cita um canal que não está conectado, toque em Conectar ao lado dele para abrir essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com o desfecho abaixo, como "Concluída: Sam assinou na terça-feira".

Acima do rascunho, uma linha discreta informa de que mensagem ele veio, com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino para você saber de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como a sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Uma conversa (Slack, WhatsApp, Telegram, Intercom…) aparece como uma única conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela de que a tarefa trata e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa aparece marcada como "Esta tarefa" e abre em destaque. **Mostrar mensagens anteriores** acrescenta mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo dele.

**Detalhes** de um e-mail mostra apenas o que não aparece no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver mais nada para mostrar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link de uma tarefa para a própria mensagem também a abre aqui, com **Abrir no Slack** no fim.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. **Chat ›** abre o chat. Uma tarefa concluída fica resumida; a mensagem original aparece em **Detalhes**.

Uma tarefa com status "Aguardando" inclui um link para sua última mensagem enviada à pessoa, aquela cuja resposta você está esperando: "E-mail para Pat · ter".

## Crie uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador) cria uma tarefa para qualquer coisa. Criá-la não envia nada. Se você não escolher Trabalho ou Pessoal, ela vai para a área certa, de acordo com quem e com o que se relaciona. Ela também encontra o e-mail ao qual dá continuidade, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "próxima sex", "3 nov", "14h" ou "em 2 horas", também no seu idioma. O ícone do calendário mostra opções rápidas e **Escolher data**.
- **Mensagem**: anexe a mensagem relacionada à tarefa: um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que The Machine tenha. Pesquise por texto ou remetente. Cada resultado informa de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou solte arquivos no formulário. No celular, use a câmera ao lado para tirar uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: The Machine preenche a tarefa a partir de um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho real.
