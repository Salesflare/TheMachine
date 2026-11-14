---
title: Microsoft Teams
area: connections
summary: Chats do Teams, chats de reuniões e notas de reuniões para uma conta corporativa ou de estudante. Ele só lê.
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 864f9e6e98309439
---
## O que ele lê

Seus chats individuais, de grupo e de reuniões no Teams: os últimos 7 dias ao conectar, depois as mensagens novas a cada poucos minutos. Cerca de um ano de chats antigos, e de threads de canais com o ok do seu admin, chega depois como [histórico](history.md), aos poucos, sem travar nada.

Com o OK do seu admin, ele também lê:

- As conversas dos canais das suas equipes.
- As transcrições das reuniões que você organizou.
- As notas de reunião e tarefas do Copilot, se você tem uma licença do Microsoft 365 Copilot.

Cada transcrição ou conjunto de notas vai para a reunião na sua agenda, marcado **Do Teams**. Sem eles, o chat da reunião continua lá.

Bots, apps e mensagens do sistema ficam de fora.

## O que ele pode fazer

Nada no Teams. Ele só lê. Para responder, abra o chat com **Abrir no Teams**.

## O que ele pede

A Microsoft pede para deixar a The Machine ler seus chats e seu perfil. Isso não precisa de admin.

Canais, transcrições e notas do Copilot precisam uma vez do OK do admin da sua organização. Até lá, o cartão do Teams diz o que ele ainda não consegue ler e por quê.

Só funciona com uma conta Microsoft corporativa ou de estudante. Contas pessoais não têm chats do Teams que dê para ler assim.

## Conectar

Numa Machine hospedada:

1. No painel, abra **Conexões**, **Chat** ou **Reuniões** e escolha **Microsoft Teams** (em Chat) ou **Reuniões do Teams** (em Reuniões). Os dois são o mesmo login.
2. Clique em **Entrar com Microsoft** e dê o OK. Você volta para o painel.
3. Para canais e notas de reuniões, mande ao seu admin o link que a página de login mostra. Quando ele aprovar, conecte o Teams de novo.

Durante a configuração, a página de configuração também tem **Connect Microsoft Teams**.

No seu próprio computador, depois que ele estiver [pareado com sua conta](friends.md#a-machine-on-your-own-computer): abra **Conexões**, depois **Chat** ou **Reuniões**, escolha **Microsoft Teams** ou **Reuniões do Teams** e clique em **Entrar com Microsoft**. Lá, ele lê seus chats e chats de reuniões. Canais e notas de reuniões ainda não estão disponíveis lá.

## Remover

No painel: **Conexões**, abra o Microsoft Teams, **Detalhes** e depois **Desconectar**. O que ele já trouxe fica.

## Revogar na Microsoft

Abra myapps.microsoft.com e remova a The Machine. Se o Outlook estiver conectado com o mesmo endereço, ele também é desconectado.
