---
title: Microsoft Outlook e Calendar
area: connections
summary: E-mails e reuniões do Outlook, para Microsoft 365 e Outlook.com. Um e-mail só é enviado depois que você aprova.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: c10bf70a327b8ec0
---
## O que ela lê

- **Outlook**: todos os seus e-mails dos últimos 7 dias quando você conecta a conta e, depois, todos os novos.
- **Outlook Calendar**: suas reuniões, somente para leitura.

E-mails em Outros e newsletters recebem uma análise rápida primeiro: remetente, assunto e algumas palavras. Quando algum é importante, ele é lido por inteiro e pode virar uma tarefa.

## O que ela pode enviar e alterar

- Um e-mail de uma tarefa, somente depois que você aprovar. Ele é enviado pelo endereço da própria caixa de entrada, não por um alias.
- Uma resposta vai para a conversa do Outlook do e-mail respondido.
- Depois que uma resposta é enviada, as mensagens da conversa vão para uma pasta de mensagens adiadas no Outlook por alguns dias (3, a menos que a tarefa diga outra coisa) e voltam para a Caixa de entrada nesse período, ou antes se alguém responder. A revisão informa isso antes do envio.

O calendário nunca é alterado.

## Fotos de colegas e contatos

A Microsoft também recebe uma solicitação para ler os perfis básicos das pessoas da sua organização (nome, e-mail e foto) e seus contatos do Outlook. Sua Machine usa essas informações apenas para mostrar fotos, cargos e empresas de pessoas que já estão no seu Graph, até 200 fotos por dia. Se alguém não tiver foto, a verificação será feita novamente após 30 dias.

O administrador da sua organização talvez precise aprovar as fotos dos colegas. Se isso não acontecer, o Outlook ainda será conectado, mas sem essas fotos. Uma conta conectada antes dessa mudança recebe uma tarefa: pressione **Reconectar** ou **Não precisa** para encerrá-la de vez. Uma conta pessoal (Outlook.com, Hotmail) não tem colegas, então a tarefa pede apenas as fotos dos contatos.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup.
2. Pressione **Conectar Microsoft** e entre na sua conta.
3. Se a Microsoft pedir aprovação do administrador, envie o link para o administrador do Microsoft 365 (**Copiar link**). Depois da aprovação, todas as pessoas da sua organização poderão conectar suas contas. Se você for o administrador, pressione **Sou o administrador: aprovar agora**.

Ou, no painel: **Conexões**, **E-mail**, escolha Outlook e pressione **Entrar com a Microsoft**. O link para o administrador fica logo abaixo do botão.

No seu próprio computador, depois que ela estiver [pareada com sua conta](friends.md#a-machine-on-your-own-computer): abra **Conexões**, depois **E-mail**, escolha Outlook e pressione **Entrar com a Microsoft**. O e-mail e o calendário são conectados juntos. Depois de passar pela Microsoft, você volta para **Conexões** no painel.

Para equipes de TI que têm seu próprio aplicativo Microsoft Entra: abra **Usar seu próprio app** nessa página ou execute `assistant connect outlook`.

## Remover

- Em uma Machine hospedada: pressione **Desconectar** ao lado da conta na página de configuração. **Desconectar ↗** em Conexões leva você até lá.
- No seu próprio computador: abra **Conexões**, selecione a conta, pressione **Detalhes** e depois **Desconectar**.

## Remover na Microsoft

A Microsoft não permite revogar um acesso, então remova-o também por lá:

- Conta corporativa ou escolar: myapps.microsoft.com
- Conta pessoal: account.live.com/consent/Manage
