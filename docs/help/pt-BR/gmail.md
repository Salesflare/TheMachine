---
title: Gmail
area: connections
summary: Lê seus e-mails e cria rascunhos de resposta no seu estilo. Só envia um e-mail depois que você aprova.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## O que ele lê

Todos os seus e-mails: os dos últimos 7 dias quando você conecta e, depois, todas as mensagens novas, recebidas e enviadas. Os e-mails que você envia também contam, assim sua assistente aprende como você escreve e o que prometeu.

E-mails de Promoções, newsletters, Atualizações e Fóruns são analisados rapidamente primeiro: remetente, assunto e algumas palavras, vários de uma vez. Quando algum importa, ele é lido por inteiro e pode virar uma tarefa. Nada passa sem ser visto.

## O que ele pode enviar

Um e-mail criado a partir de uma tarefa, e só depois que você aprova. **Fazer** prepara um rascunho; **Revisar e enviar** abre o e-mail pronto para edição, e nada é enviado até você pressionar **Enviar agora**. **Fazer login com o Google** também pede ao Google permissão para enviar. No seu próprio computador, com seu próprio app, o login permite apenas a leitura até você configurar o envio.

**De** na revisão é um pequeno seletor que aparece quando o Gmail permite que essa caixa de e-mail envie mensagens como um alias seu, marcado como **Meus** nas **Configurações**, em [Seus endereços](settings.md#your-addresses). Uma resposta a um e-mail recebido nesse alias começa com ele; um novo e-mail começa com o endereço da sua caixa de e-mail. Antes de enviar, o Gmail é consultado novamente: se não confirmar o endereço, nada é enviado.

A resposta vai para a conversa do e-mail ao qual ela responde. Se for enviada de outra caixa de e-mail sua, diferente daquela que recebeu o e-mail, a tarefa avisa antes do envio. Mesmo assim, a resposta vai para a conversa original.

Depois que uma resposta é enviada, a conversa sai da caixa de entrada e recebe o marcador Adiados por alguns dias (3, a menos que a tarefa indique outro prazo). Depois, ela volta ou reaparece antes se alguém responder. A revisão informa isso antes do envio. Essa é a sua caixa de e-mail: uma resposta que só promete realizar o trabalho mantém a tarefa aberta.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup.
2. Em **E-mail e agenda**, pressione **Conectar Google** e faça login. Na tela do Google, aparece o nome Salesflare, a empresa que criou The Machine.
3. O Gmail e o Google Calendar são conectados juntos.

Se você se cadastrou com o Google e permitiu o acesso ao Gmail e ao Calendar nessa tela, eles são conectados automaticamente. Os e-mails só são enviados quando você pressiona Enviar.

Ou, no painel: **Conexões**, **E-mail**, escolha Gmail e pressione **Fazer login com o Google**. Quando terminar, você volta ao painel.

No seu próprio computador, depois que ele estiver [pareado com sua conta](friends.md#a-machine-on-your-own-computer):

1. No painel, abra **Conexões**, depois **E-mail** e escolha Gmail.
2. Pressione **Fazer login com o Google** e faça login na aba que abrir. O Gmail e o Google Calendar são conectados juntos.

Se ainda não estiver pareada ou se você estiver usando seu próprio cliente OAuth do Google: abra **Usar seu próprio app** nessa tela ou execute `assistant connect gmail`. Pressione **Abrir o Google**, faça login e cole o endereço para o qual o Google redirecionar você. O Google Calendar do mesmo endereço também será conectado.

Talvez um administrador do Google Workspace precise permitir o app primeiro no Admin Console.

## Remover

- Em uma Machine hospedada: pressione **Desconectar** ao lado do endereço na página de configuração. Isso remove o Gmail e o Calendar desse endereço, e sua Machine esquece o login. Suas outras Machines mantêm os logins delas. No painel, **Desconectar ↗** em **Conexões** leva você até essa página. **Reconectar** nessa página permite fazer login novamente sem sair do painel.
- No seu próprio computador: abra **Conexões**, selecione Gmail, **Detalhes** e, em seguida, **Desconectar**. A leitura é interrompida. O que já foi importado permanece. Quando nenhum outro serviço usar esse login do Google, ele será esquecido. Suas outras Machines mantêm os logins delas.

## Desinstalar no Google

Na sua Conta do Google, abra **Segurança**, depois **Suas conexões com apps e serviços de terceiros**, e remova Salesflare (Fazer login com o Google ou hospedado) ou seu próprio app.
