---
title: Microsoft Outlook e Calendar
area: connections
summary: E-mails e reuniões do Outlook para Microsoft 365 e Outlook.com. Só envia um e-mail depois da sua aprovação.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 7229063d9365735d
---
## O que ela lê

- **Outlook**: todos os seus e-mails, os dos últimos 7 dias quando você conecta e, depois, tudo que chegar.
- **Outlook Calendar**: suas reuniões, apenas para leitura.

Os e-mails em Outros e as newsletters recebem uma rápida conferida primeiro: remetente, assunto e algumas palavras. Quando algo é importante, a mensagem é lida por inteiro e pode virar uma tarefa.

## O que ela pode enviar e alterar

- Um e-mail criado a partir de uma tarefa, só depois da sua aprovação. Ele é enviado pelo endereço da própria caixa de correio, não por um alias.
- Uma resposta vai para a conversa no Outlook do e-mail ao qual ela responde.
- Depois que uma resposta é enviada, as mensagens da conversa vão para uma pasta de mensagens adiadas no Outlook por alguns dias (3, a menos que a tarefa diga outra coisa) e voltam para a Caixa de Entrada depois desse período, ou antes se alguém responder. Elas nunca ficam fora da Caixa de Entrada depois do prazo da tarefa. A revisão informa isso antes do envio.

O calendário nunca é alterado.

## Fotos de colegas e contatos

A Microsoft também recebe uma solicitação para ler os perfis básicos das pessoas da sua organização (nome, e-mail e foto) e seus contatos do Outlook. Sua Machine usa essas informações apenas para mostrar fotos, cargos e empresas de pessoas que já estão no seu Graph, até 200 fotos por dia. Uma pessoa sem foto é verificada novamente após 30 dias.

Talvez o administrador da sua organização precise aprovar as fotos dos colegas. Se isso não acontecer, o Outlook ainda será conectado, mas sem essas fotos. Uma conta conectada antes disso recebe uma tarefa: pressione **Reconectar** ou **Não precisa** para encerrá-la de vez. Uma conta pessoal (Outlook.com, Hotmail) não tem colegas, então a tarefa pede apenas as fotos dos contatos.

## Conectar

Em uma Machine hospedada:

1. Acesse sua página de configuração em app.themachine.computer/setup.
2. Pressione **Conectar Microsoft** e entre na sua conta.
3. Se a Microsoft pedir aprovação do administrador, envie o link ao administrador do Microsoft 365 (**Copiar link**). Depois que ele aprovar, todas as pessoas da sua organização poderão conectar. Se você for o administrador, pressione **Sou administrador: aprovar agora**.

Ou, no painel: **Conexões**, **E-mail**, escolha Outlook e pressione **Entrar com a Microsoft**. O link para o administrador fica logo abaixo do botão.

No seu próprio computador, depois que ela estiver [conectada à sua conta](friends.md#a-machine-on-your-own-computer): abra **Conexões**, depois **E-mail**, escolha Outlook e pressione **Entrar com a Microsoft**. O e-mail e o calendário são conectados juntos. Depois de concluir o processo na Microsoft, você voltará a **Conexões** no painel.

Para equipes de TI que usam o próprio app do Microsoft Entra: abra **Usar seu próprio app** ali ou execute `assistant connect outlook`.

## Remover

- Em uma Machine hospedada: pressione **Desconectar** ao lado da conta na sua página de configuração. **Desconectar ↗** em Conexões leva você até lá.
- No seu próprio computador: **Conexões**, abra a conta, **Detalhes** e **Desconectar**.

## Desinstalar na Microsoft

A Microsoft não permite que a gente revogue uma autorização de acesso, então remova o acesso por lá também:

- Conta corporativa ou escolar: myapps.microsoft.com
- Conta pessoal: account.live.com/consent/Manage
