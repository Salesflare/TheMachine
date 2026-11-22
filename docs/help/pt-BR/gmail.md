---
title: Gmail
area: connections
summary: Lê seus e-mails e prepara respostas no seu estilo. Só envia um e-mail depois que você aprova.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: c1f2362cd496840e
---
## O que ela lê

Todos os seus e-mails: os últimos 7 dias quando você conecta, e depois tudo que chega ou é enviado. Os e-mails que você envia também contam, assim ela aprende como você escreve e o que prometeu.

E-mails de Promoções, newsletters, Atualizações e Fóruns recebem primeiro uma olhada rápida: remetente, assunto e algumas palavras, vários de uma vez. Quando algum é importante, ela lê tudo e pode transformá-lo em uma tarefa. Nada passa sem ser visto.

## O que ela pode enviar

Um e-mail criado a partir de uma tarefa, e só depois que você aprova. **Fazer** prepara um rascunho; **Revisar e enviar** abre o e-mail pronto para edição, e nada é enviado até você pressionar **Enviar agora**. **Entrar com o Google** também solicita ao Google permissão para enviar. Se você usar seu próprio app no seu próprio computador, o login permite apenas a leitura, até você adicionar o envio por conta própria.

**De** na revisão é um seletor pequeno que aparece quando o Gmail permite que essa caixa de entrada envie mensagens como um alias seu (um marcado como **Meus** em **Configurações**, [Seus endereços](settings.md#your-addresses)). Uma resposta a um e-mail recebido por esse alias é enviada por ele; um e-mail novo é enviado pelo endereço da sua caixa de entrada. Logo antes do envio, o Gmail é consultado de novo: se não confirmar o endereço, nada é enviado.

A resposta entra na conversa do e-mail ao qual responde. Se ela for enviada de outra das suas caixas de entrada, e não daquela que recebeu o e-mail, a tarefa avisa antes do envio. Mesmo assim, ela chega à conversa da pessoa.

Depois que uma resposta é enviada, a conversa sai da sua caixa de entrada e fica com o marcador Adiada por alguns dias (3, a menos que a tarefa diga outra coisa). Depois, ela volta, ou antes se alguém responder. A revisão avisa antes do envio.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup.
2. Em **E-mail e Calendário**, pressione **Conectar Google** e faça login. A tela do Google identifica a Salesflare, que criou a The Machine.
3. O Gmail e o Google Calendar se conectam juntos.

Se você se cadastrou com o Google e permitiu o acesso ao Gmail e ao Calendar nessa tela, eles se conectam automaticamente. O envio só acontece quando você pressiona Enviar.

Ou, no painel: **Conexões**, **E-mail**, escolha Gmail e pressione **Entrar com o Google**. Quando terminar, você voltará ao painel.

No seu próprio computador, depois que ela estiver [pareada com sua conta](friends.md#a-machine-on-your-own-computer):

1. No painel, abra **Conexões**, depois **E-mail** e escolha Gmail.
2. Pressione **Entrar com o Google** e faça login na guia que abrir. O Gmail e o Google Calendar se conectam juntos.

Se não estiver pareado ou você estiver usando seu próprio cliente OAuth do Google, abra **Usar seu próprio app** nessa tela ou execute `assistant connect gmail`. Pressione **Abrir o Google**, faça login e cole o endereço para o qual o Google redirecionar você. O Google Calendar do mesmo endereço também será conectado.

Talvez um administrador do Google Workspace precise permitir o app primeiro no Admin console.

## Desconectar

- Em uma Machine hospedada: pressione **Desconectar** ao lado do endereço na sua página de configuração. Isso remove o Gmail e o Calendar desse endereço, e sua Machine esquece o login. Suas outras Machines continuam conectadas. No painel, **Desconectar ↗** em Conexões leva você até essa página. **Reconectar** nessa página permite fazer login de novo sem sair do painel.
- No seu próprio computador: abra **Conexões**, abra o Gmail, selecione **Detalhes** e depois **Desconectar**. A leitura é interrompida. O que já foi importado continua lá. Se nada mais estiver usando esse login do Google, ele será esquecido. Suas outras Machines continuam conectadas.

## Desinstalar no Google

Na sua Conta do Google, abra Segurança, depois Suas conexões com apps e serviços de terceiros, e remova a Salesflare (Entrar com o Google ou hospedada) ou seu próprio app.
