---
title: WhatsApp
area: connections
summary: Seus chats do WhatsApp, lidos como dispositivo conectado. As respostas só são enviadas depois da sua aprovação.
covers: connector:whatsapp
code: onboarding.py, whatsapp_setup.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 130c64388a71b7d1
---
## O que é lido

Seus chats do WhatsApp, como dispositivo conectado ao WhatsApp do seu celular, igual ao WhatsApp em um computador. Quando você conecta, o WhatsApp também envia seus chats antigos, muitas vezes de anos atrás. Sua Machine guarda tudo, mas só as mensagens dos últimos 7 dias viram tarefas.

Uma foto, mensagem de voz ou arquivo sem legenda aparece como o que é, por exemplo, "Foto", com o ícone correspondente. Os avisos do próprio WhatsApp, como o aviso de criptografia ou a entrada de alguém em um grupo, não têm texto e são ignorados.

## Ler fotos

O recurso fica desativado até você ativá-lo. Em **Conexões**, abra o WhatsApp, toque em **Detalhes** e ative **Ler fotos**. Aí, The Machine lê as fotos dos seus chats de trabalho: um recibo, uma captura de tela, a foto de uma carta ou de um formulário. **Também em conversas pessoais** permite ler também as fotos dos seus chats pessoais. Um chat é considerado de trabalho ou pessoal conforme as regras de compartilhamento, então um chat com a família continua sendo pessoal.

The Machine baixa cada foto uma vez e a guarda na sua Machine como um anexo de e-mail: criptografada quando a proteção de mensagens está ativada e excluída quando a mensagem é apagada. O modelo da própria Machine lê o que aparece na foto e o texto nela. Isso é considerado parte da mensagem, nunca uma instrução. JPEG, PNG e WebP de até 5 MB. Códigos de uso único em fotos são ignorados.

A tarefa e a mensagem mostram a foto. Toque nela para ver em tamanho maior.

## O que pode enviar

Um texto ou um arquivo com legenda opcional, para um chat que já existe, somente depois que você aprovar na tarefa. Antes do envio, a tarefa mostra o arquivo e você pode abri-lo. O arquivo pode ter até 18 MB. Uma resposta à mensagem do WhatsApp que originou a tarefa cita essa mensagem quando alguém enviou outra mensagem depois dela ou quando a conversa é em grupo. O rascunho indica **Como resposta**.

Se uma tarefa chegou por e-mail, mas você conversa com essa pessoa pelo WhatsApp, diga isso no chat da tarefa. The Machine encontra o chat que você já tem com essa pessoa e muda o rascunho para WhatsApp, para você revisar e enviar. Ela nunca inicia um chat novo.

O WhatsApp não oferece um jeito oficial de fazer isso. Ler mensagens e enviar uma resposta ocasional que você aprovou dificilmente vai causar problemas. O envio em massa ou automatizado pode bloquear uma conta.

## Conectar

Em uma Machine hospedada:

1. No painel, abra **Conexões**, depois **Chat** e escolha WhatsApp.
2. Toque em **Mostrar o código QR**.
3. No celular, abra o WhatsApp, vá para Configurações, Dispositivos conectados, Conectar um dispositivo e escaneie o código QR.
4. Em até um minuto, o WhatsApp aparece como conectado. Seu histórico de chats continua sendo carregado depois disso, e o cartão mostra a quantidade de mensagens recebidas durante esse processo.
   Se a conexão demorar demais, uma mensagem será exibida após alguns minutos. Toque em **Tentar de novo** para continuar de onde parou.

Está configurando no celular, sem uma segunda tela para escanear o código? Abra **No celular? Conecte com um código**, digite seu número e toque em **Pegar um código**. O WhatsApp vai pedir esse código.

No seu próprio computador: abra **Conexões**, depois **Chat**, escolha WhatsApp, digite seu número de celular com o código do país e toque em **Conectar**. Um código será exibido. No celular, abra o WhatsApp, vá para Configurações, Dispositivos conectados, Conectar um dispositivo, toque em **Conectar com número de telefone** e digite o código.

Ou execute `assistant connect whatsapp` e escaneie o código exibido no terminal. Na primeira vez, o sistema oferece instalar o conector do WhatsApp, uma versão fixada e verificada pelo checksum ([código-fonte](https://github.com/Salesflare/wacli)).

Em Dispositivos conectados, ele aparece como The Machine. Se uma Machine já estava conectada, o nome antigo continua aparecendo até você conectá-la de novo.

Se o WhatsApp desconectar sua Machine, o cartão mostrará **O WhatsApp desvinculou esta Machine**. Toque em **Reconectar** e conecte-a de novo: digite seu número de telefone e, em seguida, o código exibido no WhatsApp em Dispositivos conectados, **Conectar com número de telefone**. Ela será conectada no mesmo lugar de antes, então seus chats continuarão lá. Se você configurou seu próprio serviço para manter o WhatsApp sincronizado, ele será pausado enquanto você conecta e voltará a funcionar depois.

Se o WhatsApp demorar demais para responder, a configuração avisará. Toque em **Tentar de novo** um minuto depois para receber um novo código.

## Fotos de perfil

The Machine solicita ao WhatsApp as fotos de perfil das pessoas no seu Graph que não têm uma, até 50 por dia, durante a sincronização que mantém o WhatsApp atualizado. Nada é enviado a essas pessoas. Quem ocultar a foto de perfil para você continuará sem uma.

## Remover

- Em uma Machine hospedada: toque em **Remover** ao lado dela na página de configuração. Sua Machine se desvincula e apaga tudo o que guardou do WhatsApp.
- No seu próprio computador: abra **Conexões**, o WhatsApp e **Detalhes**, depois toque em **Desconectar**. Em seguida, desvincule-a também no celular.

## Desvincular no WhatsApp

No celular, abra o WhatsApp, vá para Configurações, Dispositivos conectados, toque na sua Machine e saia.
