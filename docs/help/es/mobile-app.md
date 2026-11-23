---
title: La app móvil
area: getting-started
summary: The Machine como app en iPhone y Android: notificaciones de tus tareas y la opción de compartir contenido con The Machine desde cualquier app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 927fa395fe97f565
---
La app móvil abre tu propio panel con la misma sesión que en la web. Descárgala en [App Store](https://apps.apple.com/app/id6829875215) para iPhone y iPad, o en [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

La tarea **Saca más partido a The Machine**, que aparece al principio de Tareas, te recomienda instalarla. En el navegador de un móvil, **Descargar** abre la tienda. En un móvil configurado para mostrar sitios de escritorio, aparecen los enlaces a las dos tiendas. En un ordenador, aparece un código QR para escanearlo con el móvil y los enlaces a las dos tiendas.

En cualquier móvil, [themachine.computer/app](https://themachine.computer/app) abre la tienda correspondiente. En **Ajustes**, **Apps** aparecen las dos tiendas al principio, o solo la tienda de tu móvil si estás usando uno. En un ordenador, **Ordenador** instala el panel como una app: consulta [Instalar la app](phone-app.md).

## Conéctala

En una Machine alojada, la app inicia sesión con tu cuenta. Si la tienes alojada en tu propio servidor, abre **Ajustes**, **Apps** en un ordenador: debajo de las tiendas, **¿No estás en la Network?** muestra un código. Instala la app y escanéalo con la cámara del móvil, o escribe en la app la dirección que aparece debajo. La app te pide permiso antes de conectarse y, además, se mantiene el inicio de sesión de tu Machine.

Al tocar **Iniciar sesión con** un servicio de **Conexiones** (Shortcut, Notion, Slack, Zoom y otros), se abre la pantalla de inicio de sesión del móvil. Al terminar, vuelves a la app y la nueva conexión aparece automáticamente en **Conexiones**.

Si la app no puede conectarse a tu Machine, te lo indica y vuelve a intentarlo automáticamente. En un Mac, la app también vuelve a abrir la página automáticamente si aparece en blanco al volver de la suspensión. También se recupera el mensaje que estabas escribiendo en un chat. En un Mac o un iPad con teclado, pulsa Cmd+R para volver a cargar la página.

## Notificaciones

La primera vez que se abre, la app te pide permiso para enviar notificaciones. Toca una para abrir lo que indica: una tarea aparece resaltada en tu lista, la notificación matinal abre el día de hoy en **Calendario**, el resumen del equipo abre Tareas y una pregunta de Fleet abre su tarea. El texto de las tareas no pasa por Apple, Google ni el servicio de The Machine. Solo transmiten una frase fija, como «Tienes una tarea pendiente».

Después, la app le pide a tu propia Machine el título de la tarea y el siguiente paso, como «Responder a Sam» con «Envíale a Sam: el martes a las 10:00 me va bien». La notificación matinal incluye lo que tienes pendiente y la hora de tu primera reunión; el resumen del equipo, sus primeros elementos; y las actualizaciones de Fleet, lo que ha ocurrido. Si no puede conectarse a tu Machine, se mantiene la frase fija. En Android indica cuántas tareas tienes pendientes, por ejemplo, «Tienes 2 tareas pendientes».

Las notificaciones tienen las opciones **Posponer** (hasta mañana) y **Marcar como hecho**, y **Hazlo** para las tareas que aún no has empezado. Funcionan cuando desbloqueas el móvil, sin abrir la app. Para enviar algo o completar los últimos pasos, siempre se abre la app. Recibirás una notificación por tarea: «Preparando» cambia a «Para revisar» y desaparece cuando completas o pospones la tarea, desde aquí o desde cualquier otro sitio.

Cuando se completa un paso que has confirmado, la notificación indica **Hecho** y qué ha ocurrido. Se mantiene hasta que toques **Entendido** en Tareas. En iPhone, puede esperar hasta la próxima vez que abras la app.

Si desactivas **Texto en las notificaciones** en **Ajustes**, **Seguridad**, se muestra la frase fija. También se muestra si la pantalla de bloqueo oculta el contenido de las notificaciones. Si no hay nada que pueda mostrar, aparece «Toca para abrir». Si el móvil no puede conectarse a tu Machine cuando llega una notificación, muestra los detalles cuando vuelva a estar conectado.

Se aplican las mismas reglas que a las notificaciones push en la web: lo que hayas elegido para cada tipo en [Notificaciones](notifications.md), tu [horario laboral](work-hours.md) y ninguna notificación mientras estés usando un panel.

Cada móvil con la app aparece en **Ajustes**, **Notificaciones** como **Teléfono con la app**. **Quitar** desactiva sus notificaciones. Una Machine alojada en tu propio servidor necesita The Machine Network para enviarlas. La app funciona sin ellas.

## Compartir con The Machine

En cualquier app, toca Compartir y elige The Machine. Se abre **Nueva tarea** con el texto, el enlace o los archivos que hayas compartido. Revísala, añade una fecha si quieres y guárdala. No se añade nada hasta que lo hagas.

También puedes compartir un archivo sin nada más, como una factura o una carta. Tu Machine lee el texto de los PDF y completa la tarea con lo que es, el siguiente paso y su fecha. El archivo se envía directamente a tu Machine y se queda allí.

El panel instalado como app en Android también permite compartir contenido: solo tienes que elegirlo en el menú para compartir.

Los planes y la facturación no aparecen en la app. La opción **Abrir cuenta** sigue estando en **Ajustes** para que puedas eliminar tu cuenta.
