---
title: Microsoft Teams
area: connections
summary: Chats de Teams, chats de reuniones y notas de reuniones para cuentas profesionales o educativas. Solo responde cuando lo apruebas.
covers: connector:teams
code: connectors/teams.py, teams_send.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 9ca0bb08466b4d58
---
## Qué lee

Tus chats individuales, grupales y de reuniones en Teams: los últimos 7 días al conectarlo y, después, los mensajes nuevos cada pocos minutos. Más adelante, se importa poco a poco y sin interrumpir nada el historial de chats de aproximadamente un año y de hilos de canales, con el visto bueno de tu administrador, como [historial](history.md).

Con el visto bueno de tu administrador, también lee:

- Hilos de canales de tus equipos.
- Transcripciones de las reuniones que organizaste.
- Notas de reuniones y tareas de Copilot, si tienes una licencia de Microsoft 365 Copilot.

Cada transcripción o conjunto de notas aparece en la reunión correspondiente de tu Calendario, con la etiqueta **De Teams**. Si no hay transcripción ni notas, el chat de la reunión sigue disponible.

No se incluyen bots, aplicaciones ni mensajes del sistema.

## Qué puede hacer

Responder en un chat individual, grupal o de reunión del que surgió una tarea. The Machine redacta la respuesta, que solo se envía después de que la revises y pulses **Enviar ahora**. La envía como si fueras tú, en ese chat. Nunca inicia un chat nuevo.

No publica en canales. Para responder en un hilo de un canal, ábrelo con **Abrir en Teams**.

## Qué permisos solicita

Microsoft solicita permiso para que The Machine lea tus chats y tu perfil, y envíe mensajes de chat como si fueras tú. No hace falta la aprobación de un administrador.

Si conectaste Teams antes de que pudiera enviar mensajes, en su tarjeta aparecerá **Vuelve a conectar para enviar respuestas.** Pulsa **Reconectar** y vuelve a dar tu aprobación. Mientras tanto, el borrador queda disponible para que lo envíes desde Teams.

Tu administrador debe aprobar una sola vez el acceso a los canales, las transcripciones y las notas de Copilot. Hasta entonces, la tarjeta de Teams indica qué no puede leer todavía y por qué.

Solo funciona con una cuenta profesional o educativa de Microsoft. Las cuentas personales no tienen chats de Teams que se puedan leer de esta forma.

## Conectarlo

En una Machine alojada:

1. En el panel, abre **Conexiones** y luego **Chat** para **Microsoft Teams** o **Reuniones** para **Reuniones de Teams**. Ambas opciones usan el mismo inicio de sesión.
2. Pulsa **Iniciar sesión con Microsoft** y da tu aprobación. Volverás al panel.
3. Para habilitar los canales y las notas de reuniones, envíale a tu administrador el enlace que aparece en la página de inicio de sesión. Cuando lo apruebe, vuelve a conectar Teams.

Durante la configuración, también aparece **Conectar Microsoft Teams** en la página de configuración.

En tu propio ordenador, cuando esté [vinculada a tu cuenta](friends.md#a-machine-on-your-own-computer): abre **Conexiones** y luego **Chat** o **Reuniones**. Elige **Microsoft Teams** o **Reuniones de Teams** y pulsa **Iniciar sesión con Microsoft**. Allí lee tus chats y los chats de reuniones. Los canales y las notas de reuniones aún no están disponibles.

## Quitar la conexión

En el panel, abre **Conexiones**, selecciona Microsoft Teams y pulsa **Detalles** y luego **Desconectar**. Lo que ya se haya importado se conserva.

## Revocar el acceso en Microsoft

Abre myapps.microsoft.com y quita The Machine. Si Outlook está conectado con la misma dirección, también se desconectará.
