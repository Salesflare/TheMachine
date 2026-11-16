---
title: La app móvil
area: getting-started
summary: The Machine como app en iPhone y Android: notificaciones de tus tareas y opción de compartir contenido con The Machine desde cualquier app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 0d4d41134db91fcc
---
La app móvil abre tu propio panel, con la misma sesión que en la web. Descárgala en el [App Store](https://apps.apple.com/app/id6829875215) para iPhone y iPad, o en [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

La tarea **Saca más partido a The Machine**, que aparece en la parte superior de Tareas, te recomienda instalarla. En el navegador del teléfono, **Obtener** abre la tienda. Si el teléfono está configurado para mostrar sitios de escritorio, aparecen los enlaces a las dos tiendas. En un ordenador aparece un código QR para escanear con el teléfono y los enlaces a las dos tiendas.

En cualquier teléfono, [themachine.computer/app](https://themachine.computer/app) abre la tienda adecuada. En **Ajustes**, **Apps**, aparecen las dos tiendas en la parte superior, o solo la tienda del teléfono si estás usando uno. En un ordenador, **Ordenador** instala el panel como app: consulta [Instalar la app](phone-app.md).

## Conectarla

En una Machine alojada, la app inicia sesión con tu cuenta. En una Machine autoalojada, abre **Ajustes**, **Apps** en un ordenador. Debajo de las tiendas, **¿No estás en la Network?** muestra un código. Instala la app y escanea el código con la cámara del teléfono, o escribe en la app la dirección que aparece debajo. La app te pregunta antes de conectarse y sigue siendo necesario iniciar sesión en tu Machine.

## Notificaciones

La primera vez que se abre, la app te pide permiso para enviar notificaciones. Toca una para abrir el contenido al que hace referencia: una tarea aparece resaltada en tu lista; la notificación de la mañana abre hoy en el **Calendario**; el resumen del equipo abre Tareas, y una pregunta de Fleet abre su tarea. El texto de las tareas no pasa por Apple, Google ni el servicio de The Machine: solo transmiten un mensaje fijo, como «Hay una tarea que necesita tu atención».

Después, la app le pide a tu Machine el título de la tarea y el siguiente paso, por ejemplo, «Responder a Sam» y «Enviar a Sam: el martes a las 10:00 me va bien». La notificación de la mañana incluye lo que tienes pendiente y la hora de tu primera reunión; el resumen del equipo, sus primeros elementos; y una actualización de Fleet, lo que ha ocurrido. Si no puede conectarse a tu Machine, se mantiene el mensaje fijo. En Android indica cuántas tareas tienes pendientes, por ejemplo, «Tienes 2 tareas pendientes».

Las notificaciones incluyen **Posponer** (hasta mañana) y **Marcar como hecha**, y **Hazlo** si aún no has empezado la tarea. Estas opciones funcionan después de desbloquear el teléfono, sin abrir la app. Para enviar algo y completar los pasos finales siempre hay que abrirla. Hay una notificación por tarea: «Preparando» cambia a «Para revisar» y desaparece cuando la tarea se completa o se pospone, desde aquí o desde cualquier otro sitio.

Cuando se completa un paso que confirmaste, la notificación muestra **Hecho** y lo que ha ocurrido, hasta que toques **Entendido** en Tareas. En iPhone, puedes hacerlo la próxima vez que abras la app.

Si desactivas **Texto en las notificaciones** en **Ajustes**, **Seguridad**, se mantiene el mensaje fijo. Lo mismo ocurre si la pantalla bloqueada oculta el contenido de las notificaciones. Si no hay nada que pueda mostrar, aparece «Toca para abrir». Si el teléfono no puede conectarse a tu Machine cuando llega una notificación, muestra los detalles cuando vuelva a estar conectado.

Se aplican las mismas reglas que a las notificaciones push en la web: lo que hayas elegido para cada tipo en [Notificaciones](notifications.md), tu [horario laboral](work-hours.md) y ninguna notificación mientras usas un panel.

Cada teléfono con la app aparece en **Ajustes**, **Notificaciones** como **Teléfono con la app**. **Quitar** deja de enviar notificaciones a ese teléfono. Una Machine autoalojada necesita The Machine Network para enviarlas; la app funciona sin ellas.

## Compartir con The Machine

En cualquier app, toca Compartir y elige The Machine. Se abre una **Nueva tarea** con el texto, el enlace o los archivos que hayas compartido. Revísala, añade una fecha si quieres y guárdala. No se añade nada hasta que lo hagas.

También puedes compartir solo un archivo, como una factura o una carta. Tu Machine lee el texto de los PDF y completa la tarea: qué es, cuál es el siguiente paso y la fecha. El archivo se envía directamente a tu Machine y se queda allí.

En Android, también puedes compartir contenido con el panel instalado como app: selecciónalo en la hoja para compartir, igual que cualquier otra app.

Los planes y la facturación no aparecen en la app. **Abrir cuenta** sigue estando disponible en **Ajustes** para eliminar tu cuenta.
