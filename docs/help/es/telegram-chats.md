---
title: Chats de Telegram
area: connections
summary: Tus chats y grupos pequeños de Telegram, leídos como si fueran un dispositivo de tu propia cuenta. Solo se envían respuestas cuando las apruebas.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
translated: da17aef29a380002
---
## Qué lee

Tus chats privados y grupos de hasta 50 personas, como si fuera un dispositivo con la sesión iniciada en tu propia cuenta de Telegram, igual que Telegram Desktop. Al conectarlo, lee los últimos 7 días y, a partir de ahí, los mensajes nuevos.

Nunca lee canales, bots, Mensajes guardados ni mensajes de servicio de Telegram. También omite los chats silenciados y archivados.

No modifica tu estado de lectura ni tu estado en línea: no marca nada como leído y tu móvil sigue mostrando los mensajes nuevos como nuevos.

Esto es independiente de [Telegram](telegram.md), donde tu propio bot te envía tus tareas.

## Qué puede enviar

Un mensaje de texto en un chat que ya existe, solo después de que lo apruebes en la tarea. Los mensajes se envían de uno en uno, con una pausa entre ellos.

Si recibes una tarea por correo, pero hablas con esa persona por Telegram, dilo en el chat de la tarea. The Machine encuentra el chat que ya tienes con esa persona y cambia el borrador a Telegram para que lo revises y lo envíes. Nunca inicia un chat nuevo.

## Conectarlo

1. En el panel, abre **Conexiones** y luego **Chat**. Después, elige los chats de Telegram.
2. Elige **Escanear un código QR con Telegram en otro dispositivo**.
3. En tu móvil, abre Ajustes y Dispositivos en Telegram. Toca **Vincular dispositivo de escritorio** y escanea el código.
4. Si tu cuenta tiene una contraseña en la nube, escríbela cuando te la pidan. Se envía a Telegram y nunca se guarda.

En un móvil, el formulario muestra primero **Consigue un código para tu número de teléfono**, ya que no puedes escanear un código QR desde la misma pantalla. Indica dónde envió Telegram el código: a tu app de Telegram en otro dispositivo, por SMS o a tu correo de inicio de sesión. ¿No tienes el código? Pulsa **Enviar el código otra vez**.

En tu propio ordenador también necesitas un ID de app de Telegram propio. Créalo en [my.telegram.org](https://my.telegram.org), en API development tools, y escribe su api_id y api_hash en el formulario.

También puedes ejecutar `assistant connect telegram` en un terminal y escanear el código que aparece.

## Si deja de funcionar

- **Sesión de Telegram cerrada**: Telegram cerró la sesión de este dispositivo o la cerraste desde tu móvil. Pulsa **Reconectar** en **Conexiones**.
- **Telegram ya no acepta el ID de app**: Telegram ya no acepta el ID de app que usa esta Machine. No se lee ni se envía nada hasta que pulses **Reconectar** y añadas un ID de app propio.

Telegram puede limitar o cerrar las sesiones de apps como The Machine.

## Fotos

The Machine pide a Telegram las fotos de perfil de las personas de tu Graph que no tienen una, como máximo 50 al día. Lo hace con la misma sesión que usa para leer tus chats y solo para las personas de los chats que lee. No les envía nada. Si alguien oculta su foto para ti, seguirá sin tenerla.

## Desconectarlo

Abre los chats de Telegram en **Conexiones**, toca **Detalles** y luego **Desconectar**. Tu Machine cierra su sesión en Telegram y elimina los datos de Telegram que había guardado.

También puedes cerrarla desde tu móvil: abre Ajustes y Dispositivos en Telegram, toca The Machine y cierra la sesión.
