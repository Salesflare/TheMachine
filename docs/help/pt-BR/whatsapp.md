---
title: WhatsApp
area: connections
summary: Seus chats do WhatsApp, lidos como dispositivo conectado. As respostas só são enviadas depois da sua aprovação.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 9446d22f96229653
---
## O que ela lê

Seus chats do WhatsApp, como dispositivo conectado ao WhatsApp do seu celular, igual ao WhatsApp no computador. Quando você conecta sua Machine, o WhatsApp também envia seus chats antigos, muitas vezes de vários anos. Sua Machine mantém tudo isso, mas só as mensagens dos últimos 7 dias viram tarefas.

Uma foto, mensagem de voz ou arquivo sem legenda aparece como o que é, por exemplo, «Foto», com o ícone correspondente. Os avisos do próprio WhatsApp, como o aviso de criptografia ou de alguém entrando em um grupo, não têm texto e são ignorados.

## Ler fotos

Esse recurso fica desativado até você ativá-lo. Em **Conexões**, abra o WhatsApp, toque em **Detalhes** e ative **Ler fotos**. Assim, sua Machine lê as fotos dos seus chats de trabalho: um recibo, uma captura de tela, uma foto de uma carta ou de um formulário. **Também em conversas pessoais** faz o mesmo com as fotos dos seus chats pessoais. Um chat é de trabalho ou pessoal conforme a forma como ele é compartilhado, então um chat com a família continua sendo pessoal.

Sua Machine baixa cada foto uma vez e a mantém nela como um anexo de e-mail: criptografada quando a proteção de mensagens está ativada e excluída quando a mensagem é apagada. O modelo da Machine lê o que aparece na foto e o texto nela. Isso é considerado parte da mensagem, nunca uma instrução. São compatíveis arquivos JPEG, PNG e WebP de até 5 MB. Um código de uso único que apareça em uma foto é ignorado.

A tarefa e a mensagem mostram a foto. Toque nela para ver em tamanho grande.

## O que ela pode enviar

Um texto ou um arquivo com legenda opcional, para um chat que já existe, e só depois que você aprovar na tarefa. Antes do envio, a tarefa mostra o arquivo e você pode abri-lo. O arquivo pode ter até 18 MB. Se alguém enviar outra mensagem depois daquela que originou a tarefa, ou se a mensagem tiver sido enviada em um grupo, a resposta cita a mensagem original. O rascunho mostra **Como resposta**.

Se uma tarefa chegou por e-mail, mas você conversa com essa pessoa pelo WhatsApp, diga isso no chat da tarefa. Sua Machine encontra o chat que você já tem com ela e muda o rascunho para WhatsApp, para você revisar e enviar. Ela nunca inicia um chat novo.

O WhatsApp não oferece uma forma oficial de fazer isso. Ler mensagens e enviar uma resposta ocasional que você aprovou dificilmente causará problemas. O envio em massa ou automatizado pode fazer com que a conta seja bloqueada.

## Conectar

Em uma Machine hospedada:

1. No painel, abra **Conexões**, depois **Chat**, e escolha WhatsApp.
2. Toque em **Mostrar o código QR**.
3. No celular, abra o WhatsApp, toque em **Configurações**, **Aparelhos conectados**, **Conectar um aparelho** e escaneie o código QR.
4. Em até um minuto, o WhatsApp aparece como conectado. Depois disso, o histórico do chat continua chegando, e o cartão mostra quantas mensagens chegaram enquanto isso.
   Se a conexão demorar demais, uma mensagem vai avisar depois de alguns minutos. Toque em **Tentar de novo** para continuar de onde parou.

Está configurando pelo celular e não tem outra tela para escanear o código? Abra **No celular? Conecte com um código**, informe seu número e toque em **Pegar um código**. O WhatsApp vai pedir esse código.

No seu próprio computador: abra **Conexões**, depois **Chat**, escolha WhatsApp, informe seu número de telefone com o código do país e toque em **Conectar**. Um código vai aparecer. No celular, abra o WhatsApp, toque em **Configurações**, **Aparelhos conectados**, **Conectar um aparelho** e depois em **Conectar com número de telefone**. Em seguida, informe o código.

Ou execute `assistant connect whatsapp` e escaneie o código que aparece no terminal. Na primeira vez, a opção de instalar o conector do WhatsApp será exibida. Ele é uma versão fixada e verificada pelo checksum ([fonte](https://github.com/Salesflare/wacli)).

Em **Aparelhos conectados**, ela aparece como The Machine. Uma Machine conectada anteriormente continua aparecendo com o nome antigo até você conectá-la de novo.

Se o WhatsApp desconectar sua Machine, o cartão vai mostrar **O WhatsApp desvinculou esta Machine**. Toque em **Reconectar** e conecte-a novamente.

## Fotos de perfil

A Machine pede ao WhatsApp as fotos de perfil das pessoas do seu Graph que ainda não têm uma, no máximo 50 por dia, durante a sincronização que mantém o WhatsApp atualizado. Nada é enviado a essas pessoas. Quem oculta a foto de você continua sem uma foto de perfil.

## Remover

- Em uma Machine hospedada: toque em **Remover** ao lado dela na página de configuração. Sua Machine se desvincula e apaga o que guardou do WhatsApp.
- No seu próprio computador: abra **Conexões**, escolha WhatsApp, toque em **Detalhes** e depois em **Desconectar**. Em seguida, desvincule-a também no celular.

## Desvincular no WhatsApp

No celular, abra o WhatsApp, toque em **Configurações**, **Aparelhos conectados**, selecione sua Machine e saia da conta.
