---
title: Proton Calendar e links de calendário (ICS)
area: connections
summary: Reuniões do link de compartilhamento de um calendário: Proton Calendar, calendários publicados, escolares ou esportivos. Só leitura.
covers: connector:proton_calendar, connector:ics
code: ics_feed.py, ical.py, machine/sources/calendar_setup.py
order: 15
translated: b3bcf33b5c027baf
---
## O que ela lê

Os eventos do calendário por trás do link, com eventos recorrentes e fusos horários: a semana passada e o próximo mês, depois cada mudança. Eles aparecem no Calendário e na preparação das reuniões.

Um link só pode ser lido, então nunca muda uma reunião. Ela confere o link no máximo a cada 15 minutos. Segundo a Proton, as mudanças podem levar algumas horas para chegar a um link.

## Conecte o Proton Calendar

O Proton Calendar não tem outro acesso para apps, então usa um link de compartilhamento.

1. Abra o Proton Calendar na web, em calendar.proton.me. Nos apps de celular não dá para criar links de compartilhamento.
2. Vá em "Configurações", "Todas as configurações", "Calendários", e escolha o calendário.
3. Em "Share with anyone", clique em "Create link" e escolha "Full view". Limited view só mostra quando você está ocupado.
4. Clique em "Copy link".
5. No painel, abra **Conexões**, depois **Calendário**, escolha **Proton Calendar**, cole o link e clique em **Conectar**.

## Conecte qualquer outro link de calendário

Escolha **Link de calendário (ICS)** e cole o link: um endereço https ou webcal que termina em .ics, como um calendário público do iCloud, um calendário publicado do Outlook ou o calendário da escola do seu filho.

## Mantenha o link privado

Quem tiver o link pode ler o calendário. The Machine o guarda como uma senha: nunca em um log nem na tela. Para parar, apague o link onde você o criou e clique aqui em **Desconectar**.

## Quando para

- **O link do calendário parou de funcionar**: o link foi apagado ou mudou. Crie um novo e conecte de novo.
- **Não foi possível alcançar o servidor de calendário**: ela tenta de novo sozinha.
