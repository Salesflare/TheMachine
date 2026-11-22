---
title: Conecta otras IA
area: connections
summary: Deja que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y tu Graph. Con **Leer y editar**, también pueden hacer cambios que puedes deshacer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## Qué puede hacer otra IA

Claude, ChatGPT, Cursor, Codex, GBrain y otras IA pueden conectarse a tu Machine. Pueden leer tus tareas, promesas, resúmenes del equipo y las personas y empresas de tu Graph.

Con **Leer y editar**, también pueden añadir una tarea o un borrador de correo y actualizar tu Graph: guardar un dato, corregir detalles, campos y etiquetas, o añadir una línea al resumen de una persona.

Cada cambio aparece en **Actividad**, con la opción **Deshacer**. Nunca combinan, eliminan ni comparten registros. Lo que guardan lleva la marca **AI:** y su nombre, y tu Machine lo considera una afirmación suya, nunca una instrucción tuya.

Los borradores esperan hasta que los leas y pulses Enviar. Una IA conectada nunca envía nada ni actúa en tu nombre.

## Conecta una IA

Abre **Ajustes**, **Apps**. Debajo de **Las apps de The Machine** encontrarás **Añadir en ChatGPT** y **Añadir en Claude**. En **O añádela con una dirección** aparecen la dirección única de la app oficial para todas las Machine, `https://mcp.themachine.computer/mcp`, y **Tu dirección**, `https://<your name>.mcp.themachine.computer/mcp`, cada una con la opción **Copiar**.

Si tienes una Machine en tu propio ordenador, pulsa primero **Configurar**, debajo de **Consigue tu dirección**. Se abrirá una página de tu cuenta: comprueba que muestre el mismo código, confírmalo y elige un nombre. Tu Machine se vincula automáticamente, sin reiniciarse. Esto es necesario en ambos casos.

Tu Machine configurará automáticamente su dirección segura. Tardará unos minutos.

Para Claude, pulsa **Añadir en Claude** o abre [The Machine en el directorio de Claude](https://claude.ai/directory/the-machine) y pulsa Conectar. En los planes Team y Enterprise, alguien con permisos de propietario debe añadirla en los ajustes de la organización.

Si prefieres usar una dirección en Claude, abre Customize, Connectors, pulsa + Add y, después, Add custom connector. Ponle el nombre The Machine, pega la dirección, pulsa Continue y, después, Add.

Para ChatGPT, pulsa **Añadir en ChatGPT** o abre [The Machine en ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) y pulsa Install plugin. En los planes Business y Enterprise, puede que primero tenga que habilitarla una persona administradora.

La app oficial se conecta a una Machine alojada y también a una Machine en tu propio ordenador, una vez que tenga su dirección.

Para usar tu dirección privada o conectar una Machine que no esté en la Network, añade un servidor MCP personalizado en ChatGPT: abre chatgpt.com/plugins, pulsa + y, después, Add custom MCP server. Ponle el nombre The Machine, pega la dirección y elige OAuth. Confirma la advertencia y pulsa Create as a plugin. Tu plan o espacio de trabajo debe permitir servidores MCP personalizados.

Con la app oficial, la IA te pedirá que inicies sesión con tu cuenta de The Machine. Si tienes más de una Machine, elige cuál quieres usar y apruébalo en la página de tu Machine. Con la dirección privada, la IA se conecta directamente a tu Machine.

Las IA de un dispositivo en tu red privada (Tailscale), como Claude Code o Cursor, también pueden usar la dirección de tu panel seguida de `/mcp`. La opción **Desvincular esta Machine**, al final de **Ajustes**, **Cuenta**, quita de tu cuenta una Machine que tengas en tu propio ordenador.

Tu Machine te muestra qué IA está haciendo la solicitud. Si no puede identificarla, te indica de dónde viene la solicitud. Conéctala solo si acabas de iniciar el proceso.

Elige qué puede hacer: **Leer** o **Leer y editar**. Si tienes cuentas de Trabajo y Personal, elige a cuál puede acceder. Después, elige durante cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar** o **Cancelar** para rechazar la solicitud.

## App oficial o dirección privada

La app oficial es la opción más sencilla: usa una sola dirección para todos y tu cuenta encuentra tu Machine. Nuestra nube transmite las solicitudes, pero no guarda nada.

Con tu dirección privada, todo se cifra hasta llegar a tu Machine. La nube solo transmite los datos y no puede leerlos.

En ambos casos, quien decide es tu Machine. Solo puede acceder una IA que hayas aprobado en su página, con los permisos que hayas elegido. En **Ajustes**, **Apps**, las IA conectadas mediante la app oficial muestran **App oficial**.

## Qué puede ver

Cada conexión solo puede ver la información de su área. Trabajo incluye las tareas y promesas de tus cuentas de trabajo, las personas, empresas y proyectos de trabajo, y el resumen del equipo de tu Fleet de trabajo. Personal incluye el resto. El contenido de los mensajes permanece en tu Machine, a menos que actives **Mensajes**. Si no lo activas, la IA solo verá el remitente, el asunto y la fecha de los mensajes relacionados con una tarea.

Los registros del Team Graph de tus compañeros nunca se envían a una IA externa.

## Mensajes

**Mensajes** permite que una IA busque y lea tu correo, Slack, WhatsApp y otros chats. Está desactivado hasta que lo actives, ya sea en la página donde conectas la IA o más adelante en **Ajustes**, **Apps**. Solo permite leer: nunca envía, elimina ni marca nada.

Solo lee los mensajes de su área. Algunos nunca se comparten: los códigos de un solo uso y los enlaces de inicio de sesión, los mensajes de un tablero o proyecto **Solo tú**, las conversaciones que The Machine considera sensibles (negocios, RR. HH., asuntos legales, salud y dinero), las conversaciones que mantuviste privadas y los mensajes eliminados.

Cada lectura aparece en su **Actividad**, con el número de mensajes y las conversaciones consultadas, pero nunca con el texto. Tu Machine entrega el texto marcado como datos, así que la IA no debería seguir las instrucciones que aparezcan en un mensaje.

Mientras **Mensajes** esté activado, los cambios en Graph de una IA con **Leer y editar** esperan a que des tu visto bueno. Pulsa **Aplicar** o **Descartar** en el cambio de **Actividad**.

## En Ajustes

Abre **Ajustes**, **Apps** para ver cada IA que se haya conectado, junto con sus permisos, área, fecha de vencimiento y último uso. Desde ahí puedes activar y desactivar **Mensajes**. Pulsa **Cambiar** para modificar sus permisos, su área o cuánto tiempo dura el acceso. El cambio se aplicará en la próxima solicitud. En **Actividad** aparecen todas las solicitudes, incluidas las rechazadas. **Desactivar ahora** pausa el acceso: se cierran todas las sesiones, pero se conserva el historial. **Quitar** elimina la conexión y su historial.

Si vuelves a iniciar sesión en la misma IA, la nueva aprobación sustituye a la anterior.

Una IA que no pueda iniciar sesión por sí sola puede usar una clave. En **Añadir una clave**, ponle un nombre, elige los permisos y cuánto tiempo dura, y pulsa **Crear clave**. Copia la clave enseguida: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Mantén la seguridad

Se registran todas las solicitudes, incluidas las rechazadas. Se rechazan las conexiones vencidas o desactivadas hasta que las cambies. Tu Machine solo conserva una huella digital de cada inicio de sesión, así que una copia de sus datos no permite acceder a nada.
