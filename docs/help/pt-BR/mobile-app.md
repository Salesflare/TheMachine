---
title: O app para celular
area: getting-started
summary: Use a The Machine como app no iPhone e no Android: receba notificações das suas tarefas e compartilhe conteúdo de qualquer app com a The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: aaf34f864dadf180
---
O app para celular abre seu painel, com a mesma conta que você usa na versão web. Baixe-o na [App Store](https://apps.apple.com/app/id6829875215) para iPhone e iPad ou no [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

A tarefa **Aproveite mais a The Machine**, no topo da lista de tarefas, recomenda o app. No navegador do celular, **Baixar** abre a loja. Se o celular estiver configurado para mostrar sites para computador, o app exibe os links das duas lojas. No computador, ele mostra um QR code para escanear com o celular e links para as duas lojas.

Em qualquer celular, [themachine.computer/app](https://themachine.computer/app) abre a loja certa. Em **Configurações**, **Apps**, os links das duas lojas aparecem no topo. No celular, aparece apenas o link da loja correspondente. No computador, também aparece o app para Windows, Mac e Linux. Saiba mais em [O app para computador](desktop-app.md).

## Conectar o app

Em uma Machine hospedada, o app entra na sua conta. Em uma Machine hospedada por você, abra **Configurações** e **Apps** no computador. Abaixo dos links das lojas, **Não está na Network?** mostra um código. Instale o app e escaneie o código com a câmera do celular ou digite no app o endereço que aparece abaixo dele. O app pede sua confirmação antes de se conectar, e você ainda precisa entrar na sua Machine.

Ao tocar em **Entrar com** um serviço em **Conexões** (Shortcut, Notion, Slack, Zoom e outros), abre-se a tela de login do serviço no celular. Quando terminar, você volta ao app, e a nova conexão aparece automaticamente em **Conexões**.

Se o app não conseguir acessar sua Machine, ele avisa e tenta de novo automaticamente. No Mac, o app também reabre a página automaticamente se a janela voltar em branco depois de sair do repouso. A mensagem que você estava escrevendo no chat também volta. No Mac ou no iPad com teclado, pressione Cmd+R para carregar a página novamente.

## Notificações

Na primeira vez que abre, o app pede permissão para enviar notificações. Toque em uma notificação para abrir o conteúdo: uma tarefa aparece destacada na sua lista, a notificação da manhã abre o dia de hoje no **Calendário**, o resumo da equipe abre as tarefas e uma pergunta do Fleet abre a tarefa correspondente. O texto de uma tarefa não passa pelos serviços da Apple, do Google ou da The Machine. Eles só transmitem uma mensagem fixa, como "Uma tarefa precisa de você".

Em seguida, o app pede à sua Machine o título e a próxima etapa da tarefa, como "Responder ao Sam" e "Enviar ao Sam: terça-feira, às 10h funciona". A notificação da manhã mostra o que está pendente e o horário da sua primeira reunião. O resumo da equipe mostra os primeiros itens, e uma atualização do Fleet mostra o que aconteceu. Se o app não conseguir acessar sua Machine, a mensagem fixa permanece. No Android, a notificação informa quantas tarefas estão pendentes, como "2 tarefas precisam de você".

Uma notificação tem as opções **Adiar** (até amanhã) e **Marcar como feito**, além de **Fazer** para uma tarefa que ainda não começou. Elas funcionam depois que você desbloqueia o celular, sem abrir o app. O envio e as etapas finais sempre abrem o app. Cada tarefa tem uma notificação: "Preparando" muda para "Pronta", e a notificação desaparece quando a tarefa é concluída ou adiada, no app ou em outro lugar.

Quando uma etapa que você confirmou é concluída, a notificação mostra **Feito** e o que aconteceu, até você tocar em **Entendi** na lista de tarefas. No iPhone, você pode fazer isso na próxima vez que abrir o app.

Com **Texto nas notificações** desativado em **Configurações**, **Segurança**, a mensagem fixa continua aparecendo. O mesmo acontece quando a tela bloqueada oculta o conteúdo das notificações. Quando não há nada que possa ser exibido, aparece "Toque para abrir". Se o celular não conseguir acessar sua Machine quando uma notificação chegar, os detalhes aparecem assim que a conexão voltar.

As notificações seguem as mesmas regras das notificações push na web: as opções que você escolheu para cada tipo em [Notificações](notifications.md), seu [horário de trabalho](work-hours.md) e nenhuma notificação enquanto você estiver usando um painel.

Cada celular com o app aparece em **Configurações**, **Notificações**, como **Celular com o app**. **Remover** desativa as notificações nesse celular. Para receber notificações em uma Machine hospedada por você, é preciso usar a The Machine Network. O app funciona sem elas.

## Compartilhar com a The Machine

Em qualquer app, toque em Compartilhar e escolha The Machine. Uma **Nova tarefa** abre com o texto, o link ou os arquivos que você compartilhou. Confira o conteúdo, adicione uma data se quiser e crie a tarefa. Nada é adicionado sem a sua confirmação.

Você também pode compartilhar só um arquivo, como uma fatura ou uma carta. Sua Machine lê o texto de um PDF e preenche a tarefa com o que é o arquivo, a próxima etapa e a data. O arquivo vai direto para sua Machine e fica lá.

O painel instalado como app no Android também recebe itens compartilhados. Basta escolhê-lo na tela de compartilhamento.

Os planos e as cobranças não aparecem no app. **Abrir conta** continua disponível em **Configurações** para excluir sua conta.
