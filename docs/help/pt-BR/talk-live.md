---
title: Falar ao vivo
area: cards
summary: Uma conversa falada com a The Machine sobre uma tarefa, com a voz da OpenAI. Ela trabalha no chat da tarefa e só envia um rascunho depois que você diz sim.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Comece uma conversa

No chat de uma tarefa, toque na onda ao lado do microfone. Permita o microfone se o navegador pedir. Quando a barra mostrar **Ao vivo**, fale como numa ligação. A The Machine responde em voz alta, e você pode falar por cima para interrompê-la.

Ela conhece a tarefa em que você está: as mensagens, o rascunho e o chat dela. Também pode consultar suas outras tarefas. Diga "marca como feita", "adia" ou "não precisa" e ela faz isso sozinha. Diga "não, isso não" logo depois para desfazer.

Ouve nos seus idiomas: o do app e os que o seu navegador indica. Um ruído, uma tosse ou um som em outro idioma não recebe resposta e fica fora da transcrição.

A barra tem **Silenciar** e **Fim**. Diga tchau, ou que já terminou, e ela termina sozinha. Uma conversa dura até 10 minutos. Um minuto antes do fim, o cronômetro mostra quanto falta. Comece de novo para continuar.

## Repasse todas as suas tarefas falando

Toque em **Falar** na barra lateral (no menu, no celular) para repassar por voz tudo o que espera por você. A The Machine diz quantas há e passa por elas uma a uma: primeiro **Pronta**, depois **A decidir**. Ela também vê suas outras tarefas, como as que ainda estão **Preparando**, e avisa quando uma fica pronta.

Falar tem uma página própria: uma conversa do começo ao fim, com a tarefa de que ela fala no topo, o rascunho e **Abrir o chat**. Ela não leva você de chat em chat.

Peça para ler um rascunho, mudar, adiar, marcar como feita ou ir para a próxima. Enviar funciona como no chat de uma tarefa: um rascunho por pergunta, depois de um sim claro. O que você diz sobre uma tarefa fica no chat dessa tarefa. Quando chega uma tarefa nova, ela avisa numa pausa. Diga "crie uma tarefa para..." e ela cria uma nova, sem sair da que está aberta.

Ela também alcança o resto da The Machine. Pergunte sobre uma pessoa, uma organização, um projeto, uma reunião ou uma promessa, e ela procura e mostra. Ela pode adiar uma tarefa, marcar como feita, dispensar, renomear ou reabrir, até uma em **Feito / dispensado**. Para todo o resto, ela cria uma tarefa, deixa o chat dela cuidar disso e conta a resposta.

Enquanto isso você pode ir para outra página: a barra fica embaixo, e **Falar** na barra lateral traz você de volta. Esta conversa dura até 30 minutos. Ela continua em segundo plano no computador e no Android. No iPhone, ela para quando o app sai da tela.

## Peça coisas e envie com um sim

Quando você pede algo, como "escreva uma resposta dizendo que quinta está bom" ou "adie isso até segunda", a The Machine passa o pedido ao chat da tarefa, como se você tivesse digitado. O chat segue as regras de sempre: pode mudar o rascunho ou adiar a tarefa.

O chat também pode procurar coisas, como o horário de uma loja na web. Enquanto isso, mostra **Trabalhando nisso…**, e você pode continuar falando. Quando a resposta fica pronta, a The Machine conta para você, e onde a encontrou. Se você pedir outra coisa enquanto isso, ela espera a vez.

Para enviar um rascunho, diga isso. A The Machine pergunta antes, dizendo para quem e como, por exemplo "Enviar esta resposta para a Lotte por e-mail?". Antes, ela lê o rascunho inteiro em voz alta: para quem vai, o assunto e o texto. Assim funciona também com o celular no bolso. Responda com um sim claro, como "sim, envia", e esse rascunho é enviado.

- Ela envia exatamente o rascunho que leu. Se ele mudar depois da pergunta, ela lê de novo e pergunta de novo. Uma pergunta sem resposta em 3 minutos expira.
- Se a resposta não for um sim claro, nada é enviado e ela pergunta de novo. "Não" não envia nada.
- Um rascunho que você já viu na tela, ou ouviu nesta conversa, não é lido de novo: ela só pergunta, por exemplo "Enviar para o Nick?".
- Diga "envie os dois" ou "envie todos os prontos" e ela cita todos em uma pergunta. Um sim envia cada um.
- Falar mostra **Desfazer** com uma contagem regressiva por alguns segundos antes do envio, depois **Enviado**. Toque nele, ou diga "desfazer" ou "espera".

Você sempre pode tocar em **Aprovar** em vez disso.

"Faz isso" coloca a The Machine na tarefa, como **Fazer**, inclusive no navegador. "Marca como feita" fecha a tarefa. Diga "relatar um bug" e ela envia um relato, como **Relatar um bug** na Ajuda, perguntando antes se pode incluir mais.

## Escolha uma voz

Em **Configurações**, **Geral**, em **Entrada por voz**, escolha em **Voz** como a The Machine soa. Toque em reproduzir para ouvir uma amostra. **Cedar** é a voz padrão. A voz Cove do ChatGPT não está disponível para falar ao vivo.

## Um registro no chat

O que vocês dois dizem é escrito no chat da tarefa, sob uma linha **Conversa ao vivo**. Você pode reler depois.

## Do que você precisa

Falar ao vivo usa a voz em tempo real da OpenAI, então a OpenAI precisa estar configurada no OpenClaw:

- Um login do ChatGPT: incluído no seu plano, quando o seu plano tem acesso.
- Uma chave de API da OpenAI: a OpenAI cobra da sua chave por minuto de conversa, e a barra avisa. Quando os dois estão configurados, o OpenClaw usa a chave.

**Configurações**, **Geral**, **Entrada por voz** mostra se Falar ao vivo está pronto. Sem a OpenAI, a onda não aparece. Seu áudio vai do navegador direto para a OpenAI. Sua chave nunca chega ao navegador.

## Quando não funciona

- **O microfone está bloqueado**: permita o microfone para este site nas configurações do seu navegador.
- **Falar ao vivo não conseguiu começar**: confira a OpenAI no OpenClaw e tente de novo.
- **Falar ao vivo perdeu a conexão**: comece de novo. O que foi dito até agora fica no chat.
