---
title: Conectar otras IA
area: connections
summary: Permite que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y tu Graph, y que, con **Leer y editar**, hagan cambios que puedes deshacer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: a8637260c99df309
---
## Qué puede hacer otra IA

Claude, ChatGPT, Cursor, Codex, GBrain y otras IA pueden conectarse a tu Machine. Pueden leer tus tareas, promesas, resúmenes del equipo y las personas y empresas de tu Graph.

Con **Leer y editar**, también pueden añadir una tarea o un borrador de correo, y actualizar tu Graph: guardar un dato, corregir detalles, campos y etiquetas, o añadir una línea al resumen de una persona.

Cada cambio aparece en **Actividad** con la opción **Deshacer**. Nunca combinan, eliminan ni comparten registros. Lo que guardan aparece marcado como **AI:** con su nombre, y tu Machine lo considera una afirmación suya, nunca una instrucción tuya.

Un borrador espera hasta que lo leas y pulses **Enviar**. Una IA conectada nunca envía nada ni actúa en tu nombre.

## Conectar una IA

Abre **Ajustes**, **Apps**. Debajo de **Las apps de The Machine** están **Añadir en ChatGPT** y **Añadir en Claude**. En **O añádela con una dirección** encontrarás la dirección de la app oficial, `https://mcp.themachine.computer/mcp`, que es la misma para todas las Machines, y **Tu dirección**, `https://<your name>.mcp.themachine.computer/mcp`, cada una con la opción **Copiar**.

Si tienes una Machine en tu propio ordenador, pulsa **Configurar** debajo de **Consigue tu dirección**. Se abrirá una página de tu cuenta: comprueba que muestra el mismo código, confirma y elige un nombre. Tu Machine se vincula automáticamente, sin reiniciarse. Esto hace falta en ambos casos.

Tu Machine configurará automáticamente su dirección segura. Tardará unos minutos.

Para Claude, pulsa **Añadir en Claude** o abre [The Machine en el directorio de Claude](https://claude.ai/directory/the-machine) y pulsa **Conectar**. En Team y Enterprise, el propietario debe añadirla en los ajustes de la organización.

Si prefieres usar una dirección en Claude, abre Customize, Connectors, pulsa **+ Añadir** y luego **Añadir conector personalizado**. Ponle el nombre The Machine, pega la dirección, pulsa **Continuar** y luego **Añadir**.

Para ChatGPT, pulsa **Añadir en ChatGPT** o abre [The Machine en ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) y pulsa **Instalar plugin**. En Business y Enterprise, puede que un administrador tenga que permitirlo primero.

La app oficial se conecta a una Machine alojada y también a una Machine en tu propio ordenador, una vez que tenga su dirección.

Para usar tu dirección privada, o una Machine que no esté en la Network, añade un servidor MCP personalizado en ChatGPT: abre chatgpt.com/plugins, pulsa **+** y luego **Añadir servidor MCP personalizado**. Ponle el nombre The Machine, pega la dirección y elige OAuth. Confirma el aviso y pulsa **Crear como plugin**. Tu plan o espacio de trabajo debe permitir el uso de servidores MCP personalizados.

Con la app oficial, la IA te pedirá que inicies sesión con tu cuenta de The Machine. Si tienes más de una Machine, elige esta y aprueba la conexión en la página de tu Machine. Con la dirección privada, la IA se conecta directamente a tu Machine.

Las IA de un dispositivo de tu red privada (Tailscale), como Claude Code o Cursor, también pueden usar la dirección de tu panel seguida de `/mcp`. **Desvincular esta Machine**, al final de **Ajustes**, **Cuenta**, vuelve a quitar de tu cuenta una Machine que esté en tu propio ordenador.

Tu Machine te muestra qué IA está haciendo la solicitud. Si no puede identificarla, te muestra de dónde viene la solicitud. Conéctala solo si acabas de iniciar tú el proceso.

Elige qué puede hacer: **Leer** o **Leer y editar**. Si tienes cuentas de Trabajo y Personal, elige qué puede ver. Después, elige durante cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar** o **Cancelar** para rechazar la solicitud sin hacer cambios.

## App oficial o dirección privada

La app oficial es la opción más sencilla: una dirección para todos y tu cuenta encuentra tu Machine. Nuestra nube transmite las solicitudes y nunca guarda su contenido.

Con tu dirección privada, todo está cifrado hasta llegar a tu Machine. La nube solo lo transmite y no puede leerlo.

En ambos casos, quien decide es tu Machine. Solo puede acceder una IA que hayas aprobado en su página, con el acceso que hayas elegido. En **Ajustes**, **Apps**, las IA que se conectan mediante la app oficial muestran **App oficial**.

## Qué puede ver

Cada conexión solo ve su área. Trabajo incluye las tareas y promesas de tus cuentas de trabajo, las personas, empresas y proyectos de trabajo, y el resumen del equipo de tu Fleet de trabajo. Personal incluye todo lo demás. El texto de los mensajes se queda en tu Machine, salvo que actives **Mensajes**. Si no lo activas, la IA solo ve el remitente, el asunto y la fecha de los mensajes que originaron una tarea.

Los registros del Graph del equipo de tus compañeros nunca se envían a una IA externa.

## Mensajes

**Mensajes** permite que una IA busque y lea tu correo, Slack, WhatsApp y otros chats. Está desactivado hasta que lo actives, ya sea en la página de conexión o más adelante en **Ajustes**, **Apps**. Solo lee: nunca envía, elimina ni marca nada.

Solo lee los mensajes de su área. Algunos nunca se envían: los códigos de un solo uso y los enlaces para iniciar sesión, los mensajes de un tablero o proyecto **Solo tú**, los hilos que The Machine considera confidenciales (negocios, RR. HH., asuntos legales, salud o dinero), los hilos que mantienes privados y los mensajes eliminados.

Cada lectura aparece en su **Actividad** con el número de mensajes y los hilos correspondientes, pero nunca con el texto. Tu Machine entrega el texto marcado como datos, así que la IA no debería seguir las instrucciones escritas en un mensaje.

Mientras **Mensajes** esté activado, los cambios en el Graph de una IA con **Leer y editar** esperarán a que des tu visto bueno. Pulsa **Aplicar** o **Descartar** en el cambio dentro de **Actividad**.

## En Ajustes

Abre **Ajustes**, **Apps** para ver cada IA que se ha conectado, con su acceso, área, fecha de finalización y último uso. Desde ahí puedes activar o desactivar **Mensajes**. Pulsa **Cambiar** para modificar el acceso, el área o durante cuánto tiempo se mantiene. Se aplicará a la siguiente solicitud. **Actividad** muestra todas las solicitudes, también las rechazadas. **Desactivar ahora** la pausa: se cierran todas las sesiones, pero se conserva su historial. **Quitar** la elimina junto con su historial.

Si vuelves a iniciar sesión en la misma IA, la nueva aprobación sustituye a la anterior.

Una IA que no puede iniciar sesión por sí sola puede usar una clave. En **Añadir una clave**, ponle un nombre, elige el acceso y la duración, y pulsa **Crear clave**. Copia la clave en ese momento: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Mantén la seguridad

Se registran todas las solicitudes, también las rechazadas. Si una conexión ha caducado o está desactivada, se rechaza hasta que la cambies. Tu Machine solo guarda una huella digital de cada inicio de sesión, así que una copia de sus datos no permite acceder a nada.
