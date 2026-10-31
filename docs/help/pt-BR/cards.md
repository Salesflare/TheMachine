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

A aba **Sugestões** agrupa as tarefas:

- **Pronta para você**: preparada e aguardando sua aprovação.
- **Precisa da sua decisão**: algo que só você pode decidir.
- **Preparando**: sua Machine está trabalhando nela. Uma tarefa em que você acabou de clicar em **Fazer** fica onde estava enquanto é preparada e depois vai para **Pronta para você**.
- **Volta mais tarde**: adiada.
- **Parecem feitas**: tarefas que já parecem concluídas. Recolhidas, logo acima de **Feito / dispensado**.
- **Feito / dispensado**: todas as tarefas concluídas, das mais novas para as mais antigas, 30 por vez conforme você rola.

Em **Parecem feitas** cada tarefa é uma linha: o título e o que mostra que está feita, como "PR #3451 mesclado". **Feito** fecha uma, **Marcar todas como feitas** fecha todas (com **Desfazer**), e **Não feito** a devolve como tarefa normal para a sua Machine aprender. Toque numa linha para ver a tarefa inteira. Elas nunca aparecem como atrasadas e não contam como esperando por você. Nada fecha sem você.

Uma tarefa cujo último passo ainda está aberto do lado de outra pessoa, como uma revisão, um merge ou uma resposta, mostra **Aguardando:** esse passo e continua aberta. Ela espera em **Aguardando outras pessoas**, recolhida acima de Volta mais tarde, e não conta como pronta para você. Uma nova mensagem sobre ela a traz de volta.

**Tudo em dia.** significa que nada precisa de você agora. A linha abaixo diz quando sua Machine olhou pela última vez.

**Todos**, **Trabalho** e **Pessoal**, acima da lista na barra lateral, mostram todas as tarefas ou só um tipo. A sua Machine guarda a escolha, então o celular e o computador mostram a mesma lista. Enquanto Trabalho ou Pessoal estiver ativo, o topo da lista avisa, com **Mostrar todas** para voltar.

Uma tarefa de um projeto mostra o nome do projeto na linha abaixo do título, que abre o projeto. **Mudar projeto** em **Mais** troca o projeto (numa tarefa concluída, em **Detalhes**). Veja [as tarefas de um projeto](graph.md#a-projects-to-dos).

## Os botões

Uma tarefa nova tem **Fazer**, **Marcar como feita**, **Adiar**, **Fazer de outro jeito** e **Não precisa**. Só alguns aparecem de cada vez. Os outros ficam em **Mais**, junto com **Renomear**.

- **Fazer**: sua Machine prepara a tarefa. Veja [Fazer](do-it.md).
- **Marcar como feita**: já está resolvida.
- **Adiar**: faz a tarefa voltar mais tarde. Veja [Adiar](snooze.md).
- **Fazer de outro jeito**: diga em poucas palavras o que você prefere. Em uma tarefa já preparada, o botão é **Pedir mudanças**: diga o que mudar no rascunho e ela refaz. **Revisar e enviar** continua ao lado.
- **Não precisa**: a tarefa some. Se quiser, escolha o motivo: **Não é relevante**, **Informações erradas** ou **Já resolvido**. Sua Machine aprende com isso.

Uma tarefa fechada pode voltar com **Reabrir**. Ela também volta sozinha quando acontece algo novo, como uma nova mensagem da pessoa. Uma resposta sua não faz a tarefa voltar.

Uma tarefa que só importava até um certo momento, como uma confirmação antes de uma reunião, fecha sozinha quando esse momento passa. Ela vai para as feitas com "Não precisa mais" e quando foi. **Desfazer** traz a tarefa de volta por um dia.

Nas suas primeiras tarefas, uma linha curta abaixo dos botões mostra o essencial: **Fazer de outro jeito** (ou **Pedir mudanças**) e **Não precisa** quando uma tarefa não está bem certa, e no seu primeiro rascunho pronto, que nada sai até você tocar em **Enviar**. Uma dica some de vez assim que você usa o botão dela ou toca no ×, em todos os seus aparelhos.

Cada tarefa começa pelo título. A linha abaixo diz de quem ela trata, a organização, o projeto, Trabalho ou Pessoal (em **Todos**) e quando chegou, além de como está quando o grupo dela ainda não diz. Toque em um nome para abrir a página no Graph.

Às vezes uma linha discreta abaixo do texto diz o que não se sabe, como "Último contato há 12 dias por e-mail; nada desde então." Ela só aparece quando o último contato é antigo ou ainda está sem resposta, e cita canais não conectados por onde talvez tenham respondido, como o WhatsApp. Sua Machine prepara com os mesmos fatos, então ela diz o que não sabe em vez de adivinhar.

Um título diz o que precisa ser feito. Ele só muda quando isso muda, como com um novo pedido. Uma tarefa feita mantém o título, com embaixo como ela terminou, como o que foi enviado ou "Feito: Sam assinou na terça".

**Detalhes** mostra a mensagem de onde ela veio (toque para ler a conversa), sua última nota e o resultado de um agente de código. **Chat ›** no fim dessa linha abre o chat. Uma tarefa concluída fica curta: o título, uma linha e o que foi enviado.

Uma tarefa "Aguardando" (alguém prometeu algo a você) traz um link para a sua última mensagem para a pessoa, aquela que espera resposta: "E-mail para Pat · ter".

## Crie uma você mesmo

**Nova tarefa** (abaixo de **Encontrar uma tarefa** no computador) adiciona uma tarefa para qualquer coisa. Criar a tarefa não envia nada.

- **Vence**: digite um dia ou um horário, como "amanhã", "próxima sex", "3 nov", "15:00", "2pm", "em 2 horas" ou "amanhã 9". Ela entende outros idiomas também ("over 2 uur", "morgen 9u"). O ícone do calendário tem opções rápidas, como ao adiar, e **Escolher data**.
- **E-mail**: anexe o e-mail de que ela trata. A busca é só nos seus e-mails, pelo assunto ou pelo remetente.
- **Arquivos**: toque no clipe na caixa, cole uma captura de tela ou solte arquivos no formulário. No celular, você também pode tirar uma foto. Até 5 arquivos, dos mesmos tipos e tamanhos do chat (veja [Adicionar arquivos](card-chat.md#add-files)). × remove um.

Os arquivos ficam com a tarefa: aparecem nela e no chat dela, e a The Machine lê os arquivos quando trabalha nela.
