---
title: X
area: connections
summary: Tus menciones, respuestas y mensajes directos en X, leídos en el navegador propio de tu Machine. Solo envía después de que lo apruebes.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
---
## Qué lee

Tus menciones, respuestas y mensajes directos en X. Los lee en el navegador propio de tu Machine, con tu sesión iniciada. No usa la API para desarrolladores de X, no marca nada como visto y no puede leer el X Chat cifrado.

## Qué puede enviar

Una respuesta o un mensaje directo, y solo después de que lo apruebes en la tarea.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre X, escribe tu usuario sin la @, inicia sesión en X en el navegador de tu Machine cuando te lo pida y luego pulsa **Conectar**.

En tu propio ordenador:

1. Inicia sesión en X una vez en el navegador de tu Machine (Ajustes, **Abrir el navegador de la Machine ↗**).
2. En el panel, abre **Conexiones**, luego **+ Añadir**, y elige X. O ejecuta `assistant connect x`.
3. Escribe tu usuario, y el usuario con el que el navegador suele tener la sesión iniciada.

Si X cierra la sesión de tu Machine, consulta [Sesión cerrada en un sitio](signed-out.md).

## Quítalo

- En el panel: **Conexiones**, abre X, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Cierra su sesión en X

En X, abre Settings, Security and account access, Apps and sessions, Sessions, y cierra la sesión del navegador de tu Machine.
