---
title: Falar ao vivo
area: cards
summary: Uma conversa falada com a The Machine sobre uma tarefa, com a voz da OpenAI. Ela pode pesquisar e sugerir, mas nunca envia nada.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Comece uma conversa

No chat de uma tarefa, toque na onda ao lado do microfone. Permita o microfone se o navegador pedir. Quando a barra mostrar **Ao vivo**, fale como numa ligação. A The Machine responde em voz alta.

Ela conhece a tarefa em que você está: as mensagens e o rascunho dela. Também pode consultar suas outras tarefas.

A barra tem **Silenciar** e **Fim**. Uma conversa dura até 10 minutos. Um minuto antes do fim, o cronômetro mostra quanto falta. Comece de novo para continuar.

## Nada é enviado de uma conversa

A The Machine não pode enviar, mudar nem aprovar nada enquanto você fala. Quando você pede algo, como "escreva uma resposta dizendo que quinta está bom", ela mostra o pedido acima da barra. Toque em **Enviar ao chat** para passá-lo ao chat. O que o chat redigir então espera o seu **Aprovar**, como sempre.

Dizer "sim" ou "envia" não faz nada. Só os seus toques contam.

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
