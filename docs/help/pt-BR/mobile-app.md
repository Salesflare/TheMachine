---
title: O app para celular
area: getting-started
summary: A The Machine como app para iPhone e Android: notificações das suas tarefas e compartilhamento com a The Machine a partir de qualquer app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 672364a90f92ef8f
---
O app para celular abre seu próprio painel, com a mesma conta que você usa na web. Baixe-o na [App Store](https://apps.apple.com/app/id6829875215) para iPhone e iPad ou no [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

A tarefa **Aproveite mais a The Machine**, no topo de Tarefas, sugere que você baixe o app. No navegador do celular, **Baixar** abre a loja. Em um celular configurado para exibir sites para computador, aparecem os links das duas lojas. No computador, aparece um código QR para escanear com o celular, além dos links das duas lojas.

Em qualquer celular, [themachine.computer/app](https://themachine.computer/app) abre a loja certa. Em **Configurações**, **Apps** mostra as duas lojas no topo ou apenas a loja do seu celular, se você estiver no celular. No computador, **Computador** instala o painel como app: veja [Instalar o app](phone-app.md).

## Conecte o app

Em uma Machine hospedada, o app entra na sua conta. Em uma Machine auto-hospedada, abra **Configurações** e **Apps** em um computador. Abaixo das lojas, **Não está na Network?** mostra um código. Instale o app e escaneie o código com a câmera do celular ou digite no app o endereço que aparece abaixo dele. O app pede confirmação antes de se conectar, e o login da sua Machine continua sendo necessário.

Ao tocar em **Entrar com** um serviço em **Conexões** (Shortcut, Notion, Slack, Zoom e outros), a tela de login do serviço é aberta no celular. Quando terminar, você volta ao app e a nova conexão aparece em **Conexões** automaticamente.

Quando o app não consegue acessar sua Machine, ele avisa e tenta de novo automaticamente. Em um Mac ou iPad com teclado, Cmd+R carrega a página novamente.

## Notificações

Na primeira vez que abre, o app pede permissão para enviar notificações. Toque em uma delas para abrir o conteúdo: uma tarefa aparece destacada na sua lista, a notificação matinal abre o dia de hoje no **Calendário**, o resumo da equipe abre Tarefas e uma pergunta do Fleet abre a tarefa correspondente. O texto de uma tarefa não passa pela Apple, pelo Google nem pelo serviço da The Machine. Eles só transmitem uma mensagem fixa, como “Uma tarefa precisa de você”.

Em seguida, o app pede à sua Machine o título e a próxima etapa da tarefa, como “Responder ao Sam” e “Enviar para Sam: terça-feira, às 10h, funciona”. A notificação matinal inclui o que está pendente e o horário da sua primeira reunião; o resumo da equipe, os primeiros itens; e uma atualização do Fleet, o que aconteceu. Quando não consegue acessar sua Machine, o app mantém a mensagem fixa. No Android, ela informa quantas tarefas estão pendentes, como “2 tarefas precisam de você”.

Uma notificação tem as opções **Adiar** (até amanhã) e **Marcar como feita**, além de **Fazer** para uma tarefa que ainda não começou. Elas funcionam depois que você desbloqueia o celular, sem abrir o app. O envio e as etapas finais sempre abrem o app. Há uma notificação por tarefa: “Preparando” muda para “Pronta”, e ela desaparece quando a tarefa é concluída ou adiada, no app ou em qualquer outro lugar.

Quando uma etapa que você confirmou é concluída, a notificação mostra **Feito** e o que aconteceu, até você tocar em **Entendi** em Tarefas. No iPhone, você pode fazer isso na próxima vez que abrir o app.

Com **Texto nas notificações** desativado em **Configurações**, na seção **Segurança**, o app mantém a mensagem fixa. O mesmo acontece quando a tela bloqueada oculta o conteúdo das notificações. Quando não há nada que o app possa mostrar, aparece “Toque para abrir”. Se o celular não consegue acessar sua Machine quando uma notificação chega, os detalhes aparecem assim que ele volta a ficar online.

As notificações seguem as mesmas regras das notificações push na web: suas escolhas para cada tipo em [Notificações](notifications.md), seu [horário de trabalho](work-hours.md) e nenhuma notificação enquanto você usa um painel.

Cada celular com o app aparece em **Configurações**, **Notificações**, como **Celular com o app**. **Remover** interrompe as notificações nesse celular. Uma Machine auto-hospedada precisa ter acesso à The Machine Network para enviar notificações. O app funciona sem elas.

## Compartilhe com a The Machine

Em qualquer app, toque em Compartilhar e escolha a The Machine. Uma **Nova tarefa** abre com o texto, o link ou os arquivos que você compartilhou. Confira, adicione uma data se quiser e salve. Nada é adicionado até você fazer isso.

Você também pode compartilhar apenas um arquivo, como uma fatura ou uma carta. Sua Machine lê o texto de um PDF e preenche a tarefa com o que é, a próxima etapa e a data. O arquivo vai direto para sua Machine e fica lá.

O painel instalado como app no Android também recebe compartilhamentos: escolha-o na folha de compartilhamento da mesma forma.

Os planos e a cobrança não aparecem no app. **Abrir conta** continua disponível em **Configurações**, para você excluir sua conta.
