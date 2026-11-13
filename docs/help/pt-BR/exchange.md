---
title: Exchange Server
area: connections
summary: Reuniões de um Exchange Server que sua empresa mantém (2013 a 2019 ou Subscription Edition). Só leitura.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## O que ela lê

Suas reuniões, com convidados, salas e notas: a semana passada e o próximo mês quando você conecta, depois cada mudança. Elas aparecem no Calendário e na preparação das reuniões.

É só leitura: nunca adiciona, move ou remove uma reunião. O e-mail do Exchange Server ainda não é lido.

## Microsoft 365 ou Exchange Server?

O Exchange Server roda na sua empresa. O Microsoft 365 (Exchange Online) é a nuvem da Microsoft: para ele, escolha **Outlook Calendar**. Se o seu endereço estiver no Microsoft 365, o formulário avisa.

## Conecte

1. No painel, abra **Conexões**, depois **Calendário**, e escolha **Exchange Server**.
2. Informe seu e-mail de trabalho e sua senha do Windows.
3. Clique em **Conectar**.

O servidor é encontrado pelo seu endereço (Autodiscover). Não encontrado? Abra **Configurações do servidor** e digite o servidor que sua equipe de TI informa para o Outlook, como `mail.example.com`. Entra com um nome diferente do seu endereço? Digite-o como `DOMAIN\name` em **Usuário**.

Ela entra com NTLM ou Basic, só por https.

## Quando para

- **O servidor de calendário recusou a senha**: sua senha do Windows mudou. Conecte de novo.
- **Uma caixa do Microsoft 365**: sua caixa foi para o Microsoft 365. Desconecte esta e conecte o **Outlook Calendar**.
- **Não foi possível alcançar o servidor de calendário**: ela tenta de novo sozinha. Alguns servidores só são alcançáveis dentro da rede da empresa ou por VPN.

## Remova

**Conexões**, abra o calendário, **Detalhes**, depois **Desconectar**. O que já foi trazido fica.
