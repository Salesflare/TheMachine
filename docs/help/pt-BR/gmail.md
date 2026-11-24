---
title: Gmail
area: connections
summary: Lê seus e-mails e cria rascunhos de resposta no seu estilo. Só envia um e-mail depois da sua aprovação.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: f0565a7bf839f49f
---
## O que ela lê

Todos os seus e-mails: os dos últimos 7 dias quando você conecta a conta e, depois, todos os novos, enviados e recebidos. Os e-mails que você envia também são considerados, para que ela aprenda como você escreve e o que prometeu.

E-mails de promoções, newsletters, atualizações e fóruns são analisados rapidamente primeiro: remetente, assunto e algumas palavras, vários de uma vez. Quando algum é importante, ele é lido por completo e pode virar uma tarefa. Nada passa sem ser visto.

## O que ela pode enviar

Um e-mail relacionado a uma tarefa, e só depois da sua aprovação. **Fazer** prepara um rascunho; **Revisar e enviar** abre o rascunho pronto para edição, e nada é enviado até você pressionar **Enviar agora**. **Entrar com o Google** também pede ao Google permissão para enviar e-mails. Ao usar seu próprio app no seu próprio computador, o acesso é somente para leitura até você configurar o envio.

Na tela de revisão, **De** aparece como um seletor quando o Gmail permite que essa caixa de e-mail envie mensagens como um alias seu (um marcado como **Meus** em **Configurações**, [Seus endereços](settings.md#your-addresses)). Uma resposta a um e-mail recebido por esse alias é enviada por ele; uma nova mensagem é enviada pelo endereço da sua caixa de e-mail. Antes do envio, o Gmail é consultado novamente: se não confirmar o endereço, nada será enviado.

A resposta entra na conversa do e-mail ao qual responde. Se for enviada por outra das suas caixas de e-mail, diferente daquela que recebeu o e-mail, a tarefa informa isso antes do envio. Mesmo assim, a resposta aparece na conversa original.

Depois que uma resposta é enviada, a conversa sai da caixa de entrada e recebe o marcador Adiada por alguns dias (3, a menos que a tarefa indique outro prazo). Depois, ela volta, ou volta antes se alguém responder. Ela nunca fica fora da caixa de entrada depois do prazo da tarefa: volta no dia útil anterior e, se o prazo for hoje, permanece na caixa de entrada. A tela de revisão informa isso antes do envio. Essa é a sua caixa de e-mail: uma resposta que apenas promete realizar o trabalho mantém a tarefa aberta.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup.
2. Em **E-mail e Calendário**, pressione **Conectar Google** e faça login. Na tela do Google, aparece Salesflare, responsável pela The Machine.
3. O Gmail e o Google Calendar são conectados juntos.

Se você se cadastrou com o Google e permitiu o acesso ao Gmail e ao Calendar nessa tela, eles são conectados automaticamente. Só há envio quando você pressiona Enviar.

Ou, no painel: **Conexões**, **E-mail**, escolha Gmail e pressione **Entrar com o Google**. Quando terminar, você volta ao painel.

No seu próprio computador, depois que ela estiver [vinculada à sua conta](friends.md#a-machine-on-your-own-computer):

1. No painel, abra **Conexões**, depois **E-mail**, e escolha Gmail.
2. Pressione **Entrar com o Google** e faça login na guia que abrir. O Gmail e o Google Calendar são conectados juntos.

Se ela não estiver vinculada ou se você usar seu próprio cliente OAuth do Google: abra **Usar seu próprio app** nessa tela ou execute `assistant connect gmail`. Pressione **Abrir o Google**, faça login e cole o endereço para o qual o Google redirecionar você. O Google Calendar da mesma conta também será conectado.

Talvez um administrador do Google Workspace precise permitir o app primeiro, no Admin Console.

## Remover

- Em uma Machine hospedada: pressione **Desconectar** ao lado do endereço na sua página de configuração. Isso remove o Gmail e o Calendar desse endereço, e sua Machine apaga os dados de login. Suas outras Machines mantêm os delas. No painel, **Desconectar ↗** em Conexões leva você até essa página. **Reconectar** nessa página permite fazer login novamente sem sair do painel.
- No seu próprio computador: abra **Conexões**, escolha Gmail, **Detalhes** e depois **Desconectar**. A leitura é interrompida. O que já foi importado continua lá. Quando nenhum outro recurso usar esse login do Google, ele será apagado. Suas outras Machines mantêm os delas.

## Desinstalar no Google

Na sua Conta do Google, abra Segurança, depois Suas conexões com apps e serviços de terceiros, e remova Salesflare (Entrar com o Google ou a versão hospedada) ou seu próprio app.
