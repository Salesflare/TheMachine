---
title: Tarefas
area: cards
summary: Uma tarefa para cada coisa que precisa de você, pronta para o seu sim. O que cada parte de uma tarefa significa.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
Sua Machine lê tudo o que chega e cria uma tarefa só quando algo precisa de você. Uma tarefa por assunto, não importa quantas mensagens ele tenha.

## Onde ficam as tarefas

A página **Tarefas** agrupa as tarefas:

- **Para você**: tudo o que espera por você, o mais urgente primeiro. Cada tarefa diz **Preparada** (o trabalho está feito, e **Fazer** ou **Enviar** conclui) **Precisa de você** (primeiro precisa da sua decisão ou de uma resposta) ou **Preparando…** (sua Machine está trabalhando nela).
- **Feito agora**: uma última etapa que você confirmou, como enviar um formulário ou abrir uma issue, deu certo enquanto você estava fora. Ela mostra o que aconteceu até você tocar em **Entendi**, por um dia no máximo, e seu celular também fica sabendo. Depois fica só em Feito.
- **Volta mais tarde**: adiada, e as tarefas sem resposta a **Ainda precisa?** (abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, pelo momento em que foram concluídas, das mais novas para as mais antigas, 30 por vez conforme você rola. Uma tarefa que você acabou de enviar fica no topo, e cada uma diz quando, como "Feito há 5 minutos". As que já parecem concluídas ficam entre elas pelo momento em que começaram a parecer, com a etiqueta **Parece feito**.

Depois de enviar, um aviso curto diz onde a tarefa está, como "Enviado. Movido para Feito." ou, se ela espera uma resposta, "Enviado. Movido para Depois até seg." **Abrir** leva você até ela. A conversa sair da sua caixa de entrada por alguns dias é só sobre o seu e-mail. A busca encontra uma tarefa pelo título ou por quem a recebeu, também em Depois e Feito.

**Para você** põe primeiro o que está atrasado ou vence até amanhã, depois as perguntas do seu Fleet, depois o resto. Em cada parte, as mais novas primeiro. Uma tarefa fica no lugar enquanto sua Machine a prepara e quando termina: só a marca muda. Os outros grupos abertos põem primeiro o que está atrasado ou vence até amanhã, o resto das mais novas para as mais antigas. A barra lateral segue a mesma ordem.

Uma tarefa com **Parece feito** aparece como uma feita, com o que mostra que está feita, como "PR #3451 mesclado". Ela ainda não foi fechada: **Reabrir** a devolve para a sua lista, e a sua Machine aprende com isso. Elas nunca aparecem como atrasadas e não contam como esperando por você. Uma tarefa com um rascunho de resposta também parece feita quando você respondeu nessa conversa, como no Gmail ou no Slack.

Uma tarefa cujo último passo ainda está aberto do lado de outra pessoa, como uma revisão, um merge ou uma resposta, mostra **Aguardando:** esse passo e continua aberta. Ela espera em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, e não conta como pronta para você. Uma nova mensagem sobre ela a traz de volta. O mesmo vale se você respondeu com uma pergunta: ela volta na manhã anterior ao prazo e diz por quem ainda aguarda.

Quando uma tarefa é por um resultado que outra pessoa entrega, como um contrato assinado ou um pagamento, os **Detalhes** dela mostram esse resultado como **Concluído quando**. Enviar a sua parte não a fecha: ela espera em **Aguardando outras pessoas** até uma mensagem mostrar o resultado e então se fecha sozinha, com **Desfazer**. Se nada chegar na hora de cobrar, ela volta com **Escreva um lembrete curto** no chat. Para mudar o que conta como concluído, diga no chat.

Uma tarefa que ninguém tocou em uma semana pergunta uma vez: **Ainda precisa?** **Não precisa** fecha a tarefa, com **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Abrir, uma mensagem no chat, uma edição, adiar ou uma mensagem nova sobre ela contam como um toque. Sem resposta por mais uma semana, ela vai para Volta mais tarde, sob Ainda precisa?, em vez de sumir. Aí o número no ícone do app e o resumo da manhã deixam de contá-la. Um toque traz de volta.

Quando nada precisa de você, sua Machine tira uma soneca na lista vazia. Enquanto verifica, ela acorda e avisa. Se uma verificação falhou ou está atrasada, a linha dela diz isso, com **Verificar agora** embaixo.

**Todos**, **Trabalho** e **Pessoal**, acima da lista na barra lateral, mostram todas as tarefas ou só um tipo. A sua Machine guarda a escolha, então o celular e o computador mostram a mesma lista. Enquanto Trabalho ou Pessoal estiver ativo, o topo da lista avisa, com **Mostrar todas** para voltar.

Uma tarefa de um projeto mostra o nome do projeto na linha abaixo do título; ele abre o projeto. **Projeto** em **Detalhes** muda ou tira o projeto. Veja [as tarefas de um projeto](projects.md#a-projects-to-dos).

**Área** em **Detalhes** passa a tarefa para a sua outra área. O que ela pode ler e de onde pode enviar muda junto; as mensagens de onde ela veio ficam onde estão. **Desfazer** no aviso que aparece depois a traz de volta.

Quando uma tarefa precisa de outra área para seguir e todas as mensagens de onde ela veio estão lá, ela muda sozinha e continua. Se não, ela pede com um botão **Mover para Trabalho**. Nada muda até você tocar; depois ela continua sozinha. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal muda sozinha assim que sabe onde fica.

Quando você inicia uma tarefa, ela sempre pode ler as mensagens de onde veio, também na caixa de outra empresa. Se precisar de outras mensagens de outra área, ela pede com **Usar este e-mail para esta tarefa**; um toque as adiciona e ela continua. O e-mail para outra das suas empresas vai desde o início para as tarefas dessa empresa. Uma tarefa da sua vida pessoal, como a família escrevendo para o seu endereço de trabalho, é Pessoal desde o início.

A resposta sai mesmo assim do endereço de trabalho onde chegou, e nunca aparece em uma Work Fleet nem no Graph da equipe.

Com duas ou mais esperando, **Percorrer** no cabeçalho de Para você passa por elas uma a uma, na ordem da lista, cada rascunho inteiro, com **Enviar** ou **Fazer**, **Pedir mudanças**, **Adiar** e **Pular**. No computador, Enter envia o que está na tela, `S` adia, `→` pula e Esc para. Abaixo do título, o cabeçalho também diz quanto tempo levam no seu ritmo, como "cerca de 2 min".

Uma tarefa que pergunta algo a você fica fora dos dois: ela precisa da sua resposta, não de um toque.

## Verificar agora

Sua Machine lê cada fonte a cada poucos minutos, de dia e de noite, e verifica o que chegou em busca de tarefas assim que 40 mensagens esperam ou a mensagem mais antiga de uma pessoa espera há 15 minutos. Newsletters, notificações e recibos entram na próxima verificação, em até uma hora.

**Verificar agora** lê na hora cada fonte. Sem nada aberto, toque na linha da sua Machine para ver, com **Detalhes**, que abre Verificações em Conexões. Com tarefas abertas, fica no topo no computador. Uma linha curta aparece ali só enquanto uma verificação roda, ou quando uma falhou ou está atrasada. Você também pode pedir no chat.

LinkedIn, X e Salesflare mantêm o próprio ritmo.

## Última verificação

Depois de uma verificação que leu e-mails novos, uma linha acima das suas tarefas diz o que ela encontrou, como "12 e-mails novos verificados às 16:11 · nada precisa de você" ou "· 2 tarefas novas". Quando uma tarefa nova espera um momento melhor, como seu resumo da manhã, ela diz até quando: "1 tarefa aguardando até amanhã 08:30".

Toque na linha para ver cada conversa: quem escreveu, o assunto, e a tarefa nova ou por que nada era preciso, como "Só em cópia, um colega está respondendo" ou "Reunião já marcada para quinta". Uma conversa não mostra motivo quando a verificação deu só um vago. A linha fica por 12 horas depois da verificação.

## Os botões

Uma tarefa mostra o próximo passo, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

**Pedir mudanças** diz o que mudar: como fazer, ou, com um rascunho pronto, o que mudar nele. Se a linha não couber no celular, **Adiar** vai para **…**. **Marcar como feita** (já está resolvida) também está lá: à vista numa pronta sem rascunho, senão no topo de **…**, também numa que precisa da sua decisão. Ela sai da lista na hora, com **Desfazer** na mensagem. Deslize a mensagem para o lado, ou arraste com o mouse, para fechá-la antes. A mudança continua.

Para fazer de outro jeito, diga isso no **Chat** dela.

Em **…** (no celular, o menu abre na parte de baixo da tela):

- **Passar…**: passe a tarefa para um colega, para o [Claude Code ou o Codex](hand-to-agent.md) (os que você configurou) ou [peça para alguém revisar](ask-to-review.md).
- **Repetir…**: a tarefa [volta em um ritmo](recurring.md).
- **Não precisa**: a tarefa some. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título, ou em **Nome** em **Detalhes**, para renomear a tarefa. Seu título fica, também quando a tarefa muda.

Uma tarefa fechada pode voltar com **Reabrir**. Ela também volta sozinha quando acontece algo novo, como uma nova mensagem da pessoa. Uma resposta sua não faz a tarefa voltar.

Uma tarefa que só importava até um certo momento, como uma confirmação antes de uma reunião, fecha sozinha quando esse momento passa. Ela vai para as feitas com "Não precisa mais" e quando foi. **Desfazer** traz a tarefa de volta por um dia.

Antes que uma mensagem ou um repasse para alguém apareça como pronto, sua Machine confere suas conversas recentes com as pessoas envolvidas, em grupo também, e espera o Slack lê-las. Se uma mensagem posterior mostra que já está feito, por exemplo a pessoa já foi chamada e disse sim, a tarefa fecha sozinha. **Desfazer** traz a tarefa de volta por um dia.

Quando uma mensagem mais nova muda o plano, como uma festa que muda de lugar ou uma reserva cancelada, The Machine atualiza as tarefas sozinha. Uma que ainda importa segue o novo plano. Uma sem mais nada a fazer vai para as feitas como "Não precisa", o chat dela diz "Atualizado:" e por quê, e **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma linha curta abaixo dos botões mostra o essencial: **Pedir mudanças** e **Não precisa** quando uma tarefa não está bem certa, e no seu primeiro rascunho pronto, que nada sai até você tocar em **Enviar**. Uma dica some de vez assim que você usa o botão dela ou toca no ×, em todos os seus aparelhos.

No seu primeiro dia, o topo de Tarefas diz oi pelo seu nome e mostra quem espera sua resposta há mais tempo. A Machine rascunha essa resposta primeiro, para que esteja pronta quando você chegar. Nada sai até você enviar. A linha some depois do seu primeiro dia ou da sua primeira tarefa decidida.

Cada tarefa começa pelo título. A linha abaixo diz de quem ela trata, a organização quando trata de uma (nunca só porque alguém trabalha lá), o projeto, Trabalho ou Pessoal (em **Todos**) e quando chegou, além de como está quando o grupo dela ainda não diz. Toque em um nome para abrir a página no Graph.

Às vezes uma linha discreta abaixo do texto diz o que não se sabe, como "Último contato há 12 dias por e-mail; nada desde então." Ela só aparece quando o último contato é antigo ou ainda está sem resposta, e cita canais não conectados por onde talvez tenham respondido, como o WhatsApp. Sua Machine prepara com os mesmos fatos, então ela diz o que não sabe em vez de adivinhar.

Quando ela cita um canal não conectado, Conectar ao lado abre essa conexão.

Um título diz o que precisa ser feito. Ele só muda quando isso muda, como com um novo pedido. Uma tarefa feita mantém o título, com embaixo como ela terminou, como o que foi enviado ou "Feito: Sam assinou na terça".

Acima do rascunho, uma linha discreta mostra a mensagem de onde ela veio, com o logo do serviço (Gmail, Slack, WhatsApp…). Toque nela para ler a conversa. O rascunho começa com o logo de para onde vai, então você vê se é uma resposta no Slack ou um e-mail antes de ler. Um passo sem rascunho, como um repasse, mostra o logo no botão.

Quando o rascunho segue o que outra pessoa disse em outra mensagem, como a sugestão de um colega no Slack, uma linha abaixo da tarefa diz isso, como "Com base em Sam no #ops". Toque nela para ler essa mensagem aqui, com Abrir no Slack ou no Gmail dentro dela. Quando essa mensagem é a própria origem da tarefa, a linha de origem já a mostra, então não aparece uma segunda linha.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma única conversa, da mais antiga para a mais nova, cada mensagem uma vez; a mensagem de que trata a tarefa tem uma linha fina ao lado.

**Detalhes** mostra o nome, o projeto e a área dela (toque em um para mudar), sua última nota e o resultado de um agente de código. **Chat ›** no fim dessa linha abre o chat. Uma tarefa concluída fica curta: o título, uma linha e o que foi enviado; a mensagem de onde ela veio fica nos **Detalhes**.

Uma tarefa "Aguardando" (alguém prometeu algo a você) traz um link para a sua última mensagem para a pessoa, aquela que espera resposta: "E-mail para Pat · ter".

## Crie uma você mesmo

**Nova tarefa** (abaixo de **Pesquisar** no computador) adiciona uma tarefa para qualquer coisa. Criar a tarefa não envia nada. Sem Trabalho ou Pessoal, ela vai para onde pertence: por quem e do que trata, por uma empresa ou caixa que cita, ou pelo e-mail que ela acompanha. Se nada indicar, ela começa onde está a maioria das suas tarefas. The Machine procura esse e-mail na sua caixa, também e-mails mais antigos que ainda não trouxe.

- **Vence**: digite um dia ou um horário, como "amanhã", "próxima sex", "3 nov", "15:00", "2pm", "em 2 horas" ou "amanhã 9". Ela entende outros idiomas também ("over 2 uur", "morgen 9u"). O ícone do calendário tem opções rápidas, como ao adiar, e **Escolher data**.
- **Mensagem**: anexe a mensagem de que ela trata: um e-mail, Slack, Teams, WhatsApp, Telegram ou qualquer outra mensagem que The Machine tenha. Busque por texto ou remetente. Cada resultado mostra de onde vem, quem enviou e quando.
- **Arquivos**: toque no clipe na caixa, cole uma captura de tela ou solte arquivos no formulário. No celular, você também pode tirar uma foto. Até 5 arquivos, dos mesmos tipos e tamanhos do chat (veja [Adicionar arquivos](card-chat.md#add-files)). × remove um.

Os arquivos ficam com a tarefa: aparecem nela e no chat dela, e a The Machine lê os arquivos quando trabalha nela. Só arquivos bastam: a The Machine lê o texto de um PDF ou arquivo de texto e preenche a tarefa a partir dele.
