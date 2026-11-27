---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que significa cada parte de uma tarefa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: dfbc7ccc7313ecfe
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde as tarefas ficam

A página **Tarefas** organiza tudo assim:

- **Feito agora**: no topo, mostra uma última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema, concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia. Você também recebe uma notificação no celular.
- **Para você**: tudo que está esperando por você, primeiro o que vence até amanhã. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (primeiro, ela precisa de uma decisão ou resposta sua; quando o trabalho não pode continuar ou ser usado sem algo que só você tem, como um preço, uma informação ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas, sem novidades há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas, mensagens [programadas para mais tarde](send-later.md) e tarefas sem resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, da mais recente para a mais antiga, com o horário em que foram concluídas, como "Concluída há 5 minutos". Tarefas que parecem já estar concluídas aparecem marcadas como **Parece feito**.

Depois que você envia algo, uma nota curta informa para onde a tarefa foi, como "Enviado. Movida para Feito." ou "Enviado. Movida para Mais tarde até seg.". Uma resposta que só promete fazer o trabalho, como "Envio até terça", mantém a tarefa em aberto: "Enviado. Mantida em aberto." **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou pelo destinatário, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por fim, o restante. Em cada grupo, as tarefas mais recentes aparecem primeiro. Uma tarefa mantém o lugar enquanto sua Machine a prepara e quando ela é concluída. Só a marca muda. Nos outros grupos abertos, as tarefas atrasadas ou que vencem até amanhã aparecem primeiro, seguidas das mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebe que a tarefa foi concluída, como "PR #3451 mesclado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista e ajuda sua Machine a aprender. Essas tarefas nunca aparecem como atrasadas. Quando a mensagem mostra que a tarefa foi concluída, ela é encerrada automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, ela espera você tocar em **Marcar como feito**.

Uma tarefa que você já resolveu por conta própria, por exemplo respondendo no Gmail ou no Slack, também é encerrada automaticamente. Uma resposta que diz que um arquivo está anexado quando não está não encerra a tarefa.

Quando uma mensagem vem de um endereço que parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa deixa isso claro: "Esta pessoa não é Sam Lee." Ela identifica a pessoa pelo endereço de e-mail, nunca pelo nome que ela usou. Sua Machine confirma a mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde naquele dia, ou na manhã seguinte quando o prazo já passou. Ela informa quem ainda precisa responder.

Quando a tarefa depende de um resultado que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, é encerrada automaticamente com o resultado e a opção **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com **Escreva um lembrete curto** no chat. Para mudar o que conta como concluído, explique no chat.

Quando o resultado aparecer em uma página pública da web mencionada nas mensagens, como um artigo que vai listar você, sua Machine consulta a página na hora de cobrar. Se o resultado aparecer lá e não aparecia quando a tarefa começou a aguardar, ela é encerrada automaticamente, informa o resultado e mostra a opção **Desfazer**. Sua Machine só consulta a página, como qualquer visitante, e nunca envia nada.

Se o resultado não aparecer na página e o prazo ainda não tiver chegado, sua Machine consulta a página novamente na manhã seguinte ao prazo. Caso contrário, a tarefa volta como antes, com "Verificado" ou "Não foi possível abrir" e a página no chat.

Uma tarefa sem novidades por uma semana passa de Para você para **Mais antigos**, para que as tarefas novas apareçam primeiro depois de alguns dias fora. Não há novidades quando não chega nenhuma mensagem nova e você não faz nada na tarefa, como enviar uma mensagem no chat, editar ou adiar. Só olhar não conta.

Tarefas urgentes, que vencem em breve ou com um envio a caminho continuam em Para você. **Descartar tudo** marca todas as tarefas em Mais antigos como desnecessárias depois de uma confirmação, como **Não precisa** faz com uma tarefa de cada vez, com a opção **Desfazer**. Se algo novo acontecer em uma tarefa, ela volta para Para você.

Uma tarefa que ninguém tocou por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, a tarefa fica recolhida em Volta mais tarde, e deixa de contar no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nenhuma tarefa em aberto pode receber uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e mostra uma lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, uma linha informa isso, com a opção **Verificar agora** abaixo.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou só um tipo. O celular e o computador mostram a mesma opção selecionada. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta a mostrar todas as tarefas. Um alerta sobre a própria Machine, como uma peça que fica reiniciando, não é de Trabalho nem Pessoal e aparece só em Todos.

A linha no topo da lista também leva direto para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o último resumo da manhã ou do fim do dia e quantas tarefas ele incluiu, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque para ler o resumo de novo e use **Copiar** para colar onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, em Trabalho e Pessoal ou só na opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move a tarefa para a outra área. O que ela pode ler e de onde pode enviar mensagens também muda. **Desfazer**, na notificação, leva a tarefa de volta.

Quando uma tarefa precisa da outra área para continuar e todas as mensagens de origem estão lá, ela é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando sua Machine encontra a área certa. Até lá, ela não aparece em Trabalho nem em Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Um e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outras empresas suas vão para as tarefas daquela empresa, e uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para o endereço de trabalho, é Pessoal desde o começo.

Um assunto de trabalho que chega a uma conta pessoal, como uma mensagem de um cliente no WhatsApp, um pedido na sua caixa de entrada pessoal ou uma [promessa](promises.md) sobre trabalho, é de Trabalho desde o começo.

Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a deixou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança de área, a não ser que você escolha outro jeito.

Uma tarefa Pessoal desse tipo ainda responde pelo endereço de trabalho em que o e-mail chegou e nunca aparece em um Fleet de Trabalho ou no Graph da equipe.

Quando há duas ou mais tarefas aguardando, **Percorrer**, no cabeçalho de Para você, mostra cada uma por vez, na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo elas levam no seu ritmo, como "cerca de 2 min".

No final, o app mostra quantas tarefas foram enviadas ou encerradas e quantas ainda estão sendo preparadas.

Uma tarefa que faz uma pergunta fica de fora: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens ou quando a mensagem mais antiga de alguém está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, entre 00:00 e 06:30, as verificações são pausadas. As mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. A seção Verificações, em Conexões, mostra "Pausada durante a noite. As mensagens serão verificadas às 06:30". Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações continuam normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas em aberto, toque na linha da sua Machine para ver **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção aparece no topo da tela do computador. Uma linha curta aparece ali somente enquanto uma verificação está em andamento ou quando ela falha ou atrasa. Você também pode perguntar no chat.

LinkedIn, X e Salesflare mantêm o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que encontrou em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 tarefas novas". Ela se refere só a essa verificação: as tarefas que já estavam na sua lista continuam como estavam. Quando uma tarefa nova fica para um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã, às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação com o ícone do serviço de origem: quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo de não ser necessário fazer nada, como "Você só estava em cópia. Uma pessoa da equipe está respondendo" ou "A reunião já está marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação apresentou um motivo vago. Toque em uma mensagem para lê-la junto com o contexto.

As primeiras 10 mensagens aparecem na lista. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas há naquele chat. Uma notificação do Android sobre uma mensagem que já aparece na lista é exibida só uma vez. A linha fica visível por 12 horas após a verificação.

A contagem inclui apenas e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails da The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que deve ser alterado: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. Se você começar a escrever e sair antes de terminar, o texto vai estar lá quando voltar. **Cancelar** descarta o texto.

**Marcar como feito** significa que a tarefa foi resolvida. No computador, essa opção aparece junto com os outros botões quando eles cabem em uma linha. No celular, ela fica visível em uma tarefa pronta sem rascunho ou que faz uma pergunta. Nos outros casos, aparece no topo de **…**. A tarefa sai da lista na hora, com a opção **Desfazer** na notificação. Deslize a notificação para o lado ou arraste-a com o mouse para encerrá-la mais rápido. A alteração permanece.

Para concluir de outro jeito, explique no **Chat** da tarefa. A resposta indica apenas o que mudou, como o adiamento e até quando. Se não for possível mudar algo, como o prazo, ela avisa.

Em **…**:

- **Passar…**: atribua a tarefa a uma pessoa da equipe, a [Claude Code ou Codex](hand-to-agent.md), ou [peça para alguém revisar](ask-to-review.md).
- **Repetir…**: a tarefa [volta em intervalos regulares](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha um motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir no chat, por exemplo: "Renomeie para …". O título que você escolher permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa informa quando voltou e aparece como nova na lista. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, o prazo e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior confirma o pagamento, como uma mensagem do remetente confirmando que recebeu, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até determinado horário, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / descartado** com o motivo "Não é mais necessário". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de um repasse para outra pessoa aparecer como pronto, sua Machine verifica as conversas recentes que você teve com as pessoas envolvidas, inclusive em chats em grupo, e espera o Slack ler as mensagens. Quando uma mensagem posterior mostra que a tarefa já foi resolvida, como quando pediram algo a alguém e essa pessoa aceitou, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escrever na mesma conversa depois que o rascunho for criado, **Enviar** pausa o envio e mostra: "Não enviado: há uma mensagem nova na conversa". A tarefa mostra a mensagem, com as opções **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa em outro local ou uma reserva cancelada, a The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda importa acompanha os novos planos. Se não houver mais nada a fazer, ela vai para **Feito / descartado** com o motivo "Não precisa". No chat, aparece "Atualizada:" com o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**. Ela também explica que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão ou toca em ×.

No seu primeiro dia, o topo de Tarefas dá as boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem ou do que se trata, a organização quando for relevante (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página dessa pessoa no Graph.

Os nomes e as organizações mostram uma foto ou um logotipo quando há um disponível no Graph. Caso contrário, mostram as iniciais. Se o logotipo não ficar legível nesse tamanho, como uma imagem branca em fundo transparente ou uma marca muito larga, as iniciais também aparecem.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato por e-mail há 12 dias. Nenhuma novidade desde então". Ela aparece quando o último contato com a pessoa é antigo ou não teve resposta, e indica canais que não estão conectados, como o WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, toque em Conectar ao lado dele para abrir a conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com a forma como terminou logo abaixo, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem que deu origem à tarefa, com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do serviço para o qual será enviado, para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho depende da contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem. Ela desaparece quando uma atualização substitui o rascunho.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas que vieram depois. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa aparece marcada como "Esta tarefa" e é aberta na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Um e-mail mostra o restante da conversa recolhido acima e abaixo dele.

Uma mensagem também abre desse jeito na pesquisa, no Graph, nas respostas do Ask ou na última verificação, marcada como "Esta mensagem" (ou "Mensagens novas").

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, abre no app do Gmail se estiver instalado.

Em um e-mail, **Detalhes** mostra apenas as informações que não aparecem no cabeçalho, como os endereços completos em Cc, Bcc ou outro endereço para resposta. Se não houver nada a acrescentar, essa opção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a mensagem de origem também abre essa mensagem aqui, com **Abrir no Slack** na parte de baixo.

**Detalhes** mostram o nome, o projeto e a área da tarefa (toque em um deles para mudar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída fica resumida. A mensagem que deu origem a ela aparece em **Detalhes**.

Uma tarefa com a indicação "Aguardando" leva à sua última mensagem para a pessoa, aquela cuja resposta você está esperando, como "E-mail para Pat · ter.".

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, em **+** no celular ou por `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não selecionar **Trabalho** ou **Pessoal**, ela vai para a área certa conforme quem ou o que está envolvido. Ela também encontra o e-mail relacionado ao follow-up, mesmo que seja antigo.

Se você fechar antes de adicionar a tarefa, o texto e as opções ficam salvos para a próxima vez. Os arquivos não. **Descartar** na mensagem remove o texto e as opções.

- **Vence**: digite um dia ou horário, como "amanhã", "próxima sex.", "3 nov.", "14h" ou "daqui a 2 horas". Você também pode escrever no seu idioma. O ícone de calendário oferece opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta em intervalos regulares. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa. Pode ser um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que a The Machine tenha. Pesquise por texto ou remetente. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam na tarefa, e a The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
