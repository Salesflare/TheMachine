---
title: Conectar otras IA
area: connections
summary: Deja que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y tu Graph por MCP, cada una con su acceso y su caducidad.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Qué puede hacer otra IA

Otras IA pueden conectarse a tu Machine por MCP: Claude, ChatGPT, Cursor, Codex, GBrain y más. Pueden leer tus tareas, promesas, resúmenes del equipo y las personas y empresas de tu Graph.

Con **Leer y editar** también pueden añadir una tarea, o una tarea con un borrador de correo, y cambiar tu Graph: guardar un dato sobre una persona o empresa, corregir sus detalles, campos y etiquetas, o añadir una línea al resumen de una persona.

Cada cambio aparece en **Actividad** con **Deshacer**. Nunca fusionan, eliminan ni comparten fichas. Lo que guardan muestra **IA:** y su nombre, en su área. Puedes editarlo o quitarlo, y The Machine puede reescribir una línea del resumen más adelante. Tu Machine lo trata como lo que dice esa IA, nunca como una instrucción tuya.

Un borrador espera en tu Machine hasta que lo leas y pulses **Enviar** tú. Una IA conectada nunca envía nada ni actúa por ti. Do it y los agentes de tu Machine no forman parte de esto.

## Conectar una

Abre **Ajustes**, **IA**. Arriba está la dirección de tu Machine para las IA, `https://<tu nombre>.mcp.themachine.computer/mcp`, con **Copiar**. En una Machine en tu propio ordenador, pulsa primero **Obtener tu dirección**. Se abre una página de tu cuenta: comprueba que muestra el mismo código, confirma y elige un nombre. Tu Machine se vincula sola, sin reiniciar.

Después obtiene su propio certificado para la dirección. Tarda unos minutos y necesita el paquete `cryptography` para Python.

En ChatGPT, abre chatgpt.com/plugins, pulsa + y luego Add custom MCP server. Llámalo The Machine, pega la dirección y elige OAuth. Confirma el aviso y pulsa Create as a plugin. Tu plan o espacio de trabajo tiene que permitir servidores MCP personalizados.

En Claude, abre Customize, Connectors, pulsa + Add y luego Add custom connector. Llámalo The Machine, pega la dirección, pulsa Continue y luego Add. En Team y Enterprise, un propietario lo añade en Organization settings.

Las IA de un dispositivo en tu tailnet, como Claude Code o Cursor, también pueden usar la dirección de tu panel seguida de `/mcp`. **Desvincular** quita de tu cuenta una Machine en tu propio ordenador.

La IA te lleva a tu Machine para iniciar sesión. Tu Machine muestra qué IA es. Una IA que no reconoce muestra la dirección de la que viene: conecta solo si acabas de iniciarlo tú.

Elige qué puede hacer, **Leer** o **Leer y editar**. Con cuentas de trabajo y personales, elige también qué puede ver. Luego elige por cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar**, o **Cancelar** para devolverla sin nada.

## Qué ve

Una conexión solo ve su área. Trabajo cubre las tareas y promesas de tus cuentas de trabajo, contactos de trabajo, empresas, proyectos y el resumen del equipo de tu Work Fleet. Personal cubre el resto. El texto de los mensajes se queda en tu Machine: una IA ve las fuentes de una tarea solo por remitente, asunto y fecha.

Los datos de Team Graph de tus compañeros nunca van a una IA de fuera.

## En Ajustes

Abre **Ajustes**, **IA** para ver cada IA conectada, con su último uso y cuántas llamadas hizo. Cambia ahí su acceso, su área o la duración. La siguiente llamada ya lo usa. **Desactivar ahora** cierra todas sus sesiones a la vez. **Actividad** muestra cada llamada, también las rechazadas. **Quitar** la elimina.

Una IA que no puede iniciar sesión sola puede usar una clave. En **Añadir una clave**, ponle nombre, elige el acceso y la duración y pulsa **Crear clave**. Copia la clave enseguida: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Seguridad

Cada llamada queda registrada, también las rechazadas. Una conexión caducada o desactivada se rechaza hasta que la cambies. El inicio de sesión usa OAuth con PKCE. Tu Machine guarda solo una huella de cada token, así que una copia de sus datos no abre nada.
