---
title: Instalar o app e ativar as notificações
area: getting-started
summary: Instale a The Machine no celular ou no computador e receba uma notificação para cada tarefa. O Telegram é opcional.
covers: phone-app
code: manifest.webmanifest, sw.js, dashboard.html
order: 3
---
O painel pode ser instalado como app no celular ou no computador. Depois ele envia uma notificação para cada tarefa, resultado e lembrete quando você não está no painel, dentro do seu [horário de trabalho](work-hours.md). Escolha o que ele envia em [Notificações](notifications.md).

Um aviso discreto no topo de Tarefas oferece as duas coisas, uma de cada vez: primeiro o app, depois as notificações. **Agora não** esconde o aviso por 14 dias, e um segundo **Agora não** para de mostrar naquele dispositivo. Os mesmos controles ficam em **Configurações**, **Geral**, **Este dispositivo**.

## No computador (Chrome ou Edge)

1. Abra seu painel e clique em **Instalar** nesse aviso, ou em **Instalar app** em Configurações.
2. A The Machine abre em uma janela própria. Fixe na barra de tarefas ou no Dock.
3. Clique em **Ativar** no próximo aviso e permita as notificações. Uma notificação de teste aparece na hora.

## No Mac (Safari)

1. Na barra de menus do Safari, escolha Arquivo e depois Adicionar ao Dock.
2. Abra a The Machine pelo Dock e clique em **Ativar**.

## No Firefox

O Firefox não instala como app. As notificações funcionam na aba: clique em **Ativar** nesse aviso, ou no sino ao lado de **Notificações** em Configurações.

## No iPhone ou iPad

1. Abra seu painel no Safari. É preciso ter o iOS 16.4 ou mais recente.
2. Toque em Compartilhar e depois em Adicionar à Tela de Início.
3. Abra a The Machine pela Tela de Início e toque em **Ativar**.

As notificações só funcionam no app da Tela de Início, não em uma aba do Safari.

## No Android

1. Abra seu painel no Chrome e toque em **Instalar** nesse aviso, ou abra o menu e toque em Instalar app.
2. Abra pela tela inicial e toque em **Ativar**.

## Conferir ou mudar

Em **Configurações**, **Geral**, **Este dispositivo**, o sino ao lado de **Notificações** ativa ou desativa as notificações só naquele dispositivo, e **Enviar um teste** envia uma para ele.

Se as notificações estiverem bloqueadas, a linha diz onde permitir de novo: no computador, clique no ícone à esquerda do endereço e permita Notificações. No iPhone, abra o app Ajustes, Notificações, The Machine.

## Abrir rápido

O app abre na hora com suas últimas tarefas e depois as atualiza. Sem conexão, ele mostra o que tinha, marcado como **Offline** com o horário da última atualização. Essa cópia fica no dispositivo por no máximo 7 dias, criptografada, e é apagada quando você sai.

## Offline e wi-fi instável

No avião ou no trem, o painel continua funcionando. Uma barra no topo diz **Offline** e quando o que você vê foi atualizado pela última vez. Suas tarefas, os chats delas, o Calendário e as listas do Graph abrem a partir do dispositivo.

- **Adiar**, **Não precisa**, **Marcar como feita**, **Reabrir** e notas ou mensagens de chat para a The Machine esperam no dispositivo. A tarefa diz que será salvo quando você voltar a ficar online, com **Cancelar** até lá. Assim que sua Machine responde de novo, eles vão sozinhos, em ordem, uma vez cada.
- Mensagens para outras pessoas nunca esperam. **Enviar** diz que você está offline: envie de novo quando voltar.
- O que você digita em um chat fica no dispositivo até você enviar, mesmo depois de recarregar.
- O app tenta de novo sozinho, um pouco mais tarde a cada vez. **Tentar agora** tenta na hora.

## Mais dispositivos

Entre em cada dispositivo do mesmo jeito. Em uma Machine hospedada, uma chave de acesso por dispositivo deixa o login mais rápido: adicione uma em Segurança, na página da sua conta.

Para ler as notificações do seu celular Android como fonte, veja [Notificações do Android](android.md).
