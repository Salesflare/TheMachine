---
title: Conecta otras IA
area: connections
summary: Permite que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y tu Graph y, con Leer y editar, hagan cambios que puedes deshacer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 3a7200b2a076c274
---
## Qué puede hacer otra IA

Claude, ChatGPT, Cursor, Codex, GBrain y otras IA pueden conectarse a tu Machine. Pueden leer tus tareas, promesas, resúmenes del equipo y las personas y empresas de tu Graph.

Con **Leer y editar**, también pueden añadir una tarea o un borrador de correo y actualizar tu Graph: guardar un dato, corregir detalles, campos y etiquetas, o añadir una línea al resumen de una persona.

Cada cambio aparece en **Actividad** con **Deshacer**. Nunca combinan, eliminan ni comparten registros. Lo que guardan se marca con **IA:** y su nombre, y tu Machine lo considera una afirmación suya, nunca una instrucción tuya.

Un borrador espera hasta que lo leas y pulses Enviar. Una IA conectada nunca envía nada ni actúa en tu nombre.

## Qué aprende de ti

Cuando empieza un chat, la IA recibe un breve resumen: quién eres, tus reglas principales y qué ha cambiado desde su última visita. También puede leer lo que hay en **Aprendizaje**: tus reglas, datos generales y cómo escribes en cada canal. Así escribe como lo harías tú.

Con **Leer y editar**, puede guardar lo que acordéis en el chat. Un dato se guarda de inmediato y puedes usar **Deshacer** en **Actividad**. Una regla guía el trabajo de tu Machine, así que espera en **Aprendizaje** hasta que pulses **Aprobar** o **Descartar**. Nunca cambia tu forma de escribir.

Si a un borrador le falta algo por completar, menciona un archivo que no tiene o solo incluye tu propia dirección, vuelve a la IA para que lo corrija primero. Si una IA pide la misma tarea o el mismo borrador dos veces seguidas, solo recibes uno.

## Conectar una IA

Abre **Ajustes**, **Apps**. Debajo de **Las apps de The Machine** verás **Añadir en ChatGPT** y **Añadir en Claude**. En **O añádela con una dirección** están la dirección oficial de la app, que sirve para todas las Machines, `https://mcp.themachine.computer/mcp`, y **Tu dirección**, `https://<your name>.mcp.themachine.computer/mcp`, cada una con **Copiar**.

En una Machine que esté en tu propio ordenador, pulsa primero **Configurar**, debajo de **Consigue tu dirección**. Se abrirá una página en tu cuenta: comprueba que muestre el mismo código, confírmalo y elige un nombre. Tu Machine se vincula automáticamente, sin reiniciarse. Esto hace falta en ambos casos.

Tu Machine configura automáticamente su dirección segura. Tarda unos minutos.

Para Claude, pulsa **Añadir en Claude** o abre [The Machine en el directorio de Claude](https://claude.ai/directory/the-machine) y pulsa Connect. En los planes Team y Enterprise, el propietario debe añadirla en los ajustes de la organización.

La habilidad de The Machine le indica a Claude cuándo usar tu Machine: primero le da el resumen y, antes de redactar nada, tus reglas y tu estilo. Pulsa **Descargar**, junto a **Habilidad de Claude**. Después, en Claude, abre Customize, Skills y súbela.

Para usar una dirección en Claude, abre Customize, Connectors, pulsa + Add y, después, Add custom connector. Ponle el nombre The Machine, pega la dirección, pulsa Continue y, después, Add.

Para ChatGPT, pulsa **Añadir en ChatGPT** o abre [The Machine en ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) y pulsa Install plugin. En los planes Business y Enterprise, puede que un administrador tenga que permitirlo primero.

La app oficial se conecta a una Machine alojada y también a una Machine que esté en tu propio ordenador, una vez que tenga su dirección.

Para usar tu dirección privada o una Machine que no esté en la Network, añade un servidor MCP personalizado en ChatGPT: abre chatgpt.com/plugins, pulsa + y, después, Add custom MCP server. Ponle el nombre The Machine, pega la dirección y elige OAuth. Confirma el aviso y pulsa Create as a plugin. Tu plan o espacio de trabajo debe permitir servidores MCP personalizados.

Con la app oficial, la IA te pedirá que inicies sesión con tu cuenta de The Machine. Si tienes más de una Machine, elige esta y aprueba la conexión en la página de tu Machine. Con la dirección privada, la IA se conecta directamente a tu Machine.

Las IA de un dispositivo de tu red privada (Tailscale), como Claude Code o Cursor, también pueden usar la dirección de tu panel de control seguida de `/mcp`. **Desvincular esta Machine**, al final de **Ajustes**, **Cuenta**, quita de tu cuenta una Machine que esté en tu propio ordenador.

Tu Machine te muestra qué IA está haciendo la solicitud. Si no puede identificarla, te muestra de dónde viene la solicitud: conéctala solo si acabas de iniciar tú la conexión.

Elige qué puede hacer: **Leer** o **Leer y editar**. Si tienes cuentas de trabajo y personales, elige qué puede ver. Después, elige durante cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar** o **Cancelar** para rechazar la solicitud sin hacer cambios.

## App oficial o dirección privada

La app oficial es la opción más sencilla: una dirección para todo el mundo y tu cuenta encuentra tu Machine. Nuestra nube retransmite las solicitudes y nunca guarda su contenido.

Con tu dirección privada, todo se cifra hasta llegar a tu Machine. La nube solo lo retransmite y no puede leerlo.

En ambos casos, quien decide es tu Machine. Solo puede acceder una IA que hayas aprobado en su página, y solo con los permisos que elegiste. En **Ajustes**, **Apps**, las IA conectadas mediante la app oficial muestran **App oficial**.

## Qué puede ver

Cada conexión solo ve su ámbito. Trabajo incluye las tareas y promesas de tus cuentas de trabajo, las personas, empresas y proyectos relacionados con el trabajo y el resumen del equipo de tu Fleet de trabajo. Personal incluye el resto. El texto de los mensajes se queda en tu Machine, salvo que actives **Mensajes**: si está desactivado, una IA solo ve el remitente, el asunto y la fecha de los mensajes relacionados con una tarea.

Los registros del Graph del equipo de tus compañeros nunca se comparten con una IA externa.

## Mensajes

**Mensajes** permite que una IA busque y lea tu correo, Slack, WhatsApp y otros chats. Está desactivado hasta que lo actives, ya sea en la página donde conectas la IA o más adelante en **Ajustes**, **Apps**. Solo permite leer: nunca envía, elimina ni marca nada.

Solo lee los mensajes de su ámbito. Algunos nunca se comparten: los códigos de un solo uso y los enlaces de inicio de sesión, los mensajes de un tablero o proyecto **Solo tú**, los hilos que The Machine considera sensibles (acuerdos, RR. HH., asuntos legales, salud y dinero), los hilos que mantuviste privados y los mensajes eliminados.

Cada lectura aparece en **Actividad** e indica cuántos mensajes y qué hilos se leyeron, nunca el texto. Tu Machine entrega el texto marcado como datos, así que la IA no debería seguir las instrucciones escritas en un mensaje.

Mientras **Mensajes** esté activado, los cambios que haga en tu Graph una IA con **Leer y editar** esperan a que les des el visto bueno. Pulsa **Aplicar** o **Descartar** en el cambio, en **Actividad**.

## Eventos

**Eventos** permite que una IA como ChatGPT se active por sí sola cuando ocurre algo: una tarea nueva, un resumen para una reunión de mañana o una promesa que vence mañana. Cada evento está desactivado hasta que lo actives en **Cambiar**. La IA recibe el título y un breve motivo, nada que no pudiera leer ya y nunca información anterior al evento.

Aun así, no puede enviar nada y sus cambios aparecen en **Actividad** con **Deshacer**. Si desactivas un evento o la IA, deja de actuar al instante.

## En Ajustes

Abre **Ajustes**, **Apps** para ver cada IA que se ha conectado, una sola vez, junto con sus permisos, ámbito, fecha de finalización y último uso. Puedes activar o desactivar **Mensajes** ahí mismo. Pulsa **Cambiar** para modificar sus permisos, su ámbito o cuánto tiempo dura el acceso. El siguiente uso aplicará los cambios. **Actividad** muestra todas las solicitudes, incluidas las rechazadas. **Desactivar ahora** pausa la conexión: se cierran todas las sesiones, pero se conserva el historial. **Quitar** elimina la IA y su historial.

Si vuelves a iniciar sesión en la misma IA, la nueva aprobación sustituye a la anterior. Si ya habías iniciado sesión en esa IA, seguirá conectada con los nuevos permisos. Una IA que uses seguirá conectada hasta la fecha de finalización. Si no la usas durante 90 días, te pedirá que vuelvas a iniciar sesión.

Una IA que no puede iniciar sesión por sí sola puede usar una clave. En **Añadir una clave**, ponle un nombre, elige los permisos y cuánto tiempo dura, y pulsa **Crear clave**. Copia la clave enseguida: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Mantén la seguridad

Se registran todas las solicitudes, incluidas las rechazadas. Si una conexión ha caducado o está desactivada, se rechaza hasta que la cambies. Tu Machine solo guarda una huella digital de cada inicio de sesión, así que una copia de sus datos no permite acceder.
