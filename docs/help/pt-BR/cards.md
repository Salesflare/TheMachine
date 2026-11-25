---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para você aprovar. Veja o que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 43d9497d3a1c4a86
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, não importa quantas mensagens ele envolva.

## Onde ficam as tarefas

A página **Tarefas** agrupa as tarefas:

- **Feito agora**: no topo, mostra que uma última etapa que você confirmou, como enviar um formulário ou resolver um problema, foi concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia, e seu celular também recebe uma notificação.
- **Para você**: tudo que está esperando por você, com o que vence até amanhã primeiro. Cada tarefa indica **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a tarefa), **Precisa de você** (primeiro, você precisa decidir ou responder; quando o trabalho não pode continuar ou ser usado sem algo que só você tem, como um preço, uma informação ou uma escolha, uma linha abaixo do título explica o que falta), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou briefing, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas que não têm novidades há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas em que a próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas, mensagens que [serão enviadas mais tarde](send-later.md) e tarefas sem resposta a **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, começando pela mais recente e mostrando quando foram concluídas, como "Feito há 5 minutos". Tarefas que parecem já estar concluídas aparecem como **Parece feito**.

Depois que você envia, uma nota curta informa para onde a tarefa foi, como "Enviado. Movido para Feito." ou "Enviado. Movido para Mais tarde até seg.". Uma resposta que só promete fazer o trabalho, como "Vou enviar até terça-feira", mantém a tarefa aberta: "Enviado. Mantido em aberto." **Abrir** leva você até ela. A busca encontra tarefas pelo título ou pela pessoa para quem foram enviadas, inclusive em Mais tarde e Feito.

Em **Para você**, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, depois as perguntas do seu Fleet, em seguida os acompanhamentos de um quadro e, por último, as demais. Dentro de cada grupo, as mais recentes aparecem primeiro. A tarefa permanece no mesmo lugar enquanto sua Machine a prepara e quando é concluída: só o indicador muda. Nos outros grupos abertos, aparecem primeiro as tarefas atrasadas ou que vencem até amanhã, seguidas das mais recentes. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que a tarefa foi concluída, como "PR #3451 mesclado", mas ela ainda não foi encerrada. **Reabrir** coloca a tarefa de volta na sua lista e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem indica que a tarefa foi concluída, ela se encerra automaticamente depois de um dia, com a opção **Desfazer**. Caso contrário, ela espera você tocar em **Marcar como feito**.

Uma tarefa que você já resolveu por conta própria, como responder pelo Gmail ou Slack, também se encerra automaticamente. Uma resposta que diz que há um arquivo anexado quando não há nenhum não encerra a tarefa.

Quando uma mensagem vem de um endereço que só parece pertencer a alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa avisa claramente: "Esta pessoa não é Sam Lee." Ela mostra o endereço verdadeiro da pessoa, nunca o nome que ela usou. Sua Machine verifica esse tipo de mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou uma resposta, mostra a etapa em **Aguardando:**. Ela fica recolhida em **Aguardando outras pessoas**, acima de Volta mais tarde, até uma nova mensagem fazê-la voltar. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio dia do prazo se ele for mais tarde, ou na manhã seguinte se o prazo já tiver passado. Ela informa quem ainda está sendo aguardado.

Quando uma tarefa depende de algo que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra isso em **Concluído quando**. Enviar a sua parte não encerra a tarefa: ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, ela se encerra automaticamente, com a opção **Desfazer**. Se nada chegar até a hora de cobrar, a tarefa volta com a opção **Escreva um lembrete curto** no chat. Diga no chat o que conta como conclusão para alterar isso.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas novas apareçam primeiro depois de alguns dias fora. Não há novidades quando nenhuma mensagem nova chega e você não faz nada na tarefa, como enviar uma mensagem no chat, editar ou adiar. Só abrir a tarefa não conta.

Tarefas urgentes, que vencem em breve ou que têm um envio em andamento continuam em Para você. **Descartar tudo** marca todas as tarefas de Mais antigos como desnecessárias após uma confirmação, assim como **Não precisa** faz com uma tarefa de cada vez, com a opção **Desfazer**. Se algo novo acontecer em uma delas, ela volta para Para você.

Uma tarefa que ninguém tocou por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** encerra a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa e ela não pergunta de novo. Se ninguém responder na semana seguinte, ela é recolhida em Volta mais tarde, e deixa de ser contada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem no chat, editar, adiar ou receber uma mensagem nova faz com que ela volte.

Uma vez por semana, um projeto que ficou parado e não tem nada em aberto pode receber uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa e mostra uma lista vazia. Enquanto verifica, ela desperta e avisa. Se uma verificação falhou ou está atrasada, a linha informa isso e mostra **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no topo da barra lateral mostram todas as tarefas ou só um tipo. Seu celular e computador usam a mesma opção. Quando Trabalho ou Pessoal estiver selecionado, **Mostrar todas** volta para a lista completa. Um alerta sobre a própria Machine, como uma peça que fica reiniciando, não é de Trabalho nem Pessoal e aparece apenas em Todos.

A linha no topo da lista também permite mudar direto para a outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no topo da lista mostra o nome do seu resumo mais recente da manhã ou da noite e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque nela para ler o resumo de novo e use **Copiar** para colá-lo onde quiser. Depois que você abrir o resumo ou tocar no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua em aberto, em Trabalho e Pessoal ou apenas na opção selecionada.

Uma tarefa de um projeto mostra o nome dele abaixo do título. Toque no nome para abrir o projeto. **Projeto**, em **Detalhes**, permite mudar o projeto ou removê-lo. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para a outra área. O que ela pode ler e enviar também muda de área. **Desfazer** na nota move a tarefa de volta.

Quando uma tarefa precisa estar na outra área para continuar e todas as mensagens relacionadas estão nela, ela é movida automaticamente e continua. Caso contrário, aparece **Mover para Trabalho**, e nada é movido até você tocar nessa opção. Uma tarefa criada por você sem escolher Trabalho ou Pessoal é movida automaticamente quando sua área fica clara. Até lá, ela não aparece como Trabalho nem Pessoal e continua privada.

Uma tarefa sempre pode ler as mensagens relacionadas a ela. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de entrada de trabalho que você marcou como Pessoal conta como Pessoal. E-mails de outra empresa sua vão para as tarefas dessa empresa. Uma tarefa sobre a sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega a uma conta pessoal, como uma pessoa cliente no WhatsApp, um pedido na sua caixa de entrada pessoal ou uma [promessa](promises.md) relacionada ao trabalho, é de Trabalho desde o início.

Uma tarefa que você moveu ou criou em uma área específica sempre fica onde você colocou. Trabalho ou Pessoal define onde a tarefa aparece e com quem é compartilhada, nunca para onde ela responde: a resposta sempre vai para a conversa original, mesmo depois de uma mudança de área, a menos que você escolha outra forma.

Mesmo sendo Pessoal, uma tarefa assim ainda responde pelo endereço de trabalho para o qual o e-mail foi enviado e nunca aparece em um Fleet de Trabalho nem no Graph da equipe.

Quando houver duas ou mais tarefas esperando, **Percorrer**, no cabeçalho de Para você, permite passar por elas uma de cada vez, na ordem da lista, com o rascunho completo e as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo isso leva no seu ritmo, como "cerca de 2 min".

No fim, a lista mostra quantas tarefas foram enviadas ou encerradas e quantas ainda estão sendo preparadas.

Uma tarefa que faz uma pergunta para você não entra nessa lista: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, dia e noite. Ela verifica o que chegou quando há 40 mensagens aguardando ou quando a mensagem mais antiga de alguém está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, das 00:00 às 06:30, as verificações ficam pausadas: as mensagens novas ainda são lidas e guardadas, e são verificadas juntas às 06:30 para que suas tarefas estejam prontas antes do resumo da manhã. Em Conexões, a opção Verificações mostra "Pausadas durante a noite. Atualização às 06:30". Se você clicar, digitar ou rolar a tela no app, escrever no chat ou tocar em uma tarefa à noite, as verificações voltam ao normal até você ficar uma hora sem usar o app. **Verificar agora** sempre verifica na hora.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas em aberto, toque na linha da sua Machine para ver o status e a opção **Detalhes**, que abre Verificações em Conexões. Se houver tarefas em aberto, essa opção fica no topo da tela no computador. Uma linha curta só aparece enquanto uma verificação está em andamento ou quando uma falha ou atraso acontece. Você também pode perguntar no chat.

LinkedIn, X e Salesflare têm seu próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, uma linha acima das tarefas mostra o que foi encontrado em todas as fontes consultadas, como "13 mensagens verificadas às 16:11 · nenhuma tarefa nova" ou "· 2 tarefas novas". Ela se refere apenas àquela verificação: as tarefas que já estavam na sua lista continuam como estavam. Quando uma tarefa nova fica esperando por um momento melhor, como o resumo da manhã, a linha informa até quando: "1 tarefa aguardando até amanhã às 08:30".

Toque na linha para ver cada conversa por e-mail, chat e notificação, com o ícone da fonte. Você verá quem escreveu, o assunto ou as primeiras palavras, além da tarefa nova ou do motivo para não criar uma, como "Você estava em cópia, uma pessoa da equipe está respondendo" ou "Reunião já marcada para quinta-feira". Uma conversa não mostra o motivo quando a verificação encontrou apenas um motivo vago. Toque em uma delas para ler a mensagem e o contexto.

As 10 primeiras aparecem na tela. Toque abaixo delas para ver o restante. Um número depois do nome, como (3), indica quantas mensagens novas há naquele chat. Uma notificação do Android sobre uma mensagem que já está na lista aparece apenas uma vez. A linha fica visível por 12 horas depois da verificação.

A contagem inclui apenas os e-mails enviados para você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails da The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** permite dizer o que mudar: como fazer a tarefa ou, quando o rascunho estiver pronto, o que alterar nele. Se você começar a digitar e não terminar, o texto fica ali quando voltar. **Cancelar** descarta o texto.

**Marcar como feito** indica que a tarefa foi resolvida. No computador, ela fica junto aos outros botões quando há espaço em uma linha. No celular, aparece em uma tarefa pronta sem rascunho ou em uma tarefa que faz uma pergunta. Nos outros casos, fica no topo de **…**. A tarefa sai da lista na hora, com a opção **Desfazer** na mensagem. Deslize a mensagem para o lado ou arraste-a com o mouse para encerrá-la antes. A alteração fica salva.

Para concluir a tarefa de outra forma, diga isso no **Chat** dela. A resposta informa apenas o que mudou, como o adiamento e até quando. Se não foi possível mudar algo, como a data de vencimento, ela avisa.

Em **…**:

- **Passar…**: encaminhe a tarefa para uma pessoa da equipe, para [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta periodicamente](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, por exemplo: "Renomeie para…". O título fica salvo.

**Reabrir** traz de volta uma tarefa encerrada. Ela também volta automaticamente quando algo novo acontece, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece na lista como nova. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você precisa pagar por conta própria, em qualquer país, vira uma tarefa com o valor, a data de vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como por débito automático ou cartão cadastrado, não viram tarefas. Quando um e-mail posterior indicar que ela foi paga, como uma confirmação do remetente de que o pagamento foi recebido, a tarefa se encerra automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só era importante até determinado horário, como uma confirmação antes de uma reunião, se encerra automaticamente depois desse horário. Ela vai para **Feito / descartado** com o status "Não precisa mais". **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de um repasse para outra pessoa aparecer como pronto, sua Machine verifica suas conversas recentes com as pessoas envolvidas, inclusive conversas em grupo, e espera o Slack terminar de lê-las. Se uma mensagem posterior indicar que a tarefa já foi resolvida, por exemplo, porque alguém pediu algo e recebeu um "sim", ela se encerra automaticamente. **Desfazer** traz a tarefa de volta por um dia.

Se alguém escrever na mesma conversa depois que o rascunho for criado, **Enviar** pausa o envio: "Não enviado: há uma mensagem nova na conversa". A tarefa mostra essa mensagem com as opções **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa que mudou de local ou uma reserva que foi cancelada, a The Machine atualiza as tarefas automaticamente. Se uma tarefa ainda for necessária, ela acompanha os novos planos. Se não houver mais nada a fazer, ela vai para **Feito / descartado** com o status "Não precisa". O chat mostra "Atualizado:" e o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as ações principais: **Pedir mudanças** e **Não precisa**, além de avisar que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa o botão ou toca em ×.

No seu primeiro dia, uma saudação aparece no topo de Tarefas e mostra quem está esperando há mais tempo pela sua resposta. Essa resposta é preparada primeiro para estar pronta quando você chegar.

Cada tarefa começa com um título. A linha abaixo informa de quem é o assunto, a organização quando houver uma relação com ela (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a mensagem chegou. Toque em um nome para abrir a página da pessoa no Graph.

Os nomes de pessoas e organizações mostram a foto ou o logotipo, se houver um no Graph, ou as iniciais. Um logotipo que não ficaria legível nesse tamanho, como texto branco em fundo transparente ou um nome muito largo, também aparece como inicial.

Às vezes, uma linha discreta informa o que não se sabe, como "Último contato há 12 dias por e-mail. Nada desde então." Ela aparece quando a última conversa com alguém é antiga ou não teve resposta e indica canais que não estão conectados, como WhatsApp. Sua Machine diz o que não sabe em vez de adivinhar.

Quando a linha menciona um canal que não está conectado, toque em **Conectar** ao lado dele para abrir essa conexão.

O título informa o que precisa ser feito e só muda se isso também mudar. Uma tarefa concluída mantém o título e mostra abaixo como terminou, como "Concluída: Sam assinou na terça-feira".

Acima do rascunho, uma linha discreta identifica a mensagem de origem e mostra o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você ver logo se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na contribuição de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, uma linha informa isso, como "Com base em uma mensagem de Sam em #ops". Toque nela para ler a mensagem. Ela sai quando uma atualização substitui o rascunho.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, da mensagem mais antiga para a mais recente: as mensagens anteriores àquela relacionada à tarefa e as respostas posteriores. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa aparece com o rótulo "Esta tarefa" e é aberta na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa aparece recolhido acima e abaixo da mensagem.

Uma mensagem também pode ser aberta desse jeito pela busca, pelo Graph, pelas respostas do Ask ou pela última verificação, com o rótulo "Esta mensagem" ou "Mensagens novas".

**Abrir no Gmail** abre o e-mail na conta do Gmail que o recebeu. No Android, ele abre no app do Gmail, se estiver instalado.

Em **Detalhes**, um e-mail mostra apenas as informações que não aparecem no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço de resposta diferente. Se não houver mais nada para mostrar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link da tarefa para a mensagem original também abre essa visualização, com **Abrir no Slack** na parte de baixo.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para mudar), sua última nota e o resultado de um agente de programação. O título abre o chat. Uma tarefa concluída fica compacta; a mensagem de origem aparece em **Detalhes**.

Uma tarefa "Aguardando" tem um link para sua última mensagem para a pessoa, aquela cuja resposta você está esperando: "E-mail para Pat · ter".

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, em **+** no celular ou com `N`) cria uma tarefa para qualquer coisa. Criá-la não envia nada. Se você não escolher **Trabalho** ou **Pessoal**, a tarefa vai para a área certa, de acordo com quem e com o que ela se relaciona. Ela também encontra o e-mail ao qual é um follow-up, mesmo que seja antigo.

Se você fechar a tarefa antes de adicioná-la, o texto e as opções ficam salvos para a próxima vez. Os arquivos não ficam salvos. **Descartar** na mensagem remove o conteúdo.

- **Prazo**: digite um dia ou horário, como "amanhã", "próxima sex", "3 nov", "14h" ou "daqui a 2 horas", também no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta periodicamente. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule as pessoas ou empresas relacionadas à tarefa, até 5.
- Ícone de mensagem: anexe a mensagem relacionada à tarefa, como um e-mail ou uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outro serviço que a The Machine tenha. Pesquise pelo texto ou por quem enviou. Cada resultado mostra de onde veio, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou solte arquivos no formulário. No celular, use a câmera ao lado para tirar uma foto. Você pode adicionar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam com a tarefa, e a The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: ela preenche a tarefa com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para vê-la em tamanho grande.
