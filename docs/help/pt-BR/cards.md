---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber seu ok. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: b218e3423a2162c5
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza as tarefas assim:

- **Feito agora**: no topo, fica uma última etapa que você confirmou, como um formulário ou uma questão, que foi concluída enquanto você estava ausente. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e também aparece no seu celular.
- **Para você**: tudo que está esperando por você, começando pelo que vence até amanhã. Cada tarefa indica **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (primeiro, ela precisa da sua decisão ou resposta; quando o trabalho não pode continuar ou ser usado sem algo que só você tem, como um preço, uma informação ou uma escolha, uma linha abaixo do título explica o que é), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou informe, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não recebem nada novo há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas cuja próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas, mensagens que [vão ser enviadas mais tarde](send-later.md) e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, da mais recente para a mais antiga, com o horário em que foram concluídas, como “Feito há 5 minutos”. Tarefas que parecem já estar concluídas recebem a marca **Parece feito**.

Depois que você envia, uma nota curta mostra para onde a tarefa foi, como “Enviado. Movido para Feito.” ou “Enviado. Movido para Mais tarde até seg.”. Uma resposta que só promete concluir o trabalho, como “Envio até terça-feira”, mantém a tarefa aberta: “Enviado. Mantido em aberto.” **Abrir** leva você até ela. A busca encontra tarefas pelo título ou pela pessoa para quem foram enviadas, inclusive em Mais tarde e Feito.

Em **Para você**, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por fim, o restante. Dentro de cada grupo, a mais recente aparece primeiro. A tarefa mantém o lugar enquanto sua Machine a prepara e quando ela é concluída: só a marca muda. Nos outros grupos abertos, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, e depois as mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine vê que a tarefa foi concluída, como “PR #3451 aprovado”, mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando a marca aparece em uma mensagem, a tarefa é encerrada automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, ela espera que você toque em **Marcar como feita**.

Uma tarefa que você já resolveu por conta própria, por exemplo, respondendo pelo Gmail ou pelo Slack, também é encerrada automaticamente. Uma resposta que diz que há um arquivo anexado, quando não há, não encerra a tarefa.

Quando uma mensagem vem de um endereço que parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa deixa isso claro: “Esta pessoa não é Sam Lee.” Ela mostra o endereço real da pessoa, nunca o nome usado por quem enviou a mensagem. Sua Machine verifica a mensagem com a pessoa do endereço que você já conhece, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou uma resposta, indica **Aguardando:** essa etapa. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: ela volta na manhã anterior ao prazo, no horário do prazo se ele for mais tarde no mesmo dia, ou na manhã seguinte se o prazo já tiver passado. A tarefa também indica de quem ainda está esperando.

Quando uma tarefa depende de um resultado que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, é encerrada automaticamente com o resultado e a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com a opção **Escreva um lembrete curto** no chat. Para mudar o que conta como concluído, fale com a assistente no chat.

Antes de encerrar a tarefa, sua Machine compara o resultado com o que foi combinado na conversa, como o preço, o texto ou o link que você enviou. Ela só encerra a tarefa quando tudo corresponde, e informa o que verificou. Se algo estiver diferente, se a outra pessoa tiver ignorado seu ok ou se a sua parte de uma troca ainda estiver em aberto, a tarefa volta e explica o motivo.

Quando o resultado aparecer em uma página pública da web mencionada nas mensagens, como um artigo que vai listar você, sua Machine acessa essa página na hora de cobrar a pessoa. Se o resultado estiver lá e não estivesse quando a tarefa começou a aguardar, ela também verifica a página antes de encerrar a tarefa. Sua Machine só lê a página, como qualquer visitante, e nunca envia nada.

Se o resultado não estiver na página e o prazo ainda não tiver chegado, sua Machine acessa a página mais uma vez na manhã seguinte ao prazo. Caso contrário, a tarefa volta como antes, com a indicação “Verificado” ou “Não foi possível abrir” e a página no chat.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas recentes apareçam primeiro quando você voltar depois de alguns dias. Considera-se que não há novidades quando não chega nenhuma mensagem nova e você não faz nada na tarefa, como enviar uma mensagem no chat, editar ou adiar. Só abrir a tarefa não conta.

Tarefas urgentes, que vencem em breve ou que têm um envio em andamento continuam em Para você. **Descartar tudo** marca todas as tarefas em Mais antigos como não necessárias com uma única confirmação. **Não precisa** faz isso para uma tarefa por vez, com a opção **Desfazer**. Se algo novo acontecer em uma tarefa, ela volta para Para você.

Uma tarefa que ninguém tocou por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, ela é recolhida em Volta mais tarde, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nada em aberto pode gerar uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e a lista fica vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra a opção **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou apenas um tipo. No celular e no computador, a seleção é a mesma. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta a mostrar todas as tarefas. Um alerta sobre a própria Machine, como uma peça que fica reiniciando, não é de Trabalho nem Pessoal e aparece apenas em Todos.

A linha no topo da lista também leva direto à outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista identifica o resumo mais recente da manhã ou da noite e mostra o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque na linha para ler o resumo novamente. Use **Copiar** para colar em qualquer lugar. Depois que você abre o resumo ou toca no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, em Trabalho e Pessoal ou apenas na categoria selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque no nome para abrir o projeto. **Projeto**, em **Detalhes**, permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para a outra área. O que ela pode ler e enviar muda junto. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa estar na outra área para continuar e todas as mensagens de origem estão lá, ela é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada é movido até você tocar na opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal é movida automaticamente quando sua Machine encontra a área certa. Até lá, ela não aparece em Trabalho nem em Pessoal e fica privada.

Uma tarefa sempre pode ler as mensagens de onde veio. Quando precisa de outras mensagens da outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você identificou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa, e uma tarefa sobre sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega por uma conta pessoal, como um cliente no WhatsApp, um pedido na sua caixa de entrada pessoal ou uma [promessa](promises.md) sobre trabalho, é Trabalho desde o início.

Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a deixou. Trabalho ou Pessoal define onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para a conversa original, mesmo depois de uma mudança de área, a menos que você escolha outra opção.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho em que o e-mail chegou e nunca aparece em um Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas aguardando, **Percorrer**, no cabeçalho de Para você, mostra uma por vez, na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc encerra. O cabeçalho informa quanto tempo o processo leva no seu ritmo, como “cerca de 2 min”.

No fim, o resumo conta o que foi enviado ou encerrado e o que ainda está sendo preparado.

Uma tarefa que faz uma pergunta para você não entra nesse processo: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações pausam. As mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a seção Verificações diz “Pausadas durante a noite. Atualizadas às 06:30”. Se você clicar, digitar ou rolar a tela no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas em aberto, toque na linha da sua Machine para vê-la, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção fica no topo da página no computador. Uma linha curta aparece ali apenas enquanto uma verificação está em andamento ou quando ela falhou ou atrasou. Você também pode perguntar no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas mostra o que foi encontrado em todas as fontes verificadas, como “13 mensagens verificadas às 16:11 · nenhuma tarefa nova” ou “· 2 tarefas novas”. A linha se refere apenas àquela verificação: as tarefas que já estavam na lista continuam como estavam. Quando uma tarefa nova precisa esperar por um momento melhor, como o resumo da manhã, a linha informa até quando: “1 tarefa adiada até amanhã às 08:30”.

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras, além da nova tarefa ou do motivo para não criar uma, como “Você estava em cópia, uma pessoa da equipe está respondendo” ou “Reunião já marcada para quinta-feira”. Uma conversa não mostra um motivo quando a verificação encontrou apenas um motivo vago. Toque em uma mensagem para lê-la junto com o contexto.

As 10 primeiras aparecem de início. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação do Android sobre uma mensagem que já está na lista aparece apenas uma vez. A linha fica disponível por 12 horas depois da verificação.

A contagem inclui apenas os e-mails enviados para você. Suas respostas são lidas para entender o contexto e as promessas, mas não contam como e-mails novos. Os e-mails da própria The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que mudar: como fazer a tarefa ou, quando o rascunho estiver pronto, o que mudar nele. Se você deixar o texto pela metade, ele estará ali quando voltar. **Cancelar** descarta o texto.

**Marcar como feita** indica que a tarefa foi resolvida. No computador, ela fica junto dos outros botões quando cabe em uma linha. No celular, fica visível em uma tarefa pronta sem rascunho ou em uma que faz uma pergunta. Nos outros casos, aparece no topo de **…**. A tarefa sai da lista imediatamente, com a opção **Desfazer** na mensagem. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para encerrá-la mais rápido. A alteração permanece.

Para concluir a tarefa de outro jeito, diga como no **Chat**. A resposta informa apenas o que mudou, como o adiamento e até quando. Se não foi possível mudar algo, como a data de vencimento, a resposta avisa.

Em **…**:

- **Passar…**: encaminhe a tarefa para alguém da equipe, para [Claude Code ou Codex](hand-to-agent.md) ou [peça para alguém revisar](ask-to-review.md).
- **Repetir…**: a tarefa [volta periodicamente](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, por exemplo: “Renomeie para …”. O título escolhido permanece.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando algo novo acontece, como uma mensagem nova da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e é ordenada como nova. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior confirma o pagamento, por exemplo, o remetente confirma que recebeu o valor, a tarefa é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só era importante até determinado horário, como uma confirmação antes de uma reunião, é encerrada automaticamente depois desse horário. Ela vai para **Feito / descartado** com a indicação “Não é mais necessário”. **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de um repasse para alguém aparecer como pronto, sua Machine verifica os chats recentes que você teve com as pessoas envolvidas, inclusive chats em grupo, e espera que o Slack os leia. Se uma mensagem posterior mostrar que a tarefa já foi resolvida, por exemplo, se a pessoa recebeu o pedido e aceitou, ela é encerrada automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escrever na mesma conversa depois que o rascunho for criado, **Enviar** pausa o envio: “Não enviado: há uma mensagem nova na conversa”. A tarefa mostra essa mensagem com as opções **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de local ou uma reserva cancelada, The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda é necessária segue o novo plano. Uma tarefa sem nada a fazer vai para **Feito / descartado** com a indicação “Não precisa”. O chat mostra “Atualizado:” e o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**. Ela também explica que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa um dos botões ou toca em ×.

No primeiro dia, o topo da página Tarefas dá boas-vindas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro, para ficar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo indica de quem se trata, a organização quando for relevante (não apenas porque alguém trabalha nela), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Nomes e organizações mostram a foto ou o logotipo, se houver um no Graph, ou as iniciais. Se um logotipo não puder ser lido naquele tamanho, como um texto branco em fundo transparente ou uma marca muito larga, as iniciais aparecem no lugar.

Às vezes, uma linha discreta informa o que não se sabe, como “Último contato há 12 dias por e-mail. Nenhuma novidade desde então.” Ela aparece quando o último contato com a pessoa é antigo ou não teve resposta, e menciona canais que não estão conectados, como o WhatsApp. Sua Machine diz o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, **Conectar**, ao lado, abre a conexão correspondente.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com a forma como foi encerrada logo abaixo, como “Concluída: Sam assinou na terça-feira”.

Acima do rascunho, uma linha discreta identifica a mensagem de origem com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para que você veja de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como “Com base na sugestão de Sam em #ops”. Toque nela para ler a mensagem. Ela desaparece quando uma atualização substitui o rascunho.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela que originou a tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa tem a marca “Esta tarefa” e é aberta na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo dele.

Uma mensagem é aberta do mesmo jeito na busca, no Graph, nas respostas do Ask ou na última verificação, com a marca “Esta mensagem” ou “Mensagens novas”.

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, ele abre no app Gmail, se estiver instalado.

Em **Detalhes**, um e-mail mostra apenas as informações que não aparecem no cabeçalho, como os endereços completos de Cc, Bcc ou um endereço diferente para respostas. Se não houver outras informações, nada aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a mensagem original também a abre aqui, com **Abrir no Slack** no fim.

**Detalhes** mostra o nome, o projeto e a área (toque em um deles para mudar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída fica resumida; a mensagem que a originou aparece em **Detalhes**.

Uma tarefa com a indicação “Aguardando” inclui um link para sua última mensagem à pessoa, aquela que você está aguardando: “E-mail para Pat · ter”.

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, em **+** no celular ou em `N`) cria uma tarefa para qualquer coisa. Criá-la não envia nada. Se você não selecionar **Trabalho** ou **Pessoal**, a tarefa vai para a área certa de acordo com quem ou com o que ela trata. Ela também encontra o e-mail relacionado ao follow-up, mesmo que seja antigo.

Se você fechar a tarefa antes de adicioná-la, o texto e as escolhas ficarão salvos para a próxima vez, mas os arquivos não. **Descartar** na mensagem remove o conteúdo.

- **Vence**: digite um dia ou horário, como “amanhã”, “próxima sex.”, “3 nov.”, “14h” ou “daqui a 2 horas”. Você também pode escrever no seu idioma. O ícone do calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta periodicamente. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa: um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem disponível na The Machine. Pesquise por texto ou remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, a câmera ao lado tira uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê enquanto trabalha nela. Os arquivos bastam para criar uma tarefa: ela é preenchida a partir de um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
