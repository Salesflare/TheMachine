---
title: Microsoft Outlook e Calendar
area: connections
summary: E-mails e reuniões do Outlook, para Microsoft 365 e Outlook.com. Só envia um e-mail depois que você aprova.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 41c9c0174a2a21c7
---
## O que ele lê

- **Outlook**: todos os seus e-mails, os últimos 7 dias quando você conecta, e depois tudo o que é novo.
- **Outlook Calendar**: suas reuniões, só leitura.

E-mails em Outros e newsletters passam primeiro por uma olhada rápida: remetente, assunto e algumas palavras, vários de uma vez. Quando um importa, ele é lido por inteiro e pode virar uma tarefa. Nada é pulado sem ser visto.

## O que ele pode enviar e mudar

- Um e-mail a partir de uma tarefa, só depois que você aprova na prévia.
- Uma resposta vai para a conversa do Outlook do e-mail que ela responde.
- Quando você adia uma tarefa sobre um e-mail, as mensagens da conversa vão para uma pasta Snoozed no Outlook e voltam quando a tarefa volta.

A agenda nunca é alterada.

## Fotos de colegas e contatos

A Microsoft também recebe o pedido de ler os perfis básicos da sua organização (nome, email e foto) e seus contatos do Outlook. Sua Machine só os usa para fotos, cargos e empresas de pessoas que já estão no seu Graph, até 200 fotos por dia. Quem não tem foto é verificado de novo depois de 30 dias.

Pode ser que o admin da sua organização precise aprovar as fotos dos colegas. Se não aprovar, o Outlook conecta mesmo assim, só que sem essas fotos. Uma conta conectada antes disso recebe uma tarefa: toque em **Reconectar**, ou em **Não precisa** para fechá-la de vez. Uma conta pessoal (Outlook.com, Hotmail) não tem colegas, então a tarefa dela só pede as fotos dos contatos.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup.
2. Clique em **Conectar Microsoft** e entre.
3. Se a Microsoft pedir aprovação de um admin, envie este link ao administrador do seu Microsoft 365: themachine.computer/m365-admin-consent. **Copiar link** copia o link. Assim que ele aprovar, todos na sua organização podem se conectar. Se for você, clique em **Sou o admin: aprovar agora**.

Ou no painel: **Conexões**, **E-mail**, escolha Outlook e clique em **Entrar com Microsoft**. Quando terminar, você volta para o painel. Precisa da aprovação do seu administrador? O mesmo link fica embaixo do botão, com **Copiar link**.

No seu próprio computador, depois que ele estiver [pareado com sua conta](friends.md#a-machine-on-your-own-computer): abra **Conexões**, depois **E-mail**, escolha Outlook e clique em **Entrar com Microsoft**. E-mail e agenda se conectam juntos.

Com seu próprio app: abra **Usar seu próprio app** ali, ou execute `assistant connect outlook` ou `assistant connect outlook_calendar`. Ele usa seu próprio registro de app no Microsoft Entra e um código de login. Ele pergunta se também deve enviar o que você aprovar.

## Remover

- Em uma Machine hospedada: clique em **Desconectar** ao lado da conta na sua página de configuração. No painel, **Desconectar ↗** em Conexões leva você até lá. **Reconectar** ali entra de novo sem sair do painel.
- No seu próprio computador: **Conexões**, abra a conta, **Detalhes** e depois **Desconectar**.

## Desinstalar na Microsoft

A Microsoft não oferece um jeito de revogarmos um login, então remova lá também:

- Conta de trabalho ou escola: myapps.microsoft.com
- Conta pessoal: account.live.com/consent/Manage
