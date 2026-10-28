---
title: Telegram
area: connections
summary: Recibe tus tareas en Telegram, con los mismos botones que el panel, a través de un bot propio. Opcional.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## Qué hace

Este Telegram es una forma de recibir tus tareas. Para que The Machine lea tus propios chats de Telegram, mira [Chats de Telegram](telegram-chats.md). Tu propio bot envía cada tarea dentro de tu [horario laboral](work-hours.md), con los mismos botones que el panel: **Hazlo**, **Posponer**, **Cambiar**, **Marcar como hecha**, **No hace falta**, y **Enviar** para un mensaje preparado.

Telegram es opcional. El panel como app del teléfono envía las mismas tareas como notificaciones.

## Qué puede enviar

Solo mensajes para ti, desde tu propio bot. Un mensaje para cualquier otra persona sigue necesitando tu aprobación en la tarea.

## Conéctalo

En una Machine alojada:

1. En Telegram, escribe a @BotFather y envía /newbot. Copia el token que te da.
2. En tu página de configuración, en **Añade más cuando quieras**, abre Telegram, pega el token y pulsa **Añadir mi bot**.

No forma parte de la configuración: añádelo cuando quieras. Tu panel te lo sugiere cuando una tarea pospuesta solo volvería ahí.

En tu propio ordenador, el instalador te lo pide, o ejecuta `assistant telegram on` con tu ID de usuario de Telegram.

## Quítalo

- En una Machine alojada: pulsa **Desconectar Telegram** en tu página de configuración. Tu bot y su token se quitan de tu servidor.
- En tu propio ordenador: `assistant telegram off`. Añade `--remove-bot` para olvidar también el bot.

## Elimina el bot en Telegram

Escribe a @BotFather, envía /deletebot y elige tu bot.
