---
title: Instale o app e ative as notificações
area: getting-started
summary: Instale The Machine no celular ou computador e receba uma notificação para cada tarefa. O Telegram é opcional.
covers: phone-app
code: manifest.webmanifest, sw.js, dashboard.html
order: 3
translated: 3c10a121b1cfb06d
---
Instale The Machine como um app no celular ou computador para receber uma notificação para cada tarefa, resultado e lembrete, dentro do seu [horário de trabalho](work-hours.md). Escolha o que ela envia em [Notificações](notifications.md).

A tarefa **Aproveite mais a The Machine**, no topo da lista de tarefas, tem uma linha para cada opção: **Baixe o app para celular** (veja [O app para celular](mobile-app.md)), **Ativar notificações** e **Instalar neste computador**. Só aparecem as opções que ainda faltam naquele dispositivo. O × em uma linha fecha essa opção. Os mesmos controles ficam em **Configurações**, **Geral**, **Este dispositivo**.

No app para celular, **Receba um aviso quando algo precisar de você.** aparece enquanto as notificações estão desativadas. **Ativar** pede autorização ao celular ou abre as configurações dele. **×** oculta o aviso por 7 dias.

## No computador (Chrome ou Edge)

1. Abra o painel e clique em **Instalar** na linha correspondente dessa tarefa, em **Instalar app** nas **Configurações**, **Geral**, ou em **Instalar** ao lado de **Computador** em **Configurações**, **Apps**.
2. The Machine abre em uma janela própria. Fixe-a na barra de tarefas ou no Dock.
3. Clique em **Ativar** na linha correspondente e permita as notificações. Uma notificação de teste aparece na hora.

## No Mac (Safari)

1. Na barra de menus do Safari, escolha Arquivo e depois Adicionar ao Dock.
2. Abra The Machine pelo Dock e clique em **Ativar**.

## No Firefox

O Firefox não permite instalar o app. As notificações funcionam na aba: clique em **Ativar** na linha correspondente ou no sino ao lado de **Notificações** em **Configurações**.

## No iPhone ou iPad

1. Abra o painel no Safari. É necessário ter o iOS 16.4 ou posterior.
2. Toque em Compartilhar e depois em Adicionar à Tela de Início.
3. Abra The Machine pela Tela de Início e toque em **Ativar**.

As notificações só funcionam no app aberto pela Tela de Início, não em uma aba do Safari.

## No Android

1. Abra o painel no Chrome, abra o menu e toque em **Instalar app**.
2. Abra o app pela tela inicial e toque em **Ativar**.

## Confira ou altere

Em **Configurações**, **Geral**, **Este dispositivo**, o sino ao lado de **Notificações** ativa ou desativa as notificações apenas nesse dispositivo. **Enviar um teste** envia uma notificação para ele.

As notificações estão bloqueadas? No computador, clique no ícone à esquerda do endereço e permita as notificações. No iPhone, abra o app Ajustes e toque em Notificações, The Machine.

## Abertura rápida

O app abre mostrando suas tarefas mais recentes e depois as atualiza. Essa cópia fica no dispositivo, criptografada, por no máximo 7 dias, e é removida quando você sai da conta.

## Sem conexão ou com Wi-Fi instável

O painel continua funcionando no avião ou no trem. Uma barra no topo mostra **Sem conexão** e quando o que você está vendo foi atualizado pela última vez. Suas tarefas, os chats delas, o Calendário e as listas do Graph abrem pelo dispositivo.

- **Adiar**, **Não precisa**, **Marcar como feita**, **Reabrir** e as mensagens de chat para a The Machine ficam na fila no dispositivo, com a opção **Cancelar**. Elas são enviadas automaticamente quando você volta a ficar online.
- As mensagens para outras pessoas não ficam na fila: envie de novo quando voltar a ficar online.
- O que você digitar em um chat fica no dispositivo até enviar, mesmo se recarregar a página.
- O app continua tentando se conectar. **Tentar agora** faz uma nova tentativa na hora.
- Uma Machine sua é acessada pelo Tailscale, e o celular pode desativar o Tailscale em segundo plano. Se não for possível acessar sua Machine dessa forma, a barra mostra **O Tailscale pode estar desativado neste dispositivo**. No celular, **Abrir Tailscale** abre o app ou a página da loja para você ativá-lo novamente.
- Uma Machine ocupada pode demorar para responder. Nesse caso, o app mostra **Sua Machine está demorando para responder** e mantém o que você está vendo. Isso não significa que está sem conexão.

## Mais dispositivos

Entre em cada dispositivo da mesma forma. Em uma Machine hospedada, uma passkey por dispositivo agiliza o login: em **Configurações** › **Conta**, toque em **Gerenciar** ao lado de **Login**.

Para ler as notificações do seu celular Android como uma fonte, veja [Notificações do Android](android.md).
