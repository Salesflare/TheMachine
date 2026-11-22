---
title: Gmail
area: connections
summary: Lê seus e-mails e prepara respostas no seu estilo. Só envia um e-mail depois da sua aprovação.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## O que ela lê

Todos os seus e-mails: os últimos 7 dias quando você conecta a conta e, depois, tudo o que chegar ou for enviado. Os e-mails que você envia também contam, assim ela aprende como você escreve e o que prometeu.

E-mails de promoções, newsletters, Atualizações e Fóruns são analisados rapidamente primeiro: remetente, assunto e algumas palavras, vários de uma vez. Quando algum é importante, ele é lido por completo e pode virar uma tarefa. Nenhum passa despercebido.

## O que ela pode enviar

Um e-mail criado a partir de uma tarefa, e só depois da sua aprovação. **Fazer** prepara um rascunho; **Revisar e enviar** abre o e-mail pronto para edição, e nada é enviado até você pressionar **Enviar agora**. **Fazer login com o Google** também pede ao Google permissão para enviar. No seu próprio computador, com seu próprio app, o acesso é somente para leitura até você adicionar a permissão de envio.

**De** na revisão é um seletor simples, disponível quando o Gmail permite que essa caixa de entrada envie mensagens como um dos seus aliases (um marcado como **Meus** em Configurações, [Seus endereços](settings.md#your-addresses)). Uma resposta a um e-mail recebido nesse alias é enviada por ele; um novo e-mail é enviado pelo endereço da sua caixa de entrada. Antes de enviar, o Gmail é consultado novamente: se não confirmar o endereço, nada é enviado.

Uma resposta entra na conversa do e-mail ao qual responde. Se ela for enviada de outra caixa de entrada sua, diferente daquela que recebeu o e-mail, a tarefa avisa antes do envio. Mesmo assim, a resposta entra na conversa original.

Depois que uma resposta é enviada, a conversa sai da sua caixa de entrada e recebe o marcador Adiados por alguns dias (3, a menos que a tarefa indique outro prazo). Depois, ela volta, ou volta antes se alguém responder. A revisão avisa antes do envio. Essa é a sua caixa de entrada: uma resposta que só promete fazer o trabalho mantém a tarefa aberta.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup.
2. Em **E-mail e agenda**, pressione **Conectar Google** e faça login. Na tela do Google, Salesflare aparece como responsável pelo The Machine.
3. O Gmail e o Google Calendar são conectados juntos.

Se você se inscreveu com o Google e permitiu o acesso ao Gmail e ao Calendar nessa tela, eles se conectam automaticamente. O envio só acontece quando você pressiona Enviar.

Ou, no painel: **Conexões**, **E-mail**, escolha Gmail e pressione **Fazer login com o Google**. Quando terminar, você volta ao painel.

No seu próprio computador, depois que ele estiver [conectado à sua conta](friends.md#a-machine-on-your-own-computer):

1. No painel, abra **Conexões**, depois **E-mail**, e escolha Gmail.
2. Pressione **Fazer login com o Google** e faça login na aba que abrir. O Gmail e o Google Calendar são conectados juntos.

Se o computador não estiver conectado à sua conta ou você estiver usando seu próprio cliente OAuth do Google: abra **Usar seu próprio app** nessa tela ou execute `assistant connect gmail`. Pressione **Abrir o Google**, faça login e cole o endereço para o qual o Google redirecionar você. O Google Calendar do mesmo endereço também será conectado.

Talvez um administrador do Google Workspace precise permitir o app primeiro, no Admin console.

## Desconectar

- Em uma Machine hospedada: pressione **Desconectar** ao lado do endereço na sua página de configuração. Isso desconecta o Gmail e o Calendar desse endereço, e sua Machine esquece os dados de login. Suas outras Machines mantêm os delas. No painel, **Desconectar ↗** em Conexões leva você até lá. **Reconectar** nessa página permite fazer login novamente sem sair do painel.
- No seu próprio computador: abra **Conexões**, Gmail, **Detalhes** e pressione **Desconectar**. A leitura é interrompida. O que já foi importado continua. Quando nenhum outro serviço usa esse login do Google, sua Machine o esquece. Suas outras Machines mantêm os delas.

## Desinstalar no Google

Na sua Conta do Google, abra Segurança, depois Suas conexões com apps e serviços de terceiros, e remova Salesflare (Fazer login com o Google ou hospedada) ou seu próprio app.
