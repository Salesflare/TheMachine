---
title: Telegram
area: connections
summary: Recibe tus tareas en Telegram con un bot propio y los mismos botones que en el panel. Es opcional.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## Qué hace

Recibe tus tareas en Telegram desde un bot propio, dentro de tu [Horario laboral](work-hours.md). Cada tarea incluye los botones del panel: **Hazlo**, **Posponer**, **Pedir cambios**, **Marcar como hecho**, **No hace falta** y **Enviar** para mandar un mensaje preparado. Si quieres que The Machine lea tus chats de Telegram, consulta [Chats de Telegram](telegram-chats.md).

Es opcional: la app para móvil envía las mismas tareas como notificaciones.

## Qué puede enviar

Solo mensajes dirigidos a ti desde tu propio bot. Para enviar un mensaje a otra persona, necesitas dar tu visto bueno en la tarea.

## Conectarlo

En una Machine alojada:

1. En Telegram, escribe a @BotFather y envía /newbot. Copia el token que te dé.
2. En tu página de configuración, en **Añadir más cuando quieras**, abre Telegram, pega el token y pulsa **Añadir mi bot**.

Puedes añadirlo cuando quieras.

En tu propio ordenador, el instalador te lo pedirá. También puedes ejecutar `assistant telegram on` con tu ID de usuario de Telegram.

## Quitar la conexión

- En una Machine alojada: pulsa **Desconectar Telegram** en tu página de configuración. El bot y su token se eliminan de tu Machine.
- En tu propio ordenador: `assistant telegram off`. Añade `--remove-bot` para olvidar también el bot.

## Eliminar el bot en Telegram

Escribe a @BotFather, envía /deletebot y selecciona tu bot.
