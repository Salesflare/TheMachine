---
title: iCloud e outros calendários (CalDAV)
area: connections
summary: Reuniões do iCloud Calendar ou de qualquer calendário CalDAV, como Fastmail, Nextcloud ou Zoho. Só leitura.
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
---
## O que ela lê

Suas reuniões, com convidados, salas e notas: a semana passada e o próximo mês quando você conecta, depois cada mudança. Elas aparecem no Calendário e na preparação das reuniões, como as reuniões do Google ou do Outlook. Todos os calendários da conta são lidos, ou só o que você indicar.

É só leitura: nunca adiciona, move ou remove uma reunião.

## Conecte o iCloud Calendar

1. Crie uma senha específica de app em [appleid.apple.com](https://appleid.apple.com), em **Início de Sessão e Segurança**. A que você criou para o iCloud Mail também funciona.
2. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha **iCloud Calendar**.
3. Informe seu Apple ID e a senha específica de app, depois clique em **Conectar**.

## Conecte outro calendário

1. Abra **Conexões**, depois **+ Adicionar**, e escolha **Outro calendário**.
2. Informe seu endereço de e-mail e sua senha. Muitos provedores pedem aqui uma senha de app, criada nas configurações da sua conta.
3. Clique em **Conectar**.

O servidor é encontrado para Fastmail, Yahoo, Zoho e servidores que se anunciam. O seu não foi encontrado? Abra **Configurações do servidor** e digite o endereço CalDAV dele, como `nextcloud.example.com/remote.php/dav`. **Só este calendário** lê um único calendário pelo nome.

Calendários do Google ou da Microsoft? Escolha **Google Calendar** ou **Outlook Calendar** no lugar.

## Quando para

- **O servidor de calendário recusou a senha**: você a mudou, ou a senha de app foi removida. Conecte de novo com uma nova.
- **Não foi possível alcançar o servidor de calendário**: ela tenta de novo sozinha. Se continuar falhando, confira o endereço em Configurações do servidor.

## Remova

**Conexões**, abra o calendário, **Detalhes**, depois **Desconectar**. O que já foi trazido fica. Remova também a senha de app no seu provedor.
