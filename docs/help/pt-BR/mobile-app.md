---
title: O app para celular
area: getting-started
summary: Use The Machine como app no iPhone e no Android: receba notificações das suas tarefas e compartilhe conteúdo com The Machine de qualquer app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 3865fe910a5427fb
---
O app para celular abre seu próprio painel, com a mesma conta que você usa na web. Baixe pela [App Store](https://apps.apple.com/app/id6829875215) para iPhone e iPad ou pelo [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

A tarefa **Aproveite mais a The Machine**, no topo de Tarefas, sugere o app. No navegador do celular, **Baixar** abre a loja. Se o celular estiver configurado para mostrar sites para computador, o app mostra os links das duas lojas. No computador, ele mostra um código QR para escanear com o celular e links para as duas lojas.

Em qualquer celular, [themachine.computer/app](https://themachine.computer/app) abre a loja certa. Em **Configurações**, **Apps**, você encontra as duas lojas no topo ou, se estiver no celular, apenas a loja do seu aparelho. No computador, **Computador** instala o painel como app: veja [Instalar o app](phone-app.md).

## Conectar

Em uma Machine hospedada, o app entra com sua conta. Se você hospeda sua Machine, abra **Configurações**, **Apps** em um computador. Abaixo das lojas, **Não está na Network?** mostra um código. Instale o app e escaneie o código com a câmera do celular ou digite no app o endereço que aparece abaixo dele. O app pede sua autorização antes de se conectar, e você ainda precisa entrar na sua Machine.

## Notificações

Quando o app abre pela primeira vez, ele pede permissão para enviar notificações. Toque em uma notificação para abrir o conteúdo relacionado: uma tarefa abre o chat dela, a notificação da manhã abre o dia de hoje no **Calendário**, o resumo da equipe abre Tarefas e uma pergunta do Fleet abre a tarefa correspondente. Nenhum texto de uma tarefa passa pelos serviços da Apple, do Google ou da The Machine. Eles só transmitem uma frase fixa, como "Uma tarefa precisa de você".

O app então pede à sua Machine o título da tarefa e a próxima etapa, como "Responder para Sam", com "Enviar para Sam: terça-feira às 10h funciona". A notificação da manhã inclui o que está pendente e o horário da sua primeira reunião; o resumo da equipe, os primeiros itens; e uma atualização do Fleet, o que aconteceu. Se não conseguir se conectar à sua Machine, o app mantém a frase fixa. No Android, a notificação informa quantas tarefas estão pendentes, como "2 tarefas precisam de você".

Uma notificação tem as opções **Adiar** (até amanhã) e **Marcar como feita**, além de **Fazer** para uma tarefa que ainda não começou. Elas funcionam depois que você desbloqueia o celular, sem abrir o app. O envio e as etapas finais sempre abrem o app. Cada tarefa tem uma notificação: "Preparando" muda para "Pronta", e a notificação desaparece quando a tarefa é feita ou adiada, no app ou em outro lugar.

Quando uma etapa que você confirmou é concluída, a notificação mostra **Feito** e o que aconteceu, até você tocar em **Entendi** em Tarefas. No iPhone, você pode esperar até abrir o app novamente.

Se você desativar **Texto nas notificações** em **Configurações**, **Segurança**, o app mantém a frase fixa. O mesmo acontece se a tela bloqueada ocultar o conteúdo das notificações. Quando não houver nada que ela possa mostrar, a notificação diz "Toque para abrir". Se o celular não conseguir se conectar à sua Machine quando uma notificação chegar, os detalhes aparecem assim que ele voltar a ficar online.

As notificações seguem as mesmas regras das notificações push na web: o que você escolheu para cada tipo em [Notificações](notifications.md), seu [horário de trabalho](work-hours.md) e nenhuma notificação enquanto você estiver usando um painel.

Cada celular com o app aparece em **Configurações**, **Notificações**, como **Celular com o app**. **Remover** desativa as notificações nesse celular. Para receber notificações em uma Machine hospedada por você, é preciso usar a The Machine Network. O app funciona sem ela.

## Compartilhar com The Machine

Em qualquer app, toque em Compartilhar e escolha The Machine. Uma **Nova tarefa** será aberta com o texto, o link ou os arquivos que você compartilhou. Confira, adicione uma data se quiser e salve. Nada será adicionado até você fazer isso.

Você também pode compartilhar só um arquivo, como uma fatura ou uma carta. Sua Machine lê o texto de um PDF e preenche a tarefa com o que é o arquivo, a próxima etapa e a data. O arquivo vai direto para sua Machine e fica lá.

No Android, você também pode compartilhar conteúdo com o painel instalado como app: escolha-o na lista de compartilhamento, como faria com qualquer outro app.

Os planos e a cobrança não aparecem no app. **Abrir conta**, em **Configurações**, continua disponível para excluir sua conta.
