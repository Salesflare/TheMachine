---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 12be97d431968927
---
Sua Machine lê tudo o que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que ele apareça em várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** agrupa as tarefas:

- **Feito agora**: no topo, uma última etapa que você confirmou, como um formulário ou problema, foi concluída enquanto você estava longe. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e você também recebe uma notificação no celular.
- **Para você**: tudo o que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (o trabalho está feito, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, você precisa decidir ou responder), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa é de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, começando pelas mais recentes, com o horário em que foram concluídas, como "Feito há 5 minutos". As tarefas que parecem já estar concluídas recebem a marca **Parece feito**.

Depois que você envia algo, uma mensagem curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Volta mais tarde até seg.". **Abrir** leva você até a tarefa. A pesquisa encontra uma tarefa pelo título ou pela pessoa para quem ela foi enviada, inclusive em Volta mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas da sua Fleet, depois os acompanhamentos de um quadro e, por fim, o restante. Em cada grupo, as tarefas mais recentes aparecem primeiro. Uma tarefa mantém sua posição enquanto sua Machine a prepara e quando é concluída: só a marca muda. Nos outros grupos abertos, as tarefas atrasadas ou que vencem até amanhã aparecem primeiro, e o restante fica em ordem da mais recente para a mais antiga. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 merged", mas ela ainda não foi fechada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Depois de um dia, ela é fechada automaticamente, com a opção **Desfazer**. Uma tarefa que você já resolveu, como ao responder no Gmail ou no Slack, também é fechada automaticamente.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa informa isso claramente: "Esta pessoa não é Sam Lee." Ela mostra o endereço verdadeiro da pessoa, nunca o nome que ela usou. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda está esperando outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** essa etapa. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no horário do prazo quando ele é mais tarde no mesmo dia, ou na manhã seguinte quando o prazo já passou. Ela informa quem ainda precisa responder.

Quando uma tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não fecha a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Depois, ela é fechada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar, ela volta com a opção **Escreva um lembrete curto** no chat da tarefa. Diga no chat o que conta como concluído para mudar isso.

Se ninguém mexer em uma tarefa por uma semana, ela pergunta uma vez: **Ainda precisa?** **Não precisa** fecha a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, a tarefa é recolhida em Volta mais tarde, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma nova mensagem faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nada em aberto pode receber uma tarefa com um próximo passo específico, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e mostra uma lista vazia. Enquanto verifica, ela acorda e avisa. Se uma verificação falhou ou está atrasada, a mensagem informa isso, com a opção **Verificar agora** logo abaixo.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou só um tipo. Seu celular e computador mostram a mesma seleção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta à lista completa. Um alerta sobre a própria Machine, como uma parte que fica reiniciando, não é Trabalho nem Pessoal e aparece só em Todos.

A mensagem no topo da lista também muda direto para a outra opção: **Pessoal apenas · Trabalho · Mostrar todas**.

A linha no topo da lista mostra o resumo mais recente da manhã ou da noite e quantas tarefas ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque nela para ler o resumo de novo, com a opção **Copiar** para colar onde quiser. Depois que você abre o resumo ou toca no **×**, ele aparece em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, em Trabalho e Pessoal ou só na opção que você filtrou.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. A opção **Projeto** em **Detalhes** permite alterar ou remover o projeto. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

A opção **Área** em **Detalhes** move uma tarefa para a outra área. O que ela pode ler e enviar também é transferido. A opção **Desfazer** na mensagem move a tarefa de volta.

Quando uma tarefa precisa da outra área para continuar e todas as mensagens de origem estão lá, ela é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada é movido até você tocar nessa opção. Uma tarefa criada por você sem escolher Trabalho ou Pessoal é movida automaticamente quando encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e fica privada.

Uma tarefa sempre pode ler as mensagens de onde veio. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. Os e-mails de outra empresa sua vão para as tarefas dessa empresa. Uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para o seu endereço de trabalho, é Pessoal desde o início.

O trabalho que chega a uma conta pessoal, como uma mensagem de cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é Trabalho desde o início. Uma tarefa que você mesmo moveu ou colocou em uma área sempre fica onde você a colocou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem ela é compartilhada, nunca de onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança de área, a menos que você escolha outra forma.

Mesmo sendo Pessoal, uma tarefa desse tipo responde pelo endereço de trabalho que recebeu o e-mail e nunca aparece em uma Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer** no cabeçalho de Para você passa por elas uma de cada vez, na ordem da lista, mostrando cada rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc encerra. Abaixo do título, o cabeçalho também informa quanto tempo elas levam no seu ritmo, como "cerca de 2 min".

Uma tarefa que faz uma pergunta para você não entra nessa sequência: ela espera sua resposta, não um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, de dia e de noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações pausam: as novas mensagens ainda são lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a opção Verificações mostra "Pausadas durante a noite, retomadas às 06:30". Se você abrir o app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação imediata.

**Verificar agora** lê todas as fontes imediatamente. Se não houver nada em aberto, toque na mensagem da sua Machine para ver a opção **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, essa opção fica no topo da lista no computador. Uma mensagem curta aparece ali apenas enquanto uma verificação está em andamento ou quando ela falha ou atrasa. Você também pode perguntar no chat.

LinkedIn, X e Salesflare seguem seu próprio ritmo.

## Última verificação

Depois de uma verificação que leu novas mensagens, uma linha acima das tarefas informa o que ela encontrou em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nada precisa de você" ou "· 2 novas tarefas". Quando uma nova tarefa espera o momento certo, como o resumo da manhã, a mensagem informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo para não criar uma, como "Você estava só em cópia, outra pessoa da equipe está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação só encontrou um motivo vago. Toque em uma delas para ler.

As 10 primeiras aparecem na lista. Toque abaixo delas para ver o restante. Um número depois do nome, como (3), mostra quantas mensagens novas há naquele chat. Uma notificação no celular sobre uma mensagem que já está na lista aparece só uma vez. A linha fica visível por 12 horas depois da verificação.

A contagem inclui apenas os e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não são e-mails novos. Os próprios e-mails da The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem aparecem na lista. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que mudar: como fazer ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como feita** indica que a tarefa foi resolvida: a opção fica visível em uma tarefa pronta sem rascunho; nos outros casos, fica no topo de **…**, inclusive em uma tarefa que precisa da sua decisão. A tarefa sai da lista na hora, e a mensagem mostra a opção **Desfazer**. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para fechá-la mais rápido. A alteração é mantida.

Para concluir a tarefa de outra forma, diga como no **Chat** dela.

Em **…**:

- **Passar…**: atribua a tarefa a uma pessoa da equipe, ao [Claude Code ou Codex](hand-to-agent.md), ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta em um ritmo definido](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome** em **Detalhes** para renomear a tarefa. O título que você escolher é mantido.

**Reabrir** traz de volta uma tarefa fechada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior mostra que ela foi paga, como uma confirmação do remetente, a tarefa é fechada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até um horário determinado, como uma confirmação antes de uma reunião, é fechada automaticamente depois desse horário. Ela vai para **Feito / dispensado** com a indicação "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de mostrar como pronta uma mensagem ou um repasse para alguém, sua Machine verifica as conversas recentes com as pessoas envolvidas, inclusive chats em grupo, e espera o Slack ler as mensagens. Quando uma mensagem posterior mostra que a tarefa já foi resolvida, como quando alguém foi consultado e respondeu que sim, ela é fechada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais recente muda o plano, como uma festa que mudou de lugar ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda importa acompanha o novo plano. Uma tarefa que não precisa mais ser feita vai para **Feito / dispensado** com a indicação "Não precisa", e o chat mostra "Atualizado:" e o motivo. **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as ações principais: **Pedir mudanças** e **Não precisa**, além de avisar que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão correspondente ou toca em ×.

No seu primeiro dia, uma mensagem no topo de Tarefas dá as boas-vindas e diz quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo diz de quem é o assunto, a organização quando o assunto envolve uma (não apenas porque a pessoa trabalha nela), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

O nome e a organização mostram uma foto ou logotipo, se houver no Graph, e as iniciais caso contrário. Um logotipo que não fique legível pequeno, como texto branco em fundo transparente ou uma marca com palavras muito largas, também é substituído pelas iniciais.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato por e-mail há 12 dias; nenhuma novidade desde então." Ela aparece quando a última conversa com essa pessoa é antiga ou está sem resposta e indica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, a opção Conectar ao lado dele abre essa conexão.

O título diz o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como terminou, como "Concluído: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem de origem, junto com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho leva em conta a contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores à que deu origem à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem que deu origem à tarefa está marcada como "Esta tarefa" e abre na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Um e-mail mostra o restante da conversa recolhido acima e abaixo dele.

**Detalhes** de um e-mail mostra apenas o que não aparece no cabeçalho, como endereços completos em Cc, Bcc ou outro endereço para resposta. Se não houver nada a acrescentar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a própria mensagem também abre a conversa aqui, com **Abrir no Slack** na parte inferior.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última observação e o resultado de um agente de programação. **Chat ›** abre o chat. Uma tarefa concluída fica resumida; a mensagem de origem aparece em **Detalhes**.

Uma tarefa "Aguardando" tem um link para sua última mensagem enviada à pessoa, aquela cuja resposta você está esperando: "E-mail para Pat · ter".

## Criar uma tarefa

**Nova tarefa** (abaixo de **Pesquisar** no computador, **+** no celular ou `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não selecionar **Trabalho** ou **Pessoal**, ela vai para a área certa, de acordo com a pessoa e o assunto. Ela também encontra o e-mail relacionado, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como "amanhã", "sexta que vem", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone de calendário mostra sugestões rápidas e a opção **Escolher data**.
- **Repete**: a tarefa volta em um ritmo definido. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: associe as pessoas ou empresas relacionadas à tarefa, até 5.
- Ícone de mensagem: anexe a mensagem relacionada, como um e-mail, mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que a The Machine tenha. Pesquise por texto ou remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, use a câmera ao lado para tirar uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê quando trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
