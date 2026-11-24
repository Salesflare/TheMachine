---
title: Conversa ao vivo
area: cards
summary: Uma conversa por voz com The Machine sobre uma tarefa, usando a voz da OpenAI. Ela acontece no chat da tarefa, e só envia um rascunho depois que você confirma.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: f5555cb693a23682
---
## Comece uma conversa

No chat de uma tarefa, toque na onda ao lado do microfone e permita o acesso ao microfone, se solicitado. Quando a barra mostrar **Ao vivo**, fale como se estivesse em uma ligação. The Machine responde em voz alta. Fale por cima para interromper.

Ela conhece esta tarefa: as mensagens, o rascunho e o chat. Também pode consultar suas outras tarefas. Diga "marque como feito", "adie até amanhã às 9" ou "não precisa" para que ela faça isso. Diga "não, não era isso" logo depois para desfazer. Os horários seguem o fuso horário do seu [Horário de trabalho](work-hours.md).

Ela ouve no idioma do app e nos idiomas que o navegador lista. Tosse, ruído e outros idiomas não recebem resposta e não entram na transcrição.

A barra tem **Silenciar** e **Encerrar**. Diga tchau e a conversa termina sozinha. A conversa dura até 10 minutos, com uma contagem regressiva no último minuto. Comece de novo para continuar.

## Converse sobre todas as suas tarefas

Toque em **Conversa** na barra lateral (ou no menu, no celular). The Machine diz quantas tarefas estão esperando e percorre, uma por uma, as que estão em **Para você**, na ordem exibida na lista. Ela avisa quando uma tarefa marcada como **Preparando…** estiver pronta.

A conversa tem uma página própria: a tarefa em andamento fica no topo, com o rascunho e **Abrir o chat**.

Peça para ela ler um rascunho, alterá-lo, adiá-lo, marcá-lo como feito ou passar para a próxima tarefa. O que você disser sobre uma tarefa vai para o chat dela. The Machine menciona as novas tarefas quando há uma pausa. Diga "adicione uma tarefa para..." para incluir uma sem perder seu lugar.

Pergunte sobre uma pessoa, organização, projeto, reunião ou promessa, e ela pesquisa e mostra o que encontrou. Também pode descartar, renomear ou reabrir tarefas, inclusive as que estão em **Feito / descartado**. Para qualquer outra coisa, ela encaminha a pergunta para o chat de uma nova tarefa e conta a resposta.

Ela se lembra das conversas anteriores com você. Pergunte "o que decidi sobre o encontro fora do escritório?" e ela responde, inclusive quando você disse isso. Só a opção Conversa na barra lateral faz isso.

Enquanto isso, você pode acessar outras páginas: a barra continua na parte de baixo, e **Conversa** leva você de volta. Essa conversa dura até 30 minutos. Ela continua em segundo plano em computadores e Android. No iPhone, para quando o app sai da tela.

## Peça o que quiser e confirme antes de enviar

Peça algo, como "escreva uma resposta dizendo que quinta-feira funciona", e The Machine encaminha o pedido para o chat da tarefa como se você tivesse digitado. O chat segue as regras de sempre.

O chat também pode pesquisar informações, como o horário de funcionamento de uma loja. Ele mostra **Trabalhando nisso…** enquanto você continua conversando. Quando a resposta fica pronta, The Machine conta para você e diz onde encontrou a informação.

Para enviar um rascunho, peça o envio. The Machine lê o conteúdo em voz alta (para quem vai, o assunto e o texto) e pergunta algo como "Envio esta resposta por e-mail para Sam?". Você pode deixar o celular no bolso. Diga um sim claro, como "sim, envie", e o rascunho será enviado.

- Ela envia exatamente o rascunho que leu. Se o rascunho mudar, ela lê e pergunta de novo. Uma pergunta que você não responder em até 3 minutos expira.
- Qualquer resposta que não seja um sim claro não envia nada.
- Um rascunho que você já viu ou ouviu não é lido de novo. Ela só pergunta algo como "Envio para Pat?".
- Diga "envie todos os que estão prontos" e ela menciona todas as pessoas em uma pergunta. Um sim envia todos.
- Depois do sim, a Conversa mostra **Desfazer** com uma contagem regressiva. Toque ali ou diga "desfazer" ou "espera".
- Depois do envio, a Conversa diz "Enviado." e a tarefa mostra **Enviado para** a pessoa, com o horário. Se o envio falhar, a Conversa explica o motivo. Pergunte "foi enviado?" quando quiser: ela verifica, sem adivinhar.

Você também pode tocar em **Aprovar**.

Diga "faça isso" para iniciar The Machine na tarefa, como em **Fazer**. Diga "relate um bug" para enviar um relatório de bug, como em **Relatar um bug**, na Ajuda.

## Escolha uma voz

Em **Configurações**, **Geral**, em **Entrada por voz**, escolha uma **Voz** e toque em reproduzir para ouvi-la. **Cedar** é a opção padrão. A voz Cove do ChatGPT não está disponível.

## Um registro no chat

Tudo o que for dito aparece no chat da tarefa, abaixo da linha **Conversa ao vivo**, para você consultar depois.

## O que você precisa

A conversa ao vivo usa a voz da OpenAI, então sua Machine precisa de uma destas opções:

- Uma conta do ChatGPT: incluída nos planos que oferecem esse recurso.
- Uma chave de API da OpenAI: a OpenAI cobra por minuto, e a barra informa isso. Se você tiver as duas opções, sua Machine usa a chave.

**Configurações**, **Geral**, **Entrada por voz** mostra se a conversa ao vivo está pronta. Sem a OpenAI, a onda não aparece. O áudio vai direto do navegador para a OpenAI.

## Quando não funciona

- **O microfone está bloqueado**: permita o acesso ao microfone para este site nas configurações do navegador.
- **Não foi possível iniciar a conversa ao vivo**: confira sua conta do ChatGPT ou a chave da OpenAI e tente de novo.
- **A conversa ao vivo perdeu a conexão**: comece de novo. O que foi dito continua no chat.
- Se ela disser que não entendeu o que você falou, confira o microfone ou digite no chat.
