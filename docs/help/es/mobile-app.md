---
title: La app móvil
area: getting-started
summary: The Machine como app en iPhone y Android: notificaciones de tus tareas y la opción de compartir contenido con The Machine desde cualquier app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: f622bdc266f69965
---
La app móvil abre tu propio panel, con la misma sesión que en la web. Descárgala desde [App Store](https://apps.apple.com/app/id6829875215) para iPhone y iPad, o desde [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) para Android.

La tarea **Saca más partido a The Machine**, en la parte superior de Tareas, te la recomienda. En el navegador de un teléfono, **Obtener** abre la tienda. En un teléfono configurado para mostrar sitios de escritorio, aparecen los enlaces a las dos tiendas. En un ordenador, aparece un código QR para escanear con el teléfono y enlaces a las dos tiendas.

En cualquier teléfono, [themachine.computer/app](https://themachine.computer/app) abre la tienda adecuada. En **Ajustes**, **Apps**, aparecen las dos tiendas arriba o, si estás en un teléfono, solo la de ese teléfono. En un ordenador, **Ordenador** instala el panel como una app: consulta [Instalar la app](phone-app.md).

## Conéctala

En una Machine alojada, la app inicia sesión con tu cuenta. En una Machine autoalojada, abre **Ajustes**, **Apps** en un ordenador: debajo de las tiendas, **¿No estás en la Network?** muestra un código. Instala la app y escanéalo con la cámara del teléfono, o escribe en la app la dirección que aparece debajo. La app te pregunta antes de conectarse y sigue siendo necesario iniciar sesión en tu Machine.

Al tocar **Iniciar sesión con** un servicio en **Conexiones** (Shortcut, Notion, Slack, Zoom y otros), se abre la pantalla de inicio de sesión del teléfono. Cuando termines, volverás a la app y la nueva conexión aparecerá automáticamente en **Conexiones**.

## Notificaciones

La app te pide permiso para enviarte notificaciones la primera vez que la abres. Toca una para ver de qué se trata: una tarea aparece resaltada en tu lista, el resumen de la mañana abre el día de hoy en **Calendario**, el informe del equipo abre Tareas y una pregunta de Fleet abre su tarea. Apple, Google y el servicio de The Machine no reciben el texto de ninguna tarea: solo transmiten un mensaje fijo, como «Tienes una tarea pendiente».

A continuación, la app le pide a tu Machine el título de la tarea y el siguiente paso, por ejemplo, «Responder a Sam» y «Enviar a Sam: el martes a las 10:00 me va bien». El resumen de la mañana incluye lo que tienes pendiente y la hora de tu primera reunión; el informe del equipo, sus primeros elementos; y una actualización de Fleet, lo que ha ocurrido. Si no puede conectarse a tu Machine, se queda el mensaje fijo. En Android, indica cuántas tareas tienes pendientes, por ejemplo, «Tienes 2 tareas pendientes».

Una notificación incluye **Posponer** (hasta mañana) y **Marcar como hecha**, además de **Hazlo** para una tarea que aún no has empezado. Estas opciones funcionan después de desbloquear el teléfono, sin abrir la app. Enviar y completar los pasos finales siempre abre la app. Hay una notificación por tarea: «Preparando» pasa a «Lista» y desaparece cuando la tarea se completa o se pospone, desde aquí o desde cualquier otro lugar.

Cuando se completa un paso que confirmaste, su notificación indica **Hecho** y explica lo ocurrido, hasta que toques **Entendido** en Tareas. En iPhone, puede esperar hasta la próxima vez que abras la app.

Si desactivas **Texto en las notificaciones** en **Ajustes**, **Seguridad**, se mantiene el mensaje fijo. Lo mismo ocurre si la pantalla de bloqueo oculta el contenido de las notificaciones. Si no hay nada que mostrar, aparece «Toca para abrir». Si el teléfono no puede conectarse a tu Machine cuando llega una notificación, mostrará los detalles cuando vuelva a estar conectado.

Siguen las mismas reglas que las notificaciones push de la web: lo que hayas elegido para cada tipo en [Notificaciones](notifications.md), tu [horario laboral](work-hours.md) y ninguna notificación mientras estés usando un panel.

Cada teléfono con la app aparece en **Ajustes**, **Notificaciones** como **Teléfono con la app**. **Quitar** detiene sus notificaciones. Para recibirlas, una Machine autoalojada necesita The Machine Network; la app funciona sin ellas.

## Compartir con The Machine

En cualquier app, toca Compartir y elige The Machine. Se abre **Nueva tarea** con el texto, el enlace o los archivos que hayas compartido. Revísala, añade una fecha si quieres y agrégala. No se añade nada hasta que lo hagas.

También puedes compartir solo un archivo, como una factura o una carta. Tu Machine lee el texto de los PDF y completa la tarea con lo que es, el siguiente paso y la fecha. El archivo va directamente a tu Machine y se queda ahí.

El panel instalado como app en Android también recibe contenido compartido: selecciónalo en el menú para compartir, igual que cualquier otra app.

Los planes y la facturación no aparecen en la app. **Abrir cuenta** sigue estando disponible en **Ajustes** para que puedas eliminar tu cuenta.
