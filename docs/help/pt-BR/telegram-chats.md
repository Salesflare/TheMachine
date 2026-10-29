---
title: Chats do Telegram
area: connections
summary: Seus chats e pequenos grupos do Telegram, lidos como um dispositivo da sua própria conta. Responde só depois que você aprovar.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## O que ela lê

Seus chats privados e grupos de até 50 pessoas, como um dispositivo conectado à sua própria conta do Telegram, igual ao Telegram Desktop. Ao conectar, ela lê os últimos 7 dias e depois o que for chegando.

Ela nunca lê canais, bots, Mensagens Salvas nem as mensagens de serviço do próprio Telegram. Chats silenciados e arquivados também ficam de fora.

Ela não mexe no seu status de leitura e de online: nada é marcado como lido, e seu celular continua mostrando as mensagens novas como novas.

Isso é separado do [Telegram](telegram.md), em que o seu próprio bot envia suas tarefas para você.

## O que ela pode enviar

Um texto em um chat que já existe, só depois que você aprovar na tarefa. Os envios saem um de cada vez, com uma pausa entre eles.

Se uma tarefa chegou por e-mail, mas você fala com essa pessoa pelo Telegram, diga isso no chat da tarefa. A The Machine encontra a conversa que você já tem com ela e passa o rascunho para o Telegram, para você revisar e enviar. Ela nunca começa uma conversa nova.

## Conectar

1. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha Chats do Telegram.
2. Escolha **Escanear um QR code no Telegram do seu celular**.
3. No seu celular, no Telegram, abra Configurações, Dispositivos, **Link Desktop Device**, e escaneie o código.
4. Se a sua conta tem uma senha na nuvem, digite quando for pedida. Ela vai para o Telegram e nunca é guardada.

Configurando pelo celular, sem uma segunda tela para escanear? Escolha **Receber um código no Telegram para o seu número**. O formulário diz para onde o Telegram enviou o código: para o seu app do Telegram em outro dispositivo, por SMS ou para o seu e-mail de login. Não chegou? Toque em **Enviar o código de novo**.

No seu próprio computador, você também precisa de um ID de app do Telegram só seu. Crie um em [my.telegram.org](https://my.telegram.org), em API development tools, e preencha o api_id e o api_hash dele no formulário.

Ou rode `assistant connect telegram` em um terminal e escaneie o código que aparece lá.

## Quando ela para

- **Desconectada do Telegram**: o Telegram encerrou o login deste dispositivo, ou você desconectou pelo celular. Toque em **Reconectar** no cartão dela.
- **O Telegram parou de aceitar o ID de app**: o Telegram não aceita mais o ID de app que esta Machine usa. Nada é lido nem enviado até você tocar em **Reconectar** e adicionar um ID de app seu.

A The Machine usa a API do Telegram para isso. O Telegram pode limitar ou encerrar logins de apps como ela.

## Remover

**Conexões**, abra Chats do Telegram, **Detalhes** e depois **Desconectar**. Sua Machine sai do Telegram e exclui o que guardou do Telegram.

Ou encerre pelo celular: no Telegram, abra Configurações, Dispositivos, toque em The Machine e encerre a sessão.
