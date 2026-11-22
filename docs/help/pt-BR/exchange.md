---
title: Exchange Server
area: connections
summary: Reuniões de um Exchange Server operado pela sua empresa (de 2013 a 2019 ou Subscription Edition). Somente leitura.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: f2b98c9bd4f08dba
---
## O que ele lê

Suas reuniões, com participantes, salas e anotações: a semana anterior e o próximo mês quando você conecta, além de cada alteração. Elas aparecem no **Calendário** e na preparação para reuniões.

É somente leitura: nunca adiciona, move nem remove reuniões. Ainda não lemos e-mails do Exchange Server.

## Microsoft 365 ou Exchange Server?

O Exchange Server é operado pela sua empresa. O Microsoft 365 (Exchange Online) é a nuvem da Microsoft: escolha **Outlook Calendar** para se conectar a ele.

Digite seu endereço primeiro. Se ele estiver no Microsoft 365, o formulário vai informar isso e mostrar **Entrar com a Microsoft** no lugar do campo de senha. Isso abre a tela de entrada do Outlook Calendar, sem pedir sua senha. Se não encontrar em alguns segundos ou se sua empresa tiver um servidor próprio, o formulário de senha continua disponível.

## Conectar

1. No painel, abra **Conexões**, depois **Calendário**, e escolha **Exchange Server**.
2. Preencha seu e-mail de trabalho e sua senha do Windows.
3. Clique em **Conectar**.

O servidor é localizado pelo seu endereço (Autodiscover). Não encontrou? Abra **Configurações do servidor** e digite o servidor que sua equipe de TI informar para o Outlook, como `mail.example.com`. Se você entrar com um nome diferente do seu endereço, digite-o em **Usuário** como `DOMAIN\name`.

A autenticação usa NTLM ou Basic, somente via https.

## Quando a conexão para de funcionar

- **O servidor de calendário recusou a senha**: sua senha do Windows mudou. Conecte novamente.
- **Uma caixa de correio do Microsoft 365**: sua caixa de correio foi transferida para o Microsoft 365. Desconecte esta conta e conecte **Outlook Calendar**.
- **Não foi possível alcançar o servidor de calendário**: novas tentativas são feitas automaticamente. Alguns servidores só podem ser acessados pela rede da empresa ou pela VPN.

## Remover

Abra **Conexões**, selecione o calendário, toque em **Detalhes** e depois em **Desconectar**. O que já foi importado continua lá.
