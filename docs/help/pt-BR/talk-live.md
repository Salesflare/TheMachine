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

Ela conhece a tarefa em que você está: as mensagens, o rascunho e o chat dela. Também pode consultar suas outras tarefas.

A barra tem **Silenciar** e **Fim**. Diga tchau, ou que já terminou, e ela termina sozinha. Uma conversa dura até 10 minutos. Um minuto antes do fim, o cronômetro mostra quanto falta. Comece de novo para continuar.

## Repasse todas as suas tarefas falando

Toque em **Falar** na barra lateral (no menu, no celular) para repassar por voz tudo o que espera por você. A The Machine diz quantas há e passa por elas uma a uma: primeiro **Pronta**, depois **A decidir**. Ela também vê suas outras tarefas, como as que ainda estão **Preparando**, e avisa quando uma fica pronta.

Falar tem uma página própria: uma conversa do começo ao fim, com a tarefa de que ela fala no topo, o rascunho e **Abrir o chat**. Ela não leva você de chat em chat.

Peça para ler um rascunho, mudar, adiar, marcar como feita ou ir para a próxima. Enviar funciona como no chat de uma tarefa: um rascunho por pergunta, depois de um sim claro. O que você diz sobre uma tarefa fica no chat dessa tarefa. Quando chega uma tarefa nova, ela avisa numa pausa. Diga "crie uma tarefa para..." e ela cria uma nova, sem sair da que está aberta.

Enquanto isso você pode ir para outra página: a barra fica embaixo, e **Falar** na barra lateral traz você de volta. Esta conversa dura até 30 minutos.

## Peça coisas e envie com um sim

Quando você pede algo, como "escreva uma resposta dizendo que quinta está bom" ou "adie isso até segunda", a The Machine passa o pedido ao chat da tarefa, como se você tivesse digitado. O chat segue as regras de sempre: pode mudar o rascunho ou adiar a tarefa.

O chat também pode procurar coisas, como o horário de uma loja na web. Enquanto isso, mostra **Trabalhando nisso…**, e você pode continuar falando. Quando a resposta fica pronta, a The Machine conta para você, e onde a encontrou. Se você pedir outra coisa enquanto isso, ela espera a vez.

Para enviar um rascunho, diga isso. A The Machine pergunta antes, dizendo para quem e como, por exemplo "Enviar esta resposta para a Lotte por e-mail?". No celular, ela lê o rascunho inteiro em voz alta antes. Responda com um sim claro, em qualquer idioma, e esse rascunho é enviado.

- Ela só pergunta sobre o rascunho que aparece no chat. Se ele mudar depois da pergunta, ela pergunta de novo.
- Se a resposta não for um sim claro, nada é enviado e ela pergunta de novo. "Não" não envia nada.
- Um sim sempre envia um só rascunho. Para enviar vários, use a revisão de follow-ups.
- O chat mostra **Aprovado por voz** com **Desfazer** por alguns segundos antes do envio.

Você sempre pode tocar em **Aprovar** em vez disso.

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
