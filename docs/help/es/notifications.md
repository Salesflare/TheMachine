---
title: Notificaciones
area: settings
summary: Qué te llega, dónde y cuándo: solo te avisa lo que no puede esperar; el resto va en un único resumen matutino.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3c469ec1032f6bea
---
¿Quieres menos notificaciones o recibir otras? En **Ajustes**, **Notificaciones**, elige dónde quieres recibir cada tipo:

- **Tareas nuevas**: solo lo que no puede esperar, como algo que vence hoy o es urgente.
- **Resultados y preguntas**: una respuesta lista para enviar, una tarea que necesita que inicies sesión o una pregunta del Fleet.
- **Recordatorios**: tareas pospuestas y respuestas que estás esperando y vuelven a estar pendientes.
- **Resumen matutino**: un resumen breve de tu día. Más abajo tienes más información.
- **Resumen de la tarde**: lo que has hecho hoy y lo que queda pendiente para mañana. Más abajo tienes más información.

Cada tipo tiene un interruptor para **Push** (la app del móvil o del ordenador), **Telegram** cuando lo hayas configurado y **Correo** en una Machine alojada o en The Machine Network. Todo está activado, excepto los resúmenes en Telegram.

En la misma pestaña puedes configurar tu **Horario laboral**: los días laborables, cuándo pueden llegarte notificaciones, cuándo vuelven las tareas pospuestas, la hora de los resúmenes y tu zona horaria. Consulta [Horario laboral](work-hours.md).

## Solo lo que no puede esperar

Solo recibirás una notificación push, un aviso de Telegram o un correo por estos motivos:

- una tarea que vence hoy o está marcada como urgente;
- una respuesta que alguien está esperando, con un borrador listo para enviar;
- una tarea que necesita que inicies sesión;
- una tarea pospuesta que vuelve a la hora que elegiste.

Todo lo demás aparece discretamente en el panel (y sin sonido en Telegram) y espera al resumen matutino. En un día libre, solo recibirás avisos de lo urgente o de lo que vence hoy. Como máximo, recibirás 8 notificaciones push al día. Si pasan 3 días sin que abras el panel, solo recibirás el resumen matutino hasta que vuelvas.

## Cuándo te avisa

Comprueba si estás usando el panel, no solo si está abierto:

- Si lo estás usando (está en primer plano y has hecho clic, escrito o desplazado la página en los últimos 10 minutos), no te avisa. Los mensajes de Telegram llegan sin sonido. Abrir o recargar el panel no cuenta.
- Si no estás (está en segundo plano, cerrado o llevas 10 minutos sin actividad), recibirás una notificación push un minuto después de salir, a menos que vuelvas y la veas.
- Si 15 minutos después aún no te ha llegado nada y no puede esperar, recibirás un correo al respecto, como máximo uno por hora. Se omite lo que ya hayas visto o gestionado, y cada tarea aparece una sola vez, con su estado actual. La mayoría de los días, el resumen matutino es el único correo.
- Se considera que te ha llegado una notificación si aparece en el móvil o en el navegador, o si Telegram recibe el mensaje. No cuenta si el móvil está apagado, sin conexión o con las notificaciones desactivadas. Tampoco cuenta Telegram mientras usas el panel. Si solo aparece en un ordenador, recibirás igualmente un correo por lo urgente o lo que vence hoy, porque quizá no estés delante.
- Si no tienes la app para el móvil, las notificaciones del navegador ni Telegram, recibirás un correo por todo lo anterior.
- Si no se puede contactar contigo por Telegram, la notificación push se envía igualmente, una sola vez, y Telegram vuelve a intentarlo automáticamente.
- Si alguien del equipo te asigna una tarea y tu Machine no puede avisarte por el móvil ni por Telegram, recibirás un correo con su título y un enlace 15 minutos después, si aún no la has visto. Desactiva **Correo** en **Resultados y preguntas** para evitarlo.
- Fuera de tu horario laboral, no te llega nada. El resumen matutino incluirá esas tareas.
- Si recibes una tarea nueva de trabajo en un día libre, esperará hasta la hora del resumen del siguiente día laborable. La tarea indica cuándo te llegará, por ejemplo: Notificación lun, 2 nov · 08:30.

Los cambios y el progreso no generan notificaciones. Si aparece un resultado más reciente en una tarea que aún no has visto, se actualiza sin enviarte otra notificación. Si se producen varios avisos seguidos, recibirás una sola notificación. El icono de la app muestra cuántas tareas requieren tu atención.

## Botones de las notificaciones

Cada notificación tiene botones para dar el siguiente paso. En la app para el móvil:

- Tarea nueva: **Hazlo**, **Posponer**, **Marcar como hecho**.
- Borrador listo: **Abrir borrador**, **Posponer**, **Marcar como hecho**.
- Resultado listo: **Abrir**, **Marcar como hecho**, **Posponer**.
- Si necesita una respuesta, está bloqueada o requiere que inicies sesión: **Responder**, **Abrir** o **Iniciar sesión**; después, **Posponer** y **Marcar como hecho**.
- Recordatorio: **Marcar como hecho**, **Posponer**, **Abrir**.
- Resumen matutino: tócalo para abrirlo.

En el navegador y en Telegram aparecen dos de esos botones. Las preguntas del Fleet siempre incluyen **Responder** y **Rechazar**.

No se envía, paga ni presenta nada desde una notificación. Los borradores siempre se abren primero para que los veas antes de enviarlos. **Abrir borrador** muestra la tarea en tu lista y el borrador completo. **Hazlo** solo inicia el trabajo en una tarea nueva.

En la app para el móvil, primero tendrás que desbloquearla para usar **Posponer** o **Marcar como hecho**. En el navegador, se abre el panel, donde se realiza la acción y aparece la opción para deshacerla. **Posponer** hace que la tarea vuelva dentro de dos horas, o mañana por la mañana si es un recordatorio.

Los correos incluyen enlaces para abrir las tareas y posponer las que están pendientes. Solo abren el panel.

Si tocas una notificación o eliges **Abrir** en un correo o en Telegram, la tarea aparece resaltada en tu lista, dondequiera que esté en ese momento: **Recién hecho**, **Hecho**, **Vuelve más tarde** u otra vista. Nunca se abre el chat. Si la página aún no se había actualizado, te lleva a la tarea cuando lo haga.

## El resumen matutino

Llega los días laborables a la hora de **Resumen matutino**, a menos que no haya nada que contar. Si esa hora es anterior a **Lo pospuesto vuelve a las**, espera hasta 5 minutos después para incluir las tareas que vuelven a estar pendientes esa mañana. **Vista previa** te permite verlo sin enviarlo. De forma predeterminada, llega como notificación push y correo, y es lo bastante breve para leerlo de un vistazo:

- un saludo con lo más importante del día, como «Buenos días, Sam. Hay 2 respuestas listas para enviar» o, si hay una sola tarea, «Buenos días, Sam. Falta tu visto bueno: Envía el formulario del pedido». Solo cuentan como listas las tareas con un borrador o un resultado que aprobar; no cuentan las que primero necesitan una respuesta tuya;
- las tareas que se mencionan en el saludo, cada una con un enlace para abrirla, y lo que vence hoy; si no hay nada de eso, como máximo tres tareas por hacer;
- hasta cinco tareas que hayas añadido y estén pendientes de ti, independientemente de lo que cuente el saludo;
- cuántas tareas más pueden esperar y cuánto tardarás en ponerte al día a tu ritmo, por ejemplo: «Pueden esperar 12 más. Tardarás unos 5 min en ponerte al día». El tiempo no incluye las tareas que esperan una respuesta tuya. Tampoco se cuenta una tarea que vence hoy pero está pospuesta hasta más tarde, ni una en la que The Machine sigue trabajando, hasta que vuelva a depender de ti. El número coincide con las tareas pendientes en tu lista.
- tus reuniones, en una sola línea.

**Abrir** muestra la tarea resaltada en tu lista, aunque esté hecha o pospuesta. Una promesa abre su tarea o, si aún no tiene ninguna, su propia página.

La notificación push incluye el mismo contenido, pero sin enlaces. Tócala o usa el enlace al final del correo para volver a leer el resumen en **Tareas**.

## El resumen de la tarde

Llega una vez los días laborables, a la hora configurada en **Horario laboral**. De forma predeterminada, llega 15 minutos antes de **Hasta**, por los medios que hayas elegido en su fila. Solo lo recibirás los días que hayas estado activo: si has usado el panel o has tomado una decisión sobre una tarea en el panel, en Telegram, en el chat o por voz. Si no has completado ninguna tarea ni has asistido a ninguna reunión, no recibirás el resumen.

Empieza con un recuento del día, como «Buenas tardes, Sam. Hoy has completado 4 tareas», seguido de una sección de **Trabajo** y otra de **Personal**. Si una sección está vacía, no aparece. Las alertas sobre tu Machine no aparecen en ninguna de las dos. Cada sección incluye:

- **Hecho hoy**: hasta tres tareas que hayas completado tú o tu Machine, seguidas de «+12 más» y las reuniones del día, como «+3 reuniones: llamada sobre precios y 2 más»;
- **Pendiente para mañana** (o para el siguiente día laborable si es viernes): las primeras reuniones y lo que vence.

Al final, indica cuántas tareas siguen necesitando tu atención. Toca la notificación push o el enlace al final del correo para volver a leerlo, con las opciones **Copiar Trabajo** y **Copiar Personal**. Para dejar de recibirlo, desactiva su fila.

## Privacidad

Las notificaciones push van directamente de tu Machine a tu dispositivo, cifradas para ese dispositivo. El correo pasa por el servidor de correo de The Machine y por tu proveedor de correo. Cuando [Precavido](security-levels.md) oculta el texto de las tareas en las notificaciones, los correos solo incluyen cantidades. Desactiva **Correo** para un tipo de notificación si no quieres recibirlo por correo.

Activa las notificaciones push de un dispositivo en **Este dispositivo** o consulta [Instalar la app](phone-app.md). La [app móvil](mobile-app.md) envía una línea de texto sin formato a través de Apple o Google y luego le pide a tu Machine el título y el siguiente paso.
