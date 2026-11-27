---
title: La app móvil
area: getting-started
summary: The Machine como app en iPhone y Android: notificaciones de tus tareas y opción de compartir contenido con The Machine desde cualquier app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: aaf34f864dadf180
---
La app móvil abre tu propio panel, con la misma sesión que en la web. Descárgala en el [App Store](https://apps.apple.com/app/id6829875215) para iPhone y iPad o en [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

La tarea **Saca más partido a The Machine**, que aparece arriba en Tareas, te la recomienda. En el navegador de un móvil, **Descargar** abre la tienda. Si el móvil está configurado para mostrar sitios de escritorio, aparecen los enlaces a las dos tiendas. En un ordenador, aparece un código QR para escanear con el móvil y enlaces a las dos tiendas.

En cualquier móvil, [themachine.computer/app](https://themachine.computer/app) abre la tienda adecuada. **Ajustes**, **Apps** muestra las dos tiendas arriba o solo la tienda de tu móvil si estás usando uno. En un ordenador, también muestra la app de escritorio para Windows, Mac y Linux: consulta [La app de escritorio](desktop-app.md).

## Conéctala

En una Machine alojada, la app inicia sesión con tu cuenta. Si la Machine está alojada por tu cuenta, abre **Ajustes**, **Apps** en un ordenador: debajo de las tiendas, **¿No estás en la Network?** muestra un código. Instala la app y escanea el código con la cámara del móvil, o escribe en la app la dirección que aparece debajo. La app te pregunta antes de conectarse y se sigue aplicando el inicio de sesión propio de tu Machine.

**Iniciar sesión con** un servicio en **Conexiones** (Shortcut, Notion, Slack, Zoom y otros) abre la pantalla de inicio de sesión de tu móvil. Cuando terminas, vuelves a la app y la nueva conexión aparece automáticamente en **Conexiones**.

Si la app no puede conectarse a tu Machine, te lo indica e intenta conectarse de nuevo automáticamente. En un Mac, la app también vuelve a abrir la página automáticamente si la ventana aparece en blanco al salir del reposo, y recupera el mensaje de chat que estabas escribiendo. En un Mac o iPad con teclado, Cmd+R vuelve a cargar la página.

## Notificaciones

La primera vez que se abre, la app te pide permiso para enviar notificaciones. Toca una para abrir lo que indica: una tarea aparece resaltada en tu lista, el resumen de la mañana abre hoy en **Calendario**, el resumen del equipo abre Tareas y una pregunta del Fleet abre su tarea. El texto de una tarea nunca pasa por Apple, Google ni el servicio de The Machine: solo transmiten una frase fija, como «Una tarea te necesita».

Después, la app le pide a tu propia Machine el título y el siguiente paso de la tarea, como «Responder a Sam» y «Enviar a Sam: el martes a las 10:00 me va bien». El resumen de la mañana incluye lo que tienes pendiente y la hora de tu primera reunión; el resumen del equipo, sus primeros elementos; y una actualización del Fleet, lo que ha ocurrido. Si no puede conectarse a tu Machine, se mantiene la frase fija. En Android, indica cuántas tareas tienes pendientes, como «Tienes 2 tareas pendientes».

Una notificación incluye **Posponer** (hasta mañana) y **Marcar como hecho**, además de **Hazlo** para una tarea que aún no has empezado. Estas opciones funcionan después de desbloquear el móvil, sin abrir la app. Para enviar algo o completar los pasos finales, siempre se abre la app. Hay una notificación por tarea: «Preparando» cambia a «Para revisar» y desaparece cuando la tarea se completa o se pospone, desde aquí o desde cualquier otro sitio.

Cuando se completa un paso que has confirmado, su notificación muestra **Hecho** y lo que ha ocurrido, hasta que toques **Entendido** en Tareas. En iPhone, puedes hacerlo la próxima vez que abras la app.

Si desactivas **Texto en las notificaciones** en **Ajustes**, **Seguridad**, se mantiene la frase fija. Lo mismo ocurre si la pantalla bloqueada oculta el contenido de las notificaciones. Si no puede mostrar nada, indica «Toca para abrir». Si el móvil no puede conectarse a tu Machine cuando llega una notificación, muestra los detalles en cuanto vuelve a estar conectado.

Se aplican las mismas reglas que a las notificaciones push en la web: lo que hayas elegido para cada tipo en [Notificaciones](notifications.md), tu [horario laboral](work-hours.md) y ninguna notificación mientras estés usando un panel.

Cada móvil con la app aparece en **Ajustes**, **Notificaciones** como **Teléfono con la app**. **Quitar** desactiva sus notificaciones. Para recibirlas en una Machine alojada por tu cuenta, hace falta The Machine Network; la app funciona sin ellas.

## Comparte con The Machine

En cualquier app, toca Compartir y elige The Machine. Se abre una **Nueva tarea** con el texto, el enlace o los archivos que hayas compartido. Revísala, añade una fecha si quieres y guárdala. No se añade nada hasta que lo hagas.

También basta con compartir un archivo, como una factura o una carta. Tu Machine lee el texto de un PDF y completa la tarea con lo que es, el siguiente paso y la fecha. El archivo se envía directamente a tu Machine y se queda allí.

El panel instalado como app en Android también permite compartir contenido: selecciónalo en el menú para compartir, igual que las demás apps.

Los planes y la facturación no aparecen en la app. **Abrir cuenta** sigue estando en **Ajustes**, para que puedas eliminar tu cuenta.
