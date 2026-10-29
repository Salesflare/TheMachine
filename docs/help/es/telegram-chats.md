---
title: Chats de Telegram
area: connections
summary: Tus chats y grupos pequeños de Telegram, leídos como un dispositivo de tu propia cuenta. Responde solo después de que lo apruebes.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## Qué lee

Tus chats privados y grupos de hasta 50 personas, como un dispositivo con sesión iniciada en tu propia cuenta de Telegram, igual que Telegram Desktop. Al conectarlo lee los últimos 7 días y luego lo que va llegando.

Nunca lee canales, bots, Mensajes guardados ni los mensajes de servicio del propio Telegram. Los chats silenciados y archivados también se omiten.

No toca tu estado de leído ni de en línea: nada se marca como leído y tu teléfono sigue mostrando los mensajes nuevos como nuevos.

Esto es aparte de [Telegram](telegram.md), donde tu propio bot te envía tus tareas.

## Qué puede enviar

Un texto en un chat que ya existe, solo después de que lo apruebes en la tarea. Los envíos salen de uno en uno, con una pausa entre ellos.

Si una tarea llegó por correo pero con esa persona hablas por Telegram, dilo en el chat de la tarea. The Machine encuentra tu chat con ella y pasa el borrador a Telegram, para que lo revises y lo envíes. Nunca empieza un chat nuevo.

## Conéctalo

1. En el panel, abre **Conexiones**, luego **+ Añadir**, y elige Chats de Telegram.
2. Elige **Escanear un código QR en Telegram en tu teléfono**.
3. En tu teléfono, en Telegram, abre Ajustes, Dispositivos, **Link Desktop Device**, y escanea el código.
4. Si tu cuenta tiene una contraseña en la nube, escríbela cuando te la pida. Va a Telegram y nunca se guarda.

¿Lo configuras en el teléfono, sin una segunda pantalla desde la que escanear? Elige **Recibir un código en Telegram para tu número de teléfono**. El formulario dice adónde envió Telegram el código: a tu app de Telegram en otro dispositivo, por SMS o a tu correo de inicio de sesión. ¿No llega? Pulsa **Enviar el código otra vez**.

En tu propio ordenador también necesitas un ID de app de Telegram propio. Créalo en [my.telegram.org](https://my.telegram.org), en API development tools, y rellena su api_id y su api_hash en el formulario.

O ejecuta `assistant connect telegram` en un terminal y escanea el código que muestra ahí.

## Cuando se detiene

- **Sesión de Telegram cerrada**: Telegram terminó la sesión de este dispositivo, o la cerraste en tu teléfono. Pulsa **Reconectar** en su tarjeta.
- **Telegram ya no acepta el ID de app**: Telegram ya no acepta el ID de app que usa esta Machine. No se lee ni se envía nada hasta que pulses **Reconectar** y añadas un ID de app propio.

The Machine usa la API de Telegram para esto. Telegram puede limitar o terminar las sesiones de apps como ella.

## Quítalo

**Conexiones**, abre Chats de Telegram, **Detalles** y luego **Desconectar**. Tu Machine cierra su sesión en Telegram y elimina lo que guardaba para Telegram.

O termínalo en tu teléfono: en Telegram, abre Ajustes, Dispositivos, toca The Machine y termina la sesión.
