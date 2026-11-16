---
title: O app para celular
area: getting-started
summary: The Machine como app no iPhone e no Android: notificações das suas tarefas e compartilhamento de qualquer app com The Machine.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 0d4d41134db91fcc
---
O app para celular abre seu próprio painel, com a mesma sessão iniciada que na web. Baixe pela [App Store](https://apps.apple.com/app/id6829875215) para iPhone e iPad ou pelo [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

A tarefa **Aproveite mais a The Machine**, no topo de **Tarefas**, sugere que você instale o app. No navegador do celular, **Baixar** abre a loja. Em um celular configurado para mostrar sites para computador, aparecem os links das duas lojas. No computador, aparece um QR code para escanear com o celular e os links das duas lojas.

Em qualquer celular, [themachine.computer/app](https://themachine.computer/app) abre a loja certa. Em **Configurações**, **Apps**, os links das duas lojas aparecem no topo ou, no celular, só o link da loja correspondente. No computador, **Computador** instala o painel como app. Saiba mais em [Instalar o app](phone-app.md).

## Conectar

Em uma Machine hospedada, o app entra com sua conta. Em uma Machine auto-hospedada, abra **Configurações**, **Apps** no computador. Abaixo das lojas, **Não está na Network?** mostra um código. Instale o app e escaneie o código com a câmera do celular ou digite no app o endereço que aparece abaixo dele. O app pede sua confirmação antes de se conectar, e o login da sua própria Machine continua sendo necessário.

## Notificações

Quando abre pela primeira vez, o app pede permissão para enviar notificações. Toque em uma para abrir o conteúdo relacionado: uma tarefa aparece destacada na sua lista, a notificação da manhã abre o dia de hoje no **Calendário**, o resumo da equipe abre **Tarefas** e uma pergunta do Fleet abre a tarefa correspondente. Nenhum texto de uma tarefa passa pela Apple, pelo Google ou pelo serviço da The Machine. Eles só transmitem uma mensagem fixa, como “Uma tarefa precisa de você”.

Em seguida, o app pede à sua própria Machine o título da tarefa e a próxima etapa, por exemplo, “Responder ao Sam”, com “Enviar para Sam: terça-feira, às 10h, funciona”. A notificação da manhã mostra o que está pendente e o horário da sua primeira reunião; o resumo da equipe mostra os primeiros itens; uma atualização do Fleet mostra o que aconteceu. Se não conseguir se conectar à sua Machine, a mensagem fixa continua aparecendo. No Android, ela informa quantas tarefas estão pendentes, como “2 tarefas precisam de você”.

Uma notificação tem as opções **Adiar** (até amanhã) e **Marcar como feita**, além de **Fazer** para uma tarefa que ainda não foi iniciada. Elas funcionam depois que você desbloqueia o celular, sem abrir o app. O envio e as etapas finais sempre abrem o app. Há uma notificação por tarefa: “Preparando” muda para “Pronta” e ela desaparece quando a tarefa é feita ou adiada, no app ou em qualquer outro lugar.

Quando uma etapa que você confirmou é concluída, a notificação mostra **Feito** e o que aconteceu, até você tocar em **Entendi** em **Tarefas**. No iPhone, isso pode esperar até a próxima vez que você abrir o app.

Com **Texto nas notificações** desativado em **Configurações**, **Segurança**, a mensagem fixa continua aparecendo. O mesmo acontece quando a tela bloqueada oculta o conteúdo das notificações. Quando não há nada que ela possa mostrar, aparece “Toque para abrir”. Se o celular não conseguir se conectar à sua Machine quando uma notificação chegar, os detalhes aparecerão quando ele voltar a ficar online.

Elas seguem as mesmas regras das notificações push na web: o que você escolheu para cada tipo em [Notificações](notifications.md), seu [horário de trabalho](work-hours.md) e nenhuma notificação enquanto você estiver usando um painel.

Cada celular com o app aparece em **Configurações**, **Notificações**, como **Celular com o app**. **Remover** desativa as notificações desse celular. Uma Machine auto-hospedada precisa da The Machine Network para enviar notificações. O app funciona sem elas.

## Compartilhar com The Machine

Em qualquer app, toque em Compartilhar e escolha The Machine. Uma **Nova tarefa** é aberta com o texto, o link ou os arquivos que você compartilhou. Confira, adicione uma data se quiser e salve. Nada é adicionado antes disso.

Você também pode compartilhar apenas um arquivo, como uma fatura ou uma carta. Sua Machine lê o texto de um PDF e preenche a tarefa: o que é, a próxima etapa e a data. O arquivo vai direto para sua Machine e fica lá.

No Android, o painel instalado como app também recebe itens compartilhados. Basta escolhê-lo na folha de compartilhamento.

Os planos e a cobrança não aparecem no app. **Abrir conta** continua disponível em **Configurações** para você excluir sua conta.
