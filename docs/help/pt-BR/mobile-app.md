---
title: O app para celular
area: getting-started
summary: A The Machine como app no iPhone e Android: notificações das suas tarefas e compartilhamento com a The Machine de qualquer app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: f622bdc266f69965
---
O app para celular abre seu próprio painel, com a sessão iniciada como na versão web. Baixe-o na [App Store](https://apps.apple.com/app/id6829875215) para iPhone e iPad ou no [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

A tarefa **Aproveite mais a The Machine**, no topo da seção Tarefas, sugere que você baixe o app. No navegador do celular, **Baixar** abre a loja. Se o celular estiver configurado para exibir versões para computador, aparecem os links das duas lojas. No computador, aparece um código QR para escanear com o celular, além dos links das duas lojas.

Em qualquer celular, [themachine.computer/app](https://themachine.computer/app) abre a loja certa. Em **Configurações**, **Apps**, aparecem as duas lojas no topo ou apenas a loja do seu celular, se você estiver usando um celular. No computador, **Computador** instala o painel como app: consulte [Instalar o app](phone-app.md).

## Conectar o app

Em uma Machine hospedada, o app inicia a sessão com sua conta. Em uma Machine auto-hospedada, abra **Configurações**, **Apps** no computador. Abaixo das lojas, **Não está na Network?** mostra um código. Instale o app e escaneie o código com a câmera do celular ou digite no app o endereço que aparece abaixo dele. O app pede sua autorização antes de se conectar, e o login da sua Machine continua valendo.

Ao tocar em **Entrar com** um serviço em **Conexões** (Shortcut, Notion, Slack, Zoom e outros), aparece a tela de login do serviço no celular. Depois do login, você volta ao app, e a nova conexão aparece automaticamente em **Conexões**.

## Notificações

Na primeira vez que o app abre, ele pede permissão para enviar notificações. Toque em uma notificação para abrir o conteúdo relacionado: uma tarefa aparece destacada na sua lista, o resumo da manhã abre o **Calendário** de hoje, o resumo da equipe abre a seção Tarefas e uma pergunta do Fleet abre a tarefa correspondente. O texto de uma tarefa nunca passa pela Apple, pelo Google nem pelo serviço da The Machine. Eles só transmitem uma mensagem fixa, como "Uma tarefa precisa de você".

Em seguida, o app pede à sua Machine o título da tarefa e a próxima etapa, por exemplo, "Responder ao Sam" e "Enviar para Sam: terça-feira, às 10h, funciona". O resumo da manhã mostra o que está pendente e o horário da sua primeira reunião; o resumo da equipe mostra os primeiros itens; e uma atualização do Fleet mostra o que aconteceu. Se não conseguir se conectar à sua Machine, o app mantém a mensagem fixa. No Android, a mensagem informa quantas tarefas estão esperando, como "2 tarefas precisam de você".

Uma notificação tem as opções **Adiar** (até amanhã) e **Marcar como feita**, além de **Fazer** para uma tarefa que ainda não foi iniciada. Elas funcionam depois que você desbloqueia o celular, sem abrir o app. Para enviar algo e concluir etapas, é sempre necessário abrir o app. Há uma notificação por tarefa: "Preparando" muda para "Para revisar", e ela desaparece quando a tarefa é feita ou adiada, seja no app ou em outro lugar.

Quando uma etapa que você confirmou é concluída, a notificação mostra **Feito** e o que aconteceu, até você tocar em **Entendi** na seção Tarefas. No iPhone, ela pode ficar lá até você abrir o app novamente.

Se **Texto nas notificações** estiver desativado em **Configurações**, **Segurança**, a mensagem fixa continua aparecendo. O mesmo acontece quando a tela bloqueada oculta o conteúdo das notificações. Se não puder mostrar nada, aparece "Toque para abrir". Se o celular não conseguir se conectar à sua Machine quando uma notificação chegar, os detalhes aparecem assim que ele voltar a ficar online.

As notificações seguem as mesmas regras das notificações push na versão web: suas escolhas para cada tipo em [Notificações](notifications.md), seu [horário de trabalho](work-hours.md) e nenhuma notificação enquanto você estiver usando um painel.

Cada celular com o app aparece em **Configurações**, **Notificações** como **Celular com o app**. **Remover** interrompe as notificações desse celular. Para receber notificações em uma Machine auto-hospedada, é preciso ter a The Machine Network. O app funciona sem ela.

## Compartilhar com a The Machine

Em qualquer app, toque em Compartilhar e escolha The Machine. Uma **Nova tarefa** é aberta com o texto, o link ou os arquivos que você compartilhou. Confira, adicione uma data se quiser e salve. Nada é adicionado até você fazer isso.

Também basta compartilhar um arquivo, como uma fatura ou uma carta. Sua Machine lê o texto de um PDF e preenche a tarefa com o que é o documento, a próxima etapa e a data. O arquivo vai direto para sua Machine e fica lá.

No Android, também é possível compartilhar com o painel instalado como app. Basta escolhê-lo na folha de compartilhamento.

Os planos e as cobranças não aparecem no app. **Abrir conta**, em **Configurações**, continua disponível para excluir sua conta.
