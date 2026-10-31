---
title: Conectar otras IA
area: connections
summary: Deja que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y tu Graph por MCP, cada una con su acceso y su caducidad.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Qué puede hacer otra IA

Otras IA pueden conectarse a tu Machine por MCP: Claude, ChatGPT, Cursor, Codex, GBrain y más. Pueden leer tus tareas, promesas, resúmenes del equipo y las personas y empresas de tu Graph.

Como mucho añaden una tarea, o una tarea con un borrador de correo. Un borrador espera en tu Machine hasta que lo leas y pulses **Enviar** tú. Una IA conectada nunca envía nada ni actúa por ti. Do it y los agentes de tu Machine no forman parte de esto.

## Conectar una

En la otra IA, añade un conector personalizado o un servidor MCP con la dirección de tu Machine seguida de `/mcp`. En una Machine alojada es `https://<tu nombre>.app.themachine.computer/mcp`. En una Machine en tu propio ordenador es la dirección de tu panel, a la que solo llegan los dispositivos de tu tailnet.

La IA te lleva a tu Machine para iniciar sesión. Tu Machine muestra qué IA es. Una IA que no reconoce muestra la dirección de la que viene: conecta solo si acabas de iniciarlo tú.

Elige qué puede hacer, **Leer** o **Leer y borradores**. Con cuentas de trabajo y personales, elige también qué puede ver. Luego elige por cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar**, o **Cancelar** para devolverla sin nada.

## Qué ve

Una conexión solo ve su área. Trabajo cubre las tareas y promesas de tus cuentas de trabajo, contactos de trabajo, empresas, proyectos y el resumen del equipo de tu Work Fleet. Personal cubre el resto. El texto de los mensajes se queda en tu Machine: una IA ve las fuentes de una tarea solo por remitente, asunto y fecha.

Los datos de Team Graph de tus compañeros nunca van a una IA de fuera.

## En Ajustes

Abre **Ajustes**, **IA** para ver cada IA conectada, con su último uso y cuántas llamadas hizo. Cambia ahí su acceso, su área o la duración. La siguiente llamada ya lo usa. **Desactivar ahora** cierra todas sus sesiones a la vez. **Actividad** muestra cada llamada, también las rechazadas. **Quitar** la elimina.

Una IA que no puede iniciar sesión sola puede usar una clave. En **Añadir una clave**, ponle nombre, elige el acceso y la duración y pulsa **Crear clave**. Copia la clave enseguida: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Seguridad

Cada llamada queda registrada, también las rechazadas. Una conexión caducada o desactivada se rechaza hasta que la cambies. El inicio de sesión usa OAuth con PKCE. Tu Machine guarda solo una huella de cada token, así que una copia de sus datos no abre nada.
