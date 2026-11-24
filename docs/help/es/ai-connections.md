---
title: Conectar otras IA
area: connections
summary: Permite que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y tu Graph y, con **Leer y editar**, hagan cambios que puedes deshacer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: cf0776c294917228
---
## Qué puede hacer otra IA

Claude, ChatGPT, Cursor, Codex, GBrain y otras IA pueden conectarse a tu Machine. Pueden leer tus tareas, promesas, resúmenes del equipo y las personas y empresas de tu Graph.

Con **Leer y editar**, también pueden añadir una tarea o un borrador de correo y actualizar tu Graph: guardar un dato, corregir detalles, campos y etiquetas, o añadir una línea al resumen de una persona.

Cada cambio aparece en **Actividad** con la opción **Deshacer**. Nunca combinan, eliminan ni comparten registros. Lo que guardan se marca como **IA:** con su nombre, y tu Machine lo trata como una afirmación suya, nunca como una instrucción tuya.

Un borrador espera hasta que lo leas y pulses Enviar. Una IA conectada nunca envía nada ni actúa en tu nombre.

Si a un borrador le falta algo por completar, menciona un archivo que no tiene o solo incluye tu propia dirección, se devuelve a la IA para que lo corrija. Si una IA pide la misma tarea o el mismo borrador dos veces seguidas, solo recibes uno.

## Conectar una IA

Abre **Ajustes**, **Apps**. En **Las apps de The Machine** encontrarás **Añadir en ChatGPT** y **Añadir en Claude**. En **O añádela con una dirección** están la dirección única de la app oficial para todas las Machines, `https://mcp.themachine.computer/mcp`, y **Tu dirección**, `https://<your name>.mcp.themachine.computer/mcp`, ambas con la opción **Copiar**.

Si tienes una Machine en tu propio ordenador, primero pulsa **Configurar**, debajo de **Consigue tu dirección**. Se abrirá una página en tu cuenta: comprueba que aparezca el mismo código, confírmalo y elige un nombre. Tu Machine se vinculará automáticamente, sin reiniciarse. Necesitas hacerlo para ambas opciones.

Después, tu Machine configurará automáticamente su dirección segura. Tardará unos minutos.

Para Claude, pulsa **Añadir en Claude** o abre [The Machine en el directorio de Claude](https://claude.ai/directory/the-machine) y pulsa Connect. En Team y Enterprise, la persona propietaria debe añadirla en los ajustes de la organización.

Si prefieres usar una dirección en Claude, abre Customize, Connectors, pulsa + Add y luego Add custom connector. Ponle el nombre The Machine, pega la dirección, pulsa Continue y luego Add.

Para ChatGPT, pulsa **Añadir en ChatGPT** o abre [The Machine en ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) y pulsa Install plugin. En Business y Enterprise, es posible que un administrador tenga que permitirlo primero.

La app oficial se conecta a una Machine alojada en la nube y también a una Machine en tu propio ordenador, una vez que tenga su dirección.

Para usar tu dirección privada, o una Machine que no esté en la Network, añade un servidor MCP personalizado en ChatGPT: abre chatgpt.com/plugins, pulsa + y luego Add custom MCP server. Ponle el nombre The Machine, pega la dirección y elige OAuth. Confirma el aviso y pulsa Create as a plugin. Tu plan o espacio de trabajo debe permitir el uso de servidores MCP personalizados.

Con la app oficial, la IA te pedirá que inicies sesión con tu cuenta de The Machine. Si tienes más de una Machine, elige esta y luego aprueba la conexión en la página de tu Machine. Con la dirección privada, la IA se conecta directamente a tu Machine.

Las IA que se ejecutan en un dispositivo de tu red privada (Tailscale), como Claude Code o Cursor, también pueden usar la dirección de tu panel seguida de `/mcp`. La opción **Desvincular esta Machine**, al final de **Ajustes**, **Cuenta**, quita de tu cuenta una Machine que tengas en tu propio ordenador.

Tu Machine te muestra qué IA está haciendo la solicitud. Si no puede identificarla, te muestra de dónde procede la solicitud: conéctala solo si acabas de iniciar este proceso.

Elige qué puede hacer: **Leer** o **Leer y editar**. Si tienes cuentas de trabajo y personales, elige a qué puede acceder. Después, elige durante cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar** o **Cancelar** para rechazar la conexión.

## App oficial o dirección privada

La app oficial es la opción más sencilla: hay una dirección para todos y tu cuenta encuentra tu Machine. Nuestro servicio en la nube transmite las solicitudes y nunca guarda su contenido.

Con tu dirección privada, todo se cifra de extremo a extremo hasta llegar a tu Machine. El servicio en la nube solo lo transmite y no puede leerlo.

En ambos casos, tu Machine decide. Solo puede acceder una IA a la que hayas dado permiso en su página, con el acceso que hayas elegido. En **Ajustes**, **Apps**, las IA que se conectan a través de la app oficial aparecen como **App oficial**.

## Qué puede ver

Cada conexión solo ve su ámbito. Trabajo incluye las tareas y promesas de tus cuentas de trabajo, las personas, empresas y proyectos de trabajo, y el resumen del equipo de tu Fleet de trabajo. Personal incluye todo lo demás. El texto de los mensajes permanece en tu Machine, salvo que actives **Mensajes**: si no lo haces, la IA solo ve el remitente, el asunto y la fecha de los mensajes relacionados con una tarea.

Los registros del Graph del equipo de tus compañeros nunca se envían a una IA externa.

## Mensajes

**Mensajes** permite que una IA busque y lea tu correo, Slack, WhatsApp y otros chats. Está desactivado hasta que lo actives, ya sea en la página donde conectas la IA o más tarde en **Ajustes**, **Apps**. Solo lee: nunca envía, elimina ni marca nada.

Solo lee los mensajes de su ámbito. Algunos nunca se comparten: códigos de un solo uso y enlaces de inicio de sesión, mensajes de un tablero o proyecto con la opción **Solo tú**, conversaciones que The Machine considera sensibles (negociaciones, RR. HH., asuntos legales, Salud y dinero), conversaciones que has mantenido privadas y mensajes eliminados.

Cada lectura aparece en **Actividad** con el número de mensajes y las conversaciones consultadas, nunca con el texto. Tu Machine entrega el texto marcado como datos, para que la IA no siga las instrucciones escritas en un mensaje.

Mientras **Mensajes** esté activado, los cambios que una IA con **Leer y editar** haga en Graph esperarán tu visto bueno. Pulsa **Aplicar** o **Descartar** en el cambio, dentro de **Actividad**.

## En Ajustes

Abre **Ajustes**, **Apps** para ver una sola vez cada IA que se haya conectado, junto con su acceso, ámbito, fecha de caducidad y último uso. Desde ahí puedes activar o desactivar **Mensajes**. Pulsa **Cambiar** para modificar el acceso, el ámbito o la duración. Los cambios se aplican en la siguiente solicitud. **Actividad** muestra todas las solicitudes, incluso las rechazadas. **Desactivar ahora** la pausa: se cierran todas las sesiones, pero se conserva su historial. **Quitar** la elimina junto con su historial.

Si vuelves a iniciar sesión en la misma IA, la nueva autorización sustituye a la anterior.

Una IA que no puede iniciar sesión por su cuenta puede usar una clave. En **Añadir una clave**, asígnale un nombre, elige el acceso y la duración, y pulsa **Crear clave**. Copia la clave en ese momento: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Protege tu cuenta

Todas las solicitudes quedan registradas, incluso las rechazadas. Las conexiones caducadas o desactivadas se rechazan hasta que las cambies. Tu Machine solo conserva una huella digital de cada inicio de sesión, así que una copia de esos datos no permite acceder a nada.
