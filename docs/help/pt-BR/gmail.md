---
title: Gmail
area: connections
summary: Lê seus e-mails e prepara rascunhos de resposta no seu estilo. Só envia um e-mail depois que você aprova.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: e06946aaa6ad0e1a
---
## O que ela lê

Todos os seus e-mails: os últimos 7 dias quando você conecta, depois tudo que chega ou é enviado. Os e-mails que você envia também contam, assim ela aprende como você escreve e o que prometeu.

E-mails de promoções, newsletters, atualizações e fóruns são analisados rapidamente primeiro: remetente, assunto e algumas palavras, vários de uma vez. Quando algum é importante, ela lê tudo e pode transformá-lo em uma tarefa. Nada passa sem ser visto.

## O que ela pode enviar

Um e-mail criado a partir de uma tarefa, e só depois que você aprova. **Fazer** prepara um rascunho; **Revisar e enviar** abre o rascunho para você editar, e nada é enviado até você pressionar **Enviar agora**. **Fazer login com o Google** também pede ao Google permissão para enviar. Com seu próprio app no seu computador, o login permite apenas a leitura até você configurar o envio.

**De** na revisão é um seletor simples que aparece quando o Gmail permite que essa caixa de entrada envie como um alias seu (marcado como **Meus** em **Configurações**, [Seus endereços](settings.md#your-addresses)). Uma resposta a um e-mail enviado para esse alias começa por ele; um novo e-mail começa pelo endereço da sua caixa de entrada. Logo antes de enviar, o Gmail é consultado novamente: se não confirmar o endereço, nada será enviado.

Uma resposta vai para a conversa do e-mail ao qual responde. Se ela sair de outra das suas caixas de entrada, diferente daquela que recebeu o e-mail, a tarefa avisa você antes do envio. Mesmo assim, ela chega à conversa da pessoa.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup.
2. Em **E-mail e Calendário**, pressione **Conectar Google** e faça login. A tela do Google identifica a Salesflare, que criou The Machine.
3. Gmail e Google Calendar são conectados juntos.

Se você se cadastrou com o Google e permitiu o acesso ao Gmail e ao Calendário nessa tela, eles se conectam automaticamente. O envio só acontece quando você pressiona Enviar.

Ou, no painel: **Conexões**, **E-mail**, escolha Gmail e pressione **Fazer login com o Google**. Quando terminar, você voltará ao painel.

No seu próprio computador, depois que ele estiver [conectado à sua conta](friends.md#a-machine-on-your-own-computer):

1. No painel, abra **Conexões**, depois **E-mail**, e escolha Gmail.
2. Pressione **Fazer login com o Google** e faça login na aba que abrir. Gmail e Google Calendar são conectados juntos.

Se ainda não estiver conectado à sua conta ou se estiver usando seu próprio cliente OAuth do Google, abra **Usar seu próprio app** nessa tela ou execute `assistant connect gmail`. Pressione **Abrir o Google**, faça login e cole o endereço para o qual o Google redirecionar você. O Google Calendar do mesmo endereço também será conectado.

Talvez um administrador do Google Workspace precise permitir o app primeiro no Admin Console.

## Remover

- Em uma Machine hospedada: pressione **Desconectar** ao lado do endereço na sua página de configuração. Isso remove Gmail e Calendar desse endereço, e sua Machine esquece o login. Suas outras Machines mantêm os delas. No painel, **Desconectar ↗** em **Conexões** leva você até essa página. **Reconectar** nessa página permite fazer login de novo sem sair do painel.
- No seu próprio computador: abra **Conexões**, selecione Gmail, **Detalhes** e depois **Desconectar**. Ela para de ler. O que já trouxe continua lá. Quando mais nada nela usar esse login do Google, ela o esquecerá. Suas outras Machines mantêm os delas.

## Desinstalar no Google

Na sua Conta do Google, abra Segurança, depois Suas conexões com apps e serviços de terceiros, e remova Salesflare (Fazer login com o Google ou hospedada) ou seu próprio app.
