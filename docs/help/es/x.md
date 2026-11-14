---
title: X
area: connections
summary: Tus menciones, respuestas y mensajes directos en X, leídos en el navegador propio de tu Machine. Solo los envía cuando los apruebas.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## Qué lee

Tus menciones, respuestas y mensajes directos en X, en el navegador de tu Machine con tu sesión iniciada. No marca nada como leído y no puede leer los mensajes cifrados de X Chat.

## Qué puede enviar

Una respuesta o un mensaje directo, y solo después de que lo apruebes en la tarea.

Esto no pasa por la API oficial de X. Es muy poco probable que leer y enviar alguna respuesta que hayas aprobado cause problemas; el envío masivo o automatizado puede hacer que bloqueen una cuenta.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre X, escribe tu nombre de usuario sin la @, inicia sesión en X desde el navegador de tu Machine cuando te lo pida y pulsa **Conectar**.

En tu propio equipo:

1. En el panel, abre **Conexiones**, luego **Chat** y elige X.
2. Elige **Trabajo** con su empresa o **Personal**, escribe tu nombre de usuario sin la @ y pulsa **Conectar**.
3. Pulsa **Iniciar sesión en X** e inicia sesión en el navegador de tu Machine. Se conectará automáticamente cuando hayas iniciado sesión.

También puedes ejecutar `assistant connect x` en una terminal.

Si X cierra la sesión de tu Machine, consulta [Cierre de sesión en un sitio](signed-out.md).

## Quítalo

- En el panel: abre **Conexiones**, abre X, pulsa **Detalles** y luego **Desconectar**. Dejará de leer. Lo que ya haya importado se queda.
- En una Machine alojada, también puedes pulsar **Quitar** junto a X en tu página de configuración.

## Cierra la sesión desde X

En X, abre **Ajustes**, **Seguridad y acceso a la cuenta**, **Aplicaciones y sesiones**, **Sesiones** y cierra la sesión del navegador de tu Machine.
