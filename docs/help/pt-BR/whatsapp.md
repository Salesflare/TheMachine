---
title: WhatsApp
area: connections
summary: Leia suas conversas do WhatsApp em um dispositivo conectado. As respostas só são enviadas depois da sua aprovação.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 881c555219a98f0f
---
## O que é lido

Suas conversas do WhatsApp, como em um dispositivo conectado ao WhatsApp do seu celular, parecido com o WhatsApp no computador. Quando você conecta, o WhatsApp também envia suas conversas antigas, muitas vezes de vários anos. Sua Machine guarda tudo, mas só as mensagens dos últimos 7 dias viram tarefas.

Uma foto, mensagem de voz ou arquivo sem legenda aparece identificado pelo tipo, como "Foto", com o ícone correspondente. Avisos do próprio WhatsApp, como o aviso de criptografia ou de alguém entrando em um grupo, não têm texto e são ignorados.

## Ler fotos

Fica desativado até você ativar. Em **Conexões**, abra o WhatsApp, toque em **Detalhes** e ative **Ler fotos** para que sua Machine leia as fotos nas conversas de trabalho: um recibo, uma captura de tela, uma foto de uma carta ou de um formulário. **Também em conversas pessoais** também lê as fotos nas suas conversas pessoais. Uma conversa é de trabalho ou pessoal conforme o compartilhamento a classifica, então uma conversa com a família continua sendo pessoal.

Sua Machine baixa cada foto uma vez e a mantém nela, como um anexo de e-mail: criptografada quando a proteção de mensagens está ativada e excluída quando a mensagem é removida. O modelo da própria Machine lê o que aparece na foto e o texto nela. Isso é considerado parte da mensagem, nunca uma instrução. JPEG, PNG e WebP de até 5 MB. Um código de uso único em uma foto é ignorado.

A tarefa e a mensagem mostram a foto. Toque nela para vê-la em tamanho grande.

## O que pode enviar

Um texto para uma conversa existente, somente depois que você aprovar na tarefa. Uma resposta à mensagem do WhatsApp que originou a tarefa cita essa mensagem quando houve outras mensagens depois dela ou quando é em um grupo. O rascunho mostra **Como resposta**.

Se uma tarefa chegou por e-mail, mas você conversa com essa pessoa pelo WhatsApp, diga isso no chat da tarefa. Sua Machine encontra a conversa existente com essa pessoa e muda o rascunho para WhatsApp, para você revisar e enviar. Ela nunca inicia uma conversa nova.

O WhatsApp não oferece uma forma oficial de fazer isso. É muito improvável que ler mensagens e enviar uma resposta ocasional que você aprovou cause problemas; o envio em massa ou automatizado pode bloquear uma conta.

## Conectar

Em uma Machine hospedada:

1. No painel, abra **Conexões**, depois **Chat** e escolha WhatsApp.
2. Toque em **Mostrar o código QR**.
3. No celular, abra Configurações, Dispositivos conectados, Conectar um dispositivo no WhatsApp e escaneie o código QR.
4. O WhatsApp aparece como conectado em até um minuto. Depois disso, o histórico das conversas continua chegando, e o cartão mostra a contagem de mensagens enquanto isso acontece.
   Se a conexão demorar demais, você verá um aviso após alguns minutos. Toque em **Tentar de novo** para continuar de onde parou.

Configurando pelo celular, sem outra tela para escanear o código? Abra **No celular? Conecte com um código**, digite seu número e toque em **Pegar um código**. O WhatsApp pedirá esse código.

No seu próprio computador: abra **Conexões**, depois **Chat**, escolha WhatsApp, digite seu número de telefone com o código do país e toque em **Conectar**. Um código será exibido. No celular, abra Configurações, Dispositivos conectados, Conectar um dispositivo no WhatsApp, depois **Conectar com número de telefone** e digite o código.

Ou execute `assistant connect whatsapp` e escaneie o código exibido no terminal. Na primeira vez, você verá a opção de instalar o conector do WhatsApp, uma versão fixada cuja soma de verificação foi conferida ([código-fonte](https://github.com/Salesflare/wacli)).

Em Dispositivos conectados, ela aparece como The Machine. Uma Machine conectada anteriormente mantém o nome antigo ali até você conectá-la novamente.

## Fotos de perfil

Sua Machine pede ao WhatsApp as fotos de perfil das pessoas no seu Graph que ainda não têm uma, no máximo 50 por dia, por meio da sincronização que mantém o WhatsApp atualizado. Nada é enviado a essas pessoas. Quem oculta a foto de você continua sem foto.

## Remover

- Em uma Machine hospedada: toque em **Remover** ao lado dela na página de configuração. Sua Machine se desconecta e exclui o que guardou do WhatsApp.
- No seu próprio computador: abra WhatsApp em **Conexões**, toque em **Detalhes** e depois em **Desconectar**. Em seguida, desconecte-a também pelo celular.

## Desconectar no WhatsApp

No celular, abra Configurações, Dispositivos conectados no WhatsApp, toque na sua Machine e saia da conta.
