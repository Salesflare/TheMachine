---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para você aprovar. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: f77d6b07f6f94ce5
---
Sua Machine lê tudo o que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo assim:

- **Feito agora**: no topo, aparece uma última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e também aparece no seu celular.
- **Para você**: tudo o que está esperando por você, começando pelo que vence até amanhã. Cada tarefa indica **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, você precisa decidir ou responder; quando o trabalho não pode continuar ou ser usado sem algo que só você tem, como um preço, um fato ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não tiveram novidades na última semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas cuja próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas, mensagens que [chegam mais tarde](send-later.md) e tarefas sem resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, começando pelas mais recentes, com o horário em que foram concluídas, como "Feito há 5 minutos". Tarefas que parecem concluídas já aparecem como **Parece feito**.

Depois que você envia algo, uma nota curta indica para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". Uma resposta que só promete fazer algo, como "Envio até terça-feira", mantém a tarefa aberta: "Enviado. Mantido aberto." **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou pelo destinatário, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por último, o restante. Dentro de cada grupo, as tarefas mais recentes vêm primeiro. Uma tarefa mantém o lugar enquanto sua Machine a prepara e quando ela é concluída: só o indicador muda. Nos outros grupos abertos, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, e depois as mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 mesclado", mas ela ainda não foi fechada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem indica que a tarefa foi concluída, ela se fecha automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, ela espera você tocar em **Marcar como concluído**.

Uma tarefa que você já resolveu, por exemplo, respondendo pelo Gmail ou Slack, também se fecha automaticamente. Uma resposta que diz que um arquivo está anexado quando não está não fecha a tarefa.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa avisa claramente: "Esta pessoa não é Sam Lee." Ela mostra o endereço verdadeiro, nunca o nome usado por quem escreveu. Sua Machine confirma a mensagem com a pessoa do endereço que você já conhece, nunca com quem escreveu.

Uma tarefa que ainda está esperando outra pessoa, como uma revisão ou resposta, indica essa etapa em **Aguardando:**. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte se o prazo já tiver passado. Ela informa quem ainda precisa responder.

Quando a tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não fecha a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, ela se fecha automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com a opção **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para alterar isso.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas recentes apareçam primeiro quando você voltar depois de alguns dias. Não há novidades quando não chega nenhuma mensagem nova nem você faz algo na tarefa, como enviar uma mensagem no chat, editar ou adiar. Apenas abrir a tarefa não conta.

Tarefas urgentes, com prazo próximo ou com um envio em andamento continuam em Para você. **Descartar tudo** marca todas as tarefas de Mais antigos como desnecessárias após uma confirmação, assim como **Não precisa** faz com uma tarefa de cada vez. Você pode usar **Desfazer**. Se algo novo acontecer em uma delas, ela volta para Para você.

Uma tarefa sem nenhuma interação por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** fecha a tarefa, e você pode usar **Desfazer**. **Manter** mantém a tarefa e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela é recolhida em Volta mais tarde, e deixa de entrar na contagem do ícone do app e do resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem tarefas abertas pode receber uma tarefa com uma próxima etapa específica, até três vezes por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e mostra uma lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, uma linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal**, no topo da barra lateral, mostram todas as tarefas ou apenas as de um tipo. Seu celular e computador mostram a mesma opção selecionada. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta a exibir tudo. Um alerta sobre a própria Machine, como uma peça que reinicia continuamente, não é de Trabalho nem Pessoal e só aparece em Todos.

A linha no topo da lista também permite mudar direto para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o resumo mais recente da manhã ou da noite e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque na linha para ler o resumo de novo e use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele aparece em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua aberto, para Trabalho e Pessoal ou só para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite alterar o projeto ou remover a tarefa dele. Veja [tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para sua outra área. O acesso às mensagens que ela pode ler e enviar também muda. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar e todas as mensagens relacionadas estão lá, ela é movida automaticamente para essa área e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal é movida automaticamente quando a área certa é identificada. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa acessar outras mensagens da sua outra área, ela pergunta usando **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você classificou como Pessoal conta como Pessoal. E-mails de outras empresas suas vão para as tarefas daquela empresa. Já uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

O trabalho que chega a uma conta pessoal, como uma mensagem de cliente no WhatsApp, um pedido na sua caixa de e-mail pessoal ou uma [promessa](promises.md) relacionada ao trabalho, é Trabalho desde o início.

Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a colocou. Trabalho ou Pessoal define onde ela aparece e com quem é compartilhada, nunca onde ela responde. A resposta sempre vai para onde está a conversa, mesmo depois de uma mudança de área, a não ser que você escolha outro destino.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho que recebeu o e-mail e nunca aparece em um Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, passa por elas uma de cada vez, na ordem da lista, mostrando cada rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo isso leva no seu ritmo, como "cerca de 2 min".

No fim, a lista mostra o que foi enviado ou fechado e o que ainda está sendo preparado.

Uma tarefa que faz uma pergunta para você não entra nessa lista: ela espera sua resposta, não um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações são pausadas. As mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a opção de verificações informa: "Pausadas durante a noite, serão atualizadas às 06:30". Se você clicar, digitar ou rolar o app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações continuam normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para vê-la e abrir **Detalhes**, que leva a Verificações em Conexões. Se houver tarefas abertas, a opção fica no topo da página no computador. Uma linha curta aparece ali apenas enquanto uma verificação está em andamento ou quando falha ou atrasa. Você também pode perguntar no chat.

LinkedIn, X e Salesflare têm seu próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que foi encontrado em todas as fontes lidas, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 tarefas novas". Ela se refere apenas a essa verificação: as tarefas que já estavam na lista continuam esperando como antes. Quando uma tarefa nova fica aguardando um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa por e-mail, chat ou notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras e a nova tarefa ou o motivo de não ter sido necessária, como "Você estava em cópia, outra pessoa da equipe está respondendo" ou "A reunião já está marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação só encontrou uma resposta vaga. Toque em uma conversa para ler a mensagem e o que foi dito ao redor dela.

As 10 primeiras aparecem de início. Toque abaixo delas para ver o restante. Um número depois do nome, como (3), indica quantas mensagens novas esse chat tem. Uma notificação no celular sobre uma mensagem que já aparece na lista é exibida uma única vez. A linha fica disponível por 12 horas após a verificação.

A contagem inclui apenas e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails que sua própria Machine envia, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** permite dizer o que alterar: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. Se você começar a escrever e deixar pela metade, o texto estará lá quando voltar. **Cancelar** apaga o texto.

**Marcar como concluído** indica que a tarefa foi resolvida. A opção aparece na tarefa quando ela está pronta, mas não tem rascunho ou faz uma pergunta. Nos outros casos, fica no topo de **…**. A tarefa sai da lista na hora, e a mensagem mostra a opção **Desfazer**. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para fechá-la antes. A alteração fica salva.

Para concluir a tarefa de outra forma, diga como no **Chat**. A resposta informa apenas o que mudou, como o adiamento e até quando. Se algo não puder ser alterado, como o prazo, ela avisa.

Em **…**:

- **Passar…**: atribua a tarefa a alguém da equipe, ao [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta com uma frequência definida](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, por exemplo: "Renomeie para…". O título escolhido fica salvo.

**Reabrir** traz de volta uma tarefa fechada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece como nova na lista. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar, de qualquer país, vira uma tarefa com o valor, o vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como um débito automático ou um cartão cadastrado, não viram tarefa. Quando um e-mail posterior confirma o pagamento, como uma confirmação de recebimento enviada pelo remetente, a tarefa se fecha automaticamente. Você pode usar **Desfazer** por um dia para trazê-la de volta.

Uma tarefa que só importa até um horário definido, como uma confirmação antes de uma reunião, fecha automaticamente depois desse horário. Ela vai para **Feito / descartado** com o status "Não é mais necessário". Você pode usar **Desfazer** por um dia para trazê-la de volta.

Antes de uma mensagem ou tarefa repassada para alguém aparecer como pronta, sua Machine verifica as conversas recentes que você teve com as pessoas envolvidas, inclusive as conversas em grupo, e espera o Slack lê-las. Quando uma mensagem posterior mostra que a tarefa já foi resolvida, por exemplo, porque alguém foi consultado e respondeu que sim, ela se fecha automaticamente. Você pode usar **Desfazer** por um dia para trazê-la de volta.

Se outra pessoa escrever na mesma conversa depois da criação do rascunho, **Enviar** pausa o envio e mostra: "Não enviado: há uma mensagem nova na conversa". A tarefa mostra essa mensagem com as opções **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa que muda de local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda importa acompanha os novos planos. Se não houver mais nada a fazer, ela vai para **Feito / descartado** como "Não precisa". O chat informa "Atualizado:" e o motivo, e você pode usar **Desfazer** por um dia para trazê-la de volta.

Nas suas primeiras tarefas, uma dica curta mostra as principais ações: **Pedir mudanças** e **Não precisa**. Ela também avisa que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa um dos botões ou toca em ×.

No seu primeiro dia, uma mensagem de boas-vindas aparece no topo de Tarefas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo indica de quem ou do que ela trata, a organização quando for relevante (não apenas porque alguém trabalha nela), o projeto, se é Trabalho ou Pessoal e quando chegou. Toque em um nome para abrir a página dessa pessoa no Graph.

Os nomes de pessoas e organizações mostram uma foto ou um logotipo quando há um disponível no Graph. Caso contrário, aparecem as iniciais. Um logotipo difícil de ler em tamanho pequeno, como letras brancas em um fundo transparente ou uma marca muito larga, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato por e-mail há 12 dias; nenhuma novidade desde então". Ela aparece quando a última conversa com a pessoa é antiga ou não teve resposta e informa os canais que não estão conectados, como o WhatsApp. Sua Machine diz o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, toque em Conectar ao lado dele para abrir essa conexão.

O título diz o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como terminou, como "Concluído: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho considera a contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha avisa, por exemplo: "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem. Ela sai quando uma atualização substitui o rascunho.

Uma conversa (Slack, WhatsApp, Telegram, Intercom…) aparece como uma única sequência, da mensagem mais antiga à mais recente: as mensagens anteriores à que originou a tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa é identificada como "Esta tarefa" e fica aberta. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo da mensagem.

Uma mensagem também abre desse jeito na pesquisa, no Graph, nas respostas do Ask ou na última verificação, identificada como "Esta mensagem" (ou "Mensagens novas").

**Abrir no Gmail** abre o e-mail na conta do Gmail que o recebeu. No Android, ele abre no app Gmail, se você tiver o app instalado.

**Detalhes** de um e-mail mostram apenas o que não aparece no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver nada a acrescentar, a opção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a própria mensagem também abre essa visualização, com **Abrir no Slack** no fim.

**Detalhes** mostram o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. Toque no título para abrir o chat. Uma tarefa concluída continua compacta. A mensagem de origem fica em **Detalhes**.

Uma tarefa com o status "Aguardando" inclui um link para sua última mensagem para a pessoa e para aquilo que você está esperando: "E-mail para Pat · ter.".

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, **+** no celular ou `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, ela vai para a área certa, de acordo com quem ou com o que ela trata. Ela também encontra o e-mail relacionado ao follow-up, inclusive mensagens mais antigas.

Feche o formulário antes de adicionar a tarefa para que o texto e as escolhas fiquem salvos na próxima vez. Os arquivos não ficam salvos. **Descartar** na mensagem remove o conteúdo.

- **Vence**: digite um dia ou horário, como "amanhã", "sexta que vem", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta com uma frequência definida. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada, como um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou outro serviço disponível na sua Machine. Pesquise por texto ou remetente. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, a câmera ao lado tira uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
