---
title: Conecta otras IA
area: connections
summary: Deja que Claude, ChatGPT, Cursor, Codex o GBrain lean tus tareas y Graph. Con **Leer y editar**, también podrán hacer cambios que puedes deshacer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: acdce4a5793f7c67
---
## Qué puede hacer otra IA

Claude, ChatGPT, Cursor, Codex, GBrain y otras IA pueden conectarse a tu Machine. Pueden leer tus tareas, promesas, resúmenes del equipo y las personas y empresas de Graph.

Con **Leer y editar**, también pueden añadir una tarea o un borrador de correo, y actualizar Graph: guardar un dato, corregir detalles, campos y etiquetas, o añadir una línea al resumen de una persona.

Cada cambio aparece en **Actividad**, con la opción **Deshacer**. Nunca combinan, eliminan ni comparten registros. Lo que guardan lleva la marca **IA:** y su nombre. Tu Machine lo trata como una afirmación suya, nunca como una instrucción tuya.

Los borradores esperan hasta que los leas y pulses Enviar. Una IA conectada nunca envía nada ni actúa en tu nombre.

Si a un borrador le falta algo por completar, menciona un archivo que no tiene o solo incluye tu propia dirección, vuelve a la IA para que lo corrija. Si una IA pide la misma tarea o el mismo borrador dos veces seguidas, solo recibes uno.

## Conectar una IA

Abre **Ajustes** y **Apps**. Debajo de **Las apps de The Machine** aparecen **Añadir en ChatGPT** y **Añadir en Claude**. En **O añádela con una dirección** están la dirección única de la app oficial para cualquier Machine, `https://mcp.themachine.computer/mcp`, y **Tu dirección**, `https://<your name>.mcp.themachine.computer/mcp`, ambas con la opción **Copiar**.

Si tienes una Machine en tu propio ordenador, primero pulsa **Configurar**, debajo de **Consigue tu dirección**. Se abrirá una página de tu cuenta: comprueba que aparezca el mismo código, confírmalo y elige un nombre. Tu Machine se vincula sola, sin reiniciarse. Necesitas hacerlo con cualquiera de las dos opciones.

Después, tu Machine configura por sí sola su dirección segura. Tarda unos minutos.

Para Claude, pulsa **Añadir en Claude** o abre [The Machine en el directorio de Claude](https://claude.ai/directory/the-machine) y pulsa Conectar. En los planes Team y Enterprise, alguien con permisos de propietario debe añadirla en los ajustes de la organización.

Si prefieres usar una dirección en Claude, abre Customize, Connectors, pulsa + Add y luego Add custom connector. Ponle el nombre The Machine, pega la dirección, pulsa Continue y luego Add.

Para ChatGPT, pulsa **Añadir en ChatGPT** o abre [The Machine en ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) y pulsa Install plugin. En los planes Business y Enterprise, puede que un administrador tenga que permitirlo primero.

La app oficial se conecta a una Machine alojada en la nube y también a una Machine en tu propio ordenador, cuando ya tiene su dirección.

Para usar tu dirección privada o una Machine que no esté en Network, añade un servidor MCP personalizado en ChatGPT: abre chatgpt.com/plugins, pulsa + y luego Add custom MCP server. Ponle el nombre The Machine, pega la dirección y elige OAuth. Confirma el aviso y pulsa Create as a plugin. Tu plan o espacio de trabajo debe permitir servidores MCP personalizados.

Con la app oficial, la IA te pide que inicies sesión con tu cuenta de The Machine. Si tienes más de una Machine, elige una y aprueba la conexión en la página de tu Machine. Con la dirección privada, la IA se conecta directamente a tu Machine.

Las IA de dispositivos de tu red privada (Tailscale), como Claude Code o Cursor, también pueden usar la dirección de tu panel seguida de `/mcp`. **Desvincular esta Machine**, al final de **Ajustes**, **Cuenta**, quita de tu cuenta una Machine instalada en tu propio ordenador.

Tu Machine muestra qué IA está haciendo la solicitud. Si no puede identificarla, muestra de dónde viene la solicitud: conéctala solo si acabas de iniciar este proceso.

Elige qué puede hacer: **Leer** o **Leer y editar**. Si tienes cuentas de trabajo y personales, elige qué puede ver. Después, elige durante cuánto tiempo: **1 día**, **7 días**, **30 días** o **1 año**. Pulsa **Conectar** o **Cancelar** para rechazar la solicitud.

## App oficial o dirección privada

La app oficial es la opción más sencilla: una dirección para todos y tu cuenta encuentra tu Machine. Nuestra nube transmite las solicitudes y nunca guarda su contenido.

Con tu dirección privada, todo se cifra de extremo a extremo hasta llegar a tu Machine. La nube solo lo transmite y no puede leerlo.

En cualquiera de las dos opciones, tu Machine decide. Solo puede acceder una IA que hayas aprobado en su página, con los permisos que elegiste. En **Ajustes**, **Apps**, las IA conectadas mediante la app oficial muestran **App oficial**.

## Qué puede ver

Cada conexión solo ve su ámbito. El ámbito de trabajo incluye las tareas y promesas de tus cuentas de trabajo, las personas, empresas y proyectos del trabajo, y el resumen del equipo de tu Fleet de trabajo. El ámbito personal incluye el resto. El texto de los mensajes se queda en tu Machine, a menos que actives **Mensajes**. Si no lo activas, una IA solo ve quién envió cada tarea, el asunto y la fecha de sus mensajes de origen.

Los registros de Team Graph de tus compañeros no se comparten con ninguna IA externa.

## Mensajes

**Mensajes** permite que una IA busque y lea tus correos y chats de Slack, WhatsApp y otras apps. Está desactivado hasta que lo actives, ya sea en la página donde conectas la IA o más tarde en **Ajustes**, **Apps**. Solo permite leer: nunca envía, elimina ni marca nada.

Solo lee los mensajes de su ámbito. Algunos nunca salen de tu Machine: códigos de un solo uso y enlaces de inicio de sesión, mensajes de un tablero o proyecto con la opción **Solo tú**, conversaciones que The Machine considera confidenciales (negociaciones, Recursos Humanos, asuntos legales, salud y dinero), conversaciones que hayas mantenido privadas y mensajes eliminados.

Cada lectura aparece en **Actividad**, con el número de mensajes y las conversaciones, nunca con el texto. Tu Machine entrega el texto marcado como datos, para que la IA no siga las instrucciones que encuentre en un mensaje.

Mientras **Mensajes** esté activado, los cambios de Graph que haga una IA con **Leer y editar** esperarán a que des tu visto bueno. Pulsa **Aplicar** o **Descartar** en el cambio, desde **Actividad**.

## En Ajustes

Abre **Ajustes** y **Apps** para ver cada IA que se haya conectado, junto con sus permisos, ámbito, fecha de finalización y último uso. Desde ahí puedes activar o desactivar **Mensajes**. Pulsa **Cambiar** para modificar sus permisos, su ámbito o cuánto tiempo dura la conexión. Los cambios se aplican en la siguiente solicitud. **Actividad** muestra todas las solicitudes, incluso las rechazadas. **Desactivar ahora** pausa la conexión: se cierran todas las sesiones, pero se conserva el historial. **Quitar** la elimina junto con su historial.

Cuando vuelvas a iniciar sesión en la misma IA, la nueva autorización sustituye a la anterior. Si ya habías iniciado sesión en esa IA, seguirá conectada con los nuevos permisos. Una IA que uses seguirá conectada hasta la fecha de finalización. Si no usas una IA durante 90 días, te pedirá que vuelvas a iniciar sesión.

Una IA que no pueda iniciar sesión por su cuenta puede usar una clave. En **Añadir una clave**, ponle un nombre, elige los permisos y la duración, y pulsa **Crear clave**. Copia la clave enseguida: solo se muestra una vez. La IA la envía como `Authorization: Bearer <key>`.

## Protege tu cuenta

Se registran todas las solicitudes, incluso las rechazadas. Si una conexión ha caducado o está desactivada, se rechazará hasta que la cambies. Tu Machine solo guarda una huella digital de cada inicio de sesión, así que una copia de sus datos no permite acceder a nada.
