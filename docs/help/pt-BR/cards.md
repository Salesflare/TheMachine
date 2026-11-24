---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para sua aprovação. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 32c3a3e62b74548f
---
Sua Machine lê tudo o que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo assim:

- **Feito agora**: no topo, fica a última etapa que você confirmou, como um formulário ou problema, e que foi concluída enquanto você estava fora. Ela fica lá até você tocar em **Entendi**, por no máximo um dia. Seu celular também avisa.
- **Para você**: tudo o que está aguardando você, começando pelo que vence até amanhã. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (primeiro, você precisa decidir ou responder; quando o trabalho não pode continuar ou ser usado sem algo que só você tem, como um preço, uma informação ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não tiveram novidades por uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas cuja próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e as que não receberam resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, começando pelas mais recentes, com o momento em que foram concluídas, como "Concluída há 5 minutos". As tarefas que parecem já ter sido concluídas mostram **Parece feito**.

Depois que você envia, aparece uma nota curta indicando para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". Uma resposta que só promete fazer o trabalho, como "Envio até terça-feira", mantém a tarefa aberta: "Enviado. Mantido em aberto." **Abrir** leva você até ela. A busca encontra tarefas pelo título ou pela pessoa para quem foram enviadas, inclusive em Mais tarde e Feito.

Em **Para você**, primeiro aparecem os itens atrasados ou que vencem até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por fim, o restante. Dentro de cada grupo, os mais recentes vêm primeiro. Uma tarefa mantém sua posição enquanto sua Machine a prepara e quando é concluída: só o indicador muda. Nos outros grupos abertos, primeiro aparecem os itens atrasados ou que vencem até amanhã, e depois os mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que algo foi concluído, como "PR #3451 mesclado", mas a tarefa ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando a mensagem mostra que foi concluída, a tarefa é encerrada automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, ela fica aguardando você tocar em **Marcar como concluído**.

Uma tarefa que você já resolveu, por exemplo, respondendo pelo Gmail ou Slack, também é encerrada automaticamente. Uma resposta que diz que há um arquivo anexado quando não há nenhum não encerra a tarefa.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa informa isso claramente: "Esta pessoa não é Sam Lee." Ela mostra a pessoa pelo endereço de e-mail, nunca pelo nome usado na mensagem. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem a enviou.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra a etapa em **Aguardando:**. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde naquele dia, ou na manhã seguinte se o prazo já tiver passado. Ela informa quem ainda está sendo aguardado.

Quando uma tarefa depende de um resultado que outra pessoa precisa entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem mostrar o resultado. Então, é encerrada automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com **Escreva um lembrete curto** no chat. Para mudar o que conta como concluído, diga isso no chat.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas recentes apareçam primeiro depois de alguns dias fora. Não há novidades quando não chega uma mensagem nova e você não faz nada na tarefa, como mandar uma mensagem no chat, editar ou adiar. Só abrir a tarefa não conta.

Tarefas urgentes, com prazo próximo ou com um envio a caminho continuam em Para você. **Descartar tudo** marca como desnecessárias todas as tarefas de Mais antigos após uma confirmação. É o mesmo que fazer isso uma por uma com **Não precisa**, mas com uma única confirmação. Você pode usar **Desfazer**. Se uma tarefa tiver novidades, ela volta para Para você.

Uma tarefa que ninguém mexeu por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela fica recolhida em Volta mais tarde, e deixa de entrar na contagem do ícone do app e do resumo da manhã. Abrir a tarefa, mandar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou sem novidades e não tem tarefas em aberto pode receber uma tarefa com uma próxima etapa específica. Isso pode acontecer no máximo três vezes por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine fica em repouso, com a lista vazia. Enquanto verifica, ela acorda e avisa. Se uma verificação falhar ou atrasar, a mensagem informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou apenas um tipo. Seu celular e computador mostram a mesma opção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta para todas as tarefas. Um alerta sobre a própria Machine, como uma parte que fica reiniciando, não é de Trabalho nem Pessoal, então aparece apenas em Todos.

A linha no topo da lista também permite mudar direto para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do seu último resumo da manhã ou do fim do dia e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque para ler o resumo novamente. Com **Copiar**, você pode colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, para Trabalho e Pessoal ou só para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. Em **Detalhes**, **Projeto** permite mudar o projeto ou removê-lo. Veja [Tarefas de um projeto](projects.md#a-project-s-to-dos).

Em **Detalhes**, **Área** move uma tarefa para a outra área. O que ela pode ler e enviar também muda com ela. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa da outra área para continuar e todas as mensagens de origem estão lá, ela é movida automaticamente para essa área e continua. Caso contrário, aparece **Mover para Trabalho**, e nada é movido até você tocar nessa opção. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal é movida automaticamente quando sua Machine identifica a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e fica privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. Mensagens de outra das suas empresas vão para as tarefas dessa empresa. Uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o começo.

O trabalho que chega por uma conta pessoal, como uma mensagem de um cliente no WhatsApp, um pedido na sua caixa de entrada pessoal ou uma [promessa](promises.md) relacionada ao trabalho, é Trabalho desde o começo.

Uma tarefa que você moveu ou colocou em uma área sempre fica onde você colocou. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para a conversa de origem, mesmo depois de uma mudança de área, a menos que você escolha outro meio.

Uma tarefa Pessoal desse tipo ainda responde pelo endereço de trabalho para o qual o e-mail foi enviado e nunca aparece em um Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas aguardando, **Percorrer**, no cabeçalho de Para você, mostra cada uma por vez, na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc encerra. O cabeçalho informa quanto tempo isso leva no seu ritmo, como "cerca de 2 min".

No fim, aparece a quantidade de itens enviados ou encerrados e dos que ainda estão sendo preparados.

Uma tarefa que faz uma pergunta fica de fora: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens aguardando ou quando a mensagem mais antiga de alguém está aguardando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, em até uma hora.

À noite, da 00:00 às 06:30, as verificações pausam. As mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, as verificações mostram "Pausadas durante a noite. Serão atualizadas às 06:30". Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao ritmo normal até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes na hora. Se não houver tarefas em aberto, toque na linha da sua Machine para vê-la com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção aparece no topo da tela no computador. Uma mensagem curta aparece ali apenas enquanto uma verificação está em andamento ou se ela falhou ou atrasou. Você também pode pedir isso no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, aparece uma linha acima das tarefas com o que foi encontrado em todas as fontes lidas, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 tarefas novas". A mensagem se refere apenas a essa verificação: as tarefas que já estavam na lista continuam aguardando. Se uma tarefa nova ficar para um momento mais conveniente, como o resumo da manhã, a mensagem informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte. Você verá quem escreveu, o assunto ou as primeiras palavras, além da tarefa nova ou do motivo de não ter sido necessária, como "Você estava em cópia. Uma pessoa da equipe está respondendo" ou "A reunião já está marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação só encontrou um motivo vago. Toque em uma para ler a mensagem e o que foi dito ao redor dela.

As 10 primeiras aparecem de imediato. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), mostra quantas mensagens novas aquele chat tem. Uma notificação no celular sobre uma mensagem que já está na lista aparece apenas uma vez. A linha fica visível por 12 horas após a verificação.

A contagem inclui apenas os e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails que The Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, seu período de teste ou um convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que deve ser alterado: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como concluído** indica que a tarefa foi resolvida. A opção aparece à vista em uma tarefa pronta sem rascunho ou em uma tarefa que faz uma pergunta. Nos outros casos, fica no topo de **…**. A tarefa sai da lista na hora, com a opção **Desfazer** na mensagem. Deslize a mensagem para tirá-la da tela ou arraste-a para fora com o mouse para encerrá-la mais rápido. A alteração continua valendo.

Para fazer de outro jeito, diga como no **Chat** da tarefa. A resposta informa apenas o que mudou, como o adiamento e até quando. Se não foi possível mudar algo, como o prazo, ela avisa.

Em **…**:

- **Passar…**: atribua a tarefa a alguém da equipe, a [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta em um intervalo regular](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, por exemplo: "Renomeie para…". O título escolhido por você permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando acontece algo novo, como uma mensagem nova da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece entre as novas. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar, em qualquer país, vira uma tarefa com o valor, o prazo e os dados de pagamento indicados na conta. Contas pagas automaticamente, como débito automático ou cartão já cadastrado, não viram tarefas. Quando um e-mail posterior informa que ela foi paga, por exemplo, quando o remetente confirma o recebimento do pagamento, a tarefa é encerrada automaticamente. **Desfazer** traz de volta por um dia.

Uma tarefa que só era importante até certo horário, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / descartado** com o status "Não é mais necessário". **Desfazer** traz de volta por um dia.

Antes de uma mensagem ou de um repasse para alguém aparecer como pronto, sua Machine verifica suas conversas recentes com as pessoas envolvidas, incluindo conversas em grupo, e aguarda a leitura do Slack. Quando uma mensagem posterior mostra que o assunto já foi resolvido, por exemplo, quando alguém recebeu o pedido e aceitou, a tarefa é encerrada automaticamente. **Desfazer** traz de volta por um dia.

Se outra pessoa escrever na mesma conversa depois que o rascunho ficar pronto, **Enviar** pausa o envio: "Não enviado: chegou uma mensagem nova na conversa". A tarefa mostra essa mensagem com **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa em outro local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda é necessária acompanha os novos planos. Uma tarefa que não tem mais nada a fazer vai para **Feito / descartado** como "Não precisa". No chat, aparece "Atualizado:" com o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**. Ela também explica que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão correspondente ou toca em ×.

No seu primeiro dia, uma mensagem de boas-vindas aparece no topo de Tarefas e informa quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro para já estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem se trata, a organização quando o assunto é sobre ela, mas não só porque a pessoa trabalha lá, o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Os nomes e as organizações mostram a foto ou o logotipo, se houver no Graph, e as iniciais quando não houver. Um logotipo que não fique legível nesse tamanho, como texto branco em fundo transparente ou uma marca muito larga, também é substituído pelas iniciais.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato por e-mail há 12 dias. Nenhuma novidade desde então." Ela aparece quando o último contato com a pessoa é antigo ou não foi respondido e indica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de tentar adivinhar.

Quando a linha menciona um canal que não está conectado, **Conectar**, ao lado dele, abre a conexão correspondente.

O título informa o que precisa ser feito e só muda quando isso também muda. Uma tarefa concluída mantém o título e mostra abaixo como terminou, como "Concluída: Sam assinou na terça-feira".

Uma linha discreta acima do rascunho identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino para você saber de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem. Ela desaparece quando uma atualização substitui o rascunho.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mais antiga para a mais recente: as mensagens anteriores àquela sobre a qual a tarefa trata e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa aparece marcada como "Esta tarefa" e fica aberta na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo da mensagem.

Uma mensagem também pode ser aberta do mesmo jeito pela busca, pelo Graph, pelas respostas do Ask ou pela última verificação. Ela aparece marcada como "Esta mensagem" ou "Mensagens novas".

**Abrir no Gmail** abre o e-mail na conta do Gmail em que chegou. No Android, ele abre no app do Gmail, se você tiver o app.

Em **Detalhes**, um e-mail mostra apenas as informações que não aparecem no cabeçalho, como endereços completos em Cc, Bcc ou um endereço de resposta diferente. Se não houver mais informações, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a mensagem de origem também abre a mensagem aqui, com **Abrir no Slack** no fim.

**Detalhes** mostra o nome, o projeto e a área, que você pode alterar tocando neles, além da sua última observação e do resultado de um agente de programação. O título abre o chat. Uma tarefa concluída aparece de forma resumida. A mensagem de origem fica em **Detalhes**.

Uma tarefa com o status "Aguardando" tem um link para sua última mensagem para a pessoa, aquela cuja resposta você espera: "E-mail para Pat · ter.".

## Criar uma tarefa

**Nova tarefa**, em **Pesquisar** no computador, **+** no celular ou `N`, cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não selecionar **Trabalho** ou **Pessoal**, ela vai para a área certa com base em quem e no que se trata. Ela também encontra o e-mail relacionado ao follow-up, mesmo que seja antigo.

- **Prazo**: digite um dia ou horário, como "amanhã", "próxima sex.", "3 nov.", "14h" ou "daqui a 2 horas". Você também pode digitar no seu idioma. O ícone do calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta em um intervalo regular. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa. Pode ser um e-mail, mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que The Machine tenha. Pesquise pelo texto ou remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa usando um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
