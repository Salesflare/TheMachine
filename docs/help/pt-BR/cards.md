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

- **Pronta para você**: preparada e aguardando sua aprovação.
- **Precisa da sua decisão**: algo que só você pode decidir.
- **Preparando**: sua Machine está trabalhando nela. Uma tarefa em que você acabou de clicar em **Fazer** fica onde estava enquanto é preparada e depois vai para **Pronta para você**.
- **Feito agora**: uma última etapa que você confirmou, como enviar um formulário ou abrir uma issue, deu certo enquanto você estava fora. Ela mostra o que aconteceu até você tocar em **Entendi**, por um dia no máximo, e seu celular também fica sabendo. Depois fica só em Feito.
- **Volta mais tarde**: adiada, e as tarefas sem resposta a **Ainda precisa?** (abaixo).
- **Promessas**: o que você prometeu e o que outras pessoas prometeram a você. Veja [Promessas](promises.md).
- **Feito / dispensado**: todas as tarefas concluídas, pelo momento em que foram concluídas, das mais novas para as mais antigas, 30 por vez conforme você rola. Uma tarefa que você acabou de enviar fica no topo, e cada uma diz quando, como "Feito há 5 minutos". As que já parecem concluídas ficam entre elas pelo momento em que começaram a parecer, com a etiqueta **Parece feito**.

Depois de enviar, um aviso curto diz onde a tarefa está, como "Enviado. Movido para Feito." ou, se ela espera uma resposta, "Enviado. Movido para Depois até seg." **Abrir** leva você até ela. A conversa sair da sua caixa de entrada por alguns dias é só sobre o seu e-mail. A busca encontra uma tarefa pelo título ou por quem a recebeu, também em Depois e Feito.

Em Pronta para você, Precisa da sua decisão, Preparando e Aguardando outras pessoas, uma tarefa atrasada ou que vence até amanhã vem primeiro. As demais vêm das mais novas para as mais antigas, pela hora que cada tarefa mostra. A barra lateral segue a mesma ordem.

Uma tarefa com **Parece feito** aparece como uma feita, com o que mostra que está feita, como "PR #3451 mesclado". Ela ainda não foi fechada: **Reabrir** a devolve para a sua lista, e a sua Machine aprende com isso. Elas nunca aparecem como atrasadas e não contam como esperando por você.

Uma tarefa cujo último passo ainda está aberto do lado de outra pessoa, como uma revisão, um merge ou uma resposta, mostra **Aguardando:** esse passo e continua aberta. Ela espera em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, e não conta como pronta para você. Uma nova mensagem sobre ela a traz de volta.

Uma tarefa que ninguém tocou em uma semana pergunta uma vez: **Ainda precisa?** **Descartar** fecha a tarefa como **Não precisa**, com **Desfazer**. **Manter** mantém a tarefa, e ela não pergunta de novo. Abrir, uma mensagem no chat, uma edição, adiar ou uma mensagem nova sobre ela contam como um toque. Sem resposta por mais uma semana, ela vai para Volta mais tarde, sob Ainda precisa?, em vez de sumir. Um toque traz de volta.

**Tudo em dia.** significa que nada precisa de você agora. A linha abaixo diz quando sua Machine olhou pela última vez.

**Todos**, **Trabalho** e **Pessoal**, acima da lista na barra lateral, mostram todas as tarefas ou só um tipo. A sua Machine guarda a escolha, então o celular e o computador mostram a mesma lista. Enquanto Trabalho ou Pessoal estiver ativo, o topo da lista avisa, com **Mostrar todas** para voltar.

Uma tarefa de um projeto mostra o nome do projeto na linha abaixo do título; ele abre o projeto. **Projeto** em **Detalhes** muda ou tira o projeto. Veja [as tarefas de um projeto](graph.md#a-projects-to-dos).

**Área** em **Detalhes** passa a tarefa para a sua outra área, como uma pessoal que precisa sair do seu endereço de trabalho. O que ela pode ler e de onde pode enviar muda junto; as mensagens de onde ela veio ficam onde estão. **Desfazer** no aviso que aparece depois a traz de volta.

Quando uma tarefa precisa de outra área para seguir, ela pede com um botão **Mover para Trabalho**. Nada muda até você tocar; depois ela continua sozinha. Uma tarefa que você adicionou sem escolher Trabalho ou Pessoal muda sozinha assim que sabe onde fica.

Quando você inicia uma tarefa, ela sempre pode ler as mensagens de onde veio, também na caixa de outra empresa. Se precisar de outras mensagens de outra área, ela pede com **Usar este e-mail para esta tarefa**; um toque as adiciona e ela continua. O e-mail para outra das suas empresas vai desde o início para as tarefas dessa empresa. Uma tarefa da sua vida pessoal, como a família escrevendo para o seu endereço de trabalho, é Pessoal desde o início.

## Os botões

Uma tarefa mostra o próximo passo, como **Fazer** ou **Revisar e enviar**, com **Adiar** ao lado. Veja [Fazer](do-it.md) e [Adiar](snooze.md).

Ainda não preparada, ela tem **Mudar a abordagem** (diga como fazer de outro jeito); pronta, **Pedir mudanças** (diga o que mudar no rascunho). Se a linha não couber no celular, **Adiar** vai para **…**. **Marcar como feita** (já está resolvida) também está lá: à vista sem rascunho, senão no topo de **…**.

Para fazer de outro jeito, diga isso no **Chat** dela.

Em **…** (no celular, o menu abre na parte de baixo da tela):

- **Passar…**: passe a tarefa para um colega, para o [Claude Code ou o Codex](hand-to-agent.md) (os que você configurou) ou [peça para alguém revisar](ask-to-review.md).
- **Repetir…**: a tarefa [volta em um ritmo](recurring.md).
- **Não precisa**: a tarefa some. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Toque no título, ou em **Nome** em **Detalhes**, para renomear a tarefa. Seu título fica, também quando a tarefa muda.

Uma tarefa fechada pode voltar com **Reabrir**. Ela também volta sozinha quando acontece algo novo, como uma nova mensagem da pessoa. Uma resposta sua não faz a tarefa voltar.

Uma tarefa que só importava até um certo momento, como uma confirmação antes de uma reunião, fecha sozinha quando esse momento passa. Ela vai para as feitas com "Não precisa mais" e quando foi. **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma linha curta abaixo dos botões mostra o essencial: **Mudar a abordagem** (ou **Pedir mudanças**) e **Não precisa** quando uma tarefa não está bem certa, e no seu primeiro rascunho pronto, que nada sai até você tocar em **Enviar**. Uma dica some de vez assim que você usa o botão dela ou toca no ×, em todos os seus aparelhos.

No seu primeiro dia, o topo de Tarefas diz oi pelo seu nome e mostra quem espera sua resposta há mais tempo. A Machine rascunha essa resposta primeiro, para que esteja pronta quando você chegar. Nada sai até você enviar. A linha some depois do seu primeiro dia ou da sua primeira tarefa decidida.

Cada tarefa começa pelo título. A linha abaixo diz de quem ela trata, a organização, o projeto, Trabalho ou Pessoal (em **Todos**) e quando chegou, além de como está quando o grupo dela ainda não diz. Toque em um nome para abrir a página no Graph.

Às vezes uma linha discreta abaixo do texto diz o que não se sabe, como "Último contato há 12 dias por e-mail; nada desde então." Ela só aparece quando o último contato é antigo ou ainda está sem resposta, e cita canais não conectados por onde talvez tenham respondido, como o WhatsApp. Sua Machine prepara com os mesmos fatos, então ela diz o que não sabe em vez de adivinhar.

Um título diz o que precisa ser feito. Ele só muda quando isso muda, como com um novo pedido. Uma tarefa feita mantém o título, com embaixo como ela terminou, como o que foi enviado ou "Feito: Sam assinou na terça".

Acima do rascunho, uma linha discreta mostra a mensagem de onde ela veio, com o logo do serviço (Gmail, Slack, WhatsApp…). Toque nela para ler a conversa. O rascunho começa com o logo de para onde vai, então você vê se é uma resposta no Slack ou um e-mail antes de ler. Um passo sem rascunho, como um repasse, mostra o logo no botão.

Um chat (Slack, WhatsApp, Telegram, Intercom…) aparece como uma única conversa, da mais antiga para a mais nova, cada mensagem uma vez; a mensagem de que trata a tarefa tem uma linha fina ao lado.

**Detalhes** mostra o nome, o projeto e a área dela (toque em um para mudar), sua última nota e o resultado de um agente de código. **Chat ›** no fim dessa linha abre o chat. Uma tarefa concluída fica curta: o título, uma linha e o que foi enviado; a mensagem de onde ela veio fica nos **Detalhes**.

Uma tarefa "Aguardando" (alguém prometeu algo a você) traz um link para a sua última mensagem para a pessoa, aquela que espera resposta: "E-mail para Pat · ter".

## Crie uma você mesmo

**Nova tarefa** (abaixo de **Pesquisar** no computador) adiciona uma tarefa para qualquer coisa. Criar a tarefa não envia nada. Sem Trabalho ou Pessoal, ela vai para onde pertence: por quem e do que trata, ou pelo e-mail que ela acompanha. The Machine procura esse e-mail na sua caixa, também e-mails mais antigos que ainda não trouxe.

- **Vence**: digite um dia ou um horário, como "amanhã", "próxima sex", "3 nov", "15:00", "2pm", "em 2 horas" ou "amanhã 9". Ela entende outros idiomas também ("over 2 uur", "morgen 9u"). O ícone do calendário tem opções rápidas, como ao adiar, e **Escolher data**.
- **E-mail**: anexe o e-mail de que ela trata. A busca é só nos seus e-mails, pelo assunto ou pelo remetente.
- **Arquivos**: toque no clipe na caixa, cole uma captura de tela ou solte arquivos no formulário. No celular, você também pode tirar uma foto. Até 5 arquivos, dos mesmos tipos e tamanhos do chat (veja [Adicionar arquivos](card-chat.md#add-files)). × remove um.

Os arquivos ficam com a tarefa: aparecem nela e no chat dela, e a The Machine lê os arquivos quando trabalha nela. Só arquivos bastam: a The Machine lê o texto de um PDF ou arquivo de texto e preenche a tarefa a partir dele.
