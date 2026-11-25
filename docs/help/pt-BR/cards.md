---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa da sua atenção, pronta para você aprovar. Veja o que significa cada parte de uma tarefa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 91b111b2d6f2a97b
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa da sua atenção. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** agrupa as tarefas:

- **Feito agora**: no alto, mostra uma última etapa que você confirmou, como um formulário ou uma solicitação, concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e você também recebe uma notificação no celular.
- **Para você**: tudo que está esperando por você, primeiro o que vence até amanhã. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (ela precisa da sua decisão ou resposta primeiro; quando o trabalho não pode continuar ou ser usado sem algo que só você pode fornecer, como um preço, uma informação ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou briefing, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas, sem novidades há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas, mensagens que [chegam mais tarde](send-later.md) e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, das mais recentes para as mais antigas, com o horário em que foram concluídas, como “Concluída há 5 minutos”. Tarefas que parecem já ter sido concluídas aparecem como **Parece feito**.

Depois que você envia, uma nota curta informa para onde a tarefa foi, como “Enviado. Movido para Feito.” ou “Enviado. Movido para Volta mais tarde até seg.”. Uma resposta que só promete concluir o trabalho, como “Vou enviar até terça-feira”, mantém a tarefa aberta: “Enviado. Mantido em aberto.” **Abrir** leva você até ela. A pesquisa encontra tarefas pelo título ou pelo destinatário, também em Volta mais tarde e Feito.

Em **Para você**, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, depois as perguntas da sua Fleet, os follow-ups de um quadro e, por fim, as demais. Em cada grupo, as mais recentes vêm primeiro. A tarefa não muda de lugar enquanto sua Machine a prepara nem quando é concluída: só o status muda. Nos outros grupos abertos, as tarefas atrasadas ou que vencem até amanhã vêm primeiro, seguidas pelas mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como “PR #3451 mesclado”, mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem indica que a tarefa foi concluída, ela se encerra automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, ela aguarda você tocar em **Marcar como feita**.

Uma tarefa que você já resolveu por conta própria, por exemplo, respondendo pelo Gmail ou Slack, também se encerra automaticamente. Uma resposta que diz que um arquivo está anexado quando não está não encerra a tarefa.

Quando uma mensagem vem de um endereço que só parece pertencer a alguém que você conhece, como sam@acme-corp.example no lugar de sam@acmecorp.example, a tarefa avisa claramente: “Esta pessoa não é Sam Lee.” Ela identifica a pessoa pelo endereço dela, nunca pelo nome usado na mensagem. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou resposta, mostra **Aguardando:** e a etapa pendente. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte depois que o prazo passar, e informa quem ainda precisa responder.

Quando uma tarefa depende de um resultado que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, ela se encerra automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com **Escreva um lembrete curto** no chat. Diga no chat o que conta como concluído para alterar isso.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas novas apareçam primeiro depois de alguns dias fora. Não há novidades quando não chega nenhuma mensagem nova sobre a tarefa e você não faz nada nela, como enviar uma mensagem no chat, editar ou adiar. Só abrir a tarefa não conta.

Tarefas urgentes, que vencem em breve ou com um envio em andamento continuam em Para você. **Descartar tudo** marca como desnecessárias, após uma confirmação, todas as tarefas de Mais antigos. É o mesmo que marcar uma por uma como **Não precisa**, com a opção **Desfazer**. Se surgir algo novo em uma tarefa, ela volta para Para você.

Uma tarefa sem atividade por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Se não houver resposta por mais uma semana, a tarefa é recolhida em Volta mais tarde, e deixa de ser contabilizada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma nova mensagem traz a tarefa de volta.

Uma vez por semana, um projeto que ficou parado e não tem tarefas em aberto pode receber uma tarefa com uma próxima etapa específica, até três por semana. Veja [Projetos](projects.md).

Quando nada precisa da sua atenção, sua Machine descansa e deixa a lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra **Verificar agora**.

Os filtros **Todos**, **Trabalho** e **Pessoal**, no alto da barra lateral, mostram todas as tarefas ou apenas um tipo. Seu celular e computador usam a mesma seleção. Enquanto Trabalho ou Pessoal estiver selecionado, **Mostrar todas** volta para a lista completa. Um alerta sobre a própria Machine, como uma peça que fica reiniciando, não é de Trabalho nem Pessoal e aparece apenas em Todos.

A linha no alto da lista também leva direto ao outro filtro: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no alto da lista mostra o nome do último resumo da manhã ou da noite e o que ele contabilizou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque nela para ler o resumo novamente e use **Copiar** para colá-lo onde quiser. Depois que você abre o resumo ou toca no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, a linha mostra **Hoje até agora**: o que foi concluído hoje e o que ainda está em aberto, em Trabalho e Pessoal ou apenas no filtro selecionado.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite alterar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para a outra área. O acesso às mensagens que ela pode ler e enviar também muda. **Desfazer**, na nota, move a tarefa de volta.

Quando uma tarefa precisa da outra área para continuar e todas as mensagens de que ela veio estão lá, ela muda de área automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal muda de área automaticamente quando encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa, e uma tarefa sobre sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega por uma conta pessoal, como uma mensagem de um cliente no WhatsApp, um pedido na sua caixa pessoal ou uma [promessa](promises.md) sobre trabalho, é de Trabalho desde o início.

Uma tarefa que você moveu ou classificou por conta própria sempre fica onde você a colocou. Trabalho ou Pessoal define onde a tarefa aparece e com quem ela é compartilhada, nunca para onde ela responde: a resposta sempre vai para a conversa original, mesmo depois de uma mudança, a menos que você escolha outra opção.

Uma tarefa Pessoal desse tipo ainda responde pelo endereço de trabalho que recebeu o e-mail e nunca aparece em uma Fleet de Trabalho ou no Graph da equipe.

Quando há duas ou mais tarefas aguardando, **Percorrer**, no cabeçalho de Para você, passa por elas uma de cada vez, na ordem da lista, mostrando cada rascunho completo com **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo leva no seu ritmo, como “cerca de 2 min”.

No final, o resumo informa o que foi enviado ou encerrado e o que ainda está sendo preparado.

Uma tarefa que faz uma pergunta para você não entra nessa sequência: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, de dia e de noite. Ela verifica o que chegou quando há 40 mensagens aguardando ou quando a mensagem mais antiga de alguém está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, entre 00:00 e 06:30, as verificações são pausadas: as mensagens novas ainda são lidas e armazenadas, e são verificadas juntas às 06:30, para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, as verificações mostram “Pausadas durante a noite, serão retomadas às 06:30”. Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa durante a noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas em aberto, toque na linha da sua Machine para ver os detalhes, com **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, a opção aparece no alto da lista no computador. Uma linha curta aparece ali apenas enquanto uma verificação está em andamento ou quando ela falha ou atrasa. Você também pode pedir isso no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas informa o que encontrou em todas as fontes que leu, como “13 mensagens verificadas às 16:11 · nenhuma tarefa nova” ou “· 2 tarefas novas”. Ela se refere apenas àquela verificação: as tarefas que já estavam na lista continuam como estão. Quando uma nova tarefa fica aguardando um momento melhor, como o resumo da manhã, a linha informa até quando: “1 tarefa adiada até amanhã às 08:30”.

Toque na linha para ver cada conversa de e-mail, chat e notificação com o ícone da fonte: quem escreveu, o assunto ou as primeiras palavras e a tarefa criada ou o motivo de não ter sido necessária, como “Você só está em cópia, outra pessoa da equipe está respondendo” ou “Reunião já marcada para quinta-feira”. Uma conversa não mostra o motivo quando a verificação indicou apenas um motivo vago. Toque em uma mensagem para lê-la junto com o que foi dito ao redor dela.

As primeiras 10 aparecem. Toque abaixo delas para ver o restante. Um número depois do nome, como (3), indica quantas mensagens novas há no chat. Uma notificação no celular sobre uma mensagem que já está listada aparece apenas uma vez. A linha fica visível por 12 horas depois da verificação.

A contagem inclui apenas e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails da The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** indica o que alterar: como fazer a tarefa ou, quando o rascunho estiver pronto, o que mudar nele. Se você começar a escrever e sair antes de terminar, o texto estará lá quando voltar. **Cancelar** descarta o texto.

**Marcar como feita** indica que a tarefa foi resolvida. No computador, ela fica junto dos outros botões quando todos cabem em uma linha. No celular, aparece à vista em uma tarefa pronta sem rascunho ou em uma tarefa que faz uma pergunta. Nos outros casos, fica no alto do menu **…**. A tarefa sai da lista na hora, com a opção **Desfazer** na mensagem. Deslize a mensagem para dispensá-la ou arraste-a com o mouse para encerrá-la mais rápido. A alteração é mantida.

Para concluir a tarefa de outra forma, diga como no **Chat** dela. A resposta informa apenas o que mudou, como o adiamento e até quando. Se não foi possível alterar algo, como o prazo, ela avisa.

No menu **…**:

- **Passar…**: atribua a tarefa a alguém da equipe, a [Claude Code ou Codex](hand-to-agent.md), ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta periodicamente](recurring.md).
- **Não precisa**: a tarefa é removida. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, como “Renomeie para …”. O título fica como você definiu.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece na lista como nova. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você ainda precisa pagar por conta própria, em qualquer país, vira uma tarefa com o valor, o vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior indica que ela foi paga, como uma confirmação de recebimento do pagamento enviada por quem cobrou, a tarefa se encerra automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só era importante até um horário determinado, como uma confirmação antes de uma reunião, se encerra automaticamente depois desse horário. Ela vai para **Feito / descartado** com o status “Não precisa mais”. **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou tarefa repassada para alguém aparecer como pronta, sua Machine verifica as conversas recentes com as pessoas envolvidas, incluindo conversas em grupo, e aguarda a leitura delas pelo Slack. Quando uma mensagem posterior indica que o assunto já foi resolvido, como quando alguém recebeu o pedido e respondeu que sim, a tarefa se encerra automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escrever na mesma conversa depois que o rascunho for criado, **Enviar** pausa o envio: “Não enviado: há uma nova mensagem na conversa”. A tarefa mostra essa mensagem com **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para mandar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa transferida para outro local ou uma reserva cancelada, a The Machine atualiza as tarefas por conta própria. Uma tarefa que ainda é necessária acompanha os novos planos. Uma tarefa sem mais nada a fazer vai para **Feito / descartado** com o status “Não precisa”, e o chat informa “Atualizado:” e o motivo. **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma dica curta mostra as ações principais: **Pedir mudanças** e **Não precisa**. Ela também explica que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão correspondente ou toca em ×.

No seu primeiro dia, uma mensagem de boas-vindas aparece no alto de Tarefas e informa quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa de quem ou do que se trata, a organização quando o assunto envolve uma (não apenas porque alguém trabalha nela), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

Os nomes de pessoas e organizações mostram a foto ou o logotipo, se houver no Graph. Caso contrário, mostram as iniciais. Logotipos difíceis de ler em tamanho pequeno, como texto branco em fundo transparente ou uma marca muito larga, também aparecem como iniciais.

Às vezes, uma linha discreta informa o que não se sabe, como “Último contato há 12 dias por e-mail; sem novidades desde então”. Ela aparece quando o último contato com a pessoa é antigo ou não teve resposta, e identifica canais que não estão conectados, como WhatsApp. Sua Machine informa o que não sabe em vez de tentar adivinhar.

Quando a linha cita um canal que não está conectado, **Conectar**, ao lado dele, abre essa conexão.

O título informa o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título, e informa abaixo como foi encerrada, como “Concluída: Sam assinou na terça-feira”.

Uma linha discreta acima do rascunho identifica a mensagem de origem, com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver de imediato se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como “Com base na mensagem de Sam em #ops”. Toque nela para ler a mensagem. Essa informação desaparece quando uma atualização substitui o rascunho.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela a que a tarefa se refere e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem relacionada à tarefa aparece marcada como “Esta tarefa” e fica visível. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em uma conversa por e-mail, o restante da conversa aparece recolhido acima e abaixo da mensagem.

Uma mensagem também abre dessa forma na pesquisa, no Graph, nas respostas do Ask ou na última verificação, marcada como “Esta mensagem” ou “Mensagens novas”.

**Abrir no Gmail** abre o e-mail na conta do Gmail que o recebeu. No Android, ele abre no app do Gmail, se estiver instalado.

Em **Detalhes**, um e-mail mostra apenas as informações que não aparecem no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço diferente para respostas. Se não houver outras informações, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link de uma tarefa para a mensagem original também abre essa tela, com **Abrir no Slack** no fim.

**Detalhes** mostra o nome da tarefa, o projeto e a área (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída aparece de forma resumida; a mensagem de origem fica em **Detalhes**.

Uma tarefa “Aguardando” traz um link para a última mensagem que você enviou à pessoa e cuja resposta está aguardando: “E-mail para Pat · ter”.

## Criar uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, em **+** no celular ou usando `N`) cria uma tarefa para qualquer assunto. Criar uma tarefa não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, ela vai para a área adequada com base em quem e no que diz respeito. Ela também encontra o e-mail ao qual a tarefa dá follow-up, mesmo que seja antigo.

Se fechar a tarefa antes de adicioná-la, o texto e as opções que você escolheu estarão lá na próxima vez. Os arquivos não ficam salvos. **Descartar**, na mensagem, remove a tarefa.

- **Vence**: digite um dia ou horário, como “amanhã”, “próxima sex.”, “3 nov.”, “14h” ou “daqui a 2 horas”. Você também pode digitar no seu idioma. O ícone de calendário mostra atalhos e a opção **Escolher data**.
- **Repete**: a tarefa volta periodicamente. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até cinco pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa, como um e-mail, mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem disponível na The Machine. Pesquise pelo texto ou por quem enviou. Cada resultado informa a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste os arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode adicionar até cinco arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam na tarefa, e a The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa a partir de um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho real.
