---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para receber sua aprovação. Entenda o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 4209ed807e753101
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo:

- **Feito agora**: no topo, mostra uma última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema, concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e também aparece no seu celular.
- **Para você**: tudo que está esperando por você, começando pelo mais urgente. Cada tarefa indica **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (é preciso decidir ou responder antes; quando o trabalho parou por algo que só você tem, como uma informação, um login ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nisso) ou **Para ler** (um resumo ou informativo, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não recebem nada novo há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, da mais recente para a mais antiga, com o horário em que foram concluídas, como "Concluída há 5 minutos". Tarefas que parecem já estar concluídas aparecem como **Parece feito**.

Depois que você envia, uma nota curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg." Uma resposta que só promete fazer o trabalho, como "Vou enviar até terça-feira", mantém a tarefa aberta: "Enviado. Mantido em aberto." **Abrir** leva você até a tarefa. A pesquisa encontra tarefas pelo título ou por quem recebeu a mensagem, inclusive em Mais tarde e Feito.

**Para você** mostra primeiro o que está atrasado ou vence até amanhã, depois as perguntas do seu Fleet, depois os follow-ups de um quadro e, por fim, o restante. Em cada grupo, as tarefas mais recentes aparecem primeiro. Uma tarefa mantém a posição enquanto sua Machine a prepara e quando é concluída: só a marca muda. Nos outros grupos abertos, o que está atrasado ou vence até amanhã aparece primeiro, e o restante fica em ordem da tarefa mais recente para a mais antiga. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine vê que a tarefa foi concluída, como "PR #3451 integrado", mas ela ainda não foi fechada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem mostra que ela foi concluída, a tarefa se fecha sozinha depois de um dia, com a opção **Desfazer**. Caso contrário, ela espera você tocar em **Marcar como feito**. Uma tarefa que você já resolveu por conta própria, como responder no Gmail ou no Slack, também se fecha sozinha.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa avisa claramente: "Esta pessoa não é Sam Lee." Ela mostra o endereço verdadeiro, nunca o nome usado pela pessoa. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda espera por outra pessoa, como uma revisão ou resposta, indica **Aguardando:** essa etapa. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde naquele dia, ou na manhã seguinte quando o prazo já passou. Ela informa quem ainda precisa responder.

Quando uma tarefa depende de um resultado que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar a sua parte não fecha a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem mostrar o resultado, quando se fecha sozinha, com a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para alterar isso.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as mais recentes apareçam primeiro quando você voltar depois de alguns dias. Não há novidades quando não chega nenhuma mensagem nova nem você faz nada na tarefa, como enviar uma mensagem no chat, editar ou adiar. Só olhar a tarefa não conta.

Tarefas urgentes, com prazo próximo ou com um envio a caminho continuam em Para você. **Descartar tudo** marca todas as tarefas em Mais antigos como desnecessárias depois de uma confirmação, assim como **Não precisa** faz uma tarefa por vez, com a opção **Desfazer**. Se algo novo acontecer em uma tarefa, ela volta para Para você.

Uma tarefa que ninguém tocou por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** fecha a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela nunca mais pergunta. Se não houver resposta por mais uma semana, a tarefa é recolhida em Volta mais tarde, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nenhuma tarefa aberta pode receber uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa com a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou apenas um tipo. Seu celular e computador mostram a mesma opção selecionada. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta para a lista completa. Um alerta sobre a sua Machine, como uma peça que fica reiniciando, não é de Trabalho nem Pessoal e aparece somente em Todos.

A linha no topo da lista também permite mudar direto para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do seu último resumo da manhã ou do fim do dia e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 abertas. Toque nela para ler o resumo de novo e use **Copiar** para colar onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que ainda está aberto, para Trabalho e Pessoal ou somente para a opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto** em **Detalhes** permite mudar o projeto ou removê-lo. Veja [tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área** em **Detalhes** move uma tarefa para a outra área. O que ela pode ler e enviar também muda. **Desfazer** na nota leva a tarefa de volta.

Quando uma tarefa precisa da outra área para continuar e todas as mensagens de origem estão lá, ela é movida para essa área e continua sozinha. Caso contrário, aparece **Mover para Trabalho**, e nada é movido até você tocar nessa opção. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal é movida sozinha assim que encontra a área correta. Até lá, ela não aparece em Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa, e uma tarefa sobre sua vida pessoal, como uma mensagem da família enviada para o seu endereço de trabalho, é Pessoal desde o início.

Um trabalho que chega a você por uma conta pessoal, como uma mensagem de cliente no WhatsApp, um pedido na sua caixa de entrada pessoal ou uma [promessa](promises.md) sobre trabalho, é de Trabalho desde o início.

Uma tarefa que você moveu ou colocou em uma área sempre fica onde você a colocou. Trabalho ou Pessoal define onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para onde está a conversa, mesmo depois de uma mudança, a menos que você escolha outra opção.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho em que o e-mail chegou e nunca aparece em um Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas esperando, **Percorrer** no cabeçalho de Para você passa por elas uma de cada vez, na ordem da lista, mostrando cada rascunho completo com **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo isso leva no seu ritmo, como "cerca de 2 min".

No fim, ele conta o que foi enviado ou fechado e o que ainda está sendo preparado.

Uma tarefa que faz uma pergunta para você não entra nessa sequência: ela espera sua resposta, não um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, em até uma hora.

À noite, entre 00:00 e 06:30, as verificações ficam pausadas: as mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, as verificações mostram "Pausadas durante a noite, retomadas às 06:30". Se você clicar, digitar ou rolar o app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre faz uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas abertas, toque na linha da sua Machine para vê-la, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas abertas, a opção aparece no topo no computador. Uma linha curta aparece ali somente enquanto uma verificação está em andamento ou quando ela falha ou atrasa. Você também pode perguntar no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das suas tarefas informa o que encontrou em todas as fontes que leu, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 tarefas novas". Ela se refere somente àquela verificação: as tarefas que já estavam na sua lista continuam esperando como antes. Quando uma tarefa nova fica esperando por um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa adiada até amanhã às 08:30".

Toque na linha para ver cada conversa de e-mail, chat e notificação, com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo de não precisar de nada, como "Você estava em cópia, uma pessoa da equipe está respondendo" ou "A reunião já está marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação encontrou apenas um motivo genérico. Toque em uma delas para ler a mensagem e o que foi dito ao redor.

As 10 primeiras aparecem de início. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação do celular sobre uma mensagem que já aparece na lista é mostrada apenas uma vez. A linha fica visível por 12 horas após a verificação.

A contagem inclui apenas e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como novos e-mails. Os e-mails que The Machine envia para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** informa o que alterar: como fazer a tarefa ou, quando um rascunho estiver pronto, o que mudar nele. **Marcar como feito** indica que a tarefa foi resolvida: aparece à vista em uma tarefa pronta sem rascunho ou em uma tarefa que faz uma pergunta para você; caso contrário, fica no topo de **…**. Ela sai da lista na hora, com a opção **Desfazer** na mensagem. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para fechá-la antes. A alteração continua valendo.

Para fazer de outro jeito, diga isso no **Chat** da tarefa. A resposta informa somente o que mudou, como um adiamento e até quando. Se não foi possível mudar algo, como um prazo, ela avisa.

Em **…**:

- **Passar…**: encaminhe a tarefa para uma pessoa da equipe, para [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta com uma frequência definida](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha um motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome** em **Detalhes** para renomear a tarefa. Você também pode pedir no chat, como "Renomeie para …". O título escolhido fica salvo.

**Reabrir** traz uma tarefa fechada de volta. Ela também volta sozinha quando algo novo acontece, como uma mensagem nova da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece como nova na lista. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento que aparecem na conta. Contas pagas automaticamente, como por débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior confirma o pagamento, por exemplo, o remetente confirma que recebeu, a tarefa se fecha sozinha. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até um horário definido, como uma confirmação antes de uma reunião, se fecha sozinha depois desse horário. Ela vai para **Feito / descartado** com o status "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou encaminhamento para outra pessoa aparecer como pronto, sua Machine verifica seus chats recentes com as pessoas envolvidas, inclusive chats em grupo, e espera o Slack terminar de lê-los. Quando uma mensagem posterior mostra que a tarefa já foi resolvida, como alguém ter feito um pedido e recebido uma confirmação, a tarefa se fecha sozinha. **Desfazer** traz a tarefa de volta por um dia.

Se alguém escrever na mesma conversa depois que o rascunho for criado, **Enviar** pausa o envio: "Não enviado: há uma mensagem nova na conversa". A tarefa mostra essa mensagem com **Ler** e **Refazer para esta mensagem**. Pressione **Enviar** outra vez para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de local ou uma reserva cancelada, The Machine atualiza as tarefas sozinha. Uma tarefa que ainda importa acompanha os novos planos. Uma tarefa que não tem mais nada a fazer vai para **Feito / descartado** com o status "Não precisa", o chat informa "Atualizado:" e o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as principais opções: **Pedir mudanças** e **Não precisa**, e explica que nada é enviado até você pressionar **Enviar**. A dica desaparece de vez quando você usa o botão ou pressiona ×.

No seu primeiro dia, o topo de Tarefas dá boas-vindas e informa quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem ou do que se trata, a organização quando ela é relevante, o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Quando o Graph tem uma foto ou um logotipo, ele aparece ao lado do nome ou da organização; caso contrário, aparecem as iniciais. Um logotipo que não fique legível em tamanho pequeno, como texto branco em um fundo transparente ou uma marca muito larga, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail; nenhuma novidade desde então". Ela aparece quando a última conversa com a pessoa é antiga ou ficou sem resposta e cita os canais que não estão conectados, como o WhatsApp. Sua Machine informa o que não sabe em vez de adivinhar.

Quando ela cita um canal que não está conectado, toque em Conectar ao lado dele para abrir essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, com a forma como foi concluída abaixo, como "Concluída: Sam assinou na terça-feira".

Acima do rascunho, uma linha discreta identifica a mensagem de origem com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver na hora se é uma resposta no Slack ou um e-mail.

Quando o rascunho considera a opinião de alguém em outro lugar, como a sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base na mensagem de Sam em #ops". Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela de que a tarefa trata e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa aparece marcada como "Esta tarefa" e é aberta na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo dele.

Uma mensagem também abre desse jeito na pesquisa, no Graph, nas respostas do Ask ou na última verificação, marcada como "Esta mensagem" (ou "Mensagens novas").

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, ele abre no app Gmail se você tiver o app instalado.

**Detalhes** de um e-mail mostram somente as informações que não aparecem no cabeçalho, como endereços completos em Cc, Cco ou um endereço de resposta diferente. Se não houver mais nada para mostrar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes de a conversa começar. O link da tarefa para a própria mensagem também abre essa conversa aqui, com **Abrir no Slack** na parte inferior.

**Detalhes** mostram o nome, o projeto e a área da tarefa (toque em uma opção para alterá-la), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída continua compacta; a mensagem de origem fica em **Detalhes**.

Uma tarefa com o status "Aguardando" leva à sua última mensagem para a pessoa, aquela pela qual você está esperando: "E-mail para Pat · ter".

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, em **+** no celular ou com `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** nem **Pessoal**, ela vai para a área certa de acordo com as pessoas e o assunto. Ela também encontra o e-mail relacionado, mesmo que seja antigo.

- **Prazo**: digite um dia ou horário, como "amanhã", "próxima sex", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta com uma frequência definida. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa: um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que sua Machine tenha. Pesquise pelo texto ou por quem enviou. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, a câmera ao lado tira uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e The Machine os lê quando trabalha nela. Só os arquivos já bastam: ela preenche a tarefa a partir de um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
