---
title: WhatsApp
area: connections
summary: Suas conversas do WhatsApp, lidas como um dispositivo conectado. Só responde depois que você aprova.
covers: connector:whatsapp
code: onboarding.py, next_actions.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## O que ele lê

Suas conversas do WhatsApp, como um dispositivo conectado ao WhatsApp do seu celular, igual ao WhatsApp no computador. Quando você conecta, ele lê os últimos 7 dias.

Uma foto, mensagem de voz ou arquivo sem legenda aparece pelo que é, como "Imagem enviada". Os avisos do próprio WhatsApp, como o aviso de criptografia ou alguém entrando em um grupo, não têm texto e ficam de fora.

## O que ele pode enviar

Um texto em uma conversa que já existe, só depois que você aprova na tarefa.

Se uma tarefa chegou por e-mail, mas você fala com essa pessoa pelo WhatsApp, diga isso no chat da tarefa. A The Machine encontra a conversa que você já tem com ela e passa o rascunho para o WhatsApp, para você revisar e enviar. Ela nunca começa uma conversa nova.

## Conectar

Em uma Machine hospedada:

1. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha WhatsApp.
2. Toque em **Mostrar o QR code**.
3. No seu celular, no WhatsApp, abra Configurações, Dispositivos conectados, Conectar um dispositivo, e escaneie o QR code.

Configurando pelo celular, sem uma segunda tela para escanear? Abra **No celular? Conecte com um código**, digite seu número e toque em **Receber um código**. O WhatsApp então pede esse código.

No seu próprio computador, rode `assistant connect whatsapp` e escaneie o código que aparece no terminal. Sem o wacli, ele oferece para instalar a versão fixada de [Salesflare/wacli](https://github.com/Salesflare/wacli), verificada pelo checksum.

## Fotos

A The Machine pede ao WhatsApp as fotos de perfil das pessoas no seu Graph que não têm foto, no máximo 50 por dia, pela sincronização que mantém o WhatsApp atualizado. Nada é enviado a elas. Quem esconde a foto de você continua sem foto.

## Remover

- Em uma Machine hospedada: toque em **Remover** ao lado dele na sua página de configuração. Seu servidor se desconecta e exclui o que guardou do WhatsApp.
- No seu próprio computador: **Conexões**, abra WhatsApp, **Detalhes** e depois **Desconectar**. Depois desconecte no seu celular também.

## Desconectar no WhatsApp

No seu celular, no WhatsApp, abra Configurações, Dispositivos conectados, toque na sua Machine e saia.
