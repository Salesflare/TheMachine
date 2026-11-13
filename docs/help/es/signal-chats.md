---
title: Chats de Signal
area: connections
summary: Tus chats y grupos de Signal, leídos como un dispositivo vinculado a tu teléfono. Responde solo después de que lo apruebes.
covers: connector:signal
code: onboarding.py, signal_setup.py, signal_mirror.py, signal_store.py, signal_send.py
keywords: Signal, linked device, QR code
---
## Qué lee

Tus chats y grupos, como un dispositivo vinculado a tu teléfono, igual que Signal Desktop. Signal no da mensajes anteriores a un dispositivo recién vinculado, así que lee desde el momento en que lo vinculas.

Las fotos, notas de voz y archivos aparecen como lo que son ("Envió una foto"), nunca con su contenido. Los archivos de visualización única no guardan contenido. Las ediciones y eliminaciones siguen lo que pasó en tu teléfono, y los mensajes temporales se van de tu Machine cuando se acaba su tiempo.

Se omiten las historias, reacciones, llamadas y Notas personales. No se marca nada como leído.

## Qué puede enviar

Un texto en un chat que ya existe, solo después de que lo apruebes en la tarea. Una respuesta cita el mensaje al que responde cuando ayuda. Los envíos salen de uno en uno, con una pausa entre ellos.

Si una tarea llegó por email pero hablas con esa persona por Signal, dilo en el chat de la tarea. The Machine encuentra tu chat existente con ella y pasa el borrador a Signal, para que lo revises y lo envíes. Nunca empieza un chat nuevo.

## Conéctalo

1. En el panel, abre **Conexiones**, luego **Chat**, y elige Chats de Signal.
2. En tu teléfono, en Signal, abre Ajustes, **Dispositivos vinculados**, **Vincular nuevo dispositivo**, y escanea el código.

Necesitas una segunda pantalla desde la que escanear: Signal solo vincula un dispositivo con un código QR. O ejecuta `assistant connect signal` en una terminal y escanea el código que muestra.

Tu Machine guarda las claves del dispositivo vinculado consigo. Nunca salen de ella.

## Cuando se detiene

Usa signal-cli, un cliente de Signal no oficial. Tu Machine descarga una versión fijada y comprueba su suma de verificación antes de ejecutarla. Signal puede dejar de aceptarlo en cualquier momento.

- **Signal desvinculó esta Machine**: la quitaste en tu teléfono, o Signal terminó la vinculación. Toca **Reconectar** en **Conexiones** y escanea un código nuevo.
- **Actualiza The Machine para Signal**: Signal ya no acepta el cliente de Signal de esta Machine. Actualiza The Machine.

## Quítalo

**Conexiones**, abre Chats de Signal, **Detalles** y luego **Desconectar**. Tu Machine elimina las claves y lo que guardaba para Signal. Después quítala también en tu teléfono: Signal, Ajustes, **Dispositivos vinculados**, toca The Machine y desvincúlala.
