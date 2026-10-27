---
title: Gmail
area: connections
summary: Lê seus e-mails e escreve rascunhos de respostas com a sua voz. Só envia um e-mail depois que você aprova.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
---
## O que ele lê

Todos os seus e-mails: os últimos 7 dias quando você conecta, depois tudo o que é novo, recebido e enviado. Os e-mails que você envia também contam, para aprender como você escreve e o que você prometeu.

E-mails de Promoções, newsletters, Atualizações e Fóruns recebem primeiro uma olhada rápida: remetente, assunto e algumas palavras, muitos de uma vez. Quando um importa, ele é lido por inteiro e pode virar uma tarefa. Nada é ignorado sem ser visto.

## O que ele pode enviar

Um e-mail a partir de uma tarefa, e só depois que você aprova. **Fazer** prepara um rascunho. **Revisar e enviar** abre o rascunho pronto para editar, e nada sai até você tocar em **Enviar agora**. **Entrar com o Google** também pede permissão de envio ao Google. Com o seu próprio app no seu próprio computador, o login é só de leitura até você mesmo adicionar o envio.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup.
2. Em **E-mail e agenda**, toque em **Conectar Google** e entre. A tela do Google mostra Salesflare, quem faz a The Machine.
3. O Gmail e o Google Calendar se conectam juntos.

Ou no painel: **Conexões**, **+ Adicionar**, escolha Gmail e clique em **Entrar com Google**. Quando terminar, você volta para o painel.

No seu próprio computador, depois de [pareado com a sua conta](fleet.md):

1. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha Gmail.
2. Toque em **Entrar com o Google** e entre na aba que abrir. O Gmail e o Google Calendar se conectam juntos.

Sem pareamento, ou com o seu próprio cliente OAuth do Google: abra **Usar seu próprio app** ali, ou rode `assistant connect gmail`. Ele usa o gog. Abra o endereço que ele mostra e entre.

Um administrador do Google Workspace pode precisar liberar o app antes, no Admin console.

## Remover

- Em uma Machine hospedada: toque em **Desconectar** ao lado do endereço na sua página de configuração. Isso remove o Gmail e o Calendário desse endereço e revoga o login no Google. No painel, **Reconectar ou desconectar ↗** em Conexões leva você até lá.
- No seu próprio computador: **Conexões**, abra Gmail, **Detalhes** e depois **Desconectar**. Ele para de ler. O que já foi trazido fica. Quando nada mais usa esse login do Google, ele é revogado no Google.

## Desinstalar no Google

Na sua Conta do Google, abra Segurança, depois Suas conexões com apps e serviços de terceiros, e remova Salesflare (Entrar com o Google, ou hospedada) ou o seu próprio app.
