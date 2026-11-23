---
title: O app para celular
area: getting-started
summary: Use a The Machine como app no iPhone e no Android: receba notificações das suas tarefas e compartilhe conteúdo de qualquer app com a The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 927fa395fe97f565
---
O app para celular abre seu próprio painel, com a mesma conta que você usa na web. Baixe pela [App Store](https://apps.apple.com/app/id6829875215) para iPhone e iPad ou pelo [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

A tarefa **Aproveite mais a The Machine**, no topo de Tarefas, sugere que você baixe o app. No navegador do celular, **Baixar** abre a loja. Se o celular estiver configurado para mostrar sites para computador, o app mostra os links das duas lojas. No computador, ele mostra um QR code para escanear com o celular e os links das duas lojas.

Em qualquer celular, [themachine.computer/app](https://themachine.computer/app) abre a loja certa. Em **Configurações**, **Apps**, você encontra as duas lojas no topo ou apenas a loja do seu celular, se estiver usando um celular. No computador, **Computador** instala o painel como app. Veja [Instalar o app](phone-app.md).

## Conectar

Em uma Machine hospedada, o app entra com a sua conta. Em uma Machine hospedada por você, abra **Configurações**, **Apps** no computador. Abaixo das lojas, **Não está na Network?** mostra um código. Instale o app e escaneie o código com a câmera do celular ou digite no app o endereço que aparece abaixo dele. O app pede sua confirmação antes de se conectar, e o login da sua Machine continua valendo.

Ao tocar em **Entrar com** um serviço em **Conexões** (Shortcut, Notion, Slack, Zoom e outros), a tela de login do serviço abre no celular. Quando terminar, você volta ao app, e a nova conexão aparece automaticamente em **Conexões**.

Quando o app não consegue acessar sua Machine, ele avisa e tenta de novo automaticamente. No Mac, o app também abre a página de novo automaticamente quando a janela volta em branco depois de sair do modo de repouso. A mensagem de chat que você estava escrevendo também volta. No Mac ou no iPad com teclado, Cmd+R carrega a página de novo.

## Notificações

Na primeira vez que abre, o app pede permissão para enviar notificações. Toque em uma notificação para abrir o conteúdo correspondente: uma tarefa aparece destacada na sua lista, a notificação da manhã abre o dia de hoje no **Calendário**, o resumo da equipe abre Tarefas e uma pergunta do Fleet abre a tarefa correspondente. Nenhum texto de tarefa passa pela Apple, pelo Google ou pelo serviço da The Machine. Eles só transmitem uma mensagem fixa, como "Uma tarefa precisa de você".

O app pede então à sua própria Machine o título e a próxima etapa da tarefa, como "Responder ao Sam" e "Envie ao Sam: terça-feira, às 10h funciona". A notificação da manhã mostra o que está pendente e o horário da sua primeira reunião; o resumo da equipe mostra os primeiros itens; e uma atualização do Fleet mostra o que aconteceu. Se o app não consegue acessar sua Machine, a mensagem fixa continua aparecendo. No Android, a notificação informa quantas tarefas estão pendentes, como "2 tarefas precisam de você".

A notificação tem as opções **Adiar** (até amanhã) e **Marcar como feito**, além de **Fazer** para uma tarefa que ainda não começou. Elas funcionam depois que você desbloqueia o celular, sem precisar abrir o app. Para enviar algo ou concluir etapas, é sempre preciso abrir o app. Cada tarefa tem uma notificação: "Preparando" muda para "Para revisar" e ela desaparece quando a tarefa é concluída ou adiada, no app ou em outro lugar.

Quando uma etapa que você confirmou é concluída, a notificação mostra **Feito** e o que aconteceu, até você tocar em **Entendi** em Tarefas. No iPhone, isso pode esperar até a próxima vez que você abrir o app.

Com **Texto nas notificações** desativado em **Configurações**, **Segurança**, o app mantém a mensagem fixa. O mesmo acontece quando a tela bloqueada oculta o conteúdo das notificações. Quando não há nada que possa mostrar, aparece "Toque para abrir". Se o celular não consegue acessar sua Machine quando uma notificação chega, ele mostra os detalhes assim que volta a ficar online.

As notificações seguem as mesmas regras das notificações push na web: o que você escolheu para cada tipo em [Notificações](notifications.md), seu [horário de trabalho](work-hours.md) e nenhuma notificação enquanto você estiver usando um painel.

Cada celular com o app aparece em **Configurações**, **Notificações**, como **Celular com o app**. **Remover** desativa as notificações nesse celular. Uma Machine hospedada por você precisa da The Machine Network para enviar notificações. O app funciona sem elas.

## Compartilhar com a The Machine

Em qualquer app, toque em Compartilhar e escolha The Machine. Uma **Nova tarefa** abre com o texto, o link ou os arquivos que você compartilhou. Confira, adicione uma data se quiser e inclua a tarefa. Nada é adicionado sem a sua confirmação.

Você também pode compartilhar apenas um arquivo, como uma fatura ou uma carta. Sua Machine lê o texto de um PDF e preenche a tarefa: o que é, a próxima etapa e a data. O arquivo vai direto para sua Machine e fica lá.

No Android, você também pode compartilhar conteúdo com o painel instalado como app. Basta escolher o painel na lista de compartilhamento.

Os planos e a cobrança não aparecem no app. **Abrir conta** em **Configurações** continua disponível para excluir sua conta.
