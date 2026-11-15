---
title: WhatsApp
area: connections
summary: Seus chats do WhatsApp, lidos como dispositivo conectado. As respostas só são enviadas depois da sua aprovação.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 4ceded6544e535eb
---
## O que ele lê

Seus chats do WhatsApp, como um dispositivo conectado ao WhatsApp do seu celular, igual ao WhatsApp no computador. Quando você conecta, o WhatsApp também envia seus chats antigos, muitas vezes de anos atrás. Sua Machine guarda tudo, mas só as mensagens dos últimos 7 dias viram tarefas.

Uma foto, mensagem de voz ou arquivo sem legenda aparece identificado, como "Foto", com o ícone correspondente. Os avisos do próprio WhatsApp, como o aviso sobre criptografia ou alguém entrando em um grupo, não têm texto e ficam de fora.

## Ler fotos

O recurso fica desativado até você ativá-lo. Em **Conexões**, abra o WhatsApp, depois **Detalhes**, e ative **Ler fotos**. A Machine lê as fotos nos seus chats de trabalho: um recibo, uma captura de tela, a foto de uma carta ou de um formulário. **Também em conversas pessoais** também lê as fotos dos seus chats pessoais. Um chat é considerado de trabalho ou pessoal conforme o compartilhamento, então um chat com a família continua sendo pessoal.

A Machine baixa cada foto uma vez e a mantém na sua Machine, como um anexo de e-mail: criptografada quando a proteção de mensagens está ativada e apagada quando a mensagem é removida. O modelo da própria Machine lê o que aparece na foto e o texto nela. Isso conta como parte da mensagem, nunca como instruções. JPEG, PNG e WebP de até 5 MB. Códigos de uso único em fotos ficam de fora.

A tarefa e a mensagem mostram a foto. Toque nela para vê-la ampliada.

## O que pode enviar

Uma mensagem de texto ou um arquivo com legenda opcional para um chat existente, só depois que você aprovar a tarefa. Antes do envio, a tarefa mostra o arquivo, e você pode abri-lo. O arquivo pode ter até 18 MB. Uma resposta à mensagem do WhatsApp que originou uma tarefa cita essa mensagem quando alguém falou mais depois dela ou quando ela está em um grupo; o rascunho mostra **Como resposta**.

Se uma tarefa chegou por e-mail, mas você conversa com essa pessoa pelo WhatsApp, diga isso no chat da tarefa. A Machine encontra seu chat existente com essa pessoa e muda o rascunho para WhatsApp, para você revisar e enviar. Ela nunca inicia um chat novo.

O WhatsApp não oferece uma forma oficial de fazer isso. Ler mensagens e enviar uma resposta ocasional que você aprovou dificilmente causará problemas. O envio em massa ou automatizado pode levar ao bloqueio da conta.

## Conectar

Em uma Machine hospedada:

1. No painel, abra **Conexões**, depois **Chat**, e escolha WhatsApp.
2. Pressione **Mostrar o código QR**.
3. No celular, abra o WhatsApp, vá para **Configurações**, **Aparelhos conectados**, **Conectar aparelho** e escaneie o código QR.
4. O WhatsApp aparecerá como conectado em até um minuto. Depois disso, o histórico dos seus chats continuará sendo carregado, e o cartão mostrará quantas mensagens foram carregadas.
   Se a conexão demorar demais, uma mensagem será exibida após alguns minutos. Pressione **Tentar de novo** para continuar de onde parou.

Está configurando pelo celular, sem uma segunda tela para escanear? Abra **No celular? Conecte com um código**, digite seu número e pressione **Pegar um código**. O WhatsApp pedirá esse código.

No seu próprio computador: abra **Conexões**, depois **Chat**, escolha WhatsApp, digite seu número de telefone com o código do país e pressione **Conectar**. Um código será exibido. No celular, abra o WhatsApp, vá para **Configurações**, **Aparelhos conectados**, **Conectar aparelho** e depois **Conectar com número de telefone**, e digite o código.

Ou execute `assistant connect whatsapp` e escaneie o código exibido no terminal. Na primeira vez, a opção de instalar o conector do WhatsApp será oferecida. É uma versão fixada e verificada pelo checksum ([código-fonte](https://github.com/Salesflare/wacli)).

Em Aparelhos conectados, ela aparece como The Machine. Uma Machine conectada anteriormente mantém o nome antigo nessa lista até você conectá-la novamente.

## Fotos de perfil

A Machine pede ao WhatsApp as fotos de perfil das pessoas no seu Graph que ainda não têm uma, até 50 por dia, por meio da sincronização que mantém o WhatsApp atualizado. Nada é enviado a essas pessoas. Quem oculta a foto de perfil de você continua sem foto.

## Remover

- Em uma Machine hospedada: pressione **Remover** ao lado dela na página de configuração. Sua Machine se desconecta e apaga o que guardou do WhatsApp.
- No seu próprio computador: abra **Conexões**, depois WhatsApp, **Detalhes** e **Desconectar**. Em seguida, desconecte também pelo celular.

## Desconectar no WhatsApp

No celular, abra o WhatsApp, vá para **Configurações**, **Aparelhos conectados**, toque na sua Machine e saia da conta.
