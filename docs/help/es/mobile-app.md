---
title: La app móvil
area: getting-started
summary: The Machine como app para iPhone y Android: recibe notificaciones de tus tareas y compártelas con The Machine desde cualquier app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 672364a90f92ef8f
---
La app móvil abre tu propio panel, con la misma sesión que en la web. Descárgala en el [App Store](https://apps.apple.com/app/id6829875215) para iPhone y iPad, o en [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

La tarea **Saca más partido a The Machine**, en la parte superior de Tareas, te sugiere instalarla. En el navegador del teléfono, **Obtener** abre la tienda. Si el teléfono muestra sitios para ordenador, verás los enlaces a ambas tiendas. En un ordenador, verás un código QR para escanear con el teléfono y enlaces a ambas tiendas.

En cualquier teléfono, [themachine.computer/app](https://themachine.computer/app) abre la tienda que corresponde. En **Ajustes**, **Apps** aparecen las dos tiendas en la parte superior, o solo la tienda de tu teléfono si estás en uno. En un ordenador, **Ordenador** instala el panel como app: consulta [Instalar la app](phone-app.md).

## Conectarla

En una Machine alojada, la app inicia sesión con tu cuenta. Si la alojas tú, abre **Ajustes**, **Apps** en un ordenador: debajo de las tiendas, **¿No estás en la Network?** muestra un código. Instala la app y escanéalo con la cámara del teléfono, o escribe en la app la dirección que aparece debajo. La app te pide permiso antes de conectarse, y sigue siendo necesario iniciar sesión en tu Machine.

Al tocar **Iniciar sesión con** un servicio en **Conexiones** (Shortcut, Notion, Slack, Zoom y los demás), se abre la pantalla de inicio de sesión del teléfono. Cuando termines, volverás a la app y la nueva conexión aparecerá automáticamente en **Conexiones**.

Si la app no puede conectarse con tu Machine, te lo dice y vuelve a intentarlo automáticamente. En un Mac o un iPad con teclado, Cmd+R vuelve a cargar la página.

## Notificaciones

La app te pide permiso para enviarte notificaciones al abrirla por primera vez. Toca una para abrir lo que indica: una tarea aparece resaltada en tu lista, la notificación de la mañana abre el día de hoy en **Calendario**, el resumen del equipo abre Tareas y una pregunta de Fleet abre la tarea correspondiente. El texto de una tarea nunca pasa por Apple, Google ni el servicio de The Machine: solo transmiten un mensaje fijo, como «Hay una tarea que necesita tu atención».

Después, la app le pide a tu Machine el título de la tarea y el siguiente paso, por ejemplo, «Responder a Sam» y «Enviar a Sam: el martes a las 10:00 me va bien». La notificación de la mañana incluye lo que tienes pendiente y la hora de tu primera reunión; el resumen del equipo, sus primeros elementos; y una actualización de Fleet, lo que ha ocurrido. Si no puede conectarse con tu Machine, se mantiene el mensaje fijo. En Android, indica cuántas tareas tienes pendientes, por ejemplo, «Tienes 2 tareas pendientes».

Las notificaciones incluyen **Posponer** (hasta mañana) y **Marcar como hecha**, además de **Hazlo** si aún no has empezado una tarea. Estas opciones funcionan después de desbloquear el teléfono, sin abrir la app. Para enviar algo y completar los pasos finales, siempre se abre la app. Hay una notificación por tarea: «Preparando» cambia a «Lista» y desaparece cuando la tarea se completa o se pospone, desde aquí o desde cualquier otro lugar.

Cuando se completa un paso que confirmaste, su notificación indica **Hecho** y lo que ocurrió. Permanece hasta que toques **Entendido** en Tareas. En iPhone, puede esperar hasta que vuelvas a abrir la app.

Si desactivas **Texto en las notificaciones** en **Ajustes**, **Seguridad**, se mantiene el mensaje fijo. Lo mismo ocurre si la pantalla de bloqueo oculta el contenido de las notificaciones. Cuando no puede mostrar nada más, aparece «Toca para abrir». Si tu teléfono no puede conectarse con tu Machine cuando llega una notificación, muestra los detalles cuando vuelve a estar conectado.

Se aplican las mismas reglas que a las notificaciones push en la web: lo que hayas elegido para cada tipo en [Notificaciones](notifications.md), tu [horario laboral](work-hours.md) y ninguna notificación mientras estés usando un panel.

Cada teléfono con la app aparece en **Ajustes**, **Notificaciones** como **Teléfono con la app**. **Quitar** detiene sus notificaciones. Para recibirlas en una Machine alojada por ti, necesitas The Machine Network. La app funciona sin ellas.

## Compartir con The Machine

En cualquier app, toca Compartir y elige The Machine. Se abre **Nueva tarea** con el texto, el enlace o los archivos que hayas compartido. Revísala, añade una fecha si quieres y guárdala. No se añade nada hasta que lo hagas.

También puedes compartir solo un archivo, como una factura o una carta. Tu Machine lee el texto de los PDF y completa la tarea con lo que es, el siguiente paso y la fecha. El archivo se envía directamente a tu Machine y se queda allí.

El panel instalado como app en Android también recibe lo que compartas: selecciónalo en la hoja para compartir, igual que cualquier otra app.

Los planes y la facturación no aparecen en la app. **Abrir cuenta** en **Ajustes** sigue disponible para eliminar tu cuenta.
