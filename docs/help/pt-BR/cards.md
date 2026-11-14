---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para você aprovar. Entenda o que significa cada parte de uma tarefa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e4ad156150993936
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo assim:

- **Para você**: tudo que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (o trabalho está feito, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (ela precisa da sua decisão ou resposta primeiro) ou **Preparando…** (sua Machine está trabalhando nela).
- **Feito agora**: uma última etapa que você confirmou, como um formulário ou problema, foi concluída enquanto você estava fora. Ela fica aqui até você tocar em **Entendi**, por no máximo um dia, e seu celular também recebe uma notificação.
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta para **Ainda precisa?** (abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, começando pelas mais recentes, com o horário em que foram concluídas, como "Feito há 5 minutos". As tarefas que parecem já estar concluídas aparecem como **Parece feito**.

Depois que você envia algo, uma nota curta diz para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Volta mais tarde até seg.". **Abrir** leva você até a tarefa. A pesquisa encontra uma tarefa pelo título ou por quem a recebeu, inclusive em Volta mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet e, por último, o restante. Dentro de cada grupo, as tarefas mais recentes aparecem primeiro. Uma tarefa mantém sua posição enquanto sua Machine a prepara e quando ela é concluída. Só o status muda. Nos outros grupos abertos, o que está atrasado ou vence até amanhã aparece primeiro, seguido do restante, começando pelas tarefas mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 mesclado", mas ela ainda não foi fechada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, ela é fechada automaticamente, e você pode usar **Desfazer**. Uma tarefa que você já resolveu por conta própria, como ao responder no Gmail ou no Slack, também é fechada automaticamente.

Uma tarefa que ainda está esperando outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** seguido dessa etapa. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte se o prazo já tiver passado. Ela informa quem ainda precisa responder.

Quando uma tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não fecha a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, ela é fechada automaticamente, e você pode usar **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para mudar isso.

Se ninguém mexer em uma tarefa por uma semana, ela pergunta uma vez: **Ainda precisa?** **Não precisa** fecha a tarefa, e você pode usar **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela é recolhida em Volta mais tarde, e ela deixa de contar no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editá-la, adiá-la ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem tarefas abertas pode receber uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e deixa a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhou ou está atrasada, a linha informa isso e mostra **Verificar agora**.

Os filtros **Todos**, **Trabalho** e **Pessoal**, no alto da barra lateral, mostram todas as tarefas ou apenas um tipo. Seu celular e computador mostram a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta à lista completa. Um alerta sobre a própria Machine, como uma parte que fica reiniciando, não é de Trabalho nem Pessoal e aparece somente em Todos.

A linha no alto da lista também permite alternar diretamente para outra opção: **Só pessoal · Trabalho · Mostrar todas**.

A linha no alto da lista mostra o resumo mais recente da manhã ou da noite e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque nela para ler o resumo novamente e use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, a linha mostra **Hoje até agora**: o que foi concluído hoje e o que ainda está aberto, em Trabalho e Pessoal, ou somente na área selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-projects-to-dos).

**Área**, em **Detalhes**, move uma tarefa para a outra área. O que ela pode ler e enviar também muda com ela. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa da outra área para continuar, e todas as mensagens de origem já estão lá, ela é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando sua Machine descobre a área certa. Até lá, ela não aparece em Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa, e uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para o seu endereço de trabalho, é Pessoal desde o início.

O trabalho que chega a uma conta pessoal, como um cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é de Trabalho desde o início. Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a colocou. Trabalho ou Pessoal define onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança, a menos que você escolha outra opção.

Uma tarefa Pessoal desse tipo ainda responde pelo endereço de trabalho que recebeu o e-mail, e nunca aparece em uma Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, passa por elas uma de cada vez, na ordem da lista, mostrando cada rascunho completo, com **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc para. Abaixo do título, o cabeçalho também informa quanto tempo leva no seu ritmo, como "cerca de 2 min".

Uma tarefa que faz uma pergunta para você fica fora desse processo: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, da 00:00 às 06:30, as verificações são pausadas: as novas mensagens ainda são lidas e guardadas, mas são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a seção Verificações mostra "Pausadas durante a noite, atualizadas às 06:30". Se você abrir o app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação imediatamente.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para vê-la, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção fica no alto da tela no computador. Uma linha curta aparece ali somente enquanto uma verificação está em andamento ou quando uma falhou ou está atrasada. Você também pode pedir no chat.

LinkedIn, X e Salesflare têm o próprio ritmo.

## Última verificação

Depois de uma verificação que leu novas mensagens, uma linha acima das tarefas informa o que ela encontrou em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nada precisa de você" ou "· 2 novas tarefas". Quando uma nova tarefa fica aguardando um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo para não criar uma, como "Você estava só em cópia, uma pessoa da equipe está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação encontrou apenas um motivo vago. Toque em uma delas para ler.

As 10 primeiras aparecem na lista. Toque abaixo delas para ver o restante. Um número depois do nome, como (3), indica quantas novas mensagens aquele chat tem. Uma notificação no celular sobre uma mensagem que já está na lista aparece uma só vez. A linha fica visível por 12 horas após a verificação.

Ela conta somente os e-mails enviados para você. Suas próprias respostas são lidas para entender o contexto e as promessas, mas não contam como novos e-mails. Os e-mails que a The Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, seu período de teste ou um convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** indica o que mudar: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como feita** significa que a tarefa foi resolvida: a opção fica visível em uma tarefa pronta sem rascunho. Nos outros casos, fica no alto do menu **…**, inclusive em uma tarefa que precisa da sua decisão. A tarefa sai da lista imediatamente, e a mensagem mostra **Desfazer**. Deslize a mensagem para dispensá-la ou arraste-a para fora com o mouse para fechá-la mais rápido. A alteração continua valendo.

Para resolver de outro jeito, diga como no **Chat** da tarefa.

No menu **…**:

- **Passar…**: passe a tarefa para uma pessoa da equipe, [Claude Code ou Codex](hand-to-agent.md), ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta regularmente](recurring.md).
- **Não é relevante**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. O título que você escolher será mantido.

**Reabrir** traz de volta uma tarefa fechada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você envia uma resposta.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como um débito automático ou um cartão cadastrado, não viram tarefas. Quando um e-mail posterior mostra que ela foi paga, como uma confirmação do remetente de que o pagamento chegou, a tarefa é fechada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só era relevante até determinado horário, como uma confirmação antes de uma reunião, é fechada automaticamente depois desse horário. Ela vai para **Feito / dispensado** com o status "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou repasse para alguém aparecer como pronto, sua Machine verifica os chats recentes com as pessoas envolvidas, inclusive os chats em grupo, e espera o Slack terminar de lê-los. Se uma mensagem posterior mostrar que a tarefa já foi resolvida, como quando alguém foi solicitado e aceitou, ela é fechada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa que foi transferida para outro local ou uma reserva cancelada, The Machine atualiza as próprias tarefas. Uma tarefa que ainda é relevante segue os novos planos. Uma tarefa sem nada a fazer vai para **Feito / dispensado** com o status "Não precisa", e o chat dela informa "Atualizado:" e o motivo. **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais ações: **Pedir mudanças** e **Não precisa**, e avisa que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão dela ou toca em ×.

No seu primeiro dia, a parte de cima de Tarefas dá as boas-vindas e informa quem está esperando há mais tempo pela sua resposta. O rascunho dessa resposta é preparado primeiro, para estar pronto quando você chegar.

Cada tarefa começa com um título. A linha abaixo informa de quem se trata, a organização quando houver uma relação com ela (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página dessa pessoa no Graph.

O nome de uma pessoa e o de uma organização mostram a foto ou o logotipo, se houver no Graph, e as iniciais caso contrário. Um logotipo que não dê para ler bem em tamanho pequeno, como texto branco em fundo transparente ou uma marca com palavras em formato largo, também aparece como uma inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail; nada desde então". Ela aparece quando a última conversa com a pessoa é antiga ou não teve resposta, e menciona canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, **Conectar**, ao lado dele, abre essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com a forma como foi concluída abaixo, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho informa de qual mensagem ele veio, com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho usa uma contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa está marcada como "Esta tarefa" e aparece aberta. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Um e-mail mostra o restante da conversa recolhido acima e abaixo dele.

**Detalhes** de um e-mail mostram somente as informações que não aparecem no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver mais nada para mostrar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link de uma tarefa para a própria mensagem também a abre aqui, com **Abrir no Slack** na parte de baixo.

**Detalhes** mostram o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. **Chat ›** abre o chat. Uma tarefa concluída fica resumida; a mensagem de origem aparece em **Detalhes**.

Uma tarefa com status "Aguardando" tem um link para sua última mensagem para a pessoa, aquela cuja resposta você espera: "E-mail para Pat · ter.".

## Crie uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher Trabalho ou Pessoal, ela vai para a área certa com base em quem e no que ela trata. A tarefa também encontra o e-mail que acompanha, mesmo que seja mais antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "próxima sex.", "3 nov.", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Mensagem**: anexe a mensagem relacionada à tarefa: um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que The Machine tenha. Pesquise por texto ou remetente. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho real.
