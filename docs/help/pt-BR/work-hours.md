---
title: Horário de trabalho
area: settings
summary: Quando a sua Machine pode mandar mensagens para você, quando os itens adiados voltam e quando chega o resumo da manhã.
code: dashboard.html, assistant.py
order: 3
keywords: quiet hours, weekend, evening, night, do not disturb, time zone
---
Em **Configurações**, **Notificações**, em **Horário de trabalho**:

- **Dias de trabalho**: tarefas de trabalho e itens de trabalho adiados esperam por um dia de trabalho.
- **Mensagens das** e **Até**: nada é enviado para você fora desse horário, nem push, nem Telegram, nem e-mail.
- **Itens adiados voltam às**: quando um item adiado por um dia ou mais volta. O resumo da manhã chega pelo menos 5 minutos depois, para incluí-los.
- **Resumo da manhã**: quando chega o resumo da manhã.
- **Resumo do fim do dia**: quando chega o resumo do fim do dia. Começa 15 minutos antes de **Até** e acompanha esse horário até você escolher um seu.
- **Fuso horário**: o seu, para tudo isso.

Toque em **Salvar**. Por padrão, é de segunda a sexta, das 08:00 às 23:00, itens adiados às 09:00, o resumo da manhã às 08:30 e o do fim do dia às 22:45.

O que sai dentro desse horário, e como, está em [Notificações](notifications.md).

No seu próprio computador, `assistant hours` também mostra e muda esses horários.
