---
title: La app móvil
area: getting-started
summary: Usa The Machine como app en iPhone y Android: recibe notificaciones de tus tareas y comparte contenido con The Machine desde cualquier app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 3865fe910a5427fb
---
La app móvil abre tu propio panel con la sesión iniciada, igual que en la web. Descárgala en el [App Store](https://apps.apple.com/app/id6829875215) para iPhone y iPad, o en [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

La tarea **Saca más partido a The Machine**, que aparece arriba de Tareas, te recomienda instalarla. En el navegador del teléfono, **Obtener** abre la tienda. Si el teléfono está configurado para mostrar sitios de escritorio, aparecen los enlaces a ambas tiendas. En un ordenador, aparece un código QR para escanear con el teléfono y enlaces a las dos tiendas.

En cualquier teléfono, [themachine.computer/app](https://themachine.computer/app) abre la tienda correspondiente. En **Ajustes**, **Apps**, aparecen las dos tiendas arriba, o solo la tienda de tu teléfono si estás en uno. En un ordenador, **Ordenador** instala el panel como app: consulta [Instalar la app](phone-app.md).

## Conectarla

En una Machine alojada, la app inicia sesión con tu cuenta. En una Machine autoalojada, abre **Ajustes** y **Apps** desde un ordenador: debajo de las tiendas, **¿No estás en la Network?** muestra un código. Instala la app y escanéalo con la cámara del teléfono, o escribe en la app la dirección que aparece debajo. La app te pregunta antes de conectarse y sigue siendo necesario iniciar sesión en tu Machine.

## Notificaciones

La app te pide permiso para enviar notificaciones la primera vez que la abres. Toca una notificación para abrir lo que indica: una tarea abre su chat, la notificación de la mañana abre el día de hoy en **Calendario**, el resumen del equipo abre Tareas y una pregunta de Fleet abre su tarea. Ningún texto de una tarea pasa por Apple, Google ni los servicios de The Machine: solo transmiten un mensaje fijo, como «Una tarea te necesita».

Después, la app le pide a tu Machine el título de la tarea y el siguiente paso, por ejemplo, «Responder a Sam» con «Enviar a Sam: el martes a las 10:00 me va bien». La notificación de la mañana incluye lo que tienes pendiente y la hora de tu primera reunión; el resumen del equipo, sus primeros elementos; y una actualización de Fleet, lo que ha ocurrido. Si no puede conectarse a tu Machine, se mantiene el mensaje fijo. En Android, indica cuántas tareas tienes pendientes, por ejemplo, «Tienes 2 tareas pendientes».

Una notificación incluye **Posponer** (hasta mañana) y **Marcar como hecha**, además de **Hazlo** si aún no has empezado la tarea. Estas opciones funcionan cuando desbloqueas el teléfono, sin abrir la app. Para enviar algo y completar los pasos finales, siempre se abre la app. Hay una notificación por tarea: «Preparando» pasa a «Para revisar» y desaparece cuando la tarea se completa o se pospone, desde aquí o desde cualquier otro sitio.

Cuando se completa un paso que confirmaste, su notificación muestra **Hecho** y lo que ha ocurrido, hasta que toques **Entendido** en Tareas. En iPhone, puedes hacerlo la próxima vez que abras la app.

Si desactivas **Texto en las notificaciones** en **Ajustes**, **Seguridad**, se mantiene el mensaje fijo. Lo mismo ocurre si la pantalla de bloqueo oculta el contenido de las notificaciones. Si no hay nada que pueda mostrar, dice «Toca para abrir». Si el teléfono no puede conectarse a tu Machine cuando llega una notificación, muestra los detalles cuando vuelve a estar conectado.

Las notificaciones siguen las mismas reglas que las notificaciones push en la web: lo que hayas elegido para cada tipo en [Notificaciones](notifications.md), tu [horario laboral](work-hours.md) y que no se envían mientras estás usando un panel.

Cada teléfono con la app aparece en **Ajustes**, **Notificaciones**, como **Teléfono con la app**. **Quitar** desactiva sus notificaciones. Para recibirlas, una Machine autoalojada necesita The Machine Network. La app funciona sin ellas.

## Compartir con The Machine

En cualquier app, toca Compartir y elige The Machine. Se abre una **Nueva tarea** con el texto, el enlace o los archivos que hayas compartido. Revísala, añade una fecha si quieres y agrégala. No se añade nada hasta que lo hagas.

También puedes compartir solo un archivo, como una factura o una carta. Tu Machine lee el texto de un PDF y completa la tarea: qué es, el siguiente paso y su fecha. El archivo se envía directamente a tu Machine y se queda allí.

El panel instalado como app en Android también puede recibir contenido compartido: solo tienes que elegirlo en el menú para compartir.

Los planes y la facturación no aparecen en la app. **Abrir cuenta** sigue disponible en **Ajustes** para eliminar tu cuenta.
