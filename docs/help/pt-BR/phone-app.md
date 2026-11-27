---
title: Instale o app e ative as notificações
area: getting-started
summary: Instale a The Machine no celular ou computador e receba uma notificação para cada tarefa. O Telegram é opcional.
covers: phone-app
code: manifest.webmanifest, sw.js, dashboard.html
order: 3
translated: c1ead6181c38a6d8
---
Instale a The Machine como app no celular ou computador para receber uma notificação para cada tarefa, resultado e lembrete durante seu [horário de trabalho](work-hours.md). Escolha o que ela envia em [Notificações](notifications.md).

A tarefa **Aproveite mais a The Machine**, no topo de Tarefas, tem uma opção para cada ação: **Baixe o app para celular** (consulte [O app para celular](mobile-app.md)), **Baixar o app para computador** (consulte [O app para computador](desktop-app.md)), **Ativar notificações** e **Instalar neste computador**. Só aparecem as opções que ainda faltam naquele dispositivo. Clique no × de uma opção para fechá-la. Os mesmos controles ficam em **Configurações**, **Geral**, **Este dispositivo**.

**Instalar neste computador** só aparece em computadores sem o app para computador, como um Chromebook.

No app para celular, a mensagem **Receba um aviso quando algo precisar de você.** aparece enquanto as notificações estão desativadas. **Ativar** solicita permissão ao celular ou abre as configurações dele. **×** oculta a mensagem por 7 dias.

## No computador (Chrome ou Edge)

1. Abra o painel e clique em **Instalar app** em Configurações, **Geral**, **Este dispositivo**, ou em **Instalar** na opção da tarefa em um Chromebook.
2. A The Machine abre em uma janela própria. Fixe-a na barra de tarefas ou no Dock.
3. Clique em **Ativar** na opção e permita as notificações. Uma notificação de teste aparece na hora.

## No Mac (Safari)

1. Na barra de menus do Safari, escolha Arquivo e depois Adicionar ao Dock.
2. Abra a The Machine pelo Dock e clique em **Ativar**.

## No Firefox

Não é possível instalar o app no Firefox. As notificações funcionam na aba: clique em **Ativar** na opção ou no sino ao lado de **Notificações** em Configurações.

## No iPhone ou iPad

1. Abra o painel no Safari. É necessário ter o iOS 16.4 ou uma versão mais recente.
2. Toque em Compartilhar e depois em Adicionar à Tela de Início.
3. Abra a The Machine pela Tela de Início e toque em **Ativar**.

As notificações só funcionam pelo app na Tela de Início, não em uma aba do Safari.

## No Android

1. Abra o painel no Chrome, abra o menu e toque em **Instalar app**.
2. Abra o app pela tela inicial e toque em **Ativar**.

## Conferir ou alterar

Em **Configurações**, **Geral**, **Este dispositivo**, o sino ao lado de **Notificações** ativa ou desativa as notificações apenas nesse dispositivo. **Enviar um teste** envia uma notificação para ele.

As notificações estão bloqueadas? No computador, clique no ícone à esquerda do endereço e permita as notificações. No iPhone, abra o app Ajustes e toque em Notificações, The Machine.

## Abrir mais rápido

O app abre na hora com suas tarefas mais recentes e depois as atualiza. Essa cópia fica no dispositivo, criptografada, por no máximo 7 dias, e é apagada quando você sai da conta.

## Sem internet ou com Wi-Fi instável

O painel continua funcionando no avião ou no trem. Uma barra no topo mostra **Sem conexão** e quando as informações exibidas foram atualizadas pela última vez. Suas tarefas, os chats delas, o Calendário e as listas do Graph abrem pelo dispositivo.

- **Adiar**, **Não precisa**, **Marcar como feita**, **Reabrir** e as mensagens de chat para a The Machine ficam no dispositivo, com a opção **Cancelar**. Elas são enviadas automaticamente quando você volta a ficar on-line.
- As mensagens para outras pessoas não ficam na fila. Envie-as de novo quando voltar a ficar on-line.
- O que você digita em um chat fica no dispositivo até ser enviado, mesmo que a página seja recarregada.
- O app tenta se reconectar automaticamente. **Tentar agora** faz uma nova tentativa na hora.
- Sua Machine é acessada pela Tailscale, e um celular pode desativar a Tailscale em segundo plano. Quando não for possível acessar sua Machine dessa forma, a barra mostra **A Tailscale pode estar desativada neste dispositivo**. No celular, **Abrir Tailscale** abre o app ou a página dele na loja para você ativá-lo novamente.
- Uma Machine ocupada pode demorar para responder. Nesse caso, o app mostra **Sua Machine está demorando para responder** e mantém as informações exibidas. Isso não significa que você está sem conexão.

## Mais dispositivos

Entre na sua conta em cada dispositivo da mesma forma. Em uma Machine hospedada, uma chave de acesso por dispositivo agiliza o login. Acesse **Configurações** › **Conta** e clique em **Gerenciar**, ao lado de Login.

Para usar as notificações do seu celular Android como fonte, consulte [Notificações do Android](android.md).
