---
title: Chats do Signal
area: connections
summary: Seus chats e grupos do Signal, lidos como um aparelho conectado ao seu celular. Responde só depois que você aprovar.
covers: connector:signal
code: onboarding.py, signal_setup.py, signal_mirror.py, signal_store.py, signal_send.py
keywords: Signal, linked device, QR code
translated: b85609009f246615
---
## O que ela lê

Seus chats e grupos, como um aparelho conectado ao seu celular, igual ao Signal Desktop. O Signal não passa mensagens antigas para um aparelho recém-conectado, então ela lê a partir do momento em que você conecta.

Fotos, mensagens de voz e arquivos aparecem como o que são ("Enviou uma foto"), nunca com o conteúdo. Mídia de visualização única não guarda conteúdo nenhum. Edições e exclusões seguem o que aconteceu no seu celular, e mensagens temporárias saem da sua Machine quando o tempo delas acaba.

Stories, reações, chamadas e Nota para mim ficam de fora. Nada é marcado como lido.

## O que ela pode enviar

Um texto em um chat que já existe, só depois que você aprovar na tarefa. Uma resposta cita a mensagem que responde quando isso ajuda. Os envios saem um de cada vez, com uma pausa entre eles.

Se uma tarefa chegou por email mas você fala com essa pessoa pelo Signal, diga isso no chat da tarefa. The Machine encontra seu chat existente com ela e passa o rascunho para o Signal, para você revisar e enviar. Ela nunca começa um chat novo.

## Conectar

1. No painel, abra **Conexões**, depois **Chat**, e escolha Chats do Signal.
2. No seu celular, no Signal, abra Configurações, **Aparelhos conectados**, **Conectar novo aparelho**, e escaneie o código.

Você precisa de uma segunda tela para escanear: o Signal só conecta um aparelho por código QR. Ou rode `assistant connect signal` em um terminal e escaneie o código que aparece ali.

Sua Machine guarda as chaves do aparelho conectado com ela. Elas nunca saem dela.

## Quando ela para

Ele usa o signal-cli, um cliente não oficial do Signal. Sua Machine baixa uma versão fixada e confere o checksum antes de rodá-la. O Signal pode deixar de aceitá-lo a qualquer momento.

- **O Signal desvinculou esta Machine**: você a removeu no celular, ou o Signal encerrou a conexão. Toque em **Reconectar** em **Conexões** e escaneie um novo código.
- **Atualize The Machine para o Signal**: o Signal não aceita mais o cliente Signal desta Machine. Atualize The Machine.

## Remover

**Conexões**, abra Chats do Signal, **Detalhes** e depois **Desconectar**. Sua Machine exclui as chaves e o que guardou do Signal. Depois remova também no celular: Signal, Configurações, **Aparelhos conectados**, toque em The Machine e desconecte.
