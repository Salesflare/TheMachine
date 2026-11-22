---
title: Conectar otras IA
area: connections
summary: Deja que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y tu Graph. Con **Leer y editar**, también podrán hacer cambios que puedes deshacer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## Qué puede hacer otra IA

Claude, ChatGPT, Cursor, Codex, GBrain y otras IA pueden conectarse a tu Machine. Pueden leer tus tareas, promesas, resúmenes del equipo y las personas y empresas de tu Graph.

Con **Leer y editar**, también pueden añadir una tarea o un borrador de correo, y actualizar tu Graph: guardar un dato, corregir detalles, campos y etiquetas, o añadir una línea al resumen de una persona.

Cada cambio aparece en **Actividad**, con la opción de **Deshacer**. Nunca fusionan, eliminan ni comparten registros. Lo que guardan aparece marcado como **AI:** junto con su nombre, y tu Machine lo considera una afirmación suya, nunca una instrucción tuya.

Un borrador espera hasta que lo leas y pulses **Enviar**. Una IA conectada nunca envía nada ni actúa en tu nombre.

## Conectar una IA

Abre **Ajustes**, **Apps**. Debajo de **Las apps de The Machine** están **Añadir en ChatGPT** y **Añadir en Claude**. En **O añádela con una dirección** encontrarás la dirección de la app oficial, `https://mcp.themachine.computer/mcp`, que sirve para todas las Machines, y **Tu dirección**, `https://<your name>.mcp.themachine.computer/mcp`. Ambas tienen la opción **Copiar**.

Si tienes una Machine en tu propio ordenador, pulsa primero **Configurar**, debajo de **Consigue tu dirección**. Se abrirá una página de tu cuenta: comprueba que aparece el mismo código, confírmalo y elige un nombre. Tu Machine se vinculará automáticamente, sin reiniciarse. Este paso es necesario en ambos casos.

Después, tu Machine configurará automáticamente su dirección segura. Tardará unos minutos.

Para Claude, pulsa **Añadir en Claude** o abre [The Machine en el directorio de Claude](https://claude.ai/directory/the-machine) y pulsa **Conectar**. En los planes Team y Enterprise, un propietario debe añadirla en los ajustes de la organización.

Si prefieres usar una dirección en Claude, abre Customize, Connectors, pulsa + Add y luego Add custom connector. Ponle el nombre The Machine, pega la dirección, pulsa Continue y luego Add.

Para ChatGPT, pulsa **Añadir en ChatGPT** o abre [The Machine en ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) y pulsa Install plugin. En los planes Business y Enterprise, puede que un administrador tenga que permitirla primero.

La app oficial se conecta a una Machine alojada y también a una Machine en tu propio ordenador, una vez que tenga su dirección.

Para usar tu dirección privada o una Machine que no esté en The Machine Network, añade un servidor MCP personalizado en ChatGPT: abre chatgpt.com/plugins, pulsa + y luego Add custom MCP server. Ponle el nombre The Machine, pega la dirección y elige OAuth. Confirma el aviso y pulsa Create as a plugin. Tu plan o espacio de trabajo debe permitir servidores MCP personalizados.

Con la app oficial, la IA te pedirá que inicies sesión con tu cuenta de The Machine. Si tienes más de una Machine, elige esta y aprueba la conexión en la página de tu Machine. Con la dirección privada, la IA se conecta directamente a tu Machine.

Las IA que estén en un dispositivo de tu red privada (Tailscale), como Claude Code o Cursor, también pueden usar la dirección de tu panel seguida de `/mcp`. La opción **Desvincular esta Machine**, al final de **Ajustes**, **Cuenta**, quita de tu cuenta una Machine de tu propio ordenador.

Tu Machine te muestra qué IA solicita la conexión. Si no puede identificarla, te muestra de dónde viene la solicitud: conéctala solo si acabas de iniciar el proceso tú.

Elige qué puede hacer: **Leer** o **Leer y editar**. Si tienes cuentas de Trabajo y Personal, elige qué puede ver. Después, elige cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar** o **Cancelar** para rechazar la conexión.

## App oficial o dirección privada

La app oficial es la opción más sencilla: una dirección para todos y tu cuenta encuentra tu Machine. Nuestra nube retransmite las solicitudes y no guarda nada.

Con tu dirección privada, todo se cifra hasta llegar a tu Machine. La nube solo lo retransmite y no puede leerlo.

En ambos casos, quien decide es tu Machine. Solo puede entrar una IA que hayas aprobado en su página, con el acceso que hayas elegido. En **Ajustes**, **Apps**, las IA que se conectan mediante la app oficial muestran **App oficial**.

## Qué puede ver

Cada conexión solo ve su área. Trabajo incluye las tareas y promesas de tus cuentas de trabajo, las personas, empresas y proyectos del trabajo, y el resumen del equipo de tu Fleet de trabajo. Personal incluye todo lo demás. El texto de los mensajes se queda en tu Machine, a menos que actives **Mensajes**. Si no lo haces, una IA solo verá el remitente, el asunto y la fecha de las fuentes de una tarea.

Los registros del Graph del equipo de tus compañeros nunca se comparten con una IA externa.

## Mensajes

**Mensajes** permite que una IA busque y lea tu correo y tus chats de Slack, WhatsApp y otros servicios. Está desactivado hasta que lo actives, ya sea en la página donde conectas la IA o después en **Ajustes**, **Apps**. Solo permite leer: nunca envía, elimina ni marca nada.

Solo lee mensajes de su área. Algunos mensajes nunca se comparten: códigos de un solo uso y enlaces para iniciar sesión, mensajes de un tablero o proyecto marcado como **Solo tú**, conversaciones que The Machine ha considerado sensibles (negocios, RR. HH., asuntos legales, salud o dinero), conversaciones que mantuviste privadas y mensajes eliminados.

Cada lectura aparece en **Actividad**, con el número de mensajes y las conversaciones consultadas, nunca con su texto. Tu Machine entrega el texto marcado como datos, así que la IA no debería seguir las instrucciones escritas en un mensaje.

Mientras **Mensajes** esté activado, los cambios de una IA con **Leer y editar** en tu Graph esperan a que los apruebes. Pulsa **Aplicar** o **Descartar** en el cambio, en **Actividad**.

## En Ajustes

Abre **Ajustes**, **Apps** para ver cada IA que se ha conectado, una sola vez, junto con su acceso, área, fecha de finalización y último uso. Puedes activar o desactivar **Mensajes** desde ahí. Pulsa **Cambiar** para cambiar el acceso, el área o la duración. El siguiente acceso usará los nuevos ajustes. **Actividad** muestra cada solicitud, también las rechazadas. **Desactivar ahora** la pausa: se cierran todas sus sesiones, pero se conserva su historial. **Quitar** la elimina junto con su historial.

Si vuelves a iniciar sesión en la misma IA, la nueva aprobación sustituye a la anterior.

Una IA que no pueda iniciar sesión por sí sola puede usar una clave. En **Añadir una clave**, ponle un nombre, elige el acceso y la duración, y pulsa **Crear clave**. Copia la clave enseguida: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Mantén la seguridad

Se registran todas las solicitudes, también las rechazadas. Si una conexión ha caducado o está desactivada, se rechaza hasta que la cambies. Tu Machine solo guarda una huella digital de cada inicio de sesión, así que una copia de sus datos no permite acceder a nada.
