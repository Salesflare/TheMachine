---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e0fd02e557e6daee
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo assim:

- **Feito agora**: no topo, uma etapa final que você confirmou, como um formulário ou problema, foi concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e seu celular também recebe a notícia.
- **Para você**: tudo que está esperando por você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (ela precisa primeiro de uma decisão ou resposta sua; quando o trabalho parou por algo que só você tem, como uma informação, um login ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas sem novidades há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, começando pelas mais recentes, com o horário em que foram concluídas, como "Feito há 5 minutos". Tarefas que parecem já ter sido concluídas aparecem como **Parece feito**.

Depois que você envia, uma nota curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". Uma resposta que só promete fazer o trabalho, como "Vou enviar até terça-feira", mantém a tarefa aberta: "Enviado. Mantido em aberto." **Abrir** leva você até ela. A busca encontra tarefas pelo título ou pela pessoa para quem foram enviadas, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por fim, o restante. Em cada grupo, as tarefas mais recentes aparecem primeiro. Uma tarefa mantém o lugar enquanto sua Machine a prepara e quando é concluída. Só o marcador muda. Nos outros grupos abertos, as tarefas atrasadas ou que vencem até amanhã aparecem primeiro, e o restante vem da mais recente para a mais antiga. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 mesclado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem mostra que a tarefa foi concluída, ela se encerra sozinha depois de um dia, com a opção **Desfazer**. Caso contrário, ela espera que você toque em **Marcar como feito**. Uma tarefa que você já resolveu por conta própria, como com uma resposta no Gmail ou Slack, também se encerra sozinha.

Quando uma mensagem vem de um endereço que parece ser de alguém que você conhece, mas não é, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa deixa isso claro: "Esta pessoa não é Sam Lee." Ela mostra o endereço verdadeiro da pessoa, nunca o nome que ela usou. Sua Machine confirma a mensagem com a pessoa do endereço que você já conhece, nunca com quem a enviou.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem fazê-la reaparecer. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte quando o prazo já passou, e informa de quem ainda está esperando uma resposta.

Quando uma tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa. Ela fica em **Aguardando outras pessoas** até uma mensagem mostrar o resultado e se encerra sozinha, com a opção **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com a opção **Escreva um lembrete curto** no chat. Diga no chat o que conta como conclusão para alterar isso.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas recentes apareçam primeiro depois de alguns dias fora. Não há novidades quando a tarefa não recebeu mensagens novas nem teve nenhuma ação sua, como uma mensagem no chat, uma edição ou um adiamento. Só olhar para ela não conta.

As tarefas urgentes, que vencem em breve ou que estão prestes a ser enviadas continuam em Para você. **Descartar tudo** marca todas as tarefas em Mais antigos como desnecessárias depois de uma confirmação, assim como **Não precisa** faz com uma tarefa por vez, com a opção **Desfazer**. Uma novidade faz a tarefa voltar para Para você.

Uma tarefa que ninguém tocou por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela é recolhida em Volta mais tarde, e deixa de contar no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nenhuma tarefa aberta pode receber uma tarefa com uma próxima etapa específica, até três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e deixa a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhou ou está atrasada, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou apenas um tipo. Seu celular e computador mostram a mesma seleção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta a mostrar tudo. Um alerta sobre a própria Machine, como uma parte que fica reiniciando, não é de Trabalho nem Pessoal e aparece apenas em Todos.

A linha no topo da lista também permite ir direto para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do seu último resumo da manhã ou da noite e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque nela para ler o resumo novamente e use **Copiar** para colá-lo onde quiser. Depois que você abre o resumo ou toca no **×**, ele aparece em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, em Trabalho e Pessoal ou apenas na categoria selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto** em **Detalhes** permite alterar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área** em **Detalhes** move uma tarefa para a outra área. O que ela pode ler e enviar também muda de área. **Desfazer** na nota move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar e todas as mensagens relacionadas estão nessa área, ela é movida para lá automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa criada por você sem escolher Trabalho ou Pessoal é movida automaticamente quando sua área fica clara. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens relacionadas a ela. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa. Uma tarefa sobre a sua vida pessoal, como uma mensagem da sua família enviada para o seu endereço de trabalho, é Pessoal desde o começo.

Um assunto de trabalho que chega a uma conta pessoal, como uma mensagem de um cliente no WhatsApp ou um pedido na sua caixa de e-mail pessoal, é de Trabalho desde o começo. Uma tarefa que você moveu ou classificou por conta própria sempre fica onde você a colocou. Trabalho ou Pessoal define onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde. A resposta sempre vai para a conversa original, mesmo depois de uma mudança, a menos que você escolha outro caminho.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho que recebeu o e-mail e nunca aparece em um Fleet de Trabalho ou no Graph da equipe.

Quando houver duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, mostra cada uma em sequência, na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo isso leva no seu ritmo, como "cerca de 2 min".

No fim, a lista mostra o que foi enviado ou encerrado e o que ainda está sendo preparado.

Uma tarefa que faz uma pergunta para você não entra nessa sequência: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações ficam pausadas. As mensagens novas ainda são lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a seção de verificações mostra "Pausadas durante a noite, atualização às 06:30". Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa à noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para ver as opções, incluindo **Detalhes**, que abre as verificações em Conexões. Se houver tarefas abertas, a opção fica no topo no computador. Uma linha curta aparece ali apenas enquanto uma verificação está em andamento ou quando ela falhou ou está atrasada. Você também pode pedir isso no chat.

LinkedIn, X e Salesflare têm seu próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das suas tarefas informa o que foi encontrado em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 tarefas novas". Ela informa apenas o resultado dessa verificação. As tarefas que já estavam na lista continuam como estavam. Quando uma tarefa nova espera por um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras, e a tarefa criada ou o motivo para não criar uma, como "Você só estava em cópia, outra pessoa está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação deu apenas uma explicação vaga. Toque em uma delas para ler a mensagem e o contexto ao redor.

As primeiras 10 aparecem na lista. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação no celular sobre uma mensagem que já está na lista aparece apenas uma vez. A linha fica visível por 12 horas depois da verificação.

Ela conta apenas os e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os próprios e-mails da The Machine, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, seu período de teste ou um convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** permite dizer o que deve mudar: como fazer a tarefa ou, quando um rascunho estiver pronto, o que alterar nele. **Marcar como feito** indica que a tarefa foi resolvida. A opção aparece na tarefa pronta sem rascunho ou na que faz uma pergunta para você. Nos outros casos, fica no topo de **…**. A tarefa sai da lista na hora, com a opção **Desfazer** na mensagem. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para encerrar a tarefa mais rápido. A alteração continua valendo.

Para concluir a tarefa de outro jeito, explique no **Chat** dela. A resposta informa apenas o que mudou, como o adiamento e até quando. Se algo não puder ser alterado, como o prazo, ela avisa.

Em **…**:

- **Passar…**: encaminhe a tarefa a alguém da equipe, a [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta em intervalos regulares](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha um motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome** em **Detalhes** para renomear a tarefa. Você também pode pedir no chat, por exemplo: "Renomeie para…". O título escolhido por você permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece na lista como nova. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, o prazo e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior confirma o pagamento, como uma mensagem do remetente confirmando que recebeu o valor, a tarefa se encerra sozinha. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até um horário específico, como uma confirmação antes de uma reunião, se encerra automaticamente depois desse horário. Ela vai para **Feito / descartado** com o status "Não é mais necessário". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou tarefa passada a outra pessoa aparecer como pronta, sua Machine verifica suas conversas recentes com as pessoas envolvidas, inclusive chats em grupo, e espera o Slack ler as mensagens. Se uma mensagem posterior mostrar que a tarefa já foi concluída, como quando alguém recebeu um pedido e respondeu que sim, ela se encerra sozinha. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escrever na mesma conversa depois da criação do rascunho, **Enviar** pausa o envio: "Não enviado: há uma mensagem nova na conversa". A tarefa mostra essa mensagem com as opções **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa transferida para outro local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda é necessária acompanha os novos planos. Se não houver mais nada a fazer, ela vai para **Feito / descartado** com o status "Não precisa". O chat informa "Atualizada:" e explica o motivo. **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**, e avisa que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão correspondente ou toca em ×.

No seu primeiro dia, o topo da página Tarefas dá as boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro para estar pronta quando você chegar.

Cada tarefa começa pelo título. A linha abaixo informa de quem se trata, a organização quando o assunto envolve uma (não apenas porque alguém trabalha nela), o projeto, se é Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Os nomes e as organizações mostram uma foto ou um logotipo quando o Graph tem um. Caso contrário, mostram as iniciais. Um logotipo difícil de ler em tamanho pequeno, como letras brancas em um fundo transparente ou um logotipo horizontal com texto, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato por e-mail há 12 dias. Nada desde então." Ela aparece quando a última conversa com a pessoa é antiga ou está sem resposta, e identifica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, toque em Conectar ao lado dele para abrir essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como foi encerrada, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho usa uma informação compartilhada por alguém em outro lugar, como uma sugestão de um colega no Slack, uma linha indica isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Uma conversa no Slack, WhatsApp, Telegram, Intercom e outros serviços aparece em ordem cronológica, da mais antiga para a mais recente: as mensagens anteriores à mensagem relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens ficam à direita, como no app. A mensagem relacionada à tarefa aparece marcada como "Esta tarefa" e aberta na conversa. **Mostrar mensagens anteriores** carrega mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo da mensagem.

Uma mensagem também pode ser aberta da mesma forma pela busca, pelo Graph, pelas respostas do Ask ou pela última verificação, marcada como "Esta mensagem" ou "Mensagens novas".

**Abrir no Gmail** abre o e-mail na conta do Gmail que o recebeu. No Android, ele abre no app Gmail se você tiver o app instalado.

Os **Detalhes** de um e-mail mostram apenas o que não aparece no cabeçalho, como endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver nada a acrescentar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a mensagem original também abre essa visualização, com **Abrir no Slack** no fim.

**Detalhes** mostram o nome, o projeto e a área da tarefa. Toque em um deles para alterar. Também mostram sua última nota e o resultado de um agente de programação. Toque no título para abrir o chat. Uma tarefa concluída continua resumida. A mensagem de origem fica em **Detalhes**.

Uma tarefa com status "Aguardando" tem um link para sua última mensagem enviada à pessoa e para a resposta que você está esperando: "E-mail para Pat · ter".

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, no **+** do celular ou em `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** nem **Pessoal**, ela vai para a área apropriada de acordo com quem e com o que estiver relacionada. Ela também encontra o e-mail que deu origem ao follow-up, mesmo que seja antigo.

- **Prazo**: digite um dia ou horário, como "amanhã", "próxima sex", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone do calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta em intervalos regulares. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule as pessoas ou empresas relacionadas à tarefa, até 5.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa, como um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que The Machine tenha. Pesquise pelo texto ou pelo remetente. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode anexar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê ao trabalhar nela. Você pode criar uma tarefa só com arquivos: ela preenche os detalhes com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
