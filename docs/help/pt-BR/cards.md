---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para você aprovar. Entenda cada parte de uma tarefa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fef065570d3fd972
---
Sua Machine lê tudo que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, mesmo que envolva várias mensagens.

## Onde ficam as tarefas

A página **Tarefas** organiza tudo assim:

- **Feito agora**: no alto da lista, aparece uma última etapa que você confirmou, como o envio de um formulário ou a resolução de um problema, concluída enquanto você estava fora. Ela fica ali até você tocar em **Entendi**, por no máximo um dia. Você também recebe uma notificação no celular.
- **Para você**: tudo que depende de você, começando pelo mais urgente. Cada tarefa mostra **Preparada** (um rascunho ou resultado está pronto, e **Fazer** ou **Enviar** conclui a ação), **Precisa de você** (primeiro, ela precisa de uma decisão ou resposta sua; quando o trabalho parou por algo que só você pode fornecer, como um dado, um login ou uma escolha, aparece uma linha abaixo do título explicando o que falta), **Preparando…** (sua Machine está trabalhando nela) ou **Para ler** (um resumo ou uma nota informativa, sem nada para decidir).
- **Mais antigos**: tarefas recolhidas sem novidades há uma semana (veja abaixo).
- **Aguardando outras pessoas**: tarefas recolhidas cuja próxima etapa depende de outra pessoa (veja abaixo).
- **Volta mais tarde**: tarefas adiadas e tarefas sem resposta para **Ainda precisa?** (veja abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / descartado**: todas as tarefas concluídas, começando pela mais recente, com o horário em que foram concluídas, como “Feito há 5 minutos”. Tarefas que parecem já estar concluídas aparecem como **Parece feito**.

Depois que você envia, uma nota curta informa para onde a tarefa foi, como “Enviado. Movido para Feito.” ou “Enviado. Movido para Mais tarde até seg.”. Uma resposta que só promete concluir o trabalho, como “Envio até terça-feira”, mantém a tarefa aberta: “Enviado. Mantido em aberto.” **Abrir** leva você até a tarefa. A pesquisa encontra tarefas pelo título ou pelo destinatário, inclusive em Mais tarde e Feito.

**Para você** coloca primeiro o que está atrasado ou vence até amanhã, depois as perguntas do seu Fleet, os follow-ups de um quadro e, por fim, o restante. Dentro de cada grupo, as tarefas mais recentes aparecem primeiro. A tarefa mantém a posição enquanto sua Machine a prepara e quando é concluída. Só o indicador muda. Nos outros grupos em aberto, o que está atrasado ou vence até amanhã aparece primeiro, seguido do restante, começando pelo mais recente. A barra lateral mantém a mesma ordem.

**Parece feito** significa que sua Machine percebeu que algo foi concluído, como “PR #3451 merged”, mas a tarefa ainda não foi fechada. **Reabrir** coloca a tarefa de volta na sua lista, e sua Machine aprende com isso. Essas tarefas nunca aparecem como atrasadas. Quando uma mensagem indica que a tarefa foi concluída, ela se fecha sozinha depois de um dia, com a opção **Desfazer**. Nos outros casos, ela aguarda você tocar em **Marcar como feito**. Uma tarefa que você resolveu por conta própria, por exemplo, respondendo no Gmail ou no Slack, também se fecha sozinha.

Quando uma mensagem vem de um endereço que só parece ser de alguém que você conhece, como sam@acme-corp.example em vez de sam@acmecorp.example, a tarefa avisa claramente: “Esta pessoa não é Sam Lee.” A pessoa aparece pelo próprio endereço, nunca pelo nome que usou. Sua Machine verifica a mensagem com a pessoa do endereço que você já tem, nunca com quem escreveu.

Uma tarefa que ainda depende de outra pessoa, como uma revisão ou uma resposta, indica a etapa em **Aguardando:**. Ela fica em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, até uma nova mensagem trazê-la de volta. O mesmo acontece depois que você faz uma pergunta: a tarefa volta na manhã anterior ao prazo, no próprio prazo se ele for mais tarde hoje ou na manhã seguinte depois que o prazo passar. Ela informa de quem ainda está aguardando uma resposta.

Quando a tarefa depende de um resultado que outra pessoa vai entregar, como um contrato assinado, **Detalhes** mostra esse resultado em **Concluído quando**. Enviar sua parte não conclui a tarefa. Ela fica em **Aguardando outras pessoas** até uma mensagem indicar que o resultado chegou. Então, ela se fecha sozinha, com a opção **Desfazer**. Se nada chegar até a hora de cobrar a pessoa, a tarefa volta com a opção **Escreva um lembrete curto** no chat. Para mudar o que conta como concluído, diga isso no chat.

Uma tarefa sem novidades por uma semana sai de Para você e vai para **Mais antigos**, para que as tarefas recentes apareçam primeiro quando você voltar depois de alguns dias. Não há novidades quando não chega nenhuma mensagem nova e você não faz nada na tarefa, como enviar uma mensagem pelo chat, editar ou adiar. Só abrir a tarefa não conta.

Tarefas urgentes, com vencimento próximo ou com um envio em andamento continuam em Para você. **Descartar tudo** marca todas as tarefas de Mais antigos como desnecessárias depois de uma confirmação, assim como **Não precisa** faz com uma tarefa por vez, com a opção **Desfazer**. Uma novidade em uma tarefa a traz de volta para Para você.

Uma tarefa sem nenhuma ação por uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** fecha a tarefa, com a opção **Desfazer**. **Manter** mantém a tarefa e ela não pergunta de novo. Se você não responder por mais uma semana, a tarefa vai para Volta mais tarde, e deixa de ser contada no número do ícone do app e no resumo da manhã. Abrir a tarefa, enviar uma mensagem pelo chat, editar, adiar ou receber uma mensagem nova traz a tarefa de volta.

Uma vez por semana, um projeto que ficou parado e não tem nenhuma tarefa em aberto pode receber uma tarefa com uma próxima etapa específica, no máximo três por semana. Veja [Projetos](projects.md).

Quando nada precisa de você, sua Machine descansa com a lista vazia. Enquanto verifica, ela volta a funcionar e avisa. Se uma verificação falhar ou atrasar, a linha informa isso e mostra a opção **Verificar agora**.

As opções **Todos**, **Trabalho** e **Pessoal** no alto da barra lateral mostram todas as tarefas ou só um tipo. Seu celular e seu computador mostram a mesma seleção. Quando Trabalho ou Pessoal está selecionado, **Mostrar todas** volta à lista completa. Um alerta sobre a própria Machine, como uma parte que não para de reiniciar, não é de Trabalho nem Pessoal e aparece apenas em Todos.

A linha no alto da lista também leva direto à outra opção: em **Só pessoal**, toque em **Trabalho** ou **Mostrar todas**.

A linha no alto da lista mostra o nome do seu resumo mais recente da manhã ou do fim do dia e o que ele contou, como **Resumo do fim do dia de ontem** · 12 concluídas, 3 em aberto. Toque nela para ler o resumo novamente e use **Copiar** para colar em qualquer lugar. Depois que você abre o resumo ou toca no **×**, ele fica disponível em todos os seus dispositivos até o próximo resumo.

Se não houver um resumo recente, aparece **Hoje até agora**: o que foi concluído hoje e o que continua em aberto, em Trabalho e Pessoal ou só na opção selecionada.

Uma tarefa de um projeto mostra o nome do projeto abaixo do título. Toque nele para abrir o projeto. **Projeto**, em **Detalhes**, permite alterar ou remover o projeto. Veja [as tarefas de um projeto](projects.md#a-project-s-to-dos).

**Área**, em **Detalhes**, move uma tarefa para sua outra área. O que ela pode ler e enviar também muda com ela. **Desfazer** na nota move a tarefa de volta.

Quando uma tarefa precisa da sua outra área para continuar e todas as mensagens relacionadas estão nela, ela se move para lá sozinha e continua. Caso contrário, aparece **Mover para Trabalho**, e nada muda até você tocar nessa opção. Uma tarefa que você criou sem escolher Trabalho ou Pessoal se move sozinha quando encontra a área certa. Até lá, ela não aparece como Trabalho nem Pessoal e fica privada.

Uma tarefa sempre pode ler as mensagens de que veio. Quando precisa de outras mensagens da sua outra área, ela pergunta com **Usar este e-mail para esta tarefa**. Uma caixa de e-mail de trabalho que você marcou como Pessoal conta como Pessoal. Mensagens de outras empresas suas vão para as tarefas daquela empresa. Uma tarefa sobre sua vida pessoal, como uma mensagem da família enviada para seu endereço de trabalho, é Pessoal desde o início.

Um assunto de trabalho que chega por uma conta pessoal, como uma mensagem de um cliente no WhatsApp ou um pedido na sua caixa de entrada pessoal, é de Trabalho desde o início. Uma tarefa que você moveu ou classificou continua na área que escolheu. Trabalho ou Pessoal determina onde a tarefa aparece e com quem é compartilhada, nunca o endereço de resposta: ela sempre responde na conversa original, mesmo depois de ser movida, a menos que você escolha outro jeito.

Mesmo assim, uma tarefa Pessoal responde pelo endereço de trabalho em que o e-mail chegou, e nunca aparece em um Fleet de Trabalho nem no Graph da equipe.

Quando há duas ou mais tarefas aguardando, **Percorrer**, no cabeçalho de Para você, percorre uma de cada vez, na ordem da lista, mostrando cada rascunho completo, com as opções **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc interrompe. O cabeçalho informa quanto tempo o processo leva no seu ritmo, como “cerca de 2 min”.

No final, aparece a quantidade de tarefas enviadas ou fechadas e quantas ainda estão sendo preparadas.

Uma tarefa que faz uma pergunta fica de fora dos dois grupos: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, de dia e de noite. Ela verifica o que chegou quando há 40 mensagens esperando ou quando a mensagem mais antiga de uma pessoa está esperando há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, dentro de uma hora.

À noite, entre 00:00 e 06:30, as verificações pausam. As mensagens novas continuam sendo lidas e guardadas, e são verificadas juntas às 06:30 para deixar suas tarefas prontas antes do resumo da manhã. Em Conexões, a seção de verificações mostra “Pausadas durante a noite. Atualização às 06:30”. Se você clicar, digitar ou rolar no app, escrever no chat ou tocar em uma tarefa à noite, as verificações funcionam normalmente até você ficar uma hora sem usar o app. **Verificar agora** sempre inicia uma verificação imediatamente.

**Verificar agora** lê todas as fontes imediatamente. Se não houver tarefas em aberto, toque na linha da sua Machine para ver as opções, incluindo **Detalhes**, que abre as verificações em Conexões. Se houver tarefas em aberto, a opção aparece no alto da tela no computador. Uma linha curta aparece ali somente enquanto uma verificação está em andamento, ou se uma falhou ou atrasou. Você também pode pedir isso no chat.

LinkedIn, X e Salesflare seguem o próprio ritmo.

## Última verificação

Depois de uma verificação que leu mensagens novas, aparece uma linha acima das tarefas com o que ela encontrou em cada fonte lida, como “13 mensagens verificadas às 16:11 · nada precisa de você” ou “· 2 tarefas novas”. Quando uma tarefa nova aguarda um momento melhor, como o resumo da manhã, a linha informa até quando: “1 tarefa adiada até amanhã, às 08:30”.

Toque na linha para ver cada conversa por e-mail, chat e notificação, com o ícone da fonte, quem escreveu, o assunto ou as primeiras palavras, e a nova tarefa ou o motivo para não criar uma, como “Você estava em cópia, outra pessoa da equipe está respondendo” ou “Reunião já marcada para quinta-feira”. Uma conversa não mostra o motivo se a verificação deu apenas uma resposta vaga. Toque em uma conversa para ler.

As primeiras 10 aparecem de início. Toque abaixo delas para ver o restante. Um número depois de um nome, como (3), indica quantas mensagens novas aquele chat tem. Uma notificação do celular sobre uma mensagem que já aparece na lista é mostrada apenas uma vez. A linha fica visível por 12 horas depois da verificação.

A contagem inclui apenas os e-mails enviados a você. Suas respostas são lidas para dar contexto e identificar promessas, mas não contam como e-mails novos. Os e-mails da The Machine para você, como o resumo da manhã ou um aviso de correção, nunca são lidos nem listados. E-mails sobre cobrança, período de teste ou convite são lidos normalmente.

## Os botões

Uma tarefa mostra a próxima etapa, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** serve para dizer o que mudar: como fazer a tarefa ou, quando um rascunho estiver pronto, o que alterar nele. **Marcar como feito** indica que a tarefa foi resolvida. A opção aparece à vista em uma tarefa pronta sem rascunho; nos outros casos, fica no alto do menu **…**, inclusive em tarefas que precisam da sua decisão. A tarefa sai da lista imediatamente e a mensagem mostra **Desfazer**. Deslize a mensagem para o lado ou arraste-a para fora com o mouse para fechá-la mais rápido. A alteração continua valendo.

Para resolver de outro jeito, diga isso no **Chat** da tarefa. A resposta informa apenas o que mudou, como o adiamento e até quando. Se não for possível alterar algo, como o prazo, ela avisa.

No menu **…**:

- **Passar…**: passe a tarefa para alguém da equipe, para [Claude Code ou Codex](hand-to-agent.md) ou [peça uma revisão](ask-to-review.md).
- **Repetir…**: a tarefa [volta em um intervalo regular](recurring.md).
- **Não precisa**: a tarefa desaparece. Se quiser, escolha um motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título ou em **Nome**, em **Detalhes**, para renomear a tarefa. Você também pode pedir isso no chat, por exemplo: “Renomeie para…”. O título escolhido por você permanece.

**Reabrir** traz de volta uma tarefa fechada. Ela também volta sozinha quando acontece algo novo, como uma nova mensagem da outra pessoa, mas não quando você responde. A tarefa mostra quando voltou e aparece na lista como nova. O chat continua de onde parou, mesmo depois de semanas.

Uma conta que você precisa pagar por conta própria, de qualquer país, vira uma tarefa com o valor, o vencimento e os dados de pagamento informados na conta. Contas pagas automaticamente, como um débito automático ou um cartão cadastrado, não viram tarefas. Quando um e-mail posterior informa que ela foi paga, como uma confirmação do remetente, a tarefa se fecha sozinha. **Desfazer** traz a tarefa de volta por um dia.

Uma tarefa que só importa até um horário definido, como uma confirmação antes de uma reunião, se fecha sozinha depois desse horário. Ela vai para **Feito / descartado** com o status “Não é mais necessário”. **Desfazer** traz a tarefa de volta por um dia.

Antes de uma mensagem ou de um repasse para outra pessoa aparecer como pronto, sua Machine verifica seus chats recentes com as pessoas envolvidas, inclusive chats em grupo, e aguarda a leitura do Slack. Quando uma mensagem posterior indica que a tarefa já foi concluída, por exemplo, porque alguém pediu e a outra pessoa aceitou, a tarefa se fecha sozinha. **Desfazer** traz a tarefa de volta por um dia.

Se outra pessoa escrever na mesma conversa depois que o rascunho for criado, **Enviar** pausa o envio e mostra: “Não enviado: nova mensagem na conversa”. A tarefa mostra essa mensagem com as opções **Ler** e **Refazer para esta mensagem**. Toque em **Enviar** novamente para enviar o rascunho como está.

Quando uma mensagem mais recente muda os planos, como uma festa que vai acontecer em outro lugar ou uma reserva cancelada, a The Machine atualiza as tarefas automaticamente. Uma tarefa que ainda é necessária acompanha os novos planos. Se não houver mais nada a fazer, ela vai para **Feito / descartado** como “Não precisa”. O chat informa “Atualizado:” e o motivo, e **Desfazer** traz a tarefa de volta por um dia.

Nas primeiras tarefas, uma dica curta mostra as ações principais: **Pedir mudanças** e **Não precisa**, e avisa que nada é enviado até você tocar em **Enviar**. A dica desaparece de vez quando você usa um dos botões ou toca em ×.

No seu primeiro dia, uma mensagem de boas-vindas aparece no alto de Tarefas e informa quem está esperando há mais tempo por uma resposta sua. Essa resposta é preparada primeiro, para estar pronta quando você chegar.

Cada tarefa começa com o título. A linha abaixo informa a pessoa relacionada, a organização quando o assunto envolve uma (não apenas porque alguém trabalha lá), o projeto, Trabalho ou Pessoal e quando a tarefa chegou. Toque em um nome para abrir a página da pessoa no Graph.

O nome e a organização mostram a foto ou o logotipo, se houver um no Graph. Caso contrário, mostram as iniciais. Um logotipo difícil de ler nesse tamanho, como letras brancas em fundo transparente ou uma marca escrita em uma linha longa, também aparece com as iniciais.

Às vezes, uma linha discreta informa o que não se sabe, como “Último contato por e-mail há 12 dias. Nenhuma mensagem desde então.” Ela aparece quando já faz tempo que a pessoa não responde ou não há resposta, e informa os canais que não estão conectados, como o WhatsApp. Sua Machine diz o que não sabe em vez de adivinhar.

Quando a linha cita um canal que não está conectado, toque em Conectar ao lado dele para abrir as opções de conexão.

O título descreve o que precisa ser feito e só muda quando isso muda. Uma tarefa concluída mantém o título e mostra abaixo como terminou, como “Concluída: Sam assinou na terça-feira”.

Uma linha discreta acima do rascunho identifica a mensagem de origem, com o logotipo do serviço. Toque nela para ler a conversa. O rascunho mostra o logotipo do destino, para você saber de cara se é uma resposta no Slack ou um e-mail.

Quando o rascunho se baseia na opinião de alguém em outro lugar, como uma sugestão de uma pessoa da equipe no Slack, aparece uma linha informando isso, como “Com base na mensagem de Sam em #ops”. Toque nela para ler a mensagem.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma conversa, começando pela mensagem mais antiga: as mensagens anteriores à mensagem da tarefa e as respostas seguintes. No WhatsApp, Telegram ou Signal, suas mensagens aparecem à direita, como no app. A mensagem da tarefa está marcada como “Esta tarefa” e abre na conversa. **Mostrar mensagens anteriores** adiciona mensagens mais antigas. Em um e-mail, o restante da conversa fica recolhido acima e abaixo da mensagem.

**Abrir no Gmail** abre o e-mail na conta do Gmail em que ele chegou. No Android, ele abre no app Gmail, se você tiver o app instalado.

Em **Detalhes**, um e-mail mostra apenas o que não aparece no cabeçalho, como os endereços completos em Cc, Bcc ou um endereço de resposta diferente. Se não houver nada a acrescentar, essa seção não aparece.

Uma resposta em uma conversa do Slack também mostra o que foi dito antes do início da conversa. O link de uma tarefa para a própria mensagem também abre a conversa aqui, com **Abrir no Slack** no fim.

**Detalhes** mostra o nome, o projeto e a área da tarefa (toque em um deles para alterar), sua última nota e o resultado de um agente de programação. Toque no título para abrir o chat. Uma tarefa concluída continua resumida. A mensagem de origem fica em **Detalhes**.

Uma tarefa com status “Aguardando” tem um link para sua última mensagem enviada à pessoa e para a resposta que está aguardando: “E-mail para Pat · ter”.

## Crie uma tarefa

**Nova tarefa** (em **Pesquisar** no computador, **+** no celular ou `N`) cria uma tarefa para qualquer coisa. Criar uma tarefa não envia nada. Se você não selecionar **Trabalho** ou **Pessoal**, ela vai para a área certa, de acordo com quem e com o que está relacionada. Ela também encontra o e-mail a que a tarefa dá follow-up, mesmo que seja antigo.

- **Vence**: digite um dia ou horário, como “amanhã”, “próxima sex.”, “3 nov.”, “14h” ou “daqui a 2 horas”. Você também pode escrever no seu idioma. O ícone de calendário mostra opções rápidas e **Escolher data**.
- **Repete**: a tarefa volta em um intervalo regular. Veja [Tarefas recorrentes](recurring.md).
- **Pessoa**: vincule até 5 pessoas ou empresas relacionadas à tarefa.
- Ícone de mensagem: anexe a mensagem relacionada, como um e-mail, uma mensagem do Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que sua Machine tenha. Pesquise pelo texto ou pelo remetente. Cada resultado mostra a origem, quem enviou e quando.
- **Arquivos**: toque no clipe, cole uma captura de tela ou arraste arquivos para o formulário. No celular, toque na câmera ao lado para tirar uma foto. Você pode anexar até 5 arquivos, como no chat (veja [Adicionar arquivos](card-chat.md#add-files)). Toque em × para remover um arquivo.

Os arquivos ficam na tarefa, e a The Machine os lê enquanto trabalha nela. Só os arquivos já bastam: a tarefa é preenchida com base em um PDF ou arquivo de texto. Uma foto aparece como uma imagem pequena. Toque nela para ver em tamanho original.
