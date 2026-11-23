---
title: X
area: connections
summary: Tus menciones, respuestas y mensajes directos de X, leídos en el navegador de tu Machine. Solo envía mensajes cuando das tu visto bueno.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: e8997ab6eb32523f
---
## Qué lee

Tus menciones, respuestas y mensajes directos de X en el navegador de tu Machine, con tu sesión iniciada. No marca nada como leído y no puede leer los mensajes cifrados de X Chat.

## Qué puede enviar

Una respuesta o un mensaje directo, y solo después de que lo apruebes en la tarea.

X está migrando las cuentas a una nueva aplicación web. Si la tuya ya la tiene, tu Machine todavía no puede enviar respuestas, así que la respuesta que apruebes se detendrá antes de publicarse y te avisará. Los mensajes directos se siguen enviando.

Esto no se hace a través de la API oficial de X. Es muy poco probable que leer y enviar alguna respuesta que hayas aprobado ocasionalmente cause problemas; los envíos masivos o automatizados pueden hacer que bloqueen una cuenta.

## Conectarla

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre X, escribe tu nombre de usuario sin la @ e inicia sesión en X en el navegador de tu Machine cuando te lo pida. Después, pulsa **Conectar**.

En tu propio ordenador:

1. En el panel, abre **Conexiones**, después **Chat** y selecciona X.
2. Elige **Trabajo** si es para tu empresa, o **Personal**. Escribe tu nombre de usuario sin la @ y pulsa **Conectar**.
3. Pulsa Iniciar sesión en X e inicia sesión en el navegador de tu Machine. Se conectará automáticamente cuando hayas iniciado sesión.

O ejecuta `assistant connect x` en un terminal.

Si X cierra la sesión de tu Machine, consulta [Se cerró la sesión en un sitio](signed-out.md).

## Desconectarla

- En el panel: abre **Conexiones**, selecciona X, ve a **Detalles** y pulsa **Desconectar**. Dejará de leer. Lo que ya haya importado se conservará.
- En una Machine alojada, también puedes pulsar **Quitar** junto a X en tu página de configuración.

## Cerrar la sesión en X

En X, abre Ajustes, Seguridad y acceso a la cuenta, Aplicaciones y sesiones, Sesiones, y cierra la sesión del navegador de tu Machine.
