---
title: Microsoft Teams
area: connections
summary: Chats do Teams, chats de reuniões e anotações de reuniões em uma conta corporativa ou escolar. As respostas só são enviadas depois da sua aprovação.
covers: connector:teams
code: connectors/teams.py, teams_send.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 9ca0bb08466b4d58
---
## O que lê

Seus chats individuais, em grupo e de reuniões no Teams: as mensagens dos últimos 7 dias quando você conecta, depois novas mensagens a cada poucos minutos. Cerca de um ano de chats antigos e de conversas em canais, com a autorização do administrador, chega depois como [histórico](history.md), aos poucos, sem atrasar nada.

Com a autorização do administrador, ela também lê:

- Conversas nos canais das suas equipes.
- Transcrições de reuniões que você organizou.
- Anotações de reunião e itens de ação do Copilot, se você tiver uma licença do Microsoft 365 Copilot.

Cada transcrição ou conjunto de anotações aparece na reunião correspondente do seu Calendário, marcada como **Do Teams**. Sem isso, o chat da reunião continua disponível.

Bots, aplicativos e mensagens do sistema ficam de fora.

## O que pode fazer

Responder em um chat individual, em grupo ou de reunião de onde veio uma tarefa. The Machine prepara um rascunho da resposta. Ela só é enviada depois que você revisa e toca em **Enviar agora**, em seu nome, naquele chat. Ela nunca inicia um chat novo.

Ela não publica em canais. Para responder em uma conversa de canal, abra-a com **Abrir no Teams**.

## O que ela pede

A Microsoft pede autorização para que The Machine leia seus chats e seu perfil, e envie mensagens de chat em seu nome. Não é necessário ter autorização do administrador.

Se você conectou o Teams antes de ela poder enviar mensagens, o cartão mostra **Reconectar para enviar respostas.** Toque em **Reconectar** e autorize novamente. Até lá, o rascunho fica disponível para você enviar pelo Teams.

Para acessar canais, transcrições e anotações do Copilot, é preciso que o administrador da sua organização autorize uma vez. Até lá, o cartão do Teams informa o que ela ainda não pode ler e por quê.

Ela só funciona com uma conta Microsoft corporativa ou escolar. Contas pessoais não têm chats do Teams disponíveis para leitura dessa forma.

## Conectar

Em uma Machine hospedada:

1. No painel, abra **Conexões** e depois **Chat** para **Microsoft Teams** ou **Reuniões** para **Reuniões do Teams**. As duas opções usam o mesmo login.
2. Toque em **Entrar com a Microsoft** e autorize o acesso. Você voltará ao painel.
3. Para acessar canais e anotações de reunião, envie ao administrador o link exibido na página de login. Depois que ele autorizar, conecte o Teams novamente.

Durante a configuração, a página de configuração também tem a opção **Conectar ao Microsoft Teams**.

No seu próprio computador, depois que ele estiver [conectado à sua conta](friends.md#a-machine-on-your-own-computer): abra **Conexões** e depois **Chat** ou **Reuniões**, escolha **Microsoft Teams** ou **Reuniões do Teams** e toque em **Entrar com a Microsoft**. Nesse caso, ela lê seus chats e chats de reuniões. Canais e anotações de reunião ainda não estão disponíveis.

## Remover

No painel: abra **Conexões**, escolha Microsoft Teams, toque em **Detalhes** e depois em **Desconectar**. O conteúdo que ela já trouxe continua disponível.

## Revogar o acesso na Microsoft

Acesse myapps.microsoft.com e remova The Machine. Se o Outlook estiver conectado com o mesmo endereço, ele também será desconectado.
