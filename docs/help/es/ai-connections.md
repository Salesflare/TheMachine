---
title: Conecta otras IA
area: connections
summary: Deja que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y tu Graph. Con **Leer y editar**, también podrán hacer cambios que puedes deshacer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 7681c632f712e93c
---
## Qué puede hacer otra IA

Claude, ChatGPT, Cursor, Codex, GBrain y otras IA pueden conectarse a tu Machine. Pueden leer tus tareas, promesas, briefs del equipo y las personas y empresas de tu Graph.

Con **Leer y editar**, también pueden añadir una tarea o un borrador de correo, y actualizar tu Graph: guardar un dato, corregir detalles, campos y etiquetas, o añadir una línea al resumen de una persona.

Cada cambio aparece en **Actividad** con **Deshacer**. Nunca combinan, eliminan ni comparten registros. Lo que guardan lleva la marca **AI:** y su nombre. Tu Machine lo trata como una afirmación suya, nunca como una instrucción tuya.

Un borrador queda pendiente hasta que lo lees y pulsas Enviar tú mismo. Una IA conectada nunca envía nada ni actúa en tu nombre.

## Qué aprende de ti

Cuando empieza un chat, la IA recibe un brief breve: quién eres, tus reglas principales y qué ha cambiado desde su última visita. También puede leer lo que contiene **Aprendizaje**: tus reglas, datos generales y cómo escribes en cada canal. Así escribe como lo harías tú.

Con **Leer y editar**, puede guardar lo que acordéis en el chat. Los datos se guardan al momento y puedes usar **Deshacer** en **Actividad**. Una regla orienta el trabajo de tu Machine, así que queda pendiente en **Aprendizaje** hasta que pulses **Aprobar** o **Descartar**. Nunca cambia tu forma de escribir.

Si un borrador tiene algo pendiente de completar, menciona un archivo que no tiene o solo incluye tu propia dirección, vuelve a la IA para que lo corrija primero. Si una IA pide la misma tarea o el mismo borrador dos veces seguidas, solo recibirás uno.

## Conecta una IA

Abre **Ajustes**, **Apps**. Debajo de **Las apps de The Machine** están **Añadir en ChatGPT** y **Añadir en Claude**. En **O añádela con una dirección** encontrarás la dirección única de la app oficial para todas las Machines, `https://mcp.themachine.computer/mcp`, y **Tu dirección**, `https://<your name>.mcp.themachine.computer/mcp`, ambas con **Copiar**.

Si tienes una Machine en tu propio ordenador, pulsa primero **Configurar**, debajo de **Consigue tu dirección**. Se abrirá una página en tu cuenta: comprueba que muestre el mismo código, confírmalo y elige un nombre. Tu Machine se vincula automáticamente, sin reiniciarse. Este paso es necesario en ambos casos.

Tu Machine configurará automáticamente su dirección segura. Tardará unos minutos.

Para Claude, pulsa **Añadir en Claude** o abre [The Machine en el directorio de Claude](https://claude.ai/directory/the-machine) y pulsa Connect. En Team y Enterprise, el propietario debe añadirla en los ajustes de la organización.

La habilidad de The Machine le indica a Claude cuándo debe usar tu Machine: primero el brief, después tus reglas y tu estilo, antes de redactar nada. Pulsa **Descargar**, junto a **Habilidad de Claude**, y luego abre Customize y Skills en Claude para subirla.

Si prefieres usar una dirección en Claude, abre Customize, Connectors, pulsa + Add y luego Add custom connector. Ponle el nombre The Machine, pega la dirección, pulsa Continue y luego Add.

Para ChatGPT, pulsa **Añadir en ChatGPT** o abre [The Machine en ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) y pulsa Install plugin. En Business y Enterprise, es posible que un administrador tenga que permitirlo primero.

La app oficial se conecta a una Machine alojada en la nube y también a una Machine en tu propio ordenador, una vez que tenga su dirección.

Para usar tu dirección privada o una Machine que no esté en la Network, añade un servidor MCP personalizado en ChatGPT: abre chatgpt.com/plugins, pulsa + y luego Add custom MCP server. Ponle el nombre The Machine, pega la dirección y elige OAuth. Confirma el aviso y pulsa Create as a plugin. Tu plan o espacio de trabajo debe permitir servidores MCP personalizados.

Con la app oficial, la IA te pedirá que inicies sesión con tu cuenta de The Machine. Si tienes más de una Machine, elige esta y aprueba la conexión en la página de tu Machine. Con la dirección privada, la IA se conecta directamente a tu Machine.

Las IA de dispositivos en tu red privada (Tailscale), como Claude Code o Cursor, también pueden usar la dirección de tu panel seguida de `/mcp`. **Desvincular esta Machine**, al final de **Ajustes**, **Cuenta**, vuelve a quitar de tu cuenta una Machine que tengas en tu propio ordenador.

Tu Machine te muestra qué IA está solicitando acceso. Si no puede identificarla, te muestra de dónde viene la solicitud: conéctala solo si acabas de iniciar el proceso.

Elige qué puede hacer: **Leer** o **Leer y editar**. Si tienes cuentas de trabajo y personales, elige a cuáles puede acceder. Después, elige durante cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar** o **Cancelar** para rechazar la solicitud.

## App oficial o dirección privada

La app oficial es la opción más sencilla: una dirección para todos y tu cuenta encuentra tu Machine. Nuestra nube transmite las solicitudes, pero nunca almacena su contenido.

Con tu dirección privada, todo va cifrado hasta tu Machine. La nube solo lo transmite y no puede leerlo.

En ambos casos, quien decide es tu Machine. Solo puede acceder una IA que hayas aprobado en su página, y con los permisos que hayas elegido. En **Ajustes**, **Apps**, las IA conectadas mediante la app oficial muestran **App oficial**.

## Qué puede ver

Cada conexión solo puede acceder a su área. Trabajo incluye las tareas y promesas de tus cuentas de trabajo, las personas y empresas del trabajo, los proyectos y el brief del equipo de tu Fleet de trabajo. Personal incluye todo lo demás. El texto de los mensajes permanece en tu Machine, a menos que actives **Mensajes**. Si no lo activas, la IA solo ve el remitente, el asunto y la fecha de los mensajes relacionados con una tarea.

Los registros del Graph del equipo de tus compañeros nunca se envían a una IA externa.

## Mensajes

**Mensajes** permite que una IA busque y lea tu correo, Slack, WhatsApp y otros chats. Está desactivado hasta que lo actives, en la página donde conectas la IA o después en **Ajustes**, **Apps**. Solo permite leer: nunca envía, elimina ni marca nada.

Solo lee los mensajes de su área. Algunos nunca salen de tu Machine: los códigos de un solo uso y los enlaces de inicio de sesión, los mensajes de un tablero o proyecto **Solo tú**, los hilos que The Machine haya marcado como sensibles (acuerdos, RR. HH., asuntos legales, salud o dinero), los hilos que hayas mantenido privados y los mensajes eliminados.

Cada lectura aparece en **Actividad**, con el número de mensajes y los hilos correspondientes, nunca con el texto. Tu Machine entrega el texto marcado como datos, así que la IA no debería seguir las instrucciones escritas en un mensaje.

Mientras Mensajes esté activado, los cambios en el Graph de una IA con **Leer y editar** quedan pendientes de tu visto bueno. Pulsa **Aplicar** o **Descartar** en el cambio de **Actividad**.

## En Ajustes

Abre **Ajustes**, **Apps** para ver cada IA que se ha conectado, una sola vez, con sus permisos, área, fecha de caducidad y último uso. Desde ahí puedes activar y desactivar **Mensajes**. Pulsa **Cambiar** para modificar sus permisos, el área a la que accede o durante cuánto tiempo. Los cambios se aplican en la siguiente solicitud. **Actividad** muestra todas las solicitudes, incluso las rechazadas. **Desactivar ahora** la pausa: se cierran todas las sesiones y se conserva el historial. **Quitar** la elimina junto con su historial.

Si vuelves a iniciar sesión en la misma IA, la nueva aprobación sustituye a la anterior. Si ya habías iniciado sesión en esa IA, seguirá conectada con los nuevos permisos. Una IA que uses seguirá conectada hasta la fecha de caducidad. Si no la usas durante 90 días, tendrás que iniciar sesión otra vez.

Una IA que no pueda iniciar sesión por sí sola puede usar una clave. En **Añadir una clave**, ponle un nombre, elige los permisos y la duración, y pulsa **Crear clave**. Copia la clave en ese momento: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Seguridad

Se registra cada solicitud, incluso las rechazadas. Si una conexión ha caducado o está desactivada, se rechazarán las solicitudes hasta que la cambies. Tu Machine solo conserva una huella digital de cada inicio de sesión, así que una copia de sus datos no permite acceder a nada.
