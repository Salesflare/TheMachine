---
title: Converse ao vivo
area: cards
summary: Uma conversa por voz com a The Machine sobre uma tarefa, usando a voz da OpenAI. Funciona no chat da tarefa e só envia um rascunho depois que você autoriza.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: da63957f0556ff4f
---
## Comece uma conversa

No chat de uma tarefa, toque na onda ao lado do microfone e permita o acesso ao microfone, se solicitado. Quando a barra mostrar **Ao vivo**, fale como se estivesse em uma ligação. A The Machine responde em voz alta. Fale por cima para interrompê-la.

Ela conhece esta tarefa: as mensagens, o rascunho e o chat. Também pode consultar suas outras tarefas. Diga "marque esta tarefa como feita", "adie até amanhã às 9" ou "não precisa" para que ela faça isso. Diga "não, não era isso" logo em seguida para desfazer. Os horários seguem o fuso horário do seu [Horário de trabalho](work-hours.md).

Ela reconhece o idioma do app e os idiomas listados no seu navegador. Tosse, ruído e outros idiomas não recebem resposta nem aparecem na transcrição.

A barra tem as opções **Silenciar** e **Encerrar**. Despeça-se e a conversa termina sozinha. Cada conversa dura até 10 minutos, com uma contagem regressiva no último minuto. Comece outra para continuar.

## Converse sobre todas as suas tarefas

Toque em **Conversar** na barra lateral (no menu, pelo celular). A The Machine diz quantas tarefas estão pendentes e percorre, uma por uma e na ordem em que aparecem na lista, as tarefas em **Para você**. Ela avisa quando uma tarefa marcada como **Preparando…** estiver pronta.

O recurso de conversa tem uma página própria: a tarefa em questão fica no topo, com o rascunho e a opção **Abrir o chat**.

Peça para ler um rascunho, alterá-lo, adiá-lo, marcá-lo como feito ou ir para a próxima tarefa. O que você disser sobre uma tarefa vai para o chat dela. A The Machine menciona novas tarefas quando há uma pausa. Diga "adicione uma tarefa para..." para criar uma sem perder seu lugar.

Pergunte sobre uma pessoa, organização, projeto, reunião ou promessa para que ela pesquise e mostre as informações. Ela também pode descartar, renomear ou reabrir tarefas, inclusive as que estão em **Feito / descartado**. Para qualquer outra coisa, ela encaminha a pergunta para o chat de uma nova tarefa e conta a resposta.

Ela se lembra das conversas anteriores. Pergunte "o que decidi sobre o encontro fora do escritório?" para saber a resposta e quando você disse isso. Só o recurso Conversar na barra lateral faz isso.

Enquanto isso, você pode acessar outras páginas: a barra continua na parte inferior e **Conversar** leva você de volta. Esta conversa dura até 30 minutos. Ela continua em segundo plano em computadores e Android. No iPhone, para quando o app sai da tela.

## Peça algo e autorize o envio

Peça algo, como "escreva uma resposta dizendo que quinta-feira funciona", e a The Machine envia o pedido para o chat da tarefa como se você tivesse digitado. O chat segue as regras de sempre.

O chat também pode pesquisar informações, como o horário de funcionamento de uma loja. Ele mostra que está trabalhando, e você pode continuar conversando. Quando a resposta estiver pronta, a The Machine avisa e diz onde encontrou a informação.

Para enviar um rascunho, peça. A The Machine lê o texto em voz alta, incluindo o destinatário, o assunto e a mensagem, e pergunta algo como "Enviar esta resposta por e-mail para Sam?". Você pode fazer isso com o celular no bolso. Diga um sim claro, como "sim, envie", para que o rascunho seja enviado.

- Ela envia exatamente o rascunho que leu. Se o rascunho mudar, ela lê e pergunta de novo. Uma pergunta sem resposta expira após 3 minutos.
- Qualquer resposta que não seja um sim claro não envia nada.
- Um rascunho que você já viu ou ouviu não é lido de novo. Ela só pergunta algo como "Enviar para Pat?".
- Diga "envie todos os que estão prontos" para que ela diga todos os destinatários em uma só pergunta. Um sim envia todos.
- Depois do sim, Conversar mostra **Desfazer** com uma contagem regressiva. Toque nessa opção ou diga "desfazer" ou "espera".
- Depois do envio, Conversar diz "Enviado." e a tarefa mostra **Enviado para** essa pessoa, com o horário. Se não der certo, Conversar explica o motivo. Pergunte "foi enviado?" a qualquer momento: ela verifica e nunca adivinha.

Tocar em **Aprovar** também funciona.

Diga "faça" para iniciar a The Machine na tarefa, como em **Fazer**. Diga "relate um bug" para enviar um relatório de bug, como em **Relatar um bug** na Ajuda.

## Escolha uma voz

Em **Configurações**, **Geral**, na seção **Entrada por voz**, escolha uma **Voz** e toque em reproduzir para ouvi-la. **Cedar** é a voz padrão. A voz Cove do ChatGPT não está disponível.

## Um registro no chat

Tudo o que for dito aparece no chat da tarefa, abaixo da linha **Conversa ao vivo**, para você consultar depois.

## O que você precisa

A conversa ao vivo usa a voz da OpenAI. Para isso, sua Machine precisa de uma destas opções:

- Uma conta do ChatGPT: incluída nos planos que oferecem esse recurso.
- Uma chave de API da OpenAI: a OpenAI cobra por minuto, e a barra informa isso. Se você tiver as duas opções, sua Machine usa a chave.

Em **Configurações**, **Geral**, **Entrada por voz**, você pode ver se a conversa ao vivo está pronta. Sem a OpenAI, a onda não aparece. O áudio vai do seu navegador diretamente para a OpenAI.

## Quando não funciona

- **O microfone está bloqueado**: permita o acesso ao microfone para este site nas configurações do navegador.
- **Não foi possível iniciar a conversa ao vivo**: confira se você entrou na sua conta do ChatGPT ou se a chave da OpenAI está correta e tente de novo.
- **A conversa ao vivo perdeu a conexão**: comece de novo. O que foi dito continua no chat.
- Se a The Machine disser que não entendeu o que você falou, confira o microfone ou digite no chat.
