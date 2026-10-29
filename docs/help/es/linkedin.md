---
title: LinkedIn
area: connections
summary: Tus mensajes de LinkedIn, leídos en el navegador propio de tu Machine con tu sesión iniciada. Solo responde después de que lo apruebes.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py
site: Connect, More sources, Remove
---
## Qué lee

Tus mensajes de LinkedIn. Los lee en una pestaña del navegador propio de tu Machine, con tu sesión iniciada, de vez en cuando durante el día. No usa ninguna clave de API y no marca nada como leído.

## Qué puede enviar

Una respuesta a un mensaje, y solo después de que la apruebes en la tarea. Hasta entonces solo redacta.

## Conéctalo

En una Machine alojada:

1. Abre tu página de configuración en app.themachine.computer/setup y ve a **Más fuentes**.
2. Abre LinkedIn, inicia sesión en LinkedIn en el navegador de tu Machine cuando te lo pida y luego pulsa **Conectar**.

En tu propio ordenador:

1. Inicia sesión en LinkedIn una vez en el navegador de tu Machine (Ajustes, **Abrir el navegador de la Machine ↗**).
2. En el panel, abre **Conexiones**, luego **+ Añadir**, y elige LinkedIn. O ejecuta `assistant connect linkedin`.

Una segunda cuenta de LinkedIn tiene su propio navegador. Si LinkedIn cierra la sesión de tu Machine, consulta [Sesión cerrada en un sitio](signed-out.md).

## Si LinkedIn pide un código

La primera vez que tu Machine inicia sesión, LinkedIn suele enviar un código por correo. Escríbelo en la ventana de inicio de sesión, en **Código**, y pulsa **Iniciar sesión**. La página no se mueve mientras escribes.

Si LinkedIn vuelve al principio, o no pasa nada en dos minutos, LinkedIn detuvo este inicio de sesión. Espera un minuto y pulsa **Reintentar**. Si LinkedIn muestra una comprobación de robot, termínala en el navegador de tu Machine.

## Quítalo

- En el panel: **Conexiones**, abre LinkedIn, **Detalles** y luego **Desconectar**. Deja de leer. Lo que ya trajo se queda.
- En una Machine alojada también puedes pulsar **Quitar** junto a él en tu página de configuración.

## Cierra su sesión en LinkedIn

En LinkedIn, abre Settings, Sign in and security, Where you're signed in, y cierra la sesión del navegador de tu Machine.
