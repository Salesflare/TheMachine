---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para você aprovar. Saiba o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa para cada assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** reúne todas elas:

- **Para você**: tudo que está esperando por você, começando pelo mais urgente. Cada tarefa indica **Preparada** (o trabalho está feito, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (antes, ela precisa de uma decisão ou resposta sua) ou **Preparando…** (sua Machine está trabalhando nela).
- **Feito agora**: uma última etapa que você confirmou, como um formulário ou problema, foi concluída enquanto você estava fora. Ela fica aqui até você tocar em **Entendi**, por no máximo um dia, e também aparece no seu celular.
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, da mais recente para a mais antiga, com o horário em que foram concluídas, como "Concluída há 5 minutos". Tarefas que parecem já ter sido concluídas aparecem como **Parece feito**.

Depois que você envia algo, uma nota curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou pelo destinatário, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet e, por fim, o restante. Dentro de cada grupo, as tarefas mais recentes aparecem primeiro. Uma tarefa mantém sua posição enquanto sua Machine a prepara e quando é concluída. Só o status muda. Nos outros grupos abertos, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, e depois as mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine vê que a tarefa foi concluída, como "PR #3451 mesclado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, são encerradas automaticamente, com a opção **Desfazer**. Uma tarefa que você já resolveu por conta própria, por exemplo respondendo no Gmail ou Slack, também é encerrada automaticamente.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa avisa claramente: "Esta pessoa não é Sam Lee." Ela mostra o remetente pelo endereço real, nunca pelo nome que ele usou. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem a escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, indica a etapa em **Aguardando**. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte se o prazo já tiver passado. Ela também informa quem ainda precisa responder.

Quando uma tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem confirmar o resultado e, então, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar, ela volta com a opção **Escreva um lembrete curto** no chat. Conte no chat o que é preciso para considerar a tarefa concluída.

Se ninguém mexer em uma tarefa por uma semana, ela pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se ninguém responder por mais uma semana, ela é recolhida em Volta mais tarde, e deixa de ser contada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editá-la, adiá-la ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e sem tarefas abertas pode receber uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine fica em repouso com a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou apenas um tipo. Seu celular e computador usam a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta à lista completa. Um alerta sobre a própria Machine, como uma parte que não para de reiniciar, não é de Trabalho nem Pessoal e aparece apenas em Todos.

A linha no topo da lista também alterna diretamente entre as opções: **Só Pessoal · Trabalho · Mostrar todas**.

A linha no topo da lista mostra o nome do seu resumo mais recente da manhã ou da noite e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque nela para ler o resumo de novo e usar **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, a linha mostra **Hoje até agora**: o que foi concluído hoje e o que ainda está aberto, em Trabalho e Pessoal ou só na categoria selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque no nome para abrir o projeto. **Projeto** em **Detalhes** permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-projects-to-dos).

**Área** em **Detalhes** move uma tarefa para sua outra área. O acesso ao que ela pode ler e enviar também muda. **Desfazer** na nota move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar e todas as mensagens de origem estão lá, ela é movida para essa área automaticamente e continua. Caso contrário, ela mostra **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando encontra a área certa. Até lá, não aparece como Trabalho nem Pessoal e permanece privada.

Uma tarefa sempre pode ler as mensagens que a originaram. Quando precisa de outras mensagens da sua outra área, ela pede permissão com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você classificou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa. Já uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega a uma conta pessoal, como uma mensagem de cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é Trabalho desde o início. Uma tarefa que você mesmo moveu ou classificou sempre fica onde você a colocou. Trabalho ou Pessoal define onde a tarefa aparece e com quem é compartilhada, nunca de onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança, a menos que você escolha outra opção.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho em que o e-mail chegou e nunca aparece em uma Fleet de Trabalho nem no Team Graph.

Quando há duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, permite avançar por elas uma de cada vez, na ordem da lista, mostrando cada rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc encerra. Abaixo do título, o cabeçalho também informa quanto tempo elas levam no seu ritmo, como "cerca de 2 min".

Uma tarefa que faz uma pergunta fica de fora das duas opções: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de alguém está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, em até uma hora.

À noite, das 00:00 às 06:30, as verificações ficam pausadas: as novas mensagens ainda são lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a opção Verificações mostra "Pausadas durante a noite, serão atualizadas às 06:30". Se você abrir o app, escrever no chat ou tocar em uma tarefa à noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação imediatamente.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para ver os detalhes e **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção fica no topo, no computador. Uma linha curta aparece ali somente enquanto uma verificação está em andamento ou quando alguma falhou ou atrasou. Você também pode pedir no chat.

LinkedIn, X e Salesflare seguem seu próprio ritmo.

## Última verificação

Depois de uma verificação que leu novas mensagens, uma linha acima das tarefas informa o que encontrou em cada fonte consultada, como "13 mensagens verificadas às 16:11 · nada precisa de você" ou "· 2 novas tarefas". Quando uma nova tarefa fica esperando um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa aguardando até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte. Você verá quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo para não criar uma, como "Você estava apenas em cópia, uma pessoa da equipe está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação deu apenas uma justificativa vaga. Toque em uma mensagem para lê-la.

As 10 primeiras aparecem de início. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação no celular sobre uma mensagem que já aparece na lista só é mostrada uma vez. A linha fica visível por 12 horas depois da verificação.

A contagem inclui apenas os e-mails enviados para você. Suas próprias respostas são lidas para dar contexto e identificar promessas, mas não são e-mails novos. Os e-mails da The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, seu período de teste ou um convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** permite dizer o que mudar: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como feita** indica que a tarefa foi resolvida. Ela fica visível em uma tarefa pronta sem rascunho; nos outros casos, aparece no topo de **…**, inclusive em uma tarefa que precisa da sua decisão. A tarefa sai da lista na hora, com a opção **Desfazer** na mensagem. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para encerrá-la antes. A alteração continua valendo.

Para fazer de outro jeito, diga como no **Chat** da tarefa.

Em **…**:

- **Passar…**: atribua a tarefa a uma pessoa da equipe, a [Claude Code ou Codex](hand-to-agent.md), ou [peça para alguém revisar](ask-to-review.md).
- **Repetir…**: a tarefa [volta em intervalos regulares](recurring.md).
- **Não precisa**: a tarefa desaparece. Você pode escolher um motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome** em **Detalhes** para renomear a tarefa. O título que você escolher permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, o vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como um débito automático ou um cartão cadastrado, não viram tarefas. Quando um e-mail posterior confirma o pagamento, por exemplo, uma mensagem do remetente avisando que recebeu, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até um horário definido, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela passa para **Feito / dispensado** como "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de uma tarefa passada para alguém aparecer como pronta, sua Machine verifica seus chats recentes com as pessoas envolvidas, inclusive os chats em grupo, e espera o Slack ler as mensagens. Quando uma mensagem posterior mostra que a tarefa já foi resolvida, como quando alguém pediu algo e recebeu uma resposta positiva, ela é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de local ou uma reserva cancelada, The Machine atualiza as tarefas por conta própria. Uma tarefa que ainda importa acompanha os novos planos. Uma tarefa sem nada a fazer passa para **Feito / dispensado** como "Não precisa", e o chat informa "Atualizado:" e o motivo. **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**, e avisa que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão ou toca em ×.

No seu primeiro dia, o topo de Tarefas dá as boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem ou do que se trata, a organização quando o assunto envolve uma (não apenas porque alguém trabalha nela), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

O nome de uma pessoa e o nome de uma organização mostram a foto ou o logotipo, se houver no Graph, e as iniciais caso contrário. Se um logotipo não ficar legível tão pequeno, como texto branco em um fundo transparente ou um nome muito comprido, também aparecem as iniciais.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail; nada desde então." Ela aparece quando a última conversa com a pessoa já faz tempo ou não teve resposta, e indica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de tentar adivinhar.

Quando a linha indica um canal que não está conectado, a opção Conectar ao lado abre essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como foi resolvida, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem que originou a tarefa, com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você saber de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho considera a contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mais antiga para a mais recente: as mensagens anteriores à mensagem relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa é identificada como "Esta tarefa" e aparece aberta. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo da mensagem.

**Detalhes** de um e-mail mostram apenas o que não aparece no cabeçalho, como os endereços completos em Cc, Cco ou um endereço diferente para respostas. Se não houver nada a acrescentar, essa opção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link de uma tarefa para a mensagem relacionada também a abre aqui, com **Abrir no Slack** na parte inferior.

**Detalhes** mostram o nome da tarefa, o projeto e a área (toque em um item para alterá-lo), sua última nota e o resultado de um agente de programação. **Chat ›** abre o chat. Uma tarefa concluída fica compacta. A mensagem que a originou aparece em **Detalhes**.

Uma tarefa em "Aguardando" tem um link para sua última mensagem enviada à pessoa, aquela cuja resposta você espera: "E-mail para Pat · ter.".

## Crie uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher Trabalho ou Pessoal, ela vai para a área certa conforme quem e o que estiverem envolvidos. Ela também encontra o e-mail ao qual a tarefa dá continuidade, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "próxima sex", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Mensagem**: anexe a mensagem relacionada à tarefa: um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem disponível na The Machine. Pesquise pelo texto ou pelo remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou solte arquivos no formulário. No celular, a câmera ao lado tira uma foto. Você pode adicionar até 5 arquivos, como no chat. Veja [Adicionar arquivos](card-chat.md#add-files). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê quando trabalha nela. Só os arquivos já bastam: ela preenche a tarefa usando um PDF ou arquivo de texto. Uma foto aparece como imagem pequena. Toque nela para vê-la em tamanho real.
